#!/usr/bin/env python3
"""
PostToolUse Hook for Agent Experience Distillation

Called by Claude Code after every tool execution. Records tool-call traces
and detects fail→success patterns in real time.

Claude Code passes hook context as JSON via stdin:
{
  "tool_name": "Bash",
  "tool_input": {"command": "..."},
  "tool_output": "...",
  "is_error": false,
  "session_id": "...",
  "cwd": "..."
}

This hook is NON-BLOCKING: it writes to a trace file and exits immediately.
The actual pattern detection runs at the moment a retry succeeds, comparing
against the previous call in the same session.

Exit code 0 = don't modify Claude's behavior.
"""

import json
import os
import sys
import time
from pathlib import Path

# Resolve paths relative to this file
HOOK_DIR = Path(__file__).resolve().parent
PLUGIN_DIR = HOOK_DIR.parent
DATA_DIR = PLUGIN_DIR / "data"
TRACES_DIR = DATA_DIR / "traces"


def main() -> None:
    # Read hook context from stdin
    try:
        raw = sys.stdin.read()
        ctx = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        ctx = {}

    tool_name = ctx.get("tool_name", "")
    tool_input = ctx.get("tool_input", {})
    tool_output = ctx.get("tool_output", "")
    is_error = ctx.get("is_error", False)
    session_id = ctx.get("session_id", "unknown")
    cwd = ctx.get("cwd", "")

    # Skip non-actionable tools
    if tool_name not in ("Bash", "Write", "Edit", "Read", "MultiEdit"):
        return

    # Write trace record
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    trace_file = TRACES_DIR / f"{session_id}.jsonl"

    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tool": tool_name,
        "input": tool_input,
        "output": tool_output[:2000] if isinstance(tool_output, str) else str(tool_output)[:2000],
        "is_error": is_error,
        "session_id": session_id,
        "cwd": cwd,
    }

    try:
        with open(trace_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass

    # ── Real-time pattern detection ──────────────────────────────────────
    # When a tool call succeeds, check if the previous call of the same tool
    # in this session failed with a similar command. If so, trigger distillation.
    if not is_error and tool_name == "Bash":
        _check_retry_success(trace_file, session_id, cwd, tool_name, tool_input, tool_output)

    # Exit 0 — never block the agent
    sys.exit(0)


def _check_retry_success(
    trace_file: Path,
    session_id: str,
    cwd: str,
    tool_name: str,
    current_input: dict,
    current_output: str,
) -> None:
    """Check if this successful call is a retry of a previous failed call."""
    # Read recent records
    try:
        lines = trace_file.read_text(encoding="utf-8").strip().split("\n")
    except OSError:
        return

    if len(lines) < 2:
        return

    records = []
    for line in lines[-10:]:  # last 10 calls
        try:
            records.append(json.loads(line))
        except (json.JSONDecodeError, ValueError):
            continue

    if len(records) < 2:
        return

    current_cmd = current_input.get("command", "")
    if not current_cmd:
        return

    # Look backwards for a failed call of the same tool
    for prev in reversed(records[:-1]):  # exclude current
        if prev.get("tool") != tool_name:
            continue
        if not prev.get("is_error"):
            break  # previous call succeeded → no pattern

        prev_cmd = prev.get("input", {}).get("command", "")
        prev_error = prev.get("output", "")

        if not prev_cmd:
            break

        # Check similarity (avoid false positives from unrelated calls)
        from difflib import SequenceMatcher
        sim = SequenceMatcher(None, prev_cmd, current_cmd).ratio()
        if sim < 0.15:
            break  # too different

        # Skip permission-only errors (low learning value)
        low_err = prev_error.lower()
        if any(sig in low_err for sig in ("requested permissions", "haven't granted", "was blocked", "requires approval")):
            break

        # ── Pattern detected! Trigger distillation ───────────────────────
        # Run in background to avoid blocking
        distill_script = PLUGIN_DIR / "scripts" / "distill.py"
        if not distill_script.exists():
            break

        import subprocess

        # Compute delta for the heuristic extractor
        try:
            added = set(current_cmd.split()) - set(prev_cmd.split())
            added_str = " ".join(sorted(added)) if added else ""
        except Exception:
            added_str = ""

        # Call the distill engine in online mode (non-blocking, best-effort)
        try:
            subprocess.Popen(
                [
                    sys.executable, str(distill_script), "online",
                    "--tool", tool_name,
                    "--failed-cmd", prev_cmd[:500],
                    "--error", prev_error[:500],
                    "--succeeded-cmd", current_cmd[:500],
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                env={**os.environ, "DISTILL_CWD": cwd},
            )
        except (OSError, subprocess.SubprocessError):
            pass
        break


if __name__ == "__main__":
    main()
