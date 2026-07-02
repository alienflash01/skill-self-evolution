<!-- BEGIN AGENT-EXPERIENCE -->
## ⚠️ Known Pitfalls (Auto-distilled)

<!-- These rules were extracted from trial-and-error patterns. -->
<!-- Status: ✓=trusted(3+obs) ★=verified(2nd obs) ·=pending(1st obs) -->
<!-- To update, run: /distill offline -->

### Bash

- ★ When using sed's append command with backslash escapes, break the command into separate steps or use the Edit tool instead to avoid whitespace escaping issues.

<!-- END AGENT-EXPERIENCE -->

# Skill-Evolution — Project Documentation

## Overview

Three-layer self-improvement system for Claude Code. Captures trial-and-error patterns from coding sessions, validates them via a strict-improvement gate, and feeds them back as reusable skills.

| Layer | Trigger | Purpose | API Cost |
|-------|---------|---------|----------|
| **L1: Tool-level** | PostToolUse hook (real-time) | Detect fail→retry→success, extract rules | Zero |
| **L2: Task-level** | Stop hook (session end) | Distill complex sessions into skills | Optional |
| **L3: Offline sleep** | Cron `/sleep run` | Replay tasks, validate via gate | Batch CC calls |

## Development

### Setup

```bash
cd skill-evolution
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

### Testing

```bash
# All tests (85 tests, <1s)
.venv/bin/pytest tests/ -v

# With coverage
.venv/bin/pytest tests/ --cov=sleep --cov=distill --cov-report=term-missing
```

Test files:
- `tests/test_gate.py` — Validation gate (16 tests, 100% coverage)
- `tests/test_distill.py` — L1 distillation engine (30 tests)
- `tests/test_sleep.py` — L3 sleep cycle: harvest/mine/consolidate (21 tests)
- `tests/test_cc_backend.py` — CCBackend real Claude replay (18 tests)

### Architecture

```
hooks/post-tool-use.py     → L1 real-time pattern detection
scripts/distill.py         → L1 extraction engine (1125 lines)
scripts/sleep/cycle.py     → L3 six-stage orchestrator
scripts/sleep/gate.py      → strict-improvement gate
scripts/sleep/cc_backend.py → real Claude Code replay backend
```

### Key Commands

```bash
/distill offline          # Scan transcripts for trial-and-error rules
/distill apply            # Write verified rules to CLAUDE.md
/sleep run --backend cc   # Full sleep cycle with real CC replay
/sleep adopt              # Apply staged proposal
```

### The Validation Gate

Candidate skill must **strictly beat** baseline on held-out val set. Ties are rejected.

```python
if candidate_score > current_score:   # strictly better?
    return "accept"
return "reject"                       # tie or worse → REJECT
```

### Backends

| Backend | API Cost | Use When |
|---------|----------|----------|
| `mock` | Zero | Testing, dry-run |
| `cc` | Real CC calls | Production nightly runs |

### Safety

- Transcripts are **read-only**
- CLAUDE.md edits only within `<!-- BEGIN AGENT-EXPERIENCE -->` blocks
- Every `apply` creates a `.bak` backup
- Sleep proposals are staged, never auto-applied

## Conventions

- **TDD**: all new code requires failing test first (RED→GREEN→REFACTOR)
- **Python ≥3.10**, zero runtime dependencies (stdlib only)
- Hooks must be non-blocking (exit 0, background processes for heavy work)
- Rule lifecycle: `pending` → `verified` (2nd obs) → `trusted` (3+ obs)
