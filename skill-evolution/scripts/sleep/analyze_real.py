#!/usr/bin/env python3
"""Real transcript analysis script for sleep-engine quality assessment.

Scans all CC transcripts under ~/.claude/projects/, runs harvest() + mine(),
and produces a comprehensive quality report covering:

  - Harvest statistics (sessions, turns, tools)
  - Mine statistics (tasks, splits, outcomes)
  - Reference quality (reference_kind distribution — key metric)
  - Exit-code availability (Bash calls with is_error signals)
  - Task intent quality (actionability, length)

Outputs to both stdout and ``data/real_analysis_report.md``.

Usage:
    cd scripts && PYTHONPATH=. python3.12 sleep/analyze_real.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── sys.path bootstrap so this runs standalone ──────────────────────────────
# When executed as a module (python3.12 sleep/analyze_real.py), the scripts/
# dir is NOT automatically on sys.path. Ensure it is.
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from sleep.harvest import harvest  # noqa: E402
from sleep.mine import mine  # noqa: E402
from sleep.models import SessionDigest, TaskRecord  # noqa: E402

# ── Configuration ───────────────────────────────────────────────────────────

CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
HARVEST_SCOPE = "all"
HARVEST_LIMIT = 0  # 0 = no limit

# Keywords indicating actionable / concrete coding tasks
_ACTIONABLE_KEYWORDS = (
    # English
    "write", "test", "fix", "bug", "compile", "build", "run", "deploy",
    "install", "refactor", "optimize", "debug", "error", "fail", "pass",
    "implement", "add", "remove", "delete", "update", "create", "configure",
    "lint", "format", "migrate", "query", "execute", "commit", "merge",
    "replace", "rename", "extract", "parse", "convert", "generate",
    # Chinese
    "写", "测试", "修复", "修", "编译", "运行", "部署", "安装",
    "重构", "优化", "调试", "错误", "实现", "添加", "删除", "更新",
    "创建", "配置", "提交", "合并", "替换", "修改", "生成", "执行",
)

# Intent length thresholds
INTENT_ACTIONABLE_MIN = 20   # chars — "actionable" threshold
INTENT_TOO_SHORT_MAX = 8     # chars — too-short threshold (matches mine's filter)


# ── Transcript scanning for exit-code / is_error signals ────────────────────

def _iter_jsonl(path: str):
    """Yield parsed JSON objects from a .jsonl file, skipping bad lines."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return


def scan_exit_code_signals(
    digests: List[SessionDigest],
) -> Dict[str, Any]:
    """Scan raw transcript files for Bash tool_result is_error signals.

    Returns a dict with:
      - total_bash_calls: total Bash tool calls across all sessions
      - bash_with_signal: Bash calls where is_error is a boolean (True/False)
      - bash_success: is_error == False
      - bash_error: is_error == True
      - bash_no_signal: is_error is None/missing
    """
    total_bash = 0
    bash_with_signal = 0
    bash_success = 0
    bash_error = 0
    bash_no_signal = 0
    files_scanned = 0

    for d in digests:
        path = d.raw_path
        if not path or not os.path.isfile(path):
            continue
        files_scanned += 1

        # Build tool_use_id -> tool_name mapping for this transcript
        tool_name_map: Dict[str, str] = {}
        for rec in _iter_jsonl(path):
            msg = rec.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("id") and b.get("name"):
                    tool_name_map[b["id"]] = b["name"]

        # Now scan tool_results
        for rec in _iter_jsonl(path):
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
                    if is_error:
                        bash_error += 1
                    else:
                        bash_success += 1
                else:
                    bash_no_signal += 1

    return {
        "files_scanned": files_scanned,
        "total_bash_calls": total_bash,
        "bash_with_signal": bash_with_signal,
        "bash_success": bash_success,
        "bash_error": bash_error,
        "bash_no_signal": bash_no_signal,
    }


# ── Analysis helpers ────────────────────────────────────────────────────────

def _pct(n: int, total: int) -> str:
    """Return percentage string like '42.5%'."""
    if total == 0:
        return "0.0%"
    return f"{n / total * 100:.1f}%"


