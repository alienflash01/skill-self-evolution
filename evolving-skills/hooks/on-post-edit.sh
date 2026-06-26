#!/bin/bash
# PostToolUse hook (Write|Edit|MultiEdit) — validate & provenance-stamp SKILL.md.
# Fails safe to silent.
set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
python3 "${PLUGIN_ROOT}/scripts/validate_skill.py" 2>/dev/null || true
exit 0
