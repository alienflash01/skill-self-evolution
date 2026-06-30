---
description: Run experience distillation — extract reusable rules from trial-and-error patterns
argument-hint: "[offline | status | report | apply] (default: status)"
allowed-tools: Bash, Read
---

# /distill — Tool-level Experience Distillation (Layer 1)

Extracts reusable rules from fail→retry→success patterns in tool calls.

## Requested action: $ARGUMENTS

(If empty, treat as `status`.)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/distill.py" <command> [options]
```

| command | what it does |
|---------|-------------|
| `status` | Show rule count, verification states |
| `offline` | Scan transcripts → detect patterns → extract+verify rules. `--llm` for LLM extraction |
| `report` | Show all rules with sources and status icons (★=verified ✓=trusted ·=pending) |
| `apply` | Write rules into CLAUDE.md (backs up first) |