def _is_actionable(intent: str) -> bool:
    """Check if an intent contains actionable keywords."""
    low = intent.lower()
    return any(kw in low for kw in _ACTIONABLE_KEYWORDS)


def analyze_task_quality(tasks: List[TaskRecord]) -> Dict[str, Any]:
    """Analyze intent quality metrics."""
    if not tasks:
        return {
            "avg_length": 0,
            "actionable": 0,
            "actionable_pct": "0.0%",
            "too_short": 0,
            "too_short_pct": "0.0%",
            "keyword_counts": {},
        }

    lengths = [len(t.intent) for t in tasks]
    avg_len = sum(lengths) / len(lengths)
    actionable = sum(1 for t in tasks if len(t.intent) > INTENT_ACTIONABLE_MIN and _is_actionable(t.intent))
    too_short = sum(1 for t in tasks if len(t.intent.strip()) < INTENT_TOO_SHORT_MAX)

    # Count keyword hits
    kw_counter: Counter = Counter()
    for t in tasks:
        low = t.intent.lower()
        for kw in _ACTIONABLE_KEYWORDS:
            if kw in low:
                kw_counter[kw] += 1

    total = len(tasks)
    return {
        "avg_length": avg_len,
        "actionable": actionable,
        "actionable_pct": _pct(actionable, total),
        "too_short": too_short,
        "too_short_pct": _pct(too_short, total),
        "keyword_counts": kw_counter.most_common(15),
    }


def analyze_reference_quality(tasks: List[TaskRecord]) -> Dict[str, Any]:
    """Analyze reference_kind distribution."""
    total = len(tasks)
    kinds = Counter(t.reference_kind for t in tasks)
    return {
        "total": total,
        "none": kinds.get("none", 0),
        "exact": kinds.get("exact", 0),
        "rubric": kinds.get("rubric", 0),
        "rule": kinds.get("rule", 0),
        "other": kinds.get("other", 0),
        "raw": dict(kinds),
    }


def analyze_outcome_distribution(tasks: List[TaskRecord]) -> Dict[str, Any]:
    """Analyze outcome distribution."""
    total = len(tasks)
    outcomes = Counter(t.outcome for t in tasks)
    return {
        "total": total,
        "success": outcomes.get("success", 0),
        "fail": outcomes.get("fail", 0),
        "mixed": outcomes.get("mixed", 0),
        "unknown": outcomes.get("unknown", 0),
    }


def analyze_split_distribution(tasks: List[TaskRecord]) -> Dict[str, Any]:
    """Analyze train/val split distribution."""
    total = len(tasks)
    splits = Counter(t.split for t in tasks)
    return {
        "total": total,
        "train": splits.get("train", 0),
        "val": splits.get("val", 0),
    }


def analyze_harvest_stats(digests: List[SessionDigest]) -> Dict[str, Any]:
    """Analyze harvest-level statistics."""
    total_sessions = len(digests)
    total_user_turns = sum(d.n_user_turns for d in digests)
    total_asst_turns = sum(d.n_assistant_turns for d in digests)

    # Count unique tools across all sessions
    all_tools: Counter = Counter()
    sessions_with_bash = 0
    for d in digests:
        for t in d.tools_used:
            all_tools[t] += 1
        if "Bash" in d.tools_used:
            sessions_with_bash += 1

    # Transcripts scanned = count unique raw_paths
    total_transcripts = len({d.raw_path for d in digests if d.raw_path})

    return {
        "total_sessions": total_sessions,
        "total_transcripts": total_transcripts,
        "total_user_turns": total_user_turns,
        "total_asst_turns": total_asst_turns,
        "sessions_with_bash": sessions_with_bash,
        "sessions_with_bash_pct": _pct(sessions_with_bash, total_sessions),
        "top_tools": all_tools.most_common(15),
    }


def count_bash_tasks(tasks: List[TaskRecord]) -> int:
    """Count tasks whose source sessions involved Bash."""
    count = 0
    for t in tasks:
        # Check tags for Bash indicator
        tags_str = " ".join(t.tags)
        if "Bash" in tags_str:
            count += 1
    return count


