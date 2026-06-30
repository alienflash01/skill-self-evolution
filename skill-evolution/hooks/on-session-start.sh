#!/bin/bash
# SessionStart hook — inject self-improvement advisory + curator status.
# Fails safe to silent on any error.
set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
python3 "${PLUGIN_ROOT}/scripts/session_init.py" 2>/dev/null || true
exit 0
