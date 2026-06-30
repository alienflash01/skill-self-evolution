#!/usr/bin/env bash
# evolving-skills sleep runner — locates Python ≥3.10 and runs the sleep engine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${SCRIPT_DIR}")" && pwd)}"
SCRIPTS_DIR="${PLUGIN_ROOT}/scripts"

# Pick a Python ≥3.10
PY=""
for cand in python3.12 python3.11 python3.10 python3; do
  if command -v "$cand" >/dev/null 2>&1; then
    ver="$("$cand" -c 'import sys; print("%d%d" % sys.version_info[:2])' 2>/dev/null || echo 0)"
    if [ "${ver:-0}" -ge 310 ]; then PY="$cand"; break; fi
  fi
done
if [ -z "$PY" ]; then
  echo "[evolving-skills] ERROR: need Python >= 3.10" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then set -- status; fi

# Run from scripts/ dir (parent of sleep/) so `from sleep.models import ...` works
cd "$SCRIPTS_DIR"
PYTHONPATH="${SCRIPTS_DIR}:${PYTHONPATH:-}" exec "$PY" -c "
import sys
sys.path.insert(0, '${SCRIPTS_DIR}')
from sleep.cycle import run_sleep_cycle_cli
run_sleep_cycle_cli()
" "$@"