def count_bash_tasks_from_digests(
    tasks: List[TaskRecord],
    digests: List[SessionDigest],
) -> int:
    """Count tasks whose source sessions involved Bash (more accurate)."""
    # Build session_id -> has_bash map
    bash_sessions: set = set()
    for d in digests:
        if "Bash" in d.tools_used:
            bash_sessions.add(d.session_id)

    count = 0
    for t in tasks:
        if any(sid in bash_sessions for sid in t.source_sessions):
            count += 1
    return count


# ── Report generation ───────────────────────────────────────────────────────

def generate_conclusion(
    harvest_stats: Dict[str, Any],
    mine_stats: Dict[str, Any],
    ref_stats: Dict[str, Any],
    exit_stats: Dict[str, Any],
    quality_stats: Dict[str, Any],
    bash_task_count: int,
    total_tasks: int,
) -> str:
    """Generate an automated conclusion based on the analysis."""
    lines: List[str] = []

    # Reference quality assessment
    ref_none_pct = _pct(ref_stats["none"], ref_stats["total"]) if ref_stats["total"] else "100%"
    ref_exact_pct = _pct(ref_stats["exact"], ref_stats["total"]) if ref_stats["total"] else "0%"

    # Exit code availability
    bash_signal_pct = _pct(
        exit_stats["bash_with_signal"],
        exit_stats["total_bash_calls"],
    ) if exit_stats["total_bash_calls"] else "0%"
    bash_tasks_pct = _pct(bash_task_count, total_tasks) if total_tasks else "0%"

    # Actionable quality
    actionable_pct = quality_stats["actionable_pct"]

    # Overall assessment
    none_val = float(ref_none_pct.rstrip("%"))
    bash_signal_val = float(bash_signal_pct.rstrip("%"))

    lines.append("Based on the analysis above, here are the key findings:")
    lines.append("")

    # 1. Reference quality
    if none_val > 80:
        lines.append(
            f"1. **Reference quality is very low** — {ref_none_pct} of tasks have "
            f"reference_kind=none, meaning the current mine heuristic does not "
            f"extract ground-truth answers. This is expected for real coding "
            f"transcripts where 'correctness' is not self-evident from the session."
        )
    elif none_val > 50:
        lines.append(
            f"1. **Reference quality is low** — {ref_none_pct} of tasks have "
            f"reference_kind=none. Some ground-truth is available but not enough "
            f"for reliable exact-match scoring."
        )
    else:
        lines.append(
            f"1. **Reference quality is moderate** — {ref_none_pct} of tasks have "
            f"reference_kind=none. A reasonable proportion of tasks have extractable "
            f"references."
        )

    # 2. Exit code availability
    if bash_signal_val > 50:
        lines.append(
            f"2. **Exit-code scoring is VIABLE** — {bash_signal_pct} of Bash calls "
            f"have explicit is_error signals. Combined with {bash_tasks_pct} of tasks "
            f"involving Bash, exit-code-based grading can cover a significant portion "
            f"of tasks."
        )
    elif bash_signal_val > 20:
        lines.append(
            f"2. **Exit-code scoring is PARTIALLY viable** — {bash_signal_pct} of "
            f"Bash calls have is_error signals. Consider supplementing with test "
            f"pass/fail detection (pytest, unittest) for richer signals."
        )
    else:
        lines.append(
            f"2. **Exit-code scoring is NOT viable** — only {bash_signal_pct} of "
            f"Bash calls have is_error signals. The transcripts lack structured "
            f"success/failure markers for Bash commands. Alternative grading "
            f"approaches (LLM judge, test-based) should be used."
        )

    # 3. Task quality
    lines.append(
        f"3. **Task intent quality** — {actionable_pct} of tasks contain actionable "
        f"keywords, with an average intent length of {quality_stats['avg_length']:.0f} "
        f"chars. "
    )
    if float(actionable_pct.rstrip("%")) > 60:
        lines[-1] += "This indicates good quality, actionable task descriptions."
    else:
        lines[-1] += (
            "Some intents are too vague or short for precise grading."
        )

    # 4. Overall recommendation
    lines.append("")
    if bash_signal_val > 40 and float(actionable_pct.rstrip("%")) > 50:
        lines.append(
            "4. **Recommendation**: Exit-code-based scoring is feasible as a "
            "primary grading signal for Bash-heavy tasks. For tasks without "
            "Bash, supplement with LLM judge or structural similarity. Consider "
            "enhancing the mine() heuristic to extract reference answers from "
            "test assertions and build/lint output."
        )
    else:
        lines.append(
            "4. **Recommendation**: The current pipeline lacks sufficient "
            "structured grading signals. Consider (a) enhancing harvest to "
            "capture is_error for all tool results, (b) adding test-pass-rate "
            "detection in mine(), and (c) using LLM judge as the primary "
            "grading mechanism with exit-code as a secondary signal."
        )

    return "\n".join(lines)


