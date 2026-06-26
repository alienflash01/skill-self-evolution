---
description: Restore an archived skill back to active
argument-hint: "<skill-name>"
allowed-tools: Bash
---

# /restore-skill

Restore archived skill: $ARGUMENTS

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curator_transitions.py" restore "$ARGUMENTS"
```

Confirm the skill is back in ~/.claude/skills/ and its state is active.
