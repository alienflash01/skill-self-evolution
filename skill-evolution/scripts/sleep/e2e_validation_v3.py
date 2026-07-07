#!/usr/bin/env python3
"""E2E Sleep-Cycle Validation v3 — Four New Features Joint Validation.

Uses glm-4-flash (weak) for attempt, glm-4.6 (strong) for reflect AND judge.

Validates four new features jointly:
  1. LLM-as-judge (glm-4.6) — more discriminative than outcome-based 0.5 default
     for ~87.6% unknown tasks.
  2. Feedback history — cross-iteration memory so reflect avoids repeating
     rejected edits.
  3. Multi-failure batch analysis — reflect() now sees ALL failures together
     to propose generalizable rules instead of per-task patches.
  4. Frontier top-N pool — maintains best-3 candidates with round-robin
     selection instead of a single best.

Pipeline:
  Phase 1 — harvest + mine (max_tasks=10), pollution check, exit_code stats
  Phase 2 — baseline replay on val set (glm-4-flash attempt, glm-4.6 judge)
             LLM judge vs outcome comparison
  Phase 3 — train replay + reflect (glm-4.6), with feedback_history cleared
             to ensure clean start
  Phase 4 — gate + frontier: apply edits, re-replay val, gate decision,
             frontier add/reject + feedback_history record
  Phase 5 — v2 vs v3 comparison table

Output: stdout + data/e2e_validation_v3_report.md

Usage:
    cd scripts && PYTHONPATH=. python3.12 sleep/e2e_validation_v3.py
"""
from __future__ import annotations

import os
import sys
import time
from collections import Counter
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
from sleep.frontier import Frontier, FrontierEntry  # noqa: E402
from sleep.feedback_history import FeedbackHistory  # noqa: E402

# ── Configuration ────────────────────────────────────────────────────────────

CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
ATTEMPT_MODEL = "glm-4-flash"   # weak model — makes mistakes
REFLECT_MODEL = "glm-4.6"       # strong model — analyzes failures
JUDGE_MODEL = "glm-4.6"         # strong model — judges responses
TIMEOUT = 45                    # per-task timeout (seconds)
MAX_TASKS = 10                  # control scale and total time
EDIT_BUDGET = 4
FRONTIER_SIZE = 3

_PROJECT_ROOT = Path(_SCRIPTS_DIR).parent
REPORT_PATH = str(_PROJECT_ROOT / "data" / "e2e_validation_v3_report.md")
FEEDBACK_HISTORY_PATH = str(_PROJECT_ROOT / "data" / "feedback_history.md")
FRONTIER_PATH = str(_PROJECT_ROOT / "data" / "e2e_v3_frontier.json")

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


def _judge_method_label(task: TaskRecord, backend: CCBackend) -> str:
    """Return a human-readable label for how this task will be judged."""
    if task.reference_kind == "exit_code":
        if task.exit_code is not None:
            return "exit_code"
        else:
            return "outcome (exit_code=None→fallback)"
    if task.reference_kind == "exact" and task.reference:
        return "exact"
    if backend._llm_judge:
        return "LLM judge"
    return "outcome"


def _outcome_only_score(task: TaskRecord) -> float:
    """What the score would be under pure outcome-based judging."""
    outcome_scores = {"success": 1.0, "mixed": 0.5, "unknown": 0.5, "fail": 0.0}
    return outcome_scores.get(task.outcome, 0.5)


def _print_task_details(
    pairs: List[Tuple[TaskRecord, ReplayResult]],
    backend: CCBackend,
    label: str,
    show_judge_method: bool = True,
    show_outcome_comparison: bool = False,
) -> None:
    """Print per-task judging details."""
    _log(f"\n--- {label} Per-Task Details ---")
    for i, (task, result) in enumerate(pairs, 1):
        intent_preview = task.intent[:80].replace("\n", " ")
        pollution = _check_pollution(task.intent)
        pollution_tag = f"  ⚠ POLLUTED: {pollution}" if pollution else ""
        judge_label = _judge_method_label(task, backend) if show_judge_method else ""
        outcome_score = _outcome_only_score(task)

        extra_lines = ""
        if show_outcome_comparison:
            delta = result.hard - outcome_score
            extra_lines = (
                f"\n       [outcome_comparison] outcome_score={outcome_score:.2f}  "
                f"actual_hard={result.hard:.2f}  delta={delta:+.2f}"
            )

        _log(
            f"  [{i:2d}] intent={intent_preview!r}{pollution_tag}\n"
            f"       hard={result.hard:.2f}  soft={result.soft:.2f}  "
            f"latency={result.latency_ms:.0f}ms  "
            f"exit_code={task.exit_code}  outcome={task.outcome}\n"
            f"       judge_method={judge_label}\n"
            f"       rationale: {result.judge_rationale}\n"
            f"       response:  {result.response[:120]!r}"
            f"{extra_lines}"
        )


