---
description: Run or manage agent experience distillation — extract reusable rules from trial-and-error patterns in your Claude Code sessions
argument-hint: "[offline | status | report | apply | install-cron] (default: status)"
allowed-tools: Bash, Read
---

# /distill — Agent Experience Distillation

You are driving the **Agent Experience Distillation** system. It scans Claude Code
session transcripts, detects trial-and-error patterns (fail → retry → success),
extracts reusable rules, and consolidates them into CLAUDE.md and a structured
rules database.

## Requested action: $ARGUMENTS

(If `$ARGUMENTS` is empty, treat it as `status`.)

## How to run it

The engine is at `${CLAUDE_PLUGIN_ROOT}/scripts/distill.py`. Run actions via:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/distill.py" <command> [options]
```

| command     | what it does |
|-------------|--------------|
| `status`    | Show rule count, data location, recent rules |
| `offline`   | Scan recent transcripts → detect patterns → extract rules. Flags: `--project PATH`, `--lookback HOURS` (default 72), `--llm` (use LLM extraction), `--dry-run` |
| `report`    | Show all distilled rules with sources |
| `apply`     | Write rules into CLAUDE.md (backs up first). Flags: `--project PATH` |
| `online`    | Extract from a single fail→success pair (used by hook, not manual) |

## Steps to follow

1. **Run the requested command** via the engine script. Capture stdout.
2. **For `offline`**: after it completes, show the user:
   - How many transcripts were scanned
   - How many trial-and-error patterns were detected
   - What rules were extracted (show each rule)
   - Whether dry-run or saved
3. **If rules were saved**: offer to run `/distill apply` to write them into CLAUDE.md
4. **For `apply`**: confirm which CLAUDE.md was updated and that a backup was created
5. **For `report`**: show all rules grouped by tool type

## Scheduling offline distillation

To run nightly (e.g., at 3:17 AM):

```bash
# Add to crontab:
17 3 * * * cd /your/project && python3 "${CLAUDE_PLUGIN_ROOT}/scripts/distill.py" offline --project /your/project --llm >> /tmp/distill.log 2>&1
```

## Safety

- Transcript scanning is **read-only**.
- Rules are saved to the plugin's `data/rules.json` — never to CLAUDE.md without `apply`.
- `apply` always creates a `.bak` backup of CLAUDE.md first.
- The PostToolUse hook records lightweight traces to `data/traces/` and only triggers extraction on detected fail→success patterns.
