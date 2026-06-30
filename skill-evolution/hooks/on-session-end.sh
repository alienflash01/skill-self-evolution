#!/usr/bin/env bash
# SessionEnd hook — marks that a session just ended so the offline distiller
# knows there's fresh data to process. Async, non-blocking, zero API cost.
set -uo pipefail

STATE_DIR="${HOME}/.claude-experience"
mkdir -p "$STATE_DIR" 2>/dev/null || exit 0

# Record session end
printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${PWD}" \
  >> "$STATE_DIR/session-end.log" 2>/dev/null || true

exit 0