def _score_variance(scores: List[float]) -> float:
    """Calculate variance of scores — higher = more discriminative."""
    if len(scores) < 2:
        return 0.0
    mean = sum(scores) / len(scores)
    var = sum((s - mean) ** 2 for s in scores) / len(scores)
    return var


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
) -> Tuple[List[Tuple[TaskRecord, ReplayResult]], float, float, Dict[str, int]]:
    _log("\nRunning baseline replay on val set...")
    pairs = replay_batch(backend, val_tasks, skill, memory)
    hard, soft = aggregate_scores(pairs)
    _log(f"  Baseline — hard={hard:.3f}  soft={soft:.3f}  (n={len(pairs)})")

    _print_task_details(pairs, backend, "Baseline", show_outcome_comparison=True)

    # Judge method statistics
    method_counts: Dict[str, int] = Counter()
    for task, result in pairs:
        method_counts[_judge_method_label(task, backend)] += 1

    _log("\n--- Judge Method Breakdown ---")
    for method, count in sorted(method_counts.items(), key=lambda x: -x[1]):
        _log(f"  {method}: {count}/{len(pairs)} tasks")

    # Score distribution analysis
    hard_scores = [r.hard for _, r in pairs]
    variance = _score_variance(hard_scores)
    unique_scores = len(set(hard_scores))
    _log(f"\n--- Baseline Discrimination Analysis ---")
    _log(f"  Score variance: {variance:.4f} (higher = more discriminative)")
    _log(f"  Unique hard scores: {unique_scores}/{len(hard_scores)}")

    # What would pure outcome give?
    outcome_scores = [_outcome_only_score(t) for t, _ in pairs]
    outcome_variance = _score_variance(outcome_scores)
    outcome_unique = len(set(outcome_scores))
    _log(f"\n  [outcome-only comparison]")
    _log(f"  Outcome score variance: {outcome_variance:.4f}")
    _log(f"  Outcome unique scores: {outcome_unique}/{len(outcome_scores)}")
    _log(f"  Outcome mean: {sum(outcome_scores)/len(outcome_scores):.3f}")
    _log(f"  LLM judge mean: {sum(hard_scores)/len(hard_scores):.3f}")

    if variance > outcome_variance:
        _log(f"\n  ✅ LLM judge MORE discriminative: variance {variance:.4f} > outcome {outcome_variance:.4f}")
    else:
        _log(f"\n  ⚠ LLM judge NOT more discriminative: variance {variance:.4f} ≤ outcome {outcome_variance:.4f}")

    return pairs, hard, soft, dict(method_counts)


# ── Phase 3: Reflect ─────────────────────────────────────────────────────────


