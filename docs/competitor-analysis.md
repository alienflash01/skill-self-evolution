# Competitor Analysis: CoEvoSkills & EvoSkill vs skill-evolution

> Generated: 2026-07-06  
> Repos analyzed:  
> - CoEvoSkills: `github.com/Zhang-Henry/CoEvoSkills` (paper page, no code released)  
> - EvoSkill: `github.com/sentient-agi/EvoSkill` (full implementation, ~12,107 LoC src + ~8,658 LoC tests)  
> - Our project: `/mnt/e/02.workspace/skill-self-evolution/skill-evolution/scripts/sleep/` (~3,468 LoC, 99 tests)

---

## 1. CoEvoSkills

### Architecture

**Status: Paper-only.** The GitHub repo (`Zhang-Henry/CoEvoSkills`) contains **zero Python files** —
only a README, an `index.html` landing page, PNG result figures, and a LICENSE. The code badge
reads "coming soon." All analysis below is derived from the paper description on the project page
and arXiv abstract (2604.01687).

CoEvoSkills proposes a **three-component co-evolutionary architecture**:

```
┌─────────────────────────┐
│    Skill Generator       │  ← iteratively produces/refines multi-file skill packages
│  (LLM-driven, iterative) │     using diagnostic feedback from the verifier
└────────┬────────────────┘
         │ generate skill
         ▼
┌─────────────────────────┐
│  Surrogate Verifier      │  ← information-isolated; independently evolves test
│  (co-evolving, no GT)    │     assertions to give dense, actionable failure signals
└────────┬────────────────┘
         │ verify + feedback
         ▼
┌─────────────────────────┐
│    Opaque Oracle         │  ← ground-truth oracle returns ONLY pass/fail (no content)
│  (GT test, sealed)       │     triggers "test escalation" when surrogate disagrees
└─────────────────────────┘
```

### Core Mechanism (Generator-Verifier Co-evolution)

The central innovation is **breaking the information asymmetry** between the skill generator
and the ground-truth (GT) test content:

1. **Generator produces a multi-file skill package** (instructions + scripts + assets, not
   a single function).
2. **Surrogate verifier** — itself an evolving LLM — independently generates *test assertions*
   to check the skill. It does **NOT** see the GT test content; it only receives an **opaque
   pass/fail signal** from the GT oracle.
3. **Test escalation**: when the surrogate verifier's assessment disagrees with the oracle's
   pass/fail, the system escalates (presumably generating more/refined assertions), forcing
   the verifier to improve its own test-writing ability.
4. This creates a **minimax-like co-evolutionary pressure**: the generator must produce skills
   robust enough to pass *both* the surrogate and the oracle, while the surrogate must learn
   to approximate the oracle's criteria without seeing its content.

**Key architectural property: no GT leakage during evolution.** The verifier provides "dense
diagnostic feedback" (which lines/behaviors failed) without revealing the actual test assertions.
This is fundamentally different from:
- EvoSkill (which uses GT answers directly for scoring)
- SkillOpt (which uses held-out GT scores)
- Our skill-evolution (which uses outcome-derived/exact-match scoring)

### Key Files & Lines

| Component | Location | Lines |
|---|---|---|
| Paper page / abstract | `README.md`, `index.html` | 121 + 30K HTML |
| Framework diagram | `assets/framework.png` | — |
| Code | **Not released** ("coming soon") | 0 |

**No code to analyze.** All findings are from paper description only.

### Unique Features

1. **Generator-Verifier co-evolution** — the only system where the *evaluator itself evolves*.
   Neither EvoSkill, SkillOpt, nor our system has a co-evolving verifier.
2. **Opaque oracle with test escalation** — GT tests are sealed; only pass/fail leaks.
3. **Multi-file skill packages** — skills are structured bundles (instructions + scripts +
   references), not single markdown files. This is the first system to claim automated
   multi-file skill package generation.
4. **Information isolation** — strict protocol ensuring the verifier never sees GT content.
5. **SOTA on SkillsBench** — beats 5 baselines on both Claude Code and Codex.
6. **Cross-model transfer** — skills generated with one LLM transfer to 6 others.

