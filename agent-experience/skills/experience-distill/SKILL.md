---
name: experience-distill
description: "Use when the user wants their Claude agent to learn from trial-and-error patterns, asks about experience distillation, or says things like 'learn from mistakes', 'remember this error', 'why do I keep hitting this issue', 'distill experience', or wants to extract reusable rules from past sessions. Scans transcripts for fail→retry→success patterns and consolidates them into CLAUDE.md."
---

# Agent Experience Distillation: learn from trial-and-error

This skill extracts reusable rules from the agent's own trial-and-error patterns.
When the agent tries something, fails, retries with a modification, and succeeds,
that sequence contains valuable experience worth distilling.

## When to use

- "Learn from my past sessions" / "extract experience" / "distill rules"
- "Why does this keep failing?" → check distilled rules first
- After a complex task with multiple retries → run distillation
- Periodically (nightly) to keep rules fresh
- "Apply learned rules" / "update CLAUDE.md"

## Two modes

### Online (automatic, via PostToolUse hook)

The hook fires after every tool call. When it detects a fail→success sequence
(same tool type, similar commands, previous call errored), it automatically:
1. Computes the diff between failed and succeeded commands
2. Extracts a rule (heuristic or LLM)
3. Saves to `data/rules.json`

No user action needed — it just works in the background.

### Offline (manual or cron, deeper analysis)

```bash
# Scan recent transcripts and extract rules
python3 scripts/distill.py offline --project "$(pwd)" --llm

# Dry run (see what it would find without saving)
python3 scripts/distill.py offline --dry-run

# Show all extracted rules
python3 scripts/distill.py report

# Apply rules to CLAUDE.md
python3 scripts/distill.py apply --project "$(pwd)"
```

## What it detects

Three patterns:

1. **fail_to_success** — single failed call → retry with modification → success
   ```
   npm install pkg     → ERESOLVE error
   npm install pkg --legacy-peer-deps → success ✓
   → Rule: "When npm install fails with ERESOLVE, add --legacy-peer-deps"
   ```

2. **multi_attempt** — multiple failed approaches → eventual success
   ```
   approach_1 (fail) → approach_2 (fail) → approach_3 (success)
   → Rule: "Use approach_3 for this type of task"
   ```

3. **user_correction** — user corrects the agent
   ```
   Agent: uses requests
   User: "不对，应该用 httpx"
   → Rule: "This project uses httpx, not requests"
   ```

## Safety guarantees

- Transcripts are read-only — never modified
- Rules go to `data/rules.json` first, not CLAUDE.md
- `apply` always backs up CLAUDE.md before writing
- Permission-denial errors are filtered out (low learning value)
- Deduplication prevents the same rule from being saved twice
