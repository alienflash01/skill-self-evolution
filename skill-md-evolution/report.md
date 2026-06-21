# AI agent 中以 SKILL.md（技能指令文档）为载体的 skill 自进化方法 · 调研报告

> 共 **22** 个研究对象，每对象覆盖 37 个字段。
> 字段框架融合《A Survey of Self-Evolving Agents》(arXiv:2507.21046) What/When/How/Where 分类法 + 新增「SKILL.md 专属维度」与「可借鉴要点」。

## 研究对象分类

**A. 学术框架｜直接以 SKILL.md / 技能文档为进化载体**

1. SkillOpt
2. SkillOpt-Sleep
3. SkillSmith
4. CoEvoSkills (EvoSkills)
5. EvoSkill
6. DRAFT (From Exploration to Mastery)
7. SkillWeaver

**B. 工程实践｜SKILL.md / CLAUDE.md 自改进 agent**

8. OpenSpace
9. AutoSkill / SkillEvo
10. claude-self-improving-skills
11. claude-evolving-skills (reflect-and-learn)
12. Homunculus nightly agent (/hm-night)
13. Skill Evolver (nomadically.work)
14. venotyh/evoskill (evolutionary skill agent)

**C. 思想来源｜文本空间优化范式**

15. TextGrad
16. GEPA
17. OPRO / PromptBreeder / EvoPrompt

**D. 思想来源｜经验/记忆蒸馏为文档**

18. ExpeL
19. Agent Workflow Memory (AWM)
20. MUSE (Learning on the job)
21. Reflexion / Self-Refine

**E. 对照组｜非文档载体**

22. Voyager (对照)

## 目录

### A. 学术框架｜直接以 SKILL.md / 技能文档为进化载体

1. [SkillOpt](#skillopt) — **时间**: arXiv v1 22 May 2026; v2 25 May 2026 | **类型**: academic | **文档载体**: Yes. The core carrier is a readable markdown instruction documen…<br>**编辑粒度**: Bounded add/delete/replace edits under a textual learning-rate b… | **版本门控**: Held-out validation gate (strict-improvement): a candidate skill… | **进化时机**: sleep-time / inter-test-time offline. All optimization happens o…<br>**进化方法**: rollout_optimization (non-gradient, text-space optimization) mir… | **部署域**: general. The same optimizer interface works across QA, spreadshe…
2. [SkillOpt-Sleep](#skillopt-sleep) — **时间**: 2026 (parent SkillOpt paper May 2026, arXiv:2605.23904; SkillOpt… | **类型**: industry (open-source deployment-time companion plugin) derived… | **文档载体**: Yes (pure readable instruction markdown is the core carrier). Th…<br>**编辑粒度**: Bounded add/delete/replace edits (the SkillOpt textual learning-… | **版本门控**: Rich and multi-layer: (1) held-out validation gate (keep an edit… | **进化时机**: sleep-time — periodic offline 'sleep' (nightly / off-idle) repla…<br>**进化方法**: rollout_optimization — non-gradient text-space optimization (the… | **部署域**: specialized — coding / productivity agent domain (Claude Code, C…
3. [SkillSmith](#skillsmith) — **时间**: 2026-05-31 (arXiv v1) | **类型**: academic | **文档载体**: 混合. Core carrier is the workflow body w containing readable step…<br>**编辑粒度**: bundle(技能+工具原子联合编辑). Reflection emits an atomic proposal bundle… | **版本门控**: Pareto 前沿 + 留出验证门控(held-out). Instance-level Pareto front G main… | **进化时机**: inter-test-time + sleep-time. Evolution proceeds in discrete ite…<br>**进化方法**: co_evolutionary + population_evolutionary + rollout_optimization… | **部署域**: general(通用). Spans document QA, web search QA, and multi-modal r…
4. [CoEvoSkills (EvoSkills)](#coevoskills-evoskills) — **时间**: 2026-04-02 (arXiv v1); 2026-04-12 (v2) | **类型**: academic | **文档载体**: 混合. Core carrier includes a readable instruction document (SKILL…<br>**编辑粒度**: 全新生成 / 整文档重写. Each revision S(i+1) is produced by the generator… | **版本门控**: 留出验证门控(held-out) + best-snapshot save. A held-out Ground-Truth O… | **进化时机**: inter-test-time / sleep-time. Offline co-evolution executed per…<br>**进化方法**: co_evolutionary + rollout_optimization(非梯度, 文本空间优化). Non-gradien… | **部署域**: general(通用). SkillsBench spans 11 domains (incl. Natural Science…
5. [EvoSkill](#evoskill) — **时间**: 2026-03-03 (arXiv v1 submitted 3 Mar 2026); open-source code rep… | **类型**: academic (arXiv paper) + industry/open-source framework (Apache-… | **文档载体**: 混合 (instruction-document-centric). Core carrier is a readable SK…<br>**编辑粒度**: 全新生成 (create new skill folder+SKILL.md via action='create') + ed… | **版本门控**: 留出验证门控(held-out) + git分支前沿选择 + DAG血脉. Each new program is scored… | **进化时机**: inter-test-time(任务间离线). The self-improvement loop runs offline a…<br>**进化方法**: population_evolutionary + rollout_optimization(非梯度, 文本空间) + rewa… | **部署域**: general(通用) -> specialized. Turns general-purpose coding agents…
6. [DRAFT (From Exploration to Mastery)](#draft-from-exploration-to-mastery) — **时间**: arXiv v1 10 Oct 2024, v2 26 Feb 2025; ICLR 2025 Oral (top 1.8%) | **类型**: academic (ICLR 2025 Oral paper, open-source reference implementa… | **文档载体**: Yes (pure readable natural-language instruction document is the…<br>**编辑粒度**: Whole-document rewrite per iteration: the Rewriter emits a compl… | **版本门控**: No quality-based version gate (no held-out validation, no Pareto… | **进化时机**: inter-test-time: the documentation is refined offline, between d…<br>**进化方法**: rollout_optimization (non-gradient, text-space optimization via… | **部署域**: general — general-purpose tool-use / tool-call domain (API invoc…
7. [SkillWeaver](#skillweaver) — **时间**: 2025-04-09 (arXiv v1) | **类型**: academic | **文档载体**: 混合. The skill carrier is primarily executable Python code (the A…<br>**编辑粒度**: 全新生成 (whole-function regeneration during synthesis/polishing) +… | **版本门控**: 留出验证门控(held-out) / validation gating. Each candidate API must pa… | **进化时机**: inter-test-time + sleep-time. Skill discovery/synthesis/honing h…<br>**进化方法**: imitation_demonstration + rollout_optimization (non-gradient, te… | **部署域**: specialized (web/GUI automation domain).

### B. 工程实践｜SKILL.md / CLAUDE.md 自改进 agent

8. [OpenSpace](#openspace) — **时间**: 2026-03-25 (open-sourced); v0.1.0 on 2026-04-03. Active developm… | **类型**: industry (open-source self-evolving skill engine / agent framewo… | **文档载体**: Yes. The core carrier is a human-readable instruction document:…<br>**编辑粒度**: 最小 diff / PATCH. patch.py supports multi-file FULL / DIFF / PATC… | **版本门控**: DAG 血脉版本化 + validation gating(门控) + 确认门控. SQLite store maintains… | **进化时机**: inter-test-time + sleep-time. Post-Execution Analysis runs after…<br>**进化方法**: rollout_optimization(非梯度, 文本空间) + imitation_demonstration. Non-g… | **部署域**: general(通用). Spans coding, DevOps, web research, desktop/GUI aut…
9. [AutoSkill / SkillEvo](#autoskill-skillevo) — **时间**: arXiv v1 submitted 2026-03-01, v2 2026-03-05. Release timeline:… | **类型**: academic (formal arXiv paper with Method/System/Experimental sec… | **文档载体**: Yes (with optional hybrid extensions). The core carrier is a hum…<br>**编辑粒度**: Mainly 全新生成 (LLM extraction emits a fresh candidate skill) + 整文档… | **版本门控**: Multiple mechanisms: (1) semantic versioning with patch bump on… | **进化时机**: inter-test-time (extraction after turns/sessions; AutoSkill4Open…<br>**进化方法**: Training-free, prompt-driven composition (NO gradient/RL/SFT). F… | **部署域**: general (model-agnostic personalization layer across coding, wri…
10. [claude-self-improving-skills](#claude-self-improving-skills) — **时间**: 2026-06-09 (GitHub repo created; first public version). v0.9.0 a… | **类型**: industry (open-source framework / Claude Code plugin) leaning bl… | **文档载体**: 是 (Yes — instruction-document-centric). The core carrier is a re…<br>**编辑粒度**: 有界增删替换 (bounded add/delete/replace via the `Edit` tool) is stron… | **版本门控**: staging+backup + review-gated adopt + automatic rollback. (a) Pr… | **进化时机**: inter-test-time primarily. The Stop hook evaluates complexity at…<br>**进化方法**: imitation_demonstration + rollout_optimization (non-gradient, te… | **部署域**: specialized (Claude Code coding/agent productivity). The plugin…
11. [claude-evolving-skills (reflect-and-learn)](#claude-evolving-skills-reflect-and-learn) — **时间**: 2026-03 (LinkedIn essay 'I Stopped Chasing Viral Agentic Workflo… | **类型**: blog_practice | **文档载体**: 混合 — Core carrier is human-readable Markdown instruction documen…<br>**编辑粒度**: 有界增删替换 (add/delete/replace) on CLAUDE.md rules and memory entrie… | **版本门控**: Layered: (1) review-gated adopt — P0-AUTO (>=8.0, 3/3 voices agr… | **进化时机**: sleep-time (primary: weekly scheduled Wednesday 3am) + inter-tes…<br>**进化方法**: rollout_optimization (non-gradient text-space optimization via T… | **部署域**: specialized (coding) — Claude Code is a coding agent; skills ope…
12. [Homunculus nightly agent (/hm-night)](#homunculus-nightly-agent-hm-night) — **时间**: 2026 (v0.5.0 initial release Mar 2026; v0.6.3 evolution tiers Ma… | **类型**: industry (open-source self-evolution framework/plugin) + blog_pr… | **文档载体**: Yes (hybrid leaning yes). The core carrier of a 'skill' is a hum…<br>**编辑粒度**: Bounded add/delete/replace (not whole-doc rewrite). `/improve-sk… | **版本门控**: Multi-layer: (1) validation gating — eval→improve loop until 100… | **进化时机**: sleep-time (nightly agent, the headline mode) + inter-test-time…<br>**进化方法**: rollout_optimization (non-gradient text-space: eval→improve→roll… | **部署域**: specialized — coding / productivity agent domain (Claude Code, C…
13. [Skill Evolver (nomadically.work)](#skill-evolver-nomadicallywork) — **时间**: 2026-02-25 | **类型**: blog_practice | **文档载体**: Yes — the core carrier is human-readable Markdown instruction do…<br>**编辑粒度**: Minimal diff / bounded add-delete-replace. Apply Changes priorit… | **版本门控**: Validation gating (held-out Verification Gate) + rejected-edit f… | **进化时机**: inter-test-time (between task runs, as a dedicated pipeline stag…<br>**进化方法**: rollout_optimization (non-gradient, text-space prompt editing) +… | **部署域**: Specialized (job-posting classification / remote-EU-job filterin…
14. [venotyh/evoskill (evolutionary skill agent)](#venotyhevoskill-evolutionary-skill-agent) — **时间**: 2026 (repo activity ~2026-05; CHANGELOG 'Unreleased' section; no… | **类型**: blog_practice / industry (small open-source experimental CLI too… | **文档载体**: 否 (pure structured data, not a readable instruction document). T…<br>**编辑粒度**: 整字段重写 + 有界增删替换 (field-level, not whole-document). Mutation opera… | **版本门控**: DAG血脉 (for tracking/query only) + 生成代际剪枝 (generational pruning,… | **进化时机**: sleep-time (夜间/空闲离线) + inter-test-time (manual batch). The headl…<br>**进化方法**: population_evolutionary + reward-based (LLM-as-judge). Classic g… | **部署域**: general (通用). A general-purpose agent-skill evolution toy: not s…

### C. 思想来源｜文本空间优化范式

15. [TextGrad](#textgrad) — **时间**: arXiv preprint: 11 June 2024 (arXiv:2406.07496). Published in Na… | **类型**: academic | **文档载体**: No. The optimized object is a raw text string (natural-language…<br>**编辑粒度**: Whole-variable regeneration (全新生成 / 整变量重写). The TextualGradientD… | **版本门控**: Held-out validation gating with greedy hill-climbing selection o… | **进化时机**: Predominantly inter-test-time (offline optimization between/arou…<br>**进化方法**: rollout_optimization in text space (non-gradient) driven by rewa… | **部署域**: General — TextGrad is a general-purpose optimization framework f…
16. [GEPA](#gepa) — **时间**: 2025; published as a conference paper at ICLR 2026 | **类型**: academic | **文档载体**: 是. The optimized artifact is fundamentally a human-readable natu…<br>**编辑粒度**: 整文档重写 per module per mutation (the reflection LM emits a wholly… | **版本门控**: Pareto 前沿 + 留出验证门控. Multi-level gating: (a) Minibatch eval first… | **进化时机**: inter-test-time (offline optimization loop over D_train before d…<br>**进化方法**: rollout_optimization (文本空间, non-gradient) combined with populati… | **部署域**: general (general-purpose compound AI workflows: QA, math, instru…
17. [OPRO / PromptBreeder / EvoPrompt](#opro-promptbreeder-evoprompt) — **时间**: All three September 2023: OPRO arXiv:2309.03409 (Sep 7, 2023; v3… | **类型**: academic (three peer-reviewed papers, ICLR 2024 x2 + ICML 2024) | **文档载体**: 是. The evolved object is fundamentally human-readable natural-la…<br>**编辑粒度**: 整文档重写 (whole-instruction rewrite per mutation; no PATCH/diff). O… | **版本门控**: 留出验证门控 (held-out development set) + greedy/top-k selection. OPRO… | **进化时机**: inter-test-time (offline optimization phase before deployment).…<br>**进化方法**: population_evolutionary + rollout_optimization (文本空间, non-gradie… | **部署域**: general (general-purpose NLP reasoning: math, commonsense, class…

### D. 思想来源｜经验/记忆蒸馏为文档

18. [ExpeL](#expel) — **时间**: arXiv v1 submitted 20 Aug 2023; v2 18 Dec 2023; v3 20 Dec 2024.… | **类型**: academic (AAAI-24 paper). Model weights never trained; method is… | **文档载体**: 是 (leaning). Primary carrier is readable natural-language insigh…<br>**编辑粒度**: 有界增删替换 via four atomic operators on the insight set: ADD (new in… | **版本门控**: Count-based implicit gating only: an insight is auto-pruned when… | **进化时机**: inter-test-time (任务间离线). Insight extraction and library construc…<br>**进化方法**: reward-based (text feedback from binary success/failure outcomes… | **部署域**: general (通用). Tested across diverse decision-making domains (QA,…
19. [Agent Workflow Memory (AWM)](#agent-workflow-memory-awm) — **时间**: 2024-09-11 (arXiv v1); published at ICML 2025 (Poster), PMLR 267… | **类型**: academic | **文档载体**: Hybrid (混合). The workflow is a human-readable instruction docume…<br>**编辑粒度**: Wholesale generation + append-only addition. The LM induction mo… | **版本门控**: Minimal. (1) Online mode: an LM-evaluator (Pan et al. 2024 AutoE… | **进化时机**: Both. Offline = sleep-time / inter-test-time (induce once from t…<br>**进化方法**: imitation_demonstration + non-gradient text-space rollout optimi… | **部署域**: Specialized (web navigation / digital GUI agent domain). General…
20. [MUSE (Learning on the job)](#muse-learning-on-the-job) — **时间**: 2025-10-09 (arXiv v1) | **类型**: academic | **文档载体**: Yes (structurally). The Procedural Memory is a readable SOP ('St…<br>**编辑粒度**: Bounded incremental update + post-task global refinement merge.… | **版本门控**: No git-branch / DAG / Pareto / held-out validation gating. Quali… | **进化时机**: intra-test-time (Reflect+Memorize after EACH sub-task attempt ->…<br>**进化方法**: imitation_demonstration (distill verified-successful action traj… | **部署域**: general (general-purpose cross-application office/productivity a…
21. [Reflexion / Self-Refine](#reflexion-self-refine) — **时间**: Reflexion: arXiv v1 2023-03-20, v4 2023-10-10, NeurIPS 2023. Sel… | **类型**: academic | **文档载体**: 否 (No). Neither uses a readable instruction-document (SKILL.md /…<br>**编辑粒度**: 全新生成 (regenerate) per trial / iteration. Reflexion: each trial *… | **版本门控**: None — no held-out validation gate, no git branch, no Pareto fro… | **进化时机**: intra-test-time. Reflexion: ACROSS trials but WITHIN a single ta…<br>**进化方法**: reward-based (text feedback / self-reflection amplification) + r… | **部署域**: general (通用). Both target general-purpose reasoning, coding, dec…

### E. 对照组｜非文档载体

22. [Voyager (对照)](#voyager-对照) — **时间**: 2023-05-25 (arXiv v1); v2 revised 2023-10-19 | **类型**: academic | **文档载体**: No. The skill carrier is executable code (JavaScript), NOT a rea…<br>**编辑粒度**: 全新生成 (full regeneration). When a skill is added the entire .js p… | **版本门控**: Validation gating (held-out execution-based self-verification) —… | **进化时机**: inter-test-time + intra-test-time hybrid. The skill library evol…<br>**进化方法**: rollout_optimization (non-gradient, text/code-space optimization… | **部署域**: specialized (single game domain: Minecraft open-ended exploratio…

## 详细内容

### SkillOpt

> `academic_doc_skill` · Microsoft, 2026。把 SKILL.md 当作冻结 agent 的「可训练外部状态」，用镜像 SGD 的 文本空间优化：rollout(前向)→反思(反向)→有界 add/delete/replace 编辑(受 textual learning-rate 预算约束)→留出验证门控(仅当严格提升才接受)。rejected-edit buffer + epoch-wise slow/met

#### 基础信息

**名称**
SkillOpt

**提出机构**
Microsoft (lead); co-authors from Shanghai Jiao Tong University, Tongji University, and Fudan University

**发布时间**
arXiv v1 22 May 2026; v2 25 May 2026

**论文链接**
https://arxiv.org/abs/2605.23904

**代码链接**
https://aka.ms/SkillOpt (paper). Mirrored at https://github.com/microsoft/SkillOpt and PyPI package `skillopt` per task
note [uncertain: GitHub/PyPI URLs not directly verified, aka.ms short link is the authoritative reference in the paper]

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示. The skill document (a natural-language policy inserted into the agent context) is treated as the
'trainable external state' of a frozen target model. Model weights, harness, and evaluator are all held fixed; only the
single skill document is optimized.

**技能是否独立制品**
Yes. The deployed output is a single portable best_skill.md file (roughly 300-2000 tokens, median ~920, range 379-1995
across six benchmarks). In harness mode it is rendered as a per-task SKILL.md alongside task files. It is auditable,
inspectable text, reusable across models/harnesses without weight changes.

**是否文档载体**
Yes. The core carrier is a readable markdown instruction document (best_skill.md). No code or vector is shipped to the
target; the optimizer-side meta_skill is teacher-only and not deployed.

#### 技能表示

**技能编码方式**
技能文档 (.md / SKILL.md). A single natural-language skill document packages procedures, domain heuristics, tool policies,
output constraints, and failure modes. Contains a protected slow-update section delimited by SLOW_UPDATE_START /
SLOW_UPDATE_END markers.

**技能粒度**
策略规则 + 完整技能包. A single compact procedural skill (domain-level rules, not atomic actions or instance-specific fixes).
Rules are procedural/generalizable (e.g. answer-format constraints, evidence binding, search-frontier discipline).

#### SKILL.md_专属维度

**文档形态**
Pure instruction markdown document (best_skill.md), not YAML-frontmatter structured. Structurally it has a normal
editable body plus one protected slow-update block delimited by SLOW_UPDATE_START / SLOW_UPDATE_END that only the
epoch-boundary slow-update process may rewrite. Typical length 300-2000 tokens (observed 379-1995; median ~920). Final
skills grow only x2.5-x5.3 from the initial one-liner/paragraph and stay below a typical system-prompt budget. No
embedded executable code blocks shipped to the target.

**编辑粒度**
Bounded add/delete/replace edits under a textual learning-rate budget. Patch mode restricts each update to four atomic
operations: append, insert_after, replace, delete (localized operations, minimal-diff style). An alternative
rewrite_from_suggestions mode conditions a full skill rewrite on selected suggestions. Per step the optimizer ranks the
merged edit pool and clips to the top L_t edits (default L_t=4, cosine decay to floor 2). Step-level edits cannot
overwrite the protected slow-update field. Bundled skill+tool editing is NOT supported (tools/harness fixed).

**版本与门控**
Held-out validation gate (strict-improvement): a candidate skill is evaluated on a disjoint selection split D_sel with
the frozen target model and accepted only if it strictly exceeds the current selection score (ties are rejected).
Best-so-far skill tracked as best_skill.md; selection-score cache keyed by skill hash prevents re-evaluation. This is
propose-and-test selection, not git-branch/Pareto-front/DAG. Epoch-wise slow/meta update candidates pass through the
same gate.

**文档来源**
Hybrid: human- or one-liner-initialized skill, then LLM-driven iterative optimization from scored rollout trajectories
(成功轨迹归纳 + 失败轨迹蒸馏 via the optimizer model). Effectively offline benchmark training: the deployed artifact is produced by
a systematic training loop over train/selection/test splits, not a one-shot generation or community sharing.

**跨载体迁移**
Strong, explicitly demonstrated across three axes: (1) cross-model (SpreadsheetBench skill trained on GPT-5.4 improves
every smaller GPT variant; LiveMath skill transfers GPT-5.4->mini/nano); (2) cross-agent-harness Codex <-> Claude Code
(e.g. Codex-trained SpreadsheetBench skill transfers to Claude Code with +59.7pt; Claude Code-trained to Codex +43.6pt
on SpreadsheetBench); (3) cross-benchmark (OlympiadBench skill yields positive gains on Omni-MATH for
GPT-5.4/mini/nano). Every transfer row is positive (none below target no-skill baseline).

**技能库治理**
Single-skill design (no growing library, no Lotka-Volterra/retirement/archive). Bloat is controlled by: (a) textual
learning-rate/edit budget capping edits per step; (b) hierarchical merge that filters duplicate, contradictory, and
example-specific proposals before ranking; (c) compactness constraint keeping final artifact <2000 tokens; (d) only
strictly-improving edits survive into best_skill.md. No similarity-retrieval-based edit targeting or curator loop.

**失败记忆**
Yes. An epoch-local rejected-edit buffer records observed failure patterns plus, for rejected steps, the edits that were
tried and the score drop they caused. Later reflection/merge/ranking calls in the same epoch receive this buffer so the
optimizer avoids repeating failed edits and focuses on unresolved failures. Acts as explicit negative feedback
(anti-pattern memory) during training without adding inference-time cost.

**编辑安全**
(1) Scope boundary: only the skill .md is edited; target model weights, harness, backend, and benchmark evaluator are
fixed; source code and tools are never touched. (2) Bounded edits: textual learning-rate budget prevents destructive
whole-document rewrites and preserves continuity. (3) Held-out validation gate: plausible-but-harmful textual diagnoses
are rejected because they fail to improve D_sel, mitigating eval-hacking/overfitting. (4) Protected slow-update section
is off-limits to all step-level prompts. (5) Hashed selection cache avoids re-running identical candidates. (6)
Strict-improvement (ties rejected) gating. (7) best_skill.md is preserved across rejections (implicit rollback: a
rejected candidate simply does not replace current/best). No explicit pre-edit backup file or human-in-the-loop
confirmation is used (fully automated). No secret/injection checks mentioned.

**协同进化**
Primarily skill-only (a single portable skill is the only deployed object that evolves). Additionally, an optimizer-side
meta_skill co-evolves as teacher-only guidance: it summarizes which edit patterns helped/were rejected/persisted across
epochs and is prepended to future optimizer prompts (reflection/merging/ranking) but is NOT shipped to the target model.
This is a loose skill-prompt joint evolution on the optimizer side. The held-out gate acts as a fixed verifier (not
co-evolving). No skill-tool or skill-skill ecosystem evolution.

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (non-gradient, text-space optimization) mirrored on SGD. The loop is: forward pass = rollout batch
with current skill; backward pass = minibatch reflection over successes/failures producing structured add/delete/replace
edits; bounded update under textual learning-rate schedule; held-out validation gating accepts only strict improvements;
rejected-edit buffer as negative feedback; epoch-wise slow/meta update as a momentum analogue. Also reward-based in the
sense that the held-out score is the selection signal. The optimizer model and the frozen target model are separated.

**学习信号来源**
Held-out validation score (primary selection signal) + scored rollout trajectories (success/failure) from the benchmark
native evaluator. The optimizer also consumes trajectory metadata, messages, tool calls, observations, command outputs,
final answers, and verifier feedback (e.g. codex_trace_summary.txt in the Codex harness).

**奖励粒度**
outcome. A scalar task-level score r(s) in [0,1] per trajectory (benchmark native hard success / exact-match accuracy).
No dense process reward; procedural signal emerges from minibatch aggregation across outcome-scored rollouts.

**学习范式**
Offline, sleep-time (training is performed before deployment and adds zero inference-time optimizer calls at
deployment). Rollouts are on-policy with respect to the current skill (the frozen target executes with the current
skill). The optimized best_skill.md is then deployed unchanged.

#### 进化时机_When

**进化时机 (When)**
sleep-time / inter-test-time offline. All optimization happens offline over train/selection splits before deployment. At
inference time the target model simply consumes the fixed best_skill.md with no optimizer calls, no weight updates, no
online editing.

**触发方式**
Epoch-based periodic trigger driven by offline benchmark training (default 4 epochs). Each epoch resets the
rejected-edit buffer, shuffles the training split into rollout batches, and runs step-level optimization until the epoch
ends, at which point the slow/meta update fires. Not event/failure/curriculum/cron driven in the deployed agent; the
loop is launched explicitly to train a skill for a target domain.

#### 存储与检索

**技能库结构**
Single skill file (best_skill.md) per target domain. In tool-use harnesses the same file is rendered as a per-task
SKILL.md in the workspace. No skill library / vector store / graph / DAG / cloud registry; SkillOpt intentionally
optimizes one portable skill rather than growing a repository.

**检索/复用方式**
Always-on injection rather than retrieval: in direct chat the skill is prepended to the system/developer instruction; in
harnesses it is rendered as persistent procedural memory / SKILL.md. No semantic similarity search, BM25, or
description-triggered loading (single skill per domain, always loaded).

#### 验证与反馈

**验证方式**
Held-out evaluation + validation gating + functional correctness check. Every candidate skill is scored on a disjoint
selection split D_sel with the frozen target model and harness using the benchmark native evaluator (hard success /
exact-match). Default split 2:1:7 (train:selection:test) when no benchmark-specific split is stated (split_seed=42).
Headline numbers reported only on the disjoint held-out test split, measuring generalization not validation fit.

**错误纠正**
Self-revision via reflection + bounded patch edits + implicit rollback. Failed/rejected candidates are not applied
(best/current skill preserved); their edits and failure patterns enter the rejected-edit buffer for future avoidance.
Patch mode performs targeted diff repairs (append/insert_after/replace/delete). Up to three teacher refinement rounds
per minibatch. Replanning is realized through the epoch-wise slow/meta update that re-prioritizes editing directions
across epochs.

#### 环境与基座

**测试环境**
General/skills benchmark suite: SearchQA (extractive QA), SpreadsheetBench (spreadsheet code/tool manipulation,
multi-round codegen up to 30 turns, real openpyxl/pandas runtime), OfficeQA (multi-turn tool loops up to 24 tool calls),
DocVQA (multimodal document VQA), LiveMathematicianBench (math MCQ), ALFWorld (persistent embodied interaction up to 50
steps). Also SkillsBench-style general agent skills, and real coding-agent harnesses (Codex CLI, Claude Code CLI).

**底座模型**
Target (frozen student) models: GPT-5.5, GPT-5.4, GPT-5.4-mini, GPT-5.4-nano, GPT-5.2, Qwen3.5-4B, Qwen3.6-35B-A3B.
Optimizer (teacher) model: a frontier model (default GPT-5.5; ablation also uses target-matched optimizer).
Optimizer/target are explicitly separated. Both teacher and student calls default to medium reasoning effort.

**部署域 (Where)**
general. The same optimizer interface works across QA, spreadsheets, documents, multimodal QA, math, and embodied
decision making, and across direct-chat, Codex, and Claude Code execution modes. Procedural benchmarks (spreadsheets,
office QA, math) see the largest gains.

#### 评估指标

**评估指标**
success_rate (benchmark native hard score / exact-match accuracy on held-out test); generalization (cross-model,
cross-harness, cross-benchmark transfer, with every transfer row positive); sample/edit efficiency (only 1-4 accepted
edits committed to best_skill.md, median 2.5); cost (training tokens per absolute test-point: 0.6M-3.6M/pt for cheap
procedural benchmarks, up to 46.4M/pt for multimodal/long-trajectory benchmarks; total one-time training cost);
compactness (300-2000 deployed tokens). Skill-library growth is not a metric (single-skill design).

**关键结论**
Best-or-tied on all 52 of 52 evaluated (model, benchmark, harness) cells across 6 benchmarks, 7 target models, 3
harnesses. On GPT-5.5: lifts average no-skill accuracy by +23.5pt (direct chat, 58.8->82.3), +24.8pt (Codex), +19.1pt
(Claude Code). Beats the strongest per-cell baseline among human/one-shot LLM/Trace2Skill/TextGrad/GEPA/EvoSkill by
+5.4pt on average (direct chat), +14.0pt over EvoSkill (Codex), +3.2pt over EvoSkill (Claude Code). Per-benchmark
highlights on GPT-5.5 direct chat: SpreadsheetBench 41.8->80.7 (+38.9), OfficeQA 33.1->72.1 (+39.0), LiveMath 37.6->66.9
(+29.3 from a single accepted edit), ALFWorld 83.6->95.5 (+11.9). Average per-model improvement ~+17.6pt; small models
benefit most in relative terms (GPT-5.4-nano nearly doubles on DocVQA, triples on ALFWorld; Qwen3.5-4B ALFWorld
30.6->81.3). Cross-harness transfer: Codex->Claude Code SpreadsheetBench +59.7pt; Claude Code->Codex SpreadsheetBench
+43.6pt. Cross-benchmark: OlympiadBench skill positive on Omni-MATH (+1.3 to +3.7pt).

#### 局限与挑战

**局限与挑战**
From Appendix B: (1) scalability/feedback dependence - the loop relies on scored trajectories and a held-out selection
split, so it is most applicable when the task has automatic verifiers, exact-match metrics, executable checks, or
reliable feedback; open-ended/subjective/multi-dimensional/costly-to-judge domains may need stronger human or
model-based evaluation in the gate. (2) training cost - although the deployed artifact is just a compact best_skill.md
with zero inference-time cost, training requires extra rollout computation and optimizer-model calls; amortized only
when the skill is reused, less attractive for one-off tasks. (3) single-skill scope - intentionally optimizes one
portable skill rather than growing a library or changing weights; insufficient for highly heterogeneous domains needing
many disjoint procedures. (4) regression/transfer risk - optimized skills can encode domain-specific heuristics from the
training distribution, so careful held-out evaluation is needed before transferring to substantially different
models/harnesses/tasks. Implicit risks: eval-hacking (mitigated by held-out gate), doc_bloat (mitigated by edit budget),
optimizer_quality dependence (ablation shows target-matched optimizer recovers much of the gain).

#### 可借鉴要点

**可借鉴要点**
- 1. Treat the SKILL.md as the trainable EXTERNAL STATE of a frozen agent and import the full deep-learning discipline: rollout/reflection batch sizes control evidence noise, a textual learning-rate (edit budget) with a schedule controls step size, the held-out selection split acts as the validation set, and the epoch-wise slow/meta update acts as a momentum term. This turns ad-hoc prompt revision into a reproducible optimization process and is the core reason SkillOpt is stable and beats uncontrolled self-rewriting.
- 2. Use a STRICT held-out validation gate (accept only if strictly better; reject ties) plus a rejected-edit buffer that records failed edits and the score drops they caused. This converts the optimizer into propose-and-test search: plausible-but-harmful textual diagnoses are filtered out, failures become negative feedback for later steps, and the deployed artifact stays compact (only 1-4 edits survive into best_skill.md) rather than accumulating every reflection. This directly addresses eval-hacking, doc-bloat, and regression risk.
- 3. Separate the optimizer (a strong frontier teacher model) from the frozen target student, and keep the optimizer-side meta_skill teacher-only while shipping only a compact best_skill.md. Train once offline over train/selection splits, then deploy with ZERO inference-time optimizer calls; the resulting auditable text artifact transfers across model scales, across Codex/Claude Code harnesses, and to nearby benchmarks without any weight updates - making it a practical domain-adaptation layer for closed frontier models.

#### 不确定字段

- code_link (GitHub microsoft/SkillOpt and PyPI skillopt could not be directly fetched/verified; the paper only references the aka.ms/SkillOpt short link)
- doc_form (no explicit mention of YAML frontmatter; assumed pure natural-language markdown with a delimited protected slow-update section)
- safety_guardrails (no explicit mention of pre-edit file backups, secret/injection scanning, or human-in-the-loop gating; inferred as fully automated)

---

### SkillOpt-Sleep

> `academic_doc_skill` · Microsoft, 2026。SkillOpt 的部署期「睡眠」伴侣。夜间离线收割 ~/.claude session→ 挖掘反复出现的任务→offline replay→reflect→有界编辑→held-out gate→staged proposal→(用户) adopt。融合 SkillOpt + Claude Dreams + agent sleep 三思想。 作用于 CLAUDE.m

#### 基础信息

**名称**
SkillOpt-Sleep

**提出机构**
Microsoft (Microsoft Research; same team as the SkillOpt paper — Yifan Yang et al.; repo microsoft/SkillOpt)

**发布时间**
2026 (parent SkillOpt paper May 2026, arXiv:2605.23904; SkillOpt-Sleep plugin engineered and shipped June 2026)

**代码链接**
https://github.com/microsoft/SkillOpt/tree/main/plugins/claude-code (also plugins/codex, plugins/copilot; engine in
top-level skillopt_sleep/ package, zero-dependency from the research stack); report:
https://github.com/microsoft/SkillOpt/blob/main/docs/sleep/FINAL_REPORT.md

**类型**
industry (open-source deployment-time companion plugin) derived from academic SkillOpt research

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 (context memory & instructions): the agent's long-term memory (CLAUDE.md / AGENTS.md) and skill documents
(SKILL.md). Not model weights, not tools, not multi-agent architecture — only frozen-target external text state.

**技能是否独立制品**
Yes. The skill is an independent, reusable, human-readable markdown artifact: SKILL.md (skill) plus CLAUDE.md/AGENTS.md
(memory). Codex layout: ~/.agents/skills/<name>/SKILL.md; Claude Code: .claude skills + project CLAUDE.md; Copilot:
copilot-instructions + MCP.

**是否文档载体**
Yes (pure readable instruction markdown is the core carrier). The evolved state is a markdown instruction document; all
learning is expressed as textual rule additions/edits inside the doc.

#### 技能表示

**技能编码方式**
技能文档 (.md / SKILL.md / CLAUDE.md / AGENTS.md). Natural-language instruction markdown with protected marker-bounded
fields (a LEARNED block and <!-- SLOW_UPDATE_START --> ... <!-- SLOW_UPDATE_END --> regions).

**技能粒度**
策略规则 (policy rules) + 见解 (insights): the learned content is recurring conventions ('always add LIMIT', 'answers in
\boxed{}', 'cite the source') plus cross-night durable meta-rules from the slow-update. The container is a full skill
document but the unit of learning is rule-level.

#### SKILL.md_专属维度

**文档形态**
Pure-instruction markdown body + structured protected fields delimited by HTML-comment markers (LEARNED block;
SLOW_UPDATE_START/END). Typical length: a few hundred to ~2,000 tokens (SkillOpt best_skill.md is 300–2k tokens;
sleep-grown skills accumulate validated rules incrementally).

**编辑粒度**
Bounded add/delete/replace edits (the SkillOpt textual learning-rate budget). Step-level edits land only in the
protected LEARNED block; the slow-update writes a separate protected SLOW_UPDATE field. No whole-document rewrite; never
edits source code.

**版本与门控**
Rich and multi-layer: (1) held-out validation gate (keep an edit only if it strictly raises the real-task val score);
(2) staging (run only stages a proposal, nothing live changes); (3) backup (every adopt backs up the prior file under
staging/backup/); (4) review-gated adopt (human runs /skillopt-sleep adopt; optional --auto-adopt). Backed by a 3-way
train(dream)/val(real)/test(real) split.

**文档来源**
Session-experience extraction (read-only harvest of ~/.claude transcripts -> mine recurring tasks) + offline replay +
reflection over success/failure trajectories (contrastive multi-rollout) -> distilled rules. Fuses session-experience
extraction with success/failure-trajectory induction.

**跨载体迁移**
Cross-model (Haiku<->Sonnet) and cross-runtime / cross-agent-harness (Claude Code <-> Codex <-> Copilot) and cross-task.
Verified live: a skill optimized on one model/runtime deploys for free on another (4/4 transfers positive, including
Codex<->Claude).

**技能库治理**
Per-skill / per-project governance rather than a global skill library: bounded edit budget, protected marker fields
(LEARNED + SLOW_UPDATE) that step-edits cannot touch, slow-update consolidation that distils durable longitudinal
guidance (preventing step-level bloat). No explicit library-level dedup / retirement / Lotka-Volterra mechanism is
documented for the sleep plugin.

**失败记忆**
Yes. Rejected edits are retained as negative feedback (the SkillOpt rejected-edit buffer); the held-out gate blocks
plausible-but-wrong rules and reward-hacking; multi-rollout contrastive reflection attributes failures to specific rule
gaps; the deterministic test asserts the gate rejects an injected harmful edit.

**编辑安全**
Comprehensive: (1) scope boundary — edits only CLAUDE.md/SKILL.md/AGENTS.md, never application source code; (2)
read-only harvest of ~/.claude; (3) pre-edit backup + rollback on every adopt; (4) review-gated human-in-the-loop adopt
(staging never auto-applies unless --auto-adopt opt-in); (5) per-night token/time budget caps; (6) secrets redacted from
prompts; (7) fresh replay runs only in throwaway git worktrees; (8) isolated optimizer/target CLI calls to prevent
ambient-context leak; (9) bounded edits prevent destructive rewrites.

**协同进化**
skill-prompt 联合 (skill + memory/prompt joint): co-edits the skill doc (SKILL.md) and the memory/prompt doc
(CLAUDE.md/AGENTS.md) together. No tool evolution and no generator-verifier coevolution — the judge is a fixed rule
judge.

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization — non-gradient text-space optimization (the SkillOpt loop): offline replay (forward pass) ->
reflect on contrastive rollouts (language-level backward pass) -> bounded add/delete/replace edit -> held-out validation
gate. Augmented by imitation-style learning from success-vs-failure contrast and an epoch-wise slow/meta update.

**学习信号来源**
Success/failure trajectories (multi-rollout contrastive reflection: what did the good attempts do that the bad ones
didn't) + held-out validation score (local rule judge — the optimizer never grades itself) + self-reflection +
tool-success signal (tool_called judge for the quick-answerer seed).

**奖励粒度**
Primarily outcome (task-level pass/fail via a rule judge on the held-out set); multi-rollout contrast adds a
quasi-process signal (good vs bad attempt diff). Multi-objective reward can additionally weight tokens-down and
latency-down.

**学习范式**
Offline + sleep-time. Strictly offline imagination/replay on the user's own API budget during nightly 'sleep';
off-policy (it replays past recorded sessions); nothing is learned intra-test-time.

#### 进化时机_When

**进化时机 (When)**
sleep-time — periodic offline 'sleep' (nightly / off-idle) replay and consolidation. All evolution happens between
sessions; the live agent is never modified during a task.

**触发方式**
Periodic / cron-like (built-in `schedule` action installs a nightly entry, e.g. --hour 3 --minute 17); also usage-driven
(it harvests the user's accumulated session transcripts). Manual on-demand via /skillopt-sleep run | dry-run | adopt.

#### 存储与检索

**技能库结构**
Skill file-directory layout: skills at ~/.agents/skills/<name>/SKILL.md (Codex), .claude skills + project CLAUDE.md
(Claude Code), copilot-instructions (Copilot); proposals staged in a staging directory with a backup/ subdirectory. No
vector DB, graph, or DAG lineage.

**检索/复用方式**
Runtime: standard skill loading by description/name (the host harness loads SKILL.md on description-match). Mining
stage: frequency/recurrence-based detection of repeated tasks across session transcripts. No semantic-vector retrieval
is documented.

#### 验证与反馈

**验证方式**
Held-out evaluation + validation gating (an edit is accepted only if it strictly raises the real-task val score) +
functional correctness via a local rule judge (section_present / regex / max_chars / contains / tool_called). The
optimizer never grades itself, and dreamed tasks can never enter val/test (unit-tested invariant).

**错误纠正**
Self-revision (reflect -> re-edit across successive nights), bounded edits, rollback (every adopt backs up the prior
file), and a rejected-edit buffer as negative feedback; demonstrated multi-night convergence (e.g. thorough-analyst 0.33
-> 1.00 over 2 nights).

#### 环境与基座

**测试环境**
gbrain-evals skillopt-v1 public suite (brief-writer, advisor, thorough-analyst, quick-answerer seeds, including a real
tool-use loop); academic daily-cases (math / spreadsheet / search-QA, 4:1:5 split with dream-augmented train); fresh
SQL-analyst load-test. Real coding-agent productivity tasks via Claude Code / Codex / Copilot.

**底座模型**
Claude (Sonnet / Haiku) and Codex / OpenAI GPT (gpt-5.5); Copilot via MCP. Strong-optimizer + frozen-cheap-target split
(e.g. optimize with Sonnet, deploy on Haiku). A deterministic mock backend enables zero-cost plumbing tests.

**部署域 (Where)**
specialized — coding / productivity agent domain (Claude Code, Codex, Copilot coding assistants); adapts the agent to the user's own recurring work.

#### 评估指标

**评估指标**
success_rate (held-out score, e.g. 0.00 -> 1.00), generalization (cross-model & cross-runtime transfer), cost (per-night
token/minute budget; multi-objective accuracy-up / tokens-down / latency-down), convergence nights, gate accept/reject
counts.

**关键结论**
On gbrain-evals skillopt-v1: 4/4 Claude seeds (Sonnet->Haiku) reached held-out 0.00 -> 1.00 (brief-writer, advisor,
thorough-analyst in 1–2 nights, quick-answerer via a real tool loop); Codex self-optimized brief-writer / advisor /
quick-answerer 0 -> 1.00. 4/4 cross-model / cross-runtime transfers positive, including Codex<->Claude. The gate blocks
regressions (rejects an injected harmful edit). Honest failure logged: Claude ambient-context leak (global skills
injected into optimizer calls, one reflect returned a 21 KB skill list) fixed via isolated CLI flags (--bare
--disallowedTools '*' ...). Fresh SQL-analyst load-test 0 -> 1.00 on both backends. Honest caveat: a weak (Haiku)
optimizer is flaky — a strong optimizer model is decisive.

#### 局限与挑战

**局限与挑战**
scalability (proven on small, single-flaw skills; large production skills are expected to be messier and partial),
optimizer_quality (a weak optimizer model is flaky; needs a strong frontier optimizer), latency (each CLI call is
~14–15s startup-dominated, capping tasks/nights — fine for nightly cron but not interactive), small benchmark scale, and
deeper multi-tool / multi-turn workflows are future work. Regression and eval-hacking risks are mitigated but not fully
eliminated by the gate.

#### 可借鉴要点

**可借鉴要点**
- Sleep-time offline consolidation with a strict train(dream) / val(real) / test(real) split + held-out validation gate + review-gated human adopt. Dreaming/augmenting training data is allowed precisely because dreamed tasks can NEVER land in val or test (a unit-tested invariant) — this is the key to safe self-improvement that resists eval-hacking and overfitting.
- Strong-optimizer + frozen-cheap-target architecture: spend a little on a smart optimizer overnight to write the rules, then deploy the frozen learned skill on any cheaper model or different runtime for free ('optimize cheap, deploy anywhere'). The optimizer is a training-time lever only and adds zero inference cost at deployment.
- Bounded add/delete/replace edits confined to protected marker fields (LEARNED block, SLOW_UPDATE markers) + a rejected-edit buffer as negative feedback + mandatory backup-before-adopt + a stage-then-adopt contract. This makes self-editing of instruction docs reversible, auditable, and blast-radius-limited (source code is never touched).

#### 不确定字段

- paper_link

---

### SkillSmith

> `academic_doc_skill` · 2026。Synergy-aware Skill-Tool 协同进化框架。三大创新：(1) bundle 化的 skill-tool 联合编辑(原子提案，工具可 wrap/edit/compose/split/retire)；(2) 受 Lotka-Volterra 生态动力学启发的技能交互矩阵，建模技能间互补/冲突，指导检索/变异优先级/退休，治理 库膨胀；(3) anti-pattern me

#### 基础信息

**名称**
SkillSmith

**提出机构**
Shanghai Jiao Tong University; Eastern Institute of Technology (Ningbo); University of Science and Technology of China;
Southeast University; Ningbo Institute of Digital Twin. Authors: Yangbo Wei, Zhen Huang, Shaoqiang Lu, Junhong Qian,
Qifan Wang, Chen Wu, Lei He.

**发布时间**
2026-05-31 (arXiv v1)

**论文链接**
https://arxiv.org/abs/2606.01314

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 / Tools技能. External non-parametric state Sigma=(S,T,F): skill library S (workflow + strategy), tool library
T, and anti-pattern memory F. Model weights are NOT touched; all three components are inspectable, versionable,
transferable external assets.

**技能是否独立制品**
是. Each skill s=(m,w,r,u) is an independent reusable artifact: metadata m (name, trigger condition, version), workflow
body w (orchestration logic + step-level instructions), reference resources r (templates, domain knowledge), and scalar
utility u. Form = structured skill package (multi-component artifact, akin to a skill file directory).

**是否文档载体**
混合. Core carrier is the workflow body w containing readable step-level orchestration instructions
(instruction-document-like), but the package also bundles executable scripts and reference resources; tools expose
executable implementations f. Instruction-centric + embedded executable code => mixed.

#### 技能表示

**技能编码方式**
多文件技能包 combining natural-language SOP/workflow instructions (workflow body w) + executable scripts/code (tool
implementations f with interface description d and type signature sigma) + reference resources/templates + metadata +
scalar utility. Skills and tools are complementary, cross-referencing artifacts.

**技能粒度**
子任务workflow / 完整技能包. A skill packages a task-facing strategy with multi-step orchestration logic that invokes multiple
tools; granularity is a complete reusable capability package covering a class of tasks.

#### SKILL.md_专属维度

**编辑粒度**
bundle(技能+工具原子联合编辑). Reflection emits an atomic proposal bundle L that jointly updates skills AND tools in one
transaction; tool edits restricted to five typed lifecycle primitives (Wrap/Edit/Compose/Split/Retire). Atomicity
guarantees interdependent skill+tool changes apply simultaneously, avoiding invalid intermediate states (theorem: bundle
mutation expands the reachable valid state set Omega vs single-type edits).

**版本与门控**
Pareto 前沿 + 留出验证门控(held-out). Instance-level Pareto front G maintained (a state is non-dominated if best on >=1 training
instance); progressive validation gate before admission: tool unit test -> end-to-end integration test -> regression
check; candidates admitted only after passing all stages. Sampling from Pareto front weighted by per-instance
unique-best count.

**文档来源**
失败轨迹蒸馏. Proposal bundles generated by reflection over failed execution traces (failure set F={x: P(x)<theta});
failure-driven diagnosis with structured feedback function mu_f (compiler errors, missing-document reports, constraint
violations). Also session经验提取 via accumulated anti-pattern memory; skills can be merged via crossover of non-dominated
lineages.

**技能库治理**
库膨胀治理(Lotka-Volterra/退休/归档) + 去重合并. Ecological utility model inspired by Lotka-Volterra competition-mutualism: skill
interaction matrix beta_ij estimated from execution logs (positive=complementarity, negative=conflict); carrying
capacity K captures competition under retrieval/context/maintenance budgets; utility dynamics prioritize
mutation/retirement. Skills below retirement threshold for T_ret rounds are retired and converted to epitaphs in
anti-pattern memory. Synergy-aware merge/crossover deduplicates across non-dominated lineages. Ablation: -Eco inflates
library to 21+7 (and >80 over long run) vs 14+6 full.

**失败记忆**
是. Anti-pattern memory F: each entry phi=(p,a,c) = failure signature p + causal attribution a + remedy c. Two
mechanisms: (1) diagnostic acceleration - retrieves similar past failures and injects prior attributions into reflection
context; (2) proposal veto - blocks bundles resembling known failure patterns before submission. Also
retirement-to-epitaph pipeline converts retired skills into failure records. Ablation: removing it triples regression
rate (2.1% -> 7.6%).

**协同进化**
skill-tool + skill-skill 生态. Primary = skill-tool co-evolution via atomic bundles jointly editing skills and tools.
Secondary = skill-skill ecological dynamics (Lotka-Volterra interaction matrix modeling pairwise
complementarity/conflict under shared context capacity). Anti-pattern memory co-evolves as a third asset. Not
generator-verifier adversarial (that is the CoEvoSkills baseline).

#### 自进化机制_How

**进化方法范式 (How)**
co_evolutionary + population_evolutionary + rollout_optimization. Non-gradient, text-space optimization over a discrete
structured external policy space: reflection-driven bundle proposals (GEPA-style reflective textual evolution),
population maintained on instance-level Pareto front with mutation + synergy-aware merge/crossover operators; ecological
utility dynamics guide search. No gradient/SFT/RL on weights.

**学习信号来源**
成败轨迹 + 自我反思 + 留出验证分 + 工具成功率指标. Black-box task score P(x) on training minibatches; normalized residuals z(x)=P(x)-b(x)
remove task-difficulty confound; structured feedback mu_f (compiler errors, missing-doc reports, constraint violations);
held-out validation gating; tool error rate tracked.

**奖励粒度**
hybrid(混合). Outcome signal = task score P(x); process signal = feedback function mu_f extracting compiler errors /
missing-document reports / constraint violations; synergy signal = co-activation residuals beta_ij.

**学习范式**
offline + sleep-time. Iterative offline evolution over training set D_train with execution budget B, evaluated on
held-out D_val; evolution rounds run between deployment (inter-test-time / sleep-time replay of failures), not
intra-task online weight updates.

#### 进化时机_When

**进化时机 (When)**
inter-test-time + sleep-time. Evolution proceeds in discrete iterations: each iteration samples a candidate from the
Pareto front, executes a minibatch, collects failures, and applies a validated bundle update. Not intra-test-time online
during a single task.

**触发方式**
失败触发 + 工具退化触发. Each iteration builds failure set F={x in M: P(x)<theta} from the minibatch; reflection is triggered by
failures and prioritized by declining utility trends Delta_u and negative interaction beta_ij (conflict/suppression).
Tool-layer bottlenecks (tool errors/outdated tools) activate Tool-Smith.

#### 存储与检索

**技能库结构**
DAG 血脉 / Pareto 前沿. Instance-level Pareto front G of non-dominated system states Sigma; lineages tracked via common
ancestors for synergy-aware merge/crossover; retired skills archived as epitaphs in anti-pattern memory. Effectively a
versioned DAG lineage + Pareto archive.

**检索/复用方式**
语义相似度 + description匹配触发加载 + utility/interaction重排. Retrieval score(s_i,q,S_act) = alpha*sim(s_i,q) + gamma*u_i +
delta*Sum_j beta_ij - eta*cost(s_i), combining semantic relevance, dynamic ecological utility, pairwise interaction
compatibility with already-activated skills, and execution cost.

#### 验证与反馈

**验证方式**
执行验证(execution-based) + 留出评估 + validation gating(门控) + 功能正确性检查. Progressive validation pipeline: tool unit testing (when
bundle has tool ops) -> end-to-end integration testing -> regression checking (for merged candidates, conditioned on
task families where parents showed strength). Held-out D_val performance is the optimization objective.

**错误纠正**
自我修订 + 回滚 + 有界编辑 + 定向 diff 修补. Reflection revises failed configs via bounded typed edits; invalid candidates rejected by
validation gate (rollback); anti-pattern veto prevents repeating known-bad directions; damaged tools reconstructed via
lifecycle ops after perturbation; retired skills' info transferred to epitaphs.

#### 环境与基座

**测试环境**
tool-call + 通用 + 真实生产力任务. OfficeQA (cross-document table localization + multi-step numerical reasoning on structured
docs), SealQA (open-web QA with noisy/conflicting search results), WildClawBench (real-world multi-modal agent
deployment, 15-50 step tasks, multiple tools, high interaction density).

**底座模型**
开源LLM(Qwen3.5). Evaluated across five scales: 9B, 27B, 35B, 122B, 397B. Proposer R and Tool-Smith B_tau are LLM-driven;
model weights are optimizer/target-independent (non-parametric external state is what evolves).

**部署域 (Where)**
general(通用). Spans document QA, web search QA, and multi-modal real-world agent productivity tasks; not specialized to a single vertical.

#### 评估指标

**评估指标**
success_rate / generalization(跨模型/跨任务复杂度 scaling) / skill_library_growth / cost / 回归率. Reports accuracy, gain-vs-base by
model scale, multi-skill co-activation vs gain, regression rate, tool error rate, final library size, long-run library
size, computational cost decomposition (Appendix F).

**关键结论**
OfficeQA @397B: 80.1% (+18.3% vs Base); SealQA @397B: 49.5% (+18.9%); gains grow monotonically with scale (OfficeQA
+2.8%@9B -> +18.3%@397B). WildClawBench: SkillSmith sustains improvement through Day 6 while SkillClaw plateaus Day 2-4
(tool-layer bottleneck); largest advantage on tool-intensive categories. Ablation (122B): locking tool layer
(Skill-only) = largest drop (-6.8% WCB); FreeTool => 14.7% tool error (4.6x); -Eco => library bloat 21+7 (and >80 over
100 rounds) with accuracy 68%-><35%; -Anti => regression 2.1%->7.6% (tripled) and 40-60% oscillation. Resilience: after
perturbations SkillSmith recovers to ~70% by round 100 vs EvoSkill stuck ~30%; keeps library under 28 components.
Scaling: gains rise from ~5-10% on simple tasks to >20% on highly complex tasks.

#### 局限与挑战

**局限与挑战**
doc_bloat(文档膨胀) without ecological governance (library >80 components, accuracy collapse); regression_risk without
anti-pattern memory; optimizer_quality depends on reflection/proposer LLM quality; typed tool primitives constrain
expressiveness (vs FreeTool tradeoff); transferability evaluated only within Qwen3.5 family (cross-harness/cross-vendor
untested); computational cost of bundle validation under budget B. Paper Section 5 self-stated limitations [uncertain -
full text not captured].

#### 可借鉴要点

**可借鉴要点**
(1) Atomic skill+tool bundle edits: when a SKILL.md self-evolves, allow the same atomic transaction to also
wrap/edit/compose/split/retire tools it depends on - this fixes root causes (outdated/brittle tools) instead of
overcompensating with bloated skill text, and avoids invalid intermediate states. Largest single ablation drop comes
from locking the tool layer. (2) Ecological library governance: estimate a skill-skill interaction matrix
(complementarity vs conflict) and a global capacity from execution logs (Lotka-Volterra), then prioritize
mutation/retirement/dedup by dynamic utility - this is what prevents SKILL.md library bloat and keeps retrieval clean.
(3) Anti-pattern memory with veto: persist failure signatures + causal attributions + remedies, retrieve them during
reflection to accelerate diagnosis, and hard-veto proposed edits that repeat known mistakes - this cuts regression rate
~3x and stabilizes long-run evolution.

#### 不确定字段

- code_link
- doc_form (token length)
- cross_transfer (cross-harness / cross-task / cross-user axes)
- safety_guardrails (pre-edit backup/rollback, human-in-the-loop)
- limitations (paper Section 5 self-stated)

---

### CoEvoSkills (EvoSkills)

> `academic_doc_skill` · 2026。Generator-Verifier 协同进化验证框架，让 agent 自主构建复杂多文件 skill 包， 无需 ground truth。Skill Generator 迭代精炼 skill；信息隔离的 Surrogate Verifier 独立进化测试断言，提供密集可执行反馈，规避自我验证的确认偏差。SkillsBench 上 Claude Code/Codex 双 SOTA，跨 

#### 基础信息

**名称**
CoEvoSkills (also referred to as EvoSkills in the paper body and on evoskills.net; arXiv title and GitHub repo use CoEvoSkills)

**提出机构**
University of Illinois Chicago (lead); MBZUAI; McGill University; Columbia University; Zhejiang University; University
of British Columbia. Authors: Hanrong Zhang, Shicheng Fan, Henry Peng Zou, Yankai Chen, Zhenting Wang, Jiayu Zhou,
Chengze Li, Wei-Chieh Huang, Yifei Yao, Kening Zheng, Xue (Steve) Liu, Xiaoxiao Li, Philip S. Yu.

**发布时间**
2026-04-02 (arXiv v1); 2026-04-12 (v2)

**论文链接**
https://arxiv.org/abs/2604.01687

**代码链接**
https://github.com/Zhang-Henry/CoEvoSkills (MIT license; project page https://evoskills.net; repo marked 'Code coming soon' at time of viewing)

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Tools技能 (skills). The evolving object is a structured multi-file skill bundle S = (code + SKILL.md + scripts/assets);
model weights are NOT touched. A second co-evolving object is the Surrogate Verifier test suite V. Target/deployment
agent weights also unchanged - only external skill artifacts evolve.

**技能是否独立制品**
是. A skill is an independent reusable artifact: a structured bundle of interdependent multi-file artifacts (Anthropic
Agent Skills concept). Form = multi-file skill package comprising SKILL.md (instructions) + executable code/scripts +
reference assets, distinct from a single self-contained tool function.

**是否文档载体**
混合. Core carrier includes a readable instruction document (SKILL.md) but the package also bundles executable
code/scripts and assets; instruction-centric + embedded executable code => mixed (instruction document + code).

#### 技能表示

**技能编码方式**
多文件技能包 following Anthropic Agent Skills format: SKILL.md instruction document + executable code/scripts + reference
assets, emitted as a bundle S. The Surrogate Verifier encodes its tests as a synthesized test suite V
(assertions/scripts) per task+environment.

**技能粒度**
完整技能包. A skill packages a complete reusable capability for a class of multi-step professional tasks (instructions +
scripts + assets), larger than an atomic action or single tool function.

#### SKILL.md_专属维度

**编辑粒度**
全新生成 / 整文档重写. Each revision S(i+1) is produced by the generator LLM (Eq.7) reading the current skill S(i) together with
accumulated verifier feedback appended to context C (C(i+1)=C(i)⊕F(i,j)) - i.e. iterative wholesale regeneration of the
multi-file bundle by LLM sampling, not minimal diff/PATCH/bounded add-delete-replace. Context growth bounded by context
cap β=0.7.

**版本与门控**
留出验证门控(held-out) + best-snapshot save. A held-out Ground-Truth Oracle re-executes the skill in a fresh environment and
returns only an opaque pass/fail signal; best snapshot S* is saved whenever reward improves (S*←S(i) if R(i)>R_best).
Single skill line, iterative refinement (not Pareto-front / DAG lineage). Oracle-pass triggers deployment; oracle-fail
triggers a new co-evolution iteration.

**文档来源**
LLM一次性生成 + 失败轨迹蒸馏. Initial skill S(0) sampled from the generator given instruction I + a domain-agnostic meta-skill
S_meta (skill-creator) that teaches how to create skills; subsequent versions refined from accumulated Surrogate
Verifier failure diagnostics F(i,j) (failed test cases + root-cause analysis + actionable revision suggestions). Not
human-initialized, not success-trajectory replay.

**协同进化**
generator-verifier 协同. Core design = Skill Generator + Surrogate Verifier co-evolution via iterative
generate-verify-refine cycles: the generator refines the skill S to maximize surrogate reward R~ under fixed test suite
V; the verifier escalates its tests V when surrogate passes but the oracle fails. Strictly generator-verifier
co-evolution (NOT skill-tool, NOT skill-skill ecosystem, NOT skill-prompt).

#### 自进化机制_How

**进化方法范式 (How)**
co_evolutionary + rollout_optimization(非梯度, 文本空间优化). Non-gradient, text-space optimization via iterative LLM sampling:
Skill refinement S(i+1)~πθ(·|S(i),C(i+1)); Test escalation V(j+1)~πθV(·|I,x(i),V(j)). No SFT, no RL on weights - pure
co-evolutionary search over external skill artifacts.

**学习信号来源**
留出验证分(ground-truth oracle opaque pass/fail) + LLM-as-judge(surrogate verifier synthesizes its own tests). The surrogate
verifier reward R~(x,V) serves as a dense proxy for the opaque ground-truth reward R; per-assertion failure diagnostics
from the verifier supplement the binary oracle signal.

**奖励粒度**
hybrid(混合). Outcome = ground-truth oracle binary pass/fail; process = per-assertion structured failure diagnostics
(failed test cases, root-cause analysis, actionable revision suggestions) from the Surrogate Verifier.

#### 进化时机_When

**进化时机 (When)**
inter-test-time / sleep-time. Offline co-evolution executed per task prior to deployment to the target agent (Claude
Code / Codex); not intra-test-time online during a single task execution. Each task converges in ~4.1 verification
cycles / ~2.4 oracle rounds on average.

**触发方式**
失败触发. Surrogate test failures trigger skill refinement (maximize R~); the gap between surrogate pass and oracle fail
(indicator 1[R~(x,V)=1 ∧ R(x^)<1]) triggers test escalation so the verifier independently strengthens its tests.
Evolution runs up to N=5 oracle rounds and terminates early when the oracle passes.

#### 验证与反馈

**验证方式**
surrogate verifier(无gt) + 留出评估(held-out ground-truth oracle) + 执行验证(execution-based) + validation gating(门控). Surrogate
Verifier synthesizes test cases/scripts per task+environment and provides dense per-assertion failure diagnostics
WITHOUT ground-truth access; held-out Ground-Truth Oracle re-executes in a fresh environment and returns only opaque
pass/fail; oracle pass gates deployment.

**错误纠正**
自我修订 + 重规划. The Skill Generator revises the whole skill bundle each round from accumulated failure diagnostics F(i,j)
appended to context; test escalation forces the verifier to independently strengthen tests when surrogate and oracle
disagree. No explicit bounded-diff / rollback beyond best-snapshot save of S*.

#### 环境与基座

**测试环境**
SkillsBench. SkillsBench (Li et al., 2026b): 87 tasks across 11 domains with deterministic verifiers; the first
systematic benchmark for evaluating agent skills. Deployment harnesses: Claude Code and Codex.

**底座模型**
Claude (Opus 4.6 evolution agent; Sonnet 4.5, Haiku 4.5 transfer) + GPT-5.2 (evolution agent + transfer) + 开源LLM
(Qwen3-Coder-480B, DeepSeek V3-671B, Mistral Large 3-675B for transfer). Optimizer/target separated: evolution
(generator+verifier) driven by a frontier LLM (Claude Opus 4.6 or GPT-5.2); evolved skills then deployed to and
transferred across multiple target models.

**部署域 (Where)**
general(通用). SkillsBench spans 11 domains (incl. Natural Science, etc.); targets general multi-step
professional/coding-style agent tasks rather than a single vertical.

#### 评估指标

**评估指标**
success_rate (SkillsBench pass rate) / generalization (cross-model transfer to 6 LLMs / 5 companies; cross-harness
Claude Code vs Codex) / cost (verification cycles, oracle rounds, evolution-iteration count). Also reports evolution
trajectory (pass rate vs round) and per-domain breakdown across 11 domains.

**关键结论**
On SkillsBench (Claude Opus 4.6 + Claude Code): 71.1% pass rate, +40.5pp over no-skill baseline (30.6%), +17.6pp over
human-curated skills (53.5%), highest among 5 baselines on both Claude Code and Codex. Skill-Creator baseline only
34.1%; CoT-guided single-pass variant 30.7%. Evolution trajectory: surpasses human-curated skills by round 3, ~75% by
round 5. Ablation: removing the Surrogate Verifier drops 71.1% -> 41.1%; background-context-only 48.6%; no-verification
~30.7%. Cross-model transfer: +36 to +44pp across 6 models (e.g. GPT-5.2 +40.2pp to 65.0% with transferred skills, 69.8%
self-evolved; Mistral Large 3 4.9% -> 43.1%). Cost: avg 4.1 verification cycles and 2.4 oracle rounds per task;
surrogate verifier absorbs ~60% of iterations (only 2.4/4.1 escalate to oracle). Case study: qualitative method shift
BLS -> TLS with two-stage search reaching 100% on exoplanet transit task.

#### 局限与挑战

**局限与挑战**
optimizer_quality (relies on a strong frontier LLM as both generator and verifier - Claude Opus 4.6 / GPT-5.2); cost
(ground-truth oracle re-execution in a fresh environment is expensive, though surrogate absorbs ~60% of cycles);
requires a deterministic held-out oracle for final gating (opaque pass/fail still presupposes an oracle exists - may not
be available in fully oracle-free domains); single skill line per task with best-snapshot save (no Pareto archive /
multi-program lineage, so regression protection is limited vs population methods); transferability strong cross-model
but cross-task within a shared library not studied; library-level governance (dedup/retirement/bloat control) not
addressed. Eval-hacking mitigated by information isolation. Paper self-stated limitations (Section 5/Discussion)
[uncertain - full text not captured].

#### 可借鉴要点

**可借鉴要点**
(1) Information-isolated surrogate verifier to dodge confirmation bias: split SKILL.md self-evolution into a generator
and a FULLY isolated verifier session that sees only the task instruction and the produced output files (blind to the
generator's reasoning, code, and current SKILL.md), and let it synthesize its OWN test cases/scripts per
task+environment. The verifier returns dense per-assertion diagnostics (failed cases + root-cause + revision
suggestions) while a held-out oracle returns only an opaque pass/fail bit - this yields actionable feedback without
leaking held-out test content and prevents the verifier from inheriting generator bias. Ablation: removing it collapses
71.1% -> 41.1%. (2) Persistent context + test-escalation loop: keep a persistent conversation context C (capped, e.g.
β=0.7) that accumulates verifier feedback across iterations, and trigger TEST ESCALATION only when the surrogate passes
but the oracle fails - forcing the verifier to independently strengthen its tests without seeing ground truth. This
converges fast (~4.1 cycles, ~2.4 oracle rounds per task) and produces genuine qualitative method switches (BLS -> TLS),
not just parameter tuning. (3) Treat the skill as a co-evolving multi-file bundle (SKILL.md + code + scripts),
regenerated wholesale each round from accumulated feedback, with a single iterative skill line gated by best-snapshot
save (deploy S* only when oracle reward improves). This is simpler than Pareto/lineage archives yet reaches 71.1% and
transfers across 6 models / 5 companies with +36-44pp gains.

#### 不确定字段

- doc_form (typical token length of SKILL.md / skill bundle)
- library_governance (no multi-skill library governance described)
- failure_memory (whether a structured anti-pattern memory exists beyond per-task accumulated context)
- safety_guardrails (pre-edit backup/rollback, human-in-the-loop, key/injection checks)
- learning_paradigm (explicit sleep-time / inter-task replay framing)
- library_structure (cross-task skill library structure)
- retrieval_method (novel retrieval scheme; relies on Anthropic skill loading)
- limitations (paper Section 5 / Discussion self-stated limitations)

---

### EvoSkill

> `academic_doc_skill` · Sentient Labs + Virginia Tech, 2026。将 GEPA 的单文件提示优化扩展为「技能(.md)+系统 提示词」联合变异，每次迭代生成新 agent 程序。五阶段：base agent 跑当前程序→proposer 分析失败轨迹→generator 写新 skill 文件/重写系统提示→evaluator 在留出集打分→Pareto 前沿保留 top-N 为 git 分

#### 基础信息

**名称**
EvoSkill: Automated Skill Discovery for Multi-Agent Systems (Coding Agents)

**提出机构**
Sentient Labs (sentient-agi). Authors: Salaheddin Alzubi, Noah Provenzano, Jaydon Bingham, Weiyuan Chen, Tu Vu (Tu Vu affiliated with Virginia Tech).

**发布时间**
2026-03-03 (arXiv v1 submitted 3 Mar 2026); open-source code repo actively maintained.

**论文链接**
https://arxiv.org/abs/2603.02766

**代码链接**
https://github.com/sentient-agi/EvoSkill

**类型**
academic (arXiv paper) + industry/open-source framework (Apache-2.0 toolkit, evoskill CLI).

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能. Whole-agent program = system prompt + skill set (.claude/skills/*/SKILL.md + helper scripts)
materialized on disk; model weights are FROZEN. Each iteration yields an entirely new agent program (skill_only and/or
prompt_only mutation modes). Architecture (single agent) and weights are NOT evolved.

**技能是否独立制品**
是. Each skill is an independent reusable artifact packaged as a folder: .claude/skills/{name}/SKILL.md (instruction
markdown) + metadata + helper scripts. A program also carries .claude/program.yaml (system prompt + allowed tools +
output format + score). Skills are explicitly designed to be portable across coding-agent harnesses (agentskills.io
registry).

**是否文档载体**
混合 (instruction-document-centric). Core carrier is a readable SKILL.md markdown instruction file, but a skill folder
additionally bundles helper scripts/code; the Skill Generator reads a 'skill-creator' skill to enforce the canonical
format. So instruction-markdown as primary carrier + embedded/executable helper code => mixed, leaning toward 是.

#### 技能表示

**技能编码方式**
技能文档(.md / SKILL.md) + 多文件技能包. Each skill = SKILL.md markdown instructions inside a skill folder (with metadata + helper
scripts); the program itself is encoded as program.yaml (structured YAML: name, parent, generation, system_prompt,
allowed_tools, output_format, metadata/score).

**技能粒度**
完整技能包 / 子任务workflow / 策略规则. Each discovered skill packages a coherent reusable capability (e.g., percentage-calculator,
financial-table reader) — a complete skill package targeting a class of failure-driven capability gaps, smaller than a
full agent and larger than an atomic action.

#### SKILL.md_专属维度

**编辑粒度**
全新生成 (create new skill folder+SKILL.md via action='create') + edit existing skill (action='edit' on a target_skill) +
整系统提示重写 (prompt_only mode rewrites base_agent/prompt.txt wholesale each iteration). SkillProposerResponse chooses create
vs edit; the Generator materializes the whole file, not minimal-diff/PATCH; each iteration is one mutation. No bounded
add/delete/replace diff primitives at the doc level.

**版本与门控**
留出验证门控(held-out) + git分支前沿选择 + DAG血脉. Each new program is scored on a held-out validation set the Proposer NEVER sees;
it is admitted to a top-N 'frontier' (frontier_size default 3) only if it beats the worst frontier member by held-out
score (ProgramManager.update_frontier: single-objective score-ranked pruning). Frontier members are tagged frontier/*;
every program is a git branch program/{name} with a parent pointer forming a DAG lineage (get_lineage/get_children). The
paper frames this as a 'Pareto frontier of agent programs'; in code the frontier is a single-objective (held-out
accuracy) top-N archive, not a true multi-objective Pareto front. Selection strategies: best / random / round_robin.

**文档来源**
失败轨迹蒸馏 (failure-trace-driven induction). Skills are induced from agent failure cases: the Base agent runs the current
program on the TRAINING split; the Skill Proposer analyzes the failure traces (why they failed) and proposes a skill;
the Skill Generator writes the SKILL.md. Blog subtitle: 'Automated Skill Induction from Agent Failures'.

**跨载体迁移**
跨模型 + 跨agent harness + 跨任务 + 跨基准. Cross-harness: Claude Code, OpenCode, Codex CLI, OpenHands, Goose, Harbor all
supported (harness abstraction layer; skill folders port across them). Cross-model: skills evolved with one frozen LLM
transfer to others (demonstrated in follow-up EvoSkills paper arXiv:2604.01687; supports
Claude/GPT/GLM/Minimax/Kimi/Gemini/Qwen via OpenRouter/Anthropic/OpenAI/Fireworks). Cross-task/cross-benchmark: skills
evolved on SealQA transfer zero-shot to BrowseComp (+5.3%). All four transfer axes covered.

**技能库治理**
frontier pruning (retirement of worst) + existing-skill-aware proposals. Frontier update_frontier evicts the
lowest-scoring program when full => implicit retirement/pruning. The Skill Proposer is required to list/check existing
skills before proposing and to reference DISCARDED iterations (related_iterations lineage) to avoid repeats; the
skill-creator skill enforces a canonical concise format. No explicit dedup/merge, similarity-retrieval-edit-targeting,
curator loop, or Lotka-Volterra dynamics.

**失败记忆**
是. (1) .claude/feedback_history.md records what the Proposer tried each iteration and WHY it succeeded/failed. (2)
SkillProposerResponse.related_iterations references past discarded attempts so the Proposer learns from prior failures
and avoids repeating them. (3) feedback_descent.py accumulates failure rationales and, crucially, RESETS the feedback
history when a candidate wins (stale failures are forgotten because the baseline moved). Used as negative feedback to
redirect the search and veto repeated bad directions.

**协同进化**
skill-prompt 联合 + generator-verifier 协同. Primary = joint mutation space over skills (.md) AND system prompt (skill_only
vs prompt_only modes; the paper abstract frames 'whole agent = system prompt + skill set' and 'joint mutation of skills
+ system prompt'). Secondary = a generator-verifier-style pipeline: Skill/Prompt Proposer (analyst) -> Skill/Prompt
Generator (writer) -> Evaluator (held-out verifier). Not skill-tool co-evolution (tools are fixed allowed-tools lists,
not evolved) and not an explicit skill-skill ecological model.

#### 自进化机制_How

**进化方法范式 (How)**
population_evolutionary + rollout_optimization(非梯度, 文本空间) + reward-based. Extends GEPA's feedback-driven textual
evolution from single-file prompt optimization to whole-program (skill+prompt) evolution: a population (frontier) of
agent programs is maintained; each iteration an LLM Proposer proposes a text-space mutation from failure traces, an LLM
Generator materializes new SKILL.md/prompt files, and a held-out Evaluator scores the new program; top-N frontier
selection keeps survivors. No gradient/SFT/RL on weights (weights frozen, pure prompt/skill text-space optimization).

**学习信号来源**
成败轨迹 + 留出验证分 + LLM-as-judge + 执行验证. Failure traces on the training split drive the Proposer; held-out validation
accuracy gates frontier admission (scalar reward). Scorer types selectable: multi_tolerance/exact (string), llm
(LLM-as-judge, e.g. SealQA uses GPT-5-mini grading), script, harbor (built-in verifier), and code-execution pass@1
(LiveCodeBench runs code in Docker).

**奖励粒度**
outcome(结果) with partial-credit tolerance. Per-question outcome scoring (multi-tolerance weighted average over
0/1/2.5/5/10% tolerances; or LLM A/B/C grade => 1.0/0.0; or pass@1), aggregated as mean accuracy over the held-out set.
No process/step-level reward.

**学习范式**
offline + on-policy + benchmark-driven. Offline evolution over a benchmark dataset split into train/val (not online
during live task execution); on-policy in that each candidate program is scored by actually running the frozen agent
fresh. 'Continuous evolution' (improving from regular usage) and 'evolution without a benchmark' are explicitly listed
as open/🛠️, not yet implemented.

#### 进化时机_When

**进化时机 (When)**
inter-test-time(任务间离线). The self-improvement loop runs offline as a batch process between benchmark evaluation runs (not
intra-test-time during a single task). Can be offloaded to Docker/remote/Daytona sandboxes since runs take hours;
effectively sleep-time-capable when scheduled, but default semantics are inter-test-time.

**触发方式**
失败触发 + 周期性(epoch/iteration loop). Each iteration runs the agent on the training split, collects failures (score<0.8),
and triggers a Proposer->Generator cycle; loop repeats up to max_iterations (default 20) with early stop after
no_improvement_limit (default 5) consecutive non-improvements. Trigger is failure-driven within a fixed iteration
budget, not usage-driven.

#### 存储与检索

**技能库结构**
git 分支 + 技能文件目录 + DAG血脉 + (云端注册中心). Programs = git branches program/{name} (program/base, program/iter-skill-*);
frontier members marked with frontier/* tags; parent pointers in program.yaml form a DAG lineage
(get_lineage/get_children); skills live as folders under .claude/skills/{name}/; portable skill folders also published
to a cloud registry (agentskills.io).

**检索/复用方式**
description 匹配触发加载 (native agent skill discovery). Skills are loaded at agent run-time by each harness's native
skill-discovery mechanism (Claude setting_sources=['user','project'] loads .claude/skills/; Goose summon extension;
Codex .agents/skills/ symlink; OpenCode project config). The Skill Proposer explicitly lists/reads existing skills to
decide create-vs-edit (retrieval by listing/description, not vector similarity). No embedding/BM25 retrieval.

#### 验证与反馈

**验证方式**
执行验证(execution-based) + 留出评估 + validation gating(门控) + LLM-judge + 功能正确性检查. New programs are scored on a held-out
validation set (gating admission to the frontier). Scoring is execution-based per harness: multi-tolerance/exact string
match, LLM-as-judge (SealQA), shell-script scorer, Harbor built-in verifier, and functional correctness via Docker code
execution (LiveCodeBench pass@1).

**错误纠正**
自我修订 + 回滚 + 有界编辑 + 重规划. Non-improving candidates are discarded (git branch delete = rollback); the next iteration's
Proposer re-analyzes failures and re-plans a different skill/prompt mutation informed by feedback_history.md and
related_iterations; bounded edits are create-new or edit-existing SKILL.md (no destructive wholesale rewrites of the
whole library). feedback_descent forgets stale failures once a new best is found.

#### 环境与基座

**测试环境**
通用 (QA + coding + tool-call). OfficeQA (grounded reasoning over U.S. Treasury data), SealQA (search-augmented QA with
noisy retrieval), BrowseComp (browse, zero-shot transfer target), DabStep, LiveCodeBench (coding, Docker code
execution), SWE-bench-verified (Harbor containerized benchmark).

**底座模型**
Claude / GPT / 开源LLM (multi-model). Any model provider (Anthropic, OpenAI, OpenRouter, Fireworks) and any model (Claude,
GPT-5/o3, GLM, Minimax, Kimi, Gemini, Qwen). Optimizer agents (Proposer/Generator/Evaluator) and the target agent are
LLM-driven and can be different LLMs; weights frozen throughout. Default target e.g. claude-sonnet-4-6 / gpt-5.

**部署域 (Where)**
general(通用) -> specialized. Turns general-purpose coding agents into specialists; tested across office/finance grounded
reasoning, search-augmented QA, browse, and coding domains. Deployment artifact = copy .claude/program.yaml +
.claude/skills/ into the user's agent project.

#### 评估指标

**评估指标**
success_rate(accuracy) + generalization(跨任务/跨模型/跨harness zero-shot transfer) + cost(total_cost_usd, duration_ms, token
usage tracked per run) + skill_library_growth(# skills discovered, frontier size) + sample_efficiency(iterations to
converge). Live progress table prints Iter / Accuracy / Delta / Skills / Frontier / Status.

**关键结论**
OfficeQA: +7.3% exact-match (60.6% -> 67.9%). SealQA: +12.1% (26.6% -> 38.7%). Zero-shot transfer SealQA -> BrowseComp:
+5.3% with no modification (demonstrating skill-level optimization yields transferable capabilities beyond the training
task). Cross-model transfer demonstrated in the EvoSkills follow-up. Frontier = top-N programs kept as git branches.

#### 局限与挑战

**局限与挑战**
scalability (runs take hours; 20-min per-call timeout, 3x exponential-backoff retries; needs Docker/Daytona offload for
long runs) + optimizer_quality (depends heavily on strong Proposer/Generator LLMs; read-only Proposers limited to 8
tools) + regression_risk (validation gating catches regressions but non-improving iterations are wasted; example -1.6%
iteration discarded) + transferability (cross-task works but bounded; cross-harness portability assumed rather than
exhaustively benchmarked) + eval-hacking (mitigated by held-out split but inherent to benchmark-driven loops).
Catastrophic forgetting is N/A (weights frozen). Continuous-evolution and no-benchmark evolution are explicitly open
(🛠️).

#### 可借鉴要点

**可借鉴要点**
(1) Held-out validation gating + frontier/top-N selection + git-branch versioning of WHOLE programs: treat each (system
prompt + skill set) as one atomic 'program' artifact, version it as its own git branch (program/*, frontier/* tags,
parent->child lineage), and admit a mutation ONLY if it beats the held-out set; this gives safe rollback, full
diffability (git diff any two evolved states), and prevents eval-hacking/overfitting via a strict train/val split the
proposer never sees. This single design makes SKILL.md self-evolution auditable and regression-safe. (2)
Failure-trace-driven induction with separated Proposer/Generator/Evaluator roles: drive every edit from concrete agent
failures (run agent on training split -> collect failures -> Proposer diagnoses root cause -> Generator writes a concise
SKILL.md -> held-out Evaluator scores); keep Proposers strictly read-only (no Write/Edit) to enforce analyze-then-act,
and accumulate+forget feedback (reset failure memory when a candidate wins) so the search adapts to the new baseline.
(3) Standardized portable skill folders (.claude/skills/{name}/SKILL.md + metadata + helper scripts) as the
cross-harness/cross-model/cross-task currency: evolve skills on one task/model/harness and reuse them unchanged
elsewhere (SealQA->BrowseComp +5.3% zero-shot), turning 'skill text' into a transferable, non-parametric asset
independent of frozen weights.

#### 不确定字段

- doc_form (exact typical token length of a SKILL.md / program.yaml)
- safety_guardrails (no explicit human-in-the-loop or secret/injection scanning confirmed; inferred as absent)

---

### DRAFT (From Exploration to Mastery)

> `academic_doc_skill` · RUC + Baidu, ICLR 2025 Oral(前1.8%)。迭代精炼工具 docstring(结构化 NL 文档： description/parameters)。三角色循环：Explorer 生成多样尝试→Analyzer(LLM-as-judge) 做信用分配归因到具体文档缺陷→Rewriter 更新 docstring。含探索多样性约束 + 基于 BLEU/ 余弦相似度的工具自适应

#### 基础信息

**名称**
DRAFT (From Exploration to Mastery)

**提出机构**
Gaoling School of Artificial Intelligence, Renmin University of China (RUC) + Baidu Inc. + Institute of Computing
Technology, Chinese Academy of Sciences (corresponding author Jun Xu)

**发布时间**
arXiv v1 10 Oct 2024, v2 26 Feb 2025; ICLR 2025 Oral (top 1.8%)

**论文链接**
https://arxiv.org/abs/2410.08197

**代码链接**
https://github.com/quchangle1/DRAFT

**类型**
academic (ICLR 2025 Oral paper, open-source reference implementation)

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 (context / prompt): the tool documentation (docstring) that is injected into the LLM's prompt context. NOT
model weights, NOT the tool/API itself, NOT agent architecture — only the frozen, externally-supplied text describing
each tool.

**技能是否独立制品**
Yes. The refined tool documentation is an independent, reusable, human-readable text artifact (a structured docstring:
description + parameters). It is produced once per tool and can be plugged into any downstream LLM's prompt context as a
drop-in replacement for the raw doc.

**是否文档载体**
Yes (pure readable natural-language instruction document is the core carrier). The evolved object is a structured NL
docstring (description + parameters + usage notes); all learning is expressed as textual edits to this doc, with no code
and no vector representation.

#### 技能表示

**技能编码方式**
docstring — structured natural language (a 'description' field + a 'parameters' field, plus usage notes). Closest to a
natural-language SOP confined to a single tool; not executable code, not API schema, not vector embedding.

**技能粒度**
完整技能包 at single-tool granularity: a complete docstring covering one tool's purpose, parameters, and usage. Coarser than
an atomic action, finer than a multi-tool workflow.

#### SKILL.md_专属维度

**编辑粒度**
Whole-document rewrite per iteration: the Rewriter emits a complete new version t_i of the tool documentation each round
(conditioned on the prior version, the exploration instance, the tool feedback, the Analyzer's NL suggestions, and the
full revision history T_i). Not bounded add/delete/replace, not minimal diff, not PATCH. Iterations are bounded only by
the tool-adaptive termination.

**版本与门控**
No quality-based version gate (no held-out validation, no Pareto front, no git branch, no human review, no
backup/rollback). Only a tool-adaptive CONVERGENCE-based termination: stop when two consecutive doc versions are
sufficiently similar, measured by Δ = (cosine(embedding) + BLEU) / 2 > τ = 0.75 (embeddings from OpenAI
text-embedding-ada-002). This is an early-stop, not an accept/reject gate.

**文档来源**
Human-crafted / dataset initialization (the raw tool documentation t_0 from RestBench / ToolBench) + failure-and-success
trajectory distillation via self-driven trial-and-error exploration (the Explorer actually invokes the tool and the
Analyzer attributes outcomes to doc defects). Fuses human-initialized docs with execution-feedback distillation.

**跨载体迁移**
Cross-model (explicitly the paper's headline finding): docs refined with GPT-4o as backbone transfer to GPT-4o-mini and
Llama-3-70B; docs refined with Llama-3-70B also generalize to the other models. Not cross-agent-harness, not cross-tool
(docs are tool-specific), not cross-user/team. Rationale given: decoder-only LLMs share transformer structure and
pre-training corpora, so they converge on similar comprehension needs.

**技能库治理**
None at the library level. Each tool's documentation is refined independently; there is no global skill library, no
dedup, no retirement/archival, no Lotka-Volterra, no hierarchical index. Cosine similarity over embeddings is used ONLY
for exploration-diversity control (φ = 0.9 within a single tool's iterations), not for library-level
retrieval/edit-target selection.

**失败记忆**
Partial. The Analyzer acts as LLM-as-judge performing CREDIT ASSIGNMENT — it attributes a failed trial to specific
documentation defects (missing constraint, ambiguous parameter, etc.) and emits NATURAL-LANGUAGE (not scalar)
suggestions s_i. The Rewriter additionally consumes the full revision history T_i to avoid redundant/repetitive edits.
However, there is no explicit anti-pattern store, no failure-signature registry, and no rejected-edit buffer retained as
durable negative feedback across tools.

**编辑安全**
Limited. The only guardrail is the tool-adaptive termination (BLEU+cosine > τ=0.75) which bounds iterations and prevents
overfitting / doc-bloat. There is no enforced scope boundary (the framework only edits docs by construction but does not
hard-guard source code), no pre-edit backup or rollback, no eval-hacking defense, no human-in-the-loop confirmation, and
no secret/injection check. The process is explicitly fully automated.

**协同进化**
skill-only: only the tool documentation evolves; the underlying tool/API is fixed and not modified. Internally there is
a three-role division of labour (Explorer = generator, Analyzer = LLM-as-judge verifier, Rewriter = editor) cooperating
on a single artifact, but there is no co-evolution of separate artifacts (no skill-tool coevolution, no
generator-verifier coevolution of two evolving systems, no skill-skill ecosystem).

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (non-gradient, text-space optimization via trial-and-error) fused with reward-based learning using
INTERNAL TEXTUAL feedback (the Analyzer is an LLM-as-judge that returns natural-language credit assignment rather than a
scalar reward). Realized as a three-phase iterative loop: experience gathering -> learning from experience ->
documentation rewriting. No gradient (SFT/RL) updates.

**学习信号来源**
LLM-as-judge (the Analyzer's NL critique) + tool execution outcomes (real tool-call return values / errors from the
Explorer) + self-reflection (the Explorer's diversity-driven self-reflection when the similarity constraint is
violated). No environmental scalar reward, no held-out validation score.

**奖励粒度**
hybrid: process-level feedback (per-iteration NL credit assignment from the Analyzer diagnosing which doc defect caused
which failure) combined with outcome-level signal (the tool's actual execution result / error per exploration instance).

**学习范式**
Offline + on-policy. All refinement happens offline as a preprocessing step BEFORE the doc is deployed to downstream
tasks; the Explorer generates fresh exploration instances on-policy with respect to the current documentation version
t_{i-1}. Not sleep-time (no nightly cron / idle replay of past sessions).

#### 进化时机_When

**进化时机 (When)**
inter-test-time: the documentation is refined offline, between deployments, as a one-shot preprocessing pass per tool.
Nothing is learned intra-test-time during downstream task execution.

**触发方式**
On-demand / task-driven: DRAFT is run explicitly as a preprocessing step per tool (max I = 5 iterations). Per-tool
termination is triggered automatically when the consecutive-version similarity Δ exceeds τ = 0.75. No
event/cron/curriculum trigger; no continuous usage-driven loop.

#### 存储与检索

**技能库结构**
Flat: a per-tool documentation set D refined in isolation; no hierarchy, no vector DB (embeddings are computed on the
fly only for similarity checks), no graph, no DAG lineage, no cloud registry. The output is simply a revised
documentation set D~.

**检索/复用方式**
Deployment: standard direct injection — the refined docstring is loaded into the LLM's prompt context by
description/name match (conventional tool-doc provisioning, same as ReAct/DFSDT/EasyTool baselines). Refinement-time:
cosine similarity over OpenAI text-embedding-ada-002 embeddings is used to enforce exploration diversity, NOT to
retrieve edit targets. No BM25, no LLM re-rank.

#### 验证与反馈

**验证方式**
LLM-as-judge (the Analyzer) + execution-based signal (real tool invocations by the Explorer). No held-out validation
gate, no surrogate verifier, no functional-correctness unit test, no multi-model debate. Downstream evaluation (CP%,
Win%) is held out from the refinement loop — i.e., the refinement loop does NOT see the eval set, so there is no
held-out gating during refinement.

**错误纠正**
Self-revision via iterative whole-document rewriting (each round the Rewriter produces a new t_i guided by the
Analyzer's NL suggestions and the revision history T_i) + bounded iterations via the tool-adaptive termination. No
rollback, no directed diff patch, no re-planning at the trajectory level.

#### 环境与基座

**测试环境**
tool-call benchmarks: RestBench (TMDB — 54 movie APIs; Spotify — 40 music APIs) and ToolBench (the hardest
I3-Instruction subset requiring multiple tools from different categories).

**底座模型**
GPT-4o is the backbone/optimizer used by DRAFT to refine the docs (the model that both explores and rewrites).
Deployment/inference targets: GPT-4o, GPT-4o-mini, Llama-3-70B. Optimizer and target can be the same model or different
(cross-model). Embeddings via OpenAI text-embedding-ada-002.

**部署域 (Where)**
general — general-purpose tool-use / tool-call domain (API invocation across heterogeneous real-world categories: movies, music, web APIs).

#### 评估指标

**评估指标**
success_rate via Correct Path Rate (CP% — ground-truth tool path is a subsequence of predicted calls) and Win Rate (Win%
— pairwise ChatGPT-evaluator preference vs ReAct); generalization measured by cross-model transfer of the refined docs;
ablation measured contribution of diversity-promoting exploration and tool-adaptive termination.

**关键结论**
RestBench-TMDB CP% (GPT-4o): ReAct 71.00 -> DRAFT 88.00; Llama-3-70B 72 -> 86; GPT-4o-mini 48 -> 62. RestBench-Spotify
CP% (GPT-4o): 28.07 -> 70.17. ToolBench CP% (GPT-4o): 37 -> 51; Llama-3-70B 41 -> 53; GPT-4o-mini 35 -> 47. Headline:
GPT-4o-mini + DRAFT (CP 47) beats the GPT-4o baseline without DRAFT (CP 37) on ToolBench. Robust cross-model
generalization: docs refined by GPT-4o transfer to GPT-4o-mini and Llama-3-70B; docs refined by Llama-3-70B also
generalize; GPT-4o as optimizer yields the best results (method benefits from stronger backbone). Ablation on TMDB
(GPT-4o): full DRAFT CP 88 -> 84 w/o diversity-promoting exploration -> 80 w/o tool-adaptive termination, confirming
both mechanisms contribute. Accepted as ICLR 2025 Oral (top 1.8%).

#### 局限与挑战

**局限与挑战**
doc_bloat / overfitting if too many iterations (redundant info accumulates — only mitigated, not eliminated, by the
similarity-based termination); optimizer_quality (a stronger backbone GPT-4o yields markedly better docs than
Llama-3-70B); regression_risk (no held-out validation gate, so termination is similarity-based not performance-based and
could stop at a locally-similar but suboptimal doc); scalability to very large / rapidly-evolving tool ecosystems is not
demonstrated; evaluation limited to three tool-call benchmarks (no multi-modal, no agentic multi-turn planning beyond
tool selection); no explicit safety/eval-hacking guardrails; refined docs are tool-specific so do not transfer across
tools.

#### 可借鉴要点

**可借鉴要点**
- Three-role self-driven trial-and-error loop with NATURAL-LANGUAGE (not scalar) credit assignment: Explorer generates diverse real tool-call attempts and captures execution outcomes; Analyzer (LLM-as-judge) performs credit assignment that attributes each failure to a SPECIFIC documentation defect and outputs located NL suggestions; Rewriter integrates suggestions + full revision history to rewrite the doc. The NL credit assignment is the crux — it gives the editor actionable, defect-located feedback instead of a numeric score, directly portable to any SKILL.md self-evolution agent.
- Diversity-promoting exploration via a cosine-similarity constraint on query embeddings (φ = 0.9, OpenAI ada-002) plus self-reflection regeneration, ensuring the doc is stress-tested against a wide behavioral spectrum (edge cases, parameter combinations, error sources) rather than canonical/easy queries. Cheap, model-agnostic, and immediately reusable to guarantee coverage when self-probing any instruction document.
- Tool-adaptive convergence termination via dual similarity (Δ = (BLEU + cosine) / 2 > τ = 0.75) — a lightweight, no-held-out-set per-tool early-stop that both saves compute AND guards against overfitting/doc-bloat. Any iterative document-rewriting agent can adopt this as a minimal, training-free convergence gate when a held-out validation set is unavailable.

#### 不确定字段

- doc_form

---

### SkillWeaver

> `academic_doc_skill` · OSU/UVA/Purdue/CMU/Cisco, 2025。技能 = Python 函数 + 自然语言 docstring(含描述+先前 执行日志+前置条件)。三阶段：技能提议(LLM 自动课程)→合成(成功轨迹蒸馏为 API)→打磨 (自动测试+环境反馈)。运行时 --allow-recovery 用定向 diff 修补 API。docstring 侧即文档 技能进化。arXiv:2504.0

#### 基础信息

**名称**
SkillWeaver

**提出机构**
The Ohio State University (OSU NLP Group); University of Virginia; Purdue University; Carnegie Mellon University; Cisco
Research. Authors: Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu,
Jayanth Srinivasa, Gaowen Liu, Graham Neubig, Yu Su.

**发布时间**
2025-04-09 (arXiv v1)

**论文链接**
https://arxiv.org/abs/2504.07079

**代码链接**
https://github.com/OSU-NLP-Group/SkillWeaver

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Tools技能. The agent evolves a continually growing library of reusable skills materialized as Python APIs (Playwright
browser-automation functions). Model weights are NOT touched; the skill/API library is the sole evolving, transferable,
non-parametric asset that augments the agent's action space.

**技能是否独立制品**
是. Each skill is an independent reusable artifact: a Python function file (knowledge-base entry, e.g. kb_post_code.py)
consisting of a function signature, a natural-language docstring, and a Playwright code body. Lightweight, plug-and-play
APIs that extend the agent's action space; stored as files under a per-website knowledge-base path prefix.

**是否文档载体**
混合. The skill carrier is primarily executable Python code (the API body), but every API carries a rich natural-language
docstring (description + prior execution usage log + website precondition state) that functions as the readable
instruction document and is itself updated across executions. Instruction document (docstring) + embedded executable
code => mixed; the docstring side is the document-form skill-evolution channel.

#### 技能表示

**技能编码方式**
可执行代码 (Python API with Playwright browser automation) + docstring (NL description + usage log + preconditions).
Prompts/templates that drive the pipeline are additionally organized as separate .md files under skillweaver/templates.
Code-centric skill with an NL docstring annotating each API.

**技能粒度**
子任务workflow. Each API encapsulates a reusable sub-task workflow of three proposed types: procedural tasks (multi-action
process automation), navigational tasks (systematic page/section exploration), and information-seeking tasks
(specialized scraping). The library aggregates many sub-task APIs into a complete per-website skill package.

#### SKILL.md_专属维度

**编辑粒度**
全新生成 (whole-function regeneration during synthesis/polishing) + 定向 diff 修补 (targeted diff patching at runtime). Stage II
synthesizes an entirely new Python function from a successful trajectory; Stage III re-debugs/regenerates via env
feedback; runtime --allow-recovery applies targeted diffs to patch APIs that throw exceptions during testing (bounded
edit rather than full rewrite).

**版本与门控**
留出验证门控(held-out) / validation gating. Each candidate API must pass Stage III honing: auto-generated unit tests (direct
execution for no-arg APIs; LLM-generated parameter test cases for parameterized APIs) plus an LLM
reward-model/success-checker judging task completion. --allow-unverified-apis defaults to False, i.e. APIs that have not
executed without runtime error are gated out. Iteration directories (iter_N) provide per-round version snapshots.

**文档来源**
成功轨迹归纳 + 执行录像回放 + LLM一次性生成. Successful practice trajectories (state-action pairs with screenshots) are
distilled/generalized by an LLM into a Python API; the docstring usage log is replayed/updated from execution
recordings. Failure trajectories additionally feed Stage III debugging.

**跨载体迁移**
跨模型 + 跨 agent harness + 跨任务. Cross-agent (model) transfer is a headline result: APIs synthesized by strong agents
(gpt-4o) substantially boost weaker agents, up to +54.3% on WebArena. Cross-harness transfer demonstrated via an
experimental Browser-Use version that converts the knowledge base into a Browser-Use Controller object extending another
agent's action space. Skills also transfer across tasks within a website.

**技能库治理**
Diversification at proposal time by explicitly prompting the LLM to propose novel/reusable skills beyond the current
repertoire (diversity-driven auto-curriculum); three task types (procedural/navigational/info-seeking) broaden coverage.
The library grows iteratively per website. Explicit dedup/merge/retirement mechanisms (Lotka-Volterra, archival, curator
loop) [uncertain - not described in paper/README].

**失败记忆**
是 (implicit, per-API). The docstring usage log records prior executions (per-API success/failure history); Stage III
polishing consumes failure trajectories and reward-model feedback to debug APIs; runtime exceptions trigger
--allow-recovery patches. A dedicated global anti-pattern / failure-signature store with attribution+remedy as pooled
negative-feedback buffer [uncertain - not described]; failure memory is per-API and per-iteration rather than a shared
anti-pattern memory.

**编辑安全**
scope 边界 (only API .py files are synthesized/patched, not agent source code) + 执行验证 (static analysis of generated code
for common mistakes + execution-based unit tests before admission) + validation gating (--allow-unverified-apis=False
default) + 有界编辑 (targeted diff recovery rather than destructive full rewrites at runtime). Pre-edit backup/rollback,
human-in-the-loop, eval-hacking defenses [uncertain - not described].

**协同进化**
skill-tool. The skill IS the tool: synthesized skills become plug-and-play APIs that directly extend the agent's action
space, so skill evolution and tool evolution are the same object. A generator-verifier flavor is present (API-synthesis
LLM vs reward-model/success-checker LLM), but the dominant axis is skill-as-tool self-extension; no separate skill-skill
ecological dynamics.

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration + rollout_optimization (non-gradient, text-space). Successful execution trajectories are
distilled (imitation) into generalized Python APIs by an LLM; iterative exploration rollouts progressively expand the
API library. No gradient/SFT/RL on weights - pure LLM-driven synthesis + environment-validated iteration.

**学习信号来源**
成败轨迹 (successful trajectories distilled; failures debugged) + LLM-as-judge (reward-model/success-checker LLM judges task
completion from trajectory + screenshots + env feedback) + 工具成功率指标 (API runtime-error-free execution as admission
signal).

**奖励粒度**
outcome. The reward model judges task completion after a trajectory (success/failure of the proposed skill task), not per-step process rewards.

**学习范式**
offline + sleep-time. A dedicated exploration phase (skillweaver.explore, e.g. 160 iterations) runs offline/sleep-time
to build the API library; the synthesized library is then deployed online (attempt_task/evaluate_benchmark) without
further weight updates. Inter-test-time evolution between exploration rounds.

#### 进化时机_When

**进化时机 (When)**
inter-test-time + sleep-time. Skill discovery/synthesis/honing happens in a dedicated offline exploration loop
(between/aside from real tasks); runtime task execution only optionally triggers recovery patches (intra-test-time
bounded repair when --allow-recovery is on).

**触发方式**
curriculum(课程)驱动 (LLM auto-curriculum proposes skills each exploration iteration) + 失败触发 (runtime API exceptions trigger
recovery patching; Stage III honing triggered by unit-test failures + negative reward-model judgments).
Iteration-count-driven exploration schedule (--iterations, --explore-schedule).

#### 存储与检索

**技能库结构**
技能文件目录. Per-website knowledge-base directories (e.g. skill_library/reddit/reddit_kb_post,
logs/explore-reddit-gpt4o/iter_N/kb_post); each skill = a _code.py file plus metadata; iteration snapshots version the
library. Flat per-website file directory, not a vector DB or DAG lineage.

**检索/复用方式**
description 匹配触发加载 + 代码直接复用. At task time the agent is given the per-website API set with their docstring
descriptions/preconditions and selects/invokes the matching API by description; the verified Playwright code body is
directly reused (not generation-as-retrieval - the exact verified code is reused). The LLM chooses among APIs based on
docstring descriptions.

#### 验证与反馈

**验证方式**
执行验证(execution-based) + LLM-judge + validation gating(门控) + 功能正确性检查. Stage III: no-arg APIs run as standalone unit
tests; parameterized APIs get LLM-generated parameter test cases; reward-model/success-checker LLM (gpt-4o) judges
completion; static analysis catches common code mistakes; unverified APIs gated out by default.

**错误纠正**
定向 diff 修补 + 自我修订. Runtime --allow-recovery patches APIs that throw exceptions via targeted diffs; Stage III polishing
self-revises APIs using env feedback + reward-model signals + auto unit tests. Bounded edits rather than wholesale
regeneration at runtime.

#### 环境与基座

**测试环境**
Web. WebArena benchmark (shopping, shopping_admin, reddit, gitlab, map) + real-world websites via Online-Mind2Web tasks.

**底座模型**
GPT (gpt-4o / gpt-4o-2024-08-06 default for agent, API synthesis, and success checking). Optimizer/target separated in
cross-agent transfer experiments: strong agent (gpt-4o) synthesizes APIs, weaker agents consume them. Azure-hosted
OpenAI supported.

**部署域 (Where)**
specialized (web/GUI automation domain).

#### 评估指标

**评估指标**
success_rate + generalization (cross-agent/cross-model transfer; real-world Online-Mind2Web) + skill_library_growth
(iterations to build library) + cost (exploration iteration budget).

**关键结论**
WebArena +31.8% relative success-rate improvement; Online-Mind2Web (real-world websites) +39.8%; cross-agent transfer up
to +54.3% on WebArena (strong-agent APIs boost weaker agents); with 160 exploration iterations success rose from 25% to
38%; weaker agents improved 40%-130%. Validates honing diverse website interactions into transferable, shareable APIs.

#### 可借鉴要点

**可借鉴要点**
(1) Skill = executable API + evolving NL docstring: encode each skill as a Python function whose docstring carries
description + prior execution usage log + precondition state, and update that docstring across runs - a single artifact
that is both machine-executable and human/LLM-readable, with the docstring as the document-form evolution channel. (2)
3-stage curriculum-driven loop (LLM auto-curriculum proposal -> distill success trajectories into generalized APIs ->
polish with auto-generated unit tests + env-feedback debug) is a clean, reproducible pipeline for autonomous
skill-document evolution with zero weight updates. (3) Runtime --allow-recovery with targeted diffs to patch failing
skills - bounded, execution-validated edits rather than full rewrites, gated by --allow-unverified-apis=False - is a
safe pattern for in-production skill self-repair.

#### 不确定字段

- library_governance (explicit dedup/merge/retirement mechanisms)
- failure_memory (dedicated global anti-pattern/failure-signature store with attribution+remedy)
- safety_guardrails (pre-edit backup/rollback, human-in-the-loop, eval-hacking defenses)
- doc_form (typical token length)

---

### OpenSpace

> `engineering_practice` · HKUDS, 2026。开源自进化技能引擎。对执行录像做事后分析，产出 FIX/DERIVED/CAPTURED 最小 diff 编辑 SKILL.md；SQLite DAG 版本化(完整血缘+diff)；质量监控(技能应用率/ 完成率/回退率/工具成功率)；BM25+embedding+LLM skill_ranker 检索；工具退化触发上游 依赖技能的级联进化；云端 open-space.cl

#### 基础信息

**名称**
OpenSpace

**提出机构**
HKUDS (Data Science Lab, The University of Hong Kong). Same lab behind AnyTool, ClawWork, and nanobot, which OpenSpace builds upon.

**发布时间**
2026-03-25 (open-sourced); v0.1.0 on 2026-04-03. Active development through at least 2026-04-16.

**代码链接**
https://github.com/HKUDS/OpenSpace

**类型**
industry (open-source self-evolving skill engine / agent framework, MIT-licensed, with a hosted cloud registry at open-space.cloud)

#### 进化对象_What

**进化对象 (What)**
Tools技能 / Context记忆与提示. The evolving substrate is an external, non-parametric skill library persisted in SQLite: each
skill is a SKILL.md artifact (YAML frontmatter + markdown body, optionally bundled with src/ code) that is discovered,
applied, monitored, and re-edited over time. Model weights are never touched. The grounding agent's runtime context is
shaped by which skills get injected, and a shared cloud registry turns individual skill edits into collective knowledge
across agents.

**技能是否独立制品**
Yes. Each skill is an independent reusable artifact stored as a skill directory containing a SKILL.md file (e.g.
openspace/host_skills/delegate-task/SKILL.md, showcase/skills/large-file-write-heredoc/SKILL.md), optionally with code
assets in src/ (e.g. panel-component-xss-safe/src/utils). Artifacts follow the SKILL.md convention shared by Claude Code
/ Codex / OpenClaw / nanobot / Cursor, making them portable across host agents and shareable via the cloud registry with
full lineage + diffs.

**是否文档载体**
Yes. The core carrier is a human-readable instruction document: SKILL.md with a YAML frontmatter (name, description)
followed by a markdown body of headings (Problem / Solution / Template / Step-by-Step / Example / When to Use / Notes).
Some skills embed fenced code templates (shell/python heredoc, tool-call examples) inside the doc, and a few bundle
helper code under src/, so it is instruction-centric with occasional embedded/bundled code - predominantly a readable
instruction document.

#### 技能表示

**技能编码方式**
技能文档(.md/SKILL.md) with structured YAML frontmatter (name + description) + natural-language SOP / strategy body,
frequently containing fenced code templates (e.g. python3 heredoc write fallback, ffmpeg flags). Multi-file skill
packages appear when a skill bundles helper code (skill dir = SKILL.md + src/). The delegate-task / skill-discovery host
skills encode tool-calling contracts (execute_task / search_skills / fix_skill / upload_skill) as markdown.

**技能粒度**
子任务workflow / 策略规则. The 165 evolved GDPVal skills cluster around resilient execution patterns and error-recovery
strategies rather than domain facts: File-Format I/O fallbacks, Execution Recovery (sandbox->shell->heredoc layered
fallback), Document Generation pipelines, Quality Assurance (post-write verification), Task Orchestration, Domain
Workflows, Web/Research. Most encode a reusable workflow or fallback strategy at the sub-task level.

#### SKILL.md_专属维度

**文档形态**
Structured-field document: YAML frontmatter (name, description) on top of a markdown instruction body. Body uses
consistent sections - Problem, Solution, Template (fenced code), Step-by-Step Instructions, Full Example, When to Use
(decision tables), Notes. Fenced code blocks carry copy-pasteable templates (e.g. the heredoc write pattern). Typical
length is modest - example skills are ~1-3 KB / a few hundred to ~1k tokens; the delegate-task host skill (with tool
schemas + JSON examples) is the longer end. Multi-file packages occur when helper code is bundled
(panel-component-xss-safe = SKILL.md + src/utils).

**编辑粒度**
最小 diff / PATCH. patch.py supports multi-file FULL / DIFF / PATCH application; the README stresses 'Produces minimal,
targeted diffs rather than full rewrites, with automatic retry on failure.' Three edit outcomes: FIX (in-place repair,
same skill new version), DERIVED (new skill directory coexisting with parents), CAPTURED (brand-new skill from a
successful execution). So granularity = bounded minimal diff per evolution, not whole-document regeneration.

**版本与门控**
DAG 血脉版本化 + validation gating(门控) + 确认门控. SQLite store maintains a version DAG with full lineage + per-version diffs;
every evolved version is validated before replacing its predecessor. Confirmation gates reduce false-positive triggers
and anti-loop guards prevent runaway cycles. Predecessors are preserved in the DAG (enabling rollback). Held-out /
Pareto-front selection is NOT used (that is SkillSmith); admission is lineage + validation gated. staging+backup is
implicit via DAG persistence.

**文档来源**
执行录像回放 + 成功轨迹归纳 + 失败轨迹蒸馏 + 人工初始化 + 社区共享. (1) Human-initialized seeds: delegate-task and skill-discovery SKILL.md
authored by hand; My-Daily-Monitor seeded from analyzing open-source WorldMonitor. (2) Post-Execution Analysis replays
full execution recordings (analyzer agent loop with tool access) and proposes FIX (from failures) / DERIVED (from
parents) / CAPTURED (novel pattern from a successful run). (3) Cloud community sharing imports evolved skills from other
agents.

**编辑安全**
scope边界(skill directories / SKILL.md edits, not arbitrary source) + pre-edit lineage backup/rollback(version DAG keeps
predecessors) + 确认门控(confirmation gates reduce false positives) + anti-loop guards(prevent runaway evolution cycles) +
safety checks(flag prompt injection & credential exfiltration) + validation before replacing predecessors +
有界编辑(diff-based minimal edits, not destructive rewrites). Human-in-the-loop is optional: the host agent decides whether
to upload evolved skills to the cloud. Security hardening also covers zip-extraction / import_skill path-traversal fixes
and a pinned litellm to avoid a supply-chain CVE.

**协同进化**
skill-tool + skill-skill 生态 + 社区 collective. (1) skill-tool: when tool success rates drop, the quality monitor finds ALL
upstream dependent skills and batch-evolves them - explicit cascade co-evolution across the skill->tool dependency
graph. (2) skill-skill: dependent skills evolve together when a shared component degrades. (3) community: cloud registry
lets one agent's improvement become every connected agent's upgrade. Not generator-verifier adversarial.

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization(非梯度, 文本空间) + imitation_demonstration. Non-gradient, LLM-driven text-space evolution: an analyzer
agent (with codebase exploration + tool access) reflects on execution recordings and emits minimal diffs
(FIX/DERIVED/CAPTURED) applied via FULL/DIFF/PATCH. CAPTURED is essentially imitation - distilling a winning workflow
from a successful trajectory. A version DAG maintains lineages/populations of skill versions. No SFT, no RL, no gradient
updates.

**学习信号来源**
成败轨迹 + 工具成功率指标 + 自我反思(LLM analyzer agent loop) + 执行录像. Signals: task completion / success / failure outcomes;
skill-level applied rate, completion rate, effective rate, fallback rate; tool-call success rate, latency, flagged
issues; code-execution status and error patterns. The analyzer is itself an LLM agent (LLM-as-judge style) that gathers
evidence in the codebase before deciding edits.

**奖励粒度**
hybrid(混合). Outcome signal = task success / completion / income-capture on GDPVal; process signal = per-step tool
success rate, code-execution error patterns, per-skill applied/completion/fallback rates that drive the metric monitor.

**学习范式**
offline + sleep-time + inter-test-time. Skills are retrieved and applied intra-task (online use), but EVOLUTION happens
offline relative to the task: Post-Execution Analysis runs after each task completes; the Metric Monitor runs
periodically (daily); Tool-Degradation triggers are event-driven. No on-policy gradient updates. Version DAG replay =
sleep-time replay of execution recordings.

#### 进化时机_When

**进化时机 (When)**
inter-test-time + sleep-time. Post-Execution Analysis runs after every task (between tasks); Metric Monitor scans skill
health periodically (sleep-time / scheduled); Tool-Degradation trigger fires on event. Not intra-test-time online
editing during a single task execution.

**触发方式**
事件触发(任务后 Post-Execution Analysis) + 失败触发(FIX from broken skills / failed executions) + 工具退化触发(tool success-rate drop ->
cascade evolution of upstream dependents) + 周期性(Metric Monitor periodic scan of applied/completion/fallback rates) +
使用驱动(CAPTURED from successful executions). Three independent trigger lines of defense against skill degradation.

#### 存储与检索

**技能库结构**
DAG 血脉 + 技能文件目录 + 云端注册中心. Local: skill directories re-scanned dynamically + SQLite store holding the version DAG with
full lineage and per-version diffs + embedding cache (.openspace/openspace.db). Cloud: open-space.cloud registry for
public/private/group sharing, every evolution lineage-tracked with full diffs. Frontend dashboard visualizes Skill
Classes, Cloud Records, Version Lineage graph, Workflow Sessions.

**检索/复用方式**
BM25+embedding+LLM 重排. skill_ranker.py implements BM25 + embedding hybrid ranking; registry.py does discovery +
BM25/embedding pre-filter + LLM selection; grounding/core/search_tools.py is a Smart Tool RAG = BM25 + embedding + LLM.
Host-side skill-discovery SKILL.md triggers description-match loading; cloud search upgraded for relevance + low
latency. auto_import pulls top cloud hits locally.

#### 验证与反馈

**验证方式**
执行验证(execution-based, analyzer explores codebase & re-runs) + validation gating(门控, validated before replacing
predecessors) + LLM-judge(analyzer agent loop) + 功能正确性检查(grounding agent re-execution, QA skills verify outputs). The
analyzer gathers real evidence in the codebase before editing rather than generating blindly.

**错误纠正**
自我修订(FIX in-place) + 定向 diff 修补(FULL/DIFF/PATCH) + 回滚(predecessors kept in version DAG) + 有界编辑(bounded minimal diffs) +
重试(automatic retry on failure). FIX mode repairs broken/outdated instructions; cascade evolution repairs upstream
dependents when a tool degrades.

#### 环境与基座

**测试环境**
GDPVal + 真实生产力任务 + tool-call + 通用. GDPVal (220 real-world professional tasks / 44 occupations, 50-task subset scored,
ClawWork protocol, LLM-based scoring). Categories: Documents & Correspondence, Compliance & Form, Media Production,
Engineering, Spreadsheets, Strategy & Analysis. Showcase: My Daily Monitor - 60+ skills, 20+ panel live dashboard built
autonomously (zero human code). General agent harness integration (Claude Code / Codex / OpenClaw / nanobot).

**底座模型**
开源LLM(Qwen 3.5-Plus) for the GDPVal benchmark - identical to the ClawWork baseline so gains stem purely from skill
evolution. Pluggable backbone via LiteLLM (Anthropic Claude, MiniMax, etc.). Optimizer/target separated: the
analyzer/evolver LLM (proposes diffs, has its own agent loop + tool access) is distinct from the grounding execution
agent (target). Cloud uses embedding models for skill search.

**部署域 (Where)**
general(通用). Spans coding, DevOps, web research, desktop/GUI automation, office & professional productivity (payroll,
tax, legal memos, compliance forms, spreadsheets, media production, engineering deliverables). Designed as a universal
skill-evolution layer for any SKILL.md-compatible agent.

#### 评估指标

**评估指标**
经济价值捕获 (value capture %, $ earned) / cost (token usage, -45.9%) / success_rate (income, quality) / skill_library_growth
(165 skills) / generalization (cross-category, cross-harness) / 回归率 (controlled via validation gating + anti-loop).
Quality-monitoring metrics: skill applied rate, completion rate, effective rate, fallback rate; tool success rate,
latency, flagged issues; code-execution status & error patterns.

**关键结论**
GDPVal (50 tasks, Qwen 3.5-Plus, same backbone as ClawWork): 4.2x higher income than ClawWork; 72.8% value capture
($11,484 / $15,764 task value, best of all agents); 70.8% average quality (+30pp over best ClawWork agent at 40.8%);
-45.9% token usage in Phase 2 (warm rerun) vs Phase 1 (cold start). 165 skills self-evolved across the 50 Phase-1 tasks.
Per-category (income Δ / token Δ): Documents +3.3pp / -56%, Compliance & Form +18.5pp / -51%, Media Production +5.8pp /
-46%, Engineering +8.7pp / -43%, Spreadsheets +7.3pp / -37%, Strategy & Analysis +1.0pp / -32%. Skill taxonomy (165):
File Format I/O 44 (32 captured from failures), Execution Recovery 29 (28 captured from crashes), Document Generation 26
(document-gen-fallback evolved 13 versions - most deeply iterated), Quality Assurance 23, Task Orchestration 17, Domain
Workflow 13, Web & Research 11. Key insight: most evolved skills are tool-reliability + error-recovery patterns, not
domain knowledge. Showcase: My Daily Monitor - 60+ skills from scratch (6 seed -> +8 scaffold -> +25 build -> +12 FIX ->
+15 DERIVED -> +8 CAPTURED), 20+ live dashboard panels, zero human code.

#### 可借鉴要点

**可借鉴要点**
(1) Minimal-diff evolution on SKILL.md backed by a SQLite version DAG: have the evolver emit targeted FULL/DIFF/PATCH
edits (not whole-doc rewrites), persist every version with full lineage + diffs, validate each candidate before it
replaces its predecessor, and auto-retry on failure. This is what makes evolution token-cheap (-45.9% on warm reruns),
auditable, and rollback-safe - directly applicable to self-evolving any SKILL.md. (2) Three-trigger cascade evolution
driven by full-stack quality monitoring: run post-execution recording analysis (FIX/DERIVED/CAPTURED) after every task,
AND a periodic metric monitor over skill applied/completion/fallback rates, AND a tool-success-degradation trigger that
batch-evolves ALL upstream dependent skills via the dependency graph. Multiple independent lines of defense catch both
silent skill rot and tool/API drift - far more robust than failure-only triggers. (3) SKILL.md as a universal
cross-harness artifact + cloud registry for collective intelligence: author skills once as YAML-frontmatter markdown
(name + description + instruction body) compatible with Claude Code/Codex/OpenClaw/nanobot/Cursor, retrieve via
BM25+embedding+LLM rerank, and share through a public/private/group cloud registry with lineage tracking - turning solo
self-evolution into network-effect collective agent intelligence (one agent learns, all agents upgrade).

#### 不确定字段

- paper_link (no academic paper surfaced; shipped as open-source framework + README)
- doc_provenance / library_governance (explicit library-bloat governance / retirement / archive not documented)
- failure_memory (dedicated anti-pattern memory store with failure-signature + veto not explicitly described; only implicit via FIX + safety checks + error-pattern tracking)
- cross_transfer (cross-benchmark transfer axis untested)
- limitations (scalability of SQLite DAG / cloud registry under heavy growth; self-stated limitations not captured)

---

### AutoSkill / SkillEvo

> `engineering_practice` · ECNU-ICALK, 2026。Experience-driven Lifelong Learning(ELL)实践。从真实交互经验 (对话+agent 轨迹)自动创建可复用 Skill(SKILL.md 格式)，通过 merge+版本更新持续进化。 Local Skill Manager 做 reusable-experience triage→相似技能检索→discard/improve/ 

#### 基础信息

**名称**
AutoSkill / SkillEvo

**提出机构**
ECNU-ICALK (East China Normal University, School of Computer Science and Technology) in collaboration with Shanghai AI
Laboratory. Lead authors: Yutao Yang, Junsong Li, Qianjun Pan (co-equal); corresponding: Jie Zhou, Kai Chen, Liang He.

**发布时间**
arXiv v1 submitted 2026-03-01, v2 2026-03-05. Release timeline: AutoSkill 1.0 (2025-02-04, dialogue-time skill
extraction) -> AutoSkill4OpenClaw 1.0 (2025-02-26, trajectory-driven skill evolution) -> offline conversation extraction
(2026-03-01) -> AutoSkill4Doc 1.0 (2026-03-13, document-to-skill pipeline) -> SkillEvo 1.0 (2026-03-23,
replay/evaluation/mutation/promotion framework).

**论文链接**
https://arxiv.org/abs/2603.01145 (arXiv:2603.01145 [cs.AI], CC BY 4.0)

**代码链接**
https://github.com/ECNU-ICALK/AutoSkill (MIT license; includes autoskill/ SDK, SkillEvo/ runner, AutoSkill4Doc/,
AutoSkill4OpenClaw/, SkillBank/, web/, examples/, Docker)

**类型**
academic (formal arXiv paper with Method/System/Experimental sections) AND industry (open-source deployable framework
with Python SDK, Web UI, OpenAI-compatible proxy, Docker Compose). Classified here as academic because the arXiv paper
is the canonical citable artifact.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 (external skill memory + injected prompt context). NO model weights are updated (training-free). NO tool
definitions evolved, NO agent architecture changed. The evolution target is a library of Agent Skill artifacts
(SKILL.md) that are retrieved and injected as additive context at inference time. AutoSkill explicitly contrasts itself
with parameter-updating self-evolution.

**技能是否独立制品**
Yes. Skill is an independent reusable artifact: an Agent Skill centered on a SKILL.md file, optionally colocated with
scripts/, references/, assets/ as a multi-file package. Each artifact has a UUID id, semantic version (e.g. v0.1.34),
and is persisted on a local SkillBank directory (Skills/Users/<user_id>/<skill-slug>/SKILL.md and Common/<skill-slug>/).

**是否文档载体**
Yes (with optional hybrid extensions). The core carrier is a human-readable markdown instruction document (SKILL.md). A
minority of skills (e.g. the bundled anthropics-skill packages) also ship executable code under scripts/, making them
hybrid instruction+code packages, but AutoSkill's own extracted skills are pure markdown instruction documents.

#### 技能表示

**技能编码方式**
Structured skill document: YAML frontmatter (id, name, description, version, tags, triggers, examples) + markdown
instruction body (# Goal, # Constraints & Style, optional # Workflow, Anti-Patterns, Role & Objective, Communication &
Style Preferences, Operational Rules). NOT executable code, NOT vector-only, NOT docstring. AutoSkill4Doc adds a
configurable skill taxonomy (asset_type: macro_protocol/session_skill/micro_skill/safety_rule/knowledge_reference) and a
visible domain->family->level1->level2->micro hierarchy.

**技能粒度**
Mostly 策略规则 / 见解 (stable user preferences, stylistic constraints, response policies, domain operating conventions,
anti-patterns). Some skills are 子任务workflow (those with explicit # Workflow sections, e.g. Selenium automation, document
co-authoring). AutoSkill4Doc produces 完整技能包 with parent/child hierarchy. Atomic-action granularity is rare.

#### SKILL.md_专属维度

**文档形态**
Structured fields: YAML frontmatter (id/name/description/version/tags/triggers/examples) + markdown body (Role &
Objective, # Goal, # Constraints & Style, optional # Workflow, Anti-Patterns, Output Format). Typical token length: a
few hundred to ~1-2k tokens per skill (case-study skills 顶级心理咨询师 ~400 tokens, professional_text_rewrite ~600 tokens;
AutoSkill4Doc navigation/parent skills are larger). Multi-file packages add scripts/, references/evidence.md +
evidence_manifest.json, assets/.

**编辑粒度**
Mainly 全新生成 (LLM extraction emits a fresh candidate skill) + 整文档重写 via semantic merge (the merge model rewrites the
whole skill preserving identity; NOT raw concatenation, NOT minimal diff/PATCH). AutoSkill4Doc register_versions
supports create/strengthen/revise/merge/split/unchanged. SkillEvo uses LLM-guided + heuristic mutations of the whole
skill text. No bounded add/delete/replace or PATCH-style surgical edits are used.

**版本与门控**
Multiple mechanisms: (1) semantic versioning with patch bump on merge (Bump operator, e.g. v0.1.0 -> v0.1.1, observed up
to v0.1.34); (2) staging + backup with rollback API (POST /v1/autoskill/skills/{id}/rollback, GET .../versions,
_autoskill_version_history); (3) SkillEvo adds held-out validation gating (frozen mutate_dev split for mutation,
separate promotion_test held-out split; promote only if candidate beats current SkillEvo champion); (4) review-gated
adopt (humans can edit/save/delete SKILL.md; AutoSkill4Doc lifecycle
candidate->draft->evaluating->active->watchlist->deprecated->retired). No git-branch Pareto-frontier selection.

**文档来源**
Session 经验提取 (primary: real-time extraction from dialogue user-queries during chat), 成功轨迹归纳 (offline trajectory
extraction with --success-only 1 from agent traces), 执行录像回放 (SkillEvo builds a frozen replay pool from stored
history[].messages and replays them), LLM 一次性生成 (the extractor/merger are prompt-driven LLMs), 人工初始化 (seed skills +
bundled anthropics-skill imports), 离线 benchmark 训练 (offline extraction over WildChat-1M to bootstrap the SkillBank), and
document extraction for AutoSkill4Doc. Community 共享 via the import endpoint and Common/ library. NOT failure-trajectory
distillation.

**技能库治理**
去重合并 (merge preferred over duplicate creation when a similar user skill exists; maintainer's primary decision is
add/merge/discard), 相似度检索编辑目标 (maintenance first retrieves top-M most similar skills as local evidence rather than
reasoning over the whole bank), 灰尘清理 (auto-prune stale user skills: default prune when retrieved >= 40 and used <= 0;
per-user usage counters), 层次化索引 (AutoSkill4Doc visible domain_root / Family技能 / 一级技能 / 二级技能 / 微技能 tree). No explicit
Lotka-Volterra retirement or archive tiers in the main loop (lifecycle states exist only in AutoSkill4Doc).

**失败记忆**
Partial. (1) The merge prompt enforces 'Avoid regressions: keep important checks from the existing skill' and 'Do not
carry over stale or unrelated topic constraints', acting as soft negative guidance. (2) Each SKILL.md body commonly
includes an Anti-Patterns section (e.g. 'Do not provide medical diagnosis', 'Do not add introductory phrases') as
in-skill negative guidance. (3) SkillEvo rejects non-promoted mutations and keeps lineages in 'incubating' when replay
data is too small. However, there is NO dedicated anti-pattern memory store, NO failure-signature+attribution+remedy
buffer, and NO rejected-edit buffer reused as global negative feedback across skills (that is a SkillSmith-style feature
AutoSkill does not have).

**编辑安全**
(1) Scope 边界: AutoSkill4OpenClaw explicitly does NOT replace OpenClaw memory, ContextEngine, system prompt, tools,
provider selection, or model routing; it only edits/mirrors SKILL.md files and additive context. (2) pre-edit 备份+回滚:
version_history, rollback API, staged snapshots, AutoSkill4Doc .runtime/intermediate_runs for crash recovery. (3) 确认门控 +
人工在环: humans can directly inspect/edit/save/delete SKILL.md via REST API and the filesystem. (4) 有界编辑防破坏性重写: merge
preserves skill identity, dedupes, and avoids regressions; unsafe merge target in OpenClaw embedded mode degrades to
'add' (no blind merge); duplicate candidate skills are skipped before maintenance. (5) Discard gate rejects
generic/low-signal/non-portable candidates to prevent library noise. No explicit eval-hacking defense beyond SkillEvo
held-out split; no key/injection check.

**协同进化**
Predominantly skill-only. Skills evolve independently of tools and of each other (no skill-tool bundle editing, no
generator-verifier co-training). There is weak skill-skill ecosystem interaction via the merge/dedup decision (a new
candidate is compared to its nearest neighbor skill). AutoSkill4OpenClaw mirrors skills into OpenClaw's tool-loading
directory but does not evolve OpenClaw's tools. SkillEvo is a skill-only replay/mutation loop. So: skill-only (with
light skill-skill dedup linkage).

#### 自进化机制_How

**进化方法范式 (How)**
Training-free, prompt-driven composition (NO gradient/RL/SFT). Five LLM modules instantiated by prompts: query rewriter,
response generator, skill extractor, management judge, skill merger (+ embedding model). Paradigm blend: (a)
imitation_demonstration / 经验蒸馏 (extraction abstracts reusable patterns from user interaction traces); (b) reward-based
with LLM-as-judge (the management judge decides add/merge/discard; SkillEvo judge scores binary eval rules); (c)
rollout_optimization in text space (SkillEvo: replay -> evaluate -> mutate -> promote, non-gradient); (d)
population_evolutionary element (SkillEvo champion registry, mutation budget). The core AutoSkill loop is (a)+(b);
SkillEvo adds (c)+(d).

**学习信号来源**
成败轨迹 (offline trajectory extraction uses --success-only 1; only closed sessions with >=1 successful main turn are
extracted), LLM-as-judge (management decision, SkillEvo judge-LLM binary rules), 自我反思 (the extraction and merge are
LLM-driven abstractions), 工具成功率指标 / 使用指标 (retrieved/relevant/used usage counters drive pruning). Critically, extraction
uses ONLY user queries {q1..qt} as evidence, NOT model responses rt, to capture stable user requirements rather than
model artifacts.

**奖励粒度**
Outcome (session/turn-level). Extraction fires after a turn/session boundary; management decision is per-candidate;
SkillEvo promotion is a binary outcome on a held-out replay sample. Process-level per-step rewards are not used. Hybrid
only in the weak sense that usage counters accumulate across turns.

**学习范式**
Both online and offline; on-policy (uses the current model's own traces) for online extraction; sleep-time/offline for
SkillEvo replay, offline conversation/document/trajectory batch extraction, and startup maintenance. Online extraction
runs asynchronously in the background (non-blocking) during serving. So: online inter-test-time + offline sleep-time
replay.

#### 进化时机_When

**进化时机 (When)**
inter-test-time (extraction after turns/sessions; AutoSkill4OpenClaw agent_end hook) + sleep-time (SkillEvo offline
replay; offline batch extraction over WildChat; startup offline maintenance). intra-test-time evolution is NOT performed
(only retrieval+injection happens intra-turn; the evolution loop is async/background).

**触发方式**
事件触发 (after turn/session close; AutoSkill4OpenClaw agent_end / before_agent_start hooks; OpenAI proxy schedules
extraction after response), 使用驱动 (extract_mode=auto every extract_turn_limit turns, =always every turn, =never off;
/extract_now [hint] forces extraction), 失败触发 / 成功触发 (trajectory extraction with --success-only 1; extraction runs only
if closed session has >=1 successful main turn), 周期性 (AutoSkill4OpenClaw sessionMaxTurns=20 auto-closes long-lived
sessions to force an extraction pass). NOT curriculum-driven, NOT tool-degradation-triggered.

#### 存储与检索

**技能库结构**
技能文件目录 (SkillBank/Users/<user_id>/<skill-slug>/SKILL.md + Common/<library>/<skill-slug>/ +
vectors/<embedding-signature>.{meta.json,ids.txt,vecs.f32} + index/skills-bm25.* + skill_usage_stats.json), 向量库 (on-disk
f32 vector cache keyed by embedding signature, separate index per embedding model), 层次化 (AutoSkill4Doc
domain_root/Family技能/一级技能/二级技能/微技能 visible tree + .runtime/document_registry). Version history stored in
_autoskill_version_history within skill metadata. No git-branch frontier, no cloud registry (local-first; Docker mounts
./SkillBank).

**检索/复用方式**
Hybrid: 语义相似度 (dense embedding, sim(Memb(q~), Memb(s))) + BM25 lexical, combined by weighted sum Rel = lambda*d_hat +
(1-lambda)*b_hat, with min_score threshold eta + top-k. Preceded by LLM query rewriting (resolves coreference, preserves
task anchor, exposes retrieval-critical constraints). Management-time retrieval uses a separate weight alpha and top-M
neighbor set. AutoSkill4Doc uses embedding + BM25 over metadata-rich skill text for register_versions.
Description/tags/triggers matching effectively drives loading. No LLM re-rank step in the main loop (selection.py has an
optional LLM skill selector).

#### 验证与反馈

**验证方式**
LLM-judge (the prompt-driven management judge compares candidate vs nearest-neighbor skill on four axes: job-to-be-done,
deliverable type, hard constraints, required tools/workflow), 留出评估 (SkillEvo: frozen mutate_dev split for mutation,
separate promotion_test held-out split), 功能正确性检查 / 程序化验证 (SkillEvo compiles 3-6 binary eval rules from prompt +
requirement stats, evaluated by programmatic + judge-LLM engine), validation gating (SkillEvo promotes only if candidate
beats current champion on promotion_test), AutoSkill4Doc lifecycle gating
(candidate->draft->evaluating->active->watchlist->deprecated->retired). No multi-model debate, no execution-based
runtime test in the main loop. The paper itself does NOT report downstream task-accuracy validation.

**错误纠正**
自我修订 (LLM merge rewrites the whole skill via semantic union, removing stale/case-specific content), 回滚 (POST
/skills/{id}/rollback + version_history + AutoSkill4Doc staged intermediate snapshots for crash recovery), 有界编辑 (merge
preserves skill identity and important checks to avoid regressions), discard (rejects generic/low-signal/non-portable
candidates outright), 重规划 (query rewrite and merge re-frame the skill). No targeted diff patching; edits are
whole-document regenerations.

#### 环境与基座

**底座模型**
开源 LLM primary: InternLM Intern-S1-Pro and DashScope Qwen (qwen-plus) in demos; also supports GLM (Zhipu/BigModel),
OpenAI GPT, Anthropic Claude, and generic OpenAI-compatible backends. Embeddings: DashScope text-embedding-v4, generic
embd_qwen3vl8b, or hashing (mock). Optimizer/target separation exists in SkillEvo (separate mutation LLM vs judge LLM
via --llm-provider/--llm-model vs --judge-provider/--judge-model) and conceptually in AutoSkill (distinct modules can
share one backbone or use different ones). All modules are the same backbone LLM by default, distinguished only by
prompt.

**部署域 (Where)**
general (model-agnostic personalization layer across coding, writing, counseling, office docs, social-media copy).
AutoSkill4Doc adds specialized document domains (psychology/CBT, chemistry/analytical chemistry) via configurable
taxonomies. Primary positioning is a general lifelong-personalization layer for LLM assistants and personal digital
surrogates.

#### 局限与挑战

**局限与挑战**
doc_bloat (merge accumulates content; mitigated only by merge-time dedup, no hard token budget), regression_risk (LLM
merge could drop important constraints despite the 'avoid regressions' instruction; only SkillEvo's held-out gate guards
this, not the main AutoSkill loop), controllability / optimizer_quality (extraction and merge quality depend entirely on
the backing LLM and prompts; weak models produce noisy skills), scalability (library grows with users/sessions; pruning
is a simple retrieved>=40 && used<=0 heuristic, not learned), transferability (cross-model/cross-language demonstrated
for extraction but retrieval/injection quality across models is not benchmarked), eval-hacking (possible in SkillEvo if
promotion_test leaks; mitigated by frozen split but not formally analyzed). catastrophic_forgetting is N/A (no param
updates). The paper explicitly lacks quantitative downstream-task evaluation.

#### 可借鉴要点

**可借鉴要点**
- Discard-first extraction policy (anti-noise gate): AutoSkill extracts a skill ONLY when the user expresses DURABLE constraints/preferences/corrections (e.g. 'avoid hallucinations', institutional writing style), and explicitly returns an empty result for generic one-off requests like 'write a report'. This is the single most actionable design for keeping a self-evolving SKILL.md library clean: gate extraction on durable, reusable signal, and default to no-op. Combined with user-side-only evidence (extract from USER queries, never from model responses) this yields a clean learning signal.
- Retrieval-assisted maintenance over local evidence (scalability): Instead of feeding the entire skill bank to the judge/merger, AutoSkill first retrieves the top-M most similar existing skills and makes the add/merge/discard decision against only the single nearest neighbor. This makes maintenance O(log N)-ish and focused, avoiding the cost and context-bloat of whole-library reasoning. For a self-evolving SKILL.md system this is the right scaling pattern: maintenance decisions are local.
- Versioned semantic-union merge (continual refinement without duplication): On merge, the merger LLM performs a semantic union (not concatenation), preserves the skill identity/UUID, dedupes sections/bullets/triggers/tags/examples, strips case-specific entities, keeps prior important checks to avoid regressions, and bumps a semantic patch version (v0.1.0 -> v0.1.1 ... up to v0.1.34 observed). This lets the same skill refine continuously instead of spawning duplicate fragments. Pair this with a held-out promotion gate (SkillEvo: mutate on dev, promote only if beating the champion on a held-out split) to make iterative SKILL.md evolution both non-duplicative and non-regressive.

#### 不确定字段

- type (genuinely hybrid academic+industry; single-label forced)
- cross_transfer (cross-基准 / cross-benchmark transfer not evaluated)
- test_env (no standardized agent benchmark like AgentBench confirmed; StuLife is related work, not an AutoSkill evaluation target)
- metrics (cost/token economics and downstream task success_rate/accuracy not reported in the paper)
- key_results (no head-to-head quantitative gains vs baselines; the paper reports SkillBank statistics and case studies only)
- learning_paradigm (on-policy vs off-policy boundary is fuzzy since offline extraction reuses historical logs of potentially different models)

---

### claude-self-improving-skills

> `engineering_practice` · UniM0cha, 2026。Hermes Agent 风格的 Claude Code 自改进。专用 distiller subagent 从 工作流经验蒸馏为 SKILL.md(遵循 Anthropic skill-creator 指引)。偏好 patch 现有技能→ 伞形技能→加参考文件，仅最后才新建类级技能。编辑安全：pre-edit 备份+post-edit 验证+ provenance 

#### 基础信息

**名称**
claude-self-improving-skills (Claude Self-Improving Skills plugin; internal plugin id `self-improving-skills`)

**提出机构**
Independent / community developer UniM0cha (GitHub user). No academic or corporate institution; solo-authored
open-source Claude Code plugin. Inspired by Nous Research Hermes Agent.

**发布时间**
2026-06-09 (GitHub repo created; first public version). v0.9.0 added team skill sharing. Active as of 2026-06-19.
[uncertain: exact first-release tag/version date not confirmed beyond repo creation]

**代码链接**
https://github.com/UniM0cha/claude-self-improving-skills (MIT license, Python). Installed as a Claude Code plugin
marketplace: `/plugin marketplace add UniM0cha/claude-self-improving-skills` then `/plugin install
self-improving-skills@claude-self-improving-skills`. 8 stars / 2 forks as of 2026-06-19.

**类型**
industry (open-source framework / Claude Code plugin) leaning blog_practice. Not academic — no paper, no benchmark
evaluation; an engineering port of Hermes Agent's procedural-memory loop into Claude Code primitives.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能. The evolving object is the user's learned procedural-memory library at
`~/.claude/skills/<name>/SKILL.md` (markdown instruction documents + optional reference/template/script files). Model
weights are FROZEN; the Claude Code harness, hooks, and subagent architecture are fixed primitives that are merely WIRED
into a closed learning loop. Architecture is single-agent-with-background-subagent (a dedicated `skill-distiller`
subagent), not a multi-agent population. Factual memory is explicitly out of scope (handled by Claude Code's native
memory).

**技能是否独立制品**
Yes. Each skill is an independent reusable artifact materialized as a folder `~/.claude/skills/<name>/` containing a
`SKILL.md` (the instruction document, primary carrier) plus optional `references/`, `templates/`, `scripts/` subdirs for
bulky material. Skills live in the user directory, NOT inside the plugin, so updating the plugin never erases
accumulated knowledge. Agent-distilled skills carry `metadata.provenance: self-improving-skills` so they are
distinguishable from human/team skills.

**是否文档载体**
是 (Yes — instruction-document-centric). The core carrier is a readable markdown `SKILL.md` with YAML frontmatter (name /
description / metadata.provenance / origin) and a body (## When this applies / ## The technique / ## Gotchas). It is
mixed only in that a skill folder MAY additionally bundle executable helper scripts/templates under subdirs pointed to
by one line in the body; the instruction markdown remains the primary, deployed, and validated artifact. No vectors, no
pure-code skills.

#### 技能表示

**技能编码方式**
技能文档 (.md / SKILL.md) + 多文件技能包. Canonical Claude Code skill contract: YAML frontmatter (`name`, `description`,
`metadata.provenance`, `origin`) + markdown body. Bulky references, API dumps, and reproduction recipes are moved into
the skill's `references/` subdir and referenced by one line, keeping `SKILL.md` bodies small. The distiller subagent (in
`agents/skill-distiller.md`) encodes the procedural technique as imperative/infinitive-mood prose with a real code
example. Team-shared skills are additionally tagged `created_by: team`.

**技能粒度**
策略规则 + 完整技能包 at CLASS level. Each skill captures a reusable, class-level technique (e.g. `pyannote-speaker-diarization`,
`react-effect-cleanup`, `shadcn-v4-migration`). Explicitly NOT instance-specific: one-off task narratives, PR numbers,
error strings, codenames, `fix-X`/`debug-Y` labels are rejected. Finer than a full workflow, coarser than an atomic
action; an umbrella skill can consolidate several narrower class-level skills.

#### SKILL.md_专属维度

**文档形态**
Structured markdown document = YAML frontmatter + titled body sections. Frontmatter fields: `name`
(lowercase-hyphenated, <=64 chars, no leading/trailing/double hyphens, class-level), `description` (third-person
situation match, target <=500 chars because it is injected into EVERY future session's system prompt as a permanent
context cost — the validator warns above 500), `metadata.provenance` (= `self-improving-skills`), `origin` (=
`distilled`). Body sections: `# <Title>`, `## When this applies` (concrete trigger/situation), `## The technique`
(reusable steps/pattern/fix with a real code example), `## Gotchas` (edge cases / what bit us / what to verify).
Imperative/infinitive mood. Body target roughly 1,500-2,000 words max (~2k-3k tokens); description ~125-250 tokens.

**编辑粒度**
有界增删替换 (bounded add/delete/replace via the `Edit` tool) is strongly PREFERRED over whole-document rewrite or brand-new
generation. The distiller follows a strict ordered decision procedure: (1) patch a directly-relevant existing SKILL.md
(add a gotcha / corrected step / example); (2) patch a broader umbrella skill with a new subsection; (3) add a
supporting file under an existing skill's `references/`/`templates/`/`scripts/` subdir and point to it with one line;
(4) create a NEW class-level skill ONLY as a last resort, after checking collisions with live AND archived skills and
with installed plugin skills. Single responsibility: the distiller never pushes to a remote;
`/propose-plugin-improvement` handles upstream PRs in an isolated clone.

**版本与门控**
staging+backup + review-gated adopt + automatic rollback. (a) Pre-edit backups are taken before any skill edit; the
PostToolUse validator checks frontmatter/size/provenance and AUTOMATICALLY ROLLS BACK malformed `SKILL.md`. (b)
Provenance stamping (`metadata.provenance: self-improving-skills`) marks agent-distilled skills so the curator and
session counter can find them. (c) The `/curate-skills` LLM pass is plan-FIRST, apply-only-after-approval
(human-in-the-loop gate). (d) Team sharing is PR-gated: `/share-skill` opens a PR a human merges; `/sync-team-skills`
shows a read-only plan you confirm, then per-skill transactional apply. (e) The origin-hash rule: untouched local copies
auto-update; customized copies are NEVER overwritten (one-time diverged notice); deleted/archived copies are never
re-installed. (f) `SIS_PLUGIN_PR=1` opt-in gate for upstream plugin PRs. No git-branch frontier selection or Pareto/DAG
versioning.

**文档来源**
成功轨迹归纳 + session 经验提取. The distiller runs AFTER a piece of work is done and reads the tail of the actual transcript
JSONL (assistant `message.content[]` tool_use/text blocks) plus the changed files to ground itself in what really
happened — not a summary alone. It captures durable, reusable, class-level technique distilled from successful work.
Explicitly NOT failure-trajectory distillation: anti-patterns are listed as 'Do NOT capture' (one-off narratives,
environment-dependent workarounds, negative tool claims, already-obvious things) and are used only as negative guidance,
not stored as skills. Initial plugin code is human-authored; team skills arrive via community共享 (git repo). No offline
benchmark training.

**跨载体迁移**
跨任务 (class-level skills are reusable across tasks by construction) + 跨用户/团队 (team skill sharing via git repo with
origin-hash sync since v0.9.0; publish generalizes techniques by stripping personal style; receive is transactional and
conflict-aware) + 跨agent harness PARTIAL (skill CONTENT is portable markdown, but the PLUGIN itself is
Claude-Code-specific — it relies on Claude Code hooks/subagents/slash-commands/skill-discovery primitives, so the
self-improvement LOOP does not transfer to Codex/Cursor). NOT cross-model in the loop sense (single Claude backbone);
skill text is model-agnostic. NOT cross-benchmark (no benchmark).

**技能库治理**
灰尘清理 (curator loop) + 库膨胀治理 via recoverable archive + 去重合并 (umbrella consolidation) + 层次化索引 (umbrella vs class-level).
Concretely: agent-created skills unused for 30 days (`SIS_STALE_AFTER_DAYS`) are marked stale; after 90 days
(`SIS_ARCHIVE_AFTER_DAYS`) they are moved recoverably to `~/.claude/skills/.archive/`. Skills proven by repeated use
(`use_count >= 3`) age at HALF speed (archive threshold doubled) — a simple reputation-weighted lifecycle. The
`/curate-skills` LLM pass is an umbrella-building consolidation modeled on Hermes' curator prompt: plan first, apply
only after approval (requires >=8 learned skills, `SIS_CURATE_MIN_SKILLS`; runs every 7 days,
`SIS_CURATE_INTERVAL_DAYS`). Supporting commands: `/pin-skill`, `/archive-skill`, `/restore-skill`, `/prune-skills`,
`/curator-status`. Team skills (`created_by: team`) are NEVER touched by the personal curator — their owner is the team
repo. Bulk reads during curation never reset a skill's idle clock.

**失败记忆**
Partial / soft. There is no dedicated rejected-edit buffer or failure-signature store as a standalone artifact. Negative
knowledge is encoded as an explicit 'Do NOT capture' anti-pattern list inside the distiller's prompt (one-off
narratives, environment-dependent failures, negative tool claims, already-obvious things, pure user-directed feature
work) — this steers the generator away from junk. Negative FEEDBACK at edit time comes from the PostToolUse validator,
which rejects and rolls back malformed edits (frontmatter/size/provenance violations) and emits non-blocking quality
advisories (e.g. over-long descriptions). A declined distillation nudge stays declined and only re-fires after another
threshold of NEW work, avoiding repeated bad timing. No formal anti-pattern skill file or failure-attribution memory.

**编辑安全**
Detailed and first-class. (1) Scope boundary: edits are confined to `SKILL.md` and supporting files under
`~/.claude/skills/`; single responsibility — the distiller never pushes to a remote. (2) Pre-edit backups + automatic
rollback on malformed `SKILL.md` (PostToolUse validator enforces the Claude Code skill contract: frontmatter schema,
name format, description length, provenance). (3) Provenance stamping so agent-distilled skills are trackable. (4)
Anti-injection / anti-secret: skills are 'instructions to an agent' = a prompt-injection vector, so EVERY write of team
content (first install AND later updates) passes a static scanner for secrets, destructive commands, injection markers,
symlinks, hidden files, and size caps; blocked content is QUARANTINED, never placed in `~/.claude/skills`. (5)
Human-in-the-loop / review-gated: team sharing is PR-gated by design (a human merges); the curator is
plan-first/apply-after-approval; `/share-skill` shows a diff before opening a PR. The author states the human review
gate IS the security boundary — a real-time shared skill store is deliberately rejected because it would let one
compromised session inject instructions into every teammate's agent. (6) Personalization-always-wins via origin-hash
sync (customized copies never overwritten). (7) Fail-safe hooks: any hook error approves the original action instead of
breaking the Claude Code session. (8) Bounded edits (prefer patching over creating) limit destructive rewrites.

**协同进化**
skill-skill 生态 + skill-prompt 联合 + generator-verifier 协同. (a) skill-skill: umbrella skills consolidate narrower
class-level skills (`/curate-skills`); a skill points to reference files of other skills; the library self-organizes
into a hierarchy. (b) skill-prompt joint: every learned skill's `description` is injected into every future session's
system prompt, so the skill document and the agent's prompt co-evolve (description length is a permanent context cost,
hence the <=500 char target). (c) generator-verifier: the `skill-distiller` subagent (generator) produces edits and the
PostToolUse validator (verifier) gates them with rollback — a lightweight adversarial check. NOT skill-tool coevolution
(Claude Code's tools/hooks/subagents are fixed primitives, not evolved).

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration + rollout_optimization (non-gradient, text-space editing), flavored by LLM-as-implicit-judge.
The distiller performs in-context learning from a successful trajectory (reads transcript tail + changed files) and
emits bounded textual edits to `SKILL.md`. No gradient updates, no RL, no numeric reward, no population/evolutionary
search. The learning signal is qualitative: 'did this session produce a reusable, class-level technique?'. Modeled on
Nous Research Hermes Agent's procedural-memory + curator loop, ported into Claude Code's hook/subagent/skill primitives.

**学习信号来源**
成败轨迹 (successful work sessions — distill what worked) + 自我反思 (the distiller's own judgment of whether the technique is
reusable and class-level vs one-off) + 工具成功率指标 used as a COMPLEXITY DETECTOR (tool-call count >=
`SIS_DISTILL_THRESHOLD`=12 AND file-edit count >= `SIS_MIN_FILE_EDITS`=2 since last distillation trigger the nudge).
Separately, usage telemetry (use/view/patch counts in `~/.claude/self-improve/skill_usage.json`) drives the curator's
aging/reputation signal — patch counting runs in the PostToolUse hook so background-subagent edits are captured. No
environment reward, no held-out validation score, no LLM-as-judge scoring loop.

**奖励粒度**
outcome. The signal is evaluated per segment-of-work / per-session outcome (did this finished chunk of work yield a
reusable technique). The Stop hook fires the nudge once per segment of work, not per tool call.

**学习范式**
inter-test-time, online stream, on-policy. Distillation happens between sessions (at session end via the Stop hook, or
on-demand via `/distill-skill`), NOT intra-test-time (it does not interrupt mid-task except for the one-time
end-of-segment block nudge). It is sleep-time-LIKE (a background subagent runs after the work is done) but the author
explicitly notes Claude Code lacks Hermes' free background daemon, so distillation uses a VISIBLE/BILLABLE subagent turn
rather than a free offline replay thread. On-policy (the same Claude backbone that did the work reflects on it).

#### 进化时机_When

**进化时机 (When)**
inter-test-time primarily. The Stop hook evaluates complexity at session/segment end; the curator runs periodically
(`SIS_CURATE_INTERVAL_DAYS`=7 when learned-skill count >= `SIS_CURATE_MIN_SKILLS`=8); team-sync reminder fires on
SessionStart (once a day, no network). Manual commands (`/distill-skill`, `/curate-skills`, `/share-skill`,
`/sync-team-skills`, etc.) allow on-demand evolution at any time. NOT intra-test-time.

**触发方式**
事件触发 (session/segment end via Stop hook when the complexity threshold is met) + 使用驱动 (usage telemetry drives the
stale/archive lifecycle: 30d stale, 90d archive, half-speed aging for use_count>=3) + 周期性 (automatic curator every 7
days) + manual command trigger. The nudge is once-per-segment-of-work: a DECLINED nudge stays declined and only re-fires
after another threshold of NEW work (new tool calls + file edits accumulate since the last distillation), which prevents
nagging and prevents pure-research chats from triggering (requires >=2 file edits).

#### 存储与检索

**技能库结构**
技能文件目录 (flat user directory `~/.claude/skills/<name>/SKILL.md`) + 层次化 (`.archive/` subdir for recoverably archived
skills; umbrella skills sit alongside class-level skills and consolidate them) + git repo for team sharing (private team
repo with a `skills` subdir, configured via `~/.claude/self-improve/team_config.json`). Supporting state files:
`~/.claude/self-improve/skill_usage.json` (telemetry), team_config.json, per-skill origin-hash records. NOT a vector DB,
NOT a graph/DAG, NOT a cloud registry — a plain filesystem tree plus optional git remote.

**检索/复用方式**
description 匹配触发加载 (Claude Code's NATIVE skill discovery: each skill's `description` is injected into the session system
prompt and the skill is loaded when the description matches the user's situation — this is why description quality and
length are enforced). The distiller itself uses Glob `~/.claude/skills/**/SKILL.md` + name/description matching to find
candidate skills to patch, and `ls ~/.claude/skills/` (+ `.archive/`) for collision detection. No embedding/BM25 vector
retrieval; no generation-as-retrieval. Next session rediscovers the skill 'normally' via Claude Code's built-in
mechanism.

#### 验证与反馈

**验证方式**
validation gating + 功能正确性检查 + LLM-judge (self). The PostToolUse validator enforces the Claude Code `SKILL.md` contract:
frontmatter schema (name format: lowercase-hyphenated, <=64 chars, no leading/trailing/double hyphens; description
present; `metadata.provenance`), size limits (description <=500 char advisory, body ~1500-2000 word target), and
provenance stamping; malformed edits trigger automatic rollback from the pre-edit backup. Non-blocking quality
advisories warn about over-long descriptions (permanent context cost). The distiller self-assesses (LLM-judge) whether
the technique is reusable and class-level before writing. For team sharing, a static scanner validates
secrets/destructive-commands/injection-markers/symlinks/hidden-files/size on every team write. No execution-based
benchmark validation, no held-out evaluation, no multi-model debate — the author is explicit that there is no formal
evaluation.

**错误纠正**
回滚 (automatic rollback on malformed SKILL.md from pre-edit backup) + 有界编辑 (bounded edits strongly preferred over
whole-doc rewrite) + 定向 diff 修补 (targeted `Edit` calls to add a gotcha/step/example to an existing skill). The validator
flags problems and the distiller fixes them. Fail-safe hooks approve the original action on any hook error so a broken
hook never blocks the user's Claude Code session. The curator is intentionally conservative (archives only agent-created
skills, keeps recoverable backups, never touches team skills).

#### 环境与基座

**测试环境**
真实生产力任务 (real Claude Code coding/agent sessions in the wild). No benchmark environment. The plugin ships its own pytest
suite (`tests/`, run via `uv run --with pytest -- pytest tests/`) covering hooks/scripts/validator/team-sync/scanner,
but there is no SkillsBench/GDPVal-style task benchmark for the learned skills themselves.

**底座模型**
Claude (Claude Code). The distiller subagent uses `model: inherit` (same Claude backbone that performed the work).
Optimizer/target are NOT separated — a single Claude model both executes the task and reflects on/distills it. No VLM,
no open-source-LLM variant documented.

**部署域 (Where)**
specialized (Claude Code coding/agent productivity). The plugin is Claude-Code-specific by construction (it wires Claude
Code hooks, subagents, slash commands, and the native skill-discovery mechanism). General only in the sense that it
applies to any Claude Code workflow, not to a single coding language or domain.

#### 评估指标

**评估指标**
skill_library_growth + usage telemetry (use_count / view_count / patch_count in
`~/.claude/self-improve/skill_usage.json`) + implicit 回归率 (validator rollback rate on malformed edits). Stale/archive
lifecycle counts (30d/90d) as a library-health signal. NO success_rate, NO generalization benchmark, NO
sample-efficiency or economic-value numbers — the author explicitly lists 'Honest limitations' and provides no
quantitative evaluation. Cost is acknowledged qualitatively: distillation consumes a visible/billable subagent turn
because Claude Code has no free background daemon (unlike Hermes).

#### 局限与挑战

**局限与挑战**
Explicitly stated 'Honest limitations' plus implicit ones. (1) scalability/cost: Claude Code provides no free background
daemon thread, so distillation uses a visible/billable subagent turn (not free sleep-time replay like Hermes). (2)
scope: handles procedural memory (SKILL.md) only, NOT factual memory — must be complemented by Claude Code's native
memory or separate memory plugins. (3) controllability/regression_risk: curator is intentionally conservative (archives
only agent-created skills, keeps recoverable backups), but there is no held-out regression benchmark, so a bad
agent-distilled skill can persist until the 30/90-day lifecycle catches it. (4) safety/transferability: team sync is
PR-gated BY DESIGN — a real-time shared skill store is deliberately rejected because skills are a prompt-injection
vector and one compromised session could inject instructions into every teammate's agent; the human review gate IS the
security boundary. (5) transferability: the plugin is Claude-Code-specific (uses Claude Code
hooks/subagents/skill-discovery); only the skill CONTENT is portable. (6) optimizer_quality: the distiller's judgment of
'reusable class-level technique' is the quality bottleneck — naive auto-logging produces junk, mitigated (not solved) by
the anti-pattern 'Do NOT capture' list and class-level naming enforcement. (7) doc_bloat: mitigated by description <=500
char advisory + body 1500-2000 word cap + references/ subdir, but not formally measured.

#### 可借鉴要点

**可借鉴要点**
- 1. Encode a STRICT, ORDERED distiller decision procedure inside a dedicated subagent: (1) patch a directly-relevant existing SKILL.md, (2) patch a broader umbrella skill, (3) add a supporting reference/template/script file under an existing skill, (4) create a NEW class-level skill ONLY as a last resort — combined with an explicit 'Do NOT capture' anti-pattern list (one-off narratives, environment-dependent workarounds, negative tool claims, already-obvious things) and class-level naming enforcement (reject instance-specific names like PR numbers or fix-X labels). This ordered preference + negative guidance is the single most important defense against the skill-library bloat and junk accumulation that plagues naive auto-logging, and it keeps the loop additive-by-default rather than multiply-by-default.
- 2. Make EDIT SAFETY a first-class engineering concern, not an afterthought: take pre-edit backups, run a PostToolUse validator that enforces the SKILL.md contract (frontmatter schema / name format / description length / provenance stamp) and AUTOMATICALLY ROLLS BACK malformed edits, stamp every agent-distilled skill with `metadata.provenance` for trackability, and — for any team-sharing path — put a human review gate (PR-gated) plus a static injection/secret/symlink scanner with quarantine in front of every write. The origin-hash rule (untouched auto-updates; customized NEVER overwritten; deleted never re-installed) makes 'personalization always wins' a property that holds by construction. Treat skills as the prompt-injection vector they are: the review gate IS the security boundary.
- 3. Add a CURATOR LOOP with usage-driven aging and umbrella consolidation to keep the library from growing unboundedly: unused agent-created skills go stale after 30d and are recoverably archived after 90d, but PROVEN skills (use_count >= 3) age at HALF speed — a cheap, reputation-weighted 'Lotka-Volterra-lite' lifecycle that keeps useful skills alive while auto-pruning the rest, without any learned reward model. Pair it with an LLM `/curate-skills` pass that builds umbrella skills to fold narrower skills into a self-organizing hierarchy, run as plan-first / apply-after-approval (human-in-the-loop) and gated on a minimum library size so it only fires when there is enough to consolidate.

#### 不确定字段

- paper_link (no academic paper exists; this is an open-source Claude Code plugin)
- key_results (no quantitative benchmark/evaluation published; only qualitative description of the implemented loop and GitHub adoption counts)
- release_date (repo created 2026-06-09; exact first-version tag and v0.9.0 date not confirmed beyond the README mention)
- reward_granularity / learning_paradigm labels are interpretive (the project does not frame itself in ML-training terminology; labels assigned by mapping its behavior onto the survey taxonomy)

---

### claude-evolving-skills (reflect-and-learn)

> `engineering_practice` · PalmDr, 2026。让 Claude Code 自我改进：automated scouting + 多模型辩论(Claude+Gemini+ Codex)+reflection。reflect-and-learn 是核心自改进循环：复盘过往 session→双通道打分→ 多模型辩论→memory consolidation→experience stripping→tool co-evolu

#### 基础信息

**名称**
claude-evolving-skills (reflect-and-learn)

**发布时间**
2026-03 (LinkedIn essay 'I Stopped Chasing Viral Agentic Workflow Repos' published 2026-03-21; GitHub repo single-commit, 6 stars as of mid-2026)

**代码链接**
https://github.com/PalmDr/claude-evolving-skills

**类型**
blog_practice

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 (primary): CLAUDE.md rules, ~/.claude memory entries, and skill SKILL.md files are the evolution targets.
Tools技能 is a secondary co-evolution surface (Agent 6 promotes ephemeral ad-hoc scripts to persistent skills, and
proposes new MCP servers). Model weights and agent architecture are NOT evolved.

**技能是否独立制品**
是 — Skills exist as standalone reusable artifacts. Form: one SKILL.md file per skill folder under ~/.claude/skills/
(e.g. reflect-and-learn/SKILL.md, agentic-radar/SKILL.md, vendor-docs-radar/SKILL.md, gemini-agent/SKILL.md,
codex-agent/SKILL.md). Supporting artifacts: bash wrappers in scripts/, JSONL lineage files (evolution-tree.jsonl,
scoreboard.jsonl), REGISTRY.md tools registry.

**是否文档载体**
混合 — Core carrier is human-readable Markdown instruction documents (SKILL.md), but they embed executable bash/code
blocks (jq session parsing, git commits, launchd plists) and YAML frontmatter. The AGENTS.md explicitly frames the repo
as 'structured for both human and agent consumption' (Karpathy Software 3.0 ethos).

#### 技能表示

**技能编码方式**
技能文档(.md/SKILL.md) with YAML frontmatter (name + description with trigger phrases) + Markdown body of step-by-step
execution instructions. Memory encoded as JSONL (evolution-tree.jsonl, scoreboard.jsonl) and Markdown (reflections/*.md,
CLAUDE.md, CHANGELOG.md). No vector embeddings, no graph DB.

**技能粒度**
完整技能包 / 子任务workflow — Each skill is a complete multi-step workflow (reflect-and-learn has 6 steps, launches 6 parallel
analysis agents + synthesis + debate + adoption + consolidation). Sub-skill granularity exists (each of the 6 analysis
agents is a scoped sub-task). No atomic-action or pure-insight granularity.

#### SKILL.md_专属维度

**文档形态**
结构化字段: YAML frontmatter (name, description with trigger keywords) + Markdown body with H2/H3 sections (When to Use,
Output, Execution Instructions Step 0-6, Rubric Reference, SOTA References). Embeds fenced bash/json/jsonl/markdown code
blocks. The reflect-and-learn SKILL.md is large (~500+ lines, approaching the 600-line cap mandated by AGENTS.md). Other
skills (gemini-agent, codex-agent) are short delegation stubs.

**编辑粒度**
有界增删替换 (add/delete/replace) on CLAUDE.md rules and memory entries; targeted diffs (each proposed change is a specific
CLAUDE.md/skill edit with rationale); experience stripping = bounded deletion (rule necessity test marks STRIP_CANDIDATE
but NEVER auto-removes — always flags HIGH-IMPACT for user). Methodology changes 'append, not overwrite' per the
self-evolution protocol. Not whole-document rewrites.

**版本与门控**
Layered: (1) review-gated adopt — P0-AUTO (>=8.0, 3/3 voices agree, Safety>=8) and P1-AUTO (>=7.0, 2/3 voices)
auto-apply; HIGH-IMPACT (Safety<7 or voices disagree) flagged for user; DEFER logged only; ROLLBACK for
CONFIRMED_HARMFUL. (2) staging+backup via git commits after every reflection cycle. (3) DAG/tree lineage versioning
(evolution-tree.jsonl with parent_id→node_id) enabling AFlow-style backtracking. (4) retrospective gating — past
adoptions re-scored CONFIRMED_HELPFUL/INCONCLUSIVE/CONFIRMED_HARMFUL.

**文档来源**
session 经验提取 (extracts past week's conversation JSONL via jq) + 失败轨迹蒸馏 (Agent 1 failure analysis with text gradients) +
成功轨迹归纳 (user satisfaction detector extracts recurring praise patterns) + 社区共享 (agentic-radar/vendor-docs-radar scan
GitHub/HN/Reddit/vendor blogs for external patterns). Not LLM one-shot generated, not benchmark-trained.

**跨载体迁移**
跨模型 (multi-model debate: Claude + Gemini + Codex evaluate every proposal — explicit cross-model verification). 跨任务
(analyzes all session types: coding, debugging, research, config). 跨 agent harness: NO — Claude Code-specific (SKILL.md
format, ~/.claude/ layout); Gemini/Codex are debaters not targets. 跨用户/团队: NO — single-user personal workflow by design
(README 'adapted to my workflow'). 跨基准: NO.

**技能库治理**
doc_bloat治理 via experience stripping (AgentEvolver-inspired rule necessity test: rules unused for 4+ weeks →
STRIP_CANDIDATE) + memory consolidation (prune memories unreferenced 4+ weeks, merge redundant entries, promote
recurring patterns). No explicit Lotka-Volterra/retirement, no similarity-based skill dedup/merge, no hierarchical index
— skills are a flat directory. Tools registry (REGISTRY.md) has adoption-log tracking.

**失败记忆**
是 — Dedicated Agent 1 (Failure Analyst + Text Gradient Generator) extracts failure patterns with frequency, root cause,
and text gradient ('output was wrong BECAUSE tool X BECAUSE rule Y BECAUSE context W which no longer applies'). Concrete
error logs (input/expected/actual/error) feed the optimizer. Retrospective Evaluator (Agent 4) flags CONFIRMED_HARMFUL
past changes for rollback. DEFERRED proposals logged in scoreboard.jsonl as negative feedback to avoid repeating failed
directions. Tree's failure_branches field records degraded paths.

**编辑安全**
Multi-layered: (1) scope 边界 — operates only on ~/.claude/ config files, never touches user source code; (2) pre-edit
备份+回滚 — git commit after every cycle, ROLLBACK classification reverts CONFIRMED_HARMFUL changes; (3) 确认门控/人工在环 —
HIGH-IMPACT items require user review; (4) bounded edit policy in CLAUDE.md self-evolution protocol: 'Never remove an
existing rule without user confirmation; Never change execution style without user confirmation; Methodology changes
append, not overwrite'; (5) experience stripping NEVER auto-removes rules (always flags HIGH-IMPACT); (6) multi-model
debate as consensus gate (2/3 agreement required for auto-adopt). No explicit eval-hacking or secret-injection checks
documented.

**协同进化**
Rich multi-axis: skill-tool (Agent 6 detects repeated ad-hoc command patterns and promotes ephemeral scripts to
persistent skills; proposes new MCP servers — Live-SWE-agent ephemeral→persistent pipeline) + skill-skill ecosystem
(reflect-and-learn invokes gemini-agent and codex-agent skills; skills form a closed loop:
scan→propose→debate→adopt→verify) + generator-verifier 协同 (Claude generates proposals, Gemini+Codex verify via debate) +
skill-prompt 联合 (both CLAUDE.md prompts and SKILL.md skill files are co-edited). Not skill-only.

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (non-gradient text-space optimization via TextGrad-style text gradients on config) +
co_evolutionary (skill↔tool↔verifier co-evolution) + population_evolutionary elements (AFlow-inspired soft mixed
selection: 40% uniform exploration + 60% softmax-weighted exploitation over proposals; tree-structured lineage). NOT
reward-based RL, NOT imitation, NOT gradient/SFT. Debate-based verifier replaces scalar reward.

**学习信号来源**
自我反思 (6 parallel reflection agents on session logs) + 成败轨迹 (failure patterns, user corrections, abandoned tasks) +
LLM-as-judge (multi-model debate: Claude/Gemini/Codex score impact+risk) + 工具成功率指标 (efficiency auditor: tool-call
counts, token usage, time-to-completion) + 留出验证分 (retrospective evaluator re-scores past adoptions against subsequent
session data).

**奖励粒度**
hybrid — Explicit dual-channel scoring (AgentEvolver-inspired): Channel 1 PROCESS QUALITY (Evidence 3x + Generality 2x +
Simplicity 1x) + Channel 2 OUTCOME QUALITY (Impact 3x + Safety 2x + Text Gradient Strength 1x). Composite = 0.5*Process
+ 0.5*Outcome. Both process and outcome rewarded.

**学习范式**
sleep-time (weekly offline reflection at Wednesday 3:00am via cron/launchd, replays past week's session JSONL) + offline
(analyzes historical logs, not live) + on-policy-ish (reflects on the same agent's own sessions). Not online/intra-task.

#### 进化时机_When

**进化时机 (When)**
sleep-time (primary: weekly scheduled Wednesday 3am) + inter-test-time (manual trigger: user says
'reflect'/'self-improve'/'review workflows'/'evolve config', or after a rough session). NOT intra-test-time (does not
modify config during task execution).

**触发方式**
周期性 (cron/launchd weekly schedule: Mon=agentic-radar, Wed=reflect-and-learn, Fri=vendor-docs-radar) + 事件触发 (slash
command or natural-language trigger phrases in YAML description) + 失败触发 (author notes 'after a particularly rough
session where multiple things went wrong') + 使用驱动 (session JSONL mtime triggers analysis).

#### 存储与检索

**技能库结构**
技能文件目录 (~/.claude/skills/<name>/SKILL.md, flat one-folder-per-skill) + git history (commits after each cycle) + DAG/树状血脉
(evolution-history/evolution-tree.jsonl with parent_id→node_id lineage + success_branches/failure_branches +
scoreboard.jsonl per-change log). Reflections stored as dated Markdown in reflections/YYYY-MM-DD-reflection.md. No
vector DB, no cloud registry.

**检索/复用方式**
description 匹配触发加载 — YAML frontmatter 'description' field enumerates trigger phrases ('reflect', 'self-improve', 'review
my workflows', 'run reflection', 'evolve config', or weekly cron); Claude Code matches user input/schedule against these
to activate the skill. Skills invoke other skills by name (reflect-and-learn calls gemini-agent/codex-agent). No
semantic/vector retrieval, no BM25.

#### 验证与反馈

**验证方式**
LLM-judge (multi-model debate: Claude+Gemini+Codex independently score impact+risk 1-10) + validation gating
(P0/P1/HIGH-IMPACT/DEFER/ROLLBACK thresholds) + 多模型辩论 (2/3 consensus required for auto-adopt; divergence → flag for
user) + 留出评估/longitudinal (Retrospective Evaluator re-scores past adoptions against subsequent 2-4 weeks of session
data: CONFIRMED_HELPFUL/INCONCLUSIVE/CONFIRMED_HARMFUL). NOT execution-based on benchmarks — author explicitly notes no
controlled A/B results.

**错误纠正**
回滚 (ROLLBACK classification reverts CONFIRMED_HARMFUL changes via git) + 有界编辑 (bounded edits: append-not-overwrite for
methodology, never auto-remove rules) + 定向 diff 修补 (each adopted change is a specific targeted CLAUDE.md/skill diff with
rationale) + self-revision (meta-evolution Agent 5 proposes changes to the reflection process itself — hyper-evolution
of the mutator) + 重规划 (text gradient generates inverse edit from root cause).

#### 环境与基座

**测试环境**
真实生产力任务 — The author's own Claude Code sessions (coding, debugging, research, config, refactoring). NOT a controlled
benchmark; author explicitly: 'I don't have controlled A/B results yet' and 'Whether the reflection loop genuinely
compounds over months, or just feels like it does, is something I'm still figuring out.' No SkillsBench/GDPVal/SWE-bench
evaluation.

**底座模型**
Claude (primary optimizer AND primary target: reflect-and-learn runs on Claude Code, evolving Claude's own CLAUDE.md) +
Gemini (debater/verifier via gemini-agent skill, Gemini CLI) + Codex (debater/verifier via codex-agent skill, Codex
CLI). Optimizer/target are nominally the same model (Claude) but externally cross-checked by Gemini+Codex. Requires
GEMINI_API_KEY and OPENAI_API_KEY.

**部署域 (Where)**
specialized (coding) — Claude Code is a coding agent; skills operate on ~/.claude/ config for coding workflows. Within
coding, it is general-purpose (covers code generation, debugging, research, refactoring). Not deployed to
GUI/office/document/Web domains.

#### 评估指标

**评估指标**
成功率 (session success_rate tracked in evolution-tree.jsonl metrics) + skill_library_growth (changes adopted vs deferred
counts) + cost (~$5-10/month API for weekly multi-model debate; scouting uses mostly free-tier web search) + 回归率
(retrospective verdicts: CONFIRMED_HELPFUL/INCONCLUSIVE/CONFIRMED_HARMFUL ratios) + efficiency deltas (avg_tool_calls,
avg_tokens, user_corrections/confirmations tracked week-over-week). No sample_efficiency or economic-value-capture
metrics.

#### 局限与挑战

**局限与挑战**
regression_risk (acknowledged; mitigated by git tracking + rollback but author admits uncertainty whether gains
compound) + eval-hacking risk (self-evaluation without ground truth; multi-model debate mitigates but does not
eliminate) + transferability (Claude Code + ~/.claude layout specific; not portable to Cursor/Codex harness without
rebuild) + doc_bloat (addressed via experience stripping but author notes memory consolidation 'has needed the most
manual iteration') + controllability (open-ended personal workflow = 'honest measurement is harder') + optimizer_quality
(depends heavily on session-log quality, jq parsing, and LLM debate quality; Gemini/Codex optional — without them
multi-voice debate is lost) + scalability (single-user/single-agent scope; author notes 'the next conceptual step is
shared memory and coordination across agents' which is not yet built).

#### 可借鉴要点

**可借鉴要点**
- Multi-voice debate as a cheap, model-agnostic quality gate: have Claude (generator), Gemini, and Codex (verifiers) independently score every proposed config edit on impact+risk; auto-adopt only on 2/3 consensus, flag divergence for human review. This replaces a scalar reward with a disagreement signal that surfaces risky edits the generator would otherwise self-approve — directly portable to any SKILL.md self-edit loop without training.
- Tree-structured evolution history (AFlow-style JSONL: node_id + parent_id + per-change scores + retrospective verdicts + success/failure branches) is what enables intelligent backtracking instead of a random walk. Pair it with a weekly Retrospective Evaluator that re-scores past adoptions against subsequent session data (CONFIRMED_HELPFUL/HARMFUL) — this closes the loop from 'propose→adopt' to 'propose→adopt→verify→rollback' and is the single most important guard against config drift.
- Dual-channel scoring (process quality + outcome quality, each weighted: Evidence/Impact 3x, Generality/Safety 2x, Simplicity/Text-Gradient 1x) combined with experience stripping (rules unused for 4+ weeks become STRIP_CANDIDATEs, but NEVER auto-removed — always flagged HIGH-IMPACT) is the practical recipe for preventing doc bloat while keeping the SKILL.md/CLAUDE.md lean. The 'append, never overwrite; never remove a rule without user confirmation' protocol is the hard safety floor beneath the soft scoring.
- Sleep-time scheduling (cron/launchd, weekly, offline replay of session JSONL) decouples self-improvement from task execution — the agent evolves its config while the user sleeps, at ~$5-10/month API cost, with zero workflow interruption. This makes self-evolution economically viable for individual developers, not just labs.

#### 不确定字段

- paper_link
- key_results
- institution

---

### Homunculus nightly agent (/hm-night)

> `engineering_practice` · JavanC, 2026。夜间自主 agent：instinct harvest→将本能路由到最佳机制(hook/rule/skill/ script/agent)→skill eval(仅变更项)→health check。Evolution Tiers(Minimal/Standard/ Full)控制深度与预算(~$0.5~$10/night)。周日深度模式。阶段管线 P1进化/P2研究/P

#### 基础信息

**名称**
Homunculus nightly agent (/hm-night)

**发布时间**
2026 (v0.5.0 initial release Mar 2026; v0.6.3 evolution tiers Mar 2026; v0.11.0 cross-platform Apr 2026; v0.12.0
subscription profiles Jun 2026; latest v0.12.1 Jun 2026)

**代码链接**
https://github.com/JavanC/Homunculus (npm: https://www.npmjs.com/package/homunculus-code; install via `npx
homunculus-code init`). Key internals: docs/nightly-agent.md, commands/evolve.md, commands/improve-skill.md,
skills/{claude,cursor,codex,generic}/, examples/reference/.

**类型**
industry (open-source self-evolution framework/plugin) + blog_practice (validated on the author's own personal AI assistant over 5 weeks). Not academic.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能 + Architecture(单/多智能体). Evolves: behavioral 'instincts', skills (.md with eval specs), subagents,
hooks, path-scoped rules, automation scripts, MCP wiring, cron/launchd jobs, slash commands, and the goal tree
(architecture.yaml) + CLAUDE.md/AGENTS.md/memory. NOT model weights — purely the external runtime text/tool state of an
existing coding agent (Claude Code / Cursor / Codex CLI). Meta-evolution: the evolution mechanism itself is also tuned.

**技能是否独立制品**
Yes — skills are independent, reusable, versioned markdown artifacts: `homunculus/evolved/skills/*.md`
(agentskills.io-compatible), each paired with an eval spec in `homunculus/evolved/evals/`. Plus separate artifacts for
instincts (`homunculus/instincts/personal|archived/`), agents (`homunculus/evolved/agents/`), rules
(`.claude/rules/*.md`), commands (`.claude/commands/*.md`), and scripts (`homunculus/scripts/`). Forms: .md files + YAML
goal tree + shell/JS scripts.

**是否文档载体**
Yes (hybrid leaning yes). The core carrier of a 'skill' is a human-readable instruction markdown doc with YAML
frontmatter; instincts/rules/commands are also markdown. Skills additionally embed structured fields (frontmatter) and
reference external executable eval specs. Not pure code, not vector-only.

#### 技能表示

**技能编码方式**
技能文档 (.md / SKILL.md style). Agentskills.io-compatible markdown = YAML frontmatter (name, description, allowed-tools,
compatibility, metadata.author/version) + markdown body (Purpose/Steps/...). Instincts encoded as frontmatter-tagged
files (confidence_score, suggested_mechanism, goal_path, durability_score, supersedes). Goal tree encoded as
`architecture.yaml` (purpose/realized_by/health_check/metrics). Non-vector; file-system + git.

**技能粒度**
Mixed granularity across the stack: atomic patterns (instincts, ~single behavior) → policy rules (path-scoped rules) →
insights (memory/research suggestions) → full skill packs (skill .md + eval spec, a workflow). Same behavior migrates
granularity as it matures (instinct → rule → skill → hook).

#### SKILL.md_专属维度

**文档形态**
Structured fields: YAML frontmatter + markdown instruction body. Standard evolved-skill template: `---
name/description/allowed-tools/metadata(version,author) ---` + `# Skill: <Name>` + Version / Evolved-from / Purpose /
Steps / ... Multi-file package: a skill + its eval spec (+ optional agent). Typical length ~1–2k tokens for evolved
skills (e.g. the `homunculus.md` router skill is ~80 lines; reference skills grew to hundreds of lines).
Platform-specific copies live in skills/{claude,cursor,codex,generic}/.

**编辑粒度**
Bounded add/delete/replace (not whole-doc rewrite). `/improve-skill` analyzes FAIL/PARTIAL/GAP scenarios then makes
targeted edits: fix incorrect info / add missing rules / add a new section; bumps version +0.1 per round; max 5 rounds.
`/evolve` writes whole new small files when routing an instinct to a new mechanism. Git tracks every intermediate
version. Eval spec is never edited (tests stay fixed); only the skill file is edited.

**版本与门控**
Multi-layer: (1) validation gating — eval→improve loop until 100% pass, with 5pp noise tolerance, regression rollback,
and a Gaming Gate (score jump >5pp with ≤3 net new lines = gaming_suspected → revert); (2) multi-run eval
`--runs/--passes N` with majority vote to beat LLM-judge variance; (3) git versioning + per-edit version bump in
frontmatter; (4) Durability Gate (instincts with durability_score < 0.7 filtered); (5) staging — non-invasive
suggestions written to `homunculus/reports/` and `.new` files for customized commands; (6) `.bak` backup on upgrades;
(7) review-gated adopt — core behavior changes (hooks/rules/CLAUDE.md/file deletes/cron/deps) are NOT auto-applied, only
proposed as Suggested actions.

**文档来源**
session经验提取 (SessionEnd/PostToolUse observation hooks record tool usage → `evaluate-session.js` extracts
instincts/memory/research in one pass) + 成功轨迹归纳 (reinforced recurring patterns converge into skills) + 社区共享/外部研究
(nightly P2 scans tech news/changelogs/community with cross-night dedup). Write Gate requires an extraction to 'change
future behavior / capture a commitment / preserve a decision rationale'.

**跨载体迁移**
cross-agent-harness (explicit first-class: Claude Code ↔ Cursor ↔ Codex CLI; `init` auto-detects host and
`skills/{claude,cursor,codex,generic}/` ships the right format) + cross-model (multi-LLM harvest provider: claude-cli /
codex-cli / anthropic-api / openai-api, incl. Ollama/vLLM/OpenRouter) + cross-user (instincts under
`instincts/personal/`, per-user). Cross-task via goal-tree routing. Claims cross-platform but no quantitative transfer
metric is published.

**技能库治理**
层次化索引 (skills/agents/evals/instincts{personal,archived}/reports dirs + architecture.yaml goal tree) + 去重合并 (semantic
`supersedes` auto-archives older instincts; 2+ similar instincts → skill aggregation) + 灰尘清理/curator loop
(`prune-instincts.js`: reference-frequency scoring +25 used/−15 never used, 3-tier skill-coverage detection, 14-day
grace before confidence decay, at-risk warnings; archive-once-implemented) + retirement (archived/ dir; CLAUDE.md
coverage check avoids re-extracting already-implemented rules).

**失败记忆**
Partial. Failure signals are used as negative feedback: (1) Bash failure circuit breaker — `observe.sh` tracks last 10
failures for evolution analysis; (2) improve-skill regression detection marks previously-passing-now-failing scenarios
and rolls back; (3) Gaming Gate discards suspicious 'gaming_suspected' improvements; (4) cross-night research dedup
avoids re-proposing seen topics. But there is no dedicated anti-pattern / failure-signature+remedy store documented
(closer to a rejected-edit buffer pattern).

**编辑安全**
Layered: (1) scope boundary — `/improve-skill` only edits the skill file, never the eval spec, never application source
code; (2) pre-edit backup + rollback — `.bak` on upgrades, rollback to previous version on regression; (3)
anti-eval-hacking — Gaming Gate + multi-run majority vote; (4) confirmation gating — `/evolve` interactive mode asks for
manual confirmation (vs `--auto` for nightly); (5) human-in-the-loop — core behavior changes
(hooks/rules/CLAUDE.md/deletes/cron/deps) are proposed as Suggested actions, never auto-applied; (6) memory-safety —
nothing enters permanent memory without human review (Memory Flush queue); (7) durability/confidence decay filter
(90-day half-life); (8) bounded edits prevent destructive rewrites; (9) hook auth fallback queues failed extractions
instead of losing data.

**协同进化**
skill-tool ecosystem + generator-verifier + skill-skill. (a) Each behavior is routed to the best of 8 coexisting
mechanism types (hook/rule/skill/script/MCP/cron/command/agent), and a behavior upgrades across them as it matures
(rule→skill→hook) — a skill-tool ecosystem. (b) Generator-verifier: the skill (.md, generator of behavior) coevolves
with its eval spec (verifier, fixed); eval-discrimination meta-metric tunes the verifier. (c) Meta-evolution: the
evolution mechanism itself is tuned via 5 metrics (instinct_survival_rate, skill_convergence, eval_discrimination,
mechanism_coverage, compliance_rate).

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (non-gradient text-space: eval→improve→rollback loop on skill .md) + population_evolutionary-ish
(instincts are extracted, confidence-scored, deduped, durability-gated, converged into skills, archived once implemented
— a survival/routing dynamic) + imitation_demonstration (extract recurring patterns from observed user tool usage) +
meta-optimization (adjust the evolution knobs). No gradients, no SFT, no RL — all in text/markdown space.

**学习信号来源**
tool usage observations (PostToolUse hooks) + tool-success metrics (goal health_check commands, e.g. test pass count) +
LLM-as-judge (eval scenarios in eval specs) + self-reflection (three-layer extraction: instincts/memory/research in one
pass) + held-out-ish validation score (eval pass %, with discrimination tracking) + confidence reinforcement/decay
(90-day half-life) + reference frequency.

**奖励粒度**
Hybrid. Outcome: eval scenario pass/fail and goal health_check pass/fail. Process: instinct confidence
reinforcement/decay, reference-frequency scoring, per-phase pipeline tracking, and meta-metrics (convergence time,
survival rate).

**学习范式**
sleep-time (primary — nightly offline `/hm-night` pipeline) + inter-test-time (SessionEnd hook harvests instincts at
session boundary, streaming). Offline (replays observed sessions/observations). On-policy relative to the user's own
session. No intra-test-time learning during a live task.

#### 进化时机_When

**进化时机 (When)**
sleep-time (nightly agent, the headline mode) + inter-test-time (session-end instinct extraction). The live agent is observed but not mutated mid-task.

**触发方式**
Periodic (launchd on macOS / cron on Linux heartbeat — multi-tick, default nightly, weekly deep mode configurable day
default Sunday) + event-triggered (SessionEnd / PostToolUse / stop hooks → observation + extraction) + usage-driven
(hooks watch tool usage) + on-demand manual (`/hm-night`, `homunculus night`).

#### 存储与检索

**技能库结构**
技能文件目录 (file-system layout: `homunculus/evolved/{skills,agents,evals}/`, `homunculus/instincts/{personal,archived}/`,
`homunculus/experiments/`, `homunculus/reports/`, `.claude/{rules,commands}/`) + 层次化 (architecture.yaml goal tree as the
index/brain) + git (lineage via commits) + staging dirs. No vector DB, no graph, no cloud registry; agentskills.io
compatibility for portability.

**检索/复用方式**
description匹配触发加载 (agentskills.io-style: skill loaded on description-match by the host harness) + trigger-phrase routing
(the router skill `homunculus.md` maps natural-language/slash triggers like 'run evolution'/'hm-night' to command
workflow files) + reference-frequency tracking (which instincts/skills are actually read) + frequency/recurrence
detection for instinct harvesting. No semantic-vector retrieval documented.

#### 验证与反馈

**验证方式**
execution-based + LLM-judge (eval scenarios per skill) + functional correctness (goal health_check shell commands, e.g.
`test $(find logs/ -mtime -1 | wc -l) -gt 0`) + validation gating (100% pass required to keep a skill; <100% triggers
improve loop) + multi-run eval `--runs/--passes N` with majority vote + discrimination tracking (eval_discrimination
meta-metric: % of scenarios that actually distinguish versions). The optimizer never silently edits the eval spec (tests
stay fixed).

**错误纠正**
self-revision (eval→analyze FAIL/PARTIAL/GAP→targeted edit→re-eval, max 5 rounds) + rollback (regression → rollback to
previous version) + bounded edits + directed diff patch (add missing rules / add new section / fix incorrect info) +
circuit breaker (stops pipeline after consecutive failures) + archive (prune/archive outdated instincts once absorbed).

#### 环境与基座

**测试环境**
通用 / real productivity tasks. Validated on the author's own real personal AI assistant (5-week longitudinal run), not a
controlled academic benchmark. Domain = coding/productivity via Claude Code / Cursor / Codex CLI.

**底座模型**
Claude (default harvest via `claude --print`, Sonnet-class). Multi-LLM harvest provider is configurable: claude-cli /
codex-cli / anthropic-api / openai-api (incl. Ollama / vLLM / OpenRouter). No strict optimizer/target split like
SkillOpt-Sleep, but the harvest model is configurable via `HOMUNCULUS_HARVEST_MODEL`/`HOMUNCULUS_HARVEST_PROVIDER`, and
subscription profiles (Pro/Max5x/Max20x/API) gate Opus use (planning/review only at full tier).

**部署域 (Where)**
specialized — coding / productivity agent domain (Claude Code, Cursor, Codex CLI coding assistants). Adapts the agent to
the user's own project + workflow + goals.

#### 评估指标

**评估指标**
skill_library_growth (the headline: counts of instincts/skills/agents/hooks/scripts/commands/rules/ADRs/commits) + cost
(~$0.5/night minimal, ~$2-3 standard, ~$5-10 full; subscription users tracked via 5-hour session & weekly utilization,
not $) + success_rate (eval 100% pass) + generalization (cross-platform) + 5 meta-evolution metrics
(instinct_survival_rate, skill_convergence, eval_discrimination, mechanism_coverage, compliance_rate) +
regression/gaming counts. No formal accuracy-style benchmark.

#### 局限与挑战

**局限与挑战**
scalability (proven on one personal assistant, N=1; no multi-user/team evidence) + controllability (autonomy is
deliberately bounded — core changes need approval, so not fully hands-off) + eval-hacking/regression risk (mitigated by
Gaming Gate + rollback + multi-run vote, but LLM-judge variance remains; discrimination tracked but not eliminated) +
doc_bloat risk (mitigated by pruning/archival + Write Gate + durability filter) + optimizer_quality (depends on a
capable harvest model; weak models flaky) + cost/budget (real nightly spend; Pro tier is minimal-only) + observability
(anecdotal metrics, no standardized eval suite) + macOS/Linux only (no Windows).

#### 可借鉴要点

**可借鉴要点**
- Stable Goal Tree (architecture.yaml: purpose/metrics/health_check per node) as the optimization target, with REPLACEABLE implementations (skill/rule/hook/script/agent/MCP/cron/command) routed per behavior and upgraded as they mature (instinct→rule→skill→hook). This decouples 'what to improve' (goal health + metrics) from 'how to improve' (mechanism routing + eval→improve loop), enabling GLOBAL optimization toward user-defined goals rather than local pattern memorization — the single most portable idea for a self-evolving SKILL.md.
- Instinct lifecycle + multi-mechanism routing as a library-governance engine: extract confidence-scored instincts (90-day half-life), semantically dedup (supersedes), durability-gate (<0.7), prune by reference-frequency (+25/−15), and archive-once-absorbed; route the survivors to the cheapest correct mechanism. This directly attacks doc_bloat/regression and keeps each behavior in its optimal carrier (deterministic→hook, path-scoped→rule, reusable→skill+eval). Pair with a generator-verifier coevolve (skill .md vs fixed eval spec) + 5 meta-metrics to evolve the evolution mechanism itself.
- Tiered, budget-aware, review-gated nightly pipeline that nails the autonomy/safety balance for self-editing instruction docs: phase-based multi-tick heartbeat (P1 Evolution → P2 Research w/ cross-night dedup → P3 Experiments in isolated worktrees → P4 Sync) + circuit breaker + budget tiers (~$0.5–$10/night) + weekly deep mode. Safe ops (extract/archive/eval/improve/report) run autonomously while core behavior changes are surfaced as human-approve Suggested actions in a morning report — a directly-usable template for sleep-time self-evolution with a human in the loop.

#### 不确定字段

- paper_link
- institution
- key_results

---

### Skill Evolver (nomadically.work)

> `engineering_practice` · Vadim, 2026。六 agent 自改进 pipeline 的第三个 agent，专责编辑指令文件：CAN edit .claude/skills/*/SKILL.md, .claude/commands/*.md, .claude/hooks/*.py, CLAUDE.md, memory files；不能碰应用源码(爆炸半径限制)。基于 JSON 失败报告做 evidence-based

#### 基础信息

**名称**
Skill Evolver (nomadically.work)

**提出机构**
nomadically.work (author: Vadim Nicolai, Senior Software Engineer)

**发布时间**
2026-02-25

**类型**
blog_practice

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 — evolves Markdown instruction artifacts only: .claude/skills/*/SKILL.md, .claude/commands/*.md,
.claude/hooks/*.py, CLAUDE.md, OPTIMIZATION-STRATEGY.md, and auto-memory files. Explicitly NOT model weights, NOT
application source code (Code Improver handles that), NOT tools.

**技能是否独立制品**
Yes — skills exist as independent reusable artifacts: SKILL.md files, command .md files, hook .py files, CLAUDE.md, and
memory files. Multi-file skill package form (.claude/skills/*/SKILL.md + sibling files).

**是否文档载体**
Yes — the core carrier is human-readable Markdown instruction documents; the agent's entire editable surface is doc/prompt/memory files.

#### 技能表示

**技能编码方式**
技能文档(.md/SKILL.md) as primary carrier, plus CLAUDE.md (global instructions), .claude/commands/*.md (command docs),
.claude/hooks/*.py (executable hook code, but treated as in-scope instruction artifacts), and auto-memory files.
Structured EVOLUTION records encode proposed edits as JSON objects.

**技能粒度**
策略规则 / insight — edits target individual instructions, clarifications, and rules within skill files; each EVOLUTION
targets a specific failure mode (hallucination, wrong_tool, out_of_role).

#### SKILL.md_专属维度

**文档形态**
Structured fields + Markdown body. The editable artifacts are Markdown instruction files. Proposed edits are encoded as
structured EVOLUTION objects with fields: id, target_file, trigger_patterns, trigger_findings, change_type
(add_instruction|clarify_instruction|remove_instruction|...), before (exact text), after (new text), rationale,
expected_impact{dimensions, magnitude: small|medium|large, regression_risk: none|low|medium|high}. Anti-patterns are
documented inline in the skill file. Token length not specified, but instruction-bloat anti-pattern implies a soft size
ceiling beyond which agents may truncate/skip instructions.

**编辑粒度**
Minimal diff / bounded add-delete-replace. Apply Changes priorities: (1) minimal diff — change as little as possible;
(2) additive over destructive; (3) specific over general; (4) testable. Edits use exact before/after text replacement.
Hard cap of 5 evolutions per run. Each edit must link to trigger_patterns or trigger_findings (frequency >= 2 threshold
inherited from Trajectory Miner). No whole-document rewrite unless justified.

**版本与门控**
Validation gating (held-out Verification Gate) + rejected-edit feedback loop. Every edit passes a mandatory Verification
Gate that checks: coherence (do modified skill files still make internal sense?), cross-skill conflicts, CLAUDE.md
consistency, and hook fail-open preservation. If rejected, the Meta-Optimizer records the failure and adjusts future
priorities. No explicit git-branch/Pareto/DAG versioning mentioned.

**文档来源**
失败轨迹蒸馏 + session 经验提取. Edits are evidence-based, driven by JSON failure/pattern reports produced upstream by the
Trajectory Miner (failure signatures with frequency >= 2). No LLM one-shot generation, no offline benchmark training;
provenance is always a mined failure trajectory linked via trigger_patterns/trigger_findings.

**技能库治理**
灰尘清理 (curator-style anti-bloat) + conflict detection. Explicitly governed by 5 anti-patterns: (1) instruction bloat —
sometimes simplify rather than add, watch file-size growth; (2) contradictory instructions — must check conflicts before
writing; (3) over-specificity — frequency >= 2 threshold forbids one-off patches; (4) prompt-engineering theater — avoid
'IMPORTANT:'/'CRITICAL:' spam; (5) cargo cult — don't copy research patterns without context. Verification Gate performs
cross-skill checks. No Lotka-Volterra/retirement/archive or hierarchical index mentioned.

**失败记忆**
Yes — strong negative-feedback memory. (a) 5 documented anti-patterns act as rejected-edit-direction vetoes; (b) every
EVOLUTION must reference trigger_patterns/trigger_findings (failure signatures + attribution + remedy); (c)
CASTER-style: acts ONLY when scores drop (fixes failures, never optimizes what works); (d) Meta-Optimizer records each
Gate-rejected evolution and down-weights that edit class going forward, forming a pipeline-level rejected-edit buffer.

**编辑安全**
Highly detailed — this is the headline design dimension. SCOPE BOUNDARY (single most important decision): CAN edit only
instruction files (.claude/skills/*/SKILL.md, .claude/commands/*.md, .claude/hooks/*.py, CLAUDE.md,
OPTIMIZATION-STRATEGY.md, auto-memory); CANNOT edit application source code, schema files, config files, generated
files. Rationale: an agent that can modify both its own instructions AND the codebase has unbounded blast radius;
restricting to Markdown means worst case = a bad prompt, caught by the Verification Gate (EvoConfig-style scoped
modification). BOUNDED EDITS: max 5 evolutions per run. EVIDENCE GATING: every change must link to trigger_patterns or
trigger_findings; no 'improvements based on vibes'. MANDATORY SELF-QUESTIONING before any edit (5 questions incl. 'Is
there a simpler fix, e.g. one line in CLAUDE.md?'). ANTI-PATTERN AWARENESS (5 anti-patterns above). VERIFICATION GATE
(coherence + cross-skill + CLAUDE.md consistency + hook fail-open preservation). REGRESSION-RISK ASSESSMENT per edit
(none|low|medium|high). NO explicit pre-edit git backup/rollback mentioned, but the bounded scope + Gate serve the same
protective role.

**协同进化**
Generator-verifier 协同 + skill-prompt 联合. The Skill Evolver is the 3rd of 6 pipeline agents: Trajectory Miner (1st) feeds
it failure reports; it edits instruction docs; Verification Gate validates; Meta-Optimizer (strategic brain) records
outcomes and adjusts priorities. It co-edits the global prompt (CLAUDE.md / OPTIMIZATION-STRATEGY.md) alongside granular
skill files, so prompt and skill evolve jointly. Skills are consumed by all downstream agents, so a skill edit
implicitly co-evolves agent behavior.

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (non-gradient, text-space prompt editing) + reward-based via negative textual feedback. No
SFT/RL/gradients. Combines Meta Context Engineering's observe→diagnose→modify→observe loop, CASTER's negative-feedback
convergence, and REprompt's requirements-guided generation. Optimization happens entirely in the Markdown instruction
space.

**学习信号来源**
成败轨迹 (JSON failure reports from Trajectory Miner) + LLM-judge / self-reflection (mandatory self-questioning) +
verification signals (Verification Gate accept/reject recorded by Meta-Optimizer). expected_impact.dimensions provide a
requirements spec checked against actual score deltas.

**奖励粒度**
Outcome (结果) — triggered by task-level score drops and discrete failure-pattern frequencies; each evolution targets a
specific failure mode rather than step-level process rewards.

**学习范式**
Offline + inter-test-time (between task runs). Operates as a distinct pipeline stage consuming previously-mined failure
reports, not intra-task online. On-policy relative to the current skill version (edits the live instruction set).

#### 进化时机_When

**进化时机 (When)**
inter-test-time (between task runs, as a dedicated pipeline stage) — processes failure reports produced by the preceding
Trajectory Miner stage and feeds the Verification Gate. Not intra-test-time online editing; not sleep-time batch replay
(though it runs periodically per pipeline cycle).

**触发方式**
事件触发 / 失败触发 + 使用驱动. Acts only when scores drop or when the Trajectory Miner surfaces a failure pattern with frequency >=
2. Bounded to max 5 evolutions per run. A single bad session does NOT justify an edit (frequency gate).

#### 存储与检索

**技能库结构**
技能文件目录 — filesystem directory layout: .claude/skills/*/SKILL.md (per-skill), .claude/commands/*.md (command docs),
.claude/hooks/*.py (hooks), CLAUDE.md (global), OPTIMIZATION-STRATEGY.md (strategy), auto-memory files. Flat per-domain
directory under .claude/; no vector store / DAG / cloud registry.

#### 验证与反馈

**验证方式**
validation gating (held-out Verification Gate) + LLM-judge-style coherence checks + functional correctness checks. Gate
performs: (1) coherence — do modified skill files still make internal sense?; (2) cross-skill check — conflicts with
other skills?; (3) consistency check — are CLAUDE.md changes consistent?; (4) hook verification — do hook modifications
preserve fail-open design? Also verifies expected_impact.dimensions against actual score movement. Rejected evolutions
are logged by the Meta-Optimizer.

**错误纠正**
有界编辑 (bounded edits, max 5/run) + 定向 diff 修补 (exact before/after text replacement, minimal-diff priority, additive over
destructive) + pipeline-level 回滚 via Gate rejection (Meta-Optimizer down-weights the failed edit class). No file-level
git rollback mentioned; correction is preventive (self-questioning + anti-patterns) and gate-based rather than post-hoc
rollback.

#### 环境与基座

**测试环境**
真实生产力任务 — the nomadically.work product (remote EU job classification). Post-dates the original generic Skill Evolver:
implementation later specialized into a goal-driven 'Classifier Tuner' targeting false-negative reduction in remote EU
job classification.

**底座模型**
Claude (implied by the .claude/ harness, CLAUDE.md, .claude/skills, and Claude Code conventions). Optimizer/target
separation: the Skill Evolver (optimizer agent) edits instruction files consumed by other target agents; both run on the
same Claude backbone. Exact model variant not specified.

**部署域 (Where)**
Specialized (job-posting classification / remote-EU-job filtering domain via nomadically.work). Originally
general-purpose instruction editing, later specialized to the classifier-tuning goal.

#### 评估指标

**评估指标**
success_rate (task scores, the drop of which triggers evolution) + 回归率/regression_risk (per-edit rating
none|low|medium|high, Gate checks for regressions in other dimensions) + generalization (anti-over-specificity gate,
frequency>=2) + cost-adjacent (bounded edits, max 5/run). expected_impact.magnitude (small|medium|large) is a
self-declared effect-size estimate verified by the Gate.

#### 局限与挑战

**局限与挑战**
doc_bloat (instruction bloat — primary anti-pattern; files may grow until agents truncate/skip) + regression_risk (Gate
exists precisely because edits can regress other dimensions; rated per edit) + eval-hacking risk (prompt-engineering
theater anti-pattern — overusing IMPORTANT/Critical markers; addressed by 'be precise instead') + controllability
(relies on a strong optimizer backbone; cargo-cult anti-pattern warns against copying patterns without understanding) +
transferability (scope confined to one product pipeline; cross-model/cross-harness transfer not demonstrated).
Catastrophic forgetting less relevant (no weight training) but 'contradictory instructions' anti-pattern is its
doc-space analogue.

#### 可借鉴要点

**可借鉴要点**
- SCOPE BOUNDARY IS THE #1 SAFETY DECISION — restrict the instruction-editing agent to Markdown/instruction files ONLY (cannot touch application source code, schema, config, generated files). Rationale: an agent that can modify both its own instructions AND the codebase has unbounded blast radius; confining edits to Markdown means the worst case is a bad prompt, which a Verification Gate can catch. This single rule converts 'terrifying self-modification' into 'boring, bounded self-improvement'. Directly portable to any SKILL.md-evolver: define an explicit CAN-edit / CANNOT-edit manifest (EvoConfig-style).
- EVIDENCE-GATED EDITS + MANDATORY SELF-QUESTIONING FORCES THE SIMPLEST INTERVENTION — every proposed edit must reference a concrete failure signature (trigger_patterns/trigger_findings with frequency >= 2), and a mandatory pre-edit self-questioning step asks 'Is there a simpler fix — e.g. one line in CLAUDE.md before rewriting a whole skill file?'. This prevents the single most common failure mode of instruction-evolvers: rewriting entire skill files when a one-line global prompt tweak would suffice. Combine a hard evidence requirement with a 'simplest-first' self-question to keep edits minimal and explainable.
- NEGATIVE-FEEDBACK MEMORY AS ANTI-PATTERN VETO + GENERATOR-VERIFIER COEVOLUTION — act ONLY when scores drop (CASTER-style: failures are more informative than successes), and codify the recurring failure modes of the editor itself as explicit anti-patterns (instruction bloat, contradictory instructions, over-specificity, prompt-engineering theater, cargo cult) that serve as a rejected-edit-direction buffer. Pair the editor with an independent Verification Gate (coherence / cross-skill / consistency / fail-open checks) whose rejections feed back into a Meta-Optimizer that down-weights failed edit classes — closing a generator-verifier coevolution loop that learns which kinds of skill changes actually work.

#### 不确定字段

- paper_link
- code_link
- cross_transfer
- retrieval_method
- key_results

---

### venotyh/evoskill (evolutionary skill agent)

> `engineering_practice` · 2026。把 AI agent skill 当作可进化 genome。idle/sleep 期跑世代进化：select 最优→ mutate(prompt/instructions/tools/parameters，含 guided55%/random25%/crossover20%)→ evaluate fitness(LLM-as-judge 80%+结构分 20%)→prune。Lineag

#### 基础信息

**名称**
evoskill (venotyh/evoskill) — Evolutionary Skill Agent

**提出机构**
Independent / community author (GitHub user 'venotyh'). No affiliated institution; a personal/experimental open-source
project (1 star, 8 commits, Python). README self-deprecatingly opens with '# No!!! This project is absolute bullshit.'

**发布时间**
2026 (repo activity ~2026-05; CHANGELOG 'Unreleased' section; no tagged release/version tags published).

**代码链接**
https://github.com/venotyh/evoskill

**类型**
blog_practice / industry (small open-source experimental CLI tool, pip-installable via `pip install -e .`). Not an
academic paper. Unrelated to and predates/confuses naming with sentient-agi/EvoSkill (arXiv:2603.02766) despite the
identical command name `evoskill`.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能. The evolvable object is the Skill GENOME = system_prompt (str) + instructions (list[str]) +
tool_bindings (list[str]) + parameters (dict), defined in core/genome.py:SkillGenome. Model weights are FROZEN;
single-agent architecture is fixed. Tools themselves are a fixed built-in set (read_file, write_file, shell_exec,
web_search, search_files) — only their BINDINGS (which tools a skill uses) evolve, not the tool implementations.

**技能是否独立制品**
是. Each skill is an independent reusable artifact, but NOT as a markdown file — it is a serialized dataclass persisted
as JSON under ~/.evoskill/ (storage.py: save_skill/list_skills/load_skill/delete_skill). Artifact form = JSON record
{id, name, genome{system_prompt,instructions,tool_bindings,parameters}, parent_ids, generation, fitness,
fitness_history, mutation_type, mutation_desc, created_at, task_count}. No skill folder, no helper scripts, no SKILL.md
— pure structured data.

**是否文档载体**
否 (pure structured data, not a readable instruction document). The skill's 'instructions' live as a list of short
strings inside a JSON-serialized dataclass; there is NO markdown/SKILL.md instruction file. At agent run-time the genome
is flattened into the LLM system prompt (system_prompt + '\n\nKey instructions:\n- ...') — the document only exists
ephemerally in the LLM context, never materialized as a .md artifact on disk. (Note: a .claude/skills/ directory exists
in the repo tree but is empty — no SKILL.md is ever written there.)

#### 技能表示

**技能编码方式**
结构化字段(dataclass -> JSON) + 自然语言SOP (instructions list). SkillGenome is a Python @dataclass with 4 typed fields
(system_prompt:str, instructions:list[str], tool_bindings:list[str], parameters:dict), serialized to/from JSON dicts via
to_dict/from_dict. The agent runtime reassembles these into an LLM system message. No vector embedding, no graph, no .md
file, no multi-file package.

**技能粒度**
策略规则 / 完整技能包. Each skill encodes a complete agent persona/strategy (a system prompt + a handful of behavioral rules + a
tool subset + sampling params) — coarser than an atomic action, finer than a multi-agent workflow. The seed skill
carries 4 generic instructions; evolved skills carry 2-10 short actionable rules. granularity ≈ 'whole-agent
configuration as one genome'.

#### SKILL.md_专属维度

**文档形态**
JSON-serialized dataclass (NOT a document). Concrete shape per skill: {system_prompt: <2-5 sentence str>, instructions:
[<short actionable rule>, ...] (≤10 items, ~10-15 tokens each), tool_bindings: [<tool name>, ...] (subset of 5
built-ins), parameters: {temperature: 0.1-1.0, max_tool_calls: int, verbose: bool}}. Persisted as one JSON object per
skill in ~/.evoskill/ (data_dir). No YAML frontmatter, no markdown body, no code blocks. Typical token length of an
assembled system message (prompt + instructions) ≈ 100-300 tokens [estimated; no explicit cap beyond max_tokens=2048 on
agent calls and instructions capped at 10 items].

**编辑粒度**
整字段重写 + 有界增删替换 (field-level, not whole-document). Mutation operators target specific genome fields: (a) mutate_guided
rewrites system_prompt and/or replaces the entire instructions list wholesale (LLM emits new SYSTEM_PROMPT +
INSTRUCTIONS sections, parsed by _apply_guided_response); (b) mutate_prompt either replaces system_prompt, replaces
instructions, or appends one instruction; (c) mutate_tools adds or drops one tool binding; (d) mutate_params nudges one
numeric parameter; (e) crossover recombines fields from two parents (system_prompt from one parent, instructions
interleaved, tool_bindings unioned, params per-key random pick). NO minimal-diff/PATCH, no line-level edits — smallest
unit is one field.

**版本与门控**
DAG血脉 (for tracking/query only) + 生成代际剪枝 (generational pruning, NOT held-out validation). Each generation: population +
children merged, sorted by fitness, truncated to population_size (default 10) — weakest are pruned (save_skill persists
children but the active population is the top-N). Elitism: top-2 elites get extra deep evaluation (max_tasks=3) if
task_count<6. Lineage DAG records parent_ids/generation/mutation for every skill (queryable ancestors/descendants), but
it is descriptive bookkeeping, NOT an admission gate. There is NO held-out train/val split, NO git branching, NO Pareto
frontier, NO review-gate, NO staging+backup — admission is purely by in-sample fitness on the same 10 built-in tasks.

**文档来源**
人工初始化 + LLM一次性生成. The primordial seed skill is hand-authored (core/skill.py:create_seed_skill — fixed generic persona).
All descendants are produced by LLM-guided operators (mutate_guided asks an LLM for an 'improved version' with zero
failure context) or by random structural mutation (add/remove instruction, tweak prompt suffix, tune param). No
failure-trace distillation, no trajectory replay, no session-experience extraction — guided mutation is context-free
single-shot LLM rewriting.

**技能库治理**
生成代际剪枝 (generational pruning / implicit retirement of weakest). Each generation merges population+children and keeps
only top population_size by fitness — bounded library size by construction. Tournament selection (k=3) picks parents. NO
explicit dedup/merge, NO similarity-retrieval-edit-targeting, NO curator loop, NO Lotka-Volterra/archival dynamics.
Mutation diversity is maintained stochastically (25% random mutation) rather than by governance. All persisted skills
accumulate in ~/.evoskill/ JSON store even after being evicted from the active population (only the in-memory population
is pruned, disk records grow monotonically — potential unbounded disk growth across long sleep runs).

**失败记忆**
否 (no anti-pattern / rejected-edit / failure-signature memory). Fitness history is tracked per skill (fitness_history
list + running average) but is used only for ranking, never fed back as negative signal. The guided-mutation prompt
(_build_guided_mutation_prompt) shows the LLM only the CURRENT genome — no past failures, no rejected mutations, no
anti-patterns. There is no feedback_history, no related-iterations reference, no rejected-edit buffer. A mutation that
lowers fitness is silently pruned next generation with no recorded rationale surfaced to future mutations.

**编辑安全**
沙箱执行 (sandboxed tool execution) is the PRIMARY guardrail. (a) SkillAgent.run executes ALL tool calls (file ops,
shell_exec, web_search) inside a tempfile.TemporaryDirectory(prefix='evoskill_') with os.chdir into it and auto-cleanup
on exit — shell commands and file writes cannot touch the real filesystem. (b) MAX_TOOL_ROUNDS=8 caps agent loop length
(returns success=False on exhaustion). (c) max_tool_calls parameter per genome bounds tool use. NO pre-edit
backup/rollback (JSON overwrite in place), NO git isolation, NO held-out validation to detect eval-hacking/overfitting,
NO human-in-the-loop, NO scope boundary on which genome fields may be edited, NO secret/injection scanning, NO
bounded-edit protection against destructive prompt rewrites (guided mutation can replace the entire system_prompt). API
keys are masked in `config show` output and .mcp.json is gitignored (secret hygiene at config layer only).

**协同进化**
skill-only + skill-prompt 联合 + skill-tool-binding (weak). The genome jointly evolves system_prompt AND instructions AND
tool_bindings AND parameters as one atomic unit, so it is skill-prompt coevolution by construction (all four fields
mutate together). Tool BINDINGS co-evolve (add/drop tools) but the tools themselves are fixed built-ins — not skill-tool
coevolution in the strong sense. No skill-skill ecological interaction (skills compete only via ranking, do not
invoke/reference each other), no generator-verifier coevolution, no separate verifier evolution (the judge LLM is the
same model as the agent/mutator).

#### 自进化机制_How

**进化方法范式 (How)**
population_evolutionary + reward-based (LLM-as-judge). Classic generational evolutionary loop: initialize_population ->
tournament-select parents (k=3) -> create children via weighted mutation portfolio -> evaluate fitness ->
merge+sort+prune to population_size -> next generation. Mutation portfolio (engine.py:_create_child): Crossover 20%
(two-parent recombination), Guided mutation = guided_weight (default 55%, LLM rewrites prompt), Random mutation =
remainder 25% (uniform over prompt_mutate/tool_add-drop/param_tune). Elitism: top-2 survivors get deeper re-evaluation.
No gradient/SFT/RL — weights frozen, pure text-space evolutionary search over genome fields.

**学习信号来源**
LLM-as-judge + 工具成功率指标 (structural). Fitness = 0.8 * judge_score + 0.2 * structural_score
(fitness.py:_score_single_task). Judge: a separate LLM call scores agent output 1-10 against a strict rubric with a
reference_answer_hint. Structural: base 5.0, -2.0 if agent failed (max rounds / no output), +1.0 if output>20 chars, +
up to 2.0 for overlap between expected_tools and tools actually used. No environment reward, no self-reflection, no
held-out score, no human feedback.

**奖励粒度**
outcome (结果). Per-task scalar score 1-10, averaged over a random sample of tasks (quick_fitness uses num_tasks=2 for
children, evaluate_skill uses max_tasks=3-5 for elites). No process/step-level reward; the only intra-run signal is the
binary success flag (did the agent finish within MAX_TOOL_ROUNDS without a tool_calls-free turn).

**学习范式**
offline + sleep-time + on-policy. Evolution runs as an offline batch process (not during live user task execution).
Explicit 'sleep mode' (simulator.py:SleepSimulator, `evoskill sleep` CLI) is designed to run generational cycles during
idle periods (idle_seconds threshold, though the implementation notes it 'doesn't actually block — just notes it').
On-policy: each candidate is scored by actually instantiating a fresh SkillAgent and running it against the frozen LLM.
No off-policy replay buffer, no experience replay.

#### 进化时机_When

**进化时机 (When)**
sleep-time (夜间/空闲离线) + inter-test-time (manual batch). The headline framing is sleep-time simulation ('skills that
breed, mutate, and improve through sleep-time simulation'). Two entry points: (1) `evoskill evolve -g N` runs N
generations synchronously on demand (inter-test-time batch); (2) `evoskill sleep -g N` runs the SleepSimulator loop
intended for idle periods. No intra-test-time evolution (the agent does not self-edit during a live task).

**触发方式**
周期性 (generation loop) + 手动 (CLI) + 空闲触发 (idle threshold, nominal). `evolve` is manual on-demand; `sleep` runs a fixed
max_generations loop with a nominal idle_seconds gate (checked but not enforced — code comment: 'Don't actually block —
just note it'). No failure-triggered evolution, no cron/launchd scheduler integration, no curriculum driver, no
usage-driven trigger, no tool-degradation trigger. Trigger model = 'user starts a bounded generation loop'.

#### 存储与检索

**技能库结构**
DAG血脉 + 扁平 (flat JSON store). All skills persisted as individual JSON records in ~/.evoskill/ (flat directory,
storage.py). LineageTree (evolution/lineage.py) builds an in-memory DAG from parent_ids with a pre-built _children index
and _roots list; lineage.json stores the node map. NOT git branches, NOT a vector store, NOT a hierarchical directory,
NOT a cloud registry. The DAG supports ancestors/descendants/children/by_generation queries and ASCII tree rendering.

**检索/复用方式**
排序选择 (rank-based selection) + tournament. For task execution (`evoskill run`): list all skills, sort by fitness
descending, pick skills[0]. For parent selection: tournament selection (sample k=3, pick best, dedupe). NO semantic
similarity, NO embeddings, NO BM25, NO description-matching, NO generation-as-retrieval — retrieval is pure
fitness-ranked truncation. The 'best skill' is simply the highest-fitness JSON record.

#### 验证与反馈

**验证方式**
执行验证(execution-based) + LLM-judge. Each candidate skill is validated by actually running the SkillAgent against sampled
built-in tasks (real LLM calls + real sandboxed tool execution) and scoring the output with an LLM-as-judge rubric
(1-10) blended with structural heuristics. No held-out validation set, no surrogate verifier, no multi-model debate, no
formal functional-correctness check beyond the judge's subjective scoring. The 10 built-in tasks (core/tasks.py) are the
sole validation surface (file_summary, web_research, shell_investigation, logical_reasoning, code_explain, error_debug,
data_processing, search_organize, planning_task, system_analysis).

**错误纠正**
剪枝淘汰 (pruning) — the ONLY correction mechanism. Low-fitness children are evicted from the active population each
generation; no self-revision, no rollback (JSON overwrite, no history beyond fitness_history), no bounded-edit retry, no
targeted diff repair, no replanning. A bad mutation is simply discarded and the parent survives; the next generation may
stochastically produce a better child. Guided-mutation parse failures degrade gracefully (fall back to appending
response[:500] to system_prompt or to local structural mutation) but are not 'corrected' in a learned sense.

#### 环境与基座

**测试环境**
通用 (general-purpose toy tasks). 10 hand-authored built-in tasks across categories: tool_use (file_summary,
shell_investigation, search_organize, system_analysis), multi_step (web_research, code_explain, data_processing,
planning_task), reasoning (logical_reasoning, error_debug). NOT a standard benchmark (no SWE-bench, no SkillsBench, no
GDPVal, no Minecraft/Web/GUI environment) — synthetic mini-tasks exercising file/shell/search tools and basic reasoning.

**底座模型**
Claude / GPT / 开源LLM (multi-provider via unified LLMClient). Supports Anthropic (default claude-sonnet-4-20250514),
OpenAI (default gpt-4o), DeepSeek (default deepseek-v4-flash). Provider auto-detected from model name prefix; also
exposes an OpenAI-compatible local gateway (`evoskill gateway`). NO optimizer/target separation — the SAME configured
model is used for (a) the target agent being evaluated, (b) the guided-mutation operator, and (c) the LLM-as-judge
scorer. Weights frozen throughout.

**部署域 (Where)**
general (通用). A general-purpose agent-skill evolution toy: not specialized to coding/GUI/office/document domains. Tasks
span file ops, shell, web search, logic puzzles, code explanation — a horizontal 'make a generic assistant better at
misc tasks' framing. Deployment artifact = the best-fitness skill genome (JSON) loaded by `evoskill run` to handle an
arbitrary piped-in task.

#### 评估指标

**评估指标**
success_rate (fitness score 1-10) + skill_library_growth (total_skills, max_generation, roots count via lineage.stats())
+ best_fitness/avg_fitness trend per generation. SleepSimulator prints a generation-by-generation fitness trend bar
chart and a final delta (improved/unchanged/decreased). NO generalization metric, NO sample-efficiency tracking, NO
cost/token accounting, NO economic-value capture, NO regression-rate monitoring across runs. Mutation distribution
(counts per MutationType) is reported as a library statistic.

#### 局限与挑战

**局限与挑战**
scalability (toy 10-task suite; small population_size=10; in-sample fitness only) + eval-hacking / overfitting (judge
LLM scores the SAME 10 tasks used to drive selection — no held-out split; the judge is the same model as the
agent/mutator, risking confirmation bias and reward hacking) + regression_risk (NO validation gating; a 'fitter' child
may be overfit to the 10 tasks and regress on real work; no rollback) + optimizer_quality (guided mutation is
context-free single-shot LLM rewrite with no failure analysis; quality fully depends on the configured model;
DeepSeek/gpt-4o may behave very differently) + doc_bloat N/A (JSON genome, not prose) + transferability (untested;
structural portability assumed but not benchmarked) + unbounded disk growth (all children persisted forever even after
eviction from active population) + catastrophic_forgetting N/A (weights frozen) + controllability (fully autonomous
loop, no human-in-the-loop, no scope limits on prompt rewrites). Project self-describes as experimental/low-quality.

#### 可借鉴要点

**可借鉴要点**
(1) Skill-as-typed-GENOME (system_prompt + instructions[] + tool_bindings[] + parameters{}) rather than
skill-as-markdown-document: encoding the evolvable skill as a small structured dataclass with named typed fields lets
each evolutionary operator target a SPECIFIC field (mutate_prompt / mutate_tools / mutate_params / crossover), yielding
a clean, type-safe mutation space that is far easier to reason about and serialize than free-form markdown diffs. This
is the single most portable idea — any SKILL.md self-evolution system can benefit from decomposing the doc into named
genome fields and mutating field-by-field instead of treating the whole .md as an opaque string. (2) Weighted
three-operator mutation portfolio with an explicit exploitation/diversity dial: Guided 55% (LLM-driven exploitation,
picks the BEST parent), Random 25% (diversity maintenance, picks a RANDOM parent), Crossover 20% (two-parent
recombination) — exposed as a single `guided_weight` knob so the user can shift the balance. The lesson: do not rely on
a single mutation operator; combine LLM-guided improvement (exploit) with stochastic structural mutation (explore) and
recombination, and make the mix tunable. (3) Lineage DAG with a pre-built child index for O(depth) ancestor/descendant
queries + ASCII tree rendering: making every skill carry parent_ids/generation/mutation_type and building an inverted
children index turns evolutionary history into a queryable, visualizable artifact (`evoskill lineage`), which is
essential for trusting and debugging autonomous skill evolution — you can trace any skill back to the primordial seed
and see exactly which operator produced it. Even a SKILL.md-based system should embed this lineage metadata (frontmatter
parent_ids + generation) and render the family tree, because inspectability is a prerequisite for safe self-evolution.

#### 不确定字段

- paper_link (no paper exists; project is code+README only)
- release_date (no git tags/releases; inferred from repo activity ~2026-05 and CHANGELOG 'Unreleased' section)
- institution (independent author; no formal affiliation disclosed)
- key_results (no experiments or quantitative results reported anywhere in the repo)
- cross_transfer (structural portability across Anthropic/OpenAI/DeepSeek exists in code but no transfer experiment is documented)
- doc_form token length (no explicit cap; estimated ~100-300 tokens per assembled system message from seed-skill field sizes)

---

### TextGrad

> `idea_text_opt` · Stanford, Nature 2025(arXiv:2406.07496)。用 LLM 文本反馈做「自动微分」：把复合 AI 系统建模为计算图，对任意变量(prompt/code/分子/方案)反传 textual gradient 进行优化。 PyTorch 风格 API。GPQA 51%→55%，LeetCode-Hard +20%。是 SkillOpt「reflection=backwar

#### 基础信息

**名称**
TextGrad

**提出机构**
Stanford University (Zou Group / James Zou Lab). Authors: Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu,
Pan Lu, Zhi Huang, Carlos Guestrin, James Zou.

**发布时间**
arXiv preprint: 11 June 2024 (arXiv:2406.07496). Published in Nature: 19 March 2025 (Nature vol. 639, pp. 609-616;
Nature title: 'Optimizing generative AI by backpropagating language model feedback').

**论文链接**
https://arxiv.org/abs/2406.07496 ; Nature: https://www.nature.com/articles/s41586-025-08661-4

**代码链接**
https://github.com/zou-group/textgrad (MIT license; pip/conda install textgrad)

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 (Context/Prompts). TextGrad does NOT touch model weights; it treats the text-valued components of a
compound AI system as learnable 'variables' (tg.Variable with requires_grad=True) and optimizes them in text space.
Optimizable variables include: system/user prompts, chain-of-thought solutions, code snippets, few-shot examples,
molecular structures (SMILES), and radiotherapy plans. A compound AI system is modeled as a computation graph whose
nodes are inputs/outputs of (not-necessarily-differentiable) function calls; backpropagation flows natural-language
'textual gradients' (criticism) from an objective/loss back to each leaf variable. This is the foundational
'prompts-as-parameters' paradigm.

**技能是否独立制品**
Partial. Every optimized object is a first-class tg.Variable (value + role_description + requires_grad + gradients +
gradients_context), and the final optimized value (e.g. an improved system prompt) is a plain reusable string that can
be saved/exported. However TextGrad provides NO persistent skill-library / artifact-management abstraction: variables
live in an in-memory computation graph for the duration of the optimization run. There is no versioned skill-pack, no
cross-run registry, no skill-file format. So: artifact = a text string (prompt/solution), not a managed SKILL.md-style
file.

**是否文档载体**
No. The optimized object is a raw text string (natural-language prompt, code, or structured string like SMILES), not a
human-readable instruction document. There is no markdown/SKILL.md carrier and no structured YAML-frontmatter body. The
closest analogue is 'optimize a system-prompt string', which is pure-instruction text rather than a structured doc.
(Mixed only in the trivial sense that the variable value may contain code blocks.)

#### 技能表示

**技能编码方式**
Natural-language text string (prompts, reasoning, critiques) / executable code (LeetCode solutions) / API-call graph
(BlackboxLLM, FormattedLLMCall) / structured strings (SMILES molecules, radiotherapy plan parameters). Variables are
plain Python strings annotated with a role_description; the 'encoding' is just string + role metadata, wrapped in a
PyTorch-like autograd graph (Function/Module with forward+backward).

**技能粒度**
Strategy-rule / full-system-prompt level (the canonical use case optimizes an entire system prompt for a QA task). Also
supports whole-solution granularity (a complete CoT solution to one problem), whole-code-snippet granularity (an entire
LeetCode solution), and molecule/plan granularity. Granularity is coarse = the whole variable is one optimization unit;
there is no atomic-action or sub-step decomposition inside a variable.

#### SKILL.md_专属维度

**文档形态**
Plain-text system-prompt string (no frontmatter, no structured fields). Typical length: a system prompt of a few hundred
tokens up to ~1-2k tokens (e.g. BBH task description + accumulated instructions). The improved prompt is emitted between
<IMPROVED_VARIABLE></IMPROVED_VARIABLE> tags by the TGD optimizer. For code/molecule/plan optimization the 'doc' is the
corresponding code/SMILES/plan string. No multi-file packaging.

**编辑粒度**
Whole-variable regeneration (全新生成 / 整变量重写). The TextualGradientDescent optimizer asks the optimizer-LLM to emit a
brand-new <IMPROVED_VARIABLE> that replaces the entire old value; there is no minimal-diff / PATCH / add-delete-replace
primitive in the core. (string_based_ops.py offers a few string ops but the standard path is full rewrite.) Concretely
optimizer.step() parses new_value = response.split('<IMPROVED_VARIABLE>')[1].split('</IMPROVED_VARIABLE>')[0] and calls
parameter.set_value(new_value).

**版本与门控**
Held-out validation gating with greedy hill-climbing selection on a dev split. In evaluation/prompt_optimization.py,
run_validation_revert() evaluates the candidate prompt on val_set after each optimizer step; if val accuracy drops below
the previous best it REVERTS the variable to the previous value (system_prompt.set_value(previous_prompt)) and logs the
rejected prompt. Additional stability mechanisms: gradient_memory (keep last N textual gradients) and
TextualGradientDescentwithMomentum (keep a momentum window of past {value, gradient} pairs). No git/DAG/Pareto-front
versioning.

**文档来源**
Initial value is human/seed-initialized (e.g. STARTING_SYSTEM_PROMPT = train_set.get_task_description()). Subsequent
versions are LLM-generated from textual-gradient feedback: backward pass produces natural-language criticism, TGD
optimizer LLM rewrites the variable. So provenance = human seed + iterative LLM regeneration driven by LLM-critic
feedback (a form of failure-trajectory / criticism distillation).

**跨载体迁移**
Cross-model: strong by design — engine abstraction
(OpenAI/Anthropic/Gemini/Together/Bedrock/Cohere/Groq/vLLM/local/litellm) and explicit optimizer/target separation (a
forward 'test' engine e.g. gpt-3.5-turbo can be optimized using a stronger backward engine e.g. gpt-4o). Cross-task: the
framework is task-agnostic (same API works for QA, code, molecules, radiotherapy). Cross-user/cross-harness: not
addressed (no agent-harness concept). Optimized prompts are not empirically studied for cross-model transfer of a single
optimized prompt.

**技能库治理**
None at the skill-library level — TextGrad does not maintain a library of skills. Bounded mechanisms that resemble
governance: (1) gradient_memory keeps only the last N gradients per variable (bounded buffer, prevents unbounded
growth); (2) momentum window bounds history; (3) validation revert discards regressing candidates. No dedup/merge, no
retirement/archival, no hierarchical index, no curator loop.

**失败记忆**
Partial. (1) Validation revert logs 'rejected prompt' when a candidate underperforms on the dev split — a weak negative
signal but it is not stored as a reusable anti-pattern. (2) gradient_memory persists past textual gradients (which often
describe mistakes) for the next optimizer step. (3) momentum_storage stores past {value, gradients}. However there is NO
explicit failure-signature store, no attribution+remedy anti-pattern base, and no rejected-edit buffer reused to veto
future edits. So: implicit negative feedback via revert, not a durable failure-memory artifact.

**编辑安全**
Lightweight. (1) Held-out validation revert (run_validation_revert) is the primary safeguard — rejects regressing edits
and restores the previous value. (2) Natural-language constraints parameter on the optimizer (constraints=[...]) lets
users bound the editor with rules; (3) in_context_examples steer the rewrite; (4) gradient_memory/momentum dampen
erratic edits. No automatic pre-edit backup+rollback beyond revert, no scope-boundary enforcement (any string can be
rewritten), no eval-hacking defense, no human-in-the-loop gate, no injection/secret checks by default.

**协同进化**
Generator–verifier coevolution (forward model vs backward/eval engine) is the core architecture: the forward LLM
(target) generates outputs while a separate backward engine (LLM-as-critic) produces gradients, and a loss/eval module
acts as verifier — optimizer and target are explicitly separable (set_backward_engine). Also skill-prompt joint
optimization is possible (multiple Variables in one optimizer.parameters() list, e.g. system_prompt + few-shot examples
updated together). It is NOT skill-tool or skill-skill ecosystem coevolution (no tool registry, no multi-agent skill
ecosystem).

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization in text space (non-gradient) driven by reward-based textual feedback — this is THE foundational
How-idea of the text-space optimization paradigm. Mechanism: (1) Forward pass — run the compound system (LLM calls /
tools) to produce outputs; (2) Loss — a TextLoss/MultiFieldEvaluation/MultiChoiceTestTime/ImageQALoss module (an LLM
evaluator given a natural-language objective) scores the output and emits a textual 'loss'; (3) Backward pass — chain
rule through the autograd graph: each LLMCall.backward() asks the backward engine, given the conversation + downstream
gradient, to criticize each predecessor variable that requires_grad; aggregate()/Sum combine gradients across batch
(aggregate = LLM summarization of multiple feedbacks, see reduce_prompts.py REDUCE_MEAN_SYSTEM_PROMPT); (4)
Optimizer.step() — TextualGradientDescent feeds {variable value, role, textual gradient, constraints, in-context
examples, gradient memory} to an optimizer LLM that emits an <IMPROVED_VARIABLE>. NO weight gradients, NO SFT, NO RL
policy update — pure text-space rewrite using LLM-as-judge criticism as the 'textual gradient'. Metaphor:
autograd/backprop applied to text variables.

**学习信号来源**
LLM-as-judge (the loss/eval function is itself an LLM call with a natural-language evaluation instruction — e.g.
TextLoss, MultiChoiceTestTime 'Investigate the reasoning and answer... be very critical'); for code tasks,
execution-based signal (LeetCode test pass/fail) and for QA, ground-truth accuracy. Held-out validation score (val_set
accuracy) drives the greedy revert decision. The 'textual gradient' = the LLM critic's natural-language description of
how a variable should change.

**奖励粒度**
Hybrid, predominantly process-oriented. The TextLoss/backward engine critiques the reasoning process ('Investigate the
reasoning and answer... raise potential issues and mistakes'), so gradients are process-level criticism. Outcome signal
(correct/incorrect, test pass/fail) is used at the eval/val layer. So process (critique) + outcome (accuracy) hybrid.

**学习范式**
Offline, iterative optimization loop over mini-batches (epoch-based, batch_size default 3, max_epochs default 3).
Effectively on-policy (fresh responses generated each batch from the current variable value) and offline (runs over a
fixed train/val/test split before deployment, not during live serving). The test-time-loss variant is closer to online
intra-test-time (improving a single response in-context), but the headline prompt-optimization paradigm is offline batch
optimization.

#### 进化时机_When

**进化时机 (When)**
Predominantly inter-test-time (offline optimization between/around task execution: run the optimizer over train batches,
validate on val, evaluate on test). The MultiChoiceTestTime / test-time-loss use case is intra-test-time (refining a
single response at inference). No sleep-time/overnight replay scheduling.

**触发方式**
Periodic / curriculum-driven: a fixed optimization loop (max_epochs over train_loader batches), i.e. epoch-driven. Also
event-triggered per-batch (optimizer.step() after each batch's backward). No cron/launchd, no failure-triggered
re-optimization, no usage-driven or tool-degradation trigger in the framework itself (the user manually launches the
optimization script).

#### 存储与检索

**技能库结构**
No skill library. Variables form an ephemeral in-memory DAG (computation graph of Function/Module nodes with
predecessors and grad_fn). For prompt optimization the structure is effectively flat (one optimized system_prompt
Variable). No vector store, no file directory, no git branches, no cloud registry.

**检索/复用方式**
Not applicable in the library sense — the optimized variable is used directly (string substitution into the next forward
call). Within a run, gradient_context metadata links each gradient to the conversation/context that produced it
(gradients_context dict), which the optimizer retrieves to construct the update prompt. No semantic-similarity / BM25 /
generation-as-retrieval.

#### 验证与反馈

**验证方式**
Held-out validation (val_set) + validation gating (run_validation_revert reverts on regression) + LLM-judge (the eval_fn
/ loss is an LLM evaluator) + execution-based correctness for code (LeetCode hidden tests) and ground-truth accuracy for
QA. Multi-model debate not used; surrogate verifier = the backward engine itself. Functional-correctness checks for
code; task-specific eval_fn returned by load_task.

**错误纠正**
Rollback / revert (run_validation_revert restores previous prompt on val regression) + self-revision (the optimizer LLM
rewrites the variable per the textual gradient). Bounded editing via constraints + gradient_memory + momentum. No
directed-diff patching and no explicit replanning module — correction is full-variable regeneration gated by validation.

#### 环境与基座

**测试环境**
General-purpose / multi-domain: QA (GPQA, MMLU, BBH, GSM8K), coding (LeetCode-Hard), tool-use via compound systems,
molecule optimization (druglike small molecules, in silico binding), radiotherapy treatment planning. Provided task
loaders in textgrad/tasks: big_bench_hard, gpqa, gsm8k, leetcode, mmlu, multimodal.

**底座模型**
GPT-family primarily (GPT-4o as backward/eval engine, gpt-3.5-turbo as forward test engine in prompt-optimization
examples). Explicit optimizer/target separation: set_backward_engine() decouples the critic (strong) from the forward
model (target). Supports OpenAI, Anthropic, Gemini, Together, Bedrock, Cohere, Groq, vLLM, local (LM
Studio/OpenAI-compatible), and a litellm-based experimental engine — so any LLM can be forward or backward engine.
Multimodal via OrderedFieldsMultimodalLLMCall (GPT-4o vision).

**部署域 (Where)**
General — TextGrad is a general-purpose optimization framework for any compound AI system, demonstrated across
reasoning, coding, chemistry, and medicine; not specialized to a single vertical.

#### 评估指标

**评估指标**
success_rate / accuracy (QA accuracy on test_set, LeetCode pass rate), generalization (optimized prompts evaluated on
held-out test split and shown to improve GPT-4o zero-shot), relative performance gain (+20% relative on LeetCode-Hard),
cost (number of LLM forward+backward calls — not heavily reported), sample efficiency (converges within a few epochs / 3
steps). Also in-domain metrics: molecule docking scores, radiotherapy plan specificity. Skill-library-growth and
economic-value metrics are not applicable.

**关键结论**
(1) GPT-4o GPQA zero-shot accuracy improved 51% -> 55% out-of-the-box, no framework modification. (2) +20% relative gain
on LeetCode-Hard coding-solution optimization. (3) Improves prompts for reasoning tasks (BBH object counting example:
wrong count 7 -> correct 10 after one TGD step). (4) Designs new druglike small molecules with desirable in silico
binding. (5) Designs radiation-oncology treatment plans with high specificity. (6) Works across heterogeneous variable
types (text, code, molecules, plans) with a single PyTorch-like API and no per-task framework tuning — user supplies
only the objective function.

#### 局限与挑战

**局限与挑战**
optimizer_quality (heavily depends on a strong backward/optimizer LLM — the code explicitly warns IndexError when the
optimizer 'cannot follow the instructions' and suggests 'using a stronger model'); regression_risk on unseen data
(mitigated but not eliminated by val revert — overfits dev split); cost/scalability (each step = many forward + backward
LLM calls; computation-graph depth multiplies backward calls); eval-hacking risk (an LLM-as-judge loss can be gamed by
verbose/length-exploiting outputs); transferability of a single optimized prompt across models not guaranteed; no
catastrophic-forgetting concept (stateless variables) but no durable memory either; doc_bloat not addressed but
optimized prompts can grow unbounded across steps.

#### 可借鉴要点

**可借鉴要点**
Three directly-transferable engineering ideas for an agent that self-evolves its SKILL.md: (1) Prompts/SKILL.md as
learnable parameters — wrap the SKILL.md as a Variable with requires_grad=True inside a computation graph; every step of
agent execution is a differentiable 'Function' with a forward (run) and a backward (reflect). This is the conceptual
parent of 'reflection = backward pass': the agent's natural-language self-critique IS the textual gradient. (2)
Backward-pass-as-reflection with optimizer/target separation — use a strong, separate 'backward engine' (could be the
same model in critic mode, or a stronger judge) to read the execution trace + outcome and emit, for each editable
component of the SKILL.md, a natural-language gradient ('the instruction to do X is wrong because... change it to...');
then a TGD-style optimizer step rewrites that section. Critique is localized per-variable (per-section) via the chain
rule, not one global rewrite. (3) Held-out validation gating with greedy revert (run_validation_revert) as the practical
safety net — after every SKILL.md edit, re-evaluate on a held-out dev task batch and roll back the edit if
accuracy/regression drops; plus gradient_memory + momentum to keep the editor stable. Together these give a turn-key,
PyTorch-flavored 'autograd for skills' loop: forward=run, loss=LLM-judge+execution, backward=per-section critique,
optimizer=bounded rewrite, gate=dev-split revert.

---

### GEPA

> `idea_text_opt` · Agrawal et al., 2025。Reflective textual evolution 的 Genetic-Pareto 优化器：反射→ 精炼模式，从发展集选候选系统并优化 prompt。证明比标量奖励 RL 更样本高效；Pareto 前沿 选择保留多样候选，比 TextGrad 贪心爬山收敛更快。是 EvoSkill/SkillSmith 的直接母体。 openreview RQm2

#### 基础信息

**名称**
GEPA (Genetic-Pareto)

**提出机构**
UC Berkeley, Stanford, BespokeLabs.ai, Notre Dame, Databricks, MIT (Agrawal, Tan, Soylu, Ziems, Khare, Opsahl-Ong,
Singhvi, Shandilya, Ryan, Jiang, Potts, Sen, Dimakis, Stoica, Klein, Zaharia, Khattab)

**发布时间**
2025; published as a conference paper at ICLR 2026

**论文链接**
https://openreview.net/pdf?id=RQm2KQTM5r

**代码链接**
https://github.com/gepa-ai/gepa

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示. GEPA evolves ONLY the set of module prompts Pi_Phi of a compound AI system Phi=(M,C,X,Y); the underlying
LLM weights Theta_Phi remain frozen. Each language module M_i=(pi_i, theta_i, X_i, Y_i) has its system prompt pi_i
(instructions + optional few-shot demos) mutated; control flow C and tool APIs are untouched.

**技能是否独立制品**
是. Each candidate prompt is a standalone, reusable text artifact (a fully-instantiated <Pi, Theta_frozen> system
version) stored in a candidate pool P with explicit ancestry records (parent-child edges forming a genetic tree/DAG).
Candidates are serialized, compared, and recombined as first-class objects.

**是否文档载体**
是. The optimized artifact is fundamentally a human-readable natural-language instruction document (declarative rules,
purpose/context, step-by-step strategy, output format - see Figure 2). No executable code is embedded inside the prompt
itself; the 'skill' lives entirely as markdown-like instruction text fed to an LLM module.

#### 技能表示

**技能编码方式**
自然语言SOP encoded as system prompts (declarative instructions + optional few-shot demonstrations). GEPA-learned prompts
are rich, declarative documents: input understanding, purpose/context, key observations and lessons, how-to-build
strategy, output specification (Figure 2). Not code, not vectors, not graphs - pure instruction text per module.

**技能粒度**
子任务workflow + 策略规则. Granularity is per-module within a compound AI system: each module's prompt is a sub-task workflow
instruction (e.g., second-hop query generation, answer extraction). The evolved content encodes high-level declarative
strategy rules/lessons ('First-hop documents often cover one entity; target missing linked documents') rather than
atomic actions.

#### SKILL.md_专属维度

**文档形态**
纯指令 document (declarative natural-language instructions, no YAML frontmatter, no embedded executable code blocks).
Typical length: seed prompts are 1-2 lines (~30 tokens); GEPA-evolved prompts grow to several hundred to ~1k+ tokens of
structured prose with sections (Input Understanding, Purpose/Context, Key Observations/Lessards, How-to-Build, Output).
Form is a single flat instruction blob per module, not a multi-file pack.

**编辑粒度**
整文档重写 per module per mutation (the reflection LM emits a wholly revised prompt pi_i, not a patch/diff). Two proposal
strategies: (1) Reflective Prompt Mutation - single-parent rewrite accumulating lessons; (2) System-Aware Merge
(GEPA+Merge) - genetic crossover that combines complementary module-level prompts from two ancestors (a bundle-like
joint edit across modules). No minimal-diff/PATCH editing.

**版本与门控**
Pareto 前沿 + 留出验证门控. Multi-level gating: (a) Minibatch eval first; only if score improves over parent, (b) full D_pareto
validation eval; candidate is added to pool P only if it improves. Selection for next mutation uses Pareto-frontier
filtering (retain candidates that are best on >=1 task instance, prune strictly dominated) with stochastic sampling
weighted by #tasks-led. Ancestry DAG records lineage; Merge skips direct-ancestry and already-tried pairings.

**文档来源**
LLM 迭代生成 from execution + evaluation traces. Source signals: (1) human-initialized seed prompt (simple baseline); (2)
rollout execution traces (module inputs/outputs/reasoning); (3) evaluation traces (compiler errors, failed rubrics,
human-grader explanations via feedback function mu_f); (4) reflective attribution by an LLM. Not one-shot generation -
iteratively distilled from many failure/success trajectories.

**跨载体迁移**
跨模型 + 跨基准. Strong cross-model transfer: prompts optimized on weak Qwen3-8B ('GEPA-Qwen-Opt') gain +9pp when evaluated
unchanged on GPT-4.1-Mini, beating baselines that optimized directly on GPT-4.1-Mini. Cross-benchmark: same optimizer
applied to 6 diverse benchmarks (AIME-2025, LiveBench-Math, HotpotQA, IFBench, HoVer, PUPA). Cross-task transfer within
inference-time search (lessons from one kernel problem applied to others).

**技能库治理**
Pareto pruning = dominated-candidate retirement (analogous to Lotka-Volterra survival-of-fittest per instance); ancestry
DAG prevents redundant Merge attempts (lineage conditions skip direct ancestry and previously-tried pairs); no explicit
similarity-based dedup, no hierarchical index, no curator loop. Pool size is implicitly bounded by Pareto domination
pruning.

**失败记忆**
是, strongly. Failure signals are first-class: execution traces (failed reasoning/tool calls) AND evaluation traces
(compiler errors, failed rubric items, human-grader justifications) are captured as feedback_text by mu_f and fed into
the reflection meta-prompt for explicit credit assignment. The candidate's own ancestry accumulates lessons. Rejected
candidates (no improvement over parent on minibatch) are discarded - they do NOT feed a persistent anti-pattern buffer,
but their traces inform the next reflection.

**编辑安全**
Bounded editing via two-stage validation gating (minibatch -> full D_pareto) ensuring only improvements over parent are
committed; held-out validation set (content of validation instances restricted from optimizer); budget cap B bounds
total rollouts; scope limited to prompts (weights, control flow, source code of tools NOT touched); adversarial/probe
mode implemented by reward inversion (PUPA/AIME adversarial search). NO explicit human-in-the-loop, NO pre-edit
backup/rollback, NO eval-hacking defense documented (the system could in principle overfit validation idiosyncrasies -
generalization gap analyzed in Figure 15).

**协同进化**
skill-prompt 联合 (multi-module joint prompt evolution within one compound AI system). GEPA evolves prompts of ALL |M|
modules together (round-robin module selection), and System-Aware Merge crosses over module prompts from different
ancestors. Generator-verifier style: reflection LM acts as meta-optimizer over target system. NOT skill-tool coevolution
(tools frozen), NOT skill-skill ecosystem (single system, no library of independent skills).

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (文本空间, non-gradient) combined with population_evolutionary (genetic algorithm: mutation + crossover
+ Pareto selection) and reward-based textual feedback. Specifically: (1) Reflective Prompt Mutation =
LLM-reflect-and-refine using natural-language feedback from rollouts; (2) System-Aware Merge = genetic crossover over
Pareto-optimal ancestors; (3) Pareto-based 'illumination' candidate selection (quality-diversity a la Mouret & Clune
2015). NO gradient updates, NO SFT, NO RL policy gradients - learning happens entirely in language space.

**学习信号来源**
成败轨迹 (execution traces of reasoning/tool calls) + evaluation traces (compiler/rubric/human-grader feedback via mu_f) +
留出验证分 (D_pareto held-out scores) + LLM-as-judge (reflection LM attributes credit and proposes updates). Auxiliary:
human-written explanations per instance when available.

**奖励粒度**
hybrid. Outcome: scalar metric mu (exact match / F1 / pass rate) for selection. Process: textual feedback_text from mu_f
(compiler errors, rubric failures, module-level feedback in multi-hop) for reflective learning.

**学习范式**
offline + on-policy. Optimization is an offline sleep-time phase over D_train before deployment (inter-test-time).
Sampling is on-policy w.r.t. the current candidate (rollouts drawn from the candidate being mutated). An online
inference-time-search variant exists (D_val = D_train, overfitting target tasks).

#### 进化时机_When

**进化时机 (When)**
inter-test-time (offline optimization loop over D_train before deployment, bounded by rollout budget B). Secondary mode:
inference-time search (per-task overfitting at query time, used for code optimization on NPUEval/KernelBench). NOT
intra-test-time online adaptation during a single task execution.

**触发方式**
周期性 / budget-driven iteration (loop continues 'While Budget > 0'). No event/failure/curriculum triggers; the optimizer
runs to budget exhaustion. Merge is triggered conditionally when the pool contains two complementary Pareto-optimal
candidates sharing a common ancestor.

#### 存储与检索

**技能库结构**
Candidate pool P = Pareto frontier with ancestry DAG. Each node = a concrete <Pi, Theta_frozen> instantiation with
parent edges and per-task scores matrix (rows=candidates, cols=task instances). Filtered pool retains only non-dominated
candidates. No vector DB, no hierarchical index, no cloud registry, no git branches - in-memory genetic tree.

**检索/复用方式**
Pareto-based stochastic sampling: from the filtered (non-dominated) pool, sample a candidate weighted by number of task
instances it leads. For mutation target module: round-robin policy. For Merge: sample 2 distinct candidates with valid
lineage. Not semantic similarity, not BM25 - task-coverage-weighted sampling.

#### 验证与反馈

**验证方式**
execution-based (rollouts scored by mu) + 留出评估 (D_pareto held-out validation set, content hidden from optimizer) +
validation gating (two-stage: minibatch then full-D_pareto; commit only if improves) + functional correctness (exact
match / F1 / pass rate per benchmark). Reflection LM acts as a surrogate verifier proposing attribute-level credit.

**错误纠正**
有界编辑 (bounded edits via minibatch-gated commit) + 定向 diff 修补 (reflection LM emits targeted revisions attributing
failures to specific prompt elements) + 回滚 (rejected candidates simply discarded, parent retained). No explicit
self-revision of a committed candidate beyond proposing a new child; the genetic structure itself is the
error-correction memory.

#### 环境与基座

**测试环境**
通用 NLP reasoning + coding. Six benchmarks: multi-hop QA (HotpotQA), Math (AIME-2025, LiveBench-Math), instruction
following (IFBench), privacy-aware delegation (PUPA), retrieval-augmented verification (HoVer). Extended to coding
(NPUEval AMD NPU kernels, KernelBench CUDA kernels) as inference-time search. Adversarial prompt search on AIME-2025.

**底座模型**
Open-source LLM (Qwen3-8B) and proprietary GPT-4.1 Mini as TARGET system backbones (weights frozen). Optimizer/target
separated: a reflection LM (same family, typically stronger) acts as the meta-optimizer that proposes prompt mutations.
Inference-time search uses GPT-4o. Adversarial probe uses GPT-5 Mini. No VLM.

**部署域 (Where)**
general (general-purpose compound AI workflows: QA, math, instruction-following, verification, privacy delegation, code
generation). Not specialized to a single domain.

#### 评估指标

**评估指标**
success_rate (per-benchmark test-set score) + sample_efficiency (rollouts to reach GRPO's best validation; train-only
rollouts) + generalization (held-out test set, cross-model GEPA-Qwen-Opt -> GPT-4.1-Mini) + cost (monetary cost reported
in Appendix G.3) + generalization_gap (validation-test delta, Figure 15).

**关键结论**
On Qwen3-8B, GEPA beats GRPO (24k rollouts) by +6pp avg and up to +19pp while using up to 35x fewer rollouts (4-35x
fewer to reach optimal test perf); matches GRPO's best validation with 78x greater sample efficiency (as few as 243-1179
rollouts). Beats MIPROv2 by +13pp aggregate (vs MIPROv2's +5.6pp), +12pp on AIME-2025. On GPT-4.1-Mini, beats TextGrad
(+12.19pp vs +6.11pp), Trace/OptoPrime, MIPROv2. Cross-model: Qwen-optimized prompts gain +9pp on GPT-4.1-Mini. Pareto
selection beats SelectBestCandidate by +6.4pp and BeamSearch by +7.33pp (Table 3). Inference-time search: NPUEval mean
vector util 4.25% -> 30.52%; KernelBench PyTorch-beating CUDA from ~0% to >20%.

#### 局限与挑战

**局限与挑战**
optimizer_quality (depends on a strong reflection LM to propose good mutations; weaker optimizers degrade).
regression_risk (on AIME-2025 with Qwen3-8B, GEPA underperforms GRPO; IFBench GEPA+Merge regresses vs GEPA). scalability
(majority of rollout budget spent on validation/selection, not learning - train-only rollouts are 79-737 but full
pipeline needs thousands). doc_bloat (evolved prompts grow long; no compression). transferability (strong but variable
across tasks/models). controllability (no human-in-the-loop; no explicit eval-hacking defense - prompts could overfit
validation idiosyncrasies, though generalization gap is small).

#### 可借鉴要点

**可借鉴要点**
- PARETO-FRONTIER VERSIONING BEATS GREEDY HILL-CLIMBING: Maintain a pool of non-dominated candidate SKILL.md versions (each best on at least one task instance / user / scenario) instead of always editing the single global-best. Stochastically sample the next mutation target weighted by coverage. This escapes local optima that trap TextGrad-style greedy single-best editing - GEPA shows +6.4pp over SelectBestCandidate and +7.33pp over BeamSearch. For SKILL.md self-evolution: keep multiple competing drafts, prune only strictly-dominated ones, and let diverse scenarios keep diverse winners alive.
- REFLECT-AND-REFINE WITH BOTH EXECUTION + EVALUATION TRACES: Feed the meta-prompt not just (current prompt, scalar score) but the FULL serialized trajectory (the agent's reasoning, tool calls, tool outputs) AND the evaluation trace (compiler errors, failed rubric items, human-grader justifications) as feedback_text. The reflection LM performs implicit credit assignment and emits a whole-document rewrite. This is dramatically more sample-efficient than scalar-reward RL (4-35x fewer rollouts than GRPO) because language is a richer learning medium than sparse scalar gradients. For SKILL.md: log execution traces + structured eval feedback, and let an LLM propose full rewrites attributed to specific failure modes.
- TWO-STAGE HELD-OUT VALIDATION GATING AS CHEAP SAFETY: Every proposed edit is first evaluated on a minibatch, and only promoted to the candidate pool if it beats its parent on the held-out D_pareto validation set (content hidden from optimizer). This bounds regression risk without human review - rejected edits are simply discarded, parent retained. Combine with a hard rollout/time budget B to prevent runaway. For SKILL.md: keep a held-out eval set the self-editor cannot read, gate every commit on it, and never overwrite the parent until a child provably wins.

---

### OPRO / PromptBreeder / EvoPrompt

> `idea_text_opt` · LLM-as-optimizer 三部曲。OPRO(Yang, Google, ICLR 2024)：LLM 用自然语言描述+评分 迭代优化 prompt。PromptBreeder(Meta)：prompt 作为可进化种群，用 mutation operators 自我进化「进化策略」。EvoPrompt：遗传算法/DE 思想演化 prompt。共同点：把 prompt/ 指令当作可进化文本基因

#### 基础信息

**名称**
OPRO / PromptBreeder / EvoPrompt (LLM-as-optimizer trilogy)

**提出机构**
OPRO: Google DeepMind (Yang, Wang, Lu, Liu, Le, Zhou, Chen). PromptBreeder: Google DeepMind (Fernando, Banarse,
Michalewski, Osindero, Rocktaschel). EvoPrompt: Microsoft Research + Tsinghua University (Guo, Wang, J.Guo, Li, Song,
Tan, G.Liu, Bian, Y.Yang).

**发布时间**
All three September 2023: OPRO arXiv:2309.03409 (Sep 7, 2023; v3 Apr 15, 2024); PromptBreeder arXiv:2309.16797 (Sep 28,
2023); EvoPrompt arXiv:2309.08532 (Sep 15, 2023; v3 May 1, 2025). Both OPRO and EvoPrompt published at ICLR 2024;
PromptBreeder published at ICML 2024 (PMLR v235 fernando24a).

**论文链接**
OPRO: https://arxiv.org/abs/2309.03409 ; PromptBreeder: https://arxiv.org/abs/2309.16797 ; EvoPrompt: https://arxiv.org/abs/2309.08532

**代码链接**
OPRO official: https://github.com/google-deepmind/opro ; EvoPrompt official: https://github.com/beeevita/EvoPrompt
(mirror at microsoft/EvoPrompt) ; PromptBreeder: NO official release, community implementations only (e.g.
vaughanlove/PromptBreeder).

**类型**
academic (three peer-reviewed papers, ICLR 2024 x2 + ICML 2024)

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示. All three evolve ONLY the natural-language instruction/prompt text applied to a frozen LLM; model weights
Theta, tools, and agent architecture are untouched. OPRO optimizes a single instruction string prepended/appended to
task inputs (Q_begin/Q_end/A_begin). PromptBreeder evolves a POPULATION of task-prompts AND, uniquely, the
mutation-prompts that govern how task-prompts are mutated. EvoPrompt evolves a population of discrete prompts via GA or
DE operators instantiated through LLM calls. The optimization variable in all three is text, not parameters.

**技能是否独立制品**
是 (partial). Each candidate prompt/instruction is a standalone, reusable text artifact that can be serialized, scored,
compared, and recombined as a first-class object. OPRO keeps a trajectory list of (prompt, score) pairs; PromptBreeder
maintains explicit 'units of evolution' = {task-prompts, mutation-prompt, optional few-shot context} with ancestry;
EvoPrompt maintains a population of prompt chromosomes with fitness. However, none of the three treats the prompt as a
long-lived, named, versioned SKILL document with library governance - the artifact is a short instruction string, not a
multi-section skill file.

**是否文档载体**
是. The evolved object is fundamentally human-readable natural-language instruction text. No executable code is embedded
in the evolved artifact; the 'skill' is pure declarative instruction. Typical evolved prompts are 1-3 short sentences
(OPRO's 'Take a deep breath and work on this problem step-by-step.'; PromptBreeder's GSM8K winner 'SOLUTION' or longer
multi-rule prompts; EvoPrompt's instruction templates). Not a structured markdown/SKILL.md document - just a flat
instruction blob. This is the foundational paradigm: instruction = evolvable text gene, predating
SKILL.md-as-whole-document evolution.

#### 技能表示

**技能编码方式**
自然语言SOP encoded as instruction strings (declarative sentences) prepended/appended to task inputs. PromptBreeder
additionally encodes (a) mutation-prompts = NL instructions describing HOW to mutate a task-prompt, (b) thinking-styles
= NL cognitive-heuristic descriptions, (c) few-shot context = stored correct workings-out. EvoPrompt encodes prompts as
discrete text chromosomes (manually written or APE-generated seeds). No vector embeddings, no graphs, no code - pure
text throughout.

**技能粒度**
策略规则 (single strategy-level instruction/rule per artifact). Finer than a full skill pack, coarser than an atomic action.
PromptBreeder's units bundle a small number of co-evolving rules (2 task-prompts + 1 mutation-prompt + few-shot
examples), approaching a minimal 'skill pack'; OPRO and EvoPrompt evolve a single monolithic instruction per candidate.

#### SKILL.md_专属维度

**文档形态**
纯指令 (pure instruction text, no YAML frontmatter, no embedded executable code blocks). Typical token length is SHORT:
OPRO instructions ~5-25 tokens (e.g. 'Take a deep breath and work on this problem step-by-step.' ~10 tokens), with the
OPRO meta-prompt itself running to a few hundred tokens (20 best instruction-score pairs + 3 task exemplars +
meta-instructions). PromptBreeder task-prompts range from a single word ('SOLUTION') to multi-clause rules (~50-150
tokens); mutation-prompts are short imperatives (~10-30 tokens). EvoPrompt prompts are template-style instructions
(~20-100 tokens). None reach the multi-KB SKILL.md scale.

**编辑粒度**
整文档重写 (whole-instruction rewrite per mutation; no PATCH/diff). OPRO: optimizer LLM emits a brand-new instruction string
each step, conditioned on the trajectory of past (prompt, score) pairs - explicitly NOT editing a single input prompt.
PromptBreeder: each replication applies ONE of 9 mutation operators (uniformly sampled) which produces a wholly new
task-prompt or mutation-prompt via LLM continuation; Prompt Crossover (10% chance after mutation) replaces a task-prompt
with one from a fitness-proportionate-selected peer - a bundle-like joint edit. EvoPrompt(GA): two-parent crossover +
mutation, both realized as LLM-generated rewrites from templates (template_ga); EvoPrompt(DE): three-parent donor (a +
F(b-c)) then binomial crossover with target x, all expressed as LLM instructions (template_de). No minimal-diff editing
in any of the three.

**版本与门控**
留出验证门控 (held-out development set) + greedy/top-k selection. OPRO: at each step, 8 new instructions are scored on a small
training subset (3.5% GSM8K, 20% BBH); only the best-20-by-training-accuracy trajectory is retained in the meta-prompt;
final best prompt is selected by training accuracy and evaluated on a held-out test set. PromptBreeder:
binary-tournament GA - sample 2 units, mutate the fitter, overwrite the loser; fitness = accuracy on a random 100-Q&A
batch sampled fresh each evaluation (implicit held-out via random resampling); elite lineage history preserved per unit.
EvoPrompt(GA): after each generation, keep top-N prompts by development-set score; EvoPrompt(DE): one-to-one replacement
- new prompt p' replaces p only if it scores higher on the development set. No Pareto frontier, no git branching, no DAG
bloodline versioning, no human-in-the-loop.

**文档来源**
LLM 迭代生成 from execution + evaluation traces, seeded by human initialization. OPRO: starts from a human seed (e.g. 'Let's
solve the problem.' or empty string) and iteratively rewrites via the optimizer LLM conditioned on score-sorted
trajectory. PromptBreeder: seeds from random combinations of (problem-description D, sampled thinking-style T, sampled
mutation-prompt M) producing initial task-prompts; then evolved over generations via 9 mutation operators. EvoPrompt:
initializes population from manually-written prompts and/or APE-generated prompts (prompts.txt, prompts_auto.txt). All
three iteratively distill improvements from fitness feedback, not one-shot generation.

**跨载体迁移**
跨任务 + 跨模型 (within-benchmark and across LLMs). OPRO: instructions optimized on GSM8K transfer to MultiArith and AQuA;
OPRO also demonstrates cross-optimizer transfer (prompts found by PaLM 2-L-IT vs gpt-3.5-turbo vs gpt-4 differ in style
but all improve scorer); cross-scorer transfer studied. PromptBreeder: same system adapts across arithmetic (GSM8K,
MultiArith, SingleEq, AddSub, SVAMP, AQuA-RAT), commonsense (SQA, CSQA), instruction induction (APE tasks), and
hate-speech classification (ETHOS) - one general-purpose mechanism, many domains. EvoPrompt: optimized on 31 datasets
spanning language understanding, generation, and BBH; cross-LLM (GPT-3.5 <-> Alpaca) reported. None address
cross-agent-harness (Claude/Codex/Cursor) or cross-user/team transfer.

**技能库治理**
Minimal. OPRO: implicit dedup via top-20 retention (low-quality prompts dropped from trajectory); no explicit
similarity-based dedup, no hierarchical index, no curator loop. PromptBreeder: EDA mutation operator applies
BERT-embedding cosine similarity filtering (>0.95 similarity pruned) to maintain population diversity - a
quality-diversity-style curator; no retirement/archival, no library-growth bound beyond fixed population size.
EvoPrompt: fixed population size with top-N (GA) or one-to-one replacement (DE) implicitly bounding growth; no
similarity dedup. None implement Lotka-Volterra, hierarchical indexing, or explicit dust-cleaning loops.

**失败记忆**
Weak / implicit. OPRO: low-scoring prompts remain in the trajectory (sorted ascending) so the optimizer LLM sees what
does NOT work - a soft anti-pattern signal, but no explicit failure-signature buffer; rejected candidates are not
isolated as a negative-feedback store. PromptBreeder: lineage-based mutation operator exposes the chronological elite
history (bad->good gradient) which implicitly encodes failure recovery; Lamarckian operator reverse-engineers
task-prompts from SUCCESSFUL workings-out (positive signal only); no anti-pattern store. EvoPrompt: rejected offspring
simply discarded; no rejected-edit buffer. None maintain an explicit failure-signature+attribution+remedy memory.

**编辑安全**
Minimal - these are research prototypes, not production editors. Scope: edits are confined to the prompt text string
(model weights, source code, tools untouched) - an implicit scope boundary. Bounded editing: PromptBreeder's
binary-tournament GA and EvoPrompt(DE)'s 'replace only if better' provide implicit bounded-edit safety (regressors
discarded); OPRO's top-20 retention similarly bounds. Held-out evaluation sets (OPRO test set, PromptBreeder
random-batch fitness, EvoPrompt development set) act as soft validation gating. NO pre-edit backup/rollback, NO explicit
eval-hacking defense (OPRO Section 5.4 explicitly analyzes overfitting to training-subset idiosyncrasies), NO
human-in-the-loop, NO secret/injection checks, NO scope-limiting to specific files (no filesystem interaction at all -
pure text optimization).

**协同进化**
skill-prompt 联合 (PromptBreeder only) / skill-only (OPRO, EvoPrompt). PromptBreeder is the standout: it co-evolves
task-prompts WITH mutation-prompts (the strategy that generates strategies) in a self-referential loop - this is the
closest precedent to 'evolving the SKILL.md that evolves SKILL.md'. OPRO evolves only the task instruction (single
gene); the meta-prompt structure is hand-designed and frozen. EvoPrompt evolves only task prompts; the GA/DE operator
templates (template_ga.py, template_de.py) are frozen. None co-evolve with external tools or with a separate
generator-verifier pair (the LLM is both generator and the mutation operator).

#### 自进化机制_How

**进化方法范式 (How)**
population_evolutionary + rollout_optimization (文本空间, non-gradient) + reward-based textual feedback. NO gradients, NO
SFT, NO RL policy updates - all learning happens in language space. OPRO: a black-box text-space optimizer - the
optimizer LLM generates new candidate solutions from a meta-prompt containing the optimization trajectory (past
solutions + scores, sorted ascending); multiple solutions per step (8) with tuned sampling temperature (1.0 default) for
exploration-exploitation; demonstrably general (linear regression, TSP, prompt optimization). PromptBreeder: full
binary-tournament GENETIC ALGORITHM (Harvey 2011) with 9 mutation operators across 5 classes - (1) Direct Mutation
[zero-order prompt generation, first-order prompt generation], (2) Estimation-of-Distribution Mutation [EDA mutation,
EDA rank/index mutation, lineage-based mutation], (3) Hyper-Mutation [zero-order hyper-mutation, first-order
hyper-mutation] - this class mutates the MUTATION-PROMPTS themselves = evolution of evolvability, (4) Lamarckian
Mutation [working-out -> task-prompt reverse engineering from successful phenotypes], (5) Prompt Crossover (10%
post-mutation, fitness-proportionate peer) + Context Shuffling; uniform random selection over the 9 operators per
replication. EvoPrompt: instantiates two classical EAs through LLM calls - EvoPrompt(GA): selection
(wheel/random/tournament) -> crossover (LLM template_ga) -> mutation (LLM template_ga) -> keep top-N; EvoPrompt(DE):
mutation vector y = a + F(b-c) realized as LLM instruction, binomial crossover with target x, greedy replacement. Common
thread: prompt/instruction = evolvable text gene, LLM = the optimization/mutation operator.

**学习信号来源**
环境奖励 (task accuracy on a training/dev set) is the dominant signal in all three. OPRO: scorer-LLM greedy-decoded accuracy
on the training subset (3.5% GSM8K / 20% BBH). PromptBreeder: fitness = task accuracy on a random 100-Q&A batch drawn
from the full training set each evaluation (random resampling provides a curriculum-like effect). EvoPrompt:
development-set metric (accuracy for classification, BLEU/ROUGE for generation, exact-match for BBH). NO LLM-as-judge
for reward (the LLM is the optimizer, not the judge - reward comes from ground-truth task labels). NO self-reflection as
a learning signal (PromptBreeder's Lamarckian operator uses successful workings-out, but this is positive-only). NO
explicit failure attribution.

**奖励粒度**
outcome (result-level). All three optimize a single scalar task-accuracy (or task-metric) score per candidate prompt. NO
process-level reward decomposition in OPRO or EvoPrompt. PromptBreeder's Lamarckian 'working-out -> task-prompt'
operator uses intermediate reasoning traces (a quasi-process signal) but only from successful rollouts; the selection
signal itself is outcome-level accuracy.

**学习范式**
offline + on-policy. All three run as offline optimization loops over a fixed train/dev set before deployment
(inter-test-time / sleep-time style); no online adaptation during task execution. Sampling is on-policy w.r.t. the
current candidate population (each new prompt is generated from and evaluated against the current population state).
PromptBreeder's random-batch-resampling per evaluation introduces mild off-policy flavor (fitness estimated on different
batches across generations).

#### 进化时机_When

**进化时机 (When)**
inter-test-time (offline optimization phase before deployment). All three are batch optimization procedures that run to
convergence (or step/time budget) and then emit a single best prompt (or population) for downstream use. NOT
intra-test-time - the optimized prompt is frozen during task execution. NOT sleep-time scheduled - the optimization is
launched explicitly by the practitioner, not triggered by idle cycles or a cron.

**触发方式**
周期性 / budget-driven iteration. OPRO: loop continues until 'the LLM is unable to propose new solutions with better
optimization scores, or a maximum number of optimization steps has reached' - convergence-or-budget termination.
PromptBreeder: runs for a fixed number of generations n (CLI argument). EvoPrompt: fixed number of iterations /
generations. No event triggers (no failure-triggered re-evolution, no curriculum-driven trigger, no usage-driven
trigger, no tool-degradation trigger). The evolution is a one-shot offline batch job, not a continuous lifecycle - a key
contrast with later SKILL.md self-evolution work where evolution is triggered in-loop by task outcomes.

#### 存储与检索

**技能库结构**
In-memory population / trajectory, no persistent library. OPRO: trajectory list of (prompt, score) pairs (sorted
ascending, top-20 retained) - effectively a flat leaderboard, no vector DB, no filesystem. PromptBreeder: fixed-size
population of 'units of evolution' (each = task-prompts + mutation-prompt + few-shot context) with per-unit elite
lineage history - a flat population with implicit ancestry edges, no DAG persistence. EvoPrompt: fixed-size population
of prompt chromosomes (size = init popsize argument), no ancestry tracking, no hierarchical index. None use git
branches, cloud registries, graphs, or persistent skill-file directories - the 'library' is a process-local list that
dies when the optimization finishes.

**检索/复用方式**
Score-weighted / fitness-proportionate sampling from the population (NOT semantic similarity, NOT
generation-as-retrieval). OPRO: meta-prompt explicitly includes score-sorted trajectory so the optimizer LLM attends to
high-scoring patterns; no sampling per se, the full top-20 is presented. PromptBreeder: binary tournament samples 2
random units and picks the fitter; EDA mutation samples the diversity-filtered population; Prompt Crossover uses
fitness-proportionate (roulette) selection. EvoPrompt: selection mode argument - 'wheel' (fitness-proportionate,
default), 'random', 'tour' (tournament). No BM25, no embedding retrieval, no description-match triggering - the
population is small enough to scan exhaustively.

#### 验证与反馈

**验证方式**
execution-based (rollouts on the task) + 留出评估 (held-out test set used ONLY for final reporting, not during optimization)
+ functional correctness (exact-match / accuracy / BLEU). OPRO: scorer LLM greedily decodes answers on the training
subset during optimization; test accuracy reported only post-optimization; overfitting analysis in Section 5.4.
PromptBreeder: fitness = accuracy on random 100-Q&A batch (resampled each eval); held-out test reported
post-optimization. EvoPrompt: development set used for selection during optimization; held-out test set reported
post-optimization. NO LLM-judge, NO surrogate verifier, NO multi-model debate, NO validation gating with
reject-and-retry - simple score-then-select throughout.

**错误纠正**
有界编辑 (bounded edits via population-level selection - bad candidates are simply not selected, parent retained) + 定向 diff
修补 (PromptBreeder's first-order hyper-mutation 'Please summarize and improve the following instruction' is a targeted
revision of the mutation-prompt; PromptBreeder's lineage-based mutation provides an explicit bad->good gradient to
follow). NO self-revision of a committed candidate (the population IS the memory). NO rollback (no committed state to
roll back to - everything is in the population). NO replanning. OPRO and EvoPrompt lack explicit error correction - they
rely purely on generate-and-select.

#### 环境与基座

**测试环境**
通用 NLP reasoning + classification + generation. OPRO: GSM8K (grade-school math), Big-Bench Hard (23 tasks), MultiArith,
AQuA, plus motivating linear-regression and TSP studies. PromptBreeder: arithmetic reasoning (GSM8K, MultiArith,
SingleEq, AddSub, SVAMP, AQuA-RAT), commonsense reasoning (SportsQA, CommonsenseQA), hate-speech classification (ETHOS),
APE instruction-induction tasks (23 sub-tasks). EvoPrompt: 31 datasets - language understanding (classification),
generation (summarization, translation), BBH. NO coding agents, NO GUI, NO Minecraft, NO tool-use environments - these
are pure NLP benchmarks.

**底座模型**
Proprietary + open-source LLMs as frozen scorers; optimizer/target separated. OPRO: optimizer LLMs = PaLM 2-L, PaLM
2-L-IT, text-bison, gpt-3.5-turbo, gpt-4; scorer LLMs = pre-trained PaLM 2-L, text-bison (optimizer and scorer can
differ). PromptBreeder: PaLM 2-L as both optimizer and scorer. EvoPrompt: GPT-3.5 (closed) and Alpaca (open) as target
scorers; GPT-3.5 as the evolutionary operator LLM. No VLMs, no fine-tuning of any backbone.

**部署域 (Where)**
general (general-purpose NLP reasoning: math, commonsense, classification, generation, instruction induction). NOT
specialized to coding/GUI/office. The paradigm generalizes - the authors frame it as a universal prompt optimizer - but
the empirical scope is NLP benchmarks.

#### 评估指标

**评估指标**
success_rate (per-benchmark test accuracy) is the primary metric in all three. OPRO additionally:
optimization-convergence curves (per-step best/mean training accuracy with std-dev shading), transferability
(GSM8K-optimized -> MultiArith/AQuA), ablation studies on meta-prompt components (#exemplars, #trajectory-prompts,
temperature). PromptBreeder: cross-method comparison vs CoT / Plan-and-Solve / APE / OPRO on 8 arithmetic+commonsense
benchmarks; per-operator ablation (Appendix J.4); evolved-mutation-prompt quality analysis. EvoPrompt: comparison vs APE
/ human prompts across 31 datasets (BBH up to +25%), GA-vs-DE ablation, GPT-3.5-vs-Alpaca ablation. NO
skill-library-growth metric (no persistent library). NO economic-value metric. NO sample-efficiency-vs-RL baseline (that
comes later with GEPA).

**关键结论**
OPRO (PaLM 2-L scorer): GSM8K 80.2% zero-shot with 'Take a deep breath and work on this problem step-by-step.' (PaLM
2-L-IT optimizer) vs 71.8% for human 'Let's think step by step' (+8.4pp); +up to 50% on BBH over human prompts;
transfers GSM8K->MultiArith/AQuA. PromptBreeder (PaLM 2-L): GSM8K 83.9% zero-shot (vs OPRO's 80.2%) with the
unexpectedly minimal prompt 'SOLUTION'; beats CoT, Plan-and-Solve, APE across arithmetic (MultiArith 99.7, SingleEq
96.4, AddSub 87.8, SVAMP 90.2) and commonsense (SQA 71.8, CSQA 85.4, AQuA-RAT 62.2); evolves intricate hate-speech
classifiers on ETHOS. EvoPrompt: up to +25% on BBH over human-engineered prompts; outperforms APE and other automatic
prompt-generation baselines across 31 datasets; demonstrates GA/DE synergy with LLMs; both GPT-3.5 and Alpaca benefit.
Collective significance: established that LLMs can serve as text-space optimizers over natural-language instructions,
founding the 'prompt-as-evolvable-gene' paradigm that later SKILL.md self-evolution inherits.

#### 局限与挑战

**局限与挑战**
optimizer_quality (all three depend on a strong LLM as the optimizer/mutator - OPRO's gpt-4 handily beats gpt-3.5-turbo
and text-bison on TSP; weaker optimizers stall). scalability (OPRO's context-window limit makes large-scale optimization
hard - linear regression with high-dim data and large TSP instances fail; PromptBreeder's many rollouts are expensive -
the paper notes batched/threaded mutation as engineering work). eval-hacking / overfitting (OPRO Section 5.4 explicitly
analyzes overfitting to training-subset idiosyncrasies; semantically similar prompts can yield drastically different
accuracies - a noise floor the optimizer can latch onto). regression_risk (EvoPrompt GA's top-N and DE's
replace-only-if-better bound this, but no formal guarantee). transferability (cross-task/cross-model transfer
demonstrated but variable). doc_bloat (PromptBreeder's evolved prompts can grow verbose; OPRO and EvoPrompt less so).
controllability (NO human-in-the-loop in any of the three; the optimizer's creative direction is opaque).
catastrophic_forgetting (N/A - no weight updates).

#### 可借鉴要点

**可借鉴要点**
- META-PROMPT = OPTIMIZATION TRAJECTORY (OPRO's central reusable idea): instead of asking an LLM to 'edit this prompt for me', present the LLM with the FULL score-sorted history of past candidates (prompt, score) pairs plus a few task exemplars, and ask it to generate a NEW candidate that scores higher. The trajectory itself carries the gradient - the LLM performs in-context pattern recognition over good vs bad examples. This is the single most replicated design choice in the prompt-optimization literature and maps directly onto SKILL.md self-evolution: maintain a versioned history of (SKILL.md draft, eval score) and feed the whole trajectory to the meta-LLM when proposing the next draft, rather than editing in isolation. OPRO's empirical win (GSM8K 34% empty-string -> 80.2%) on a tiny 3.5% training subset proves that a short score-annotated trajectory is a remarkably sample-efficient learning medium.
- CO-EVOLVE THE MUTATION OPERATOR, NOT JUST THE ARTIFACT (PromptBreeder's self-referential hyper-mutation): PromptBreeder's decisive innovation over OPRO/EvoPrompt is that it evolves not only task-prompts but ALSO the mutation-prompts that govern how task-prompts are mutated (first-order hyper-mutation: 'Please summarize and improve the following instruction'). This is 'evolution of evolvability' - the system improves the way it improves itself. For SKILL.md self-evolution this is the deepest borrowable idea: maintain a small evolving pool of EDIT STRATEGIES (e.g. 'compress the failure-handling section', 'add a worked example for the trickiest step', 'rewrite the trigger conditions to be more specific') alongside the SKILL.md drafts themselves, and let the meta-LLM periodically refine the edit strategies based on which ones produced winning drafts. PromptBreeder's 9 mutation operators (direct, EDA, hyper-, Lamarckian, crossover+context-shuffle) are a concrete starting taxonomy of edit operators any SKILL.md evolver can adopt - especially the Lamarckian operator that reverse-engineers a prompt from a successful trace, which directly translates to 'distill a SKILL.md revision from a successful task trajectory'.
- POPULATION + DIVERSITY MAINTENANCE BEATS GREEDY HILL-CLIMBING (EvoPrompt + PromptBreeder consensus): EvoPrompt shows GA (population + crossover + top-N) and DE (population + 3-parent donor + greedy replace) both beat single-thread optimizers; PromptBreeder adds explicit diversity maintenance via BERT-cosine-similarity filtering (>0.95 pruned) in its EDA operator and random-batch fitness resampling. The lesson for SKILL.md self-evolution: keep a POPULATION of competing drafts (not a single canonical version), prune by similarity to avoid mode collapse, and use binary-tournament or fitness-proportionate selection so that diverse niche winners (best on different task types / user profiles) coexist. EvoPrompt's DE template (y = a + F(b-c)) is also worth piloting: ask the meta-LLM to produce a draft that combines one strong parent 'a' with a scaled 'difference' between two other parents 'b' and 'c' - a surprisingly effective text-space analog of vector arithmetic.

---

### ExpeL

> `idea_distill` · THU LeapLab, AAAI 2024(arXiv:2308.10144)。从成败轨迹蒸馏可复用 NL 见解/规则，带 重要性计数(ADD/UPVOTE/DOWNVOTE/EDIT，降至0裁剪)；成功轨迹存 Faiss 向量库做 RAG。 思想可迁移到 SKILL.md 的「见解沉淀+裁剪治理」。github LeapLabTHU/ExpeL

#### 基础信息

**名称**
ExpeL (Experiential Learning agent)

**提出机构**
Tsinghua University, LeapLab (THU). Authors: Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, Gao
Huang (corresponding). Funded by National Key R&D Program of China (2022ZD0114900), NSFC (62022048, U2336214, 62332019),
and Guoqiang Institute of Tsinghua University.

**发布时间**
arXiv v1 submitted 20 Aug 2023; v2 18 Dec 2023; v3 20 Dec 2024. Accepted at AAAI-24 (38th AAAI Conference on Artificial
Intelligence). [Oral status per task note; exact session unverified]

**论文链接**
https://arxiv.org/abs/2308.10144

**代码链接**
https://github.com/LeapLabTHU/ExpeL (project page: https://andrewzh112.github.io/expel)

**类型**
academic (AAAI-24 paper). Model weights never trained; method is purely prompt/experience-based and runs on closed-source API LLMs.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 ONLY. The agent's context is augmented with (a) a concatenated list of extracted natural-language insights
and (b) top-k retrieved successful trajectories used as in-context fewshot examples. NO model-weight updates (explicitly
designed for API-only models like GPT-4/Claude), NO tool evolution, NO architecture change. The paper likens this to
off-policy learning from a behavior policy's trajectories stored in an experience pool.

**技能是否独立制品**
是. Two reusable non-parametric artifacts: (1) a set of NL insights (each with an integer importance count) that act as
transferable rules; (2) a Faiss vectorstore of successful trajectories reusable as fewshot demonstrations. Form = memory
entries / NL rules + vector-indexed trajectories, NOT a .md/SKILL.md file on disk. Users can inspect/modify/remove
insights (interpreted as a strength vs finetuning).

**是否文档载体**
是 (leaning). Primary carrier is readable natural-language insight rules injected into the prompt; no embedded executable
code. It is 'instruction-document-centric' in spirit (NL SOP rules) even though the literal carrier is an in-memory
insight list rather than a markdown file on disk. So: 是 in form (NL instructions), 否 in literal SKILL.md-on-disk
packaging.

#### 技能表示

**技能编码方式**
自然语言SOP/见解 (NL insight rules, each a short guideline like 'consider the answer might be in the observations already
made') + 向量嵌入 (Faiss vectorstore of successful trajectories embedded with all-mpnet-base-v2). Insights are stored as NL
text with an integer importance-count side-state; trajectories are stored as raw text + dense embeddings.

**技能粒度**
见解(insight) / 策略规则. Atomic NL guidelines at the strategy-rule level (smaller than a full skill package, larger than a
single action): e.g., cross-task best practices and prevalent-failure-pattern avoidance rules. Trajectories are full
sub-task workflows used as fewshot demonstrations.

#### SKILL.md_专属维度

**文档形态**
Form = a flat list of NL insight strings, each carrying an integer importance count; at inference the FULL list is
concatenated (ι̂ = concat(ι1,ι2,...)) and prepended to the task specification (Fig. 3 prompt template). Insights are
bounded to fit within the LLM context window (paper explicitly notes 'extracted insights do not exceed the current LLM
token limit'); lifelong-learning regime would require insight retrieval (noted as future work). No YAML frontmatter, no
markdown file, no multi-file package. Typical per-insight length = 1-3 sentences; typical list size = [uncertain, on the
order of tens of insights per environment].

**编辑粒度**
有界增删替换 via four atomic operators on the insight set: ADD (new insight, initial importance count=2), EDIT (rewrite
content of an existing insight), UPVOTE (agree, +1 count), DOWNVOTE (disagree, -1 count). No whole-document rewrite, no
PATCH/diff format; each extraction step applies one operator per insight. Trajectory library grows by append-only
ingestion of whole trajectories (no trajectory editing).

**版本与门控**
Count-based implicit gating only: an insight is auto-pruned when its importance count reaches 0 (DOWNVOTE-dominated). NO
held-out validation gate, NO git branch frontier, NO Pareto/DAG lineage, NO human review gate, NO staging+backup. The
importance count acts as a soft vote-based popularity gate; there is no separate held-out scoring step for individual
insights (only the end-to-end 4-fold task success rate validates the whole library).

**文档来源**
成功轨迹归纳 + 失败轨迹蒸馏 + 执行录像回放 + session 经验提取. Insights are distilled offline from two contrastive sources drawn from the
experience pool: (a) success/failure pairs of the SAME task (failure-trajectory distillation), and (b) chunks of L
successes from DIFFERENT tasks (success-trajectory induction / best-practice pattern mining). Trajectories are gathered
autonomously via trial-and-error with Reflexion-style self-reflection retries on failure (up to Z retries per training
task).

**跨载体迁移**
跨任务 + 跨基准 (demonstrated). Positive forward transfer HotpotQA (source) -> FEVER (target): source-domain insights are
'finetuned' to the target domain via a prompt template that adapts them using a few target-task demonstrations (Fig. 4).
Agent with task demos outperforms agent without. 跨模型 (claimed in principle: 'not restricted to specific language
models'; gpt-4 extractor > gpt-3.5 extractor shown). 跨agent-harness / 跨user: NOT demonstrated (it is a research agent,
not a harness-portable artifact).

**技能库治理**
Importance-count retirement (count->0 prunes an insight) + Faiss vector index over trajectories. This is the key
governance mechanism: a simple, self-cleaning, bounded-growth rule library driven by UPVOTE/DOWNVOTE votes during
extraction. NO explicit dedup/merge of semantically similar insights, NO curator loop, NO Lotka-Volterra dynamics, NO
hierarchical index (insight list is flat; retrieval over insights is explicitly left as future work). Trajectory library
grows monotonically (no retirement of trajectories).

**失败记忆**
是 (contrastive-pair form). Failure trajectories are NOT stored as standalone anti-patterns; instead each failure is
paired with a success on the SAME task and fed to LLM_insights to extract/revise insights that encode 'prevalent failure
patterns' and corrective best practices (the prompt explicitly emphasizes 'extracting prevalent failure patterns or best
practices'). DOWNVOTE acts as negative feedback that retires misleading insights. No explicit
failure-signature+attribution+remedy structuring and no rejected-edit buffer; the negative signal is folded into the
insight vote count.

**编辑安全**
Interpretability + user-editability + bounded growth (count pruning). The paper explicitly frames NL
insights/trajectories as inspectable/modifiable/removable by users (a safety/controllability strength vs finetuned
weights). Bounded editing operators (ADD/EDIT/UP/DOWN) prevent destructive wholesale rewrites. NO pre-edit
backup/rollback, NO explicit eval-hacking guard (no held-out split between insight-extraction and evaluation), NO
secret/injection scan, NO human-in-the-loop gate, NO scope-boundary enforcement (insights are pure text, so source-code
scope is moot).

**协同进化**
skill-only with role separation. The single agent's context (insights + retrieved trajectories) is the only thing that
evolves; tools (Wikipedia Docstore API, WebShop/ALFWorld action spaces) are fixed, no other skills co-evolve, no
separate verifier co-evolves. However there IS a clean role separation among LLMs: LLM_ReAct (policy/actor,
gpt-3.5-turbo), LLM_reflect (Reflexion reflector), LLM_insights (extractor, gpt-4-0613) - a soft generator/extractor
division of labor, but not a co-evolutionary loop.

#### 自进化机制_How

**进化方法范式 (How)**
reward-based (text feedback from binary success/failure outcomes) + imitation_demonstration (retrieved successful
trajectories injected as fewshot in-context demonstrations). NOT gradient/SFT/RL on weights, NOT
population-evolutionary, NOT rollout-optimization in the prompt-tuning sense. The closest framing in the paper is
'off-policy learning from a behavior policy's experience pool' realized entirely in text/prompt space. Insight
extraction is an LLM-driven abstraction step over contrastive trajectory pairs.

**学习信号来源**
成败轨迹 (success/failure trajectory outcomes from the environment) + 自我反思 (Reflexion-style LLM_reflect outputs during
gathering). The environment provides a deterministic binary success signal per trajectory; insights are derived by
comparing success vs failure on the same task and by pattern-mining across successful trajectories.

**奖励粒度**
outcome (结果). Binary per-trajectory success/failure (exact-match for HotpotQA/FEVER, task-completion for ALFWorld,
all-attribute-match for WebShop). No process/step-level reward; no dense reward. WebShop additionally reports a mean
reward r in [0,1] as a soft outcome metric.

**学习范式**
offline + off-policy. A distinct offline TRAINING stage (gather trajectories on training tasks -> extract insights ->
build vectorstore) precedes a single-shot EVALUATION stage (no retries at deployment). Off-policy: the agent learns from
trajectories produced by a behavior policy (including failed attempts and Reflexion-retry attempts), analogous to
replay-buffer learning. NOT online, NOT on-policy, NOT sleep-time scheduled (though the offline training stage is
conceptually sleep-time-compatible).

#### 进化时机_When

**进化时机 (When)**
inter-test-time (任务间离线). Insight extraction and library construction happen once, offline, between training-task
experience gathering and evaluation-task deployment - explicitly NOT during a single task at test time (deployment is
single-shot, no retries, no online learning). Paper contrasts this with Reflexion's intra-task retry-based improvement.

**触发方式**
事件触发 (after the experience-gathering loop completes over N training tasks) + 失败触发 (Reflexion retry up to Z times per
training task during gathering, triggered by task failure). It is a one-shot batch training trigger, not periodic/cron,
not curriculum-driven, not usage-driven at deployment.

#### 存储与检索

**技能库结构**
向量库 (Faiss vectorstore of successful trajectories) + 扁平 insight list (flat, unordered set of NL insights with importance
counts). NO hierarchy, NO git branches, NO DAG lineage, NO cloud registry. The experience pool B holds ALL trajectories
(success+failure) for insight extraction; only successes are indexed in Faiss for retrieval.

**检索/复用方式**
语义相似度 (Faiss kNN with all-mpnet-base-v2 embedder; ranking by maximum inner-product task similarity between the
evaluation task and stored successful trajectories; top-k retrieved as fewshot in-context examples). For insights: NO
retrieval - the FULL insight list is concatenated into the prompt; the paper explicitly flags insight retrieval as
future work for lifelong learning. Ablation shows task-similarity ranking > reason-similarity ranking > random sampling.

#### 验证与反馈

**验证方式**
执行验证(execution-based) + 留出评估 (4-fold cross-validation on benchmarks, mean+std reported). NO LLM-judge gate on individual
insights, NO surrogate verifier, NO validation gating that decides whether an insight is admitted (admission is governed
solely by the importance-count vote during extraction). Insights are validated only indirectly via end-to-end task
success-rate improvement. Functional-correctity metrics: exact-match (HotpotQA/FEVER), task completion (ALFWorld),
attribute-match (WebShop).

**错误纠正**
自我修订 + 定向 diff 修补 (insight-level EDIT operator rewrites a misleading insight; DOWNVOTE retires it via count decay;
Reflexion self-reflection during gathering produces corrective reflections for the next retry). NO rollback (insights
once added cannot be reverted, only voted down), NO whole-library rewrite, NO re-planning at deployment (single-shot).
Emergent self-correction behavior observed at inference: agent reverts wrong actions mid-trajectory (e.g., puts back a
wrong object in ALFWorld).

#### 环境与基座

**测试环境**
通用 / Web + tool-call + text-GUI. HotpotQA (multi-hop QA via Wikipedia Docstore search API), ALFWorld (text-based
household embodied tasks), WebShop (text-based online-shopping multi-step decision-making), FEVER (fact verification,
transfer target). All four are text-observation deterministic environments following the ReAct benchmark suite.

**底座模型**
GPT (closed-source). Policy/actor = gpt-3.5-turbo-0613 (all agents incl. baselines use this at evaluation, temperature
0, greedy). Insight extractor LLM_insights = gpt-4-0613 (ablation shows gpt-4 > gpt-3.5-turbo at following the
ADD/EDIT/UPVOTE/DOWNVOTE operator instructions and hallucinates less). Reflector LLM_reflect = same family. Optimizer
(extractor) and target (policy) ARE separated and use different model tiers. Embedder = all-mpnet-base-v2 (Song et al.
2020) for Faiss retrieval.

**部署域 (Where)**
general (通用). Tested across diverse decision-making domains (QA, embodied household, web shopping, fact verification);
not specialized to a single vertical. The method is domain-agnostic by design (any ReAct-style task with a binary
success signal).

#### 评估指标

**评估指标**
success_rate (primary, 4-fold mean+std-error) + generalization (cross-task forward transfer HotpotQA->FEVER) +
sample_efficiency (ablation: effect of number/diversity of gathered experiences on downstream SR) + skill_library_growth
(implicit: insight set size and vote dynamics). Additional: mean reward r in [0,1] for WebShop, per-task-type breakdown
for ALFWorld. No explicit cost/token-economic metric.

**关键结论**
Main (Fig.5): ExpeL consistently beats ReAct and Act on all three domains. HotpotQA SR: ExpeL 39% vs ReAct 28.0 +/-1.4
(insights-only 36% / retrieve-only 31% -> synergistic). ALFWorld SR: ExpeL 59% (insights-only 50% / retrieve-only 55%).
WebShop: insights/retrieve near-equilibrium (37%/38% SR, 0.675/0.67 reward). Matches/beats Reflexion R3 without retries
(HotpotQA 39% vs Reflexion R3 40%; ALFWorld 59% vs Reflexion R3 54%). Ablations: (1) experience quantity+diversity
matters (fewshot-only = no gain over ReAct; Reflexion-gathered > ReAct-gathered); (2) learned insights > hand-crafted
insights (39% vs 32%); (3) adding Reflexion reflections INTO insight extraction HURTS (29%, hallucinations); (4) gpt-4
extractor > gpt-3.5-turbo extractor; (5) task-similarity retrieval > reason-similarity > random. Transfer:
HotpotQA->FEVER positive forward transfer, larger with target task demos ('finetuning'). Emergent abilities: analytical
deduction, world-model belief update (e.g., ALFWorld pan now searched on stoveburners), mid-trajectory self-correction.

#### 局限与挑战

**局限与挑战**
transferability (only HotpotQA->FEVER transfer tested; WebShop SR approaches the low end of Reflexion's range) +
optimizer_quality (depends on a strong insight-extractor LLM; gpt-4 materially better than gpt-3.5-turbo) +
scalability/doc_bloat (insights must fit within the context window; lifelong/long-horizon learning would require insight
retrieval, explicitly future work) + modality (text-only observations; no VLM/image support) + closed-source dependency
(API-only LLMs; open-source-LLM variant unexplored) + controllability/theoretical (prompting-based, lacks RL's
theoretical underpinnings). NO catastrophic-forgetting risk (weights frozen). NO explicit eval-hacking guard (no
held-out split between insight extraction and final eval).

#### 可借鉴要点

**可借鉴要点**
(1) Importance-count-based insight sedimentation + count-to-zero auto-pruning as library governance: every SKILL.md rule
carries an integer vote count with four atomic operators (ADD at count=2 / UPVOTE +1 / DOWNVOTE -1 / EDIT rewrite) and
is auto-retired when the count hits 0. This gives a simple, self-cleaning, bounded-growth, fully-interpretable rule
library that learns from contrastive success/failure pairs WITHOUT any held-out validation gate or human review -
directly portable to SKILL.md governance. (2) Dual memory modes that are synergistic and complementary: abstracted NL
insights (generalization, dominant for reasoning tasks like HotpotQA) + a Faiss vectorstore of past successful
trajectories retrieved as fewshot demonstrations (imitation, dominant for execution-heavy tasks like ALFWorld). A
self-evolving SKILL.md system should maintain BOTH: distilled rules in the doc AND a searchable archive of successful
run transcripts, and pick the balance per task type. (3) Offline inter-task experience gathering with Reflexion retries
-> contrastive success/failure pairs drive insight extraction -> deploy single-shot with NO retries: separate a
dedicated offline 'study session' (gather experiences, extract/revise insights) from a fast single-shot inference
deployment; do NOT learn online during user-facing tasks. Plus the cheap-but-impactful lesson: use a stronger LLM
(gpt-4) as the offline insight EXTRACTOR even if the deployed policy is a cheaper model (gpt-3.5).

#### 不确定字段

- release_date (AAAI-24 oral/poster status - task note says Oral; arXiv dates confirmed but conference session unverified)
- doc_form (exact typical token length / list size of the extracted insight set per environment - paper does not report counts)

---

### Agent Workflow Memory (AWM)

> `idea_distill` · CMU+MIT, ICML 2025(arXiv:2409.07429)。归纳模块从经验轨迹提取通用子例程(workflow) 文本块，抽象掉示例特有上下文，注入提示记忆。在线(流式测试从成功轨迹归纳)+离线两种。 仅~40 示例即见效。思想≈「把验证过的行动链固化为可复用文档」。github zorazrw/ agent-workflow-memory

#### 基础信息

**名称**
Agent Workflow Memory (AWM)

**提出机构**
Carnegie Mellon University (CMU) + Massachusetts Institute of Technology (MIT). Authors: Zora Zhiruo Wang, Jiayuan Mao (MIT), Daniel Fried, Graham Neubig (CMU).

**发布时间**
2024-09-11 (arXiv v1); published at ICML 2025 (Poster), PMLR 267:63897-63911.

**论文链接**
https://arxiv.org/abs/2409.07429

**代码链接**
https://github.com/zorazrw/agent-workflow-memory

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 (Context memory & prompt). Workflows are text blocks induced from experience trajectories and integrated
into the agent's prompt/context memory (system prompt or auxiliary context). No model weight updates, no
tool/action-space creation, no architecture change. Purely non-parametric, in-context memory evolution.

**技能是否独立制品**
Yes. Each workflow is an independent reusable text artifact stored in a flat workflow memory. Form = a text block
pairing (1) an NL workflow description (goal/sub-goal summary) with (2) an ordered trajectory of steps, where each step
contains an NL environment-state description, NL reasoning, and an executable action program (e.g., click('42'),
fill('130','{RepositoryName}')). Workflows are segmented by double-line breaks and stored separately.

**是否文档载体**
Hybrid (混合). The workflow is a human-readable instruction document (NL goal + state + reasoning) with embedded
executable action code calls. It functions as a mini-SOP whose action layer is executable programs over the environment.
The dominant carrier is readable instruction text augmented with action code, so it leans toward 'document-like skill'
rather than pure code or pure vector.

#### 技能表示

**技能编码方式**
Natural-language SOP (sub-routine style) with embedded executable action programs. A workflow = NL description + step
list [(NL state, NL reasoning, action program), ...]. The LM-based induction module produces these via a single
prompting pass; outputs are segmented into separate workflow text blocks. Not vector embeddings, not a graph, not a
multi-file package.

**技能粒度**
Sub-task workflow (reusable sub-routine). Workflows are deliberately extracted at a finer granularity than full task
instructions (e.g., 'search for a product on Amazon' rather than 'Buy dry cat food...'). Each workflow has >=2 steps.
New complex workflows compose earlier primitive workflows (e.g., 'find a place by name' -> 'get zip code of a place').

#### SKILL.md_专属维度

**文档形态**
Instruction + embedded code blocks (hybrid). Each workflow is a structured text block: a header line (## domain:
workflow_name) + an NL goal description + a numbered/segmented step list. Each step mixes (a) NL environment-state
description, (b) NL reasoning/justification, (c) an executable action program call. Concrete values are abstracted to
descriptive variable names ({product-name}, {RepositoryName}). Typical length: a few steps per workflow (~2-5 steps).
Workflow count per website is small (~7.4 on WebArena, ~7.3 on Mind2Web). Memory is flat (no YAML frontmatter, no
multi-file packaging).

**编辑粒度**
Wholesale generation + append-only addition. The LM induction module generates entire workflows from one or more
experiences in a single prompt; induced workflows are appended to the flat memory (M + W). No bounded add/delete/replace
diff, no PATCH, no destructive edits, no in-place rewrite. Complex workflows are built compositionally on top of earlier
ones (snowball), but each new workflow is a freshly generated artifact, not an edit of an existing one.

**版本与门控**
Minimal. (1) Online mode: an LM-evaluator (Pan et al. 2024 AutoEval) emits a binary success label; only trajectories
judged successful are turned into workflows (success-gated induction). (2) Offline mode: workflows are induced from
gold-labeled training examples (assumed correct). No held-out validation, no Pareto-front selection, no git branching,
no DAG lineage, no staging+backup, no human review-gate, no rollback. Once a workflow is added it is never versioned or
reverted.

**文档来源**
Two modes. Offline = success/gold-trajectory induction from annotated training examples (offline benchmark training).
Online = self-generated successful trajectories extracted during streaming test sessions (session experience
extraction). In both cases the source is successful action trajectories; the induction LM abstracts away
example-specific context. Not human-initialized, not execution-video replay, not community-shared.

**跨载体迁移**
Cross-task, cross-website, and cross-domain transfer are explicitly evaluated WITHIN the benchmarks (Mind2Web
cross-task/website/domain splits; WebArena cross-template subset). Online AWM generalizes better as train-test
distribution gaps widen (+8.9 to +14.0 absolute points). NOT demonstrated cross-model (only GPT-3.5/GPT-4 used) nor
cross-agent-harness. Workflows are website-scoped (per-website memory), so transfer across entirely different sites is
limited; offline AWM degrades when the domain gap is large.

**技能库治理**
Minimal / soft dedup. Flat per-website workflow memory (all workflows for a website coexist). The induction prompt
instructs 'Do not generate similar or overlapping workflows', which is the only de-duplication mechanism. The paper
measures function-overlap as a quality metric (0.08 on WebArena, 0.20 on Mind2Web) but performs no active
merge/retirement/archival. No Lotka-Volterra dynamics, no curator loop, no hierarchical index, no retirement policy.
Library growth is unbounded (append-only).

**失败记忆**
No explicit anti-pattern / failure memory. Failure is handled only by exclusion: unsuccessful trajectories are NOT
induced into workflows (filtered by the LM-evaluator success gate in online mode). Failures are discarded rather than
retained; there is no failure-signature store, no attribution/remedy buffer, no rejected-edit buffer, no negative
feedback to veto future similar workflows. The paper acknowledges online AWM can still induce incorrect workflows from
mis-judged self-trajectories.

**编辑安全**
Minimal/None. No scope boundary enforcement (workflows are text, not source code, so there is no .md-vs-code separation
concern), no pre-edit backup or rollback, no anti-eval-hacking measures, no confirmation gate, no human-in-the-loop, no
bounded-edit protection (append-only is the only structural safeguard). The sole gate is the LM-evaluator binary success
judgment in online mode. Context-length overflow risk from append-only memory is not actively guarded.

**协同进化**
skill-only (with a weak emergent skill-skill effect). Workflows evolve independently; the tool/action space is fixed
(built-in CLICK, TYPE, FILL, etc.) and never created or modified. The LM evaluator is a fixed external module (no
generator-verifier coevolution). There is an emergent compositional effect (new complex workflows build on earlier
simpler ones), but this is not a structured skill-skill coevolution mechanism.

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration + non-gradient text-space rollout optimization. The LM induction module generalizes successful
trajectories into reusable text workflows (imitation from success, abstracted). No reward-based RL, no gradient/SFT, no
population/evolutionary search. It is best characterized as LM-based experience generalization into a text-memory prompt
augmentation (a non-gradient, text-space optimization of the agent's context).

**学习信号来源**
Success/failure trajectories (binary). Offline: gold-labeled canonical examples (assumed correct). Online: an
LM-as-judge evaluator (AutoEval, Pan et al. 2024) emits a binary success label over the self-generated trajectory. No
environment reward shaping, no self-reflection, no held-out validation score, no tool-success metric beyond task
success.

**奖励粒度**
Outcome (result-level). The success judgment is at the whole-trajectory/task level (did the trajectory solve the instruction?), not a per-step process reward.

**学习范式**
Both offline and online. Offline = induce from training examples before inference (off-policy, sleep-time-like). Online
= induce from the agent's own self-generated successful trajectories during streaming test queries (on-policy,
inter-test-time). Not gradient-based; purely prompt/context-space.

#### 进化时机_When

**进化时机 (When)**
Both. Offline = sleep-time / inter-test-time (induce once from training examples before serving test queries). Online =
inter-test-time (after finishing one streamed test task and judging it successful, induce workflow(s) and add to memory
before the next task). NOT intra-test-time (no induction occurs in the middle of a single task execution).

**触发方式**
Event-triggered (post-success) + curriculum-driven. Online: after each test task completes, if judged successful, induce
workflow(s). A snowball/curriculum effect emerges: increasingly complex workflows are built on earlier induced workflows
(e.g., 'find a place' enables 'get zip code of a place'). Not periodic/cron, not failure-triggered (failures do not
trigger induction), not usage-driven retrieval. Offline: a one-shot batch induction over all training examples per
website.

#### 存储与检索

**技能库结构**
Flat, per-website workflow memory. All induced workflows for a given website are concatenated into the agent's auxiliary
memory/context. No hierarchy, no vector store, no graph/DAG lineage, no cloud registry. The paper explicitly groups
examples by website to keep each local workflow collection small and relevant.

**检索/复用方式**
None / all-in-context injection (generation-as-retrieval is NOT used). AWM loads ALL workflows induced for the relevant
website into the prompt for every test task on that website; there is no per-query semantic-similarity retrieval, no
BM25+embedding rerank, no workflow matching. The only scoping is website-level grouping. This is a deliberate contrast
with retrieval-based exemplar methods like Synapse/ExpeL. (The abstract's phrase 'selectively providing workflows'
refers to website-level selection, not per-query retrieval.)

#### 验证与反馈

**验证方式**
LLM-judge (online) + gold-label assumption (offline). Online: the LM-evaluator (AutoEval) provides a binary success gate
that decides whether a trajectory is eligible to be distilled into a workflow. WebArena additionally provides
execution-based functional-correctness evaluation for reporting. No held-out validation gating of the induced workflows
themselves, no surrogate verifier beyond the success judge, no multi-model debate. Workflow quality is assessed post-hoc
via #workflows, coverage, function-overlap, and utility-rate metrics.

**错误纠正**
Limited / filter-at-induction. Errors are handled by exclusion: only successful trajectories are distilled, so noise is
filtered upstream. Once a workflow is induced it is never revised, rolled back, diff-patched, or bounded-edited. The
paper notes online AWM can still inject incorrect workflows (when self-predicted trajectories are mis-judged as
successful) and that agents sometimes struggle to diverge from workflow guidelines (slightly lower action F1 than
MindAct).

#### 环境与基座

**测试环境**
Web navigation (WebArena + Mind2Web). WebArena: 812 execution-based tasks on 5 websites
(e-commerce/CMS/Reddit/GitLab/Maps). Mind2Web: cross-task/website/domain splits over 200+ domains.

**底座模型**
GPT (closed-source). GPT-4 (gpt-4-0613) and GPT-3.5-turbo, temperature 0.0. The SAME model is used for workflow
induction and for agent action generation (no optimizer/target separation). Text-only inputs (accessibility-tree webpage
representation); no vision-language model.

**部署域 (Where)**
Specialized (web navigation / digital GUI agent domain). General-purpose web tasks (travel, shopping, social media, dev collaboration, content management).

#### 评估指标

**评估指标**
success_rate (task-level and step-level SR, element accuracy, action F1); generalization (cross-task / cross-website /
cross-domain / cross-template); sample_efficiency (rapid learning from ~40 examples); skill_library_growth (number of
workflows, coverage, function-overlap, utility rate); cost (average number of steps per successful task).

**关键结论**
WebArena: 35.5% total SR vs BrowserGym_ax-tree 23.5% (+12.0 absolute, +51.1% relative) and vs AutoEval 20.2%;
outperforms SteP (14 human-written workflows) by +7.6% relative without any human supervision; reduces
steps-per-successful-task by ~2.0 vs baseline (~40.8 fewer than AutoEval). Mind2Web cross-task: +24.6% relative step SR
(AWM_4 step SR 45.1 vs MindAct 36.2). Cross-template subset: 33.2% SR (still best). Online AWM generalization: +8.9 to
+14.0 (up to +16.9) absolute points over MindAct across cross-task/website/domain, with margins widening as distribution
gap grows. Sample efficiency: most gain acquired within first ~40 streamed examples. Workflow quality: ~7.4
workflows/website (WebArena), utility rate 0.94, function overlap 0.08.

#### 局限与挑战

**局限与挑战**
transferability (offline AWM degrades as train-test domain gap widens; workflows are website-scoped); regression_risk /
optimizer_quality (online AWM induces workflows from model-predicted trajectories that are 'not always correct', so
mis-judged successes inject incorrect workflows that can degrade performance); doc_bloat / scalability (append-only flat
memory with no retirement; all workflows loaded into context with no retrieval, risking context overflow at scale);
controllability (agents sometimes cannot diverge from workflow guidelines when the state diverges, lowering action F1);
single closed-source backbone family (GPT-3.5/4); text-only observations (no vision); dependence on a reasonably strong
LM for both induction and generation.

#### 可借鉴要点

**可借鉴要点**
- Abstract away example-specific context when distilling skills. AWM's induction prompt deliberately replaces concrete values with descriptive variable names (e.g., 'dry cat food' -> '{product-name}') and extracts sub-routines finer than full task instructions. This makes a skill reusable across many tasks, and empirically beats retrieving concrete full-trajectory exemplars (Synapse): +5.0 element accuracy, +4.0 step SR. Lesson for SKILL.md: write skills as generalized, parameterized SOPs, not literal transcripts.
- Gate self-evolution on a binary success verdict before committing a skill. In the supervision-free online mode, an LM-evaluator judges each trajectory successful/failed, and ONLY successes are distilled into the memory. This is a cheap, label-free quality gate that lets an agent autonomously grow its SKILL.md from its own verified wins while filtering most noise. (Caveat they note: the judge can be wrong, so some bad skills still leak in.)
- Snowball via append-only compositional memory. AWM never destructively edits workflows; it only appends new ones, and later complex workflows are built by composing earlier primitive ones ('find a place' -> 'get zip code of a place'). This produces a curriculum effect with fast early gains (~40 examples). Lesson: for a self-evolving SKILL.md, prefer non-destructive append of new, composable skills over risky in-place rewrites, so capabilities accumulate without regression.
- Full-context injection beats retrieval at small scale but won't scale. AWM loads all (~7) per-website workflows into the prompt with no retrieval and still wins. This suggests that for a small, well-scoped SKILL.md library, simple full-context loading is fine; but the append-only, no-dedup, no-retirement design is an acknowledged scalability ceiling that future SKILL.md systems should address with retrieval + library governance.

---

### MUSE (Learning on the job)

> `idea_distill` · 2025(arXiv:2510.08002)。层次化记忆 M={战略洞见, 过程层 SOP 文档(≈过程型 SKILL.md), 工具层动态指令}。Plan-Execute-Reflect-Memorize 循环。仅~10% 任务即累积记忆。SOP 文档 形态与 SKILL.md 高度同构。github KnowledgeXLab/MUSE

#### 基础信息

**名称**
MUSE (Memory-Utilizing and Self-Evolving)

**提出机构**
Central South University; Shanghai Artificial Intelligence Laboratory; Fudan University; Shanghai Innovation Institute;
Zhejiang University (corresponding: Haifeng Li, Botian Shi)

**发布时间**
2025-10-09 (arXiv v1)

**论文链接**
https://arxiv.org/abs/2510.08002

**代码链接**
https://github.com/KnowledgeXLab/MUSE

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示. No model weight updates / no fine-tuning; evolution is entirely in a hierarchical natural-language Memory
Module M = {strategic, procedural, tool} that is injected into the agent's system prompt and observation stream,
extending capability beyond static pretrained parameters.

**技能是否独立制品**
Yes. Memory is persisted as standalone reusable JSON artifacts (procedural_memory.json, strategic_memory.json,
tool_memory.json) that are loaded at startup, updated after each task, and carried across runs/iterations. Form: memory
entries + SOP documents (structured natural language), not code.

**是否文档载体**
Yes (structurally). The Procedural Memory is a readable SOP ('Standard Operating Procedure') instruction document with
preconditions/steps/notes, homologous to a procedural SKILL.md; however it is encoded as structured JSON rather than
markdown. Strategic Memory = Dilemma->Strategy key-value guidance; Tool Memory = description+instruction. So 'yes' in
spirit (instruction-document-centric) but JSON-serialized rather than .md files.

#### 技能表示

**技能编码方式**
Natural-language SOP (procedural: platform->{operation->{preconditions, steps as 'A -> B -> C', notes}}) + key-value
pairs (strategic: pattern_key -> pattern+rationale) + structured JSON fields (tool: tool_description /
tool_instruction). All content is LLM-agnostic natural language; no vector embeddings, no executable code as the skill
carrier.

**技能粒度**
Hierarchical across granularities: Strategic = 策略规则/insights (max 10 high-level resolution patterns); Procedural = 子任务
workflow SOPs (multi-step operation guides indexed by application); Tool = 原子动作 (single-tool usage guidance).

#### SKILL.md_专属维度

**文档形态**
Three JSON files. Procedural SOP = nested dict {<platform_or_application>: {<operation_name>: {preconditions, steps
('Open -> Select -> Save -> Verify'), notes}}}; only a lightweight outline index is loaded into the system prompt at
startup (dict_to_outline_str), full content fetched on demand via a dedicated memory tool (index/content separation to
respect context limits). Strategic = {<pattern_key>: '<pattern_statement + short rationale>'}, capped at 10 items, fully
loaded into system prompt. Tool = {<tool_name>: {tool_description, tool_instruction}}, static description in system
prompt + dynamic instruction appended to observation after tool use. Pure natural-language instruction content (no
embedded code blocks, no YAML frontmatter). Typical token length not reported; strategic kept concise (<=10 items),
procedural index kept lightweight to avoid context-window bloat.

**编辑粒度**
Bounded incremental update + post-task global refinement merge. Procedural memory updated via deep_update (bounded
add/replace of new SOP entries immediately after a successful sub-task); after the overall task, an LLM 'Merge Expert'
prompt performs deduplication, platform canonicalization, operation clustering and consolidation. Strategic memory
extracted then merged via a 'Resolution Patterns Merge Expert' that consolidates new+old and enforces a hard <=10 item
cap. Not whole-document rewrite, not minimal-diff PATCH; closest to bounded add/delete/replace + merge consolidation.

**版本与门控**
No git-branch / DAG / Pareto / held-out validation gating. Quality gate is (a) success-gated distillation: only
Reflect-Agent-verified SUCCESSFUL sub-task trajectories are distilled into Procedural Memory; (b) an independent
verifier (Reflect Agent) using a 3-axis checklist acts as the adoption gate; (c) LLM-merge-expert prompts perform
dedup+size-cap as soft governance. For the TAC full benchmark the accumulated memory was frozen after 3
continual-learning rounds. No explicit pre-edit backup/rollback or version history.

**文档来源**
Primarily 成功轨迹归纳 (successful sub-task trajectories distilled into SOPs by Reflect Agent) + session 经验提取 (post-task
distillation of dilemmas into Strategic Memory and tool-usage into Tool Memory). Failure trajectories produce an
in-session failure-cause-analysis report R_fail used for replanning (not directly written to a persistent anti-pattern
store). No human initialization; fully autonomous generation.

**跨载体迁移**
跨模型 + 跨任务. Memory is natural-language and LLM-agnostic: demonstrated transfer of memory accumulated by Gemini-2.5-Flash
to DeepSeek-V3 (S_partial 28.01%->36.75%), and zero-shot generalization to unseen hard tasks (23.65%->33.41%) and to the
full 175-task TAC benchmark. No cross-harness (Claude/Codex/Cursor) or cross-user/community sharing tested; all
evaluation within the single TAC benchmark.

**技能库治理**
去重合并 + 灰尘清理(curator/merge-expert loop) + 层次化索引 + size cap. merge_application_prompt canonicalizes platform names,
clusters by operation intent, consolidates duplicates, adds preconditions/notes; merge_methodology_prompt enforces a
hard maximum of 10 strategic patterns and merges overlapping ideas. Hierarchical index: platform -> operation ->
{preconditions, steps, notes}. No retirement/archive/Lotka-Volterra/population pruning; procedural growth is otherwise
unbounded (potential bloat risk).

**失败记忆**
Partial. On failure the Reflect Agent emits a failure-cause-analysis report R_fail fed back to the PE Agent for
replanning (in-session negative feedback), and the summarize prompt also captures 'Reflections on Failures' lessons; the
retry path additionally DISABLES procedural-memory retrieval to force novel exploration (an implicit
anti-overfitting-to-bad-skill mechanism). However there is no dedicated persistent anti-pattern / rejected-edit buffer /
failure-signature store carried as structured memory across runs.

**编辑安全**
Limited explicit safety machinery. No human-in-the-loop (framework is explicitly 'without human intervention'); no
pre-edit backup/rollback; no git versioning. Implicit bounds: edits confined to the three memory JSON files (never
source code), success-gating prevents junk-SOP adoption, per-sub-task max-action cap N=20 prevents runaway loops, and
retry can bypass memory to escape bad knowledge. No eval-hacking defense, secret/injection check, or destructive-rewrite
guard mentioned.

**协同进化**
skill-tool + generator-verifier协同. The three memory types (strategic/procedural/tool) are co-distilled and co-refined by
the same Reflect Agent after each task (Tool Memory evolves alongside the skill SOPs). Architecturally a
generator-verifier pair: PE Agent (generator/executor) vs Reflect Agent (independent verifier/supervisor) sharing the
same toolset, with the verifier producing the learning signal.

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration (distill verified-successful action trajectories into reusable SOPs) + LLM-based 自我反思 (Reflect
Agent). Non-gradient, text-space experience accumulation/deduplication via prompt-driven merge experts. No RL, no SFT,
no population evolution. Closest to trajectory-to-memory distillation with LLM-judge gating.

**学习信号来源**
成败轨迹 (success/failure of sub-tasks judged by Reflect Agent) + 自我反思 (Reflect Agent's autonomous checklist) + 环境反馈 (active
verification: the Reflect Agent uses the same tools to interact with the environment and cross-check key info rather
than trusting the executor's claims). No external reward model.

**奖励粒度**
Hybrid. Process-level signal: Reflect Agent evaluates each sub-task against a 3-axis checklist
(truthfulness/deliverable/data-fidelity) and checkpoint progress; Outcome-level signal: binary task-full-completion flag
S_full feeding the official S_partial metric.

**学习范式**
On-policy + online (intra-test-time) accumulation during task execution, with inter-test-time carry-over of the memory
across sequential tasks and 3 continual-learning rounds. No off-policy replay buffer; no dedicated sleep-time/offline
replay phase (all learning happens live in the loop).

#### 进化时机_When

**进化时机 (When)**
intra-test-time (Reflect+Memorize after EACH sub-task attempt -> immediate SOP reuse) + inter-test-time (carry
accumulated memory across tasks and across the 3 continual-learning iterations; frozen snapshot used for
full-benchmark/generalization eval). Not sleep-time (no overnight idle replay).

**触发方式**
事件触发. After each sub-task completion or max-action-limit -> Reflect Agent evaluate/distill; after overall task
completion -> full-memory upgrade (strategic dilemma extraction, tool codification, dedup/merge refinement). Not
periodic/cron/curriculum/tool-degradation driven.

#### 存储与检索

**技能库结构**
层次化 + 技能文件目录. Procedural = hierarchical platform->operation->{preconditions,steps,notes} stored as
procedural_memory.json; Strategic = flat key-value dict (<=10) in strategic_memory.json; Tool =
tool_name->{description,instruction} in tool_memory.json. All three as flat JSON files under a memory/ directory with
index/content separation for the procedural layer.

**检索/复用方式**
Hybrid: description/index匹配触发加载 + generation-as-retrieval via dedicated tool. Strategic Memory + Procedural SOP INDEX
loaded entirely into the system prompt at startup (outline form); full Procedural SOP CONTENT fetched on demand via a
dedicated memory_retriever tool a_mem (prompt engineering encourages the agent to query at sub-task start); Tool Memory
static description always in prompt, dynamic instruction returned inline with each tool observation. No vector/BM25
similarity search; matching is LLM-driven over the outline index.

#### 验证与反馈

**验证方式**
surrogate verifier (Reflect Agent as independent third-party supervisor with NO ground truth) + execution-based active
verification (uses tools to interact with environment and cross-check) + functional-correctness check via an ordered
3-axis checklist: Truthfulness Verification (conclusions grounded in real env feedback to suppress hallucination),
Deliverable Verification (existence/completeness/correctness of output files), Data Fidelity (no
loss/truncation/alteration). No held-out eval gating for adopted memory.

**错误纠正**
自我修订 via replan + 重规划 (PE Agent adaptively refreshes sub-task queue Q after each Reflect assessment) + 重试 (one retry
granted on sub-task failure/max-actions, during which procedural-memory use is DISABLED to encourage exploration over
exploitation of possibly-wrong knowledge). No bounded diff-patch editing of memory; correction is via replanning/retry,
while memory self-correction is handled by the merge-expert dedup step.

#### 环境与基座

**测试环境**
真实生产力任务: TheAgentCompany (TAC), a long-horizon corporate-productivity benchmark of 175 tasks across 6 roles
(HR/PM/SDE/etc.) in a fully functional OS using chat, cloud storage, project management, code editor and browser; avg
>40 action steps/task, frequently spanning 2+ applications. Cross-application GUI + tool-call + web.

**底座模型**
Gemini-2.5 Flash for both PE Agent and Reflect Agent (same model, no optimizer/target split); NPCs in TAC powered by
GPT-4o; visual extractor uses GPT-4o. Transfer experiment swaps both agents to open-source DeepSeek-V3-250324.
Closed-source Gemini primary; no fine-tuning of any backbone.

**部署域 (Where)**
general (general-purpose cross-application office/productivity automation spanning chat/storage/PM/coding/browser; not specialized to a single vertical).

#### 评估指标

**评估指标**
success_rate (official TAC S_partial = 0.5*ckpt_ratio + 0.5*S_full; aggregate S_ckpt; Perfect Completion Rate PCR) +
generalization (zero-shot on unseen hard tasks, full-benchmark transfer) + sample_efficiency (memory acquired from only
~10% of tasks) + continual-learning improvement across rounds + skill_library_growth (memory accumulation) + cost
(lightweight Flash model).

**关键结论**
New SOTA on TAC full 175-task benchmark: avg S_partial 51.78% (first to break 50%), S_ckpt 59.92%, PCR 41.14% with
Gemini-2.5-Flash, ~20% above prior SOTA (OpenHands-versa/Claude-4-Sonnet 43.19%). Continual learning: monotonic
improvement over 3 rounds, final round >10% over memory-less baseline. Zero-shot generalization on 12 hard tasks:
S_partial 23.65%->33.41% with accumulated memory (vs OpenHands/Gemini-2.5-Pro 3% and Claude-4-Sonnet 2%). Model-agnostic
transfer: memory boosts DeepSeek-V3 from S_partial 28.01%->36.75% / S_ckpt 34.12%->50.59%, beating all other open-source
frameworks. Reflect-Agent ablation: removing it drops S_partial 55.85%->43.21% on T_cl. Ranks #1 on the official TAC
leaderboard.

#### 局限与挑战

**局限与挑战**
transferability (validated only within the single TAC benchmark; no cross-harness/cross-user/cross-domain evidence);
regression_risk (no held-out validation gating for newly merged memory - adoption relies solely on per-task Reflect
success + LLM merge, so a bad SOP could persist and the frozen 3-round snapshot is never re-validated);
doc_bloat/scalability (procedural library growth is unbounded - only strategic layer is hard-capped at 10; index loaded
into prompt can grow); optimizer_quality (distillation+merge quality depends heavily on the Gemini/Reflect-LLM
capability); controllability (fully autonomous, no human-in-the-loop, no backup/rollback); eval-hacking risk not
explicitly addressed.

#### 可借鉴要点

**可借鉴要点**
1) Hierarchical 3-layer memory with INDEX/CONTENT SEPARATION + on-demand retrieval - load only a lightweight SOP outline
into the system prompt and fetch full body via a tool on demand; this keeps the prompt compact while enabling deep
procedural recall. The procedural SOP shape {platform:{operation:{preconditions, steps('A->B->C'), notes}}} is
structurally homologous to a procedural SKILL.md and is a directly reusable template. 2) SUCCESS-GATED DISTILLATION via
an INDEPENDENT VERIFIER (Reflect Agent) using a 3-axis checklist (truthfulness/deliverable/data-fidelity with active
environment cross-check) - only verified-successful trajectories may become durable memory; this is the quality gate
that prevents junk-skill accumulation, and is the single most transferable idea for self-evolving SKILL.md (an
independent verifier must confirm a workflow truly worked before it is adopted). 3) LLM-AGNOSTIC NATURAL-LANGUAGE MEMORY
+ MERGE-EXPERT GOVERNANCE PROMPTS (dedup, platform canonicalization, operation clustering, and a HARD <=10 cap on
strategic patterns) - this enables cross-model transfer and fights library bloat; the 'Resolution Patterns Merge Expert'
with a hard item cap is a directly reusable governance pattern for keeping a strategic SKILL.md concise, and the
retry-with-memory-disabled trick is a cheap anti-overfitting safeguard.

#### 不确定字段

- doc_form - exact per-SOP token length not reported in the paper/repo (procedural_memory.json ships empty as a runtime-populated placeholder); structural shape inferred from methodology + summarize_prompt.py / merge_application_prompt.py templates
- version_gating - whether any internal staging/backup of memory JSON exists before deep_update overwrite; not described (assumed none based on the save-in-place pattern in memory_manager.py)

---

### Reflexion / Self-Refine

> `idea_distill` · Reflexion(Northeastern/Princeton/MIT, NeurIPS 2023, arXiv:2303.11366)：verbal RL， 把稀疏奖励放大为 NL 反思存入情景记忆滑窗。Self-Refine(CMU/AllenAI, arXiv:2303.17651)： 同一 LLM 的 FEEDBACK→REFINE 任务内循环。两者是「反思驱动自改进」的根源范式，区别在

#### 基础信息

**名称**
Reflexion / Self-Refine

**提出机构**
Reflexion: Northeastern University (Shinn, Cassano, Berman), MIT (Gopinath), Princeton University (Narasimhan, Yao).
Self-Refine: Carnegie Mellon University (Madaan, Gupta, Gao, Alon, Yang), Allen Institute for AI (Tandon, Wiegreffe,
Dziri, Gupta, Clark), University of Washington (Hallinan, Welleck), NVIDIA (Prabhumoye), UC San Diego (Majumder), Google
DeepMind (Hermann, Yazdanbakhsh).

**发布时间**
Reflexion: arXiv v1 2023-03-20, v4 2023-10-10, NeurIPS 2023. Self-Refine: arXiv v1 2023-03-30, v2 2023-05-25, NeurIPS 2023.

**论文链接**
Reflexion: https://arxiv.org/abs/2303.11366 ; Self-Refine: https://arxiv.org/abs/2303.17651

**代码链接**
Reflexion: https://github.com/noahshinn/reflexion ; Self-Refine: https://github.com/madaan/self-refine (demo: https://selfrefine.info/)

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示. Neither method updates model weights, tools, or architecture. Reflexion evolves an episodic memory buffer
of NL self-reflections (verbal RL over memory). Self-Refine iteratively refines the in-context output draft. Policy is
parameterized as {LLM, memory/context} — optimization happens purely in text/prompt space.

**技能是否独立制品**
No persistent reusable artifact. Reflexion: reflections are transient NL memory entries scoped to a single task instance
(question / AlfWorld env / programming item), discarded when the task ends. Self-Refine: the refined output is a
temporary draft for one generation call; nothing is stored for reuse. Crucially, neither is a cross-task 'skill'
artifact — only a task-internal temporary 'skill'.

**是否文档载体**
否 (No). Neither uses a readable instruction-document (SKILL.md / markdown) as the core carrier. Reflexion = free-form NL
reflection strings in a memory list; Self-Refine = NL feedback text + refined output draft. No markdown instruction, no
YAML frontmatter, no doc-as-skill form. (This is the central distinction from the SKILL.md self-evolution line of work:
these are root paradigms of *reflection-driven self-improvement* but lack the persistent, reviewable document carrier.)

#### 技能表示

**技能编码方式**
自然语言SOP / NL reflection text. Reflexion: free-form first-person natural-language self-reflection strings (e.g., 'I
should have searched the drawer first...'), appended to an episodic memory list. Self-Refine: structured multi-aspect NL
feedback (e.g., dimensions like positivity, conciseness) + NL refined output. No executable code artifact, no vector
embedding, no graph, no multi-file skill package.

**技能粒度**
见解 (insight) / 策略规则. Reflexion: per-trial verbal lessons/strategy hints distilled from a failed trajectory (e.g., a 'new
plan' for an AlfWorld env). Self-Refine: per-iteration critique points on the current draft. Granularity is
insight/feedback-level, not atomic action, not complete skill package, not sub-task workflow.

#### SKILL.md_专属维度

**文档形态**
N/A — no markdown doc form. Reflexion memory entry: short NL reflection (~1-3 sentences, first-person, e.g. 'New plan:
check the drawer before the fridge'). Self-Refine: a short NL feedback block + a refined output draft. Typical token
length: Reflexion reflections are small (bounded by Ω=1-3 entries); Self-Refine feedback ~ a few hundred tokens. No YAML
frontmatter, no structured fields, no embedded code blocks as carrier (Self-Refine's code-optimization task refines code
but it is the *output* being improved, not a skill doc).

**编辑粒度**
全新生成 (regenerate) per trial / iteration. Reflexion: each trial *appends* a freshly-generated reflection; the memory is a
bounded sliding window (Ω=1-3) so old reflections are dropped — effectively append + window-trim, not diff/patch on a
fixed document. Self-Refine: each iteration *fully regenerates* the refined output conditioned on new feedback. No
bounded add/delete/replace on a persistent artifact, no minimal diff, no PATCH, no bundle edit.

**版本与门控**
None — no held-out validation gate, no git branch, no Pareto frontier, no review-gated adopt, no staging+backup.
Reflexion: simple sliding-window replacement of memory entries (a primitive forced-retirement rule, Ω max). Self-Refine:
stopping criterion only — the model itself decides 'no further refinement needed' or a fixed iteration cap is hit.
Accepted reflections/refinements are NOT validated against a held-out set; a wrong self-reflection can still condition
the next trial (no rejection buffer).

**文档来源**
失败轨迹蒸馏 (failure-trajectory distillation) + 成功轨迹归纳 (success-trajectory distillation in test-gen variant). Reflexion:
self-reflection is distilled by the Self-Reflection model from {failed trajectory τ_t, sparse reward r_t} → verbal
lesson sr_t. Self-Refine: feedback is generated from the current (often flawed) draft. Both: trajectory → NL. Neither
uses session-experience extraction, community sharing, or offline benchmark training as the doc source.

**跨载体迁移**
跨任务: No — memory is reset across tasks (the defining limitation vs SKILL.md library methods). 跨模型: Conceptually yes
(prompt-only, model-agnostic) but NOT studied as a transfer axis. 跨 agent harness / 跨用户 / 跨基准: not addressed. Reflexion
explicitly notes task-instance-scoped memory; Self-Refine is intra-output. This no-transfer property is exactly why
later SKILL.md-evolution works (SkillOpt, EvoSkill, OpenSpace) build on top of these paradigms but add a persistent,
portable document.

**技能库治理**
N/A — no skill library. Reflexion's only governance primitive is the sliding-window cap Ω (1-3), which is a crude
forced-retirement/forgetting rule to respect context limits — a proto-form of doc-bloat control but not a curator loop,
no dedup/merge, no similarity-based edit targeting, no hierarchical index, no Lotka-Volterra ecology. Self-Refine keeps
only the latest draft.

**失败记忆**
Yes, but transient and task-local. Reflexion: reflections are explicitly failure-derived (anti-pattern + remediation: 'I
did X wrong, should do Y'). This is a failure-signature + attribution + remedy triple — but it lives only for the
current task instance and is discarded afterward; no persistent anti-pattern store, no rejected-edit buffer as
cross-task negative feedback. Self-Refine: feedback highlights flaws in the draft (a transient negative signal), no
durable failure memory.

**编辑安全**
Minimal. Reflexion: bounded memory Ω to prevent context overflow; for programming, an isolated execution environment is
mandated (authors 'highly advise isolated execution environments' for autonomous code writing) and self-generated unit
tests are AST-validated for syntactic validity before use. Self-Refine: a stopping criterion to avoid infinite feedback
loops. Neither has pre-edit backup/rollback, scope boundaries (no doc to bound), human-in-the-loop, eval-hacking
defense, or bounded-edit destructive-rewrite protection — because there is no persistent artifact to protect.

**协同进化**
skill-only / generator-verifier 协同 (within one task). Reflexion: Actor + Evaluator + Self-Reflection are three distinct
prompts/roles co-evolving the same memory (a generator-verifier-reflector triad), but all operate on the task instance —
no skill-tool coevolution, no skill-skill ecosystem. Self-Refine: generator / critic / refiner are the *same* LLM with
different prompts (skill-prompt joint, self-collaboration). Neither coevolves with external tools or other skills.

#### 自进化机制_How

**进化方法范式 (How)**
reward-based (text feedback / self-reflection amplification) + rollout_optimization (non-gradient, text-space
optimization). Reflexion ('verbal RL'): a sparse reward r_t (binary pass/fail, scalar, or self-test result) is AMPLIFIED
by the Self-Reflection model into a NL verbal feedback sr_t, stored in episodic memory, which conditions the next
rollout — policy optimization in language space without gradient updates. Self-Refine: self-generated multi-aspect
feedback acts as an implicit reward that guides iterative text-space refinement of the output. Both explicitly avoid
gradient/SFT/RL: 'does not require any supervised training data, additional training, or reinforcement learning'
(Self-Refine); 'reinforce language agents not by updating weights, but instead through linguistic feedback' (Reflexion).

**学习信号来源**
Reflexion: 环境奖励 (env reward — AlfWorld heuristic success signal, HotpotQA exact-match grading) + 工具成功率指标 (self-written
unit tests as surrogate verifier for HumanEval/MBPP) + 自我反思 (LLM self-evaluation / classification for decision-making).
Self-Refine: LLM-as-judge (the same LLM critiques its own output along task-specific dimensions) + 成败轨迹 (the current
draft as the trajectory). Both sources are test-time, no offline training labels.

**奖励粒度**
hybrid (混合). Reflexion: outcome-level binary/scalar reward per trial (pass/fail) AMPLIFIED into process-level NL
reflection (so outcome → process). Self-Refine: process-level multi-aspect critique on the draft (direct process
reward).

**学习范式**
online; on-policy; intra-test-time (NOT sleep-time / offline). Both generate and learn from their own rollouts at
inference time, no replay buffer, no offline sleep-time consolidation. Reflexion is technically iterative on-policy
within an episode; Self-Refine is single-call iterative refinement.

#### 进化时机_When

**进化时机 (When)**
intra-test-time. Reflexion: ACROSS trials but WITHIN a single task instance (memory persists across attempts on the
*same* question / AlfWorld env / programming item; reset between items). Self-Refine: WITHIN a single generation task
(iterative feedback-refine loop until stop). Neither does inter-test-time sleep-time offline evolution of a persistent
artifact.

**触发方式**
失败触发 (failure-triggered) + 事件触发 (event-driven). Reflexion: reflection is triggered on evaluator failure (env says fail,
or a hand-written heuristic detects the agent is stuck — same action repeated >3 cycles, or >30 actions in an AlfWorld
env — 'inefficient planning'). Self-Refine: triggers a feedback step each iteration until the model's stopping criterion
is met (model says no more refinement needed) or a fixed iteration cap is reached. Neither is periodic/cron nor
curriculum-driven nor tool-degradation-triggered.

#### 存储与检索

**技能库结构**
None. Reflexion: a flat list (memory buffer) holding the last Ω (1-3) NL reflections, scoped to a single task instance —
no vector store, no hierarchical index, no DAG, no git, no cloud registry, no graph. Self-Refine: no library at all;
only the current draft + latest feedback live in context. The authors explicitly flag this as future work: 'we encourage
future work to extend the memory component of Reflexion with more advanced structures such as vector embedding databases
or traditional SQL databases.'

**检索/复用方式**
Same-instance direct reuse — NO semantic retrieval. Reflexion: ALL stored reflections for the current task instance are
prepended to the next trial's prompt (no embedding, no BM25, no LLM rerank, no description-match trigger; targeting is
by identity of the task instance, not by similarity). Self-Refine: the latest feedback directly conditions the next
refine step. There is no generation-as-retrieval or workflow-match. The commonplace review confirms: 'no global vector
store, semantic retrieval layer, or cross-task memory index.'

#### 验证与反馈

**验证方式**
execution-based + LLM-judge + surrogate verifier (no ground truth). Reflexion: AlfWorld uses env execution success + an
LLM/heuristic self-evaluator; HotpotQA uses exact-match execution grading; programming uses SELF-WRITTEN unit tests as a
surrogate verifier (AST-filtered, n≤6) — a no-ground-truth validation gating that makes it pass@1-eligible. Self-Refine:
LLM-as-judge (the same model produces the feedback that serves as validation). No held-out validation set, no
multi-model debate.

**错误纠正**
self-revision + 重规划 (replan). Reflexion: regenerate the full trajectory conditioned on the new reflection (for AlfWorld,
a 'new plan'); for code, debug guided by test/compile feedback then rewrite the implementation. Self-Refine: localized
edits on the draft guided by multi-aspect feedback. Neither uses bounded diff-patch on a persistent doc, nor explicit
rollback (there is no persistent artifact to roll back to).

#### 环境与基座

**测试环境**
Reflexion: coding (HumanEval, MBPP, LeetcodeHardGym — a new 40-question hard benchmark), sequential decision-making
(AlfWorld, 134 envs / 6 task types; WebShop ablation), reasoning QA (HotpotQA). Self-Refine: 7 diverse generation tasks
— dialog response generation, math reasoning, code optimization, acronym generation, story generation, sentiment
reversal, toxicity removal / constrained generation. Overall: 通用 (general).

**底座模型**
GPT family. Reflexion: GPT-3 (AlfWorld few-shot), GPT-3.5 / GPT-4 (reasoning + programming, including text-davinci-003
and gpt-3.5-turbo); the Reflexion actor role also explores Chain-of-Thought and ReAct as the action generator.
Self-Refine: GPT-3.5 (text-davinci-003, gpt-3.5-turbo), GPT-4, and Codex (code-davinci-002) for code. Optimizer/target
separation: Self-Refine explicitly uses ONE LLM as generator + feedback provider + refiner (no separation). Reflexion
uses three distinct *prompts* (Actor / Evaluator / Self-Reflection) but the same underlying model family — a logical
role separation, not a model-weights separation.

**部署域 (Where)**
general (通用). Both target general-purpose reasoning, coding, decision-making, and language generation — not a
specialized vertical (not GUI-only, not office-only). Reflexion is agentic (env-interaction); Self-Refine is
output-refinement; both are general-domain.

#### 评估指标

**评估指标**
success_rate (pass@1 for HumanEval/MBPP/LeetcodeHard; solve-rate for AlfWorld 134 envs; exact-match for HotpotQA) +
sample_efficiency (trials-to-converge curves over up to 12 trials) + generalization (cross-task robustness, ablations
across actor types / feedback signals / feedback-incorporation methods). Self-Refine adds human preference rate +
task-specific auto metrics (e.g., constraint-accuracy, BLEU) + 'refinement rate per iteration'. NO skill_library_growth
metric (no library). NO cost/economic-value-capture metric (pre-dates that framing).

**关键结论**
Reflexion: HumanEval Python pass@1 91% (vs prior SOTA GPT-4 80%); AlfWorld 130/134 solved (+22% absolute over ReAct
baseline within 12 iterative learning steps; ReAct-only plateaus at ~22% hallucination rate); HotpotQA +20% absolute
(CoT-GT +14% via reflection, self-reflection adds +8% over episodic-memory-only ablation); HumanEval Rust 68% (vs GPT-4
60%), MBPP Rust 75.4%, LeetcodeHard 15% (vs GPT-4 7.5%); MBPP Python 77.1% (slightly BELOW GPT-4 80.1% — attributed to
16.3% false-positive self-test rate vs 1.4% for HumanEval). Ablation: removing test-gen → 52%, removing self-reflection
→ 60% (no gain over baseline) on HumanEval-Rust. Self-Refine: ~20% absolute average improvement across 7 tasks (range
5-40%); outputs preferred by both humans and automatic metrics over one-shot GPT-3.5/GPT-4; up to +13% on Codex code
tasks.

#### 局限与挑战

**局限与挑战**
scalability (sliding-window memory Ω=1-3 caps context, no vector/SQL store) + catastrophic_forgetting / no cross-task
transfer (memory reset between task instances — the defining gap vs SKILL.md libraries) + transferability (no
cross-model/cross-harness study) + controllability (no formal success guarantee; 'may succumb to non-optimal local
minima') + optimizer_quality (relies entirely on LLM self-evaluation quality; weak self-eval → weak reflection) +
eval-hacking risk on code (flaky self-written tests → false-positive pass@1, as shown by MBPP-Python regression) +
local-minima failure on exploration-heavy tasks (Reflexion fails to improve on WebShop — terminated after 4 trials;
'unable to solve tasks that require a significant amount of diversity and exploration'). Self-Refine: can over-refine /
amplify its own errors when self-feedback is unreliable; cost grows linearly with iterations. Both: doc_bloat N/A (no
doc).

#### 可借鉴要点

**可借鉴要点**
Three directly-transferable engineering ideas for letting an agent self-evolve its SKILL.md, derived from these two root
paradigms: (1) Amplify sparse reward into NL reflection before writing to the artifact — Reflexion's core move is to
convert a binary/scalar signal into a first-person verbal lesson ('I did X wrong; next time do Y'). For SKILL.md
evolution this is the seed of every edit: failure-trajectory → distilled insight → append/amend doc, instead of editing
blindly from raw reward. (2) Bounded sliding-window memory (Ω=1-3) as the simplest possible anti-bloat /
forced-retirement governance — Reflexion shows that even a crude cap prevents context explosion while keeping recent
lessons live; a SKILL.md system should inherit this as a minimum edit-budget / entry-retirement rule before reaching for
Lotka-Volterra-style ecology. (3) Self-Refine's single-LLM-as-generator/critic/refiner with multi-aspect process-level
feedback is the cheapest test-time loop (no training, no extra model) — directly applicable to having one agent critique
its own SKILL.md on dimensions like clarity / coverage / safety / regression-risk and make localized edits. THE KEY GAP
to close when porting to SKILL.md: both paradigms are intra-task and discard memory across tasks — the leap to a
self-evolving SKILL.md requires (a) promoting task-local reflections into a persistent, reviewable markdown artifact,
(b) adding the validation gate they lack (held-out / Pareto / review-gated adopt) so a bad reflection cannot poison the
doc, and (c) adding cross-task retrieval so insights transfer — exactly what SkillOpt / EvoSkill / OpenSpace layer on
top of Reflexion's verbal-RL primitive.

---

### Voyager (对照)

> `contrast` · NVIDIA/Caltech/UT Austin/Stanford, 2023(arXiv:2305.16291)。技能=可执行 JavaScript 代码 (非文档)，向量嵌入检索，自动课程+迭代提示+自我验证门控。作为「代码技能库」对照项， 论证文档载体(SKILL.md)在可读性/可审查性/可迁移性上的差异。github MineDojo/Voyager

#### 基础信息

**名称**
Voyager

**提出机构**
NVIDIA, Caltech, UT Austin, ASU (MineDojo team). Authors: Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei
Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar.

**发布时间**
2023-05-25 (arXiv v1); v2 revised 2023-10-19

**论文链接**
https://arxiv.org/abs/2305.16291

**代码链接**
https://github.com/MineDojo/Voyager

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能. No model weights are updated (pure black-box GPT-4 queries, no fine-tuning). The evolving
artifacts are (a) the agent's growing skill library of executable JavaScript programs and (b) the in-context automatic
curriculum that proposes the next exploration task. Both live entirely outside the LLM weights.

**技能是否独立制品**
Yes. Each skill is a standalone reusable artifact stored on disk as: (1) `skill/code/<name>.js` — the executable
JavaScript program targeting the Mineflayer bot API; (2) `skill/description/<name>.txt` — an LLM-generated
natural-language description used purely for retrieval; (3) a row in `skills.json` and a vector in a Chroma vector DB
keyed by description embedding. A small set of hand-written `control_primitives/*.js` (mineBlock, craftItem, killMob,
exploreUntil, placeItem, smeltItem, useChest, shoot) are seeded as atomic building blocks that generated skills compose.

**是否文档载体**
No. The skill carrier is executable code (JavaScript), NOT a readable markdown instruction document. The NL description
exists only as an indexing/retrieval index (embedded as a `//` comment header inside the .js file), not as the primary
artifact. This is precisely why Voyager is included in this survey as a CONTRAST case against SKILL.md.

#### 技能表示

**技能编码方式**
Executable code (JavaScript programs) + natural-language description as comment header for embedding-based retrieval.
Multi-file skill package per skill: code file, description file, plus JSON registry and Chroma vector store. Atomic
primitives (control_primitives) are hand-authored JS; learned skills are GPT-4-generated JS that calls primitives.

**技能粒度**
Sub-task workflow / complete skill. Each skill is a named temporally-extended behavior (e.g., 'craft wooden pickaxe',
'hunt cows for leather') realized as a JS function `async function <name>(bot) { ... }`. Complex skills compose simpler
ones by calling previously-stored skill functions — a hierarchical, compositional skill library.

#### SKILL.md_专属维度

**文档形态**
Not applicable in the SKILL.md sense — Voyager has no markdown document carrier. The closest analog is the .js skill
file, whose 'document form' = a single async function with: (a) an LLM-generated multi-line `// description` header
(used for embedding & retrieval) and (b) the body calling Mineflayer primitives. Typical program length is tens of lines
of JS. The description is short (a few sentences). Token length is dominated by executable code, not prose.

**编辑粒度**
全新生成 (full regeneration). When a skill is added the entire .js program is generated end-to-end by GPT-4 in one shot,
then iteratively regenerated wholesale (not patched) via the iterative-prompting loop using env feedback + execution
errors + self-verification until it passes. Re-adding an existing skill name triggers a versioned rewrite: the old file
is archived as `<name>V2.js`, `V3.js`, ... while the active entry in skills.json is overwritten — a coarse whole-file
replace, not bounded add/delete/replace diffs.

**版本与门控**
Validation gating (held-out execution-based self-verification) — NOT git branches / Pareto / DAG. Only skills that pass
GPT-4 self-verification (the verifier agent inspecting the latest env state via chest inventory + nearby entities +
status) are committed to the library; failing programs stay in the iterative-prompting loop (up to 4 rounds) and are
discarded if still failing. Soft versioning only: re-generated skills of the same name are dumped as V2/V3/... backups
on disk but not actively selected between. No staging, no rollback, no human review gate.

**文档来源**
LLM一次性生成 + 失败轨迹蒸馏 (via iterative regeneration from execution errors) + 执行录像回放 (self-verification reads post-execution
env state). Atomic primitives (control_primitives) are 人工初始化 (hand-written seed code). New skills are produced by GPT-4
from (curriculum task + retrieved relevant skills + primitive context + env feedback).

**跨载体迁移**
跨任务 (within Minecraft) is the headline result: a learned skill library is reused zero-shot in a brand-new Minecraft
world to solve unseen tasks, while baselines (ReAct, AutoGPT, ReSP) fail to generalize. 跨模型 — not demonstrated; tightly
bound to GPT-4 (the prompts assume GPT-4-level code generation and verification). 跨 agent harness — not applicable; the
skill carrier is Mineflayer-specific JS, so it cannot port to Claude/Codex/Cursor or non-Minecraft harnesses without
rewriting. 跨用户/团队 — only via the open-source skill_library/ directory in the repo.

**技能库治理**
层次化索引 (vector DB) + 相似度检索编辑目标 (retrieval_top_k=5 by description embedding) + minimal 灰尘清理. Explicit anti-bloat rule:
deposit-chest skills are never added ('No need to reuse the deposit skill'). Same-name skills are versioned (V2.js,
V3.js) rather than deduplicated/merged. No Lotka-Volterra retirement, no curator loop, no archival of obsolete skills
beyond on-disk version backups.

**失败记忆**
Partial. Within a single skill-learning episode, execution errors and env feedback are fed back into the
iterative-prompting loop (up to ~4 regeneration rounds) — a short-horizon negative signal. Critic/curriculum agent
records past progress (new items, biomes, mobs, blocks) to avoid re-proposing already-achieved tasks. However, no
persistent anti-pattern store, no failure-signature + remediation library, no rejected-edit buffer that survives across
episodes to veto future harmful edits.

**编辑安全**
Minimal / execution-only. Scope is bounded to the Minecraft sandbox — destructive edits cannot escape the game world
(implicit containment). Self-verification acts as a soft pre-commit gate. No pre-edit backup+rollback (only post-hoc
V2.js version dumps for accidental same-name overwrites), no human-in-the-loop, no eval-hacking defense, no
secret/injection checks. Effectively relies on the closed Minecraft environment for safety rather than on
document-editing guardrails (because the artifacts are programs, not docs).

**协同进化**
skill-skill 生态 + generator-verifier 协同. New skills compose and call older skills (skill-skill ecosystem, compounding
ability). A separate verifier agent (GPT-4 as critic) co-evolves with the skill generator: the same GPT-4 serves both as
code generator and as self-verifier. The automatic curriculum agent (also GPT-4) proposes what skill to learn next based
on the current skill inventory and discovery state — a curriculum-skill coevolution. No skill-tool joint editing (the
primitive tool API is fixed/hand-authored).

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization (non-gradient, text/code-space optimization via iterative prompting) + imitation_demonstration
(few-shot seed primitives in prompts). Concretely: GPT-4 generates a JS program; runs it in Mineflayer; env feedback +
execution error + self-verification are folded back into the prompt and the program is regenerated, looping until
verification passes. No gradient/SFT/RL on the LLM — black-box API queries only. The curriculum component performs
in-context novelty search (LLM proposes the next most-exploration-valuable task given progress so far).

**学习信号来源**
成败轨迹 (execution success/failure) + 环境奖励 (implicit: did the program produce the intended state change in Minecraft) +
自我反思 (GPT-4 self-verification reads chest inventory, nearby entities, and bot status to judge whether the task was
achieved). Curriculum agent additionally uses discovery novelty (new items/biomes/mobs) as exploration signal. No
external reward model, no held-out validation set.

**奖励粒度**
outcome (per-skill: did the verified task succeed?). The self-verification is binary outcome-level on the final env state, not per-step process credit.

**学习范式**
online (during lifelong learning) + on-policy (each skill is generated fresh by current GPT-4 with current retrieved
context, not from a replay buffer of old trajectories). inter-test-time in flavor: skills learned in earlier episodes
are persisted and reused in later episodes, but no offline sleep-time replay — all learning happens live inside the
running Minecraft session.

#### 进化时机_When

**进化时机 (When)**
inter-test-time + intra-test-time hybrid. The skill library evolves between tasks (inter-test-time: after each
curriculum task completes, a new skill may be committed) AND intra-test-time within a single skill-learning episode (the
iterative-prompting loop regenerates the program up to ~4 times until verification passes).

**触发方式**
curriculum(课程)驱动 + 失败触发. The automatic curriculum agent proposes each next task (= explicit curriculum-driven trigger
for new skill generation). Within a skill-learning episode, execution failure / verification failure triggers iterative
regeneration. The whole loop is event-driven by the curriculum proposing the next exploration task and by env feedback
on the current one — not periodic cron, not usage-driven.

#### 存储与检索

**技能库结构**
扁平 + 向量库 hybrid. Skills are stored as flat files in `skill/code/*.js` + `skill/description/*.txt` + a `skills.json`
registry, indexed by a flat Chroma vector store (`skill/vectordb/`) keyed by description embedding. The hierarchy is
implicit via composition (a skill's code can call another skill's exported function), not via an explicit tree/DAG on
disk. Checkpoint directories under `skill_library/trialN/` snapshot a learned library for transfer.

**检索/复用方式**
语义相似度 (semantic similarity over description embeddings, top_k=5 via Chroma OpenAIEmbeddings
similarity_search_with_score). Retrieved skills' code is concatenated with control primitives and injected into the
generation prompt as few-shot context. Generation-as-retrieval is NOT used; retrieval is description-embedding-only, no
BM25, no LLM rerank, no workflow matching.

#### 验证与反馈

**验证方式**
execution-based self-verification (validation gating). After a candidate skill runs, a separate GPT-4 verifier call
inspects the resulting Minecraft state (chest contents, nearby entities, bot inventory/status, completed sub-goals) and
emits an accept/reject decision. Only accepted skills are committed to the library; rejected ones re-enter the
iterative-prompting loop. No held-out benchmark, no surrogate verifier, no multi-model debate.

**错误纠正**
自我修订 (self-revision) via iterative regeneration. Each failed/verified-failed attempt feeds execution error message + env
feedback + self-verification critique back into the prompt; the same skill is regenerated from scratch (not patched) for
up to ~4 rounds. No rollback, no bounded diff edit, no targeted patch — correction = full re-generation with richer
context. Re-planning happens at the curriculum level (curriculum agent re-chooses the next task if progress stalls).

#### 环境与基座

**测试环境**
Minecraft (specifically MineDojo-flavored Minecraft via Mineflayer headless bot, with fabric mods and a 1.19
fabric-loader instance). Single embodied game environment only.

**底座模型**
GPT-4 (closed, via OpenAI black-box API) for all three agents: automatic curriculum, skill code generation, and
self-verification. No optimizer/target split — GPT-4 is both the policy and the verifier. Code generation assumes
GPT-4-level capability; ablation shows gpt-3.5-turbo degrades sharply. The Mineflayer bot runtime is the executor, not a
learned model.

**部署域 (Where)**
specialized (single game domain: Minecraft open-ended exploration). The skill library, prompt templates, and primitives
are Minecraft-specific; the methodological pattern (lifelong-learning code-skill library + automatic curriculum +
self-verification) is generalizable but the artifacts are not.

#### 评估指标

**评估指标**
skill_library_growth (number of skills acquired, lifelong) + sample_efficiency (episodes / iterations to reach
milestones) + generalization (zero-shot success on unseen tasks in a NEW Minecraft world) + functional correctness
(tech-tree milestones unlocked) + exploration coverage (unique items obtained, distance traveled, biomes discovered).
Cost (GPT-4 API tokens) is reported qualitatively but not the headline metric.

**关键结论**
3.3x more unique items obtained, 2.3x longer travel distance, and up to 15.3x faster tech-tree milestones vs prior SOTA
(ReAct, AutoGPT-style, ReSP). Strong lifelong learning: continuously acquires skills without catastrophic forgetting
(attributed to the explicit external skill library vs weight-based memory). Zero-shot transfer: a skill library trained
in one world solves all unseen tasks in a new world from scratch, while baselines fail to generalize. Ablations show
removing the skill library, automatic curriculum, or self-verification each significantly degrades performance — all
three components are necessary.

#### 局限与挑战

**局限与挑战**
optimizer_quality (relies on a frontier GPT-4-class LLM; gpt-3.5-turbo ablation collapses) + transferability (skills are
tightly bound to Mineflayer/Minecraft bot API and cannot port to other harnesses or non-game domains) + controllability
(curriculum is novelty-driven and may pursue irrelevant tasks; no human steering) + catastrophic_forgetting is mitigated
but at the cost of library bloat (V2/V3 dumps, no real retirement) + eval-hacking risk (self-verification by the same
GPT-4 that generated the code — no independent judge) + scalability (each skill = a full GPT-4 generation + execution
round; cost scales linearly with library size) + regression_risk (no held-out regression test for previously acquired
skills when a new skill of the same name overwrites the old). Notably, the artifact form itself (executable code) makes
human audit expensive — reviewers must read JS + Mineflayer semantics, unlike a markdown instruction.

#### 可借鉴要点

**可借鉴要点**
- BORROW (1) — Self-verification gating before commit. Voyager's verifier inspects post-execution state and only commits skills that pass; for SKILL.md evolution, an analogous verifier (LLM-as-judge over the doc's stated effects vs. an actual rollout, or a held-out task pass-rate gate) should gate every edit before it lands in the skill directory. Without this, SKILL.md files accumulate unverified prose.
- BORROW (2) — Embedding-indexed retrieval over NL descriptions + compositional reuse. Even though Voyager's primary artifact is code, it still generates a separate NL description per skill purely for vector-DB retrieval (top-k=5) and injects retrieved skills as in-context examples. SKILL.md should adopt the same: keep a concise description field (YAML frontmatter) optimized for embedding retrieval, even when the body is rich instruction prose, and let complex SKILL.md skills reference/compose simpler ones.
- BORROW (3) — Iterative regeneration with execution feedback, not one-shot writes. The iterative-prompting loop (env feedback + execution error + self-critique, up to N rounds) is directly portable: SKILL.md edits should also be regenerate-with-feedback loops, not single LLM writes, when a dry-run/sandbox of the doc is available.
- BORROW (4) — Anti-bloat rule + same-name versioning. Voyager explicitly refuses to store 'deposit useless items' skills and dumps V2/V3 backups for same-name overwrites. SKILL.md governance should likewise (a) maintain a deny-list of low-value doc types to never commit, and (b) keep versioned backups on overwrite to recover from regressions.
- CONTRAST (where SKILL.md wins) — Readability: a SKILL.md is human-readable instructions; Voyager's .js skill requires Mineflayer + JS expertise to audit. Auditability: SKILL.md can be human-reviewed or sanctioned before deploy (human-in-the-loop is natural); Voyager's verifier is the same GPT-4 that wrote the code (no independent check). Transferability: SKILL.md instructions are agent-harness-portable (Claude/Codex/Cursor all read markdown); Voyager's skills are locked to Mineflayer/Minecraft. Compositionality differs in kind: Voyager composes via function-call in JS (precise, deterministic, replayable) while SKILL.md composes via reference + plan (flexible, but loses deterministic replay). Net: borrow Voyager's verification + retrieval + anti-bloat engineering, but keep SKILL.md's prose carrier to win on readability, auditability, and cross-harness transfer — accept the tradeoff of weaker deterministic replayability.

#### 不确定字段

- library_governance — exact retirement/archival policy beyond V2.js backup is not documented; inferred from source code only
- failure_memory — whether any cross-episode failure signal persists in the checkpoint beyond skills.json and the curriculum's progress record
- release_date — minor ambiguity between arXiv v1 (2023-05-25) and v2 (2023-10-19); used v1 as primary
- reward_granularity — paper describes self-verification as outcome-level; no per-step credit assignment, but curriculum novelty is process-flavored

---
