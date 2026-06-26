---
description: Run or manage the offline sleep cycle (review past sessions, replay tasks, consolidate validated memory + skills)
argument-hint: "[run | dry-run | status | adopt | harvest | schedule]"
allowed-tools: Bash, Read
---

# /sleep — Evolving-Skills offline self-evolution

You are driving the **offline sleep cycle**: review past Claude Code sessions,
replay recurring tasks, and consolidate what was learned into **validated**
memory (`CLAUDE.md`) and skills (`SKILL.md`). Changes are gated: a change is
kept only if it improves a held-out replay score. Nothing live is modified until
the user adopts it.

## Requested action: $ARGUMENTS

(If empty, treat as `status`.)

## How to run it

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/run-sleep.sh" <action> --project "$(pwd)" --scope invoked
```

| action | what it does |
|--------|-------------|
| `status` | show nights run + latest staged proposal (READ-ONLY) |
| `dry-run` | harvest → mine → replay → report, **stage nothing** |
| `run` | full cycle: **stage** a proposal (still no live edits) |
| `adopt` | apply staged proposal to live CLAUDE.md / SKILL.md (backs up first) |
| `harvest` | debug: print mined tasks |

Default backend is `mock` (no API spend). Add `--backend claude` for real budget.

## Steps

1. **Run the requested action** via the runner. Capture stdout.
2. **For `run` / `dry-run`:** Read the `report.md` in the staging dir and show:
   - held-out score: baseline → candidate
   - gate decision (accept/reject) and exact edits
   - where the proposal is staged
3. **For accepted proposal:** tell the user nothing live changed yet. Offer `/sleep adopt`.
4. **For `adopt`:** confirm which files were updated and backups written.
5. **Never** edit CLAUDE.md or SKILL.md yourself — only the `adopt` action does that.

## Safety

- Harvest is **read-only** over `~/.claude`. Mock replay has no side effects.
- The cycle stages proposals; the user controls adoption.
