#!/bin/bash
# PreToolUse hook (Write|Edit|MultiEdit) — back up SKILL.md before edit.
# Fails safe to silent; never blocks.
set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
python3 "${PLUGIN_ROOT}/scripts/backup_skill.py" 2>/dev/null || true
exit 0
