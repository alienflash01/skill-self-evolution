#!/bin/bash
# Stop hook — nudge the agent to distill reusable skills after complex work.
# Delegates to analyze_turn.py. Fails safe to {"decision":"approve"} on ANY error.
set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
out=$(python3 "${PLUGIN_ROOT}/scripts/analyze_turn.py" 2>/dev/null) || {
  echo '{"decision":"approve"}'
  exit 0
}
if [ -z "$out" ]; then
  echo '{"decision":"approve"}'
  exit 0
fi
printf '%s\n' "$out"
exit 0
