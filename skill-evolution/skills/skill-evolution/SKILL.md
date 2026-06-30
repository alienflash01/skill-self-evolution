---
name: skill-evolution
description: "Use when the user wants their Claude agent to self-improve, learn from mistakes, distill experience, run offline sleep cycles, consolidate memory/skills, or manage skill lifecycle. Three layers: (1) tool-level experience distillation from fail→retry→success patterns, (2) task-level skill distillation from complex sessions, (3) offline sleep cycle with validation gate."
---

# Skill-Evolution: unified self-improvement for Claude Code

Three complementary learning layers, one plugin:

## Layer 1: Tool-level Experience Distillation (real-time)

**Trigger**: PostToolUse hook fires after every Bash/Write/Edit call.
**What it does**: Detects fail→retry→success patterns. Extracts reusable rules.
**Output**: `data/rules.json` + CLAUDE.md pitfall section.

Commands:
- `/distill offline` — batch scan transcripts for patterns
- `/distill report` — show all rules with verification status
- `/distill apply` — write rules to CLAUDE.md (with backup)
- `/distill status` — current state

Rule lifecycle: `pending` (1st obs) → `verified` ★ (2nd obs) → `trusted` ✓ (3+ obs)

## Layer 2: Task-level Skill Distillation (session-end)

**Trigger**: Stop hook fires when session stops after ≥12 tool calls + ≥2 file edits.
**What it does**: Delegates to `skill-distiller` subagent to capture reusable techniques.
**Output**: `~/.claude/skills/<name>/SKILL.md` with provenance.

Commands:
- `/distill-skill` — manually trigger task-level distillation

## Layer 3: Offline Sleep Cycle (nightly)

**Trigger**: Manual `/sleep run` or cron schedule.
**What it does**: harvest → mine → replay → reflect → **GATE** → stage → adopt.
**Output**: Validated CLAUDE.md + SKILL.md updates (held-out gate).

Commands:
- `/sleep dry-run` — preview
- `/sleep run` — full cycle, stage proposal
- `/sleep adopt` — apply (with backup)
- `/sleep status` — history

## Governance

- `/curator-status` — skill library health
- `/curate-skills` — consolidate/archive stale skills
- `/pin-skill <name>` — protect from archival

## Memory model

- **CLAUDE.md**: protected blocks `<!-- BEGIN AGENT-EXPERIENCE -->` + `<!-- EVOLVING-SKILLS:LEARNED -->`
- **rules.json**: structured rules with status/confidence/times_observed
- **SKILL.md**: `metadata.provenance: skill-evolution`, `origin: tool-distill|task-distill|offline-sleep`

Hand-written content outside protected regions is **never** touched.
