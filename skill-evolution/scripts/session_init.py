#!/usr/bin/env python3
"""SessionStart hook — inject self-improvement context.

Reads skill library status and emits additionalContext for the session.
Fails safe to silent.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import usage_store
except Exception:
    usage_store = None

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
STATE_DIR = os.path.expanduser("~/.evolving-skills")


def _learned_count():
    count = 0
    try:
        for entry in os.listdir(SKILLS_DIR):
            if entry.startswith("."):
                continue
            if os.path.isfile(os.path.join(SKILLS_DIR, entry, "SKILL.md")):
                count += 1
    except Exception:
        pass
    return count


def _stale_count():
    if usage_store is None:
        return 0
    try:
        records = usage_store.all_records()
        return sum(
            1
            for r in records.values()
            if r.get("state") == "stale" and r.get("created_by") == "agent"
        )
    except Exception:
        return 0


def _last_sleep():
    state_path = os.path.join(STATE_DIR, "sleep_state.json")
    try:
        import json as j

        with open(state_path) as f:
            data = j.load(f)
        return data.get("night", 0), data.get("last_run", "never")
    except Exception:
        return 0, "never"


def main():
    learned = _learned_count()
    stale = _stale_count()
    night, last_run = _last_sleep()

    parts = []
    if learned > 0:
        parts.append(
            f"[evolving-skills] {learned} learned skill(s) loaded. "
            f"{stale} stale."
        )
    if night > 0:
        parts.append(f"Last sleep cycle: night {night} ({last_run}).")
    parts.append(
        "Complex work will trigger a distillation nudge. "
        "Run /sleep status to check offline evolution."
    )

    context = "\n".join(parts)
    sys.stdout.write(
        json.dumps({"additionalContext": context})
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
