# Evolving Skills

> **Dual-layer skill self-evolution for Claude Code** — online distillation (real-time) × offline sleep cycle (validated) × memory consolidation.

Fuses three open-source projects into one plugin:
- [**self-improving-skills**](https://github.com/UniM0cha/claude-self-improving-skills) — Stop hook → skill-distiller闭环 (Hermes Agent port)
- [**SkillOpt-Sleep**](https://github.com/microsoft/SkillOpt) — offline harvest→mine→replay→**gate**→adopt
- [**evolving-skills**](https://github.com/PalmDr/claude-evolving-skills) — evolution tree, multi-model debate concepts

## What it does

### Online (real-time)
```
complex work ends → Stop hook detects ≥12 tool calls + ≥2 file edits
  → blocks once → delegates to skill-distiller subagent
  → patches or creates SKILL.md → validates + stamps provenance
```

### Offline (nightly)
```
harvest ~/.claude transcripts → mine recurring tasks → replay offline
  → reflect on failures → propose bounded edits → GATE on held-out tasks
  → stage proposal → (you) adopt with backup
```

### Memory
- CLAUDE.md protected block: `<!-- EVOLVING-SKILLS:LEARNED START/END -->`
- SKILL.md provenance: `metadata.provenance: evolving-skills`
- Evolution tree: `~/.evolving-skills/evolution-tree.jsonl`
- Curator: stale(30d) → archived(90d), pinned never touched

## Install

```bash
# 1. clone or copy to your machine
cd ~/.claude/plugins  # or wherever you keep plugins
# (copy this directory there)

# 2. inside Claude Code:
/plugin marketplace add ~/.claude/plugins/evolving-skills
/plugin install evolving-skills@evolving-skills

# 3. verify
/curator-status
```

## Commands

| Command | Layer | Description |
|---------|-------|-------------|
| `/distill-skill` | Online | Manually trigger skill distillation |
| `/sleep dry-run` | Offline | Preview what would be learned |
| `/sleep run` | Offline | Full cycle, stage proposal |
| `/sleep adopt` | Offline | Apply staged proposal (backup first) |
| `/sleep status` | Offline | Show sleep history |
| `/curator-status` | Governance | Skill library health |
| `/curate-skills` | Governance | Consolidate/archive stale skills |
| `/prune-skills [days]` | Governance | Bulk archive idle skills |
| `/pin-skill <name>` | Governance | Protect from archival |
| `/restore-skill <name>` | Governance | Restore archived skill |

## Configuration

All optional. Set in shell or `~/.claude/settings.json` under `env`:

| Variable | Default | Meaning |
|----------|---------|---------|
| `SIS_DISTILL_THRESHOLD` | `12` | Tool calls before online nudge fires |
| `SIS_MIN_FILE_EDITS` | `2` | Min file edits (prevents pure Q&A from triggering) |
| `SIS_STALE_AFTER_DAYS` | `30` | Days idle → marked stale |
| `SIS_ARCHIVE_AFTER_DAYS` | `90` | Days idle → archived (doubled if use_count ≥ 3) |
| `SIS_CURATE_INTERVAL_DAYS` | `7` | Auto-curator interval |

## How it works

### Hooks (Claude Code lifecycle events)

| Hook | Trigger | What happens |
|------|---------|-------------|
| **Stop** | Session stops | `analyze_turn.py` checks if work was complex + undistilled → blocks once |
| **SessionStart** | Session begins | Injects skill count + last sleep status |
| **PreToolUse** | Write/Edit to SKILL.md | Backs up the file first |
| **PostToolUse** | Write/Edit to SKILL.md | Validates frontmatter + stamps provenance + records telemetry |
| **SessionEnd** | Session ends | Appends activity marker (for offline harvest) |

### Offline sleep cycle (6 stages)

1. **Harvest** — read-only scan of `~/.claude/projects/*/*.jsonl`
2. **Mine** — extract recurring tasks + outcome labels
3. **Replay** — re-run tasks with current skill+memory
4. **Consolidate** — reflect on failures → propose edits → **held-out GATE**
5. **Stage** — write proposal to `.evolving-skills/staging/`
6. **Adopt** — user confirms → backup → apply

### Validation gate

Each proposed edit is accepted **only if** it improves the held-out replay score:
```
candidate_score > baseline_score → accept
candidate_score ≤ baseline_score → reject (kept as negative feedback)
```

## License

MIT
