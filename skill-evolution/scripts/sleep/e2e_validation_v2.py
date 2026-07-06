#!/usr/bin/env python3
"""E2E Sleep-Cycle Validation v2 — Dual-Model Strategy.

Uses glm-4-flash (weak) for attempt/replay, and glm-4.6 (strong) for reflect.

Validates three improvements jointly:
  1. Prompt-pollution filter (_is_self_referential) — harvested tasks should
     NOT contain "# Skill Instructions" pollution.
  2. Exit-code judging — binary 0/1 signal, more discriminative than outcome.
  3. Strong reflect model (glm-4.6) — should produce more concrete rules than
     the weak model's 0-edit result in the previous round.

Pipeline:
  Phase 1 — harvest + mine (max_tasks=10), print each task's intent (first 80 chars)
  Phase 2 — baseline replay on val set (glm-4-flash), print per-task details
  Phase 3 — train replay + reflect (reflect uses glm-4.6), print proposed edits
  Phase 4 — if edits exist, gate validation

Output: stdout + data/e2e_validation_v2_report.md

Usage:
    cd scripts && PYTHONPATH=. python3.12 sleep/e2e_validation_v2.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── sys.path bootstrap ───────────────────────────────────────────────────────
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from sleep.harvest import harvest, _iter_jsonl  # noqa: E402
from sleep.mine import mine  # noqa: E402
from sleep.models import SessionDigest, TaskRecord, ReplayResult, EditRecord  # noqa: E402
from sleep.cc_backend import CCBackend  # noqa: E402
from sleep.replay import replay_batch, aggregate_scores  # noqa: E402
from sleep.gate import evaluate_gate, select_gate_score  # noqa: E402
from sleep.memory import apply_edits  # noqa: E402

# ── Configuration ────────────────────────────────────────────────────────────

CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
ATTEMPT_MODEL = "glm-4-flash"   # weak model — makes mistakes in replay
REFLECT_MODEL = "glm-4.6"       # strong model — analyzes failures
TIMEOUT = 45                    # per-task timeout (seconds)
MAX_TASKS = 10                  # control scale and total time
EDIT_BUDGET = 4
REPORT_PATH = str(Path(_SCRIPTS_DIR).parent / "data" / "e2e_validation_v2_report.md")

BASELINE_SKILL = "# Skill\nNo instructions yet."
BASELINE_MEMORY = ""

# Markers to check for prompt pollution
_POLLUTION_MARKERS = (
    "# Skill Instructions",
    "evolving-skills",
    "EVOLVING-SKILLS",
    "sleep cycle",
    "sleep_cycle",
    "e2e_validation",
    "analyze_real",
    "BEGIN AGENT-EXPERIENCE",
)

# ── Helpers ──────────────────────────────────────────────────────────────────

_report_lines: List[str] = []


def _log(msg: str = "") -> None:
    """Print to stdout and buffer for report."""
    print(msg)
    _report_lines.append(msg)


def _sep(char: str = "=", width: int = 72) -> None:
    _log(char * width)


def _section(title: str) -> None:
    _log("")
    _sep("=")
    _log(f"  {title}")
    _sep("=")


def _check_pollution(text: str) -> List[str]:
    """Return list of pollution markers found in text."""
    found = []
    for marker in _POLLUTION_MARKERS:
        if marker in text:
            found.append(marker)
    return found


def _print_task_details(pairs: List[Tuple[TaskRecord, ReplayResult]], label: str) -> None:
    """Print per-task judging details: intent, hard, soft, rationale."""
    _log(f"\n--- {label} Per-Task Details ---")
    for i, (task, result) in enumerate(pairs, 1):
        intent_preview = task.intent[:80].replace("\n", " ")
        pollution = _check_pollution(task.intent)
        pollution_tag = f"  ⚠ POLLUTED: {pollution}" if pollution else ""
        _log(
            f"  [{i:2d}] intent={intent_preview!r}{pollution_tag}\n"
            f"       hard={result.hard:.2f}  soft={result.soft:.2f}  "
            f"latency={result.latency_ms:.0f}ms  "
            f"exit_code={task.exit_code}  outcome={task.outcome}\n"
            f"       rationale: {result.judge_rationale}\n"
            f"       response:  {result.response[:120]!r}"
        )


# ── Phase 1: harvest + mine + pollution check ────────────────────────────────


def extract_exit_codes(
    tasks: List[TaskRecord],
    digests: List[SessionDigest],
) -> Dict[str, Any]:
    """Scan transcripts for Bash tool_result is_error signals."""
    sid_to_path: Dict[str, str] = {}
    for d in digests:
        if d.raw_path and os.path.isfile(d.raw_path):
            sid_to_path[d.session_id] = d.raw_path

    total_bash = 0
    bash_with_signal = 0
    bash_success = 0
    bash_error = 0
    tasks_with_exit = 0
    tasks_without_transcript = 0

    for task in tasks:
        transcript_path = None
        for sid in task.source_sessions:
            if sid in sid_to_path:
                transcript_path = sid_to_path[sid]
                break

        if transcript_path is None:
            tasks_without_transcript += 1
            continue

        tool_name_map: Dict[str, str] = {}
        for rec in _iter_jsonl(transcript_path):
            msg = rec.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("id"):
                    tool_name_map[b["id"]] = b.get("name", "")

        has_any_error = False
        has_any_success = False
        bash_results_in_session: List[bool] = []
        for rec in _iter_jsonl(transcript_path):
            msg = rec.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") != "tool_result":
                    continue
                tuid = b.get("tool_use_id", "")
                tname = tool_name_map.get(tuid, "")
                if tname != "Bash":
                    continue
                total_bash += 1
                is_error = b.get("is_error")
                if isinstance(is_error, bool):
                    bash_with_signal += 1
                    bash_results_in_session.append(is_error)
                    if is_error:
                        bash_error += 1
                        has_any_error = True
                    else:
                        bash_success += 1
                        has_any_success = True

        if bash_results_in_session:
            task.exit_code = 1 if has_any_error else 0
            task.reference_kind = "exit_code"
            tasks_with_exit += 1

    return {
        "total_bash_calls": total_bash,
        "bash_with_signal": bash_with_signal,
        "bash_success": bash_success,
        "bash_error": bash_error,
        "tasks_with_exit_code": tasks_with_exit,
        "tasks_without_transcript": tasks_without_transcript,
        "total_tasks": len(tasks),
    }


# ── Phase 2: Baseline replay ─────────────────────────────────────────────────


def run_baseline(
    backend: CCBackend,
    val_tasks: List[TaskRecord],
    skill: str,
    memory: str,
) -> List[Tuple[TaskRecord, ReplayResult]]:
    _log("\nRunning baseline replay on val set...")
    pairs = replay_batch(backend, val_tasks, skill, memory)
    hard, soft = aggregate_scores(pairs)
    _log(f"  Baseline — hard={hard:.3f}  soft={soft:.3f}  (n={len(pairs)})")
    _print_task_details(pairs, "Baseline")
    return pairs


# ── Phase 3: Reflect ─────────────────────────────────────────────────────────


def run_reflect(
    backend: CCBackend,
    train_tasks: List[TaskRecord],
    skill: str,
    memory: str,
) -> Tuple[
    List[Tuple[TaskRecord, ReplayResult]],
    List[EditRecord],
    List[Tuple[TaskRecord, ReplayResult]],
    List[Tuple[TaskRecord, ReplayResult]],
]:
    _log("\nRunning train-set replay for reflect...")
    train_pairs = replay_batch(backend, train_tasks, skill, memory)
    thard, tsoft = aggregate_scores(train_pairs)
    _log(f"  Train — hard={thard:.3f}  soft={tsoft:.3f}  (n={len(train_pairs)})")
    _print_task_details(train_pairs, "Train")

    failures = [(t, r) for t, r in train_pairs if r.hard < 1.0]
    successes = [(t, r) for t, r in train_pairs if r.hard >= 1.0]
    _log(f"\n  Failures (hard < 1.0): {len(failures)}")
    _log(f"  Successes (hard >= 1.0): {len(successes)}")

    if not failures:
        _log("\n  No failures → nothing to reflect on.")
        return train_pairs, [], failures, successes

    _log(f"\n  Calling backend.reflect() (model={REFLECT_MODEL}, timeout={TIMEOUT}s)...")
    t0 = time.time()
    try:
        edits = backend.reflect(
            failures, successes, skill, memory, edit_budget=EDIT_BUDGET,
        )
    except Exception as e:
        _log(f"  [ERROR] reflect() raised: {e}")
        edits = []
    elapsed = time.time() - t0
    _log(f"  reflect() returned {len(edits)} edits in {elapsed:.1f}s")

    _log("\n--- Proposed Edits ---")
    for i, e in enumerate(edits, 1):
        _log(
            f"  [{i}] target={e.target}  op={e.op}\n"
            f"      content:   {e.content}\n"
            f"      rationale: {e.rationale}"
        )

    if not edits:
        _log("\n  (No edits proposed — reflect returned empty)")

    return train_pairs, edits, failures, successes


# ── Phase 4: Gate ────────────────────────────────────────────────────────────


_val_pairs_cache: List[Tuple[TaskRecord, ReplayResult]] = []


def run_gate(
    backend: CCBackend,
    val_tasks: List[TaskRecord],
    skill: str,
    memory: str,
    edits: List[EditRecord],
    baseline_hard: float,
    baseline_soft: float,
) -> None:
    if not edits:
        _log("\n  No edits to gate — skipping Phase 4.")
        return

    skill_edits = [e for e in edits if e.target == "skill"]
    memory_edits = [e for e in edits if e.target == "memory"]

    cand_skill = skill
    cand_memory = memory
    applied: List[EditRecord] = []

    if skill_edits:
        new_skill, app_s = apply_edits(cand_skill, skill_edits)
        cand_skill = new_skill
        applied.extend(app_s)
        _log(f"\n  Applied {len(app_s)}/{len(skill_edits)} skill edits")

    if memory_edits:
        new_mem, app_m = apply_edits(cand_memory, memory_edits)
        cand_memory = new_mem
        applied.extend(app_m)
        _log(f"  Applied {len(app_m)}/{len(memory_edits)} memory edits")

    if not applied:
        _log("\n  No edits were actually applied (all duplicates/no-ops) — skipping gate.")
        return

    _log(f"\n  Candidate skill (first 500 chars):\n  {cand_skill[:500]}")

    _log("\n  Replaying val set with candidate skill...")
    cand_pairs = replay_batch(backend, val_tasks, cand_skill, cand_memory)
    cand_hard, cand_soft = aggregate_scores(cand_pairs)
    _log(f"  Candidate — hard={cand_hard:.3f}  soft={cand_soft:.3f}  (n={len(cand_pairs)})")
    _print_task_details(cand_pairs, "Candidate")

    base_score = select_gate_score(baseline_hard, baseline_soft, "hard")
    cand_score = select_gate_score(cand_hard, cand_soft, "hard")

    gate = evaluate_gate(
        candidate_skill=cand_skill,
        cand_hard=cand_hard,
        current_skill=skill,
        current_score=base_score,
        best_skill=skill,
        best_score=base_score,
        best_step=0,
        global_step=1,
        cand_soft=cand_soft,
        metric="hard",
    )

    _log("\n--- Gate Decision ---")
    _log(f"  baseline_score={base_score:.3f}  candidate_score={cand_score:.3f}")
    _log(f"  gate_action: {gate.action}")
    _log(f"  accepted: {gate.action != 'reject'}")

    _log("\n--- Baseline vs Candidate Comparison ---")
    _log(f"  {'Task':<6} {'Base hard':>10} {'Cand hard':>10} {'Delta':>8}")
    for i, ((bt, br), (ct, cr)) in enumerate(zip(_val_pairs_cache, cand_pairs), 1):
        delta = cr.hard - br.hard
        sign = "+" if delta >= 0 else ""
        _log(f"  [{i:2d}]   {br.hard:>10.2f} {cr.hard:>10.2f} {sign}{delta:>7.2f}")


# ── Comparison section ───────────────────────────────────────────────────────


def write_comparison(
    n_polluted: int,
    total_tasks: int,
    baseline_hard: float,
    baseline_soft: float,
    n_edits: int,
    edits: List[EditRecord],
    exit_stats: Dict[str, Any],
) -> None:
    """Write a comparison section contrasting v1 (single model) vs v2 (dual model)."""
    _section("Comparison: v1 (single glm-4-flash) vs v2 (dual model)")

    _log("\n  Metric                              | v1 (glm-4-flash only)       | v2 (dual model)")
    _log("  " + "-" * 100)
    _log(f"  Prompt pollution                    | Widespread (most tasks)     | {n_polluted}/{total_tasks} tasks polluted")
    _log(f"  reflect model                       | glm-4-flash                 | {REFLECT_MODEL}")
    _log(f"  reflect edits produced              | 0                           | {n_edits}")
    _log(f"  Baseline val hard score             | 0.375                       | {baseline_hard:.3f}")
    _log(f"  Baseline val soft score             | 0.413                       | {baseline_soft:.3f}")

    if n_polluted == 0:
        _log("\n  ✅ Prompt pollution ELIMINATED: _is_self_referential() filter working correctly.")
        _log("     No harvested task contains '# Skill Instructions' or other sleep-cycle markers.")
    else:
        _log(f"\n  ⚠ {n_polluted}/{total_tasks} tasks still have pollution — filter may need tuning.")

    if n_edits > 0:
        _log(f"\n  ✅ reflect() with {REFLECT_MODEL} produced {n_edits} edits (vs 0 from glm-4-flash).")
        _log("     Edit quality assessment:")
        for e in edits[:4]:
            content_preview = e.content[:120]
            _log(f"       • [{e.target}] {content_preview}")
        _log("\n     → Compare: are these rules concrete/actionable or vague?")
    else:
        _log(f"\n  ⚠ reflect() with {REFLECT_MODEL} still produced 0 edits.")
        _log("     Possible causes: timeout, JSON parse failure, or model returned [].")

    # Exit-code discrimination analysis
    n_exit = exit_stats["tasks_with_exit_code"]
    n_fail_exit = sum(1 for k, v in [(0, 0), (1, 0)] for _ in [])  # placeholder
    _log(f"\n  Exit-code judging: {n_exit}/{total_tasks} tasks have binary signal.")
    _log(f"    (v1: 5/15 tasks had exit_code; v2: {n_exit}/{total_tasks})")
    _log("    Exit-code judging converts ambiguous 'unknown' outcomes into clear 0/1,")
    _log("    improving discrimination beyond the degenerate outcome=0.5 default.")


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    global _val_pairs_cache

    _sep("=")
    _log("  E2E Sleep-Cycle Validation v2 — Dual-Model Strategy")
    _log(f"  Attempt Model: {ATTEMPT_MODEL}   Reflect Model: {REFLECT_MODEL}")
    _log(f"  Timeout: {TIMEOUT}s   Max Tasks: {MAX_TASKS}")
    _sep("=")

    # ── Phase 1 ──────────────────────────────────────────────────────────────
    _section("Phase 1: Harvest + Mine + Pollution Check")

    _log(f"\nHarvesting transcripts from {CLAUDE_PROJECTS_DIR} ...")
    t0 = time.time()
    digests = harvest(CLAUDE_PROJECTS_DIR)
    _log(f"  Harvested {len(digests)} sessions in {time.time()-t0:.1f}s")

    if not digests:
        _log("\n[FATAL] No sessions harvested. Exiting.")
        _write_report()
        return 1

    _log(f"\nMining tasks (max_tasks={MAX_TASKS}) ...")
    tasks = mine(digests, max_tasks=MAX_TASKS, seed=42)
    _log(f"  Mined {len(tasks)} tasks")

    train_tasks = [t for t in tasks if t.split == "train"]
    val_tasks = [t for t in tasks if t.split == "val"]
    _log(f"  Train: {len(train_tasks)}   Val: {len(val_tasks)}")

    # ── Pollution check on mined tasks ───────────────────────────────────────
    _log("\n--- Task Intent Preview (first 80 chars each) ---")
    n_polluted = 0
    for i, task in enumerate(tasks, 1):
        intent_preview = task.intent[:80].replace("\n", " ")
        pollution = _check_pollution(task.intent)
        if pollution:
            n_polluted += 1
            _log(f"  [{i:2d}] ⚠ POLLUTED ({len(pollution)} markers): {intent_preview!r}")
            _log(f"         markers: {pollution}")
        else:
            _log(f"  [{i:2d}] ✅ clean: {intent_preview!r}")

    _log(f"\n  Pollution check: {n_polluted}/{len(tasks)} tasks contain sleep-cycle markers.")
    if n_polluted == 0:
        _log("  ✅ PASS — _is_self_referential() filter successfully removed polluted sessions.")
    else:
        _log("  ⚠ WARN — some tasks still polluted. Filter may need additional markers.")

    # Exit code extraction
    _log("\nExtracting exit codes from transcripts...")
    exit_stats = extract_exit_codes(tasks, digests)
    _log(f"  Bash calls scanned: {exit_stats['total_bash_calls']}")
    _log(f"  Bash with is_error signal: {exit_stats['bash_with_signal']}")
    _log(f"    - success (is_error=False): {exit_stats['bash_success']}")
    _log(f"    - error   (is_error=True):  {exit_stats['bash_error']}")
    _log(f"  Tasks with exit_code set: {exit_stats['tasks_with_exit_code']}/{exit_stats['total_tasks']}")
    _log(f"  Tasks without transcript: {exit_stats['tasks_without_transcript']}")

    from collections import Counter
    outcome_dist = Counter(t.outcome for t in tasks)
    exit_dist = Counter(t.exit_code for t in tasks if t.exit_code is not None)
    _log(f"\n  Outcome distribution: {dict(outcome_dist)}")
    _log(f"  Exit-code distribution: {dict(exit_dist)}")

    # ── Phase 2 ──────────────────────────────────────────────────────────────
    _section("Phase 2: Baseline Replay (Val Set, glm-4-flash)")

    backend = CCBackend(
        model=ATTEMPT_MODEL,
        reflect_model=REFLECT_MODEL,
        timeout=TIMEOUT,
    )
    _log(f"\n  Backend: CCBackend(model={ATTEMPT_MODEL!r}, reflect_model={REFLECT_MODEL!r}, timeout={TIMEOUT})")
    _log(f"  Skill: {BASELINE_SKILL!r}")

    base_pairs = run_baseline(backend, val_tasks, BASELINE_SKILL, BASELINE_MEMORY)
    _val_pairs_cache = base_pairs
    baseline_hard, baseline_soft = aggregate_scores(base_pairs)

    # ── Phase 3 ──────────────────────────────────────────────────────────────
    _section("Phase 3: Reflect (Train Set, reflect=glm-4.6)")

    train_pairs, edits, failures, successes = run_reflect(
        backend, train_tasks, BASELINE_SKILL, BASELINE_MEMORY,
    )

    # ── Phase 4 ──────────────────────────────────────────────────────────────
    _section("Phase 4: Gate (Candidate vs Baseline)")

    run_gate(
        backend, val_tasks, BASELINE_SKILL, BASELINE_MEMORY,
        edits, baseline_hard, baseline_soft,
    )

    # ── Comparison ───────────────────────────────────────────────────────────
    write_comparison(
        n_polluted=n_polluted,
        total_tasks=len(tasks),
        baseline_hard=baseline_hard,
        baseline_soft=baseline_soft,
        n_edits=len(edits),
        edits=edits,
        exit_stats=exit_stats,
    )

    # ── Summary ──────────────────────────────────────────────────────────────
    _section("Summary")
    _log(f"\n  Tasks: {len(tasks)} (train={len(train_tasks)}, val={len(val_tasks)})")
    _log(f"  Pollution: {n_polluted}/{len(tasks)} tasks (v1 had widespread pollution)")
    _log(f"  Tasks with exit_code: {exit_stats['tasks_with_exit_code']}")
    _log(f"  Baseline val score: hard={baseline_hard:.3f}  soft={baseline_soft:.3f}")
    _log(f"  Train failures: {len(failures)}  successes: {len(successes)}")
    _log(f"  Proposed edits: {len(edits)} (v1 had 0)")

    _log("\n  --- Improvement #1: Prompt pollution filter ---")
    if n_polluted == 0:
        _log(f"  ✅ PASS: 0/{len(tasks)} tasks polluted. _is_self_referential() is working.")
    else:
        _log(f"  ⚠ PARTIAL: {n_polluted}/{len(tasks)} tasks still polluted.")

    _log("\n  --- Improvement #2: Exit-code judging ---")
    n_exit_judged = sum(1 for t in tasks if t.reference_kind == "exit_code")
    n_outcome_unknown = outcome_dist.get("unknown", 0)
    _log(f"  Tasks judged by exit_code: {n_exit_judged}/{len(tasks)}")
    _log(f"  Tasks that were 'unknown' outcome but now have exit_code: "
         f"{sum(1 for t in tasks if t.outcome == 'unknown' and t.exit_code is not None)}")
    if n_exit_judged > 0:
        _log(f"  → Binary exit_code signal for {n_exit_judged} tasks, vs outcome's degenerate 0.5 default.")

    _log("\n  --- Improvement #3: Strong reflect model (glm-4.6) ---")
    if edits:
        _log(f"  ✅ PASS: reflect() with glm-4.6 produced {len(edits)} edits (v1: 0 edits with glm-4-flash).")
        _log("  Edit content samples:")
        for e in edits[:3]:
            _log(f"    • [{e.target}] {e.content[:100]}")
    else:
        _log(f"  ⚠ reflect() produced 0 edits even with glm-4.6.")

    _write_report()
    return 0


def _write_report() -> None:
    """Write buffered report lines to markdown file."""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    header = (
        f"# E2E Sleep-Cycle Validation v2 Report\n\n"
        f"**Attempt Model:** {ATTEMPT_MODEL}  \n"
        f"**Reflect Model:** {REFLECT_MODEL}  \n"
        f"**Timeout:** {TIMEOUT}s  \n"
        f"**Max Tasks:** {MAX_TASKS}  \n"
        f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}  \n"
        f"**Strategy:** Dual-model (weak attempt, strong reflect)\n\n"
        f"---\n\n"
    )
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(header)
        for line in _report_lines:
            f.write(line + "\n")
    print(f"\n[Report written to {REPORT_PATH}]")


if __name__ == "__main__":
    sys.exit(main())
