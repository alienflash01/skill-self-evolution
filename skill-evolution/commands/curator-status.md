---
description: Show evolving-skills library status — skill counts, stale, archived, last sleep cycle
allowed-tools: Bash, Read
---

# /curator-status

Run the status check:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/usage_store.py"
```

Also run:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curator_transitions.py" --dry-run 2>/dev/null || true
```

Show the user:
- Total learned skills, broken down by state (active/stale/archived)
- Skills that would be pruned in the next curator run
- Last sleep cycle night number and date
- Any pinned skills

Format as a compact table or bullet list.
