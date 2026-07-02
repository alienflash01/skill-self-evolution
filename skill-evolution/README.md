# Skill-Evolution

> **Three-layer self-improvement for Claude Code** — learn from mistakes in real time, evolve skills overnight, validate every change with a strict gate.

```
白天（实时，零 API 成本）              夜间（批量，利用闲置算力）
┌──────────────────────────┐     ┌──────────────────────────────────┐
│  L1: PostToolUse Hook     │     │  L3: Sleep Cycle (cron/手动)      │
│  检测 fail→retry→success  │     │  harvest → mine → replay → gate   │
│  启发式提取规则（不调 API）│     │  用真实 CC 调用验证规则改进        │
│  ↓ rules.json             │     │  ↓ staging（人工 adopt）           │
│  pending → verified → trusted │ │  strict-improvement gate           │
└──────────────────────────┘     └──────────────────────────────────┘
```

## Why?

Every Claude Code session produces trial-and-error patterns — failed commands, corrected approaches, user feedback. These lessons are lost when the session ends.

**Skill-Evolution captures them, validates them, and feeds them back.**

Unlike CC's built-in `auto-memory` (which stores whatever CC thinks is useful, with no quality gate), Skill-Evolution uses a **SkillOpt-style strict-improvement gate**: a candidate rule is accepted only if it measurably improves the held-out validation score. Ties are rejected.

## Install

```bash
# Clone
git clone https://github.com/alienflash01/skill-self-evolution.git
cd skill-self-evolution/skill-evolution

# Symlink into Claude Code plugins
ln -s "$(pwd)" ~/.claude/plugins/skill-evolution

# Verify
cc-pipeline --version  # or just check hooks load on next CC session
```

**Prerequisites:** Python ≥ 3.10 | Claude Code CLI (`claude -p`)

## Three Layers

| Layer | Trigger | What It Does | API Cost |
|-------|---------|-------------|----------|
| **L1: Tool-level** | PostToolUse hook (real-time) | Detects fail→success patterns, extracts rules via heuristics | Zero |
| **L2: Task-level** | Stop hook (session end) | Distills complex sessions into reusable skills | Optional |
| **L3: Offline sleep** | Cron / `/sleep run` | Replays tasks under candidate skills, validates via gate | Batch CC calls |

### L1: Real-time Distillation

Every Bash/Write/Edit call is traced. When a retry succeeds after a failure:

```
Bash: gcc test.c              → FAIL (undefined reference to sin)
Bash: gcc test.c -lm          → SUCCESS
                                    ↓
Rule extracted: "When gcc fails with 'undefined reference', add -lm"
Status: pending (1st observation)
```

Rule lifecycle: `pending` (·) → `verified` ★ (2nd observation) → `trusted` ✓ (3+ observations)

### L3: Offline Sleep Cycle

Six-stage pipeline inspired by [SkillOpt](https://aka.ms/SkillOpt):

```
harvest → mine → replay → reflect → GATE → stage → (adopt)
```

1. **Harvest** — Scan CC transcripts, extract session digests
2. **Mine** — Turn sessions into TaskRecords with train/val split (34% holdout)
3. **Replay** — Re-run tasks with current skill via `claude -p`
4. **Reflect** — Analyze failures, propose bounded skill edits
5. **Gate** — Candidate must **strictly beat** baseline on held-out val set (ties rejected)
6. **Stage** — Write proposal to staging directory for manual review

## Commands

```bash
# L1: Tool-level distillation
/distill offline              # Scan transcripts, extract trial-and-error rules
/distill report               # Show all rules with verification status
/distill apply                # Write verified rules to CLAUDE.md (with backup)
/distill status               # Current state

# L3: Offline sleep cycle
/sleep dry-run                # Preview what would be harvested/mined
/sleep run                    # Full cycle (mock backend, no API cost)
/sleep run --backend cc       # Full cycle with real Claude Code replay
/sleep adopt                  # Apply staged proposal (with backup)
/sleep status                 # History of sleep cycles
```

### Nightly Cron

```bash
# Every night at 3:17 AM
17 3 * * * bash /path/to/skill-evolution/scripts/nightly.sh /your/project >> /tmp/skill-evo.log 2>&1
```

## The Validation Gate

The gate is what makes Skill-Evolution different from "just write rules to a file":

```python
# gate.py — the core decision
def evaluate_gate(candidate, current, best):
    if candidate_score > current_score:   # strictly better?
        if candidate_score > best_score:
            return "accept_new_best"      # new champion
        return "accept"                   # improvement
    return "reject"                       # tie or worse → REJECT
```

**Ties are rejected by design.** This prevents skill bloat — rules that don't measurably help are never adopted.

## Backends

| Backend | Class | API Cost | Use When |
|---------|-------|----------|----------|
| `mock` | `MockBackend` | Zero | Development, testing, dry-run |
| `cc` | `CCBackend` | Real CC calls | Production nightly runs |

CCBackend calls `claude -p` to re-attempt mined tasks with the candidate skill, then judges the response (exact match or outcome-derived scoring).

## Architecture

```
skill-evolution/
├── hooks/
│   ├── post-tool-use.py        # L1: real-time pattern detection
│   ├── on-stop.sh              # L2: session-end trigger
│   ├── on-session-start.sh     # Inject advisory on startup
│   └── hooks.json              # Hook configuration
├── scripts/
│   ├── distill.py              # L1 engine (1125 lines)
│   ├── nightly.sh              # Cron entry point
│   ├── run-sleep.sh            # Sleep runner
│   └── sleep/
│       ├── cycle.py            # L3: six-stage orchestrator
│       ├── harvest.py          # Stage 1: transcript → SessionDigest
│       ├── mine.py             # Stage 2: SessionDigest → TaskRecord
│       ├── replay.py           # Stage 3: Backend + MockBackend
│       ├── cc_backend.py       # Stage 3: CCBackend (real Claude)
│       ├── consolidate.py      # Stage 4: reflect → gate
│       ├── gate.py             # Strict-improvement gate
│       ├── staging.py          # Stage 5: write proposal
│       ├── memory.py           # Apply edits to skill/memory
│       ├── state.py            # Persistent sleep state
│       └── models.py           # Data types (SessionDigest, TaskRecord, etc.)
├── agents/
│   └── skill-distiller.md      # L2: subagent definition
├── commands/                    # Slash commands (/distill, /sleep)
├── data/
│   ├── rules.json              # L1 extracted rules
│   └── staging/                # L3 staged proposals
└── tests/                       # 85 tests, all green
```

## Testing

```bash
# Run all tests (85 tests, <1s)
pytest tests/ -v

# With coverage
pytest tests/ --cov=sleep --cov=distill --cov-report=term-missing
```

## Safety

- **Transcripts are read-only** — never modified
- **CLAUDE.md protected blocks** — `<!-- BEGIN AGENT-EXPERIENCE -->` sections only
- **Every `apply` creates a backup** — `.bak` files before any write
- **Staging + adopt workflow** — sleep proposals are staged, never auto-applied
- **Gate validation** — no rule is accepted without measurable improvement

## Differences from CC auto-memory

| | CC auto-memory | Skill-Evolution |
|---|---|---|
| What it stores | Whatever CC decides | Fail→success patterns + validated rules |
| Quality control | None | Strict-improvement gate |
| Version management | Overwrite | Staging + backup + adopt |
| Real-time | Passive (CC writes when it feels like) | Active (PostToolUse hook detects patterns) |
| Offline | None | Nightly sleep cycle with replay |
| Scoring | None | Held-out validation set (34% holdout) |

## License

MIT
