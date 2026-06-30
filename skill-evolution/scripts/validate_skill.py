#!/usr/bin/env python3
"""PostToolUse hook — validate & provenance-stamp learned SKILL.md files.

Checks frontmatter correctness, stamps provenance, and emits non-blocking
advisories for quality issues (e.g. over-long descriptions).
Silent for non-skill edits.
"""

import json
import os
import re
import sys

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
PROVENANCE = "evolving-skills"
MAX_NAME = 64
MAX_DESC = 1024
DESC_WARN = 500
MAX_CONTENT = 100000
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import usage_store
except Exception:
    usage_store = None


def _is_skill_path(p):
    norm = str(p or "").replace("\\", "/")
    return "/.claude/skills/" in norm and norm.endswith("SKILL.md")


def _split_frontmatter(text):
    if not text.startswith("---"):
        return None, None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def _scalar(fm, key):
    m = re.match(
        rf"^{re.escape(key)}\s*:\s*(.*)$", fm, re.MULTILINE
    )
    if not m:
        return None
    val = m.group(1).strip()
    if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
        val = val[1:-1]
    return val


def validate(text):
    problems = []
    if len(text) > MAX_CONTENT:
        problems.append(
            f"File too large (>{MAX_CONTENT} chars). Move content to references/."
        )
    fm, body = _split_frontmatter(text)
    if fm is None:
        problems.append("Missing YAML frontmatter. Must start with --- and close with ---.")
        return problems
    name = _scalar(fm, "name")
    if not name:
        problems.append("Frontmatter missing `name`.")
    else:
        if len(name) > MAX_NAME:
            problems.append(f"`name` exceeds {MAX_NAME} chars.")
        if not NAME_RE.match(name):
            problems.append(
                "`name` must use lowercase letters, digits, hyphens only."
            )
    desc = _scalar(fm, "description")
    if not desc:
        problems.append(
            "Frontmatter missing `description` (critical for skill trigger)."
        )
    elif len(desc) > MAX_DESC:
        problems.append("`description` too long.")
    if not body or not body.strip():
        problems.append("Missing body after frontmatter.")
    return problems


def advisory_for(text):
    fm, _ = _split_frontmatter(text)
    if not fm:
        return None
    notes = []
    desc = _scalar(fm, "description") or ""
    if len(desc) > DESC_WARN:
        notes.append(
            f"description is {len(desc)} chars. Learned skill descriptions "
            f"enter every session's system prompt — please compress to "
            f"under {DESC_WARN} while keeping trigger phrases."
        )
    return "\n".join(f"- {n}" for n in notes) if notes else None


def stamp_provenance(path, text):
    try:
        if PROVENANCE in text:
            return text
        fm, body = _split_frontmatter(text)
        if fm is None or body is None:
            return text
        if re.search(r"^metadata\s*:", fm, re.MULTILINE):
            if "provenance:" not in fm:
                fm = fm.rstrip() + f"\n  provenance: {PROVENANCE}\n"
            if "origin:" not in fm:
                fm = fm.rstrip() + "  origin: distilled\n"
        else:
            fm = fm.rstrip() + (
                f"\nmetadata:\n  provenance: {PROVENANCE}\n  origin: distilled\n"
            )
        return f"---\n{fm}\n---\n{body}"
    except Exception:
        return text


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
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return

    problems = validate(text)
    if problems:
        # Try rollback from backup
        backup_dir = os.path.expanduser("~/.evolving-skills/skill_backups")
        name = os.path.basename(os.path.dirname(file_path))
        try:
            backups = sorted(
                f for f in os.listdir(backup_dir) if f.startswith(f"{name}_")
            )
            if backups:
                import shutil

                shutil.copy2(
                    os.path.join(backup_dir, backups[-1]), file_path
                )
        except Exception:
            pass
        # Emit advisory (non-blocking)
        msg = "[evolving-skills] SKILL.md validation failed, rolled back:\n- " + \
              "\n- ".join(problems)
        sys.stdout.write(json.dumps({"advisory": msg}))
        return

    # Stamp provenance
    new_text = stamp_provenance(file_path, text)
    if new_text != text:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_text)
        except Exception:
            pass

    # Record patch in telemetry
    if usage_store is not None:
        try:
            name = os.path.basename(os.path.dirname(file_path))
            usage_store.apply_events([(name, "patch", "agent")])
        except Exception:
            pass

    # Non-blocking advisory
    adv = advisory_for(text)
    if adv:
        sys.stdout.write(
            json.dumps({"advisory": f"[evolving-skills] Advisory:\n{adv}"})
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