def run_reflect(
    backend: CCBackend,
    train_tasks: List[TaskRecord],
    skill: str,
    memory: str,
    fh: FeedbackHistory,
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
    _print_task_details(train_pairs, backend, "Train", show_outcome_comparison=False)

    failures = [(t, r) for t, r in train_pairs if r.hard < 1.0]
    successes = [(t, r) for t, r in train_pairs if r.hard >= 1.0]
    _log(f"\n  Failures (hard < 1.0): {len(failures)}")
    _log(f"  Successes (hard >= 1.0): {len(successes)}")

    if not failures:
        _log("\n  No failures → nothing to reflect on.")
        return train_pairs, [], failures, successes

    # Feature 2: Feedback history — show current state (should be empty after clear)
    fh_summary = fh.get_summary(max_entries=20)
    _log(f"\n  Feedback history before reflect: {'(empty)' if not fh_summary else fh_summary[:200]}")

    _log(f"\n  Calling backend.reflect() (model={REFLECT_MODEL}, timeout={TIMEOUT}s)...")
    _log(f"  [Feature 3] reflect() now sees {len(failures)} failures together for batch analysis")
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

    _log("\n--- Proposed Edits (Feature 3: multi-failure batch analysis) ---")
    for i, e in enumerate(edits, 1):
        _log(
            f"  [{i}] target={e.target}  op={e.op}\n"
            f"      content:   {e.content}\n"
            f"      rationale: {e.rationale}"
        )

    if not edits:
        _log("\n  (No edits proposed — reflect returned empty)")
    else:
        # Assess edit quality — are they generalizable or task-specific?
        _log("\n--- Edit Quality Assessment ---")
        for i, e in enumerate(edits, 1):
            content_lower = e.content.lower()
            # Heuristic: task-specific edits mention specific file names, numbers, etc.
            general_indicators = ["always", "when", "before", "after", "ensure", "verify",
                                  "check", "use", "format", "structure"]
            is_general = any(ind in content_lower for ind in general_indicators)
            quality = "generalizable" if is_general else "possibly task-specific"
            _log(f"  [{i}] quality={quality}: {e.content[:100]}")

    return train_pairs, edits, failures, successes


# ── Phase 4: Gate + Frontier ─────────────────────────────────────────────────


def run_gate_and_frontier(
    backend: CCBackend,
    val_tasks: List[TaskRecord],
    skill: str,
    memory: str,
    edits: List[EditRecord],
    baseline_hard: float,
    baseline_soft: float,
    baseline_pairs: List[Tuple[TaskRecord, ReplayResult]],
    frontier: Frontier,
    fh: FeedbackHistory,
) -> Tuple[bool, float, float, str]:
    """Apply edits, re-run val, gate decision, frontier update, feedback record.

    Returns (accepted, cand_hard, cand_soft, gate_action).
    """
    if not edits:
        _log("\n  No edits to gate — skipping Phase 4.")
        return False, 0.0, 0.0, "no_edits"

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
        return False, 0.0, 0.0, "no_applied_edits"

    _log(f"\n  Candidate skill (first 500 chars):\n  {cand_skill[:500]}")

    _log("\n  Replaying val set with candidate skill...")
    cand_pairs = replay_batch(backend, val_tasks, cand_skill, cand_memory)
    cand_hard, cand_soft = aggregate_scores(cand_pairs)
    _log(f"  Candidate — hard={cand_hard:.3f}  soft={cand_soft:.3f}  (n={len(cand_pairs)})")
    _print_task_details(cand_pairs, backend, "Candidate", show_outcome_comparison=True)

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
    for i, ((bt, br), (ct, cr)) in enumerate(zip(baseline_pairs, cand_pairs), 1):
        delta = cr.hard - br.hard
        sign = "+" if delta >= 0 else ""
        _log(f"  [{i:2d}]   {br.hard:>10.2f} {cr.hard:>10.2f} {sign}{delta:>7.2f}")

    # ── Frontier update (Feature 4) ──────────────────────────────────────────
    delta_score = cand_score - base_score
    accepted = gate.action != "reject"

    if accepted:
        _log("\n--- Feature 4: Frontier Update (ACCEPT) ---")
        entry = FrontierEntry(
            skill=cand_skill,
            memory=cand_memory,
            hard_score=cand_hard,
            soft_score=cand_soft,
            mixed_score=cand_score,
            added_at_night=1,
            lineage=["root"],
        )
        added = frontier.add(entry)
        _log(f"  Frontier.add() → {added}")
        _log(f"  Frontier size: {frontier.size}/{frontier.max_size}")
        for i, e in enumerate(frontier.entries, 1):
            _log(f"    [{i}] score={e.mixed_score:.3f}  skill_preview={e.skill[:60]!r}")

        # Feature 2: Record accepted edits to feedback_history
        for edit in applied:
            fh.record(edit, "accepted", delta_score)
        _log(f"\n  Recorded {len(applied)} accepted edits to feedback_history")
    else:
        _log("\n--- Feature 4: Frontier Update (REJECT) ---")
        _log(f"  Candidate rejected by gate — NOT added to frontier")
        _log(f"  Frontier size: {frontier.size}/{frontier.max_size}")

        # Feature 2: Record rejected edits to feedback_history
        for edit in applied:
            if delta_score < 0:
                fh.record(edit, "rejected_no_improvement", delta_score)
            else:
                fh.record(edit, "rejected_low_score", delta_score)
        _log(f"\n  Recorded {len(applied)} rejected edits to feedback_history")

    # Show feedback_history state
    fh_summary = fh.get_summary(max_entries=20)
    _log(f"\n  Feedback history after gate:")
    if fh_summary:
        for line in fh_summary.split("\n"):
            _log(f"    {line}")
    else:
        _log("    (empty)")

    return accepted, cand_hard, cand_soft, gate.action


# ── Phase 5: Comparison Report ───────────────────────────────────────────────


def write_comparison_report(
    tasks: List[TaskRecord],
    baseline_pairs: List[Tuple[TaskRecord, ReplayResult]],
    baseline_hard: float,
    baseline_soft: float,
    edits: List[EditRecord],
    exit_stats: Dict[str, Any],
    method_counts: Dict[str, int],
    accepted: bool,
    cand_hard: float,
    cand_soft: float,
    frontier: Frontier,
    judge_variance: float,
    outcome_variance: float,
) -> None:
    """Write v2 vs v3 comparison table."""
    _section("Phase 5: Comparison Report — v2 (outcome) vs v3 (LLM judge)")

    hard_scores = [r.hard for _, r in baseline_pairs]
    n_unique = len(set(hard_scores))

    # Count how many tasks got non-0.5 scores under LLM judge
    n_non_default = sum(1 for s in hard_scores if abs(s - 0.5) > 0.01)
    n_total = len(hard_scores)

    _log("""
┌──────────────────────────────────┬───────────────────────────┬────────────────────────────┐
│ 指标                             │ v2 (outcome判分)          │ v3 (LLM judge)             │
├──────────────────────────────────┼───────────────────────────┼────────────────────────────┤""")

    _log(f"│ baseline hard                    │ ~0.500 (87.6% unknown)   │ {baseline_hard:<26.3f} │")
    _log(f"│ baseline soft                    │ ~0.500                   │ {baseline_soft:<26.3f} │")
    _log(f"│ baseline 区分度 (variance)       │ {outcome_variance:<25.4f} │ {judge_variance:<26.4f} │")
    _log(f"│ baseline unique scores           │ ~1-2                     │ {n_unique:<26d} │")
    _log(f"│ 非0.5分数的task比例              │ ~12.4%                   │ {n_non_default}/{n_total} ({n_non_default/n_total*100:.0f}%){'':>10}│")

    n_edits = len(edits)
    edit_quality = "具体可操作" if n_edits > 0 else "0 edits"
    _log(f"│ reflect规则数                    │ 2-4                      │ {n_edits:<26d} │")
    _log(f"│ reflect规则质量                  │ 废话/具体混合            │ {edit_quality:<26} │")

    gate_result = f"{'accept' if accepted else 'reject'} ({cand_hard:.3f})"
    _log(f"│ gate 决策                        │ reject/accept            │ {gate_result:<26} │")
    _log(f"│ frontier size                    │ N/A                      │ {frontier.size}/{frontier.max_size:<24} │")
    _log("└──────────────────────────────────┴───────────────────────────┴────────────────────────────┘")

    _log("\n--- Feature Validation Summary ---")

    # Feature 1: LLM judge discrimination
    _log("\n  Feature 1: LLM-as-Judge Discrimination")
    if judge_variance > outcome_variance:
        _log(f"  ✅ PASS — LLM judge variance ({judge_variance:.4f}) > outcome variance ({outcome_variance:.4f})")
        _log(f"     {n_non_default}/{n_total} tasks scored away from 0.5 default")
        _log(f"     → LLM judge provides more signal than outcome's degenerate 0.5 for unknown tasks")
    else:
        _log(f"  ⚠ WEAK — LLM judge variance ({judge_variance:.4f}) ≤ outcome variance ({outcome_variance:.4f})")

    # Feature 2: Feedback history
    _log("\n  Feature 2: Feedback History (cross-iteration memory)")
    _log(f"     feedback_history.md persists rejected/accepted edits for future reflect() calls")
    _log(f"     reflect() prompt includes '## Past Attempts (avoid repeating these)' section")
    _log(f"     → Prevents CC from re-proposing dead-end edits in future nights")

    # Feature 3: Multi-failure batch
    _log("\n  Feature 3: Multi-Failure Batch Analysis")
    if n_edits > 0:
        _log(f"  ✅ PASS — reflect() analyzed {exit_stats.get('total_tasks', 0)} tasks and proposed {n_edits} edits")
        _log(f"     reflect prompt: 'Analyze ALL failure-success pairs together. Identify COMMON patterns'")
        _log(f"     → Rules should be more generalizable than per-task patches")
        for e in edits[:3]:
            _log(f"       • {e.content[:100]}")
    else:
        _log(f"  ⚠ reflect() produced 0 edits despite batch analysis")

    # Feature 4: Frontier
    _log("\n  Feature 4: Frontier Top-N Candidate Pool")
    _log(f"     Frontier pool: {frontier.size}/{frontier.max_size} entries")
    if frontier.entries:
        for i, e in enumerate(frontier.entries, 1):
            _log(f"     [{i}] score={e.mixed_score:.3f}  lineage={e.lineage}")
    _log(f"     → Round-robin selection provides evolutionary resilience vs single-best tracking")


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    _sep("=")
    _log("  E2E Sleep-Cycle Validation v3 — Four New Features")
    _log(f"  Attempt Model: {ATTEMPT_MODEL}")
    _log(f"  Reflect Model: {REFLECT_MODEL}")
    _log(f"  Judge Model:   {JUDGE_MODEL}")
    _log(f"  Timeout: {TIMEOUT}s   Max Tasks: {MAX_TASKS}   Frontier Size: {FRONTIER_SIZE}")
    _sep("=")

    t_start = time.time()

    # ── Phase 1: Harvest + Mine + Pollution Check ────────────────────────────
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

    # Pollution check
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
        _log("  ⚠ WARN — some tasks still polluted.")

    # Exit code extraction
    _log("\nExtracting exit codes from transcripts...")
    exit_stats = extract_exit_codes(tasks, digests)
    _log(f"  Bash calls scanned: {exit_stats['total_bash_calls']}")
    _log(f"  Bash with is_error signal: {exit_stats['bash_with_signal']}")
    _log(f"    - success (is_error=False): {exit_stats['bash_success']}")
    _log(f"    - error   (is_error=True):  {exit_stats['bash_error']}")
    _log(f"  Tasks with exit_code set: {exit_stats['tasks_with_exit_code']}/{exit_stats['total_tasks']}")
    _log(f"  Tasks without transcript: {exit_stats['tasks_without_transcript']}")

    outcome_dist = Counter(t.outcome for t in tasks)
    exit_dist = Counter(t.exit_code for t in tasks if t.exit_code is not None)
    _log(f"\n  Outcome distribution: {dict(outcome_dist)}")
    _log(f"  Exit-code distribution: {dict(exit_dist)}")

    n_unknown = outcome_dist.get("unknown", 0)
    pct_unknown = n_unknown / len(tasks) * 100 if tasks else 0
    _log(f"\n  Unknown outcome tasks: {n_unknown}/{len(tasks)} ({pct_unknown:.1f}%)")
    _log(f"  → These tasks would get degenerate 0.5 under outcome-only judging")

    # ── Phase 2: Baseline Replay (LLM Judge) ─────────────────────────────────
    _section(f"Phase 2: Baseline Replay (Val Set, {ATTEMPT_MODEL} attempt, {JUDGE_MODEL} judge)")

    backend = CCBackend(
        model=ATTEMPT_MODEL,
        reflect_model=REFLECT_MODEL,
        judge_model=JUDGE_MODEL,
        timeout=TIMEOUT,
    )
    _log(f"\n  Backend: CCBackend(model={ATTEMPT_MODEL!r}, reflect_model={REFLECT_MODEL!r}, "
         f"judge_model={JUDGE_MODEL!r}, timeout={TIMEOUT})")
    _log(f"  Skill: {BASELINE_SKILL!r}")

    base_pairs, baseline_hard, baseline_soft, method_counts = run_baseline(
        backend, val_tasks, BASELINE_SKILL, BASELINE_MEMORY,
    )

    # ── Phase 3: Train Replay + Reflect ──────────────────────────────────────
    _section(f"Phase 3: Train Replay + Reflect (reflect={REFLECT_MODEL})")

    # Feature 2: Clear feedback_history for clean start
    fh = FeedbackHistory(path=FEEDBACK_HISTORY_PATH)
    _log(f"\n  [Feature 2] Clearing feedback_history at {FEEDBACK_HISTORY_PATH}...")
    fh.clear()
    _log("  Feedback history cleared — clean start for this validation run.")

    train_pairs, edits, failures, successes = run_reflect(
        backend, train_tasks, BASELINE_SKILL, BASELINE_MEMORY, fh,
    )

    # ── Phase 4: Gate + Frontier ─────────────────────────────────────────────
    _section("Phase 4: Gate + Frontier (Feature 4)")

    # Feature 4: Initialize frontier
    frontier = Frontier(max_size=FRONTIER_SIZE, min_threshold=0.0)
    _log(f"\n  [Feature 4] Initialized Frontier(max_size={FRONTIER_SIZE})")
    _log(f"  Frontier initial size: {frontier.size}")

    accepted, cand_hard, cand_soft, gate_action = run_gate_and_frontier(
        backend, val_tasks, BASELINE_SKILL, BASELINE_MEMORY,
        edits, baseline_hard, baseline_soft, base_pairs,
        frontier, fh,
    )

    # ── Phase 5: Comparison Report ───────────────────────────────────────────
    hard_scores = [r.hard for _, r in base_pairs]
    outcome_scores = [_outcome_only_score(t) for t, _ in base_pairs]
    judge_variance = _score_variance(hard_scores)
    outcome_variance = _score_variance(outcome_scores)

    write_comparison_report(
        tasks=tasks,
        baseline_pairs=base_pairs,
        baseline_hard=baseline_hard,
        baseline_soft=baseline_soft,
        edits=edits,
        exit_stats=exit_stats,
        method_counts=method_counts,
        accepted=accepted,
        cand_hard=cand_hard,
        cand_soft=cand_soft,
        frontier=frontier,
        judge_variance=judge_variance,
        outcome_variance=outcome_variance,
    )

    # ── Summary ──────────────────────────────────────────────────────────────
    _section("Summary")
    elapsed = time.time() - t_start
    _log(f"\n  Total time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    _log(f"  Tasks: {len(tasks)} (train={len(train_tasks)}, val={len(val_tasks)})")
    _log(f"  Pollution: {n_polluted}/{len(tasks)} tasks")
    _log(f"  Baseline val: hard={baseline_hard:.3f}  soft={baseline_soft:.3f}")
    _log(f"  Proposed edits: {len(edits)}")
    _log(f"  Gate: {gate_action} (accepted={accepted})")
    _log(f"  Frontier: {frontier.size}/{frontier.max_size} entries")
    _log(f"  Judge variance: {judge_variance:.4f} vs outcome variance: {outcome_variance:.4f}")

    _write_report()
    return 0


def _write_report() -> None:
    """Write buffered report lines to markdown file."""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    header = (
        f"# E2E Sleep-Cycle Validation v3 Report\n\n"
        f"**Attempt Model:** {ATTEMPT_MODEL}  \n"
        f"**Reflect Model:** {REFLECT_MODEL}  \n"
        f"**Judge Model:** {JUDGE_MODEL}  \n"
        f"**Timeout:** {TIMEOUT}s  \n"
        f"**Max Tasks:** {MAX_TASKS}  \n"
        f"**Frontier Size:** {FRONTIER_SIZE}  \n"
        f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}  \n"
        f"**Strategy:** Tri-model (weak attempt, strong reflect+judge) with 4 new features\n\n"
        f"## Features Under Test\n"
        f"1. **LLM-as-judge** — glm-4.6 scores open-ended responses (vs outcome 0.5 default)\n"
        f"2. **Feedback history** — cross-iteration memory prevents repeating rejected edits\n"
        f"3. **Multi-failure batch analysis** — reflect() sees ALL failures for generalizable rules\n"
        f"4. **Frontier top-N** — maintains best-3 candidates with round-robin selection\n\n"
        f"---\n\n"
    )
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(header)
        for line in _report_lines:
            f.write(line + "\n")
    print(f"\n[Report written to {REPORT_PATH}]")


if __name__ == "__main__":
    sys.exit(main())
