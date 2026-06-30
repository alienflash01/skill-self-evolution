#!/usr/bin/env bash
# Skill-Evolution nightly script — runs both layers while you sleep.
#
# Usage in crontab:
#   17 3 * * * bash /path/to/skill-evolution/scripts/nightly.sh /your/project >> /tmp/skill-evo.log 2>&1
#
# What it does:
#   1. Tool-level distill: scan transcripts, extract trial-and-error rules, verify existing rules
#   2. Offline sleep: harvest → mine → replay → gate → stage proposal
#   3. Auto-apply tool-level rules to CLAUDE.md (backup first)
#   4. Sleep proposals stay staged — user adopts manually via /sleep adopt

set -euo pipefail

PROJECT="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "════════════════════════════════════════════════════════"
echo "  Skill-Evolution Nightly Run"
echo "  Project: $PROJECT"
echo "  Time:    $(date)"
echo "════════════════════════════════════════════════════════"

# ── Layer 1: Tool-level experience distillation ────────────────────────────
echo ""
echo "── Layer 1: Tool-level distill ──────────────────────────"
python3 "$SCRIPT_DIR/distill.py" offline --project "$PROJECT" --llm 2>&1 || true

# Auto-apply distilled rules to CLAUDE.md
echo ""
echo "── Applying rules to CLAUDE.md ──────────────────────────"
python3 "$SCRIPT_DIR/distill.py" apply --project "$PROJECT" 2>&1 || true

# ── Layer 3: Offline sleep cycle ───────────────────────────────────────────
echo ""
echo "── Layer 3: Offline sleep cycle ─────────────────────────"
bash "$SCRIPT_DIR/run-sleep.sh" run --project "$PROJECT" --scope invoked 2>&1 || true

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Done. Review sleep proposals with: /sleep adopt"
echo "════════════════════════════════════════════════════════"
