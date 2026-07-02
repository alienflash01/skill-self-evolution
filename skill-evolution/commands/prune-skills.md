---
description: Bulk-archive unpinned agent-distilled skills idle for N days (default from config)
argument-hint: "[days] [--apply]"
allowed-tools: Bash
---

# /prune-skills

Preview and optionally archive stale skills.

First, preview (dry-run):
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curator_transitions.py" --dry-run
```

Show the user which skills would be archived. If the user confirms, run:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curator_transitions.py"
```

$ARGUMENTS may contain a day threshold (e.g. `60`).
