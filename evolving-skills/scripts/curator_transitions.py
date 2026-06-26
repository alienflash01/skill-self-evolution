#!/usr/bin/env python3
"""Time-based skill lifecycle state machine — the periodic pruning of unused skills.

Reads usage telemetry and moves each agent-distilled, unpinned skill through
active → stale → archived based on idle days:

    idle >= SIS_ARCHIVE_AFTER_DAYS (default 90)  → archived (moved to .archive/)
    idle >= SIS_STALE_AFTER_DAYS   (default 30)  → stale
    was stale but idle < stale cutoff            → reactivated to active

NEVER touches:
  - skills with created_by != "agent" (user-authored / team)
  - pinned skills
  - already-archived skills

Archiving moves to ~/.claude/skills/.archive/<name> (recoverable), never deletes.
Pure/deterministic — no LLM.
"""

import os
import re
import shutil
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import usage_store  # noqa: E402

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
ARCHIVE_DIR = os.path.join(SKILLS_DIR, ".archive")
STATE_DIR = os.path.expanduser("~/.evolving-skills")
LOG_DIR = os.path.join(STATE_DIR, "logs", "curator")


def _int_env(name, default):
    try:
        return int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        return default


def _now():
    return datetime.now(timezone.utc)


def _parse(ts):
    if not ts:
        return None
    try:
        d = datetime.fromisoformat(str(ts))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d
    except Exception:
        return None


def _frontmatter_pinned(name):
    try:
        with open(
            os.path.join(SKILLS_DIR, name, "SKILL.md"),
            encoding="utf-8",
            errors="ignore",
        ) as fh:
            return bool(
                re.search(r"^\s*pinned\s*:\s*true", fh.read(2048), re.I | re.M)
            )
    except Exception:
        return False


def _learned_names():
    names = set()
    try:
        for e in os.listdir(SKILLS_DIR):
            if e.startswith("."):
                continue
            if os.path.isfile(os.path.join(SKILLS_DIR, e, "SKILL.md")):
                names.add(e)
    except Exception:
        pass
    return names


def _archive_dir(name):
    src = os.path.join(SKILLS_DIR, name)
    if not os.path.isdir(src):
        return
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    dst = os.path.join(ARCHIVE_DIR, name)
    if os.path.exists(dst):
        dst = dst + "." + _now().strftime("%Y%m%dT%H%M%SZ")
    try:
        shutil.move(src, dst)
    except Exception:
        pass


def restore(name):
    src = os.path.join(ARCHIVE_DIR, name)
    dst = os.path.join(SKILLS_DIR, name)
    if not os.path.isdir(src) or os.path.exists(dst):
        return False
    try:
        shutil.move(src, dst)
        usage_store.set_fields(name, state="active")
        return True
    except Exception:
        return False


def _idle_days(rec, now):
    latest = None
    for k in ("last_used_at", "last_viewed_at", "last_patched_at"):
        d = _parse(rec.get(k))
        if d and (latest is None or d > latest):
            latest = d
    anchor = latest or _parse(rec.get("created_at")) or now
    return (now - anchor).days


def _use_count(rec):
    try:
        return int(rec.get("use_count", 0) or 0)
    except (TypeError, ValueError):
        return 0


def _archive_days_for(rec, base_days):
    if _use_count(rec) >= 3:
        return base_days * 2
    return base_days


def archive_one(name, absorbed_into=None, dry_run=False):
    src = os.path.join(SKILLS_DIR, name)
    if not os.path.isdir(src):
        return {"name": name, "ok": False, "reason": "not found"}
    if dry_run:
        return {"name": name, "ok": True, "dry_run": True}
    _archive_dir(name)
    fields = {"state": "archived"}
    if absorbed_into is not None:
        fields["absorbed_into"] = absorbed_into
    usage_store.set_fields(name, **fields)
    return {"name": name, "ok": True, "absorbed_into": absorbed_into}


def run(dry_run=False):
    stale_days = _int_env("SIS_STALE_AFTER_DAYS", 30)
    archive_days = _int_env("SIS_ARCHIVE_AFTER_DAYS", 90)
    now = _now()
    records = usage_store.all_records()
    learned = _learned_names()
    summary = {
        "stale": [],
        "archived": [],
        "reactivated": [],
        "skipped_pinned": [],
        "skipped_user": [],
        "stale_days": stale_days,
        "archive_days": archive_days,
        "dry_run": dry_run,
        "ran_at": now.replace(microsecond=0).isoformat(),
    }

    for name in sorted(learned):
        rec = records.get(name, {})
        if rec.get("created_by", "agent") != "agent":
            summary["skipped_user"].append(name)
            continue
        if rec.get("pinned") or _frontmatter_pinned(name):
            summary["skipped_pinned"].append(name)
            continue
        if rec.get("state") == "archived":
            continue
        idle = _idle_days(rec, now)
        if idle >= _archive_days_for(rec, archive_days):
            summary["archived"].append({"name": name, "idle_days": idle})
            if not dry_run:
                _archive_dir(name)
                usage_store.set_fields(name, state="archived")
        elif idle >= stale_days:
            if rec.get("state") != "stale":
                summary["stale"].append({"name": name, "idle_days": idle})
                if not dry_run:
                    usage_store.set_fields(name, state="stale")
        else:
            if rec.get("state") == "stale":
                summary["reactivated"].append(name)
                if not dry_run:
                    usage_store.set_fields(name, state="active")

    _write_report(summary)
    return summary


def _write_report(summary):
    try:
        ts = _now().strftime("%Y%m%dT%H%M%SZ")
        d = os.path.join(LOG_DIR, ts)
        os.makedirs(d, exist_ok=True)
        prefix = "[DRY-RUN] " if summary["dry_run"] else ""
        lines = [
            f"# {prefix}Curator transition report",
            "",
            f"- ran_at: {summary['ran_at']}",
            f"- thresholds: stale>={summary['stale_days']}d, archive>={summary['archive_days']}d",
            f"- archived: {len(summary['archived'])} | stale: {len(summary['stale'])} | reactivated: {len(summary['reactivated'])}",
            f"- skipped (pinned): {len(summary['skipped_pinned'])} | skipped (user): {len(summary['skipped_user'])}",
            "",
        ]
        if summary["archived"]:
            lines.append("## Archived (moved to .archive/)")
            lines += [f"- {x['name']} (idle {x['idle_days']}d)" for x in summary["archived"]]
            lines.append("")
        if summary["stale"]:
            lines.append("## Marked stale")
            lines += [f"- {x['name']} (idle {x['idle_days']}d)" for x in summary["stale"]]
        with open(os.path.join(d, "REPORT.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
    except Exception:
        pass


if __name__ == "__main__":
    import json

    args = sys.argv[1:]
    if args and args[0] == "restore" and len(args) >= 2:
        print(json.dumps({"restored": args[1], "ok": restore(args[1])}))
    elif args and args[0] == "archive" and len(args) >= 2:
        absorbed = args[2] if len(args) >= 3 else None
        print(json.dumps(archive_one(args[1], absorbed_into=absorbed, dry_run=("--dry-run" in args))))
    else:
        print(json.dumps(run(dry_run=("--dry-run" in args)), ensure_ascii=False, indent=2))
