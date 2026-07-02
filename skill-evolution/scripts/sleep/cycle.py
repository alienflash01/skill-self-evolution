"""Offline sleep engine — the six-stage cycle orchestrator.

harvest → mine → replay → consolidate(gate) → stage → (optional adopt)

With backend="mock" (default) it runs with NO API key and NO external deps.
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import List, Optional

# Ensure local imports work when run as a script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sleep.consolidate import consolidate
from sleep.harvest import harvest as do_harvest
from sleep.memory import ensure_skill_scaffold
from sleep.mine import mine as do_mine
from sleep.replay import Backend, MockBackend, replay_batch, aggregate_scores
from sleep.staging import adopt as adopt_staging, write_staging
from sleep.state import SleepState
from sleep.models import SleepReport, TaskRecord

CLAUDE_HOME = os.path.expanduser("~/.claude")
STATE_DIR = os.path.expanduser("~/.evolving-skills")


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _render_report_md(report: SleepReport) -> str:
    lines = [
        f"# Evolving-Skills — night {report.night} report",
        "",
        f"- project: `{report.project}`",
        f"- sessions harvested: {report.n_sessions}",
        f"- tasks mined: {report.n_tasks} (replayed: {report.n_replayed})",
        f"- held-out score: {report.baseline_score:.3f} → {report.candidate_score:.3f}",
        f"- gate: **{report.gate_action}** (accepted={report.accepted})",
        "",
    ]
    if report.edits:
        lines.append("## Accepted edits")
        for e in report.edits:
            lines.append(f"- [{e.target}/{e.op}] {e.content}")
        lines.append("")
    if report.rejected_edits:
        lines.append("## Rejected by gate")
        for e in report.rejected_edits:
            lines.append(f"- [{e.target}/{e.op}] {e.content}")
        lines.append("")
    lines.append("_Run `/sleep adopt` to apply, or discard._")
    return "\n".join(lines)


def run_sleep_cycle(
    project: Optional[str] = None,
    *,
    dry_run: bool = False,
    backend_name: str = "mock",
    lookback_hours: int = 72,
    max_tasks: int = 40,
    edit_budget: int = 4,
    auto_adopt: bool = False,
) -> dict:
    project = project or os.getcwd()
    state = SleepState.load()
    night = state.begin_night()

    # Select backend
    if backend_name == "mock":
        backend = MockBackend()
    elif backend_name == "cc":
        from sleep.cc_backend import CCBackend
        backend = CCBackend()
    else:
        backend = MockBackend()

    # Live files
    live_memory_path = os.path.join(project, "CLAUDE.md")
    live_skill_path = os.path.join(CLAUDE_HOME, "skills", "evolving-skills-learned", "SKILL.md")
    raw_skill = _read(live_skill_path)
    skill = raw_skill or ensure_skill_scaffold(
        "", name="evolving-skills-learned",
        description="Learned from past sessions.",
    )
    memory = _read(live_memory_path)

    # 1. Harvest
    since = state.last_harvest_for(project)
    if since is None and lookback_hours > 0:
        since = time.strftime("%Y-%m-%dT%H:%M:%S",
                              time.localtime(time.time() - lookback_hours * 3600))

    transcripts_dir = os.path.join(CLAUDE_HOME, "projects")
    digests = do_harvest(transcripts_dir, scope="all", since_iso=since, limit=max_tasks * 3)
    n_sessions = len(digests)

    # 2. Mine
    tasks = do_mine(digests, max_tasks=max_tasks)

    report = SleepReport(
        night=night, project=project, started_at=_now_iso(),
        n_sessions=n_sessions, n_tasks=len(tasks),
    )

    if not tasks:
        report.ended_at = _now_iso()
        report.notes.append("no tasks mined — nothing to consolidate")
        state.set_last_harvest(project, report.started_at)
        state.record_night({"night": night, "accepted": False, "n_tasks": 0})
        if not dry_run:
            state.save()
        return {"status": "noop", "report": report.to_dict()}

    # 3+4. Replay + Consolidate (gate)
    result = consolidate(
        backend, tasks, skill, memory,
        edit_budget=edit_budget,
    )

    report.n_replayed = len(tasks)
    report.baseline_score = result.baseline_score
    report.candidate_score = result.candidate_score
    report.accepted = result.accepted
    report.gate_action = result.gate_action
    report.edits = result.applied_edits
    report.rejected_edits = result.rejected_edits
    report.ended_at = _now_iso()

    # 5. Stage
    staging_dir = ""
    adopted = False
    if not dry_run:
        report_md = _render_report_md(report)
        proposed_skill = result.new_skill if result.accepted else None
        proposed_memory = result.new_memory if result.accepted else None
        staging_dir = write_staging(
            project, report=report,
            proposed_skill=proposed_skill, proposed_memory=proposed_memory,
            live_skill_path=live_skill_path, live_memory_path=live_memory_path,
            report_md=report_md,
        )
        state.set_last_harvest(project, report.started_at)
        state.record_night({
            "night": night, "accepted": result.accepted,
            "baseline": result.baseline_score, "candidate": result.candidate_score,
            "n_tasks": len(tasks), "staging": staging_dir,
            "ran_at": _now_iso(),
        })

        # 6. Adopt (opt-in)
        if auto_adopt and result.accepted:
            adopt_staging(staging_dir)
            adopted = True

        state.save()

    # Evolution tree
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from evolution_tree import append_node
        append_node(
            source="offline",
            changes=[
                {"target": e.target, "op": e.op, "content": e.content,
                 "gate": "accept" if result.accepted else "reject"}
                for e in result.applied_edits
            ],
            metrics={
                "night": night, "tasks": len(tasks),
                "baseline": result.baseline_score, "candidate": result.candidate_score,
            },
        )
    except Exception:
        pass

    return {
        "status": "ok",
        "night": night,
        "accepted": result.accepted,
        "baseline": result.baseline_score,
        "candidate": result.candidate_score,
        "edits": len(result.applied_edits),
        "rejected": len(result.rejected_edits),
        "staging_dir": staging_dir,
        "adopted": adopted,
        "report": report.to_dict(),
    }


def run_sleep_cycle_cli():
    """CLI entry point: python -c 'from cycle import ...' -- args"""
    import argparse

    parser = argparse.ArgumentParser(description="Evolving-Skills sleep cycle")
    parser.add_argument("action", nargs="?", default="status",
                        choices=["run", "dry-run", "status", "adopt", "harvest"])
    parser.add_argument("--project", default=None)
    parser.add_argument("--scope", default="invoked")
    parser.add_argument("--backend", default="mock")
    parser.add_argument("--lookback-hours", type=int, default=72)
    parser.add_argument("--max-tasks", type=int, default=40)
    parser.add_argument("--edit-budget", type=int, default=4)
    parser.add_argument("--auto-adopt", action="store_true")
    parser.add_argument("--json", action="store_true")

    # Parse known args (run-sleep.sh passes action as first positional)
    args, _unknown = parser.parse_known_args()

    if args.action == "status":
        state = SleepState.load()
        print(json.dumps({
            "night": state.night,
            "last_run": state.last_run,
            "history_count": len(state.data.get("history", [])),
        }, indent=2))
        return

    if args.action == "adopt":
        from sleep.staging import adopt, latest_staging
        project = args.project or os.getcwd()
        staging = latest_staging(project)
        if not staging:
            print("No staged proposal to adopt.")
            return
        updated = adopt(staging)
        print(f"Adopted: {updated}")
        return

    if args.action == "harvest":
        transcripts_dir = os.path.join(CLAUDE_HOME, "projects")
        digests = do_harvest(transcripts_dir, limit=20)
        for d in digests[:5]:
            print(f"  {d.session_id}: {d.n_user_turns} turns, {d.n_assistant_turns} asst")
        print(f"Total: {len(digests)} sessions")
        return

    # run / dry-run
    result = run_sleep_cycle(
        project=args.project,
        dry_run=(args.action == "dry-run"),
        backend_name=args.backend,
        lookback_hours=args.lookback_hours,
        max_tasks=args.max_tasks,
        edit_budget=args.edit_budget,
        auto_adopt=args.auto_adopt,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        r = result.get("report", {})
        print(f"Night {result.get('night', '?')}: "
              f"baseline={result.get('baseline', 0):.3f} → "
              f"candidate={result.get('candidate', 0):.3f} "
              f"gate={'accept' if result.get('accepted') else 'reject'} "
              f"edits={result.get('edits', 0)}")
        if result.get("staging_dir"):
            print(f"Staged: {result['staging_dir']}")
            print("Run /sleep adopt to apply.")
