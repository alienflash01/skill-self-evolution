#!/usr/bin/env python3
"""End-to-end sleep-cycle validation with improved CCBackend.

Runs a real E2E cycle using the glm-4-flash weak model to validate:
  1. exit-code judging has more discriminative power than outcome judging
  2. the restructured reflect() (with success-path contrast) produces
     more concrete, actionable rules

Pipeline:
  Phase 1 — harvest + mine real transcripts, extract exit codes
  Phase 2 — baseline replay on val set, print per-task details
  Phase 3 — replay train set, collect failures, call reflect()
  Phase 4 — apply edits, re-replay val set, gate decision

Output: stdout + data/e2e_validation_report.md

Usage:
    cd scripts && PYTHONPATH=. python3.12 sleep/e2e_validation.py
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
from sleep.replay import replay_batch, aggregate_scores, replay_one  # noqa: E402
from sleep.gate import evaluate_gate, select_gate_score  # noqa: E402
from sleep.memory import apply_edits  # noqa: E402

# ── Configuration ────────────────────────────────────────────────────────────

CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
MODEL = "glm-4-flash"
TIMEOUT = 45        # per-task timeout (seconds)
MAX_TASKS = 15      # control total scale
EDIT_BUDGET = 4
REPORT_PATH = str(Path(_SCRIPTS_DIR).parent / "data" / "e2e_validation_report.md")

BASELINE_SKILL = "# Skill\nNo instructions yet."
BASELINE_MEMORY = ""

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


def _print_task_details(pairs: List[Tuple[TaskRecord, ReplayResult]], label: str) -> None:
    """Print per-task judging details: intent, hard, soft, rationale."""
    _log(f"\n--- {label} Per-Task Details ---")
    for i, (task, result) in enumerate(pairs, 1):
        intent_preview = task.intent[:80].replace("\n", " ")
        _log(
            f"  [{i:2d}] intent={intent_preview!r}\n"
            f"       hard={result.hard:.2f}  soft={result.soft:.2f}  "
            f"latency={result.latency_ms:.0f}ms  "
            f"exit_code={task.exit_code}  outcome={task.outcome}\n"
            f"       rationale: {result.judge_rationale}\n"
            f"       response:  {result.response[:120]!r}"
        )


# ── Phase 1: Real data collection + exit-code extraction ─────────────────────


def extract_exit_codes(
    tasks: List[TaskRecord],
    digests: List[SessionDigest],
) -> Dict[str, Any]:
    """Scan transcripts for Bash tool_result is_error signals.

    For each task, find its source session transcript, scan all Bash
    tool_results, and derive an exit code:
      - is_error=False → exit_code=0 (success)
      - is_error=True  → exit_code=1 (failure)

    If a session has mixed results, the LAST Bash result wins (final state).
    Sets task.exit_code and task.reference_kind = 'exit_code' when available.

    Returns stats dict.
    """
    # Build session_id → raw_path mapping
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
        # Find transcript for this task's source sessions
        transcript_path = None
        for sid in task.source_sessions:
            if sid in sid_to_path:
                transcript_path = sid_to_path[sid]
                break

        if transcript_path is None:
            tasks_without_transcript += 1
            continue

        # Build tool_use_id → tool_name map for this transcript
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

        # Scan tool_results for Bash calls — collect ALL exit signals
        # Strategy: if ANY Bash call had is_error=True, the task "failed"
        # (the agent hit at least one command failure).
        # This is more discriminative than last-result-wins.
        has_any_error = False
        has_any_success = False
        bash_results_in_session: List[bool] = []  # True=error
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

        # Derive exit_code from the collected Bash signals:
        #   - If there was ANY error → exit_code=1 (the task encountered failures)
        #   - If all Bash calls succeeded → exit_code=0
        #   - If no Bash signal at all → leave as None
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
) -> Tuple[List[Tuple[TaskRecord, ReplayResult]], List[EditRecord], List[Tuple[TaskRecord, ReplayResult]], List[Tuple[TaskRecord, ReplayResult]]]:
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

    _log(f"\n  Calling backend.reflect() (model={MODEL}, timeout={TIMEOUT}s)...")
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
            f"      content:  {e.content}\n"
            f"      rationale: {e.rationale}"
        )

    if not edits:
        _log("\n  (No edits proposed — reflect returned empty)")

    return train_pairs, edits, failures, successes


# ── Phase 4: Gate ────────────────────────────────────────────────────────────


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

    # Apply edits to skill
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

    # Re-replay val set with candidate
    _log("\n  Replaying val set with candidate skill...")
    cand_pairs = replay_batch(backend, val_tasks, cand_skill, cand_memory)
    cand_hard, cand_soft = aggregate_scores(cand_pairs)
    _log(f"  Candidate — hard={cand_hard:.3f}  soft={cand_soft:.3f}  (n={len(cand_pairs)})")
    _print_task_details(cand_pairs, "Candidate")

    # Gate decision
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

    _log(f"\n--- Gate Decision ---")
    _log(f"  baseline_score={base_score:.3f}  candidate_score={cand_score:.3f}")
    _log(f"  gate_action: {gate.action}")
    _log(f"  accepted: {gate.action != 'reject'}")

    # Comparison table
    _log(f"\n--- Baseline vs Candidate Comparison ---")
    _log(f"  {'Task':<6} {'Base hard':>10} {'Cand hard':>10} {'Delta':>8}")
    for i, ((bt, br), (ct, cr)) in enumerate(zip(
        _val_pairs_cache, cand_pairs
    ), 1):
        delta = cr.hard - br.hard
        sign = "+" if delta >= 0 else ""
        _log(f"  [{i:2d}]   {br.hard:>10.2f} {cr.hard:>10.2f} {sign}{delta:>7.2f}")


# Module-level cache for comparison table (set in main)
_val_pairs_cache: List[Tuple[TaskRecord, ReplayResult]] = []


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    global _val_pairs_cache

    _sep("=")
    _log("  E2E Sleep-Cycle Validation — CCBackend (exit-code + contrast reflect)")
    _log(f"  Model: {MODEL}   Timeout: {TIMEOUT}s   Max Tasks: {MAX_TASKS}")
    _sep("=")

    # ── Phase 1 ──────────────────────────────────────────────────────────────
    _section("Phase 1: Real Data Collection")

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

    # Split info
    train_tasks = [t for t in tasks if t.split == "train"]
    val_tasks = [t for t in tasks if t.split == "val"]
    _log(f"  Train: {len(train_tasks)}   Val: {len(val_tasks)}")

    _log("\nExtracting exit codes from transcripts...")
    exit_stats = extract_exit_codes(tasks, digests)
    _log(f"  Bash calls scanned: {exit_stats['total_bash_calls']}")
    _log(f"  Bash with is_error signal: {exit_stats['bash_with_signal']}")
    _log(f"    - success (is_error=False): {exit_stats['bash_success']}")
    _log(f"    - error   (is_error=True):  {exit_stats['bash_error']}")
    _log(f"  Tasks with exit_code set: {exit_stats['tasks_with_exit_code']}/{exit_stats['total_tasks']}")
    _log(f"  Tasks without transcript: {exit_stats['tasks_without_transcript']}")

    # Pre-replay outcome distribution (for comparison)
    from collections import Counter
    outcome_dist = Counter(t.outcome for t in tasks)
    exit_dist = Counter(t.exit_code for t in tasks if t.exit_code is not None)
    _log(f"\n  Outcome distribution: {dict(outcome_dist)}")
    _log(f"  Exit-code distribution: {dict(exit_dist)}")
    _log(f"\n  → Key comparison: outcome has {outcome_dist.get('unknown', 0)} 'unknown' tasks,")
    _log(f"    while exit_code provides binary signal for {exit_stats['tasks_with_exit_code']} tasks.")

    # ── Phase 2 ──────────────────────────────────────────────────────────────
    _section("Phase 2: Baseline Replay (Val Set)")

    backend = CCBackend(model=MODEL, timeout=TIMEOUT)
    _log(f"\n  Backend: CCBackend(model={MODEL!r}, timeout={TIMEOUT})")
    _log(f"  Skill: {BASELINE_SKILL!r}")

    base_pairs = run_baseline(backend, val_tasks, BASELINE_SKILL, BASELINE_MEMORY)
    _val_pairs_cache = base_pairs
    baseline_hard, baseline_soft = aggregate_scores(base_pairs)

    # ── Phase 3 ──────────────────────────────────────────────────────────────
    _section("Phase 3: Reflect (Train Set)")

    train_pairs, edits, failures, successes = run_reflect(
        backend, train_tasks, BASELINE_SKILL, BASELINE_MEMORY,
    )

    # ── Phase 4 ──────────────────────────────────────────────────────────────
    _section("Phase 4: Gate (Candidate vs Baseline)")

    run_gate(
        backend, val_tasks, BASELINE_SKILL, BASELINE_MEMORY,
        edits, baseline_hard, baseline_soft,
    )

    # ── Summary ──────────────────────────────────────────────────────────────
    _section("Summary")
    _log(f"\n  Tasks: {len(tasks)} (train={len(train_tasks)}, val={len(val_tasks)})")
    _log(f"  Tasks with exit_code: {exit_stats['tasks_with_exit_code']}")
    _log(f"  Baseline val score: hard={baseline_hard:.3f}  soft={baseline_soft:.3f}")
    _log(f"  Train failures: {len(failures)}  successes: {len(successes)}")
    _log(f"  Proposed edits: {len(edits)}")

    _log("\n  --- Validation of Improvement #1 (exit-code judging) ---")
    n_exit_judged = sum(1 for t in tasks if t.reference_kind == "exit_code")
    n_outcome_unknown = outcome_dist.get("unknown", 0)
    _log(f"  Tasks judged by exit_code: {n_exit_judged}/{len(tasks)}")
    _log(f"  Tasks that were 'unknown' outcome but now have exit_code: "
         f"{sum(1 for t in tasks if t.outcome == 'unknown' and t.exit_code is not None)}")
    if n_exit_judged > 0:
        _log(f"  → exit-code judging provides BINARY signal (0/1) for {n_exit_judged} tasks,")
        _log(f"    replacing the degenerate outcome path where {n_outcome_unknown} tasks scored 0.5.")

    _log("\n  --- Validation of Improvement #2 (contrast reflect) ---")
    if edits:
        _log(f"  reflect() produced {len(edits)} edits. Content samples:")
        for e in edits[:3]:
            _log(f"    • [{e.target}] {e.content[:100]}")
        _log(f"  → Check above: are these specific/actionable, or vague platitudes?")
    else:
        _log(f"  reflect() produced 0 edits (model may have timed out or found nothing).")

    _write_report()
    return 0


def _write_report() -> None:
    """Write buffered report lines to markdown file."""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    header = (
        f"# E2E Sleep-Cycle Validation Report\n\n"
        f"**Model:** {MODEL}  \n"
        f"**Timeout:** {TIMEOUT}s  \n"
        f"**Max Tasks:** {MAX_TASKS}  \n"
        f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"---\n\n"
    )
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(header)
        for line in _report_lines:
            f.write(line + "\n")
    print(f"\n[Report written to {REPORT_PATH}]")


if __name__ == "__main__":
    sys.exit(main())