def build_report(
    timestamp: str,
    harvest_stats: Dict[str, Any],
    outcome_stats: Dict[str, Any],
    split_stats: Dict[str, Any],
    ref_stats: Dict[str, Any],
    exit_stats: Dict[str, Any],
    quality_stats: Dict[str, Any],
    bash_task_count: int,
    total_tasks: int,
) -> str:
    """Build the full markdown report."""
    sections: List[str] = []

    sections.append(f"# Real Transcript Analysis Report")
    sections.append(f"Generated: {timestamp}")
    sections.append("")

    # Harvest
    sections.append("## Harvest")
    sections.append(f"- Total sessions: {harvest_stats['total_sessions']}")
    sections.append(f"- Total transcripts scanned: {harvest_stats['total_transcripts']}")
    sections.append(f"- Total user turns: {harvest_stats['total_user_turns']}")
    sections.append(f"- Total assistant turns: {harvest_stats['total_asst_turns']}")
    sections.append(f"- Sessions with Bash: {harvest_stats['sessions_with_bash']} ({harvest_stats['sessions_with_bash_pct']})")
    sections.append(f"- Top tools used:")
    for tname, cnt in harvest_stats["top_tools"][:10]:
        sections.append(f"  - `{tname}`: {cnt}")
    sections.append("")

    # Mine
    sections.append("## Mine")
    sections.append(f"- Total tasks: {outcome_stats['total']}")
    sections.append(f"- Train: {split_stats['train']} / Val: {split_stats['val']}")
    sections.append(
        f"- Outcome distribution: "
        f"success={outcome_stats['success']} "
        f"fail={outcome_stats['fail']} "
        f"mixed={outcome_stats['mixed']} "
        f"unknown={outcome_stats['unknown']}"
    )
    # Outcome percentages
    if outcome_stats["total"]:
        for key in ("success", "fail", "mixed", "unknown"):
            val = outcome_stats[key]
            sections.append(f"  - {key}: {val} ({_pct(val, outcome_stats['total'])})")
    sections.append("")

    # Reference quality
    sections.append("## Reference Quality (KEY METRIC)")
    total_ref = ref_stats["total"] or 1
    sections.append(f"- reference_kind=none: {ref_stats['none']} ({_pct(ref_stats['none'], total_ref)})")
    sections.append(f"- reference_kind=exact: {ref_stats['exact']} ({_pct(ref_stats['exact'], total_ref)})")
    sections.append(f"- reference_kind=rubric: {ref_stats['rubric']} ({_pct(ref_stats['rubric'], total_ref)})")
    sections.append(f"- reference_kind=rule: {ref_stats['rule']} ({_pct(ref_stats['rule'], total_ref)})")
    sections.append(f"- reference_kind=other: {ref_stats['other']} ({_pct(ref_stats['other'], total_ref)})")
    sections.append("")

    # Exit code availability
    sections.append("## Exit Code Availability")
    bash_tasks_pct = _pct(bash_task_count, total_tasks) if total_tasks else "0%"
    sections.append(f"- Tasks involving Bash: {bash_task_count} ({bash_tasks_pct})")
    sections.append(f"- Total Bash calls scanned: {exit_stats['total_bash_calls']}")
    sections.append(f"- Bash calls with is_error signal: {exit_stats['bash_with_signal']} ({_pct(exit_stats['bash_with_signal'], exit_stats['total_bash_calls'] or 1)})")
    sections.append(f"  - is_error=False (success): {exit_stats['bash_success']}")
    sections.append(f"  - is_error=True (error): {exit_stats['bash_error']}")
    sections.append(f"- Bash calls WITHOUT signal: {exit_stats['bash_no_signal']} ({_pct(exit_stats['bash_no_signal'], exit_stats['total_bash_calls'] or 1)})")
    sections.append(f"- Transcript files scanned for signals: {exit_stats['files_scanned']}")
    sections.append("")

    # Task intent quality
    sections.append("## Task Intent Quality")
    sections.append(f"- Average intent length: {quality_stats['avg_length']:.1f} chars")
    sections.append(f"- Tasks with actionable intent (>20 chars + keyword): {quality_stats['actionable']} ({quality_stats['actionable_pct']})")
    sections.append(f"- Tasks too short (<{INTENT_TOO_SHORT_MAX} chars): {quality_stats['too_short']} ({quality_stats['too_short_pct']})")
    if quality_stats["keyword_counts"]:
        sections.append("- Top actionable keywords found:")
        for kw, cnt in quality_stats["keyword_counts"][:10]:
            sections.append(f"  - `{kw}`: {cnt}")
    sections.append("")

    # Conclusion
    sections.append("## Conclusion")
    sections.append("")
    conclusion = generate_conclusion(
        harvest_stats, outcome_stats, ref_stats, exit_stats,
        quality_stats, bash_task_count, total_tasks,
    )
    sections.append(conclusion)
    sections.append("")

    return "\n".join(sections)


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[analyze_real] Starting analysis at {timestamp}", file=sys.stderr)
    print(f"[analyze_real] Scanning: {CLAUDE_PROJECTS_DIR}", file=sys.stderr)

    # ── Step 1: Harvest ──
    print("[analyze_real] Running harvest()...", file=sys.stderr)
    digests = harvest(
        CLAUDE_PROJECTS_DIR,
        scope=HARVEST_SCOPE,
        limit=HARVEST_LIMIT,
    )
    print(f"[analyze_real] Harvest complete: {len(digests)} sessions", file=sys.stderr)

    # ── Step 2: Mine ──
    print("[analyze_real] Running mine()...", file=sys.stderr)
    tasks = mine(digests, max_tasks=500, seed=42)
    print(f"[analyze_real] Mine complete: {len(tasks)} tasks", file=sys.stderr)

    # ── Step 3: Analyze ──
    print("[analyze_real] Analyzing harvest stats...", file=sys.stderr)
    harvest_stats = analyze_harvest_stats(digests)

    print("[analyze_real] Analyzing outcome distribution...", file=sys.stderr)
    outcome_stats = analyze_outcome_distribution(tasks)

    print("[analyze_real] Analyzing split distribution...", file=sys.stderr)
    split_stats = analyze_split_distribution(tasks)

    print("[analyze_real] Analyzing reference quality...", file=sys.stderr)
    ref_stats = analyze_reference_quality(tasks)

    print("[analyze_real] Analyzing exit-code signals (scanning transcripts)...", file=sys.stderr)
    exit_stats = scan_exit_code_signals(digests)

    print("[analyze_real] Analyzing task quality...", file=sys.stderr)
    quality_stats = analyze_task_quality(tasks)

    bash_task_count = count_bash_tasks_from_digests(tasks, digests)

    # ── Step 4: Build report ──
    print("[analyze_real] Building report...", file=sys.stderr)
    report = build_report(
        timestamp=timestamp,
        harvest_stats=harvest_stats,
        outcome_stats=outcome_stats,
        split_stats=split_stats,
        ref_stats=ref_stats,
        exit_stats=exit_stats,
        quality_stats=quality_stats,
        bash_task_count=bash_task_count,
        total_tasks=len(tasks),
    )

    # ── Step 5: Output ──
    # Print to stdout
    print(report)

    # Write to file
    # data/ is relative to project root (parent of scripts/)
    project_root = _SCRIPTS_DIR.parent
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    report_path = data_dir / "real_analysis_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\n[analyze_real] Report saved to: {report_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
