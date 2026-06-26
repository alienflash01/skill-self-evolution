---
name: evolving-skills
description: "Use when the user wants their Claude agent to self-improve, asks about skill distillation, offline 'sleep' or 'dream' cycles, memory/skill consolidation, or says things like 'make my agent better', 'review past sessions', 'learn my preferences', 'consolidate what you learned'. Drives dual-layer evolution: online distillation (Stop hook → skill-distiller) + offline sleep cycle (harvest → mine → replay → gate → adopt)."
---

# Evolving Skills: dual-layer self-evolution for Claude Code

This plugin gives your Claude agent two complementary learning loops:

## Online distillation (real-time)

When you finish a complex work segment (≥12 tool calls + ≥2 file edits), the
Stop hook nudges Claude to capture reusable techniques into `~/.claude/skills/`.

Commands:
- `/distill-skill` — manually trigger distillation from the current session

## Offline sleep cycle (deep review)

Reviews your past Claude Code sessions, replays recurring tasks, and consolidates
what it learns into **validated** memory and skills. Only changes that pass a
held-out validation gate are kept.

Commands:
- `/sleep dry-run` — safe preview, stages nothing
- `/sleep run` — full cycle, stages a proposal (no live edits)
- `/sleep adopt` — apply staged proposal (with backup)
- `/sleep status` — see history

## Governance

- `/curator-status` — skill library health
- `/curate-skills` — consolidate/archive stale skills
- `/prune-skills` — bulk archive idle skills
- `/pin-skill <name>` — protect from archival
- `/restore-skill <name>` — restore archived skill

## Memory model

Both loops write to protected regions:
- **CLAUDE.md** — `<!-- EVOLVING-SKILLS:LEARNED START -->` ... `END -->` block
- **SKILL.md** — `metadata.provenance: evolving-skills`, `origin: online-distill|offline-sleep`

Hand-written content outside protected regions is **never** touched.

## Configuration

Environment variables (all optional, in shell or `~/.claude/settings.json` under `env`):

| Variable | Default | Meaning |
|----------|---------|---------|
| `SIS_DISTILL_THRESHOLD` | 12 | Tool calls before online nudge |
| `SIS_MIN_FILE_EDITS` | 2 | Min file edits before nudge |
| `SIS_STALE_AFTER_DAYS` | 30 | Days idle → stale |
| `SIS_ARCHIVE_AFTER_DAYS` | 90 | Days idle → archived (×2 if use_count≥3) |
