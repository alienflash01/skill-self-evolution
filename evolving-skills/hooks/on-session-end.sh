#!/bin/bash
# SessionEnd hook (async) — record session activity for offline harvest.
# Zero-cost, non-blocking. Just appends a timestamp marker.
set -uo pipefail

STATE_DIR="${HOME}/.evolving-skills"
mkdir -p "$STATE_DIR" 2>/dev/null || exit 0
printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${PWD}" \
  >> "$STATE_DIR/session-end.log" 2>/dev/null || true
exit 0
