#!/usr/bin/env python3
"""PreToolUse hook — back up a learned SKILL.md before edit.

Reads the PreToolUse payload on stdin, checks if the target file is a
SKILL.md under ~/.claude/skills, and if so copies it to a backup dir.
Silent for non-skill edits; never blocks.
"""

import json
import os
import shutil
import sys
import time

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
BACKUP_DIR = os.path.expanduser("~/.evolving-skills/skill_backups")


def _is_skill_path(p):
    norm = str(p or "").replace("\\", "/")
    return "/.claude/skills/" in norm and norm.endswith("SKILL.md")


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path") or tool_input.get("path", "")

    if not _is_skill_path(file_path):
        return

    if not os.path.isfile(file_path):
        return

    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        ts = time.strftime("%Y%m%dT%H%M%S")
        name = os.path.basename(os.path.dirname(file_path))
        dst = os.path.join(BACKUP_DIR, f"{name}_{ts}.md")
        shutil.copy2(file_path, dst)

        # Keep only last 20 backups
        backups = sorted(
            f for f in os.listdir(BACKUP_DIR) if f.startswith(f"{name}_")
        )
        for old in backups[:-20]:
            try:
                os.remove(os.path.join(BACKUP_DIR, old))
            except Exception:
                pass
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
