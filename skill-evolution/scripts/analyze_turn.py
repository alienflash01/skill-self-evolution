#!/usr/bin/env python3
"""Stop-hook analyzer for evolving-skills.

Reads the Claude Code Stop-hook payload on stdin, measures how many tool calls
and file edits have accumulated since the last skill-distillation "anchor",
and emits a Stop-hook decision. If the work looks substantial and hasn't been
distilled, it BLOCKs and instructs the agent to delegate to skill-distiller.

Fails safe to {"decision":"approve"} on ANY error.
"""

import json
import os
import re
import sys
from typing import NoReturn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import usage_store
except Exception:
    usage_store = None

SKILL_MARKER = "skill-distiller"
EDIT_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")
SKILLS_DIR = os.path.expanduser("~/.claude/skills")


def emit(obj) -> NoReturn:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()
    sys.exit(0)


def approve() -> NoReturn:
    emit({"decision": "approve"})


def _int_env(name, default):
    try:
        return int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        return default


def _tool_uses(row):
    if not isinstance(row, dict) or row.get("type") != "assistant":
        return
    msg = row.get("message")
    if not isinstance(msg, dict):
        return
    content = msg.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block


def _is_skill_path(file_path):
    norm = str(file_path or "").replace("\\", "/")
    return "/.claude/skills/" in norm and norm.endswith("SKILL.md")


def _learned_skill_names():
    names = set()
    try:
        for entry in os.listdir(SKILLS_DIR):
            if entry.startswith("."):
                continue
            if os.path.isfile(os.path.join(SKILLS_DIR, entry, "SKILL.md")):
                names.add(entry)
    except Exception:
        pass
    return names


def _seed_created_by(name):
    try:
        safe = os.path.basename(str(name))
        with open(
            os.path.join(SKILLS_DIR, safe, "SKILL.md"),
            encoding="utf-8",
            errors="ignore",
        ) as fh:
            head = fh.read(2048)
        if re.search(r"origin\s*:\s*distilled", head) or (
            "provenance: evolving-skills" in head
            or "provenance: self-improving-skills" in head
        ):
            return "agent"
    except Exception:
        pass
    return "user"


def _capture_telemetry(rows, session_id):
    if usage_store is None:
        return
    learned = _learned_skill_names()
    try:
        usage_store.forget_missing(learned)
    except Exception:
        pass

    offset = 0
    try:
        offset = usage_store.get_offset(session_id)
    except Exception:
        offset = 0
    if offset < 0 or offset > len(rows):
        offset = 0

    events = []
    if learned:
        cb_cache = {}

        def _cb(name):
            if name not in cb_cache:
                cb_cache[name] = _seed_created_by(name)
            return cb_cache[name]

        maintenance = False
        for row in rows[offset:]:
            for tu in _tool_uses(row):
                if tu.get("name") == "Skill":
                    raw_inp = tu.get("input")
                    inp = raw_inp if isinstance(raw_inp, dict) else {}
                    sk = str(inp.get("skill", "")).split(":")[-1]
                    if sk in ("curate-skills", "curator-status"):
                        maintenance = True
                        break
            if maintenance:
                break

        for row in rows[offset:]:
            for tu in _tool_uses(row):
                name = tu.get("name")
                raw_inp = tu.get("input")
                inp = raw_inp if isinstance(raw_inp, dict) else {}
                if name == "Skill":
                    sk = str(inp.get("skill", "")).split(":")[-1]
                    if sk in learned:
                        events.append((sk, "use", _cb(sk)))
                elif name == "Read" and not maintenance:
                    fp = inp.get("file_path", "")
                    if _is_skill_path(fp):
                        norm = str(fp).replace("\\", "/")
                        parts = norm.replace("/SKILL.md", "").split("/")
                        sn = parts[-1] if parts else None
                        if sn in learned:
                            events.append((sn, "view", _cb(sn)))
    try:
        usage_store.apply_events(events, session_id, len(rows))
    except Exception:
        pass


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        approve()

    if payload.get("stop_hook_active"):
        approve()

    path = payload.get("transcript_path") or ""
    if not path or not os.path.isfile(path):
        approve()

    threshold = _int_env("SIS_DISTILL_THRESHOLD", 12)
    min_edits = _int_env("SIS_MIN_FILE_EDITS", 2)

    rows = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        approve()

    session_id = str(payload.get("session_id") or os.path.basename(path))

    try:
        _capture_telemetry(rows, session_id)
    except Exception:
        pass

    # Find last distillation anchor
    anchor = -1
    for i, row in enumerate(rows):
        for tu in _tool_uses(row):
            name = tu.get("name")
            raw_inp = tu.get("input")
            inp = raw_inp if isinstance(raw_inp, dict) else {}
            subagent_type = str(inp.get("subagent_type", ""))
            if SKILL_MARKER in subagent_type:
                anchor = i
            elif name in EDIT_TOOLS and _is_skill_path(inp.get("file_path")):
                anchor = i

    # Nudge-once guard
    nudged_rows = 0
    if usage_store is not None:
        try:
            nudged_rows = usage_store.get_nudge_row(session_id)
        except Exception:
            nudged_rows = 0
    if nudged_rows > len(rows):
        nudged_rows = 0
    start = max(anchor + 1, nudged_rows)

    # Count work since anchor
    total_calls = 0
    file_edits = 0
    for row in rows[start:]:
        for tu in _tool_uses(row):
            total_calls += 1
            name = tu.get("name")
            if name in EDIT_TOOLS:
                file_edits += 1

    nudge_fires = total_calls >= threshold and file_edits >= min_edits
    if nudge_fires:
        if usage_store is not None:
            try:
                usage_store.record_nudge(session_id, len(rows))
            except Exception:
                pass
        reason = (
            f"This work segment accumulated {total_calls} tool calls "
            f"({file_edits} file edits) and hasn't been distilled yet. "
            f"Before stopping, run /distill-skill or delegate to the "
            f'skill-distiller subagent '
            f'(subagent_type="evolving-skills:skill-distiller") '
            f"with run_in_background=true to capture reusable techniques "
            f"from this session into ~/.claude/skills.\n\n"
            f"Include this session's transcript path in the prompt so the "
            f"distiller can read what actually happened: {path}\n\n"
            f"Principles:\n"
            f"- Prefer patching an existing skill over creating a new one.\n"
            f"- Skip one-off tasks (specific PR, specific bug, env workaround).\n"
            f"- If distillation is unnecessary, tell the user in one line and stop."
        )
        emit({"decision": "block", "reason": reason})

    approve()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        approve()