### What We Can Learn

- **Co-evolving verifier is a research frontier.** If they release code, the surrogate verifier
  + opaque oracle pattern could replace our static scoring with a self-improving judge.
- **Multi-file skill packages** are their key differentiator. Our skills are single `SKILL.md`
  files. Supporting multi-file packages (instructions + helper scripts + references) would
  significantly increase skill expressiveness.
- **Information isolation protocol** is a rigorous way to prevent reward hacking — worth
  studying even without their code.
- **Test escalation** is an interesting fallback: when the verifier can't decide, escalate to
  the oracle. We could implement something similar: when our judge confidence is low, escalate
  to an LLM judge (which we don't have).

---

## 2. EvoSkill

### Architecture

**Status: Full open-source implementation** by Sentient AGI (Sentient Labs). Built as a
production-grade toolkit with CLI, Python API, Docker/Daytona support, and 6-agent harness
integrations.

EvoSkill's architecture is a **frontier-based evolutionary loop** (GEPA-inspired) that extends
single-prompt optimization to complete agent program evolution:

```
┌──────────────────────────────────────────────────────────┐
│                   SelfImprovingLoop                        │
│                                                            │
│  1. Base Agent runs benchmark questions                    │
│     → produces traces + answers                            │
│     → scored against GT answers                            │
│                                                            │
│  2. Failures collected (score < 0.8)                       │
│     → round-robin sampled across categories                │
│     → feedback_history.md accumulated                      │
│                                                            │
│  3. Proposer analyzes failures                             │
│     → proposes CREATE new skill or EDIT existing skill     │
│     → structured Pydantic output (SkillProposerResponse)   │
│                                                            │
│  4. Generator implements the proposal                      │
│     → writes multi-file skill (.claude/skills/NAME/SKILL.md)│
│     → or rewrites system prompt (prompt.txt)               │
│                                                            │
│  5. Child program evaluated on held-out val set            │
│     → scored; compared to parent                           │
│                                                            │
│  6. Frontier update (top-N git branches)                   │
│     → accepted if improves over worst frontier member       │
│     → discarded branch deleted                             │
│                                                            │
│  Repeat for max_iterations                                 │
└──────────────────────────────────────────────────────────┘
```

**Key design decisions:**
- Each "program" = a **git branch** with `.claude/program.yaml` (config) + `.claude/skills/` (skills)
- Frontier = top-N programs tracked as **git tags** (`frontier/*`)
- Skills are **multi-file directories** (`SKILL.md` + optional scripts/references)
- Scoring is **GT-answer-based** (requires a benchmark with known answers)
- All agent execution delegates to one of 6 harness SDKs (Claude, OpenCode, OpenHands, Codex, Goose, Harbor)

### Core Mechanism (Skill Discovery from Failures)

EvoSkill's skill discovery is a **proposer-driven, failure-analysis pipeline**, not clustering
or rule-based mining:

1. **Failure detection**: after the base agent answers benchmark questions, any answer scoring
   below 0.8 (multi-tolerance fuzzy match) is flagged as a failure.

2. **Multi-failure analysis**: the proposer agent receives **all failures from the current
   iteration batch** (not just one), along with:
   - Full execution traces (truncated adaptively: 60K→20K→5K chars on retry)
   - Feedback history from previous iterations (outcome-tracked)
   - List of existing skills (to avoid duplication)
   - Task constraints

3. **Proposer decision** (structured via Pydantic `SkillProposerResponse`):
   ```python
   class SkillProposerResponse(BaseModel):
       action: Literal["create", "edit"]    # create new or edit existing
       target_skill: str | None              # required if action="edit"
       proposed_skill: str                   # high-level description
       justification: str                    # reasoning
       related_iterations: list[str]         # references to past iterations
   ```
   The proposer **must** use a "Brainstorming skill" to generate 2-3 approaches before settling.
   It checks for anti-patterns (don't create if existing skill covers similar ground).

4. **Generator implementation**: a separate agent reads the proposal and writes the actual
   `SKILL.md` file (with full tool access: Read, Write, Bash, Glob, Grep, Edit, WebFetch, etc.).

5. **Feedback loop**: after evaluation, the outcome (improved/discarded) + score delta is
   written to `feedback_history.md`, which future proposer runs read to avoid repeating
   discarded approaches.

**Algorithm classification**: **LLM-extraction with failure-pattern analysis** — not clustering,
not rules. The proposer is prompted to "identify COMMON patterns across failures" and propose
GENERAL improvements, not single-case fixes.

### Key Files & Lines

| Component | File | Lines | Role |
|---|---|---|---|
| Main loop | `src/loop/runner.py` | 711 | 5-stage evolutionary cycle orchestrator |
| Loop config | `src/loop/config.py` | 69 | Iteration, frontier, sampling, mode config |
| Loop helpers | `src/loop/helpers.py` | 266 | Query builders, feedback I/O, truncation |
| Program manager (git) | `src/registry/manager.py` | 606 | Git branch/tag versioning of programs |
| Program config model | `src/registry/models.py` | 93 | Pydantic model for program.yaml |
| Skill proposer prompt | `src/agent_profiles/skill_proposer/prompt.py` | 134 | System prompt for failure analysis |
| Skill generator | `src/agent_profiles/skill_generator/skill_generator.py` | 54 | Agent options for skill writing |
| Reward/scoring | `src/evaluation/reward.py` | 443 | Fuzzy match: numeric tolerance, text overlap |
| Parallel evaluation | `src/evaluation/evaluate.py` | 85 | Concurrent agent eval with cache |
| Scorer factory | `src/cli/shared.py` | 282 | multi_tolerance/exact/llm/script/harbor scorers |
| Agent wrapper | `src/harness/agent.py` | 248 | SDK-agnostic agent with retry/timeout |
| Run cache | `src/cache/run_cache.py` | 338 | Content-hash-based eval result caching |
| Feedback descent | `src/feedback_descent.py` | 132 | Pairwise comparison optimization (GEPA core) |
| CLI init | `src/cli/commands/init.py` | 675 | Project setup wizard |
| CLI run | `src/cli/commands/run.py` | 531 | Loop execution command |
| **Total src** | | **~12,107** | |
| **Total tests** | 29 test files | **~8,658** | 627 test functions |

### Unique Features

1. **Git-branch-based versioning** (`ProgramManager`) — every iteration is a git branch
   (`program/iter-skill-N`), frontier members are git tags. Full lineage tracking, diff, reset.
   This is **the most sophisticated version control** of any skill evolution system.

2. **Frontier-based selection** — maintains top-N programs (configurable `frontier_size=3`),
   with 3 selection strategies: `best` (greedy), `random`, `round_robin`. Our system has no
   frontier concept.

3. **Multi-agent architecture** — 4 distinct agent roles:
   - **Base agent**: answers questions
   - **Skill proposer**: analyzes failures, decides create/edit
   - **Skill generator**: writes skill files
   - **Prompt generator**: optimizes system prompts
   Each runs as a separate LLM session with its own system prompt and tool set.

4. **Adaptive truncation fallback** — when the proposer fails (context limit/timeout), it
   retries with progressively more aggressive truncation (Level 0: full → Level 1: moderate →
   Level 2: aggressive), then falls back to single-shortest-failure focus.

5. **Feedback history with outcome tracking** — every proposal records whether it improved,
   was kept, or discarded, with score deltas. Future proposers read this to avoid repeating
   failed approaches.

6. **5 scorer types**: `multi_tolerance` (fuzzy numeric/text), `exact`, `llm` (LLM-as-judge
   with rubric), `script` (shell command), `harbor` (container verifier reward).

7. **LLM-as-judge scorer** — configurable rubric + model + provider. Supports Anthropic,
   OpenAI, Google, OpenRouter, Fireworks. Our system has no LLM judge.

8. **6 agent harness integrations**: Claude Code, OpenCode, OpenHands, Codex CLI, Goose, Harbor.
   Each has its own executor + options module. Harbor runs containerized benchmarks.

9. **Run caching** — content-hash of `.claude/skills/` + `prompt.txt` + question → cached
   AgentTrace. Automatically invalidates when skills change.

10. **Checkpoint/resume** — saves iteration + sampling state to `.evoskill/loop_checkpoint.json`
    for exact resume after interruption. `--continue` flag resumes from existing frontier.

11. **Multi-provider LLM calls** — `call_llm()` supports anthropic, openai, openrouter,
    fireworks, google with unified interface.

12. **Docker + Daytona remote execution** — run the entire loop in a container or cloud sandbox.

13. **FeedbackDescent** (from GEPA paper) — pairwise comparison optimization via textual feedback
    rather than scalar rewards. Separate module, not wired into main loop but available.

### What We Can Learn

**High-priority borrowable features:**

1. **Frontier-based selection** (★★★★★) — keeping top-N programs and selecting parents
   strategically would make our single-best-only gate much more robust. We currently discard
   all non-improving edits; a frontier would let us explore multiple promising directions.

2. **Git-branch versioning** (★★★★★) — every iteration as a git branch gives full lineage,
   diffing, and rollback. Our staging directory approach is fragile by comparison.

3. **Feedback history with outcome tracking** (★★★★☆) — recording whether each proposal
   improved/regressed, and feeding it back to the proposer, would make our reflect() calls
   smarter over time. We currently have no cross-cycle memory of what was tried before.

4. **LLM-as-judge scorer** (★★★★☆) — for tasks without exact answers or exit codes, an LLM
   judge with configurable rubric would dramatically expand the types of tasks we can evolve
   on. Currently we only have exact-match and outcome-derived scoring.

5. **Multi-failure pattern analysis** (★★★★☆) — analyzing ALL failures in a batch to find
   COMMON patterns, rather than per-task fixes. Our reflect() processes failures individually.

6. **Adaptive truncation fallback** (★★★☆☆) — progressive context reduction on proposer
   failure is a simple, effective resilience pattern.

7. **Run caching by content hash** (★★★☆☆) — would save significant API costs on re-evaluation
   of unchanged skill/memory configurations.

**Lower priority:**
- Multi-harness support (we only target Claude Code) — but architecturally interesting
- Docker/Daytona remote execution — operational convenience
- Prompt evolution mode — we focus on skill/memory, not system prompts

---

## 3. Triple Comparison Table

### Architecture & Philosophy

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Core paradigm** | Multi-epoch trainer | Generator-Verifier co-evolution | Frontier-based evolutionary loop | Offline sleep cycle |
| **Code status** | Proprietary | Paper-only (0 LoC) | Full OSS (~12K LoC) | Active (~3.5K LoC) |
| **Test count** | Unknown | 0 | 627 functions / 29 files | 99 tests |
| **Primary language** | Python | — | Python | Python |
| **Execution model** | In-process training | Unknown | Multi-agent subprocess loop | 6-stage pipeline |
| **Design philosophy** | Gradient-descent analog | Co-evolutionary game theory | Evolutionary programming | Biological sleep cycle |

### Skill Package Format

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Skill format** | Single doc (skill string) | Multi-file package | Multi-file dir (`SKILL.md` + scripts) | Single `SKILL.md` file |
| **Skill storage** | In-memory / file | Unknown | `.claude/skills/NAME/` dirs | `~/.claude/skills/NAME/SKILL.md` |
| **Multi-file support** | ❌ | ✅ (instructions + scripts + assets) | ✅ (SKILL.md + references + scripts) | ❌ |
| **Memory/CLAUDE.md** | ❌ | ❌ | ❌ | ✅ (separate memory evolution) |
| **Metadata** | Score tracking | Unknown | `program.yaml` (prompt, tools, score) | EditRecord (target, op, content, rationale) |

### Evolution Mechanism

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Training loop** | Multi-epoch (2376 LoC) | Iterative generate-verify-refine | Iterative (max_iterations=20) | Single-night cycle (6 stages) |
| **LR scheduler** | ✅ Cosine | ❌ | ❌ | ❌ |
| **Edit operations** | add/delete/replace | Unknown | create/edit (skill), rewrite (prompt) | add/delete/replace |
| **Gradient merge** | ✅ Layered LLM merge | ❌ | ❌ | ❌ |
| **Slow update** | ✅ Cross-epoch accumulation | ❌ | ❌ | ❌ |
| **Rejected-edit buffer** | ✅ | ❌ | ✅ (feedback_history.md with outcomes) | ✅ (rejected_edits in report) |
| **Frontier/top-N** | ❌ (single best) | ❌ | ✅ (frontier_size=3, 3 strategies) | ❌ (single best) |
| **Parent selection** | N/A | N/A | best/random/round_robin | N/A |
| **Co-evolving verifier** | ❌ | ✅ (surrogate verifier) | ❌ | ❌ |
| **Proposer brainstorming** | ❌ | Unknown | ✅ (mandatory 2-3 approaches) | ❌ |
| **Multi-failure analysis** | ❌ | Unknown | ✅ (batch failures → common patterns) | ❌ (per-task) |

### Scoring & Validation

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Gate/validation** | ✅ Strict improvement | ✅ Opaque oracle pass/fail | ✅ Score > frontier worst | ✅ Strict improvement (hard/soft/mixed) |
| **Ground truth needed** | ✅ (benchmark) | ✅ (sealed oracle) | ✅ (benchmark answers) | ❌ (works without GT) |
| **Score types** | Hard + soft | Pass/fail (opaque) | Hard only (0/1) | Hard + soft |
| **Scoring methods** | Exact + partial credit | Unknown | multi_tolerance/exact/llm/script/harbor | exact + outcome-derived + keyword-soft |
| **LLM-as-judge** | ❌ | ✅ (surrogate verifier) | ✅ (configurable rubric + model) | ❌ |
| **Exit-code judging** | ❌ | ❌ | ✅ (LiveCodeBench sandbox) | ✅ |
| **Fuzzy matching** | ❌ | ❌ | ✅ (numeric tolerance, unit detection, text overlap) | ✅ (keyword overlap soft score) |
| **Multi-tolerance levels** | ❌ | ❌ | ✅ (5 levels, weighted avg) | ❌ |
| **Information isolation** | ❌ | ✅ (verifier can't see GT) | ❌ | ❌ |

### Data Sources & Harvesting

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Data source** | Academic benchmarks | SkillsBench | CSV / Harbor datasets | Real session transcripts |
| **Harvest from live sessions** | ❌ | ❌ | ❌ | ✅ (`~/.claude/projects/*.jsonl`) |
| **Feedback signal detection** | ❌ | ❌ | ❌ | ✅ (pos/neg keywords, bilingual) |
| **Self-referential filtering** | ❌ | ❌ | ❌ | ✅ (filters own sleep-cycle sessions) |
| **Headless replay filtering** | ❌ | ❌ | ❌ | ✅ |
| **Category/stratified sampling** | ❌ | Unknown | ✅ (round-robin per category) | ❌ |
| **Train/val split** | ✅ | Unknown | ✅ (stratified, configurable ratio) | ✅ (hash-based, 34% holdout) |
| **Dream/generated data** | ❌ | ❌ | ❌ | ✅ (`origin="dream"` support in models) |

### Backend & LLM Support

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Agent harnesses** | 1 (in-process) | 2 (Claude Code, Codex) | 6 (Claude, OpenCode, OpenHands, Codex, Goose, Harbor) | 1 (Claude Code) |
| **LLM providers** | 9 | Unknown | 5+ (Anthropic, OpenAI, Google, OpenRouter, Fireworks) | 1 (Anthropic via claude CLI) |
| **Mock/dry-run mode** | ❌ | ❌ | ❌ | ✅ (MockBackend, zero deps) |
| **Real backend** | ✅ | ✅ | ✅ | ✅ (CCBackend via `claude -p`) |
| **Containerized execution** | ❌ | ❌ | ✅ (Docker, Daytona) | ❌ |
| **Cost tracking** | ❌ | ❌ | ✅ (per-iteration + cumulative $) | ✅ (token estimation) |

### Versioning & Persistence

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Versioning method** | In-memory state | Unknown | Git branches + tags | Staging directories |
| **Lineage tracking** | ❌ | Unknown | ✅ (parent chain via program.yaml) | ✅ (evolution_tree.py) |
| **Checkpoint/resume** | ❌ | Unknown | ✅ (loop_checkpoint.json, `--continue`) | ✅ (SleepState per-night) |
| **Run caching** | ❌ | ❌ | ✅ (content-hash-based RunCache) | ❌ |
| **Reset/cleanup** | ❌ | ❌ | ✅ (`evoskill reset`) | ❌ |
| **Diff between iterations** | ❌ | ❌ | ✅ (`evoskill diff`) | ❌ |

### Feedback & Learning Loop

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Cross-iteration feedback memory** | ✅ (slow_update) | ✅ (verifier evolution) | ✅ (feedback_history.md) | ❌ |
| **Outcome tracking** | ✅ | Unknown | ✅ (improved/kept/discarded + score delta) | ✅ (accepted/rejected edits in report) |
| **Discarded approach avoidance** | ✅ (rejected buffer) | Unknown | ✅ (proposer reads past discards) | ❌ |
| **Comparison-based optimization** | ❌ | Unknown | ✅ (FeedbackDescent pairwise) | ❌ |
| **Reflect on successes** | ✅ | Unknown | ❌ (failures only) | ✅ (CCBackend pairs failure vs success) |

### Real-time & Integration Features

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **L1 real-time distillation** | ❌ | ❌ | ❌ | ✅ |
| **PostToolUse hook** | ❌ | ❌ | ❌ | ✅ |
| **CLI interface** | ❌ | ❌ | ✅ (`evoskill init/run/eval/skills/diff/logs/reset`) | ✅ (`cycle.py --action run/dry-run/status/adopt`) |
| **Python API** | ❌ | ❌ | ✅ (`EvoSkill` class) | ❌ |
| **Progress reporting** | ✅ | ❌ | ✅ (live table, events callback) | ✅ (markdown report) |
| **Config format** | Python args | — | TOML (`.evoskill/config.toml`) | Python args |

### Cross-task / Cross-model Transfer

| Feature | SkillOpt | CoEvoSkills | EvoSkill | Our skill-evolution |
|---|---|---|---|---|
| **Cross-model transfer** | ❌ | ✅ (6 LLMs) | ✅ (demonstrated) | ❌ |
| **Cross-task transfer** | ❌ | ✅ (11 domains) | ✅ (SealQA → BrowseComp) | ❌ |
| **Cross-agent transfer** | ❌ | ✅ (Claude + Codex) | ✅ (6 harnesses) | ❌ |

---

## 4. Recommendations

Ranked by **impact-to-effort ratio** (highest first):

### Tier 1 — High Impact, Moderate Effort (do these first)

| # | Feature | Source | Effort | Impact | Rationale |
|---|---|---|---|---|---|
| 1 | **Frontier-based selection (top-N)** | EvoSkill | 2-3 days | ★★★★★ | Our single-best gate is fragile — one bad night resets progress. A frontier of 3-5 candidates gives evolutionary resilience. Implementation: extend `gate.py` + `state.py` to track multiple candidates with scores. |
| 2 | **Feedback history with outcome tracking** | EvoSkill | 1-2 days | ★★★★★ | Our `reflect()` has no memory of past attempts. Recording "what was tried, what worked, what was discarded" and feeding it to the next `reflect()` call would prevent repeating failed approaches. Implementation: append-only markdown file read by CCBackend.reflect(). |
| 3 | **LLM-as-judge scorer** | EvoSkill | 2 days | ★★★★☆ | Our scoring is limited to exact-match + outcome-derived. An LLM judge with configurable rubric would let us evolve on open-ended tasks. Implementation: new `LLMJudge` class implementing `Backend.judge()`, calling an LLM with a rubric prompt. |
| 4 | **Multi-failure pattern analysis** | EvoSkill | 1-2 days | ★★★★☆ | Our reflect() processes failures individually. Batching all failures and asking the LLM to find COMMON patterns would produce more general, transferable skill edits. Implementation: modify CCBackend.reflect() to pass all failures in one prompt. |

### Tier 2 — High Impact, Higher Effort

| # | Feature | Source | Effort | Impact | Rationale |
|---|---|---|---|---|---|
| 5 | **Git-branch versioning** | EvoSkill | 3-5 days | ★★★★☆ | Replace staging directories with git branches for full lineage, diffing, and rollback. Big architectural change but pays off long-term. |
| 6 | **Run caching by content hash** | EvoSkill | 2 days | ★★★☆☆ | Hash of skill+memory+task → cached result. Saves significant API costs when re-evaluating unchanged configurations across nights. |
| 7 | **Checkpoint/resume mid-cycle** | EvoSkill | 1-2 days | ★★★☆☆ | If a sleep cycle is interrupted, resume from the last completed stage rather than restarting. |

### Tier 3 — Medium Impact, Exploratory

| # | Feature | Source | Effort | Impact | Rationale |
|---|---|---|---|---|---|
| 8 | **Adaptive truncation fallback** | EvoSkill | 0.5 days | ★★★☆☆ | When reflect() hits context limits, retry with shorter traces. Simple resilience improvement. |
| 9 | **Proposer brainstorming** | EvoSkill | 1 day | ★★★☆☆ | Force the reflect LLM to generate 2-3 approaches before settling. Could improve edit quality. |
| 10 | **Multi-file skill packages** | CoEvoSkills | 5+ days | ★★★★☆ | Support skills with helper scripts + references, not just markdown. High value but large change to harvest/replay/staging. |
| 11 | **Multi-tolerance scoring** | EvoSkill | 1 day | ★★☆☆☆ | Weighted average across 5 tolerance levels. Marginal improvement over our current keyword-soft score. |
| 12 | **Co-evolving verifier** | CoEvoSkills | Unknown | ★★★★★+ | The holy grail — a self-improving judge. But CoEvoSkills hasn't released code, so this is research-grade. Track their release. |

### What We Already Have That Others Don't (don't lose these)

| Feature | Our Advantage | None of the 3 competitors have |
|---|---|---|
| **L1 real-time distillation** | Learn from live sessions in real-time | SkillOpt, CoEvoSkills, EvoSkill all require offline benchmarks |
| **PostToolUse hook** | Intercept tool calls for immediate feedback | No competitor has this |
| **Works without ground truth** | Evolve from real session transcripts | EvoSkill and CoEvoSkills both require benchmarks with GT |
| **Bilingual feedback detection** | Chinese + English feedback keywords | Others are English-only |
| **Mock backend with zero deps** | Test the full pipeline without API keys | EvoSkill requires real agent SDKs |
| **Failure-vs-success contrast** | CCBackend pairs each failure with most similar success | EvoSkill only looks at failures |
| **99 tests, all green** | Robust, well-tested core | CoEvoSkills has 0 tests, EvoSkill has 627 but many are harness-specific |

### Strategic Positioning

Our **unique value proposition** remains: **the only system that evolves skills from real,
unsupervised agent usage sessions without requiring any benchmark or ground truth.**

- **EvoSkill** requires a CSV/Harbor benchmark with known answers → can't help with day-to-day
  agent usage that has no GT.
- **CoEvoSkills** requires SkillsBench → same limitation, plus no code released.
- **SkillOpt** requires academic benchmarks → same limitation.
- **Our system** harvests real transcripts, mines tasks from them, and evolves → zero-setup
  continuous improvement.

The **best borrowing strategy** is to take EvoSkill's proven evolutionary mechanics (frontier,
feedback history, LLM judge) and graft them onto our unique data pipeline (harvest → mine →
replay from real sessions). This would give us EvoSkill's rigor with our zero-setup advantage.
