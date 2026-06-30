---
description: Run offline sleep cycle — review past sessions, replay tasks, consolidate validated skills
argument-hint: "[run | dry-run | status | adopt]"
allowed-tools: Bash, Read
---

# /sleep — Offline Sleep Cycle (Layer 3)

Reviews past Claude Code sessions, replays recurring tasks, consolidates into
**validated** memory and skills. Only changes passing held-out gate are kept.

## Requested action: $ARGUMENTS

(If empty, treat as `status`.)

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/run-sleep.sh" <action> --project "$(pwd)" --scope invoked
```

| action | what it does |
|--------|-------------|
| `status` | Show nights run + latest staged proposal |
| `dry-run` | Safe preview, stages nothing |
| `run` | Full cycle, stage proposal (no live edits) |
| `adopt` | Apply staged proposal (backup first) |
