#!/usr/bin/env bash
# evolving-skills install script
# Installs as a Claude Code local marketplace plugin.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="${HOME}/.claude"
PLUGINS_DIR="${CLAUDE_HOME}/plugins"

echo "╔══════════════════════════════════════════════╗"
echo "║   evolving-skills — installer                 ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# 1. Ensure dirs
mkdir -p "${CLAUDE_HOME}/skills" "${CLAUDE_HOME}/self-improve"

# 2. Make scripts executable
chmod +x "${SCRIPT_DIR}"/hooks/*.sh 2>/dev/null || true
chmod +x "${SCRIPT_DIR}"/scripts/run-sleep.sh 2>/dev/null || true
chmod +x "${SCRIPT_DIR}"/scripts/*.py 2>/dev/null || true

# 3. Initialize state
mkdir -p "${HOME}/.evolving-skills"

# 4. Initialize evolution tree if needed
touch "${HOME}/.evolving-skills/evolution-tree.jsonl"

echo "✅ Plugin files ready at: ${SCRIPT_DIR}"
echo ""
echo "To install in Claude Code, run these commands inside Claude Code:"
echo ""
echo "  /plugin marketplace add ${SCRIPT_DIR}"
echo "  /plugin install evolving-skills@evolving-skills"
echo ""
echo "Then restart Claude Code or run /reload-skills."
echo ""
echo "Verify with:"
echo "  /curator-status"
echo ""
echo "Optional: schedule nightly offline cycle (copy into crontab -e):"
echo "  17 3 * * *  \"${SCRIPT_DIR}/scripts/run-sleep.sh\" run --project \"\$HOME\" --scope invoked --backend mock >> \"${HOME}/.evolving-skills/cron.log\" 2>&1"
