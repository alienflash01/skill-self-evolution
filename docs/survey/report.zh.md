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

1. [SkillOpt](#skillopt) — **时间**: arXiv v1 2026-05-22；v2 2026-05-25 | **类型**: academic | **文档载体**: 是。核心载体是可读的 markdown 指令文档（best_skill.md）。不向目标交付任何代码或向量；optimizer…<br>**编辑粒度**: 在文本学习率预算下的有界 add/delete/replace 编辑。Patch 模式将每次更新限制为四种原子操作：append… | **版本门控**: 留出验证门控（strict-improvement）：候选技能在互斥的选择集 D_sel 上用冻结目标模型评估，仅当严格超过当前… | **进化时机**: sleep-time / inter-test-time 离线。所有优化在部署前离线地在 train/selection 划分上…<br>**进化方法**: rollout_optimization（非梯度、文本空间优化），镜像 SGD。循环为：前向 = 用当前技能做 rollout… | **部署域**: general。同一 optimizer 接口横跨 QA、表格、文档、多模态 QA、数学与具身决策，并横跨 direct-cha…
2. [SkillOpt-Sleep](#skillopt-sleep) — **时间**: 2026（母版 SkillOpt 论文 2026 年 5 月，arXiv:2605.23904；SkillOpt-Sleep 插… | **类型**: industry (open-source deployment-time companion plugin) derived… | **文档载体**: 是（纯可读指令 markdown 为核心载体）。进化后的状态是一份 markdown 指令文档；所有学习都以文档内的文本规则增改…<br>**编辑粒度**: 有界 add/delete/replace 编辑（SkillOpt 文本学习率预算）。step 级编辑仅落入受保护的 LEARN… | **版本门控**: 丰富且多层：(1) 留出验证门控（仅当严格提升真实任务 val 分时保留编辑）；(2) 暂存（run 仅暂存提案，不改动线上任何… | **进化时机**: sleep-time——周期性离线「睡眠」（每夜 / 空闲时）replay 与合并。所有进化发生在会话之间；运行中的 agent…<br>**进化方法**: rollout_optimization——非梯度文本空间优化（SkillOpt 循环）：离线 replay（前向）-> 对对比… | **部署域**: specialized——coding / 生产力 agent 领域（Claude Code、Codex、Copilot cod…
3. [SkillSmith](#skillsmith) — **时间**: 2026-05-31（arXiv v1） | **类型**: academic | **文档载体**: 混合。核心载体是 workflow body w，包含可读的 step 级编排指令（类似指令文档），但该包还捆绑了可执行脚本与…<br>**编辑粒度**: bundle（技能+工具原子联合编辑）。Reflection 发出一个原子 proposal bundle L，在一个事务中联合… | **版本门控**: Pareto 前沿 + 留出验证门控（held-out）。维护实例级 Pareto 前沿 G（一个状态若在 >=1 个训练实例上… | **进化时机**: inter-test-time + sleep-time。进化以离散迭代推进：每次迭代从 Pareto 前沿采样一个候选，执行一…<br>**进化方法**: co_evolutionary + population_evolutionary + rollout_optimization… | **部署域**: general（通用）。横跨文档 QA、网络搜索 QA 与多模态真实 agent 生产力任务；不专精于单一垂直领域。
4. [CoEvoSkills (EvoSkills)](#coevoskills-evoskills) — **时间**: 2026-04-02（arXiv v1）；2026-04-12（v2） | **类型**: academic | **文档载体**: 混合。核心载体包含一份可读的指令文档（SKILL.md），但该包同时打包了可执行 code/scripts 与 assets；以…<br>**编辑粒度**: 全新生成 / 整文档重写。每次修订 S(i+1) 由 generator LLM（Eq.7）读取当前技能 S(i) 连同追加到上… | **版本门控**: 留出验证门控（held-out）+ best-snapshot 保存。一个留出的 Ground-Truth Oracle 在全新… | **进化时机**: inter-test-time / sleep-time。离线 co-evolution 在部署到目标 agent（Claude…<br>**进化方法**: co_evolutionary + rollout_optimization（非梯度，文本空间优化）。通过迭代式 LLM 采样进… | **部署域**: general（通用）。SkillsBench 横跨 11 个领域（含 Natural Science 等）；面向通用的多步专业…
5. [EvoSkill](#evoskill) — **时间**: 2026-03-03（arXiv v1 提交于 2026 年 3 月 3 日）；开源代码仓库持续维护。 | **类型**: academic (arXiv paper) + industry/open-source framework (Apache-… | **文档载体**: 混合（以指令文档为中心）。核心载体是可读的 SKILL.md markdown 指令文件，但技能文件夹额外捆绑 helper s…<br>**编辑粒度**: 全新生成（通过 action='create' 创建新技能文件夹 + SKILL.md）+ 编辑已有技能（对 target_sk… | **版本门控**: 留出验证门控（held-out）+ git 分支前沿选择 + DAG 血脉。每个新 program 在一个 Proposer 永… | **进化时机**: inter-test-time（任务间离线）。自我改进循环作为批处理在 benchmark 评估运行之间离线执行（而非单任务执行…<br>**进化方法**: population_evolutionary + rollout_optimization（非梯度，文本空间）+ reward… | **部署域**: general（通用）-> specialized。将通用 coding agents 转变为专家；测试覆盖 office/fi…
6. [DRAFT (From Exploration to Mastery)](#draft-from-exploration-to-mastery) — **时间**: arXiv v1 2024-10-10，v2 2025-02-26；ICLR 2025 Oral（top 1.8%） | **类型**: academic (ICLR 2025 Oral paper, open-source reference implementa… | **文档载体**: 是（纯可读的自然语言指令文档是核心载体）。进化对象是结构化 NL docstring（description + paramet…<br>**编辑粒度**: 每轮迭代整文档重写：Rewriter 每轮产出工具文档的完整新版本 t_i（条件为前一版本、探索实例、工具反馈、Analyzer… | **版本门控**: 无基于质量的版本门控（无留出验证、无 Pareto 前沿、无 git branch、无人工评审、无备份/回滚）。仅有一个 too… | **进化时机**: inter-test-time：文档在部署之间离线精炼，作为每个工具的一次性预处理 pass。下游任务执行期间无 intra-t…<br>**进化方法**: rollout_optimization（非梯度、经 trial-and-error 的文本空间优化），融合 reward-ba… | **部署域**: general——通用 tool-use / tool-call 领域（跨异构真实世界类别的 API 调用：电影、音乐、web…
7. [SkillWeaver](#skillweaver) — **时间**: arXiv v1 2025-04-09 | **类型**: academic | **文档载体**: 混合。技能载体主要是可执行的 Python 代码（API 体），但每个 API 都带有丰富的自然语言 docstring（描述…<br>**编辑粒度**: 全新生成（synthesis/polishing 期间的整函数重生成）+ 定向 diff 修补（运行期的 targeted di… | **版本门控**: 留出验证门控（held-out）/ validation gating。每个候选 API 必须通过 Stage III honi… | **进化时机**: inter-test-time + sleep-time。技能的发现/合成/honing 发生在一个专门的离线探索循环中（在真实…<br>**进化方法**: imitation_demonstration + rollout_optimization（非梯度、文本空间）。成功的执行轨迹… | **部署域**: specialized（web/GUI 自动化领域）。

### B. 工程实践｜SKILL.md / CLAUDE.md 自改进 agent

8. [OpenSpace](#openspace) — **时间**: 2026-03-25（开源）；v0.1.0 于 2026-04-03 发布。活跃开发至少持续到 2026-04-16。 | **类型**: industry (open-source self-evolving skill engine / agent framewo… | **文档载体**: 是。核心载体是可读的指令文档：SKILL.md，顶部为 YAML frontmatter（name、description），其…<br>**编辑粒度**: 最小 diff / PATCH。patch.py 支持多文件 FULL / DIFF / PATCH 应用；README 强调「… | **版本门控**: DAG 血脉版本化 + validation gating（门控）+ 确认门控。SQLite 存储维护一个版本 DAG，含完整血… | **进化时机**: inter-test-time + sleep-time。Post-Execution Analysis 在每个任务后运行（任务…<br>**进化方法**: rollout_optimization（非梯度，文本空间）+ imitation_demonstration。非梯度、LLM… | **部署域**: general（通用）。横跨 coding、DevOps、web research、桌面/GUI 自动化、办公与专业生产力（薪酬…
9. [AutoSkill / SkillEvo](#autoskill-skillevo) — **时间**: arXiv v1 提交于 2026-03-01，v2 于 2026-03-05。发布时间线：AutoSkill 1.0（2025… | **类型**: academic (formal arXiv paper with Method/System/Experimental sec… | **文档载体**: 是（含可选的混合扩展）。核心载体是人类可读的 markdown 指令文档（SKILL.md）。少数技能（如内置的 anthrop…<br>**编辑粒度**: 以全新生成为主（LLM 提取产出一个全新的候选技能）+ 经语义合并的整文档重写（合并模型重写整个技能并保持身份；非原始拼接，非最… | **版本门控**: 多种机制：(1) 合并时补丁号递增的语义化版本（Bump 算子，如 v0.1.0 -> v0.1.1，观测到最高 v0.1.34… | **进化时机**: inter-test-time（轮次/会话后的提取；AutoSkill4OpenClaw 的 agent_end hook）+…<br>**进化方法**: Training-free、prompt 驱动的组合（无 gradient/RL/SFT）。由 prompt 实例化的五个 LL… | **部署域**: general（横跨编程、写作、咨询、办公文档、社媒文案的模型无关个性化层）。AutoSkill4Doc 通过可配置分类法增加…
10. [claude-self-improving-skills](#claude-self-improving-skills) — **时间**: 2026-06-09（GitHub repo 创建；首个公开版本）。v0.9.0 新增 team 技能共享。截至 2026-06… | **类型**: industry (open-source framework / Claude Code plugin) leaning bl… | **文档载体**: 是（instruction-document-centric）。核心载体是可读的 markdown `SKILL.md`，带 Y…<br>**编辑粒度**: 有界增删替换（bounded add/delete/replace，通过 `Edit` 工具）被强烈优先于整文档重写或全新生成。… | **版本门控**: 暂存+备份 + review-gated adopt + 自动回滚。(a) 任何技能编辑前都会取 pre-edit 备份；Pos… | **进化时机**: 主要是 inter-test-time。Stop hook 在会话/段结束时评估复杂度；curator 周期性运行（当 lear…<br>**进化方法**: imitation_demonstration + rollout_optimization（非梯度、文本空间编辑），带有 LL… | **部署域**: specialized（Claude Code coding/agent 生产力）。该 plugin 按构造即是 Claude-…
11. [claude-evolving-skills (reflect-and-learn)](#claude-evolving-skills-reflect-and-learn) — **时间**: 2026-03（LinkedIn 文章《I Stopped Chasing Viral Agentic Workflow Rep… | **类型**: blog_practice | **文档载体**: 混合 — 核心载体是人类可读的 Markdown 指令文档（SKILL.md），但其中内嵌可执行的 bash/代码块（jq 会话…<br>**编辑粒度**: 在 CLAUDE.md 规则和记忆条目上的有界 add/delete/replace；定向 diff（每条提议的修改是一个带理由… | **版本门控**: 分层：(1) 评审门控采纳 — P0-AUTO（>=8.0，3/3 声音一致，Safety>=8）和 P1-AUTO（>=7.0… | **进化时机**: sleep-time（主要：每周三凌晨 3am 定期调度）+ inter-test-time（手动触发：用户说「reflect」…<br>**进化方法**: rollout_optimization（通过对 config 施加 TextGrad 式 text gradient 的非梯度… | **部署域**: specialized（coding）— Claude Code 是 coding agent；技能作用于 ~/.claude/…
12. [Homunculus nightly agent (/hm-night)](#homunculus-nightly-agent-hm-night) — **时间**: 2026（v0.5.0 首次发布 2026 年 3 月；v0.6.3 evolution tiers 2026 年 3 月；v0… | **类型**: industry (open-source self-evolution framework/plugin) + blog_pr… | **文档载体**: 是（混合，偏向是）。一个「技能」的核心载体是带 YAML frontmatter 的可读指令 markdown 文档；insti…<br>**编辑粒度**: 有界 add/delete/replace（非整文档重写）。`/improve-skill` 分析 FAIL/PARTIAL/G… | **版本门控**: 多层：(1) 验证门控——eval→improve 循环直到 100% 通过，含 5pp 噪声容忍、回归 rollback，以及… | **进化时机**: sleep-time（nightly agent，头条模式）+ inter-test-time（session-end inst…<br>**进化方法**: rollout_optimization（非梯度文本空间：在 skill .md 上做 eval→improve→rollbac… | **部署域**: specialized——coding / 生产力 agent 领域（Claude Code、Cursor、Codex CLI…
13. [Skill Evolver (nomadically.work)](#skill-evolver-nomadicallywork) — **时间**: 2026-02-25 | **类型**: blog_practice | **文档载体**: 是。核心载体是人类可读的 Markdown 指令文档；agent 的全部可编辑面为 doc/prompt/memory 文件。<br>**编辑粒度**: Minimal diff / 有界 add-delete-replace。Apply Changes 优先级：(1) minim… | **版本门控**: 验证门控（留出 Verification Gate）+ rejected-edit 反馈循环。每条编辑都须通过强制的 Verif… | **进化时机**: inter-test-time（任务运行之间，作为专用 pipeline 阶段）— 处理由前序 Trajectory Miner…<br>**进化方法**: rollout_optimization（非梯度、文本空间 prompt 编辑）+ reward-based（经负向文本反馈）。… | **部署域**: specialized（job-posting 分类 / remote-EU-job 过滤领域，经 nomadically.wo…
14. [venotyh/evoskill (evolutionary skill agent)](#venotyhevoskill-evolutionary-skill-agent) — **时间**: 2026（仓库活跃时间约 2026-05；CHANGELOG 处于 'Unreleased' 区段；未发布任何 tag/rele… | **类型**: blog_practice / industry (small open-source experimental CLI too… | **文档载体**: 否（纯结构化数据，非可读的指令文档）。技能的 'instructions' 作为一串短字符串存放于 JSON 序列化的 data…<br>**编辑粒度**: 整字段重写 + 有界 add/delete/replace（field-level，非整文档）。mutation 算子定向具体的… | **版本门控**: DAG 血脉（仅用于追踪/查询）+ 生成代际剪枝（generational pruning，非留出验证）。每一代：populat… | **进化时机**: sleep-time（夜间/空闲离线）+ inter-test-time（手动批处理）。主打框架是 sleep-time 模拟（…<br>**进化方法**: population_evolutionary + reward-based（LLM-as-judge）。经典代际进化循环：in… | **部署域**: general（通用）。一个通用的 agent-skill 进化玩具：未专门面向 coding/GUI/office/docum…

### C. 思想来源｜文本空间优化范式

15. [TextGrad](#textgrad) — **时间**: arXiv 预印本：2024-06-11（arXiv:2406.07496）。发表于 Nature：2025-03-19（Nat… | **类型**: academic | **文档载体**: 否。被优化对象是一个原始文本字符串（自然语言提示、代码或如 SMILES 的结构化字符串），而非人类可读的指令文档。没有 mar…<br>**编辑粒度**: 整变量重写（whole-variable regeneration）。TextualGradientDescent optimi… | **版本门控**: 留出验证门控 + 在 dev 划分上的贪心爬山选择。在 evaluation/prompt_optimization.py 中，… | **进化时机**: 以 inter-test-time 为主（任务执行之间/前后的离线优化：在 train batch 上跑 optimizer，在…<br>**进化方法**: reward-based 的文本反馈驱动的文本空间 rollout_optimization（非梯度）——这是文本空间优化范式的… | **部署域**: general——TextGrad 是面向任意复合 AI 系统的通用优化框架，横跨推理、编程、化学与医学得到验证；不专用于单一垂…
16. [GEPA](#gepa) — **时间**: 2025；以 conference paper 发表于 ICLR 2026 | **类型**: academic | **文档载体**: 是。优化后的制品本质上是一份人类可读的自然语言指令文档（声明式规则、目的/上下文、分步策略、输出格式——见图 2）。提示自身不内…<br>**编辑粒度**: 每个模块每次变异为整文档重写（reflection LM 输出一个完整修订后的提示 pi_i，而非 patch/diff）。两种… | **版本门控**: Pareto 前沿 + 留出验证门控。多级门控：(a) 先做 minibatch 评估；仅当分数超过父代时，(b) 再做完整 D… | **进化时机**: inter-test-time（部署前在 D_train 上的离线优化循环，受 rollout 预算 B 约束）。次要模式：推理…<br>**进化方法**: rollout_optimization（文本空间、非梯度）与 population_evolutionary（遗传算法：变异… | **部署域**: general（通用复合 AI workflow：QA、数学、指令遵循、验证、隐私委派、代码生成）。非专门面向单一领域。
17. [OPRO / PromptBreeder / EvoPrompt](#opro-promptbreeder-evoprompt) — **时间**: 三者均为 2023 年 9 月: OPRO arXiv:2309.03409 (2023-09-07; v3 2024-04-1… | **类型**: academic (three peer-reviewed papers, ICLR 2024 x2 + ICML 2024) | **文档载体**: 是。被进化的对象本质上是人类可读的自然语言 instruction 文本。被进化的制品中不内嵌任何可执行代码; 「技能」是纯声明…<br>**编辑粒度**: 整文档重写 (每次变异整体重写指令; 无 PATCH/diff)。OPRO: optimizer LLM 每步发出一条全新的 i… | **版本门控**: 留出验证门控 (held-out development set) + greedy/top-k 选择。OPRO: 每步在小训练… | **进化时机**: inter-test-time (部署前的离线优化阶段)。三者都是批量优化过程, 运行至收敛 (或步数/时间预算) 后输出单条最…<br>**进化方法**: population_evolutionary + rollout_optimization (文本空间, non-gradie… | **部署域**: general (通用 NLP 推理: 数学、常识、分类、生成、instruction induction)。非专门用于 cod…

### D. 思想来源｜经验/记忆蒸馏为文档

18. [ExpeL](#expel) — **时间**: arXiv v1 提交于 2023-08-20；v2 2023-12-18；v3 2024-12-20。被 AAAI-24（第… | **类型**: academic (AAAI-24 paper). Model weights never trained; method is… | **文档载体**: 是（偏向）。主要载体是注入提示的可读自然语言 insight 规则；不含内嵌可执行代码。它在精神上是「指令文档中心」的（NL S…<br>**编辑粒度**: 有界增删替换，通过对 insight 集合施以四种原子操作实现：ADD（新 insight，初始 importance coun… | **版本门控**: 仅基于计数的隐式门控：当某条 insight 的 importance count 降到 0 时（被 DOWNVOTE 主导）自… | **进化时机**: inter-test-time（任务间离线）。insight 抽取与库构建发生一次、离线进行，位于训练任务经验采集与评估任务部署…<br>**进化方法**: reward-based（来自二元成败结果的文本反馈）+ imitation_demonstration（将检索到的成功轨迹作为… | **部署域**: general（通用）。横跨多样决策领域测试（QA、具身家务、网页购物、事实验证）；不专精于单一垂直领域。该方法在设计上是领域无…
19. [Agent Workflow Memory (AWM)](#agent-workflow-memory-awm) — **时间**: 2024-09-11 (arXiv v1)；发表于 ICML 2025 (Poster)，PMLR 267:63897-6391… | **类型**: academic | **文档载体**: 混合。workflow 是一份人类可读的指令文档（自然语言目标 + 状态 + 推理），其中嵌入了可执行的动作代码调用。它相当于一…<br>**编辑粒度**: 整段生成 + 仅追加（append-only）的添加。LM 归纳模块在单次 prompt 中从一个或多个经验生成整个 workf… | **版本门控**: 最小。(1) 在线模式：一个 LM-evaluator（Pan et al. 2024 AutoEval）输出二元成功标签；仅被… | **进化时机**: 两者皆有。离线 = sleep-time / inter-test-time（在服务测试查询前从训练样本一次性归纳）。在线 =…<br>**进化方法**: imitation_demonstration + 非梯度文本空间 rollout 优化。LM 归纳模块将成功轨迹泛化为可复用的… | **部署域**: Specialized（Web 导航 / 数字 GUI agent 领域）。通用 Web 任务（旅行、购物、社交媒体、开发协作、…
20. [MUSE (Learning on the job)](#muse-learning-on-the-job) — **时间**: 2025-10-09（arXiv v1） | **类型**: academic | **文档载体**: 是（结构上）。Procedural Memory 是一份可读的 SOP（'Standard Operating Procedur…<br>**编辑粒度**: 有界增量更新 + 任务后全局精炼合并。Procedural memory 经 deep_update 更新（成功的子任务后立即对… | **版本门控**: 无 git-branch / DAG / Pareto / held-out 验证门控。质量门控为：(a) success-ga… | **进化时机**: intra-test-time（每个子任务尝试后 Reflect+Memorize -> 立即复用 SOP）+ inter-te…<br>**进化方法**: imitation_demonstration（将验证成功的动作轨迹蒸馏为可复用 SOP）+ 基于 LLM 的自我反思（Refl… | **部署域**: general（横跨 chat/storage/PM/coding/browser 的通用跨应用办公/生产力自动化；未专门化于单…
21. [Reflexion / Self-Refine](#reflexion-self-refine) — **时间**: Reflexion: arXiv v1 2023-03-20, v4 2023-10-10, NeurIPS 2023。Self… | **类型**: academic | **文档载体**: 否。两者均不使用可读的指令文档（SKILL.md / markdown）作为核心载体。Reflexion = memory 列表…<br>**编辑粒度**: 逐试次/迭代全新生成（regenerate）。Reflexion：每次试次追加一条新生成的反思；memory 是一个有界滑动窗口… | **版本门控**: 无——无留出验证门控、无 git 分支、无 Pareto 前沿、无评审门控采纳、无 staging+backup。Reflexi… | **进化时机**: intra-test-time。Reflexion：跨试次但在单个任务实例之内（memory 在同一问题 / AlfWorld…<br>**进化方法**: reward-based（文本反馈 / 自我反思放大）+ rollout_optimization（非梯度、文本空间优化）。Re… | **部署域**: general。两者均面向通用推理、编程、决策与语言生成——而非 specialized 垂直领域（非仅 GUI、非仅 offi…

### E. 对照组｜非文档载体

22. [Voyager (对照)](#voyager-对照) — **时间**: 2023-05-25（arXiv v1）；v2 修订于 2023-10-19 | **类型**: academic | **文档载体**: 否。技能载体是可执行代码（JavaScript），而非可读的 markdown 指令文档。自然语言描述仅作为索引/检索条目存在（…<br>**编辑粒度**: 全新生成（full regeneration）。当一个技能被添加时，整个 .js 程序由 GPT-4 端到端一次性生成，随后通过… | **版本门控**: 验证门控（留出、基于执行的 self-verification）——而非 git 分支 / Pareto / DAG。只有通过… | **进化时机**: inter-test-time + intra-test-time 混合。技能库在任务之间进化（inter-test-time：…<br>**进化方法**: rollout_optimization（非梯度，文本/代码空间优化，经迭代提示）+ imitation_demonstrati… | **部署域**: specialized（单一游戏域：Minecraft 开放式探索）。技能库、提示模板与原语都是 Minecraft 特定的；方…

## 详细内容

### SkillOpt

> `academic_doc_skill` · Microsoft, 2026。把 SKILL.md 当作冻结 agent 的「可训练外部状态」，用镜像 SGD 的 文本空间优化：rollout(前向)→反思(反向)→有界 add/delete/replace 编辑(受 textual learning-rate 预算约束)→留出验证门控(仅当严格提升才接受)。rejected-edit buffer + epoch-wise slow/met

#### 基础信息

**名称**
SkillOpt

**提出机构**
Microsoft（主导）；合作作者来自 Shanghai Jiao Tong University、Tongji University、Fudan University

**发布时间**
arXiv v1 2026-05-22；v2 2026-05-25

**论文链接**
https://arxiv.org/abs/2605.23904

**代码链接**
https://aka.ms/SkillOpt（论文）。镜像于 https://github.com/microsoft/SkillOpt 及 PyPI 包 `skillopt`，见 task note [uncertain: GitHub/PyPI 链接未直接验证，aka.ms 短链为论文中的权威引用]

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示。技能文档（一段注入 agent context 的自然语言策略）被视为冻结目标模型的「可训练外部状态」。模型权重、harness 与评估器全部固定；仅优化单一技能文档。

**技能是否独立制品**
是。部署产物是单一可移植的 best_skill.md 文件（约 300-2000 tokens，中位数 ~920，六个基准上范围 379-1995）。在 harness 模式下它被渲染为与任务文件并列的 per-task SKILL.md。它是可审计、可检查的文本，可跨模型/harness 复用而无需改动权重。

**是否文档载体**
是。核心载体是可读的 markdown 指令文档（best_skill.md）。不向目标交付任何代码或向量；optimizer 侧的 meta_skill 仅限 teacher 使用、不部署。

#### 技能表示

**技能编码方式**
技能文档 (.md / SKILL.md)。单一自然语言技能文档封装了流程、领域启发式、工具策略、输出约束与失败模式。包含一个由 SLOW_UPDATE_START / SLOW_UPDATE_END 标记界定的受保护 slow-update 区段。

**技能粒度**
策略规则 + 完整技能包。单一紧凑的过程化技能（领域级规则，而非原子动作或实例级修补）。规则是过程化/可泛化的（如答案格式约束、证据绑定、搜索前沿纪律）。

#### SKILL.md_专属维度

**文档形态**
纯指令 markdown 文档（best_skill.md），非 YAML-frontmatter 结构化。结构上有一个常规可编辑正文，外加一个由 SLOW_UPDATE_START / SLOW_UPDATE_END 界定的受保护
slow-update 块，仅 epoch 边界的 slow-update 流程可改写。典型长度 300-2000 tokens（观测值 379-1995；中位数 ~920）。最终技能相比初始的一行/一段文字仅增长
x2.5-x5.3，并保持在典型 system-prompt 预算之下。不向目标交付内嵌可执行代码块。

**编辑粒度**
在文本学习率预算下的有界 add/delete/replace 编辑。Patch 模式将每次更新限制为四种原子操作：append、insert_after、replace、delete（局部化操作，minimal-diff 风格）。另一种
rewrite_from_suggestions 模式基于选中的建议对技能进行整体重写。每步 optimizer 对合并后的编辑池排序并截断到前 L_t 条（默认 L_t=4，cosine 衰减至下限 2）。step 级编辑不能覆写受保护的
slow-update 字段。不支持 skill+tool 的 bundle 联合编辑（工具/harness 固定）。

**版本与门控**
留出验证门控（strict-improvement）：候选技能在互斥的选择集 D_sel 上用冻结目标模型评估，仅当严格超过当前选择分时才被接受（平局拒绝）。最优技能以 best_skill.md 跟踪；以技能 hash
为键的选择分缓存防止重复评估。这是 propose-and-test 选择，而非 git-branch/Pareto-front/DAG。epoch 级 slow/meta 更新候选同样过该门控。

**文档来源**
混合：由人工或一行文字初始化技能，随后基于带分的 rollout 轨迹（成功轨迹归纳 + 失败轨迹蒸馏，经 optimizer 模型）进行 LLM 驱动的迭代优化。本质上是离线 benchmark 训练：部署制品由在 train/selection/test 划分上的系统性训练循环产出，而非一次性生成或社区共享。

**跨载体迁移**
强，沿三条轴线得到明确验证：(1) 跨模型（在 GPT-5.4 上训练的 SpreadsheetBench 技能提升所有更小的 GPT 变体；LiveMath 技能从 GPT-5.4 迁移到 mini/nano）；(2) 跨 agent
harness Codex <-> Claude Code（如 Codex 训练的 SpreadsheetBench 技能迁移到 Claude Code 达 +59.7pt；Claude Code 训练的迁移到 Codex 在
SpreadsheetBench 上 +43.6pt）；(3) 跨基准（OlympiadBench 技能在 Omni-MATH 上为 GPT-5.4/mini/nano 带来正向收益）。每一行迁移均为正（无一低于目标 no-skill
基线）。

**技能库治理**
单技能设计（无不断增长的技能库，无 Lotka-Volterra/retirement/archive）。膨胀由以下方式控制：(a) 文本学习率/编辑预算限制每步编辑数；(b) 分层合并在排序前过滤重复、矛盾与样本特定的提案；(c)
紧凑性约束保证最终制品 <2000 tokens；(d) 仅严格改进的编辑存活进 best_skill.md。无基于相似度检索的编辑定向，也无 curator loop。

**失败记忆**
是。一个 epoch 局部的 rejected-edit buffer 记录观察到的失败模式，并对于被拒绝的步骤，记录尝试过的编辑及其造成的掉分。同一 epoch 中后续的 reflection/merge/ranking 调用会接收该
buffer，使 optimizer 避免重复失败编辑并聚焦于未解决的失败。在训练中充当显式负反馈（anti-pattern memory），且不增加推理期成本。

**编辑安全**
(1) 范围边界：仅编辑技能 .md；目标模型权重、harness、后端与 benchmark 评估器固定；源码与工具从不触碰。(2) 有界编辑：文本学习率预算防止破坏性的整文档重写并保持连续性。(3)
留出验证门控：看似合理实则有害的文本诊断因无法提升 D_sel 而被拒绝，缓解 eval-hacking/过拟合。(4) 受保护的 slow-update 区段对所有 step 级 prompt 禁入。(5)
哈希化的选择缓存避免重复运行相同候选。(6) 严格改进（平局拒绝）门控。(7) best_skill.md 在拒绝中被保留（隐式回滚：被拒候选不会替换
current/best）。无显式的编辑前备份文件或人工在环确认（全自动）。未提及密钥/注入检查。

**协同进化**
主要是 skill-only（单一可移植技能是唯一进化的部署对象）。此外，optimizer 侧的 meta_skill 作为 teacher-only 指导协同进化：它汇总跨 epoch 哪些编辑模式有效/被拒/留存，并前置于未来的
optimizer prompt（reflection/merging/ranking），但不交付给目标模型。这是 optimizer 侧松散的 skill-prompt 联合进化。留出门控充当固定验证器（不协同进化）。无
skill-tool 或 skill-skill 生态进化。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（非梯度、文本空间优化），镜像 SGD。循环为：前向 = 用当前技能做 rollout 批次；反向 = 在成功/失败上做 minibatch 反思，产出结构化 add/delete/replace
编辑；在文本学习率调度下做有界更新；留出验证门控仅接受严格改进；rejected-edit buffer 作为负反馈；epoch 级 slow/meta 更新作为动量类比。也属
reward-based，因为留出分即选择信号。optimizer 模型与冻结目标模型相互分离。

**学习信号来源**
留出验证分（主选择信号）+ 来自 benchmark 原生评估器的带分 rollout 轨迹（成功/失败）。optimizer 还消费轨迹元数据、消息、工具调用、观测、命令输出、最终答案与验证器反馈（如 Codex harness 中的 codex_trace_summary.txt）。

**奖励粒度**
outcome。每条轨迹一个标量任务级分数 r(s)∈[0,1]（benchmark 原生硬成功 / exact-match 准确率）。无密集 process reward；过程化信号来自跨 outcome 打分 rollout 的 minibatch 聚合。

**学习范式**
离线、sleep-time（训练在部署前完成，部署时零推理期 optimizer 调用）。rollout 相对当前技能为 on-policy（冻结目标用当前技能执行）。优化后的 best_skill.md 随后原样部署。

#### 进化时机_When

**进化时机 (When)**
sleep-time / inter-test-time 离线。所有优化在部署前离线地在 train/selection 划分上完成。推理期目标模型仅消费固定的 best_skill.md，无 optimizer 调用、无权重更新、无在线编辑。

**触发方式**
由离线 benchmark 训练驱动的 epoch 周期性触发（默认 4 个 epoch）。每个 epoch 重置 rejected-edit buffer，将训练划分打乱为 rollout 批次，并运行 step 级优化直至 epoch
结束，此时触发 slow/meta 更新。在部署的 agent 中并非事件/失败/课程/cron 驱动；该循环被显式启动以针对目标领域训练一个技能。

#### 存储与检索

**技能库结构**
每个目标域单一技能文件（best_skill.md）。在 tool-use harness 中同一文件被渲染为工作区里的 per-task SKILL.md。无技能库 / 向量库 / 图谱 / DAG / 云端注册中心；SkillOpt 有意优化单一可移植技能，而非扩充仓库。

**检索/复用方式**
常驻注入而非检索：在 direct chat 中技能被前置到 system/developer 指令；在 harness 中被渲染为持久化过程记忆 / SKILL.md。无语义相似度检索、BM25 或 description 触发加载（每域单技能，始终加载）。

#### 验证与反馈

**验证方式**
留出评估 + 验证门控 + 功能正确性检查。每个候选技能在互斥选择集 D_sel 上用冻结目标模型与 harness、以 benchmark 原生评估器（硬成功 / exact-match）打分。当未声明 benchmark 特定划分时默认
2:1:7（train:selection:test）（split_seed=42）。头条数字仅在互斥的留出 test 划分上报告，衡量泛化而非验证拟合。

**错误纠正**
经反思的自我修订 + 有界 patch 编辑 + 隐式回滚。失败/被拒候选不被应用（保留 best/current 技能）；其编辑与失败模式进入 rejected-edit buffer 以备将来规避。Patch 模式执行定向 diff
修补（append/insert_after/replace/delete）。每个 minibatch 至多三轮 teacher refinement。重规划通过 epoch 级 slow/meta 更新实现，跨 epoch
重新排定编辑方向优先级。

#### 环境与基座

**测试环境**
通用 / 技能 benchmark 套件：SearchQA（抽取式 QA）、SpreadsheetBench（表格代码/工具操作，多轮 codegen 最多 30 轮，真实 openpyxl/pandas
运行时）、OfficeQA（多轮工具循环最多 24 次工具调用）、DocVQA（多模态文档 VQA）、LiveMathematicianBench（数学 MCQ）、ALFWorld（持久化具身交互最多 50 步）。还包括
SkillsBench 风格的通用 agent 技能，以及真实 coding-agent harness（Codex CLI、Claude Code CLI）。

**底座模型**
目标（冻结学生）模型：GPT-5.5、GPT-5.4、GPT-5.4-mini、GPT-5.4-nano、GPT-5.2、Qwen3.5-4B、Qwen3.6-35B-A3B。Optimizer（teacher）模型：一个前沿模型（默认
GPT-5.5；消融也用与目标匹配的 optimizer）。Optimizer/target 显式分离。teacher 与 student 调用默认 medium reasoning effort。

**部署域 (Where)**
general。同一 optimizer 接口横跨 QA、表格、文档、多模态 QA、数学与具身决策，并横跨 direct-chat、Codex 与 Claude Code 执行模式。过程化 benchmark（表格、office QA、数学）收益最大。

#### 评估指标

**评估指标**
success_rate（留出 test 上的 benchmark 原生硬分 / exact-match 准确率）；泛化（跨模型、跨 harness、跨基准迁移，每一行迁移均为正）；样本/编辑效率（仅 1-4 条被接受编辑写入
best_skill.md，中位数 2.5）；成本（每绝对 test-point 的训练 token：廉价过程化 benchmark 0.6M-3.6M/pt，多模态/长轨迹 benchmark 高达
46.4M/pt；一次性总训练成本）；紧凑度（300-2000 部署 token）。技能库增长不是指标（单技能设计）。

**关键结论**
在覆盖 6 个 benchmark、7 个目标模型、3 个 harness 的全部 52 个（模型, benchmark, harness）评估单元上 best-or-tied。在 GPT-5.5 上：将平均 no-skill 准确率提升
+23.5pt（direct chat，58.8->82.3）、+24.8pt（Codex）、+19.1pt（Claude Code）。相对 human/one-shot
LLM/Trace2Skill/TextGrad/GEPA/EvoSkill 中每个单元的最强基线，平均领先 +5.4pt（direct chat）、相对 EvoSkill +14.0pt（Codex）、+3.2pt（Claude
Code）。GPT-5.5 direct chat 各基准亮点：SpreadsheetBench 41.8->80.7（+38.9）、OfficeQA 33.1->72.1（+39.0）、LiveMath
37.6->66.9（+29.3，来自单条被接受编辑）、ALFWorld 83.6->95.5（+11.9）。平均每模型提升 ~+17.6pt；小模型相对收益最大（GPT-5.4-nano 在 DocVQA 上近翻倍、在 ALFWorld
上翻三倍；Qwen3.5-4B ALFWorld 30.6->81.3）。跨 harness 迁移：Codex->Claude Code SpreadsheetBench +59.7pt；Claude Code->Codex
SpreadsheetBench +43.6pt。跨基准：OlympiadBench 技能在 Omni-MATH 上为正（+1.3 至 +3.7pt）。

#### 局限与挑战

**局限与挑战**
来自附录 B：(1) 可扩展性/反馈依赖——循环依赖带分轨迹与留出选择集，故最适用于具备自动验证器、exact-match
指标、可执行检查或可靠反馈的任务；开放/主观/多维/评判成本高的领域可能需要在门控中使用更强的人工或基于模型的评估。(2) 训练成本——尽管部署制品只是一个紧凑的 best_skill.md、推理期零成本，训练仍需额外 rollout
计算与 optimizer 模型调用；仅在技能被复用时摊销，对一次性任务吸引力较低。(3) 单技能范围——有意优化单一可移植技能，而非扩充技能库或改权重；对需要许多互斥过程的高度异构领域不足。(4)
回归/迁移风险——优化后的技能可能编码训练分布的领域特定启发式，故在迁移到显著不同的模型/harness/任务前需谨慎的留出评估。隐含风险：eval-hacking（由留出门控缓解）、doc_bloat（由编辑预算缓解）、optimizer_quality
依赖（消融显示与目标匹配的 optimizer 能恢复大部分收益）。

#### 可借鉴要点

**可借鉴要点**
- 1. 把 SKILL.md 当作冻结 agent 的可训练「外部状态」，并引入完整的深度学习纪律：rollout/reflection 的 batch size 控制证据噪声、带调度的文本学习率（编辑预算）控制步长、留出选择集充当验证集、epoch 级 slow/meta 更新充当动量项。这把 ad-hoc 的 prompt 修订变成可复现的优化过程，也是 SkillOpt 稳定、胜过不受控自我重写的核心原因。
- 2. 采用严格留出验证门控（仅当严格更优时接受；平局拒绝）外加一个记录失败编辑及其掉分的 rejected-edit buffer。这把 optimizer 转化为 propose-and-test 搜索：看似合理实则有害的文本诊断被滤除、失败成为后续步骤的负反馈、部署制品保持紧凑（仅 1-4 条编辑存活进 best_skill.md），而非累积每一条反思。这直接应对 eval-hacking、doc-bloat 与回归风险。
- 3. 将 optimizer（强前沿 teacher 模型）与冻结目标学生分离，把 optimizer 侧 meta_skill 保持在 teacher-only，仅交付一个紧凑的 best_skill.md。在 train/selection 划分上离线训练一次，再以零推理期 optimizer 调用部署；由此产生的可审计文本制品可跨模型规模、跨 Codex/Claude Code harness、并迁移到邻近 benchmark，而无需任何权重更新——使其成为闭源前沿模型的实用领域自适应层。

#### 不确定字段

- code_link（GitHub microsoft/SkillOpt 与 PyPI skillopt 无法直接抓取/验证；论文仅引用 aka.ms/SkillOpt 短链）
- doc_form（未明确提及 YAML frontmatter；假定为带界定受保护 slow-update 区段的纯自然语言 markdown）
- safety_guardrails（未明确提及编辑前文件备份、密钥/注入扫描或人工在环门控；推断为全自动）

---

### SkillOpt-Sleep

> `academic_doc_skill` · Microsoft, 2026。SkillOpt 的部署期「睡眠」伴侣。夜间离线收割 ~/.claude session→ 挖掘反复出现的任务→offline replay→reflect→有界编辑→held-out gate→staged proposal→(用户) adopt。融合 SkillOpt + Claude Dreams + agent sleep 三思想。 作用于 CLAUDE.m

#### 基础信息

**名称**
SkillOpt-Sleep

**提出机构**
Microsoft（Microsoft Research；与 SkillOpt 论文同一团队——Yifan Yang 等；仓库 microsoft/SkillOpt）

**发布时间**
2026（母版 SkillOpt 论文 2026 年 5 月，arXiv:2605.23904；SkillOpt-Sleep 插件于 2026 年 6 月工程化并发布）

**代码链接**
https://github.com/microsoft/SkillOpt/tree/main/plugins/claude-code（另有 plugins/codex、plugins/copilot；引擎位于顶层
skillopt_sleep/ 包，与研究栈零依赖）；报告：https://github.com/microsoft/SkillOpt/blob/main/docs/sleep/FINAL_REPORT.md

**类型**
industry (open-source deployment-time companion plugin) derived from academic SkillOpt research

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示（context memory & instructions）：agent 的长期记忆（CLAUDE.md / AGENTS.md）与技能文档（SKILL.md）。不是模型权重、不是工具、不是多 agent 架构——仅为冻结目标的外部文本状态。

**技能是否独立制品**
是。技能是独立、可复用、人类可读的 markdown 制品：SKILL.md（技能）加 CLAUDE.md/AGENTS.md（记忆）。Codex 布局：~/.agents/skills/<name>/SKILL.md；Claude
Code：.claude skills + 项目 CLAUDE.md；Copilot：copilot-instructions + MCP。

**是否文档载体**
是（纯可读指令 markdown 为核心载体）。进化后的状态是一份 markdown 指令文档；所有学习都以文档内的文本规则增改表达。

#### 技能表示

**技能编码方式**
技能文档（.md / SKILL.md / CLAUDE.md / AGENTS.md）。带受保护标记界定字段（一个 LEARNED 块与 <!-- SLOW_UPDATE_START --> ... <!-- SLOW_UPDATE_END --> 区段）的自然语言指令 markdown。

**技能粒度**
策略规则（policy rules）+ 见解（insights）：学习到的内容是反复出现的约定（'always add LIMIT'、'answers in \boxed{}'、'cite the source'）加上来自
slow-update 的跨夜持久 meta-rules。容器是完整技能文档，但学习单元是规则级。

#### SKILL.md_专属维度

**文档形态**
纯指令 markdown 正文 + 由 HTML 注释标记界定的结构化受保护字段（LEARNED 块；SLOW_UPDATE_START/END）。典型长度：数百至约 2,000 tokens（SkillOpt best_skill.md 为 300–2k tokens；睡眠期生长的技能增量累积已验证规则）。

**编辑粒度**
有界 add/delete/replace 编辑（SkillOpt 文本学习率预算）。step 级编辑仅落入受保护的 LEARNED 块；slow-update 写入独立的受保护 SLOW_UPDATE 字段。无整文档重写；从不编辑源代码。

**版本与门控**
丰富且多层：(1) 留出验证门控（仅当严格提升真实任务 val 分时保留编辑）；(2) 暂存（run 仅暂存提案，不改动线上任何内容）；(3) 备份（每次 adopt 将先前文件备份至 staging/backup/ 下）；(4)
审查门控的 adopt（人工运行 /skillopt-sleep adopt；可选 --auto-adopt）。由三分 train(dream)/val(real)/test(real) 划分支撑。

**文档来源**
会话经验抽取（只读采集 ~/.claude 转录 -> 挖掘反复出现的任务）+ 离线 replay + 对成功/失败轨迹的反思（对比式多 rollout）-> 蒸馏规则。融合会话经验抽取与成功/失败轨迹归纳。

**跨载体迁移**
跨模型（Haiku<->Sonnet）与跨 runtime / 跨 agent harness（Claude Code <-> Codex <-> Copilot）以及跨任务。经实测验证：在一个模型/runtime 上优化的技能可免费部署到另一个（4/4 迁移为正，含 Codex<->Claude）。

**技能库治理**
按技能 / 按项目治理而非全局技能库：有界编辑预算、step 编辑不可触碰的受保护标记字段（LEARNED + SLOW_UPDATE）、蒸馏持久纵向指导的 slow-update 合并（防止 step 级膨胀）。sleep 插件未文档化显式的库级去重 / 退役 / Lotka-Volterra 机制。

**失败记忆**
是。被拒绝编辑作为负反馈保留（SkillOpt rejected-edit buffer）；留出门控阻断看似合理实则错误的规则与 reward-hacking；多 rollout 对比式反思将失败归因于特定规则缺口；确定性测试断言门控拒绝被注入的有害编辑。

**编辑安全**
全面：(1) 范围边界——仅编辑 CLAUDE.md/SKILL.md/AGENTS.md，从不编辑应用源代码；(2) 只读采集 ~/.claude；(3) 每次 adopt 前备份 + 回滚；(4) 审查门控人工在环 adopt（除非
--auto-adopt 显式开启，否则暂存绝不自动应用）；(5) 每夜 token/时间预算上限；(6) 从 prompt 中抹除密钥；(7) 全新 replay 仅在一次性 git worktree 中运行；(8) 隔离
optimizer/target CLI 调用以防 ambient-context 泄漏；(9) 有界编辑防止破坏性重写。

**协同进化**
skill-prompt 联合（skill + memory/prompt joint）：协同编辑技能文档（SKILL.md）与记忆/提示文档（CLAUDE.md/AGENTS.md）。无工具进化、无 generator-verifier 协同进化——judge 是固定的规则 judge。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization——非梯度文本空间优化（SkillOpt 循环）：离线 replay（前向）-> 对对比式 rollout 反思（语言级反向）-> 有界 add/delete/replace 编辑 ->
留出验证门控。辅以从成功-失败对比中的模仿式学习与逐 epoch 的 slow/meta 更新。

**学习信号来源**
成功/失败轨迹（多 rollout 对比式反思：好的尝试做了什么而坏的没做）+ 留出验证分（本地规则 judge——optimizer 从不给自己打分）+ 自反思 + 工具成功信号（为 quick-answerer seed 使用的 tool_called judge）。

**奖励粒度**
主要为 outcome（经留出集上规则 judge 的任务级 pass/fail）；多 rollout 对比补充准 process 信号（好与坏尝试的 diff）。多目标 reward 还可额外加权 tokens-down 与 latency-down。

**学习范式**
离线 + sleep-time。严格在每夜「睡眠」期间于用户自有 API 预算上做离线想象/replay；off-policy（重放过往录制会话）；intra-test-time 不学习任何内容。

#### 进化时机_When

**进化时机 (When)**
sleep-time——周期性离线「睡眠」（每夜 / 空闲时）replay 与合并。所有进化发生在会话之间；运行中的 agent 在任务期间从不被修改。

**触发方式**
周期性 / cron 式（内置 `schedule` 动作安装每夜入口，如 --hour 3 --minute 17）；亦为使用驱动（采集用户累积的会话转录）。经 /skillopt-sleep run | dry-run | adopt 手动按需触发。

#### 存储与检索

**技能库结构**
技能文件目录布局：技能位于 ~/.agents/skills/<name>/SKILL.md（Codex）、.claude skills + 项目 CLAUDE.md（Claude
Code）、copilot-instructions（Copilot）；提案暂存于带 backup/ 子目录的 staging 目录。无向量 DB、图或 DAG 溯源。

**检索/复用方式**
运行时：按 description/name 的标准技能加载（宿主 harness 在 description 匹配时加载 SKILL.md）。挖掘阶段：跨会话转录的频率/复现检测重复任务。未文档化语义向量检索。

#### 验证与反馈

**验证方式**
留出评估 + 验证门控（仅当严格提升真实任务 val 分时才接受编辑）+ 经本地规则 judge（section_present / regex / max_chars / contains /
tool_called）的功能正确性。optimizer 从不给自己打分，且 dreamed 任务永不进入 val/test（经单元测试的不变式）。

**错误纠正**
自我修订（反思 -> 跨连续数夜重新编辑）、有界编辑、回滚（每次 adopt 备份先前文件）以及作为负反馈的 rejected-edit buffer；已展示多夜收敛（如 thorough-analyst 0.33 -> 1.00 跨 2 夜）。

#### 环境与基座

**测试环境**
gbrain-evals skillopt-v1 公开套件（brief-writer、advisor、thorough-analyst、quick-answerer seeds，含真实工具使用循环）；学术 daily-cases（数学 /
表格 / search-QA，4:1:5 划分配 dream-augmented 训练）；全新 SQL-analyst load-test。经 Claude Code / Codex / Copilot 的真实 coding-agent
生产力任务。

**底座模型**
Claude（Sonnet / Haiku）与 Codex / OpenAI GPT（gpt-5.5）；Copilot 经由 MCP。强 optimizer + 冻结廉价目标分离（如用 Sonnet 优化、在 Haiku 上部署）。一个确定性 mock 后端实现零成本管路测试。

**部署域 (Where)**
specialized——coding / 生产力 agent 领域（Claude Code、Codex、Copilot coding 助手）；将 agent 适配到用户自身的重复性工作。

#### 评估指标

**评估指标**
success_rate（留出分，如 0.00 -> 1.00）、泛化（跨模型与跨 runtime 迁移）、成本（每夜 token/分钟预算；多目标 accuracy-up / tokens-down / latency-down）、收敛夜数、门控接受/拒绝计数。

**关键结论**
在 gbrain-evals skillopt-v1 上：4/4 Claude seeds（Sonnet->Haiku）达到留出 0.00 -> 1.00（brief-writer、advisor、thorough-analyst 在
1–2 夜内，quick-answerer 经真实工具循环）；Codex 自优化的 brief-writer / advisor / quick-answerer 0 -> 1.00。4/4 跨模型 / 跨 runtime 迁移为正，含
Codex<->Claude。门控阻断回归（拒绝被注入的有害编辑）。如实记录的失败：Claude ambient-context 泄漏（全局技能被注入 optimizer 调用，一次 reflect 返回 21 KB 技能列表）经隔离
CLI 标志（--bare --disallowedTools '*' ...）修复。全新 SQL-analyst load-test 在两个后端均 0 -> 1.00。如实警示：弱（Haiku）optimizer 不稳定——强
optimizer 模型具有决定性。

#### 局限与挑战

**局限与挑战**
可扩展性（仅在小型、单缺陷技能上验证；大型生产技能预计更杂乱且部分有效）、optimizer_quality（弱 optimizer 模型不稳定；需要强前沿 optimizer）、延迟（每次 CLI 调用约
14–15s、由启动主导，限制了任务/夜数——对每夜 cron 无碍但不适合交互）、基准规模较小，以及更深的 multi-tool / multi-turn workflow 属未来工作。回归与 eval-hacking
风险经门控缓解但未完全消除。

#### 可借鉴要点

**可借鉴要点**
- Sleep-time 离线合并配严格 train(dream) / val(real) / test(real) 划分 + 留出验证门控 + 审查门控人工 adopt。之所以允许 dream/augment 训练数据，正因为 dreamed 任务永不进入 val 或 test（经单元测试的不变式）——这是抵抗 eval-hacking 与过拟合的安全自我改进之关键。
- 强 optimizer + 冻结廉价目标架构：在夜间花少许成本用智能 optimizer 写规则，然后将冻结的已学技能免费部署到任意更廉价模型或不同 runtime（「optimize cheap, deploy anywhere」）。optimizer 仅为训练期杠杆，部署时零推理成本。
- 有界 add/delete/replace 编辑限于受保护标记字段（LEARNED 块、SLOW_UPDATE 标记）+ 作为负反馈的 rejected-edit buffer + 强制 adopt 前备份 + stage-then-adopt 契约。这使得指令文档的自编辑可逆、可审计且爆炸半径受限（源代码从不被触碰）。

#### 不确定字段

- paper_link

---

### SkillSmith

> `academic_doc_skill` · 2026。Synergy-aware Skill-Tool 协同进化框架。三大创新：(1) bundle 化的 skill-tool 联合编辑(原子提案，工具可 wrap/edit/compose/split/retire)；(2) 受 Lotka-Volterra 生态动力学启发的技能交互矩阵，建模技能间互补/冲突，指导检索/变异优先级/退休，治理 库膨胀；(3) anti-pattern me

#### 基础信息

**名称**
SkillSmith

**提出机构**
上海交通大学；东方理工（宁波）；中国科学技术大学；东南大学；宁波数字孪生研究院。作者：Yangbo Wei、Zhen Huang、Shaoqiang Lu、Junhong Qian、Qifan Wang、Chen Wu、Lei He。

**发布时间**
2026-05-31（arXiv v1）

**论文链接**
https://arxiv.org/abs/2606.01314

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 / Tools技能。外部非参数化状态 Sigma=(S,T,F)：技能库 S（workflow + 策略）、工具库 T 与 anti-pattern memory F。模型权重不被触碰；三者均为可检查、可版本化、可迁移的外部资产。

**技能是否独立制品**
是。每个技能 s=(m,w,r,u) 是一个独立可复用的制品：metadata m（名称、触发条件、版本）、workflow body w（编排逻辑 + step 级指令）、reference resources r（模板、领域知识）与标量 utility u。形态 = 结构化技能包（多组件制品，类似技能文件目录）。

**是否文档载体**
混合。核心载体是 workflow body w，包含可读的 step 级编排指令（类似指令文档），但该包还捆绑了可执行脚本与 reference resources；工具暴露可执行实现 f。以指令为中心 + 内嵌可执行代码 => 混合。

#### 技能表示

**技能编码方式**
多文件技能包，结合自然语言 SOP/workflow 指令（workflow body w）+ 可执行脚本/代码（工具实现 f，带接口描述 d 与类型签名 sigma）+ reference resources/模板 + metadata + 标量 utility。技能与工具是互补、相互引用的制品。

**技能粒度**
子任务 workflow / 完整技能包。一个技能封装面向任务的策略与多步编排逻辑（调用多个工具）；粒度为覆盖一类任务的完整可复用能力包。

#### SKILL.md_专属维度

**编辑粒度**
bundle（技能+工具原子联合编辑）。Reflection 发出一个原子 proposal bundle L，在一个事务中联合更新技能与工具；工具编辑限定于五种类型化 lifecycle
primitives（Wrap/Edit/Compose/Split/Retire）。原子性保证相互依赖的 skill+tool 变更同时应用，避免无效中间状态（定理：bundle 变异相比单类型编辑扩展了可达有效状态集 Omega）。

**版本与门控**
Pareto 前沿 + 留出验证门控（held-out）。维护实例级 Pareto 前沿 G（一个状态若在 >=1 个训练实例上最优即为 non-dominated）；准入前有渐进式验证门控：tool unit test -> 端到端
integration test -> regression check；候选仅在通过全部阶段后才被准入。从 Pareto 前沿采样，按 per-instance unique-best 计数加权。

**文档来源**
失败轨迹蒸馏。Proposal bundle 由 reflection 在失败执行轨迹上生成（失败集 F={x: P(x)<theta}）；以失败驱动的诊断配合结构化 feedback function
mu_f（编译错误、缺文档报告、约束违反）。亦经累积的 anti-pattern memory 做 session 经验提取；技能可通过对 non-dominated 血脉的 crossover 合并。

**技能库治理**
库膨胀治理（Lotka-Volterra/退休/归档）+ 去重合并。受 Lotka-Volterra 竞争-互利启发的生态 utility 模型：技能交互矩阵 beta_ij 由执行日志估计（正=互补、负=冲突）；承载容量 K
捕获在检索/context/维护预算下的竞争；utility dynamics 优先处理 mutation/retirement。低于退休阈值达 T_ret 轮的技能被退休，并转化为 anti-pattern memory 中的
epitaph。Synergy-aware merge/crossover 在 non-dominated 血脉间去重。消融：-Eco 使库膨胀至 21+7（长期 >80），而完整版为 14+6。

**失败记忆**
是。Anti-pattern memory F：每个条目 phi=(p,a,c) = 失败签名 p + 因果归因 a + 补救 c。两种机制：(1) 诊断加速——检索相似的历史失败并将先验归因注入 reflection
context；(2) proposal veto——在提交前阻断形似已知失败模式的 bundle。另有 retirement-to-epitaph pipeline 将退休技能转为失败记录。消融：移除它使回归率升至三倍（2.1% ->
7.6%）。

**协同进化**
skill-tool + skill-skill 生态。主轴 = skill-tool 协同进化，通过原子 bundle 联合编辑技能与工具。次轴 = skill-skill 生态动态（Lotka-Volterra 交互矩阵建模在共享
context 容量下的成对互补/冲突）。Anti-pattern memory 作为第三类资产协同进化。非 generator-verifier 对抗（那是 CoEvoSkills 基线）。

#### 自进化机制_How

**进化方法范式 (How)**
co_evolutionary + population_evolutionary + rollout_optimization。在离散结构化外部策略空间上的非梯度、文本空间优化：reflection 驱动的 bundle
proposal（GEPA 风格的反思式文本进化），种群维持在实例级 Pareto 前沿，配以 mutation + synergy-aware merge/crossover 算子；生态 utility dynamics
引导搜索。权重上无 gradient/SFT/RL。

**学习信号来源**
成败轨迹 + 自我反思 + 留出验证分 + 工具成功率指标。训练 minibatch 上的黑盒任务分 P(x)；归一化残差 z(x)=P(x)-b(x) 消除任务难度混淆；结构化 feedback mu_f（编译错误、缺文档报告、约束违反）；留出验证门控；工具错误率被跟踪。

**奖励粒度**
hybrid（混合）。Outcome 信号 = 任务分 P(x)；process 信号 = feedback function mu_f 抽取编译错误 / 缺文档报告 / 约束违反；synergy 信号 = 共激活残差 beta_ij。

**学习范式**
offline + sleep-time。在训练集 D_train 上以执行预算 B 做迭代式离线进化，在留出 D_val 上评估；进化轮次在部署之间运行（inter-test-time / sleep-time 重放失败），而非 intra-task 在线权重更新。

#### 进化时机_When

**进化时机 (When)**
inter-test-time + sleep-time。进化以离散迭代推进：每次迭代从 Pareto 前沿采样一个候选，执行一个 minibatch，收集失败，并应用一个已验证的 bundle 更新。并非在单个任务内的 intra-test-time 在线进行。

**触发方式**
失败触发 + 工具退化触发。每次迭代从 minibatch 构建失败集 F={x in M: P(x)<theta}；reflection 由失败触发，并按下降的 utility 趋势 Delta_u 与负交互 beta_ij（冲突/抑制）排定优先级。工具层瓶颈（工具错误/过时工具）激活 Tool-Smith。

#### 存储与检索

**技能库结构**
DAG 血脉 / Pareto 前沿。non-dominated 系统状态 Sigma 的实例级 Pareto 前沿 G；经共同祖先追踪血脉以做 synergy-aware merge/crossover；退休技能作为 epitaph
归档于 anti-pattern memory。实质为版本化的 DAG 血脉 + Pareto 归档。

**检索/复用方式**
语义相似度 + description 匹配触发加载 + utility/interaction 重排。Retrieval score(s_i,q,S_act) = alpha*sim(s_i,q) + gamma*u_i +
delta*Sum_j beta_ij - eta*cost(s_i)，结合语义相关性、动态生态 utility、与已激活技能的成对交互兼容性及执行成本。

#### 验证与反馈

**验证方式**
执行验证（execution-based）+ 留出评估 + validation gating（门控）+ 功能正确性检查。渐进式验证流水线：tool unit testing（当 bundle 含工具操作时）-> 端到端
integration testing -> regression checking（对合并候选，conditioned on 其父代表现强劲的 task families）。留出 D_val 性能为优化目标。

**错误纠正**
自我修订 + 回滚 + 有界编辑 + 定向 diff 修补。Reflection 经有界类型化编辑修订失败配置；无效候选被验证门控拒绝（回滚）；anti-pattern veto 防止重蹈已知坏方向；受损工具在扰动后经 lifecycle ops 重建；退休技能的信息转移到 epitaph。

#### 环境与基座

**测试环境**
tool-call + 通用 + 真实生产力任务。OfficeQA（跨文档表格定位 + 结构化文档上的多步数值推理）、SealQA（开放网络 QA，含噪声/冲突的搜索结果）、WildClawBench（真实多模态 agent 部署，15-50 步任务，多工具，高交互密度）。

**底座模型**
开源 LLM（Qwen3.5）。横跨五个规模评估：9B、27B、35B、122B、397B。Proposer R 与 Tool-Smith B_tau 为 LLM 驱动；模型权重与 optimizer/target 无关（进化的是非参数化外部状态）。

**部署域 (Where)**
general（通用）。横跨文档 QA、网络搜索 QA 与多模态真实 agent 生产力任务；不专精于单一垂直领域。

#### 评估指标

**评估指标**
success_rate / generalization（跨模型/跨任务复杂度 scaling）/ skill_library_growth / cost / 回归率。报告准确率、按模型规模的 gain-vs-base、多技能共激活 vs 收益、回归率、工具错误率、最终库规模、长期库规模、计算成本分解（附录 F）。

**关键结论**
OfficeQA @397B：80.1%（+18.3% vs Base）；SealQA @397B：49.5%（+18.9%）；收益随规模单调增长（OfficeQA +2.8%@9B ->
+18.3%@397B）。WildClawBench：SkillSmith 持续改进至第 6 天，而 SkillClaw 在第 2-4 天停滞（工具层瓶颈）；在工具密集类目上优势最大。消融（122B）：锁定工具层（Skill-only）=
最大跌幅（-6.8% WCB）；FreeTool => 14.7% 工具错误（4.6x）；-Eco => 库膨胀 21+7（100 轮内 >80），准确率 68%-><35%；-Anti => 回归 2.1%->7.6%（三倍）且
40-60% 振荡。韧性：扰动后 SkillSmith 在第 100 轮恢复至 ~70%，而 EvoSkill 卡在 ~30%；库保持在 28 个组件以下。Scaling：收益从简单任务上的 ~5-10% 升至高度复杂任务上的 >20%。

#### 局限与挑战

**局限与挑战**
无生态治理下的 doc_bloat（文档膨胀）（库 >80 个组件，准确率崩溃）；无 anti-pattern memory 下的 regression_risk；optimizer_quality 依赖
reflection/proposer LLM 质量；类型化工具 primitive 限制表达力（vs FreeTool tradeoff）；可迁移性仅在 Qwen3.5 家族内评估（cross-harness/cross-vendor
未测）；预算 B 下 bundle 验证的计算成本。论文第 5 节自述局限 [uncertain - 全文未捕获]。

#### 可借鉴要点

**可借鉴要点**
(1) 原子 skill+tool bundle 编辑：当 SKILL.md 自我进化时，允许同一原子事务同时 wrap/edit/compose/split/retire
它所依赖的工具——这修复了根因（过时/脆弱的工具），而非用过臃肿的技能文本来过度补偿，并避免无效中间状态。单一最大消融跌幅来自锁定工具层。(2) 生态库治理：从执行日志估计 skill-skill 交互矩阵（互补 vs
冲突）与全局容量（Lotka-Volterra），再按动态 utility 优先处理 mutation/retirement/dedup——这正是防止 SKILL.md 库膨胀并保持检索干净的所在。(3) 带 veto 的
anti-pattern memory：持久化失败签名 + 因果归因 + 补救，在 reflection 中检索它们以加速诊断，并对重复已知错误的 proposal 编辑硬 veto——这把回归率降低 ~3x 并稳定长期进化。

#### 不确定字段

- code_link
- doc_form（token 长度）
- cross_transfer（cross-harness / cross-task / cross-user 轴线）
- safety_guardrails（pre-edit backup/rollback、human-in-the-loop）
- limitations（论文第 5 节自述）

---

### CoEvoSkills (EvoSkills)

> `academic_doc_skill` · 2026。Generator-Verifier 协同进化验证框架，让 agent 自主构建复杂多文件 skill 包， 无需 ground truth。Skill Generator 迭代精炼 skill；信息隔离的 Surrogate Verifier 独立进化测试断言，提供密集可执行反馈，规避自我验证的确认偏差。SkillsBench 上 Claude Code/Codex 双 SOTA，跨 

#### 基础信息

**名称**
CoEvoSkills (also referred to as EvoSkills in the paper body and on evoskills.net; arXiv title and GitHub repo use CoEvoSkills)

**提出机构**
伊利诺伊大学芝加哥分校（主导）；MBZUAI；麦吉尔大学；哥伦比亚大学；浙江大学；英属哥伦比亚大学。作者：Hanrong Zhang、Shicheng Fan、Henry Peng Zou、Yankai Chen、Zhenting
Wang、Jiayu Zhou、Chengze Li、Wei-Chieh Huang、Yifei Yao、Kening Zheng、Xue (Steve) Liu、Xiaoxiao Li、Philip S. Yu。

**发布时间**
2026-04-02（arXiv v1）；2026-04-12（v2）

**论文链接**
https://arxiv.org/abs/2604.01687

**代码链接**
https://github.com/Zhang-Henry/CoEvoSkills（MIT 许可证；项目主页 https://evoskills.net；查看时仓库标注 'Code coming soon'）

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
工具技能 (skills)。进化的对象是一个结构化的多文件技能包 S = (code + SKILL.md + scripts/assets)；模型权重不被触碰。第二个协同进化的对象是 Surrogate Verifier 测试套件 V。目标/部署 agent 的权重同样不变——只有外部技能制品进化。

**技能是否独立制品**
是。技能是一个独立可复用的制品：一个由相互依赖的多文件制品组成的结构化包（Anthropic Agent Skills 概念）。形式 = 多文件技能包，包含 SKILL.md（指令）+ 可执行 code/scripts + 参考 assets，区别于单一自包含的工具函数。

**是否文档载体**
混合。核心载体包含一份可读的指令文档（SKILL.md），但该包同时打包了可执行 code/scripts 与 assets；以指令为中心 + 内嵌可执行代码 => 混合（指令文档 + 代码）。

#### 技能表示

**技能编码方式**
遵循 Anthropic Agent Skills 格式的多文件技能包：SKILL.md 指令文档 + 可执行 code/scripts + 参考 assets，作为一个包 S 产出。Surrogate Verifier 将其测试编码为每个任务+环境对应的合成测试套件 V（断言/脚本）。

**技能粒度**
完整技能包。一个技能为一类多步专业任务封装一个完整可复用的能力（指令 + 脚本 + assets），大于一个原子动作或单一工具函数。

#### SKILL.md_专属维度

**编辑粒度**
全新生成 / 整文档重写。每次修订 S(i+1) 由 generator LLM（Eq.7）读取当前技能 S(i) 连同追加到上下文 C 的累积 verifier 反馈产生（C(i+1)=C(i)⊕F(i,j)）——即由 LLM
采样迭代式地整体重新生成多文件包，而非 minimal-diff/PATCH/有界 add-delete-replace。上下文增长由上下文上限 β=0.7 约束。

**版本与门控**
留出验证门控（held-out）+ best-snapshot 保存。一个留出的 Ground-Truth Oracle 在全新环境中重新执行技能并仅返回一个不透明的 pass/fail 信号；每当 reward 改进时保存最佳快照
S*（当 R(i)>R_best 时 S*←S(i)）。单一技能线，迭代式精修（非 Pareto-front / DAG lineage）。oracle-pass 触发部署；oracle-fail 触发新一轮 co-evolution
迭代。

**文档来源**
LLM 一次性生成 + 失败轨迹蒸馏。初始技能 S(0) 由 generator 在给定指令 I + 一个教授如何创建技能的领域无关 meta-skill S_meta（skill-creator）下采样得到；后续版本基于累积的
Surrogate Verifier 失败诊断 F(i,j)（失败测试用例 + 根因分析 + 可操作的修订建议）进行精修。非人工初始化，非成功轨迹回放。

**协同进化**
generator-verifier 协同。核心设计 = Skill Generator + Surrogate Verifier 通过迭代式 generate-verify-refine 循环协同进化：generator 在固定测试套件
V 下精修技能 S 以最大化 surrogate reward R~；当 surrogate 通过但 oracle 失败时，verifier 升级其测试 V。严格为 generator-verifier 协同进化（非
skill-tool，非 skill-skill 生态，非 skill-prompt）。

#### 自进化机制_How

**进化方法范式 (How)**
co_evolutionary + rollout_optimization（非梯度，文本空间优化）。通过迭代式 LLM 采样进行非梯度、文本空间优化：技能精修 S(i+1)~πθ(·|S(i),C(i+1))；测试升级
V(j+1)~πθV(·|I,x(i),V(j))。无 SFT、权重上无 RL——仅对外部技能制品进行纯 co-evolutionary 搜索。

**学习信号来源**
留出验证分（ground-truth oracle 不透明 pass/fail）+ LLM-as-judge（surrogate verifier 合成其自己的测试）。surrogate verifier reward R~(x,V)
作为不透明 ground-truth reward R 的密集代理；verifier 的逐断言失败诊断补充了二值 oracle 信号。

**奖励粒度**
hybrid（混合）。Outcome = ground-truth oracle 二值 pass/fail；process = 来自 Surrogate Verifier 的逐断言结构化失败诊断（失败测试用例、根因分析、可操作的修订建议）。

#### 进化时机_When

**进化时机 (When)**
inter-test-time / sleep-time。离线 co-evolution 在部署到目标 agent（Claude Code / Codex）之前按任务执行；非单次任务执行期间的 intra-test-time 在线。每个任务平均在约 4.1 个验证周期 / 约 2.4 个 oracle 轮次内收敛。

**触发方式**
失败触发。surrogate 测试失败触发技能精修（最大化 R~）；surrogate 通过与 oracle 失败之间的差距（指示符 1[R~(x,V)=1 ∧ R(x^)<1]）触发测试升级，使 verifier 独立地强化其测试。进化最多运行 N=5 个 oracle 轮次，并在 oracle 通过时提前终止。

#### 验证与反馈

**验证方式**
surrogate verifier（无 gt）+ 留出评估（held-out ground-truth oracle）+ 执行验证（execution-based）+ validation gating（门控）。Surrogate
Verifier 按任务+环境合成测试用例/脚本，并在不访问 ground-truth 的情况下提供密集的逐断言失败诊断；留出的 Ground-Truth Oracle 在全新环境中重新执行并仅返回不透明的 pass/fail；oracle
通过即门控部署。

**错误纠正**
自我修订 + 重规划。Skill Generator 每一轮从追加到上下文的累积失败诊断 F(i,j) 修订整个技能包；当 surrogate 与 oracle 不一致时，测试升级迫使 verifier 独立地强化测试。除 S* 的 best-snapshot 保存外，无显式的有界 diff / 回滚。

#### 环境与基座

**测试环境**
SkillsBench。SkillsBench（Li et al., 2026b）：覆盖 11 个领域的 87 个任务，带确定性 verifiers；首个用于评估 agent 技能的系统性 benchmark。部署 harness：Claude Code 与 Codex。

**底座模型**
Claude（Opus 4.6 进化 agent；Sonnet 4.5、Haiku 4.5 迁移）+ GPT-5.2（进化 agent + 迁移）+ 开源 LLM（Qwen3-Coder-480B、DeepSeek
V3-671B、Mistral Large 3-675B 用于迁移）。optimizer/target 分离：进化（generator+verifier）由前沿 LLM（Claude Opus 4.6 或
GPT-5.2）驱动；进化后的技能随后部署到并迁移跨多个目标模型。

**部署域 (Where)**
general（通用）。SkillsBench 横跨 11 个领域（含 Natural Science 等）；面向通用的多步专业/编程风格的 agent 任务，而非单一垂直领域。

#### 评估指标

**评估指标**
success_rate（SkillsBench pass rate）/ 泛化（跨模型迁移到 6 个 LLM / 5 家公司；跨 harness Claude Code vs Codex）/ 成本（验证周期、oracle
轮次、进化迭代次数）。还报告进化轨迹（pass rate vs round）与跨 11 个领域的逐领域分解。

**关键结论**
在 SkillsBench 上（Claude Opus 4.6 + Claude Code）：71.1% pass rate，相对 no-skill 基线（30.6%）+40.5pp，相对人工策划技能（53.5%）+17.6pp，在
Claude Code 与 Codex 上均为 5 个基线中最高。Skill-Creator 基线仅 34.1%；CoT-guided 单次变体 30.7%。进化轨迹：到第 3 轮超越人工策划技能，到第 5 轮约 75%。消融：移除
Surrogate Verifier 使 71.1% -> 41.1%；仅背景上下文 48.6%；无验证约 30.7%。跨模型迁移：跨 6 个模型 +36 至 +44pp（如 GPT-5.2 用迁移技能 +40.2pp 至
65.0%，自进化 69.8%；Mistral Large 3 4.9% -> 43.1%）。成本：每个任务平均 4.1 个验证周期和 2.4 个 oracle 轮次；surrogate verifier 吸收约 60% 的迭代（仅
2.4/4.1 升级到 oracle）。案例研究：定性方法转换 BLS -> TLS，两阶段搜索在 exoplanet transit 任务上达到 100%。

#### 局限与挑战

**局限与挑战**
optimizer_quality（依赖一个强前沿 LLM 同时充当 generator 与 verifier——Claude Opus 4.6 / GPT-5.2）；成本（ground-truth oracle
在全新环境中的重新执行开销大，尽管 surrogate 吸收了约 60% 的周期）；最终门控需要一个确定性的 held-out oracle（不透明的 pass/fail 仍预设一个 oracle 存在——在完全无 oracle
的领域可能不可用）；每个任务单一技能线带 best-snapshot 保存（无 Pareto archive / multi-program lineage，故相对 population
方法的回归保护有限）；跨模型可迁移性强，但共享库内的跨任务未研究；库级治理（dedup/retirement/bloat control）未涉及。eval-hacking 由信息隔离缓解。论文自述局限（Section 5 /
Discussion）[uncertain - 未抓取全文]。

#### 可借鉴要点

**可借鉴要点**
(1) 信息隔离的 surrogate verifier 以规避确认偏置：将 SKILL.md 自我进化拆分为一个 generator 和一个完全隔离的 verifier 会话——后者只看到任务指令与产出的输出文件（对 generator
的推理、code 与当前 SKILL.md 不可见），并让它按任务+环境合成其自己的测试用例/脚本。verifier 返回密集的逐断言诊断（失败用例 + 根因 + 修订建议），而留出的 oracle 仅返回一个不透明的 pass/fail
位——这在不泄露留出测试内容的情况下产出可操作的反馈，并防止 verifier 继承 generator 的偏置。消融：移除它使 71.1% 崩塌至 41.1%。(2) 持久上下文 + 测试升级循环：保持一个持久化的对话上下文
C（有上限，如 β=0.7）跨迭代累积 verifier 反馈，并仅当 surrogate 通过但 oracle 失败时触发测试升级——迫使 verifier 在看不到 ground truth
的情况下独立强化其测试。这收敛很快（每个任务约 4.1 个周期、约 2.4 个 oracle 轮次），并产生真正的定性方法转换（BLS -> TLS），而非仅是参数调优。(3) 将技能视为一个协同进化的多文件包（SKILL.md +
code + scripts），每一轮基于累积反馈整体重新生成，单一迭代技能线由 best-snapshot 保存门控（仅当 oracle reward 改进时部署 S*）。这比 Pareto/lineage archive 更简单，却达到
71.1%，并以 +36-44pp 的增益跨 6 个模型 / 5 家公司迁移。

#### 不确定字段

- doc_form（SKILL.md / 技能包的典型 token 长度）
- library_governance（未描述多技能库治理）
- failure_memory（除每任务累积的上下文外是否存在结构化的 anti-pattern memory）
- safety_guardrails（编辑前备份/回滚、人工在环、密钥/注入检查）
- learning_paradigm（显式的 sleep-time / inter-task replay 框架）
- library_structure（跨任务技能库结构）
- retrieval_method（新颖的检索方案；依赖 Anthropic 技能加载）
- limitations（论文 Section 5 / Discussion 自述局限）

---

### EvoSkill

> `academic_doc_skill` · Sentient Labs + Virginia Tech, 2026。将 GEPA 的单文件提示优化扩展为「技能(.md)+系统 提示词」联合变异，每次迭代生成新 agent 程序。五阶段：base agent 跑当前程序→proposer 分析失败轨迹→generator 写新 skill 文件/重写系统提示→evaluator 在留出集打分→Pareto 前沿保留 top-N 为 git 分

#### 基础信息

**名称**
EvoSkill: Automated Skill Discovery for Multi-Agent Systems (Coding Agents)

**提出机构**
Sentient Labs (sentient-agi)。作者：Salaheddin Alzubi、Noah Provenzano、Jaydon Bingham、Weiyuan Chen、Tu Vu（Tu Vu 隶属 Virginia Tech）。

**发布时间**
2026-03-03（arXiv v1 提交于 2026 年 3 月 3 日）；开源代码仓库持续维护。

**论文链接**
https://arxiv.org/abs/2603.02766

**代码链接**
https://github.com/sentient-agi/EvoSkill

**类型**
academic (arXiv paper) + industry/open-source framework (Apache-2.0 toolkit, evoskill CLI).

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能。Whole-agent program = system prompt + skill set（.claude/skills/*/SKILL.md + helper
scripts）物化于磁盘；模型权重 FROZEN。每次迭代产出一个全新的 agent program（skill_only 和/或 prompt_only 变异模式）。架构（单 agent）与权重不被进化。

**技能是否独立制品**
是。每个技能是一个独立的可复用制品，打包为一个文件夹：.claude/skills/{name}/SKILL.md（指令 markdown）+ metadata + helper scripts。一个 program 还携带
.claude/program.yaml（system prompt + allowed tools + output format + score）。技能被显式设计为可跨 coding-agent harness
移植（agentskills.io 注册中心）。

**是否文档载体**
混合（以指令文档为中心）。核心载体是可读的 SKILL.md markdown 指令文件，但技能文件夹额外捆绑 helper scripts/代码；Skill Generator 读取一个 'skill-creator'
技能以强制规范格式。因此指令 markdown 为主载体 + 内嵌/可执行 helper 代码 => 混合，偏于是。

#### 技能表示

**技能编码方式**
技能文档（.md / SKILL.md）+ 多文件技能包。每个技能 = 技能文件夹内的 SKILL.md markdown 指令（含 metadata + helper scripts）；program 本身被编码为
program.yaml（结构化 YAML：name、parent、generation、system_prompt、allowed_tools、output_format、metadata/score）。

**技能粒度**
完整技能包 / 子任务 workflow / 策略规则。每个发现的技能打包一个连贯的可复用能力（如 percentage-calculator、financial-table reader）——一个针对一类失败驱动能力缺口的完整技能包，比完整 agent 小，比原子动作大。

#### SKILL.md_专属维度

**编辑粒度**
全新生成（通过 action='create' 创建新技能文件夹 + SKILL.md）+ 编辑已有技能（对 target_skill 执行 action='edit'）+ 整系统提示重写（prompt_only 模式每次迭代整体重写
base_agent/prompt.txt）。SkillProposerResponse 选择 create 还是 edit；Generator 物化整个文件，而非 minimal-diff/PATCH；每次迭代是一次变异。文档级没有有界
add/delete/replace diff 原语。

**版本与门控**
留出验证门控（held-out）+ git 分支前沿选择 + DAG 血脉。每个新 program 在一个 Proposer 永不可见的留出验证集上打分；仅当其留出分击败前沿最差成员时才被接纳进
top-N「frontier」（frontier_size 默认 3）（ProgramManager.update_frontier：单目标分排序剪枝）。前沿成员打上 frontier/* 标签；每个 program 是一个带 parent
指针、构成 DAG 血脉（get_lineage/get_children）的 git 分支 program/{name}。论文将其表述为「a Pareto frontier of agent
programs」；在代码中前沿是单目标（留出准确率）top-N archive，而非真正的多目标 Pareto 前沿。选择策略：best / random / round_robin。

**文档来源**
失败轨迹蒸馏（failure-trace-driven induction）。技能从 agent 失败案例中归纳：Base agent 在 TRAINING 划分上运行当前 program；Skill Proposer
分析失败轨迹（为何失败）并提出一个技能；Skill Generator 写出 SKILL.md。博客副标题：「Automated Skill Induction from Agent Failures」。

**跨载体迁移**
跨模型 + 跨 agent harness + 跨任务 + 跨基准。跨 harness：Claude Code、OpenCode、Codex CLI、OpenHands、Goose、Harbor 均支持（harness
抽象层；技能文件夹跨它们移植）。跨模型：用一个冻结 LLM 进化的技能迁移到其他模型（在后续 EvoSkills 论文 arXiv:2604.01687 中演示；经 OpenRouter/Anthropic/OpenAI/Fireworks
支持 Claude/GPT/GLM/Minimax/Kimi/Gemini/Qwen）。跨任务/跨基准：在 SealQA 上进化的技能 zero-shot 迁移到 BrowseComp（+5.3%）。四条迁移轴线全部覆盖。

**技能库治理**
frontier 剪枝（淘汰最差）+ 感知已有技能的提案。frontier 的 update_frontier 在满员时驱逐最低分 program => 隐式退役/剪枝。Skill Proposer
被要求在提案前列出/检查已有技能，并引用被 DISCARD 的迭代（related_iterations 血脉）以避免重复；skill-creator 技能强制规范紧凑格式。无显式去重/合并、相似度检索编辑定向、curator loop 或
Lotka-Volterra 动力学。

**失败记忆**
是。(1) .claude/feedback_history.md 记录 Proposer 每次迭代尝试了什么以及为何成功/失败。(2) SkillProposerResponse.related_iterations
引用过去被丢弃的尝试，使 Proposer 从先前失败中学习并避免重复。(3) feedback_descent.py 累积失败理由，且关键地，在候选获胜时 RESET feedback
history（陈旧失败被遗忘，因为基线已移动）。用作负反馈以重定向搜索并否决重复的坏方向。

**协同进化**
skill-prompt 联合 + generator-verifier 协同。主 = 跨技能（.md）与 system prompt 的联合变异空间（skill_only vs prompt_only 模式；论文摘要将「whole
agent = system prompt + skill set」与「skills + system prompt 的联合变异」作为框架）。次 = generator-verifier 风格流水线：Skill/Prompt
Proposer（分析师）-> Skill/Prompt Generator（写者）-> Evaluator（留出验证器）。非 skill-tool 协同进化（工具是固定的 allowed-tools 列表，不被进化），也非显式的
skill-skill 生态模型。

#### 自进化机制_How

**进化方法范式 (How)**
population_evolutionary + rollout_optimization（非梯度，文本空间）+ reward-based。将 GEPA 的反馈驱动文本进化从单文件 prompt 优化扩展到
whole-program（skill+prompt）进化：维护一个 agent program 的种群（frontier）；每次迭代由 LLM Proposer 从失败轨迹提出文本空间变异，LLM Generator 物化新的
SKILL.md/prompt 文件，留出 Evaluator 给新 program 打分；top-N frontier 选择保留幸存者。权重上无 gradient/SFT/RL（权重冻结，纯 prompt/skill 文本空间优化）。

**学习信号来源**
成败轨迹 + 留出验证分 + LLM-as-judge + 执行验证。训练划分上的失败轨迹驱动 Proposer；留出验证准确率门控 frontier 接纳（标量 reward）。可选 Scorer
类型：multi_tolerance/exact（字符串）、llm（LLM-as-judge，如 SealQA 用 GPT-5-mini 打分）、script、harbor（内置验证器）以及 code-execution
pass@1（LiveCodeBench 在 Docker 中运行代码）。

**奖励粒度**
outcome（结果），带部分得分容差。每题 outcome 打分（multi-tolerance 对 0/1/2.5/5/10% 容差加权平均；或 LLM A/B/C 等级 => 1.0/0.0；或 pass@1），聚合为留出集上的平均准确率。无 process/step 级 reward。

**学习范式**
offline + on-policy + benchmark 驱动。在划分为 train/val 的 benchmark 数据集上离线进化（而非单任务执行期间的在线）；on-policy 体现在每个候选 program
通过实际全新运行冻结 agent 来打分。「Continuous evolution」（从常规使用中改进）与「evolution without a benchmark」被显式列为开放/🛠️，尚未实现。

#### 进化时机_When

**进化时机 (When)**
inter-test-time（任务间离线）。自我改进循环作为批处理在 benchmark 评估运行之间离线执行（而非单任务执行期间的 intra-test-time）。由于运行耗时数小时，可卸载到
Docker/remote/Daytona 沙箱；在调度时实质具备 sleep-time 能力，但默认语义为 inter-test-time。

**触发方式**
失败触发 + 周期性（epoch/iteration 循环）。每次迭代在训练划分上运行 agent，收集失败（score<0.8），并触发 Proposer->Generator 循环；循环重复最多 max_iterations（默认
20）次，在连续 no_improvement_limit（默认 5）次无改进后早停。触发在固定迭代预算内由失败驱动，而非使用驱动。

#### 存储与检索

**技能库结构**
git 分支 + 技能文件目录 + DAG 血脉 +（云端注册中心）。programs = git 分支 program/{name}（program/base、program/iter-skill-*）；frontier 成员以
frontier/* 标签标记；program.yaml 中的 parent 指针构成 DAG 血脉（get_lineage/get_children）；技能以文件夹形式存在于 .claude/skills/{name}/
下；可移植技能文件夹也发布到云端注册中心（agentskills.io）。

**检索/复用方式**
description 匹配触发加载（原生 agent skill discovery）。技能在各 harness 的原生 skill-discovery 机制下于 agent 运行时加载（Claude 的
setting_sources=['user','project'] 加载 .claude/skills/；Goose summon 扩展；Codex .agents/skills/ 软链；OpenCode project
config）。Skill Proposer 显式列出/读取已有技能以决定 create 还是 edit（通过列出/description 检索，而非向量相似度）。无 embedding/BM25 检索。

#### 验证与反馈

**验证方式**
执行验证（execution-based）+ 留出评估 + validation 门控 + LLM-judge + 功能正确性检查。新 programs 在留出验证集上打分（门控 frontier 接纳）。打分按 harness 基于
execution：multi-tolerance/exact 字符串匹配、LLM-as-judge（SealQA）、shell-script scorer、Harbor 内置验证器，以及经 Docker
代码执行的功能正确性（LiveCodeBench pass@1）。

**错误纠正**
自我修订 + 回滚 + 有界编辑 + 重规划。非改进候选被丢弃（git 分支删除 = 回滚）；下一次迭代的 Proposer 重新分析失败，并在 feedback_history.md 与 related_iterations
指导下重新规划一个不同的 skill/prompt 变异；有界编辑为 create-new 或 edit-existing SKILL.md（不对整个技能库做破坏性整体重写）。feedback_descent 在发现新的最优后遗忘陈旧失败。

#### 环境与基座

**测试环境**
通用（QA + coding + tool-call）。OfficeQA（基于美国财政部数据的 grounded reasoning）、SealQA（带噪声检索的 search-augmented
QA）、BrowseComp（browse，zero-shot 迁移目标）、DabStep、LiveCodeBench（coding，Docker 代码执行）、SWE-bench-verified（Harbor 容器化
benchmark）。

**底座模型**
Claude / GPT / 开源 LLM（multi-model）。任意 model
provider（Anthropic、OpenAI、OpenRouter、Fireworks）与任意模型（Claude、GPT-5/o3、GLM、Minimax、Kimi、Gemini、Qwen）。optimizer
agents（Proposer/Generator/Evaluator）与目标 agent 均为 LLM 驱动且可以是不同的 LLM；权重全程冻结。默认目标如 claude-sonnet-4-6 / gpt-5。

**部署域 (Where)**
general（通用）-> specialized。将通用 coding agents 转变为专家；测试覆盖 office/finance grounded reasoning、search-augmented QA、browse 与
coding 领域。部署制品 = 复制 .claude/program.yaml + .claude/skills/ 到用户的 agent 项目中。

#### 评估指标

**评估指标**
success_rate（accuracy）+ generalization（跨任务/跨模型/跨 harness zero-shot 迁移）+ cost（total_cost_usd、duration_ms、每次运行的 token
用量被跟踪）+ skill_library_growth（发现的 # skills、frontier 大小）+ sample_efficiency（收敛迭代数）。实时进度表打印 Iter / Accuracy / Delta /
Skills / Frontier / Status。

**关键结论**
OfficeQA：+7.3% exact-match（60.6% -> 67.9%）。SealQA：+12.1%（26.6% -> 38.7%）。Zero-shot 迁移 SealQA -> BrowseComp：+5.3%（无修改）（表明
skill 级优化产生超越训练任务的可迁移能力）。跨模型迁移在 EvoSkills 后续工作中演示。frontier = 作为 git 分支保留的 top-N programs。

#### 局限与挑战

**局限与挑战**
scalability（运行耗时数小时；每次调用 20 分钟超时、3x 指数退避重试；长运行需 Docker/Daytona 卸载）+ optimizer_quality（严重依赖强 Proposer/Generator LLM；只读
Proposers 限于 8 个工具）+ regression_risk（验证门控能捕获回归，但非改进迭代被浪费；例如 -1.6% 的迭代被丢弃）+ transferability（跨任务可行但有界；跨 harness
可移植性是假设而非穷尽 benchmark）+ eval-hacking（由留出划分缓解，但 benchmark 驱动循环固有）。灾难性遗忘 N/A（权重冻结）。Continuous-evolution 与 no-benchmark
evolution 显式为开放项（🛠️）。

#### 可借鉴要点

**可借鉴要点**
(1) 留出验证门控 + frontier/top-N 选择 + WHOLE programs 的 git 分支版本化：将每个（system prompt + skill set）视为一个原子「program」制品，将其版本化为独立的
git 分支（program/*、frontier/* 标签、parent->child 血脉），并仅当其击败留出集时才接纳该变异；这带来安全回滚、完整可 diff 性（git diff 任意两个进化状态），并通过 Proposer
永不可见的严格 train/val 划分防止 eval-hacking/过拟合。这一单一设计使 SKILL.md 自我进化可审计且回归安全。(2) 带分离 Proposer/Generator/Evaluator
角色的失败轨迹驱动归纳：每次编辑都由具体 agent 失败驱动（在训练划分上运行 agent -> 收集失败 -> Proposer 诊断根因 -> Generator 写出简洁 SKILL.md -> 留出 Evaluator
打分）；保持 Proposers 严格只读（无 Write/Edit）以强制 analyze-then-act，并累积+遗忘反馈（候选获胜时重置失败记忆），使搜索适应新基线。(3)
标准化可移植技能文件夹（.claude/skills/{name}/SKILL.md + metadata + helper scripts）作为跨 harness/跨模型/跨任务的通用货币：在一个任务/模型/harness
上进化技能，并在其他地方原样复用（SealQA->BrowseComp +5.3% zero-shot），将「skill text」转化为独立于冻结权重的可迁移、非参数资产。

#### 不确定字段

- doc_form（SKILL.md / program.yaml 的确切典型 token 长度）
- safety_guardrails（未确认显式 human-in-the-loop 或密钥/注入扫描；推断为缺失）

---

### DRAFT (From Exploration to Mastery)

> `academic_doc_skill` · RUC + Baidu, ICLR 2025 Oral(前1.8%)。迭代精炼工具 docstring(结构化 NL 文档： description/parameters)。三角色循环：Explorer 生成多样尝试→Analyzer(LLM-as-judge) 做信用分配归因到具体文档缺陷→Rewriter 更新 docstring。含探索多样性约束 + 基于 BLEU/ 余弦相似度的工具自适应

#### 基础信息

**名称**
DRAFT (From Exploration to Mastery)

**提出机构**
中国人民大学高瓴人工智能学院 + 百度 + 中国科学院计算技术研究所（通讯作者 Jun Xu）

**发布时间**
arXiv v1 2024-10-10，v2 2025-02-26；ICLR 2025 Oral（top 1.8%）

**论文链接**
https://arxiv.org/abs/2410.08197

**代码链接**
https://github.com/quchangle1/DRAFT

**类型**
academic (ICLR 2025 Oral paper, open-source reference implementation)

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示（context / prompt）：注入 LLM prompt context 的工具文档（docstring）。不是模型权重、不是工具/API 本身、不是 agent 架构——仅是描述每个工具的冻结、外部提供的文本。

**技能是否独立制品**
是。精炼后的工具文档是独立、可复用、人类可读的文本制品（结构化 docstring：description + parameters）。每个工具产出一次，可作为 raw doc 的 drop-in 替换插入任何下游 LLM 的 prompt context。

**是否文档载体**
是（纯可读的自然语言指令文档是核心载体）。进化对象是结构化 NL docstring（description + parameters + usage notes）；所有学习都表达为对该文档的文本编辑，无代码、无向量表示。

#### 技能表示

**技能编码方式**
docstring——结构化自然语言（一个 'description' 字段 + 一个 'parameters' 字段，外加 usage notes）。最接近限定于单一工具的自然语言 SOP；非可执行代码、非 API schema、非向量嵌入。

**技能粒度**
单工具粒度上的完整技能包：覆盖一个工具用途、参数与用法的完整 docstring。粗于原子动作，细于多工具 workflow。

#### SKILL.md_专属维度

**编辑粒度**
每轮迭代整文档重写：Rewriter 每轮产出工具文档的完整新版本 t_i（条件为前一版本、探索实例、工具反馈、Analyzer 的 NL 建议与完整修订历史 T_i）。非有界 add/delete/replace、非 minimal
diff、非 PATCH。迭代仅由 tool-adaptive termination 界定。

**版本与门控**
无基于质量的版本门控（无留出验证、无 Pareto 前沿、无 git branch、无人工评审、无备份/回滚）。仅有一个 tool-adaptive 的基于 CONVERGENCE 的终止：当两个连续文档版本足够相似时停止，以 Δ =
(cosine(embedding) + BLEU) / 2 > τ = 0.75 度量（嵌入来自 OpenAI text-embedding-ada-002）。这是 early-stop，而非 accept/reject 门控。

**文档来源**
人工编写 / 数据集初始化（来自 RestBench / ToolBench 的原始工具文档 t_0）+ 经自驱动 trial-and-error 探索的成败轨迹蒸馏（Explorer 实际调用工具，Analyzer 将结果归因于文档缺陷）。将人工初始化的文档与执行反馈蒸馏相融合。

**跨载体迁移**
跨模型（明确为论文的头条发现）：以 GPT-4o 为 backbone 精炼的文档迁移到 GPT-4o-mini 和 Llama-3-70B；以 Llama-3-70B 精炼的文档也泛化到其他模型。非跨 agent
harness、非跨工具（文档是 tool-specific 的）、非跨用户/团队。给出的理由：decoder-only LLM 共享 transformer 结构与预训练语料，故收敛于相似的理解需求。

**技能库治理**
库级别无治理。每个工具的文档独立精炼；无全局技能库、无去重、无 retirement/archival、无 Lotka-Volterra、无分层索引。嵌入上的 cosine 相似度仅用于探索多样性控制（单一工具迭代内 φ = 0.9），不用于库级别检索/编辑目标选择。

**失败记忆**
部分。Analyzer 充当 LLM-as-judge 执行 CREDIT ASSIGNMENT——它将一次失败试验归因于具体的文档缺陷（缺失约束、参数歧义等），并产出 NATURAL-LANGUAGE（而非标量）建议
s_i。Rewriter 额外消费完整修订历史 T_i 以避免冗余/重复编辑。然而，无显式 anti-pattern 存储、无失败特征注册表、无作为跨工具持久负反馈保留的 rejected-edit buffer。

**编辑安全**
有限。唯一的护栏是 tool-adaptive termination（BLEU+cosine > τ=0.75），它界定迭代并防止过拟合 / 文档膨胀。无强制范围边界（框架仅按构造编辑文档，但不硬性守护源代码）、无编辑前备份或回滚、无
eval-hacking 防御、无人工在环确认、无密钥/注入检查。该过程明确为全自动。

**协同进化**
skill-only：仅工具文档进化；底层工具/API 固定且不被修改。内部存在一个三角色分工（Explorer = generator、Analyzer = LLM-as-judge verifier、Rewriter =
editor）协作于单一制品，但无独立制品的协同进化（无 skill-tool 协同进化、无两个进化系统的 generator-verifier 协同进化、无 skill-skill 生态）。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（非梯度、经 trial-and-error 的文本空间优化），融合 reward-based 学习，使用 INTERNAL TEXTUAL 反馈（Analyzer 是一个返回自然语言 credit
assignment 而非标量 reward 的 LLM-as-judge）。实现为三阶段迭代循环：experience gathering -> learning from experience -> documentation
rewriting。无梯度（SFT/RL）更新。

**学习信号来源**
LLM-as-judge（Analyzer 的 NL 评判）+ 工具执行结果（Explorer 的真实工具调用返回值/错误）+ 自我反思（当相似度约束被违反时 Explorer 由多样性驱动的自我反思）。无环境标量 reward、无留出验证分。

**奖励粒度**
hybrid：process 级反馈（Analyzer 每迭代的 NL credit assignment，诊断哪个文档缺陷导致了哪个失败）结合 outcome 级信号（每次探索实例中工具的实际执行结果/错误）。

**学习范式**
离线 + on-policy。所有精炼作为预处理步骤在文档部署到下游任务之前离线完成；Explorer 相对当前文档版本 t_{i-1} on-policy 地生成新鲜探索实例。非 sleep-time（无夜间 cron / 空闲时回放过往会话）。

#### 进化时机_When

**进化时机 (When)**
inter-test-time：文档在部署之间离线精炼，作为每个工具的一次性预处理 pass。下游任务执行期间无 intra-test-time 学习。

**触发方式**
按需 / 任务驱动：DRAFT 作为每个工具的预处理步骤被显式运行（最多 I = 5 次迭代）。当连续版本相似度 Δ 超过 τ = 0.75 时，每个工具的终止被自动触发。无事件/cron/课程触发；无持续的 usage-driven 循环。

#### 存储与检索

**技能库结构**
扁平：一个逐工具的文档集 D 被独立精炼；无层级、无 vector DB（嵌入仅即时计算用于相似度检查）、无图谱、无 DAG lineage、无云端注册中心。输出仅为一个修订后的文档集 D~。

**检索/复用方式**
部署：标准直接注入——精炼后的 docstring 通过 description/name 匹配加载到 LLM 的 prompt context（常规 tool-doc 配给，与 ReAct/DFSDT/EasyTool
基线相同）。精炼期：OpenAI text-embedding-ada-002 嵌入上的 cosine 相似度用于强制探索多样性，而非检索编辑目标。无 BM25、无 LLM re-rank。

#### 验证与反馈

**验证方式**
LLM-as-judge（Analyzer）+ 基于执行的信号（Explorer 的真实工具调用）。无留出验证门控、无代理验证器、无功能正确性单元测试、无多模型辩论。下游评估（CP%、Win%）与精炼循环留出隔离——即精炼循环看不到评估集，故精炼期间无留出门控。

**错误纠正**
经迭代整文档重写的自我修订（每轮 Rewriter 在 Analyzer 的 NL 建议与修订历史 T_i 引导下产出新 t_i）+ 经 tool-adaptive termination 的有界迭代。无回滚、无定向 diff patch、无轨迹级别的重规划。

#### 环境与基座

**测试环境**
tool-call benchmark：RestBench（TMDB——54 个电影 API；Spotify——40 个音乐 API）与 ToolBench（最难的 I3-Instruction 子集，需要不同类别的多个工具）。

**底座模型**
GPT-4o 是 DRAFT 用于精炼文档的 backbone/optimizer（既探索又重写的模型）。部署/推理目标：GPT-4o、GPT-4o-mini、Llama-3-70B。Optimizer 与 target
可为同一模型或不同（跨模型）。嵌入经由 OpenAI text-embedding-ada-002。

**部署域 (Where)**
general——通用 tool-use / tool-call 领域（跨异构真实世界类别的 API 调用：电影、音乐、web API）。

#### 评估指标

**评估指标**
success_rate 经由 Correct Path Rate（CP%——真实工具路径是预测调用的子序列）与 Win Rate（Win%——相对 ReAct 的成对 ChatGPT
评估器偏好）衡量；泛化以精炼文档的跨模型迁移衡量；消融衡量 diversity-promoting exploration 与 tool-adaptive termination 的贡献。

**关键结论**
RestBench-TMDB CP%（GPT-4o）：ReAct 71.00 -> DRAFT 88.00；Llama-3-70B 72 -> 86；GPT-4o-mini 48 -> 62。RestBench-Spotify
CP%（GPT-4o）：28.07 -> 70.17。ToolBench CP%（GPT-4o）：37 -> 51；Llama-3-70B 41 -> 53；GPT-4o-mini 35 -> 47。头条：GPT-4o-mini +
DRAFT（CP 47）在 ToolBench 上击败无 DRAFT 的 GPT-4o 基线（CP 37）。稳健的跨模型泛化：GPT-4o 精炼的文档迁移到 GPT-4o-mini 和 Llama-3-70B；Llama-3-70B
精炼的文档也泛化；GPT-4o 作为 optimizer 产出最佳结果（方法受益于更强的 backbone）。TMDB 上的消融（GPT-4o）：完整 DRAFT CP 88 -> 去 diversity-promoting
exploration 为 84 -> 去 tool-adaptive termination 为 80，证实两种机制均有贡献。被接收为 ICLR 2025 Oral（top 1.8%）。

#### 局限与挑战

**局限与挑战**
若迭代过多则 doc_bloat / 过拟合（冗余信息累积——仅由基于相似度的终止缓解而非消除）；optimizer_quality（更强的 backbone GPT-4o 产出明显优于 Llama-3-70B
的文档）；regression_risk / 回归风险（无留出验证门控，故终止基于相似度而非性能，可能在局部相似但次优的文档处停止）；对非常大 / 快速演化的工具生态的可扩展性未被验证；评估限于三个 tool-call
benchmark（无多模态、无超越工具选择的 agentic 多轮规划）；无显式安全/eval-hacking 护栏；精炼文档是 tool-specific 的，故不跨工具迁移。

#### 可借鉴要点

**可借鉴要点**
- 带 NATURAL-LANGUAGE（而非标量）credit assignment 的三角色自驱动 trial-and-error 循环：Explorer 生成多样的真实工具调用尝试并捕获执行结果；Analyzer（LLM-as-judge）执行 credit assignment，将每次失败归因于一个具体的文档缺陷，并输出定位的 NL 建议；Rewriter 整合建议与完整修订历史以重写文档。NL credit assignment 是关键——它给予编辑器可操作、已定位缺陷的反馈而非数值分数，可直接移植到任何 SKILL.md self-evolution agent。
- 经由 query embedding 上的 cosine 相似度约束（φ = 0.9，OpenAI ada-002）外加自我反思再生的 diversity-promoting exploration，确保文档在广泛的行为谱（边界情况、参数组合、错误源）上而非 canonical/easy 查询上被压力测试。廉价、model-agnostic，且可立即复用以保证自探查任何指令文档时的覆盖度。
- 经由双重相似度（Δ = (BLEU + cosine) / 2 > τ = 0.75）的 tool-adaptive convergence termination——一个轻量、无需留出集的逐工具 early-stop，既节省计算又防止过拟合/文档膨胀。当留出验证集不可用时，任何迭代文档重写 agent 都可采用其作为一个最小、无需训练的 convergence gate。

#### 不确定字段

- doc_form

---

### SkillWeaver

> `academic_doc_skill` · OSU/UVA/Purdue/CMU/Cisco, 2025。技能 = Python 函数 + 自然语言 docstring(含描述+先前 执行日志+前置条件)。三阶段：技能提议(LLM 自动课程)→合成(成功轨迹蒸馏为 API)→打磨 (自动测试+环境反馈)。运行时 --allow-recovery 用定向 diff 修补 API。docstring 侧即文档 技能进化。arXiv:2504.0

#### 基础信息

**名称**
SkillWeaver

**提出机构**
The Ohio State University (OSU NLP Group)、University of Virginia、Purdue University、Carnegie Mellon University、Cisco
Research。作者：Boyuan Zheng、Michael Y. Fatemi、Xiaolong Jin、Zora Zhiruo Wang、Apurva Gandhi、Yueqi Song、Yu Gu、Jayanth
Srinivasa、Gaowen Liu、Graham Neubig、Yu Su。

**发布时间**
arXiv v1 2025-04-09

**论文链接**
https://arxiv.org/abs/2504.07079

**代码链接**
https://github.com/OSU-NLP-Group/SkillWeaver

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Tools技能。agent 演化出一个持续增长的、由可复用技能组成的技能库，这些技能以 Python API（Playwright 浏览器自动化函数）的形式物化。模型权重不被触碰；技能/API 库是唯一进化的、可迁移的、非参数化资产，用以扩展 agent 的动作空间。

**技能是否独立制品**
是。每个技能是一个独立可复用的制品：一个 Python 函数文件（知识库条目，如 kb_post_code.py），由函数签名、自然语言 docstring 与 Playwright 代码体组成。轻量、即插即用的 API 扩展 agent 的动作空间；以文件形式存储在每个网站的知识库路径前缀下。

**是否文档载体**
混合。技能载体主要是可执行的 Python 代码（API 体），但每个 API 都带有丰富的自然语言 docstring（描述 + 先前执行使用日志 +
网站前置条件状态），它充当可读的指令文档并跨执行自我更新。指令文档（docstring）+ 内嵌可执行代码 => 混合；docstring 侧是文档形式的技能演化通道。

#### 技能表示

**技能编码方式**
可执行代码（Python API，带 Playwright 浏览器自动化）+ docstring（NL 描述 + 使用日志 + 前置条件）。驱动该流水线的 prompt/模板另外以独立的 .md 文件组织在
skillweaver/templates 下。以代码为中心的技能，每个 API 由一条 NL docstring 注释。

**技能粒度**
子任务 workflow。每个 API 封装一个可复用的子任务 workflow，分为三种被提出的类型：过程化任务（多动作流程自动化）、导航类任务（系统化的页面/分区探索）与信息检索类任务（专门的抓取）。技能库将许多子任务 API 聚合为一个完整的 per-website 技能包。

#### SKILL.md_专属维度

**编辑粒度**
全新生成（synthesis/polishing 期间的整函数重生成）+ 定向 diff 修补（运行期的 targeted diff patching）。Stage II 从一条成功轨迹合成出一个全新的 Python 函数；Stage
III 通过 env 反馈重新调试/重生成；运行期 --allow-recovery 对在测试中抛出异常的 API 应用定向 diff 进行修补（有界编辑而非整体重写）。

**版本与门控**
留出验证门控（held-out）/ validation gating。每个候选 API 必须通过 Stage III honing：自动生成的单元测试（对无参 API 直接执行；对参数化 API 用 LLM 生成的参数测试用例），外加一个
LLM reward-model/success-checker 判定任务完成情况。--allow-unverified-apis 默认为 False，即未能在无运行期错误下执行的 API
会被门控挡掉。迭代目录（iter_N）提供每轮版本快照。

**文档来源**
成功轨迹归纳 + 执行录像回放 + LLM 一次性生成。成功的实践轨迹（带截图的 state-action 对）被一个 LLM 蒸馏/泛化为一个 Python API；docstring 的使用日志从执行录像回放/更新。失败轨迹另外喂入 Stage III 调试。

**跨载体迁移**
跨模型 + 跨 agent harness + 跨任务。跨 agent（模型）迁移是头条结果：由强 agent（gpt-4o）合成的 API 显著提升较弱 agent，在 WebArena 上高达 +54.3%。跨 harness
迁移经一个实验性的 Browser-Use 版本得到验证，该版本将知识库转换为 Browser-Use Controller 对象，扩展另一个 agent 的动作空间。技能还在一个网站内跨任务迁移。

**技能库治理**
在 proposal 时通过显式 prompt 让 LLM 提出超出当前储备的新颖/可复用技能来实现多样化（diversity-driven
auto-curriculum）；三种任务类型（过程化/导航/信息检索）拓宽覆盖面。技能库逐网站迭代增长。显式的去重/合并/淘汰机制（Lotka-Volterra、归档、curator loop）[uncertain - 论文/README
未描述]。

**失败记忆**
是（隐式、per-API）。docstring 使用日志记录先前的执行（per-API 成功/失败历史）；Stage III polishing 消费失败轨迹与 reward-model 反馈来调试 API；运行期异常触发
--allow-recovery 修补。一个带归因+补救的、作为汇聚负反馈 buffer 的专用全局 anti-pattern / failure-signature 存储 [uncertain - 未描述]；失败记忆是 per-API 与
per-iteration 的，而非共享的 anti-pattern 记忆。

**编辑安全**
scope 边界（仅合成/修补 API .py 文件，不碰 agent 源码）+ 执行验证（对生成代码做静态分析以捕捉常见错误 + 准入前做基于执行的单元测试）+ validation
gating（--allow-unverified-apis=False 默认）+ 有界编辑（运行期做定向 diff 恢复而非破坏性整体重写）。编辑前备份/回滚、人工在环、eval-hacking 防御 [uncertain - 未描述]。

**协同进化**
skill-tool。技能即工具：合成的技能成为即插即用的 API，直接扩展 agent 的动作空间，故技能进化与工具进化是同一对象。存在 generator-verifier 色彩（API-synthesis LLM 对
reward-model/success-checker LLM），但主导轴线是 skill-as-tool 自我扩展；无单独的 skill-skill 生态动态。

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration + rollout_optimization（非梯度、文本空间）。成功的执行轨迹被一个 LLM 蒸馏（模仿）为泛化的 Python API；迭代的探索 rollout 渐进扩展 API
库。权重上无 gradient/SFT/RL——纯 LLM 驱动的合成 + 环境验证的迭代。

**学习信号来源**
成败轨迹（成功轨迹被蒸馏；失败被调试）+ LLM-as-judge（reward-model/success-checker LLM 从轨迹 + 截图 + env 反馈判定任务完成）+ 工具成功率指标（API 无运行期错误的执行作为准入信号）。

**奖励粒度**
outcome。reward model 在一条轨迹之后判定任务完成情况（被提出技能任务的成功/失败），而非逐步的 process reward。

**学习范式**
offline + sleep-time。一个专门的探索阶段（skillweaver.explore，如 160 iterations）在离线/sleep-time 运行以构建 API
库；随后合成的库在线部署（attempt_task/evaluate_benchmark）而无需进一步权重更新。在探索轮次之间存在 inter-test-time 进化。

#### 进化时机_When

**进化时机 (When)**
inter-test-time + sleep-time。技能的发现/合成/honing 发生在一个专门的离线探索循环中（在真实任务之间/之外）；运行期任务执行仅可选地触发恢复修补（当 --allow-recovery 开启时的 intra-test-time 有界修复）。

**触发方式**
curriculum（课程）驱动（LLM auto-curriculum 在每个探索 iteration 提出技能）+ 失败触发（运行期 API 异常触发恢复修补；Stage III honing 由单元测试失败 + 负向
reward-model 判定触发）。由 iteration 计数驱动的探索调度（--iterations、--explore-schedule）。

#### 存储与检索

**技能库结构**
技能文件目录。per-website 知识库目录（如 skill_library/reddit/reddit_kb_post、logs/explore-reddit-gpt4o/iter_N/kb_post）；每个技能 = 一个
_code.py 文件加元数据；iteration 快照为技能库做版本管理。扁平的 per-website 文件目录，而非向量库或 DAG 谱系。

**检索/复用方式**
description 匹配触发加载 + 代码直接复用。在任务期，agent 被给予 per-website API 集合（带其 docstring 描述/前置条件），并按描述选择/调用匹配的 API；经验证的 Playwright
代码体被直接复用（非 generation-as-retrieval——复用的是确切的经验证代码）。LLM 基于 docstring 描述在 API 之间做选择。

#### 验证与反馈

**验证方式**
执行验证（execution-based）+ LLM-judge + validation gating（门控）+ 功能正确性检查。Stage III：无参 API 作为独立单元测试运行；参数化 API 获得 LLM
生成的参数测试用例；reward-model/success-checker LLM（gpt-4o）判定完成情况；静态分析捕捉常见代码错误；未经验证的 API 默认被门控挡掉。

**错误纠正**
定向 diff 修补 + 自我修订。运行期 --allow-recovery 通过定向 diff 修补抛出异常的 API；Stage III polishing 使用 env 反馈 + reward-model 信号 + 自动单元测试对 API 做自我修订。运行期做有界编辑而非整体重生成。

#### 环境与基座

**测试环境**
Web。WebArena benchmark（shopping、shopping_admin、reddit、gitlab、map）+ 经 Online-Mind2Web 任务的真实世界网站。

**底座模型**
GPT（gpt-4o / gpt-4o-2024-08-06 作为 agent、API 合成与 success checking 的默认值）。在跨 agent 迁移实验中 optimizer/target 分离：强
agent（gpt-4o）合成 API，较弱 agent 消费它们。支持 Azure 托管的 OpenAI。

**部署域 (Where)**
specialized（web/GUI 自动化领域）。

#### 评估指标

**评估指标**
success_rate + 泛化（跨 agent/跨模型迁移；真实世界 Online-Mind2Web）+ skill_library_growth（构建技能库的 iteration 数）+ 成本（探索 iteration 预算）。

**关键结论**
WebArena 相对成功率提升 +31.8%；Online-Mind2Web（真实世界网站）+39.8%；跨 agent 迁移在 WebArena 上高达 +54.3%（强 agent 的 API 提升较弱 agent）；经 160
个探索 iteration，成功率从 25% 升至 38%；较弱 agent 提升 40%-130%。验证了把多样的网站交互 honing 为可迁移、可共享的 API。

#### 可借鉴要点

**可借鉴要点**
(1) 技能 = 可执行 API + 不断演化的 NL docstring：将每个技能编码为一个 Python 函数，其 docstring 承载描述 + 先前执行使用日志 + 前置条件状态，并跨运行更新该
docstring——这是一个既机器可执行又人/LLM 可读的单一制品，docstring 作为文档形式的演化通道。(2) 三阶段 curriculum 驱动的循环（LLM auto-curriculum proposal ->
把成功轨迹蒸馏为泛化 API -> 用自动生成的单元测试 + env-feedback 调试做 polishing）是一条干净、可复现的、零权重更新的自主技能文档演化流水线。(3) 运行期 --allow-recovery 用定向 diff
修补失败技能——有界、经执行验证的编辑而非整体重写，由 --allow-unverified-apis=False 门控——是 in-production 技能自修复的安全范式。

#### 不确定字段

- library_governance（显式的去重/合并/淘汰机制）
- failure_memory（带归因+补救的专用全局 anti-pattern/failure-signature 存储）
- safety_guardrails（编辑前备份/回滚、人工在环、eval-hacking 防御）
- doc_form（典型 token 长度）

---

### OpenSpace

> `engineering_practice` · HKUDS, 2026。开源自进化技能引擎。对执行录像做事后分析，产出 FIX/DERIVED/CAPTURED 最小 diff 编辑 SKILL.md；SQLite DAG 版本化(完整血缘+diff)；质量监控(技能应用率/ 完成率/回退率/工具成功率)；BM25+embedding+LLM skill_ranker 检索；工具退化触发上游 依赖技能的级联进化；云端 open-space.cl

#### 基础信息

**名称**
OpenSpace

**提出机构**
HKUDS（香港大学数据科学实验室）。即 AnyTool、ClawWork 与 nanobot 背后的同一实验室，OpenSpace 在其基础上构建。

**发布时间**
2026-03-25（开源）；v0.1.0 于 2026-04-03 发布。活跃开发至少持续到 2026-04-16。

**代码链接**
https://github.com/HKUDS/OpenSpace

**类型**
industry (open-source self-evolving skill engine / agent framework, MIT-licensed, with a hosted cloud registry at open-space.cloud)

#### 进化对象_What

**进化对象 (What)**
Tools技能 / Context记忆与提示。进化的载体是一个持久化于 SQLite 的外置、非参数化技能库：每个技能是一个 SKILL.md 制品（YAML frontmatter + markdown 正文，可选附带 src/
代码），随时间被发现、应用、监控并重新编辑。模型权重从不改动。grounding agent 的运行期 context 由被注入的技能决定，而共享云端注册中心把单个技能编辑转化为跨 agent 的集体知识。

**技能是否独立制品**
是。每个技能是一个独立可复用的制品，存储为包含 SKILL.md 文件的技能目录（如
openspace/host_skills/delegate-task/SKILL.md、showcase/skills/large-file-write-heredoc/SKILL.md），可选附带 src/ 下的代码资产（如
panel-component-xss-safe/src/utils）。制品遵循 Claude Code / Codex / OpenClaw / nanobot / Cursor 共享的 SKILL.md 约定，从而可跨 host
agent 移植，并可通过云端注册中心共享，附带完整血脉 + diffs。

**是否文档载体**
是。核心载体是可读的指令文档：SKILL.md，顶部为 YAML frontmatter（name、description），其后是带各级标题的 markdown 正文（Problem / Solution / Template /
Step-by-Step / Example / When to Use / Notes）。部分技能在文档内嵌入受围栏代码模板（shell/python heredoc、工具调用示例），少数在 src/
下打包辅助代码，故为以指令为中心、偶有内嵌/打包代码——总体上是一份可读的指令文档。

#### 技能表示

**技能编码方式**
技能文档（.md/SKILL.md），含结构化 YAML frontmatter（name + description）+ 自然语言 SOP / 策略正文，常包含受围栏代码模板（如 python3 heredoc 写入回退、ffmpeg
参数）。当技能附带辅助代码时出现多文件技能包（技能目录 = SKILL.md + src/）。delegate-task / skill-discovery 等 host 技能将工具调用契约（execute_task /
search_skills / fix_skill / upload_skill）编码为 markdown。

**技能粒度**
子任务workflow / 策略规则。165 个进化出的 GDPVal 技能围绕鲁棒执行模式与错误恢复策略，而非领域事实：File-Format I/O 回退、Execution
Recovery（sandbox->shell->heredoc 分层回退）、Document Generation 流水线、Quality Assurance（写后验证）、Task Orchestration、Domain
Workflows、Web/Research。大多数在子任务层级编码一个可复用 workflow 或回退策略。

#### SKILL.md_专属维度

**文档形态**
结构化字段文档：YAML frontmatter（name、description）置于 markdown 指令正文之上。正文采用一致的章节——Problem、Solution、Template（受围栏代码）、Step-by-Step
Instructions、Full Example、When to Use（决策表）、Notes。受围栏代码块承载可复制粘贴的模板（如 heredoc 写入模式）。典型长度适中——示例技能约 1-3 KB / 几百到约 1k
tokens；delegate-task host 技能（含工具 schema + JSON 示例）处于较长一端。当打包辅助代码时出现多文件包（panel-component-xss-safe = SKILL.md +
src/utils）。

**编辑粒度**
最小 diff / PATCH。patch.py 支持多文件 FULL / DIFF / PATCH 应用；README 强调「产生最小、定向的 diff
而非整文档重写，并在失败时自动重试。」三种编辑结果：FIX（就地修复，同一技能新版本）、DERIVED（新技能目录与父代并存）、CAPTURED（从一次成功执行中诞生的全新技能）。故粒度 = 每次进化的有界最小
diff，而非整文档重新生成。

**版本与门控**
DAG 血脉版本化 + validation gating（门控）+ 确认门控。SQLite 存储维护一个版本 DAG，含完整血脉 + 逐版本 diff；每个进化版本在替换其前代之前均经验证。确认门控降低误报触发，anti-loop
守卫防止失控循环。前代在 DAG 中保留（支持回滚）。未使用 held-out / Pareto-front 选择（那是 SkillSmith）；准入由血脉 + validation 门控。staging+backup 通过 DAG
持久化隐式实现。

**文档来源**
执行录像回放 + 成功轨迹归纳 + 失败轨迹蒸馏 + 人工初始化 + 社区共享。(1) 人工初始化种子：delegate-task 与 skill-discovery 的 SKILL.md 由人工撰写；My-Daily-Monitor
通过分析开源 WorldMonitor 播种。(2) Post-Execution Analysis 回放完整执行录像（analyzer agent loop，具工具访问）并提出 FIX（源自失败）/ DERIVED（源自父代）/
CAPTURED（源自一次成功运行的新颖模式）。(3) 云端社区共享从其他 agent 导入进化技能。

**编辑安全**
scope 边界（技能目录 / SKILL.md 编辑，而非任意源码）+ 编辑前血脉 备份/回滚（版本 DAG 保留前代）+ 确认门控（confirmation gates 降低误报）+ anti-loop
guards（防止失控进化循环）+ safety checks（标记 prompt injection 与 credential exfiltration）+ 替换前代前的 validation + 有界编辑（基于 diff
的最小编辑，非破坏性重写）。人工在环为可选：host agent 决定是否将进化技能上传至云端。安全加固还涵盖 zip 解压 / import_skill 路径穿越修复，以及 pinned litellm 以规避供应链 CVE。

**协同进化**
skill-tool + skill-skill 生态 + 社区 collective。(1) skill-tool：当工具成功率下降时，quality monitor 找出所有上游依赖技能并批量进化它们——沿 skill->tool
依赖图的显式级联协同进化。(2) skill-skill：当共享组件退化时，依赖技能共同进化。(3) community：云端注册中心让一个 agent 的改进成为每个相连 agent 的升级。非 generator-verifier
对抗。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（非梯度，文本空间）+ imitation_demonstration。非梯度、LLM 驱动的文本空间进化：一个 analyzer agent（具 codebase 探索 +
工具访问）反思执行录像并发出最小 diff（FIX/DERIVED/CAPTURED），经 FULL/DIFF/PATCH 应用。CAPTURED 本质上是 imitation——从成功轨迹中蒸馏出制胜 workflow。一个版本 DAG
维护技能版本的血脉/种群。无 SFT、无 RL、无梯度更新。

**学习信号来源**
成败轨迹 + 工具成功率指标 + 自我反思（LLM analyzer agent loop）+ 执行录像。信号：任务完成 / 成功 / 失败 outcome；技能级 applied rate、completion
rate、effective rate、fallback rate；工具调用 success rate、latency、flagged issues；代码执行状态与错误模式。analyzer 本身是一个 LLM
agent（LLM-as-judge 风格），在决定编辑前于 codebase 中收集证据。

**奖励粒度**
hybrid（混合）。outcome 信号 = GDPVal 上的任务成功 / 完成 / 收入捕获；process 信号 = 逐步工具 success rate、代码执行错误模式、驱动 metric monitor 的逐技能 applied/completion/fallback 率。

**学习范式**
offline + sleep-time + inter-test-time。技能在任务内被检索并应用（在线使用），但 EVOLUTION 相对任务离线发生：Post-Execution Analysis 在每个任务完成后运行；Metric
Monitor 周期性运行（每日）；Tool-Degradation 触发为事件驱动。无 on-policy 梯度更新。版本 DAG replay = 执行录像的 sleep-time replay。

#### 进化时机_When

**进化时机 (When)**
inter-test-time + sleep-time。Post-Execution Analysis 在每个任务后运行（任务之间）；Metric Monitor 周期性扫描技能健康度（sleep-time /
定时）；Tool-Degradation 触发在事件发生时启动。非单次任务执行期间的 intra-test-time 在线编辑。

**触发方式**
事件触发（任务后 Post-Execution Analysis）+ 失败触发（源自损坏技能 / 失败执行的 FIX）+ 工具退化触发（tool success-rate 下降 -> 上游依赖的级联进化）+ 周期性（Metric
Monitor 对 applied/completion/fallback 率的周期扫描）+ 使用驱动（源自成功执行的 CAPTURED）。三条独立触发防线对抗技能退化。

#### 存储与检索

**技能库结构**
DAG 血脉 + 技能文件目录 + 云端注册中心。本地：动态重扫技能目录 + 持有版本 DAG（含完整血脉与逐版本 diff）的 SQLite 存储 + embedding
cache（.openspace/openspace.db）。云端：open-space.cloud 注册中心用于 public/private/group 共享，每次进化均带完整 diff 的血脉追踪。前端 dashboard 可视化
Skill Classes、Cloud Records、Version Lineage 图、Workflow Sessions。

**检索/复用方式**
BM25+embedding+LLM 重排。skill_ranker.py 实现 BM25 + embedding 混合排序；registry.py 做发现 + BM25/embedding 预过滤 + LLM
选择；grounding/core/search_tools.py 是一个 Smart Tool RAG = BM25 + embedding + LLM。host 侧 skill-discovery SKILL.md 触发
description-match 加载；云端搜索为 relevance + 低 latency 升级。auto_import 将顶部云端命中拉取到本地。

#### 验证与反馈

**验证方式**
执行验证（execution-based，analyzer 探索 codebase 并重跑）+ validation gating（门控，替换前代前 validated）+ LLM-judge（analyzer agent loop）+
功能正确性检查（grounding agent 重执行，QA 技能验证输出）。analyzer 在编辑前于 codebase 中收集真实证据，而非盲目生成。

**错误纠正**
自我修订（FIX in-place）+ 定向 diff 修补（FULL/DIFF/PATCH）+ 回滚（前代保留于版本 DAG）+ 有界编辑（bounded minimal diffs）+ 重试（失败时 automatic retry）。FIX 模式修复损坏/过时指令；当工具退化时级联进化修复上游依赖。

#### 环境与基座

**测试环境**
GDPVal + 真实生产力任务 + tool-call + 通用。GDPVal（220 个真实世界专业任务 / 44 种职业，50 任务子集打分，ClawWork protocol，基于 LLM 的打分）。类别：Documents &
Correspondence、Compliance & Form、Media Production、Engineering、Spreadsheets、Strategy & Analysis。Showcase：My Daily
Monitor——60+ 技能、20+ 面板的实时 dashboard 自主构建（零人工代码）。通用 agent harness 集成（Claude Code / Codex / OpenClaw / nanobot）。

**底座模型**
开源 LLM（Qwen 3.5-Plus）用于 GDPVal benchmark——与 ClawWork 基线相同，故增益纯粹源自技能进化。backbone 经 LiteLLM 可插拔（Anthropic Claude、MiniMax
等）。optimizer/target 分离：analyzer/evolver LLM（提出 diff，有自己的 agent loop + 工具访问）与 grounding 执行 agent（target）相互独立。云端使用
embedding 模型做技能搜索。

**部署域 (Where)**
general（通用）。横跨 coding、DevOps、web research、桌面/GUI 自动化、办公与专业生产力（薪酬、税务、法律备忘录、合规表单、电子表格、媒体制作、工程交付物）。被设计为面向任何兼容 SKILL.md 的 agent 的通用技能进化层。

#### 评估指标

**评估指标**
经济价值捕获（value capture %、$ 收入）/ cost（token usage，-45.9%）/ success_rate（收入、质量）/ skill_library_growth（165 个技能）/
generalization（跨类别、跨 harness）/ 回归率（经 validation gating + anti-loop 控制）。质量监控指标：技能 applied rate、completion rate、effective
rate、fallback rate；工具 success rate、latency、flagged issues；代码执行状态与错误模式。

**关键结论**
GDPVal（50 任务，Qwen 3.5-Plus，与 ClawWork 相同 backbone）：收入比 ClawWork 高 4.2x；72.8% value capture（$11,484 / $15,764 任务价值，所有
agent 中最佳）；70.8% 平均质量（较最佳 ClawWork agent 的 40.8% 高 +30pp）；Phase 2（warm rerun）相对 Phase 1（cold start）token usage -45.9%。在
50 个 Phase-1 任务上自进化出 165 个技能。逐类别（收入 Δ / token Δ）：Documents +3.3pp / -56%、Compliance & Form +18.5pp / -51%、Media
Production +5.8pp / -46%、Engineering +8.7pp / -43%、Spreadsheets +7.3pp / -37%、Strategy & Analysis +1.0pp / -32%。技能
taxonomy（165）：File Format I/O 44（32 个源自失败 captured）、Execution Recovery 29（28 个源自崩溃 captured）、Document Generation
26（document-gen-fallback 进化 13 个版本——迭代最深）、Quality Assurance 23、Task Orchestration 17、Domain Workflow 13、Web & Research
11。关键 insight：多数进化技能是工具可靠性 + 错误恢复模式，而非领域知识。Showcase：My Daily Monitor——从零起 60+ 技能（6 seed -> +8 scaffold -> +25 build ->
+12 FIX -> +15 DERIVED -> +8 CAPTURED）、20+ 实时 dashboard 面板、零人工代码。

#### 可借鉴要点

**可借鉴要点**
(1) 由 SQLite 版本 DAG 支撑的 SKILL.md 最小 diff 进化：让 evolver 发出定向 FULL/DIFF/PATCH 编辑（而非整文档重写），持久化每个版本并附完整血脉 +
diff，在每个候选替换其前代前验证它，并在失败时自动重试。正是这使进化 token 廉价（warm rerun 上 -45.9%）、可审计、回滚安全——直接适用于自进化任何 SKILL.md。(2)
由全栈质量监控驱动的三触发级联进化：在每个任务后运行执行录像分析（FIX/DERIVED/CAPTURED），并且对技能 applied/completion/fallback 率运行周期性 metric
monitor，并且有一个工具退化触发经依赖图批量进化所有上游依赖技能。多条独立防线同时捕获隐性技能腐烂与工具/API 漂移——远比仅失败触发鲁棒。(3) SKILL.md 作为通用跨 harness 制品 +
用于集体智能的云端注册中心：一次性将技能撰写为兼容 Claude Code/Codex/OpenClaw/nanobot/Cursor 的 YAML-frontmatter markdown（name + description +
指令正文），经 BM25+embedding+LLM 重排检索，并通过带血脉追踪的 public/private/group 云端注册中心共享——把孤立的自我进化转化为具备网络效应的集体 agent 智能（一个 agent 学习，所有
agent 升级）。

#### 不确定字段

- paper_link（未发现学术论文；以开源框架 + README 形式发布）
- doc_provenance / library_governance（显式库膨胀治理 / retirement / archive 未见文档）
- failure_memory（带失败签名 + 否决的专门 anti-pattern memory store 未被明确描述；仅经 FIX + 安全检查 + 错误模式跟踪隐式存在）
- cross_transfer（跨基准迁移轴线未测试）
- limitations（重度增长下 SQLite DAG / 云端注册中心的可扩展性；自述限制未捕获）

---

### AutoSkill / SkillEvo

> `engineering_practice` · ECNU-ICALK, 2026。Experience-driven Lifelong Learning(ELL)实践。从真实交互经验 (对话+agent 轨迹)自动创建可复用 Skill(SKILL.md 格式)，通过 merge+版本更新持续进化。 Local Skill Manager 做 reusable-experience triage→相似技能检索→discard/improve/ 

#### 基础信息

**名称**
AutoSkill / SkillEvo

**提出机构**
ECNU-ICALK（华东师范大学计算机科学与技术学院），与上海人工智能实验室合作。主要作者：Yutao Yang、Junsong Li、Qianjun Pan（同等贡献）；通讯作者：Jie Zhou、Kai Chen、Liang He。

**发布时间**
arXiv v1 提交于 2026-03-01，v2 于 2026-03-05。发布时间线：AutoSkill 1.0（2025-02-04，对话期技能提取）-> AutoSkill4OpenClaw
1.0（2025-02-26，轨迹驱动技能进化）-> 离线对话提取（2026-03-01）-> AutoSkill4Doc 1.0（2026-03-13，文档转技能流水线）-> SkillEvo
1.0（2026-03-23，回放/评估/变异/晋升框架）。

**论文链接**
https://arxiv.org/abs/2603.01145 (arXiv:2603.01145 [cs.AI], CC BY 4.0)

**代码链接**
https://github.com/ECNU-ICALK/AutoSkill（MIT 许可证；包含 autoskill/ SDK、SkillEvo/ 运行器、AutoSkill4Doc/、AutoSkill4OpenClaw/、SkillBank/、web/、examples/、Docker）

**类型**
academic (formal arXiv paper with Method/System/Experimental sections) AND industry (open-source deployable framework
with Python SDK, Web UI, OpenAI-compatible proxy, Docker Compose). Classified here as academic because the arXiv paper
is the canonical citable artifact.

#### 进化对象_What

**进化对象 (What)**
Context 记忆与提示（外部技能记忆 + 注入的提示 context）。不更新任何模型权重（training-free）。不进化工具定义，不改变 agent 架构。进化目标是一组 Agent Skill
制品（SKILL.md），在推理期被检索并作为附加 context 注入。AutoSkill 明确将自身与更新参数的自进化相对照。

**技能是否独立制品**
是。技能是独立的可复用制品：以 SKILL.md 文件为核心的 Agent Skill，可选地与 scripts/、references/、assets/ 共置为多文件包。每个制品拥有 UUID id、语义版本（如
v0.1.34），并持久化在本地 SkillBank 目录中（Skills/Users/<user_id>/<skill-slug>/SKILL.md 与 Common/<skill-slug>/）。

**是否文档载体**
是（含可选的混合扩展）。核心载体是人类可读的 markdown 指令文档（SKILL.md）。少数技能（如内置的 anthropics-skill 包）还在 scripts/ 下附带可执行代码，使其成为指令+代码的混合包，但 AutoSkill 自身提取的技能是纯 markdown 指令文档。

#### 技能表示

**技能编码方式**
结构化技能文档：YAML frontmatter（id、name、description、version、tags、triggers、examples）+ markdown 指令正文（# Goal、# Constraints &
Style、可选的 # Workflow、Anti-Patterns、Role & Objective、Communication & Style Preferences、Operational Rules）。非可执行代码，非纯向量，非
docstring。AutoSkill4Doc 增加可配置的技能分类法（asset_type:
macro_protocol/session_skill/micro_skill/safety_rule/knowledge_reference）与可见的 domain->family->level1->level2->micro
层次结构。

**技能粒度**
以策略规则 / 见解为主（稳定的用户偏好、风格约束、响应策略、领域操作约定、anti-pattern）。部分技能是子任务 workflow（带显式 # Workflow 区段者，如 Selenium 自动化、文档协同撰写）。AutoSkill4Doc 产出带父子层次结构的完整技能包。原子动作粒度很少见。

#### SKILL.md_专属维度

**文档形态**
结构化字段：YAML frontmatter（id/name/description/version/tags/triggers/examples）+ markdown 正文（Role & Objective、# Goal、#
Constraints & Style、可选的 # Workflow、Anti-Patterns、Output Format）。典型 token 长度：每个技能几百到约 1-2k tokens（案例研究技能 顶级心理咨询师 ~400
tokens、professional_text_rewrite ~600 tokens；AutoSkill4Doc 导航/父技能更大）。多文件包额外包含 scripts/、references/evidence.md +
evidence_manifest.json、assets/。

**编辑粒度**
以全新生成为主（LLM 提取产出一个全新的候选技能）+ 经语义合并的整文档重写（合并模型重写整个技能并保持身份；非原始拼接，非最小 diff/PATCH）。AutoSkill4Doc 的 register_versions 支持
create/strengthen/revise/merge/split/unchanged。SkillEvo 使用 LLM 引导 + 启发式对整段技能文本进行变异。不使用有界 add/delete/replace 或 PATCH
式的精细编辑。

**版本与门控**
多种机制：(1) 合并时补丁号递增的语义化版本（Bump 算子，如 v0.1.0 -> v0.1.1，观测到最高 v0.1.34）；(2) 暂存 + 备份，带回滚 API（POST
/v1/autoskill/skills/{id}/rollback、GET .../versions、_autoskill_version_history）；(3) SkillEvo 增加留出验证门控（冻结的 mutate_dev
划分用于变异，单独的 promotion_test 留出划分；仅当候选击败当前 SkillEvo 冠军时才晋升）；(4) 审查门控采纳（人工可编辑/保存/删除 SKILL.md；AutoSkill4Doc 生命周期
candidate->draft->evaluating->active->watchlist->deprecated->retired）。无 git-branch Pareto 前沿选择。

**文档来源**
会话经验提取（主要：聊天期间从对话用户 query 实时提取）、成功轨迹归纳（用 --success-only 1 从 agent 轨迹离线提取）、执行录像回放（SkillEvo 从存储的 history[].messages
构建冻结的回放池并重放）、LLM 一次性生成（提取器/合并器是 prompt 驱动的 LLM）、人工初始化（种子技能 + 内置 anthropics-skill 导入）、离线 benchmark 训练（在 WildChat-1M
上离线提取以引导 SkillBank），以及 AutoSkill4Doc 的文档提取。通过 import 端点与 Common/ 库进行社区共享。非失败轨迹蒸馏。

**技能库治理**
去重合并（当存在相似的用户技能时优先合并而非新建副本；维护者的主要决策是 add/merge/discard）、相似度检索编辑目标（维护先检索 top-M 最相似技能作为局部证据，而非对整个库推理）、灰尘清理（自动清理陈旧用户技能：默认在
retrieved >= 40 且 used <= 0 时清理；按用户的用量计数器）、层次化索引（AutoSkill4Doc 可见的 domain_root / Family 技能 / 一级技能 / 二级技能 / 微技能
树）。主循环中无显式的 Lotka-Volterra 退役或归档分层（生命周期状态仅存在于 AutoSkill4Doc）。

**失败记忆**
部分。(1) 合并 prompt 强制「避免回归：保留现有技能中的重要检查」与「不要带入陈旧或无关主题的约束」，充当软负向指导。(2) 每个 SKILL.md 正文通常包含一个 Anti-Patterns
区段（如「不要提供医学诊断」、「不要添加开场客套」）作为技能内负向指导。(3) SkillEvo 拒绝未晋升的变异，并在回放数据过小时将谱系保持在「incubating」状态。但不存在专门的 anti-pattern 记忆存储，不存在
failure-signature+attribution+remedy buffer，也不存在跨技能复用为全局负反馈的 rejected-edit buffer（那是 SkillSmith 式的能力，AutoSkill 不具备）。

**编辑安全**
(1) 范围边界：AutoSkill4OpenClaw 明确不替换 OpenClaw 的记忆、ContextEngine、system prompt、工具、provider 选择或模型路由；它仅编辑/镜像 SKILL.md 文件与附加
context。(2) 编辑前备份+回滚：version_history、rollback API、暂存快照、AutoSkill4Doc 的 .runtime/intermediate_runs 用于崩溃恢复。(3) 确认门控 +
人工在环：人工可通过 REST API 与文件系统直接检查/编辑/保存/删除 SKILL.md。(4) 有界编辑防破坏性重写：合并保持技能身份、去重并避免回归；OpenClaw
嵌入模式下不安全的合并目标降级为「add」（不盲目合并）；重复的候选技能在维护前被跳过。(5) Discard 门控拒绝通用/低信号/不可移植的候选以防止技能库噪声。除 SkillEvo 留出划分外无显式 eval-hacking
防御；无密钥/注入检查。

**协同进化**
以 skill-only 为主。技能独立于工具和彼此进化（无 skill-tool bundle 编辑，无 generator-verifier 协同训练）。存在通过合并/去重决策产生的弱 skill-skill
生态交互（新候选与其最近邻技能比较）。AutoSkill4OpenClaw 将技能镜像到 OpenClaw 的工具加载目录，但不进化 OpenClaw 的工具。SkillEvo 是一个 skill-only
的回放/变异循环。因此：skill-only（带轻量 skill-skill 去重联动）。

#### 自进化机制_How

**进化方法范式 (How)**
Training-free、prompt 驱动的组合（无 gradient/RL/SFT）。由 prompt 实例化的五个 LLM 模块：query rewriter、response generator、skill
extractor、management judge、skill merger（+ embedding 模型）。范式混合：(a) imitation_demonstration / 经验蒸馏（提取从用户交互轨迹中抽象出可复用模式）；(b)
reward-based 配合 LLM-as-judge（management judge 决定 add/merge/discard；SkillEvo judge 对二元 eval 规则打分）；(c) 文本空间的
rollout_optimization（SkillEvo：replay -> evaluate -> mutate -> promote，非梯度）；(d) population_evolutionary 元素（SkillEvo
冠军注册表、变异预算）。核心 AutoSkill 循环是 (a)+(b)；SkillEvo 增加 (c)+(d)。

**学习信号来源**
成败轨迹（离线轨迹提取使用 --success-only 1；仅提取含 >=1 个成功主轮次的已关闭会话）、LLM-as-judge（管理决策、SkillEvo judge-LLM 二元规则）、自我反思（提取与合并是 LLM
驱动的抽象）、工具成功率指标 / 使用指标（retrieved/relevant/used 用量计数器驱动清理）。关键在于，提取仅以用户 query {q1..qt} 为证据，而非模型响应 rt，以捕获稳定的用户需求而非模型产物。

**奖励粒度**
outcome（会话/轮次级）。提取在轮次/会话边界后触发；管理决策按候选进行；SkillEvo 晋升是在留出回放样本上的二元 outcome。不使用 process 级逐步奖励。仅在弱意义上混合：用量计数器跨轮次累积。

**学习范式**
在线与离线兼有；在线提取为 on-policy（使用当前模型自身的轨迹）；SkillEvo 回放、离线对话/文档/轨迹批量提取与启动期维护为 sleep-time/离线。在线提取在服务期间于后台异步运行（非阻塞）。因此：online
inter-test-time + offline sleep-time replay。

#### 进化时机_When

**进化时机 (When)**
inter-test-time（轮次/会话后的提取；AutoSkill4OpenClaw 的 agent_end hook）+ sleep-time（SkillEvo 离线回放；在 WildChat
上的离线批量提取；启动期离线维护）。不进行 intra-test-time 进化（轮次内只发生检索+注入；进化循环是异步/后台的）。

**触发方式**
事件触发（轮次/会话关闭后；AutoSkill4OpenClaw 的 agent_end / before_agent_start hooks；OpenAI proxy 在响应后调度提取）、使用驱动（extract_mode=auto 每
extract_turn_limit 轮、=always 每轮、=never 关闭；/extract_now [hint] 强制提取）、失败触发 / 成功触发（用 --success-only 1 的轨迹提取；仅当已关闭会话含 >=1
个成功主轮次时才运行提取）、周期性（AutoSkill4OpenClaw 的 sessionMaxTurns=20 自动关闭长会话以强制一次提取）。非课程驱动，非工具退化触发。

#### 存储与检索

**技能库结构**
技能文件目录（SkillBank/Users/<user_id>/<skill-slug>/SKILL.md + Common/<library>/<skill-slug>/ +
vectors/<embedding-signature>.{meta.json,ids.txt,vecs.f32} + index/skills-bm25.* + skill_usage_stats.json）、向量库（按
embedding 签名索引的磁盘 f32 向量缓存，每个 embedding 模型一个独立索引）、层次化（AutoSkill4Doc 的 domain_root/Family 技能/一级技能/二级技能/微技能 可见树 +
.runtime/document_registry）。版本历史存储在技能元数据内的 _autoskill_version_history 中。无 git-branch 前沿，无云端注册中心（local-first；Docker 挂载
./SkillBank）。

**检索/复用方式**
混合：语义相似度（dense embedding，sim(Memb(q~), Memb(s))）+ BM25 词法，以加权和 Rel = lambda*d_hat + (1-lambda)*b_hat 组合，带 min_score 阈值
eta + top-k。前置 LLM query 重写（解析共指、保留任务锚点、暴露对检索关键的约束）。管理期检索使用单独的权重 alpha 与 top-M 邻居集。AutoSkill4Doc 在元数据丰富的技能文本上使用
embedding + BM25 用于 register_versions。Description/tags/triggers 匹配实际驱动加载。主循环中无 LLM re-rank 步骤（selection.py 有一个可选的 LLM
技能选择器）。

#### 验证与反馈

**验证方式**
LLM-judge（prompt 驱动的 management judge 在四个轴上比较候选与最近邻技能：job-to-be-done、交付物类型、硬约束、所需工具/workflow）、留出评估（SkillEvo：冻结的
mutate_dev 划分用于变异，单独的 promotion_test 留出划分）、功能正确性检查 / 程序化验证（SkillEvo 从 prompt + 需求统计编译 3-6 条二元 eval 规则，由程序化 + judge-LLM
引擎评估）、validation 门控（SkillEvo 仅当候选在 promotion_test 上击败当前冠军时才晋升）、AutoSkill4Doc
生命周期门控（candidate->draft->evaluating->active->watchlist->deprecated->retired）。无多模型辩论，主循环中无基于执行的运行时测试。论文本身未报告下游任务准确率验证。

**错误纠正**
自我修订（LLM 合并经语义并集重写整个技能，移除陈旧/案例特定的内容）、回滚（POST /skills/{id}/rollback + version_history + AutoSkill4Doc
暂存的中间快照用于崩溃恢复）、有界编辑（合并保持技能身份与重要检查以避免回归）、discard（直接拒绝通用/低信号/不可移植的候选）、重规划（query 重写与合并重新框定技能）。无定向 diff 修补；编辑是整文档重新生成。

#### 环境与基座

**底座模型**
以开源 LLM 为主：demo 中使用 InternLM Intern-S1-Pro 与 DashScope Qwen（qwen-plus）；也支持 GLM（Zhipu/BigModel）、OpenAI GPT、Anthropic
Claude 与通用 OpenAI 兼容后端。Embedding：DashScope text-embedding-v4、通用 embd_qwen3vl8b 或 hashing（mock）。Optimizer/target 分离存在于
SkillEvo（通过 --llm-provider/--llm-model 与 --judge-provider/--judge-model 分离 mutation LLM 与 judge LLM），概念上也存在于
AutoSkill（不同模块可共享一个 backbone 或使用不同的）。默认所有模块为同一 backbone LLM，仅以 prompt 区分。

**部署域 (Where)**
general（横跨编程、写作、咨询、办公文档、社媒文案的模型无关个性化层）。AutoSkill4Doc 通过可配置分类法增加 specialized 文档领域（心理学/CBT、化学/分析化学）。主要定位是面向 LLM 助手与个人数字替身的 general 终身个性化层。

#### 局限与挑战

**局限与挑战**
doc_bloat（合并累积内容；仅由合并期去重缓解，无硬 token 预算）、regression_risk（尽管有「避免回归」指令，LLM 合并仍可能丢弃重要约束；仅 SkillEvo 的留出门控守护这一点，而非主 AutoSkill
循环）、controllability / optimizer_quality（提取与合并质量完全依赖底层 LLM 与 prompt；弱模型产出噪声技能）、scalability（技能库随用户/会话增长；清理是简单的
retrieved>=40 && used<=0 启发式，非学习所得）、transferability（跨模型/跨语言在提取上得到验证，但跨模型的检索/注入质量未被 benchmark）、eval-hacking（若
promotion_test 泄漏则可能在 SkillEvo 中发生；由冻结划分缓解但未正式分析）。catastrophic_forgetting 为 N/A（无参数更新）。论文明确缺乏定量下游任务评估。

#### 可借鉴要点

**可借鉴要点**
- Discard 优先的提取策略（anti-noise 门控）：AutoSkill 仅当用户表达持久的约束/偏好/纠正（如「避免幻觉」、机构写作风格）时才提取技能，并对「写一份报告」这类通用一次性请求显式返回空结果。这是保持自进化 SKILL.md 库整洁的最具可操作性的设计：以持久的、可复用的信号门控提取，并默认 no-op。结合仅用户侧证据（从用户 query 提取，绝不从模型响应提取），这产生了干净的学习信号。
- 基于局部证据的检索辅助维护（可扩展性）：AutoSkill 不把整个技能库喂给 judge/merger，而是先检索 top-M 最相似的现有技能，并仅对单一最近邻做出 add/merge/discard 决策。这使维护近似 O(log N) 且聚焦，避免全库推理的成本与 context 膨胀。对自进化 SKILL.md 系统，这是正确的扩展范式：维护决策是局部的。
- 版本化语义并集合并（无重复的持续精炼）：合并时，merger LLM 执行语义并集（非拼接），保持技能身份/UUID，对区段/要点/triggers/tags/examples 去重，剥离案例特定实体，保留先前的重要检查以避免回归，并递增语义补丁版本（v0.1.0 -> v0.1.1 ... 观测到最高 v0.1.34）。这让同一技能持续精炼而非繁殖重复碎片。将其与留出晋升门控（SkillEvo：在 dev 上变异，仅当在留出划分上击败冠军时才晋升）配合，使迭代式 SKILL.md 进化既不重复也不回归。

#### 不确定字段

- type（真正的 academic+industry 混合；被迫单标签）
- cross_transfer（跨基准 / cross-benchmark 迁移未被评估）
- test_env（未确认使用如 AgentBench 的标准化 agent benchmark；StuLife 是相关工作，非 AutoSkill 评估对象）
- metrics（论文未报告 cost/token 经济性与下游任务 success_rate/准确率）
- key_results（无相对基线的正面交锋定量收益；论文仅报告 SkillBank 统计与案例研究）
- learning_paradigm（on-policy 与 off-policy 边界模糊，因为离线提取复用了可能来自不同模型的历史日志）

---

### claude-self-improving-skills

> `engineering_practice` · UniM0cha, 2026。Hermes Agent 风格的 Claude Code 自改进。专用 distiller subagent 从 工作流经验蒸馏为 SKILL.md(遵循 Anthropic skill-creator 指引)。偏好 patch 现有技能→ 伞形技能→加参考文件，仅最后才新建类级技能。编辑安全：pre-edit 备份+post-edit 验证+ provenance 

#### 基础信息

**名称**
claude-self-improving-skills (Claude Self-Improving Skills plugin; internal plugin id `self-improving-skills`)

**提出机构**
独立 / 社区开发者 UniM0cha（GitHub 用户）。无学术或企业机构；独立作者的开源 Claude Code plugin。灵感来自 Nous Research Hermes Agent。

**发布时间**
2026-06-09（GitHub repo 创建；首个公开版本）。v0.9.0 新增 team 技能共享。截至 2026-06-19 仍活跃。[uncertain: 仓库创建之外的首个发布 tag/version 日期未确认]

**代码链接**
https://github.com/UniM0cha/claude-self-improving-skills（MIT 协议，Python）。作为 Claude Code plugin marketplace 安装：先 `/plugin
marketplace add UniM0cha/claude-self-improving-skills`，再 `/plugin install
self-improving-skills@claude-self-improving-skills`。截至 2026-06-19 有 8 stars / 2 forks。

**类型**
industry (open-source framework / Claude Code plugin) leaning blog_practice. Not academic — no paper, no benchmark
evaluation; an engineering port of Hermes Agent's procedural-memory loop into Claude Code primitives.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能。进化的对象是用户在 `~/.claude/skills/<name>/SKILL.md` 处习得的过程记忆库（markdown 指令文档 + 可选的
reference/template/script 文件）。模型权重冻结；Claude Code 的 harness、hooks 与 subagent 架构是固定原语，仅被接入（WIRED）到一个闭环学习循环中。架构是
single-agent-with-background-subagent（一个专用 `skill-distiller` subagent），而非 multi-agent 群体。事实记忆明确不在范围内（由 Claude Code 的原生
memory 处理）。

**技能是否独立制品**
是。每个技能是一个独立可复用的制品，实例化为一个文件夹 `~/.claude/skills/<name>/`，内含一个 `SKILL.md`（指令文档，主要载体）外加可选的
`references/`、`templates/`、`scripts/` 子目录用于存放体积较大的材料。技能位于用户目录，而非 plugin 内部，因此更新 plugin 永远不会抹去累积的知识。Agent 蒸馏的技能携带
`metadata.provenance: self-improving-skills`，以便与 human/team 技能区分。

**是否文档载体**
是（instruction-document-centric）。核心载体是可读的 markdown `SKILL.md`，带 YAML frontmatter（name / description / metadata.provenance
/ origin）与正文（## When this applies / ## The technique / ## Gotchas）。其混合之处仅在于：一个技能文件夹可以在正文中一行所指向的子目录下额外打包可执行的辅助
scripts/templates；指令 markdown 仍是主要的、部署的、被验证的制品。无向量、无纯代码技能。

#### 技能表示

**技能编码方式**
技能文档 (.md / SKILL.md) + 多文件技能包。规范的 Claude Code 技能契约：YAML
frontmatter（`name`、`description`、`metadata.provenance`、`origin`）+ markdown 正文。体积较大的 references、API dumps 与复现 recipe
被移入技能的 `references/` 子目录并以一行引用，以保持 `SKILL.md` 正文精简。distiller subagent（位于
`agents/skill-distiller.md`）以祈使/不定式语气的散文加上一个真实代码示例来编码过程化技术。team 共享的技能额外标注 `created_by: team`。

**技能粒度**
策略规则 + 完整技能包，处于 CLASS 级别。每个技能捕获一个可复用的、class 级别的技术（例如
`pyannote-speaker-diarization`、`react-effect-cleanup`、`shadcn-v4-migration`）。明确不是实例特定的：一次性的任务叙事、PR
编号、错误字符串、代号、`fix-X`/`debug-Y` 标签都会被拒绝。比完整 workflow 更细，比原子动作更粗；一个 umbrella 技能可以整合若干更窄的 class 级别技能。

#### SKILL.md_专属维度

**文档形态**
结构化 markdown 文档 = YAML frontmatter + 带标题的正文区段。Frontmatter 字段：`name`（小写连字符，<=64 字符，无首尾/连续连字符，class
级别）、`description`（第三人称情境匹配，目标 <=500 字符，因为它会被注入到每个未来会话的 system prompt 中作为永久 context 开销——validator 在超过 500
时发出警告）、`metadata.provenance`（= `self-improving-skills`）、`origin`（= `distilled`）。正文区段：`# <Title>`、`## When this
applies`（具体触发条件/情境）、`## The technique`（可复用的步骤/pattern/fix，附一个真实代码示例）、`## Gotchas`（边界情况 / 我们踩过的坑 /
需要验证什么）。祈使/不定式语气。正文目标最多约 1,500-2,000 词（~2k-3k tokens）；description 约 125-250 tokens。

**编辑粒度**
有界增删替换（bounded add/delete/replace，通过 `Edit` 工具）被强烈优先于整文档重写或全新生成。distiller 遵循严格的有序决策流程：(1) patch 一个直接相关的现有 SKILL.md（增加一个
gotcha / 修正的步骤 / 示例）；(2) 用一个新子区段 patch 一个更广的 umbrella 技能；(3) 在一个现有技能的 `references/`/`templates/`/`scripts/`
子目录下添加支撑文件并以一行指向它；(4) 仅作为最后手段才创建一个 NEW class 级别技能，且需先检查与 live 和 archived 技能以及已安装 plugin 技能的冲突。单一职责：distiller 永不 push
到远程；`/propose-plugin-improvement` 在一个隔离的 clone 中处理 upstream PR。

**版本与门控**
暂存+备份 + review-gated adopt + 自动回滚。(a) 任何技能编辑前都会取 pre-edit 备份；PostToolUse validator 检查
frontmatter/size/provenance，并对格式错误的 `SKILL.md` 自动回滚。(b) Provenance stamping（`metadata.provenance:
self-improving-skills`）标记 agent 蒸馏的技能，以便 curator 与 session 计数器能找到它们。(c) `/curate-skills` LLM pass 是
plan-FIRST、apply-only-after-approval（人工在环门控）。(d) team 共享是 PR-gated：`/share-skill` 开一个由人工 merge 的 PR；`/sync-team-skills`
展示一个只读 plan 供你确认，然后逐技能事务性 apply。(e) origin-hash 规则：未改动的本地副本自动更新；已定制的副本永不被覆写（一次性 diverged 通知）；已删除/归档的副本永不重装。(f)
`SIS_PLUGIN_PR=1` 作为 upstream plugin PR 的 opt-in 门控。无 git-branch 前沿选择或 Pareto/DAG 版本管理。

**文档来源**
成功轨迹归纳 + session 经验提取。distiller 在一段工作完成之后运行，读取实际 transcript JSONL 的尾部（assistant `message.content[]` 的 tool_use/text
块）以及改动过的文件，让自己立足于真实发生的事情——而非仅凭一份摘要。它捕获从成功工作中蒸馏出的、持久的、可复用的、class 级别技术。明确不是失败轨迹蒸馏：anti-pattern 被列为 'Do NOT
capture'（一次性叙事、依赖环境的 workaround、对工具的负面断言、已显而易见的东西），仅作为负向指引使用，不存储为技能。初始 plugin 代码由人工编写；team 技能通过社区共享（git repo）到达。无离线
benchmark 训练。

**跨载体迁移**
跨任务（class 级别技能按构造即可跨任务复用）+ 跨用户/团队（自 v0.9.0 起经 git repo 进行 team 技能共享并带 origin-hash sync；publish 通过剥离个人风格来泛化技术；receive
是事务性且 conflict-aware 的）+ 跨 agent harness 部分成立（技能 CONTENT 是可移植 markdown，但 PLUGIN 本身是 Claude-Code-specific——它依赖 Claude
Code 的 hooks/subagents/slash-commands/skill-discovery 原语，故 self-improvement LOOP 无法迁移到 Codex/Cursor）。在循环意义上不是跨模型（单一
Claude backbone）；技能文本是 model-agnostic 的。不跨 benchmark（无 benchmark）。

**技能库治理**
灰尘清理（curator loop）+ 库膨胀治理（经可恢复 archive）+ 去重合并（umbrella consolidation）+ 层次化索引（umbrella vs class-level）。具体而言：agent 创建的技能若
30 天未使用（`SIS_STALE_AFTER_DAYS`）被标记为 stale；90 天后（`SIS_ARCHIVE_AFTER_DAYS`）被可恢复地移至
`~/.claude/skills/.archive/`。被反复使用证明有效的技能（`use_count >= 3`）以半速老化（archive 阈值翻倍）——一个简单的 reputation-weighted
生命周期。`/curate-skills` LLM pass 是一个以 Hermes 的 curator prompt 为蓝本的 umbrella-building consolidation：先 plan，仅在批准后 apply（要求
>=8 个已学技能，`SIS_CURATE_MIN_SKILLS`；每 7
天运行一次，`SIS_CURATE_INTERVAL_DAYS`）。支撑命令：`/pin-skill`、`/archive-skill`、`/restore-skill`、`/prune-skills`、`/curator-status`。team
技能（`created_by: team`）永不被个人 curator 触碰——其所有者是 team repo。curation 期间的批量读取从不重置技能的空闲时钟。

**失败记忆**
部分 / 软性。没有一个作为独立制品的 dedicated rejected-edit buffer 或 failure-signature store。负向知识被编码为 distiller prompt 内一个显式的 'Do NOT
capture' anti-pattern 列表（一次性叙事、依赖环境的失败、对工具的负面断言、已显而易见的东西、纯用户主导的功能开发）——这引导 generator 远离垃圾内容。编辑期的负向 FEEDBACK 来自
PostToolUse validator，它拒绝并回滚格式错误的编辑（frontmatter/size/provenance 违规），并发出非阻塞的质量建议（例如过长的 description）。一个被 decline 的
distillation nudge 保持 declined，仅在又一次达到 NEW work 阈值后才重新触发，避免反复在不当时机打扰。无正式的 anti-pattern 技能文件或 failure-attribution 记忆。

**编辑安全**
详尽且一等公民。(1) 范围边界：编辑被限制在 `SKILL.md` 与 `~/.claude/skills/` 下的支撑文件；单一职责——distiller 永不 push 到远程。(2) Pre-edit 备份 + 对格式错误的
`SKILL.md` 自动回滚（PostToolUse validator 强制执行 Claude Code 技能契约：frontmatter schema、name 格式、description 长度、provenance）。(3)
Provenance stamping 使 agent 蒸馏的技能可追踪。(4) Anti-injection / anti-secret：技能是 'instructions to an agent' = 一个
prompt-injection 向量，因此每次 team 内容写入（首次安装及后续更新）都通过一个静态扫描器检查 secrets、破坏性命令、injection 标记、symlinks、隐藏文件与大小上限；被拦截的内容被
QUARANTINED，绝不放入 `~/.claude/skills`。(5) 人工在环 / review-gated：team 共享按设计是 PR-gated（由人工 merge）；curator 是
plan-first/apply-after-approval；`/share-skill` 在开 PR 前展示 diff。作者指出人工 review 门控就是安全边界——实时共享技能商店被有意拒绝，因为那样会让一个被攻陷的 session
向每个队友的 agent 注入指令。(6) Personalization-always-wins，通过 origin-hash sync 实现（已定制副本永不被覆写）。(7) Fail-safe hooks：任何 hook
错误都会批准原始动作，而非中断 Claude Code 会话。(8) 有界编辑（优先 patch 而非 create）限制破坏性重写。

**协同进化**
skill-skill 生态 + skill-prompt 联合 + generator-verifier 协同。(a) skill-skill：umbrella 技能整合更窄的 class
级别技能（`/curate-skills`）；一个技能指向其他技能的 reference 文件；技能库自组织为一个层次结构。(b) skill-prompt 联合：每个已学技能的 `description` 被注入到每个未来会话的
system prompt，因此技能文档与 agent 的 prompt 协同进化（description 长度是永久 context 开销，故有 <=500 字符目标）。(c)
generator-verifier：`skill-distiller` subagent（generator）产出编辑，PostToolUse validator（verifier）以回滚来门控它们——一个轻量的对抗性检查。不是
skill-tool 协同进化（Claude Code 的 tools/hooks/subagents 是固定原语，不进化）。

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration + rollout_optimization（非梯度、文本空间编辑），带有 LLM-as-implicit-judge 风味。distiller 从一条成功轨迹进行 in-context
learning（读取 transcript 尾部 + 改动文件），并向 `SKILL.md` 发出有界的文本编辑。无梯度更新、无 RL、无数值 reward、无 population/evolutionary
搜索。学习信号是定性的：'这个会话是否产生了一个可复用的、class 级别的技术？'。以 Nous Research Hermes Agent 的 procedural-memory + curator loop 为蓝本，移植进
Claude Code 的 hook/subagent/skill 原语。

**学习信号来源**
成败轨迹（成功的工作会话——蒸馏出有效的部分）+ 自我反思（distiller 自身对该技术是否可复用、是 class 级别还是一次性的判断）+ 工具成功率指标，用作 COMPLEXITY DETECTOR（自上次 distillation
起，tool-call 数 >= `SIS_DISTILL_THRESHOLD`=12 且 file-edit 数 >= `SIS_MIN_FILE_EDITS`=2 时触发 nudge）。此外，usage
telemetry（`~/.claude/self-improve/skill_usage.json` 中的 use/view/patch 计数）驱动 curator 的老化/声誉信号——patch 计数在 PostToolUse hook
中运行，以便捕获 background-subagent 的编辑。无环境 reward、无 held-out validation 分数、无 LLM-as-judge 打分循环。

**奖励粒度**
outcome。信号按每段工作 / 每会话的 outcome 评估（这段已完成的工作是否产生了一个可复用的技术）。Stop hook 每段工作触发一次 nudge，而非每次 tool call。

**学习范式**
inter-test-time、online stream、on-policy。Distillation 发生在会话之间（在会话结束时经 Stop hook，或按需经 `/distill-skill`），而非
intra-test-time（除了一次性的 end-of-segment 块 nudge 外，它不在任务中途打断）。它是 sleep-time 式的（一个 background subagent 在工作完成后运行），但作者明确指出
Claude Code 缺少 Hermes 那种免费 background daemon，因此 distillation 使用一个 VISIBLE/BILLABLE 的 subagent turn，而非免费的离线 replay
线程。On-policy（执行工作的同一个 Claude backbone 对其进行反思）。

#### 进化时机_When

**进化时机 (When)**
主要是 inter-test-time。Stop hook 在会话/段结束时评估复杂度；curator 周期性运行（当 learned-skill 数 >= `SIS_CURATE_MIN_SKILLS`=8
时，`SIS_CURATE_INTERVAL_DAYS`=7）；team-sync 提醒在 SessionStart
触发（每天一次，无网络）。手动命令（`/distill-skill`、`/curate-skills`、`/share-skill`、`/sync-team-skills` 等）允许任何时候按需进化。非 intra-test-time。

**触发方式**
事件触发（复杂度阈值满足时经 Stop hook 在会话/段结束时）+ 使用驱动（usage telemetry 驱动 stale/archive 生命周期：30d stale、90d archive、use_count>=3 半速老化）+
周期性（每 7 天自动 curator）+ 手动命令触发。nudge 是每段工作一次：一个 DECLINED 的 nudge 保持 declined，仅在又一次达到 NEW work 阈值后才重新触发（自上次 distillation
起新的 tool calls + file edits 累积），这避免了唠叨，并阻止纯研究性 chat 触发（要求 >=2 次 file edits）。

#### 存储与检索

**技能库结构**
技能文件目录（扁平用户目录 `~/.claude/skills/<name>/SKILL.md`）+ 层次化（`.archive/` 子目录用于可恢复归档的技能；umbrella 技能与 class 级别技能并列并整合后者）+ 用于
team 共享的 git repo（私有 team repo，带一个 `skills` 子目录，经 `~/.claude/self-improve/team_config.json`
配置）。支撑状态文件：`~/.claude/self-improve/skill_usage.json`（telemetry）、team_config.json、每个技能的 origin-hash 记录。不是 vector DB、不是
graph/DAG、不是 cloud registry——一个普通文件系统树加可选 git remote。

**检索/复用方式**
description 匹配触发加载（Claude Code 的 NATIVE skill discovery：每个技能的 `description` 被注入会话 system prompt，当 description
匹配用户情境时该技能被加载——这就是为何 description 质量与长度被强制约束的原因）。distiller 自身使用 Glob `~/.claude/skills/**/SKILL.md` + name/description
匹配来寻找待 patch 的候选技能，并用 `ls ~/.claude/skills/`（+ `.archive/`）做冲突检测。无 embedding/BM25 向量检索；无 generation-as-retrieval。下一次会话通过
Claude Code 内置机制'正常地'重新发现技能。

#### 验证与反馈

**验证方式**
validation 门控 + 功能正确性检查 + LLM-judge（自身）。PostToolUse validator 强制执行 Claude Code `SKILL.md` 契约：frontmatter schema（name
格式：小写连字符、<=64 字符、无首尾/连续连字符；description 存在；`metadata.provenance`）、大小限制（description <=500 字符建议、正文 ~1500-2000 词目标）以及
provenance stamping；格式错误的编辑触发从 pre-edit 备份的自动回滚。非阻塞的质量建议对过长 description（永久 context 开销）发出警告。distiller
在写入前自我评估（LLM-judge）该技术是否可复用且 class 级别。对于 team 共享，一个静态扫描器在每次 team 写入时验证
secrets/destructive-commands/injection-markers/symlinks/hidden-files/size。无基于执行的 benchmark validation、无 held-out 评估、无
multi-model debate——作者明确表示没有正式评估。

**错误纠正**
回滚（对格式错误的 SKILL.md 从 pre-edit 备份自动回滚）+ 有界编辑（强烈优先于整文档重写的有界编辑）+ 定向 diff 修补（定向 `Edit` 调用，为现有技能增加
gotcha/step/example）。validator 标记问题，distiller 修正它们。Fail-safe hooks 在任何 hook 错误时批准原始动作，因此一个损坏的 hook 永不阻塞用户的 Claude Code
会话。curator 有意保持保守（仅归档 agent 创建的技能、保留可恢复备份、从不触碰 team 技能）。

#### 环境与基座

**测试环境**
真实生产力任务（野外的真实 Claude Code coding/agent 会话）。无 benchmark 环境。该 plugin 自带 pytest 套件（`tests/`，经 `uv run --with pytest --
pytest tests/` 运行），覆盖 hooks/scripts/validator/team-sync/scanner，但对所学技能本身没有 SkillsBench/GDPVal 风格的任务 benchmark。

**底座模型**
Claude（Claude Code）。distiller subagent 使用 `model: inherit`（执行工作的同一个 Claude backbone）。Optimizer/target 不分离——单一 Claude 模型既执行任务又对其反思/蒸馏。无 VLM、无文档化的开源 LLM 变体。

**部署域 (Where)**
specialized（Claude Code coding/agent 生产力）。该 plugin 按构造即是 Claude-Code-specific（它接入 Claude Code 的 hooks、subagents、slash
commands 与原生 skill-discovery 机制）。仅在适用于任何 Claude Code workflow、而非单一编程语言或领域的意义上是 general 的。

#### 评估指标

**评估指标**
skill_library_growth + usage telemetry（`~/.claude/self-improve/skill_usage.json` 中的 use_count / view_count /
patch_count）+ 隐式回归率（validator 对格式错误编辑的回滚率）。Stale/archive 生命周期计数（30d/90d）作为 library-health 信号。无 success_rate、无
generalization benchmark、无 sample-efficiency 或 economic-value 数字——作者明确列出 'Honest limitations'
且未提供任何定量评估。成本在定性上被承认：distillation 消耗一个 visible/billable 的 subagent turn，因为 Claude Code 没有免费 background daemon（不同于
Hermes）。

#### 局限与挑战

**局限与挑战**
明确声明的 'Honest limitations' 加上隐含的限制。(1) 可扩展性/成本：Claude Code 不提供免费 background daemon 线程，因此 distillation 使用一个
visible/billable 的 subagent turn（不像 Hermes 那样是免费 sleep-time replay）。(2) 范围：仅处理过程记忆（SKILL.md），不处理事实记忆——必须由 Claude Code
的原生 memory 或独立 memory plugin 补充。(3) 可控性/回归风险：curator 有意保守（仅归档 agent 创建的技能、保留可恢复备份），但没有 held-out 回归 benchmark，因此一个糟糕的
agent 蒸馏技能可能持续存在，直到 30/90 天生命周期将其捕获。(4) 安全/可迁移性：team sync 按设计是 PR-gated——实时共享技能商店被有意拒绝，因为技能是 prompt-injection 向量，一个被攻陷的
session 可能向每个队友的 agent 注入指令；人工 review 门控就是安全边界。(5) 可迁移性：该 plugin 是 Claude-Code-specific（使用 Claude Code 的
hooks/subagents/skill-discovery）；只有技能 CONTENT 可移植。(6) optimizer_quality：distiller 对 'reusable class-level technique'
的判断是质量瓶颈——naive 的自动记录会产生垃圾，由 anti-pattern 'Do NOT capture' 列表与 class 级别命名强制来缓解（未解决）。(7) doc_bloat：由 description <=500
字符建议 + 正文 1500-2000 词上限 + references/ 子目录缓解，但未正式度量。

#### 可借鉴要点

**可借鉴要点**
- 1. 在一个专用 subagent 内编码一个严格的、有序的 distiller 决策流程：(1) patch 一个直接相关的现有 SKILL.md，(2) patch 一个更广的 umbrella 技能，(3) 在一个现有技能下添加支撑性的 reference/template/script 文件，(4) 仅作为最后手段才创建一个 NEW class 级别技能——配合一个显式的 'Do NOT capture' anti-pattern 列表（一次性叙事、依赖环境的 workaround、对工具的负面断言、已显而易见的东西）与 class 级别命名强制（拒绝实例特定的名字，如 PR 编号或 fix-X 标签）。这种有序偏好 + 负向指引是抵御困扰 naive 自动记录的技能库膨胀与垃圾累积的最重要防线，并使循环默认做加法（additive-by-default）而非默认做乘法（multiply-by-default）。
- 2. 把 EDIT SAFETY 当作一等工程关切，而非事后补救：取 pre-edit 备份、运行一个强制执行 SKILL.md 契约（frontmatter schema / name 格式 / description 长度 / provenance stamp）并自动回滚格式错误编辑的 PostToolUse validator、为每个 agent 蒸馏的技能盖上 `metadata.provenance` 以便追踪，并且——对任何 team 共享路径——在每次写入前放置一个人工 review 门控（PR-gated）外加一个带隔离的静态 injection/secret/symlink 扫描器。origin-hash 规则（未改动的自动更新；已定制的永不被覆写；已删除的永不重装）使 'personalization always wins' 成为按构造成立的性质。把技能当作它本就是的 prompt-injection 向量来对待：review 门控就是安全边界。
- 3. 增加一个带 usage 驱动老化与 umbrella consolidation 的 CURATOR LOOP，以防技能库无界增长：未使用的 agent 创建技能 30d 后变 stale、90d 后被可恢复地归档，但 PROVEN 技能（use_count >= 3）以半速老化——一个廉价、reputation-weighted 的 'Lotka-Volterra-lite' 生命周期，在自动修剪其余技能的同时保留有用技能，无需任何学到的 reward model。将其与一个 LLM `/curate-skills` pass 配对，后者构建 umbrella 技能以把更窄的技能折叠进一个自组织层次结构，以 plan-first / apply-after-approval（人工在环）方式运行，并以最低库大小为门控，使其仅在值得整合时才触发。

#### 不确定字段

- paper_link（无学术论文；这是一个开源 Claude Code plugin）
- key_results（未发布定量 benchmark/evaluation；仅有已实现循环的定性描述与 GitHub 采用计数）
- release_date（repo 创建于 2026-06-09；README 提及之外，确切的 first-version tag 与 v0.9.0 日期未确认）
- reward_granularity / learning_paradigm 标签是解释性的（该项目不以 ML 训练术语自述；标签是通过将其行为映射到 survey taxonomy 上来赋予的）

---

### claude-evolving-skills (reflect-and-learn)

> `engineering_practice` · PalmDr, 2026。让 Claude Code 自我改进：automated scouting + 多模型辩论(Claude+Gemini+ Codex)+reflection。reflect-and-learn 是核心自改进循环：复盘过往 session→双通道打分→ 多模型辩论→memory consolidation→experience stripping→tool co-evolu

#### 基础信息

**名称**
claude-evolving-skills (reflect-and-learn)

**发布时间**
2026-03（LinkedIn 文章《I Stopped Chasing Viral Agentic Workflow Repos》发表于 2026-03-21；GitHub 仓库单 commit，截至 2026 年中 6 stars）

**代码链接**
https://github.com/PalmDr/claude-evolving-skills

**类型**
blog_practice

#### 进化对象_What

**进化对象 (What)**
Context 记忆与提示（主要）：CLAUDE.md 规则、~/.claude 记忆条目和技能 SKILL.md 文件是进化目标。Tools 技能是次要的协同进化面（Agent 6 将临时 ad-hoc 脚本提升为持久化技能，并提议新的 MCP server）。模型权重和 agent 架构不被进化。

**技能是否独立制品**
是 — 技能以独立可复用制品的形式存在。形式：~/.claude/skills/ 下每个技能文件夹一个 SKILL.md 文件（如
reflect-and-learn/SKILL.md、agentic-radar/SKILL.md、vendor-docs-radar/SKILL.md、gemini-agent/SKILL.md、codex-agent/SKILL.md）。辅助制品：scripts/
中的 bash 包装脚本、JSONL 血脉文件（evolution-tree.jsonl、scoreboard.jsonl）、REGISTRY.md 工具注册表。

**是否文档载体**
混合 — 核心载体是人类可读的 Markdown 指令文档（SKILL.md），但其中内嵌可执行的 bash/代码块（jq 会话解析、git commit、launchd plist）和 YAML frontmatter。AGENTS.md
明确将该仓库定位为「既适合人类也适合 agent 消费的结构」（Karpathy Software 3.0 理念）。

#### 技能表示

**技能编码方式**
技能文档（.md/SKILL.md），带 YAML frontmatter（name + description 含触发短语）+ 由分步执行指令构成的 Markdown 正文。记忆编码为
JSONL（evolution-tree.jsonl、scoreboard.jsonl）和 Markdown（reflections/*.md、CLAUDE.md、CHANGELOG.md）。无向量嵌入，无图数据库。

**技能粒度**
完整技能包 / 子任务 workflow — 每个技能是一个完整的多步 workflow（reflect-and-learn 有 6 个步骤，启动 6 个并行分析 agent + 综合汇总 + 辩论 + 采纳 + 整合）。存在子技能粒度（6
个分析 agent 中的每一个都是一个有界子任务）。无原子动作或纯 insight 粒度。

#### SKILL.md_专属维度

**文档形态**
结构化字段：YAML frontmatter（name、description 含触发关键词）+ 带 H2/H3 小节的 Markdown 正文（When to Use、Output、Execution Instructions Step
0-6、Rubric Reference、SOTA References）。内嵌 fenced bash/json/jsonl/markdown 代码块。reflect-and-learn 的 SKILL.md 较大（约 500+ 行，接近
AGENTS.md 规定的 600 行上限）。其他技能（gemini-agent、codex-agent）是简短的委派 stub。

**编辑粒度**
在 CLAUDE.md 规则和记忆条目上的有界 add/delete/replace；定向 diff（每条提议的修改是一个带理由的特定 CLAUDE.md/技能编辑）；experience stripping =
有界删除（规则必要性测试标记 STRIP_CANDIDATE 但绝不自动移除 — 始终标记为 HIGH-IMPACT 交由用户）。按自进化协议，方法论变更「append, not overwrite」。非整文档重写。

**版本与门控**
分层：(1) 评审门控采纳 — P0-AUTO（>=8.0，3/3 声音一致，Safety>=8）和 P1-AUTO（>=7.0，2/3 声音）自动应用；HIGH-IMPACT（Safety<7 或声音分歧）标记交由用户；DEFER
仅记录；ROLLBACK 用于 CONFIRMED_HARMFUL。(2) 通过每个反思周期后的 git commit 做暂存+备份。(3) DAG/树状血脉版本控制（evolution-tree.jsonl 以
parent_id→node_id 记录），支持 AFlow 式回溯。(4) 回顾性门控 — 过去的采纳被重新评分 CONFIRMED_HELPFUL/INCONCLUSIVE/CONFIRMED_HARMFUL。

**文档来源**
session 经验提取（通过 jq 抽取过去一周的对话 JSONL）+ 失败轨迹蒸馏（Agent 1 用 text gradient 做失败分析）+ 成功轨迹归纳（用户满意度检测器抽取反复出现的赞扬模式）+
社区共享（agentic-radar/vendor-docs-radar 扫描 GitHub/HN/Reddit/厂商博客以获取外部模式）。非 LLM 一次性生成，非 benchmark 训练。

**跨载体迁移**
跨模型（多模型辩论：Claude + Gemini + Codex 评估每条提议 — 显式的跨模型验证）。跨任务（分析所有 session 类型：coding、debugging、research、config）。跨 agent
harness：否 — Claude Code 专用（SKILL.md 格式、~/.claude/ 布局）；Gemini/Codex 是辩手而非目标。跨用户/团队：否 — 设计上即单用户个人 workflow（README「adapted
to my workflow」）。跨基准：否。

**技能库治理**
通过 experience stripping 治理 doc_bloat（AgentEvolver 启发的规则必要性测试：4 周以上未使用的规则 → STRIP_CANDIDATE）+ 记忆整合（剪枝 4
周以上未被引用的记忆、合并冗余条目、提升反复出现的模式）。无显式的 Lotka-Volterra/retirement，无基于相似度的技能去重/合并，无分层索引 — 技能是扁平目录。工具注册表（REGISTRY.md）有采纳日志追踪。

**失败记忆**
是 — 专用的 Agent 1（Failure Analyst + Text Gradient Generator）抽取失败模式，附带频率、根因和 text gradient（「output was wrong BECAUSE tool X
BECAUSE rule Y BECAUSE context W which no longer applies」）。具体的错误日志（input/expected/actual/error）输入给
optimizer。Retrospective Evaluator（Agent 4）将过去的 CONFIRMED_HARMFUL 变更标记为待回滚。DEFERRED 提议记录在 scoreboard.jsonl
中作为负反馈，以避免重复失败方向。树的 failure_branches 字段记录退化路径。

**编辑安全**
多层：(1) scope 边界 — 仅操作 ~/.claude/ 配置文件，从不触碰用户源代码；(2) 编辑前备份+回滚 — 每个周期后 git commit，ROLLBACK 分类回滚 CONFIRMED_HARMFUL 变更；(3)
确认门控/人工在环 — HIGH-IMPACT 项需用户评审；(4) CLAUDE.md 自进化协议中的有界编辑策略：「Never remove an existing rule without user confirmation;
Never change execution style without user confirmation; Methodology changes append, not overwrite」；(5) experience
stripping 绝不自动移除规则（始终标记 HIGH-IMPACT）；(6) 多模型辩论作为共识门控（自动采纳需 2/3 一致）。未记录显式的 eval-hacking 或密钥注入检查。

**协同进化**
丰富的多轴：skill-tool（Agent 6 检测重复的 ad-hoc 命令模式并将临时脚本提升为持久化技能；提议新的 MCP server — Live-SWE-agent 的临时→持久化流水线）+ skill-skill
生态（reflect-and-learn 调用 gemini-agent 和 codex-agent 技能；技能形成闭环：scan→propose→debate→adopt→verify）+ generator-verifier
协同（Claude 生成提议，Gemini+Codex 通过辩论验证）+ skill-prompt 联合（CLAUDE.md 提示与 SKILL.md 技能文件均被联合编辑）。非 skill-only。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（通过对 config 施加 TextGrad 式 text gradient 的非梯度文本空间优化）+ co_evolutionary（skill↔tool↔verifier 协同进化）+
population_evolutionary 元素（AFlow 启发的软混合选择：40% 均匀探索 + 60% 对提议 softmax 加权利用；树状血脉）。非 reward-based RL、非模仿、非梯度/SFT。基于辩论的
verifier 取代标量奖励。

**学习信号来源**
自我反思（6 个并行 reflection agent 作用于 session 日志）+ 成败轨迹（失败模式、用户纠正、被放弃的任务）+ LLM-as-judge（多模型辩论：Claude/Gemini/Codex 对
impact+risk 打分）+ 工具成功率指标（efficiency auditor：工具调用次数、token 用量、完成耗时）+ 留出验证分（retrospective evaluator 对照后续 session
数据对过去的采纳重新打分）。

**奖励粒度**
hybrid — 显式双通道打分（AgentEvolver 启发）：通道 1 PROCESS QUALITY（Evidence 3x + Generality 2x + Simplicity 1x）+ 通道 2 OUTCOME
QUALITY（Impact 3x + Safety 2x + Text Gradient Strength 1x）。Composite = 0.5*Process + 0.5*Outcome。process 与 outcome 均被奖励。

**学习范式**
sleep-time（每周三凌晨 3:00 经由 cron/launchd 的离线反思，重放过去一周的 session JSONL）+ 离线（分析历史日志，非实时）+ on-policy-ish（反思同一 agent 自己的 session）。非在线/intra-task。

#### 进化时机_When

**进化时机 (When)**
sleep-time（主要：每周三凌晨 3am 定期调度）+ inter-test-time（手动触发：用户说「reflect」/「self-improve」/「review workflows」/「evolve
config」，或在一次糟糕的 session 之后）。非 intra-test-time（不在任务执行期间修改 config）。

**触发方式**
周期性（cron/launchd 每周调度：周一=agentic-radar、周三=reflect-and-learn、周五=vendor-docs-radar）+ 事件触发（slash command 或 YAML description
中的自然语言触发短语）+ 失败触发（作者注「after a particularly rough session where multiple things went wrong」）+ 使用驱动（session JSONL 的 mtime
触发分析）。

#### 存储与检索

**技能库结构**
技能文件目录（~/.claude/skills/<name>/SKILL.md，每个技能一个文件夹的扁平结构）+ git history（每个周期后的 commit）+
DAG/树状血脉（evolution-history/evolution-tree.jsonl 以 parent_id→node_id 记录血脉 + success_branches/failure_branches +
scoreboard.jsonl 每次变更日志）。反思以带日期的 Markdown 存储于 reflections/YYYY-MM-DD-reflection.md。无向量 DB，无云端注册表。

**检索/复用方式**
description 匹配触发加载 — YAML frontmatter 的 'description' 字段枚举触发短语（「reflect」「self-improve」「review my workflows」「run
reflection」「evolve config」，或每周 cron）；Claude Code 将用户输入/调度与这些短语匹配以激活技能。技能按名称调用其他技能（reflect-and-learn 调用
gemini-agent/codex-agent）。无语义/向量检索，无 BM25。

#### 验证与反馈

**验证方式**
LLM-judge（多模型辩论：Claude+Gemini+Codex 独立对 impact+risk 打分 1-10）+ 验证门控（P0/P1/HIGH-IMPACT/DEFER/ROLLBACK 阈值）+ 多模型辩论（自动采纳需 2/3
共识；分歧 → 标记交由用户）+ 留出评估/longitudinal（Retrospective Evaluator 对照后续 2-4 周的 session
数据对过去的采纳重新打分：CONFIRMED_HELPFUL/INCONCLUSIVE/CONFIRMED_HARMFUL）。非基于 benchmark 的执行验证 — 作者明确指出没有受控 A/B 结果。

**错误纠正**
回滚（ROLLBACK 分类经由 git 回滚 CONFIRMED_HARMFUL 变更）+ 有界编辑（方法论采用 append-not-overwrite，绝不自动移除规则）+ 定向 diff 修补（每条采纳的变更是一个带理由的特定定向
CLAUDE.md/技能 diff）+ self-revision（meta-evolution Agent 5 对反思流程本身提出修改 — mutator 的 hyper-evolution）+ 重规划（text gradient
由根因生成逆向编辑）。

#### 环境与基座

**测试环境**
真实生产力任务 — 作者自己的 Claude Code session（coding、debugging、research、config、refactoring）。非受控 benchmark；作者明确：「I don't have
controlled A/B results yet」以及「Whether the reflection loop genuinely compounds over months, or just feels like it does,
is something I'm still figuring out.」。无 SkillsBench/GDPVal/SWE-bench 评估。

**底座模型**
Claude（主 optimizer 且主 target：reflect-and-learn 运行于 Claude Code，进化 Claude 自己的 CLAUDE.md）+ Gemini（经由 gemini-agent 技能的
debater/verifier，Gemini CLI）+ Codex（经由 codex-agent 技能的 debater/verifier，Codex CLI）。Optimizer/target 名义上是同一模型（Claude），但由
Gemini+Codex 外部交叉校验。需要 GEMINI_API_KEY 和 OPENAI_API_KEY。

**部署域 (Where)**
specialized（coding）— Claude Code 是 coding agent；技能作用于 ~/.claude/ 配置以服务 coding workflow。在 coding 范围内，它是
general-purpose（覆盖代码生成、debugging、research、refactoring）。未部署到 GUI/office/document/Web 领域。

#### 评估指标

**评估指标**
成功率（session success_rate 记录于 evolution-tree.jsonl 的 metrics 中）+ skill_library_growth（采纳 vs 延迟的变更计数）+ cost（每周多模型辩论约
$5-10/月 API；侦察主要用免费层网络搜索）+ 回归率（回顾性裁决：CONFIRMED_HELPFUL/INCONCLUSIVE/CONFIRMED_HARMFUL 比例）+ efficiency
deltas（avg_tool_calls、avg_tokens、user_corrections/confirmations 按周追踪）。无 sample_efficiency 或 economic-value-capture 指标。

#### 局限与挑战

**局限与挑战**
regression_risk（已承认；由 git 追踪 + 回滚缓解，但作者承认增益是否能复利累积仍不确定）+ eval-hacking 风险（无 ground truth 的自评估；多模型辩论缓解但不消除）+
transferability（Claude Code + ~/.claude 布局专用；不重建则无法迁移到 Cursor/Codex harness）+ doc_bloat（通过 experience stripping
应对，但作者指出记忆整合「has needed the most manual iteration」）+ controllability（开放式个人 workflow =「honest measurement is harder」）+
optimizer_quality（严重依赖 session-log 质量、jq 解析和 LLM 辩论质量；Gemini/Codex 可选 — 缺失则失去多声音辩论）+ scalability（单用户/单 agent 范围；作者注「the
next conceptual step is shared memory and coordination across agents」尚未构建）。

#### 可借鉴要点

**可借鉴要点**
- 多声音辩论作为廉价、模型无关的质量门控：让 Claude（generator）、Gemini 和 Codex（verifier）独立对每条提议的 config 编辑在 impact+risk 上打分；仅在 2/3 共识时自动采纳，分歧则标记交由人工评审。这用分歧信号取代了标量奖励，能浮现出 generator 本会自我批准的危险编辑 — 无需训练即可直接移植到任何 SKILL.md 自编辑循环。
- 树状进化历史（AFlow 式 JSONL：node_id + parent_id + 每次变更打分 + 回顾性裁决 + success/failure 分支）是使智能回溯成为可能（而非随机游走）的关键。将其与每周的 Retrospective Evaluator 配对 — 后者对照后续 session 数据对过去的采纳重新打分（CONFIRMED_HELPFUL/HARMFUL）— 这把闭环从「propose→adopt」推进到「propose→adopt→verify→rollback」，是抵御 config drift 的最重要单一防线。
- 双通道打分（process quality + outcome quality，各自加权：Evidence/Impact 3x、Generality/Safety 2x、Simplicity/Text-Gradient 1x）结合 experience stripping（4 周以上未使用的规则成为 STRIP_CANDIDATE，但绝不自动移除 — 始终标记 HIGH-IMPACT）是预防文档膨胀同时保持 SKILL.md/CLAUDE.md 精简的实用配方。「append, never overwrite; never remove a rule without user confirmation」协议是软打分之下的硬安全底线。
- sleep-time 调度（cron/launchd、每周、离线重放 session JSONL）将自我改进与任务执行解耦 — agent 在用户睡眠时进化其 config，约 $5-10/月 API 成本，对 workflow 零干扰。这使得自我进化对个人开发者也经济可行，而不仅限于实验室。

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
2026（v0.5.0 首次发布 2026 年 3 月；v0.6.3 evolution tiers 2026 年 3 月；v0.11.0 跨平台 2026 年 4 月；v0.12.0 subscription profiles 2026 年 6 月；最新 v0.12.1 2026 年 6 月）

**代码链接**
https://github.com/JavanC/Homunculus（npm: https://www.npmjs.com/package/homunculus-code；通过 `npx homunculus-code init`
安装）。关键内部文件：docs/nightly-agent.md、commands/evolve.md、commands/improve-skill.md、skills/{claude,cursor,codex,generic}/、examples/reference/。

**类型**
industry (open-source self-evolution framework/plugin) + blog_practice (validated on the author's own personal AI assistant over 5 weeks). Not academic.

#### 进化对象_What

**进化对象 (What)**
Context 记忆与提示 + Tools 技能 + Architecture（单/多智能体）。进化：行为性 instincts、技能（带 eval spec 的 .md）、子 agent、hooks、路径作用域 rules、自动化
scripts、MCP 接线、cron/launchd jobs、slash 命令，以及目标树（architecture.yaml）+ CLAUDE.md/AGENTS.md/memory。不含模型权重——仅是既有 coding
agent（Claude Code / Cursor / Codex CLI）的外部运行时文本/工具状态。Meta-evolution：进化机制本身也被调优。

**技能是否独立制品**
是——技能是独立、可复用、带版本的 markdown 制品：`homunculus/evolved/skills/*.md`（兼容 agentskills.io），每个都配一份 `homunculus/evolved/evals/` 中的
eval spec。另有独立制品用于
instincts（`homunculus/instincts/personal|archived/`）、agents（`homunculus/evolved/agents/`）、rules（`.claude/rules/*.md`）、commands（`.claude/commands/*.md`）与
scripts（`homunculus/scripts/`）。形态：.md 文件 + YAML 目标树 + shell/JS scripts。

**是否文档载体**
是（混合，偏向是）。一个「技能」的核心载体是带 YAML frontmatter 的可读指令 markdown 文档；instincts/rules/commands 也是 markdown。技能额外内嵌结构化字段（frontmatter）并引用外部可执行 eval spec。非纯代码，也非纯向量。

#### 技能表示

**技能编码方式**
技能文档（.md / SKILL.md 风格）。兼容 agentskills.io 的 markdown = YAML
frontmatter（name、description、allowed-tools、compatibility、metadata.author/version）+ markdown
正文（Purpose/Steps/...）。instincts 编码为 frontmatter
标记的文件（confidence_score、suggested_mechanism、goal_path、durability_score、supersedes）。目标树编码为
`architecture.yaml`（purpose/realized_by/health_check/metrics）。非向量；file-system + git。

**技能粒度**
跨栈混合粒度：原子模式（instincts，~单个行为）→ 策略规则（路径作用域 rules）→ insights（memory/research 建议）→ 完整技能包（skill .md + eval spec，一个
workflow）。同一行为随成熟度迁移粒度（instinct → rule → skill → hook）。

#### SKILL.md_专属维度

**文档形态**
结构化字段：YAML frontmatter + markdown 指令正文。标准 evolved-skill 模板：`--- name/description/allowed-tools/metadata(version,author)
---` + `# Skill: <Name>` + Version / Evolved-from / Purpose / Steps / ...。多文件包：一个技能 + 其 eval spec（+ 可选 agent）。evolved
技能典型长度 ~1–2k tokens（例如 `homunculus.md` 路由技能约 ~80 行；参考技能增长到数百行）。平台特定副本位于 skills/{claude,cursor,codex,generic}/。

**编辑粒度**
有界 add/delete/replace（非整文档重写）。`/improve-skill` 分析 FAIL/PARTIAL/GAP 场景后做定向编辑：修正错误信息 / 增补缺失 rules / 增加新章节；每轮 version
+0.1；最多 5 轮。`/evolve` 在把一个 instinct 路由到新机制时写入全新的小文件。Git 跟踪每一个中间版本。Eval spec 从不被编辑（测试保持固定）；仅技能文件被编辑。

**版本与门控**
多层：(1) 验证门控——eval→improve 循环直到 100% 通过，含 5pp 噪声容忍、回归 rollback，以及 Gaming Gate（分数跳变 >5pp 且净新增行 ≤3 = gaming_suspected →
revert）；(2) 多次运行 eval `--runs/--passes N` 配多数投票以压制 LLM-judge 方差；(3) git 版本控制 + frontmatter 中每次编辑 bump version；(4)
Durability Gate（durability_score < 0.7 的 instincts 被过滤）；(5) staging——非侵入式建议写入 `homunculus/reports/` 与定制化命令的 `.new`
文件；(6) 升级时 `.bak` 备份；(7) review-gated adopt——核心行为变更（hooks/rules/CLAUDE.md/文件删除/cron/deps）不被自动应用，仅作为 Suggested 行为提议。

**文档来源**
session 经验提取（SessionEnd/PostToolUse observation hooks 记录工具使用 → `evaluate-session.js` 一遍提取 instincts/memory/research）+
成功轨迹归纳（被强化的重复模式收敛为技能）+ 社区共享/外部研究（nightly P2 扫描技术新闻/changelog/社区，跨夜去重）。Write Gate 要求一次提取必须「改变未来行为 / 捕获一项承诺 / 保留一个决策依据」。

**跨载体迁移**
cross-agent-harness（显式一等公民：Claude Code ↔ Cursor ↔ Codex CLI；`init` 自动探测宿主并由 `skills/{claude,cursor,codex,generic}/`
提供正确格式）+ cross-model（多 LLM harvest provider：claude-cli / codex-cli / anthropic-api / openai-api，含
Ollama/vLLM/OpenRouter）+ cross-user（`instincts/personal/` 下的 instincts，按用户隔离）。经目标树路由实现 cross-task。声称 cross-platform
但未公开定量迁移指标。

**技能库治理**
层次化索引（skills/agents/evals/instincts{personal,archived}/reports 目录 + architecture.yaml 目标树）+ 去重合并（语义 `supersedes` 自动归档更旧的
instincts；2+ 相似 instincts → 技能聚合）+ 灰尘清理 / curator loop（`prune-instincts.js`：reference-frequency 评分 +25 used/−15 never
used、3 级 skill-coverage 检测、confidence 衰减前 14 天宽限、at-risk 警告；archive-once-implemented）+ retirement（archived/ 目录；CLAUDE.md
覆盖检查避免重复提取已实现的 rules）。

**失败记忆**
部分。失败信号被用作负反馈：(1) Bash failure circuit breaker——`observe.sh` 跟踪最近 10 次失败供 evolution 分析；(2) improve-skill
回归检测标记此前通过、现在失败的场景并 rollback；(3) Gaming Gate 丢弃可疑的 'gaming_suspected' 改进；(4) cross-night research
去重避免重复提议已见过的主题。但没有文档化的专用 anti-pattern / failure-signature+remedy 存储（更接近 rejected-edit buffer 模式）。

**编辑安全**
分层：(1) 范围边界——`/improve-skill` 仅编辑技能文件，绝不编辑 eval spec，绝不触碰应用源码；(2) 编辑前备份 + rollback——升级时 `.bak`，回归时 rollback 到前一版本；(3)
anti-eval-hacking——Gaming Gate + 多次运行多数投票；(4) 确认门控——`/evolve` interactive 模式要求人工确认（对比 nightly 的 `--auto`）；(5)
人工在环——核心行为变更（hooks/rules/CLAUDE.md/删除/cron/deps）作为 Suggested 行为提议，绝不自动应用；(6) memory-safety——未经人工审核不得进入永久 memory（Memory
Flush 队列）；(7) durability/confidence 衰减过滤（90 天半衰期）；(8) 有界编辑防止破坏性重写；(9) hook auth fallback 将失败的提取入队而非丢数据。

**协同进化**
skill-tool 生态 + generator-verifier + skill-skill。(a) 每个行为被路由到 8
种共存机制类型（hook/rule/skill/script/MCP/cron/command/agent）中最合适的一个，并随成熟度跨机制升级（rule→skill→hook）——一个 skill-tool 生态。(b)
generator-verifier：技能（.md，行为 generator）与其 eval spec（verifier，固定）协同进化；eval-discrimination meta-metric 调校 verifier。(c)
Meta-evolution：进化机制本身经由 5
个指标调优（instinct_survival_rate、skill_convergence、eval_discrimination、mechanism_coverage、compliance_rate）。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（非梯度文本空间：在 skill .md 上做 eval→improve→rollback 循环）+ population_evolutionary-ish（instincts
被提取、confidence 打分、去重、durability 门控、收敛为技能、一旦实现即归档——一种生存/路由动态）+ imitation_demonstration（从观测到的用户工具使用中提取重复模式）+
meta-optimization（调整 evolution 的旋钮）。无梯度、无 SFT、无 RL——全在 text/markdown 空间内。

**学习信号来源**
工具使用观测（PostToolUse hooks）+ 工具成功指标（goal health_check 命令，如 test 通过数）+ LLM-as-judge（eval spec 中的 eval 场景）+
self-reflection（三层提取：一遍提取 instincts/memory/research）+ held-out-ish 验证分（eval 通过率 %，含 discrimination 跟踪）+ confidence
强化/衰减（90 天半衰期）+ reference frequency。

**奖励粒度**
混合。Outcome：eval 场景通过/失败与 goal health_check 通过/失败。Process：instinct confidence 强化/衰减、reference-frequency 打分、按阶段 pipeline
跟踪，以及 meta-metrics（convergence time、survival rate）。

**学习范式**
sleep-time（主要——nightly 离线 `/hm-night` pipeline）+ inter-test-time（SessionEnd hook 在会话边界流式 harvest instincts）。离线（回放观测到的
sessions/observations）。相对用户自己的 session 为 on-policy。活体任务期间无 intra-test-time 学习。

#### 进化时机_When

**进化时机 (When)**
sleep-time（nightly agent，头条模式）+ inter-test-time（session-end instinct 提取）。活体 agent 被观测但任务期间不被改动。

**触发方式**
周期性（macOS 上 launchd / Linux 上 cron 心跳——multi-tick，默认 nightly，weekly deep 模式可配置，默认 Sunday）+ 事件触发（SessionEnd / PostToolUse
/ stop hooks → observation + extraction）+ 使用驱动（hooks 监视工具使用）+ 按需手动（`/hm-night`、`homunculus night`）。

#### 存储与检索

**技能库结构**
技能文件目录（file-system
布局：`homunculus/evolved/{skills,agents,evals}/`、`homunculus/instincts/{personal,archived}/`、`homunculus/experiments/`、`homunculus/reports/`、`.claude/{rules,commands}/`）+
层次化（architecture.yaml 目标树作为 index/brain）+ git（经 commits 的 lineage）+ staging 目录。无向量 DB、无图谱、无云端 registry；兼容 agentskills.io
以便移植。

**检索/复用方式**
description 匹配触发加载（agentskills.io 风格：由宿主 harness 在 description 匹配时加载技能）+ trigger-phrase 路由（router 技能 `homunculus.md`
把自然语言/slash 触发词如 'run evolution'/'hm-night' 映射到 command workflow 文件）+ reference-frequency 跟踪（哪些 instincts/skills 实际被读取）+
frequency/recurrence 检测用于 instinct harvest。未文档化语义向量检索。

#### 验证与反馈

**验证方式**
execution-based + LLM-judge（每个技能的 eval 场景）+ 功能正确性（goal health_check shell 命令，如 `test $(find logs/ -mtime -1 | wc -l) -gt
0`）+ 验证门控（100% 通过才保留技能；<100% 触发 improve 循环）+ 多次运行 eval `--runs/--passes N` 配多数投票 + discrimination 跟踪（eval_discrimination
meta-metric：实际能区分版本的场景占比 %）。optimizer 从不静默编辑 eval spec（测试保持固定）。

**错误纠正**
self-revision（eval→分析 FAIL/PARTIAL/GAP→定向 edit→重新 eval，最多 5 轮）+ rollback（回归 → rollback 到前一版本）+ 有界编辑 + 定向 diff patch（增补缺失
rules / 增加新章节 / 修正错误信息）+ circuit breaker（连续失败后停止 pipeline）+ archive（过时的 instincts 一旦被吸收即 prune/archive）。

#### 环境与基座

**测试环境**
通用 / 真实生产力任务。在作者自己的真实个人 AI 助手上验证（5 周纵向运行），而非受控学术 benchmark。领域 = 经 Claude Code / Cursor / Codex CLI 的 coding/生产力。

**底座模型**
Claude（默认经 `claude --print` harvest，Sonnet 级）。Multi-LLM harvest provider 可配置：claude-cli / codex-cli / anthropic-api /
openai-api（含 Ollama / vLLM / OpenRouter）。无 SkillOpt-Sleep 那种严格的 optimizer/target 分离，但 harvest 模型可经
`HOMUNCULUS_HARVEST_MODEL`/`HOMUNCULUS_HARVEST_PROVIDER` 配置，且 subscription profiles（Pro/Max5x/Max20x/API）门控 Opus 使用（仅在
full tier 用于 planning/review）。

**部署域 (Where)**
specialized——coding / 生产力 agent 领域（Claude Code、Cursor、Codex CLI coding 助手）。把 agent 适配到用户自己的 project + workflow + goals。

#### 评估指标

**评估指标**
skill_library_growth（头条：instincts/skills/agents/hooks/scripts/commands/rules/ADRs/commits 计数）+ cost（最低 ~$0.5/night、标准
~$2-3、完整 ~$5-10；subscription 用户经 5 小时会话与周利用率跟踪，而非 $）+ success_rate（eval 100% 通过）+ generalization（cross-platform）+ 5 个
meta-evolution 指标（instinct_survival_rate、skill_convergence、eval_discrimination、mechanism_coverage、compliance_rate）+
regression/gaming 计数。无正式 accuracy 风格 benchmark。

#### 局限与挑战

**局限与挑战**
scalability（仅在一个个人助理上验证，N=1；无多用户/团队证据）+ controllability（autonomy 被有意设界——核心变更需批准，故非完全 hands-off）+ eval-hacking/regression
风险（由 Gaming Gate + rollback + 多次运行投票缓解，但 LLM-judge 方差仍在；discrimination 被跟踪但未消除）+ doc_bloat 风险（由 pruning/archival + Write
Gate + durability 过滤缓解）+ optimizer_quality（依赖一个能干的 harvest 模型；弱模型不稳定）+ cost/budget（真实 nightly 开销；Pro tier 仅 minimal）+
observability（轶事性指标，无标准化 eval 套件）+ 仅 macOS/Linux（无 Windows）。

#### 可借鉴要点

**可借鉴要点**
- 稳定的目标树（architecture.yaml：每个节点 purpose/metrics/health_check）作为优化目标，配以可替换的实现（skill/rule/hook/script/agent/MCP/cron/command）按行为路由、随成熟度升级（instinct→rule→skill→hook）。这把「改进什么」（goal health + metrics）与「怎么改进」（机制路由 + eval→improve 循环）解耦，使系统能朝用户定义的目标做全局优化而非局部模式记忆——这是自进化 SKILL.md 最可移植的单点思想。
- instinct 生命周期 + 多机制路由作为 library-governance 引擎：提取 confidence 打分的 instincts（90 天半衰期）、语义去重（supersedes）、durability 门控（<0.7）、按 reference-frequency prune（+25/−15）、一旦吸收即 archive；把幸存者路由到最便宜的正确机制。这直接攻击 doc_bloat/regression，并把每个行为保持在其最优载体中（确定性→hook、路径作用域→rule、可复用→skill+eval）。配以 generator-verifier 协同进化（skill .md 对固定 eval spec）+ 5 个 meta-metrics 来进化进化机制本身。
- 分层、预算感知、review-gated 的 nightly pipeline，为自编辑指令文档钉住 autonomy/safety 平衡：基于阶段的多 tick 心跳（P1 Evolution → P2 Research 带 cross-night 去重 → P3 Experiments 在隔离 worktree 中 → P4 Sync）+ circuit breaker + 预算 tier（~$0.5–$10/night）+ 每周 deep 模式。安全操作（extract/archive/eval/improve/report）自主运行，而核心行为变更以 human-approve 的 Suggested 行为形式在晨报中呈现——这是一个可直接使用的、带人工在环的 sleep-time 自进化模板。

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
nomadically.work（作者：Vadim Nicolai，高级软件工程师）

**发布时间**
2026-02-25

**类型**
blog_practice

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 — 仅优化 Markdown
指令制品：.claude/skills/*/SKILL.md、.claude/commands/*.md、.claude/hooks/*.py、CLAUDE.md、OPTIMIZATION-STRATEGY.md 以及
auto-memory 文件。明确不优化模型权重、不优化应用源码（由 Code Improver 负责）、不优化工具。

**技能是否独立制品**
是。技能以独立可复用制品形式存在：SKILL.md 文件、command .md 文件、hook .py 文件、CLAUDE.md 与 memory 文件。为多文件技能包形式（.claude/skills/*/SKILL.md + 同级文件）。

**是否文档载体**
是。核心载体是人类可读的 Markdown 指令文档；agent 的全部可编辑面为 doc/prompt/memory 文件。

#### 技能表示

**技能编码方式**
技能文档(.md/SKILL.md) 为主载体，外加 CLAUDE.md（全局指令）、.claude/commands/*.md（command 文档）、.claude/hooks/*.py（可执行 hook
代码，但被视为在范围内的指令制品）以及 auto-memory 文件。结构化 EVOLUTION 记录将提议的编辑编码为 JSON 对象。

**技能粒度**
策略规则 / insight — 编辑针对技能文件内的单条指令、澄清与规则；每条 EVOLUTION 针对一个特定失败模式（hallucination、wrong_tool、out_of_role）。

#### SKILL.md_专属维度

**文档形态**
结构化字段 + Markdown 正文。可编辑制品为 Markdown 指令文件。提议的编辑被编码为结构化 EVOLUTION
对象，包含字段：id、target_file、trigger_patterns、trigger_findings、change_type（add_instruction|clarify_instruction|remove_instruction|...）、before（精确文本）、after（新文本）、rationale、expected_impact{dimensions,
magnitude: small|medium|large, regression_risk: none|low|medium|high}。anti-pattern 内联记录在技能文件中。Token 长度未明确，但
instruction-bloat anti-pattern 暗示一个软性大小上限，超过该上限 agent 可能截断/跳过指令。

**编辑粒度**
Minimal diff / 有界 add-delete-replace。Apply Changes 优先级：(1) minimal diff — 尽量少改动；(2) additive 优先于 destructive；(3)
specific 优先于 general；(4) testable。编辑使用精确的 before/after 文本替换。每次运行硬性上限 5 次 evolution。每条编辑必须关联 trigger_patterns 或
trigger_findings（frequency >= 2 阈值继承自 Trajectory Miner）。除非有正当理由，否则不做整文档重写。

**版本与门控**
验证门控（留出 Verification Gate）+ rejected-edit 反馈循环。每条编辑都须通过强制的 Verification
Gate，检查：coherence（修改后的技能文件是否仍内在自洽？）、跨技能冲突、CLAUDE.md 一致性以及 hook fail-open 保留。若被拒绝，Meta-Optimizer 记录该失败并调整未来优先级。未提及显式的
git-branch/Pareto/DAG 版本管理。

**文档来源**
失败轨迹蒸馏 + session 经验提取。编辑基于证据，由 Trajectory Miner 在上游产出的 JSON 失败/模式报告（frequency >= 2 的失败签名）驱动。无 LLM 一次性生成、无离线 benchmark
训练；来源始终是经由 trigger_patterns/trigger_findings 关联的被挖掘失败轨迹。

**技能库治理**
灰尘清理（curator 式 anti-bloat）+ 冲突检测。显式由 5 个 anti-pattern 治理：(1) instruction bloat — 有时应简化而非新增，关注文件体积增长；(2) contradictory
instructions — 写入前必须检查冲突；(3) over-specificity — frequency >= 2 阈值禁止一次性修补；(4) prompt-engineering theater — 避免
'IMPORTANT:'/'CRITICAL:' 滥用；(5) cargo cult — 不脱离上下文照搬研究模式。Verification Gate 执行跨技能检查。未提及
Lotka-Volterra/retirement/archive 或分层索引。

**失败记忆**
是。强负反馈记忆。(a) 5 个文档化的 anti-pattern 充当 rejected-edit 方向否决；(b) 每条 EVOLUTION 必须引用 trigger_patterns/trigger_findings（失败签名 +
归因 + 补救）；(c) CASTER 式：仅在分数下降时行动（修复失败，从不优化已生效的部分）；(d) Meta-Optimizer 记录每条被 Gate 拒绝的 evolution，并在后续下调该编辑类的权重，形成 pipeline
级的 rejected-edit buffer。

**编辑安全**
高度详尽 —
这是头条设计维度。范围边界（最重要的单一决策）：仅可编辑指令文件（.claude/skills/*/SKILL.md、.claude/commands/*.md、.claude/hooks/*.py、CLAUDE.md、OPTIMIZATION-STRATEGY.md、auto-memory）；不可编辑应用源码、schema
文件、config 文件、生成文件。理由：能同时修改自身指令与代码库的 agent 具有无界爆炸半径；限定在 Markdown 意味着最坏情况 = 一个糟糕的 prompt，会被 Verification Gate 拦截（EvoConfig
式受范围限定修改）。有界编辑：每次运行最多 5 次 evolution。证据门控：每条变更必须关联 trigger_patterns 或 trigger_findings；不允许「凭感觉的改进」。强制自我质询：任何编辑前（5
个问题，含「是否有更简单的修复，例如 CLAUDE.md 里一行？」）。anti-pattern 意识（上述 5 个 anti-pattern）。Verification Gate（coherence + 跨技能 + CLAUDE.md
一致性 + hook fail-open 保留）。每条编辑的回归风险评估（none|low|medium|high）。未提及显式的编辑前 git 备份/回滚，但有界范围 + Gate 起到同样的保护作用。

**协同进化**
Generator-verifier 协同 + skill-prompt 联合。Skill Evolver 是 6 个 pipeline agent 中的第 3 个：Trajectory Miner（第 1
个）向其输入失败报告；它编辑指令文档；Verification Gate 校验；Meta-Optimizer（策略大脑）记录结果并调整优先级。它连同细粒度技能文件一并协同编辑全局 prompt（CLAUDE.md /
OPTIMIZATION-STRATEGY.md），故 prompt 与技能联合进化。技能被所有下游 agent 消费，因此一次技能编辑隐式协同进化 agent 行为。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（非梯度、文本空间 prompt 编辑）+ reward-based（经负向文本反馈）。无 SFT/RL/gradients。结合 Meta Context Engineering 的
observe→diagnose→modify→observe 循环、CASTER 的负反馈收敛，以及 REprompt 的需求引导生成。优化完全发生在 Markdown 指令空间内。

**学习信号来源**
成败轨迹（来自 Trajectory Miner 的 JSON 失败报告）+ LLM-judge / 反思（强制自我质询）+ 验证信号（Verification Gate 的接受/拒绝由 Meta-Optimizer
记录）。expected_impact.dimensions 提供一个需求规约，用于对照实际分数变化核查。

**奖励粒度**
outcome — 由任务级分数下降与离散失败模式频率触发；每次 evolution 针对一个特定失败模式，而非 step 级 process reward。

**学习范式**
Offline + inter-test-time（任务运行之间）。作为独立的 pipeline 阶段运行，消费先前挖掘的失败报告，而非 intra-task 在线。相对当前技能版本为 on-policy（编辑活动的指令集）。

#### 进化时机_When

**进化时机 (When)**
inter-test-time（任务运行之间，作为专用 pipeline 阶段）— 处理由前序 Trajectory Miner 阶段产出的失败报告并输入 Verification Gate。非 intra-test-time 在线编辑；非
sleep-time 批量回放（尽管它按每个 pipeline 周期定期运行）。

**触发方式**
事件触发 / 失败触发 + 使用驱动。仅在分数下降或 Trajectory Miner 暴露出 frequency >= 2 的失败模式时行动。每次运行最多 5 次 evolution。单次糟糕 session 不足以促成编辑（frequency 门控）。

#### 存储与检索

**技能库结构**
技能文件目录 — 文件系统目录布局：.claude/skills/*/SKILL.md（每技能）、.claude/commands/*.md（command
文档）、.claude/hooks/*.py（hook）、CLAUDE.md（全局）、OPTIMIZATION-STRATEGY.md（策略）、auto-memory 文件。.claude/ 下扁平的按域目录；无向量库 / DAG /
云端注册中心。

#### 验证与反馈

**验证方式**
验证门控（留出 Verification Gate）+ LLM-judge 式 coherence 检查 + 功能正确性检查。Gate 执行：(1) coherence — 修改后的技能文件是否仍内在自洽？；(2) 跨技能检查 —
是否与其他技能冲突？；(3) 一致性检查 — CLAUDE.md 的改动是否一致？；(4) hook 校验 — hook 修改是否保留 fail-open 设计？此外对照实际分数变动核查
expected_impact.dimensions。被拒绝的 evolution 由 Meta-Optimizer 记录。

**错误纠正**
有界编辑（bounded edits，每次运行最多 5 次）+ 定向 diff 修补（精确 before/after 文本替换、minimal-diff 优先、additive 优先于 destructive）+ 经 Gate 拒绝的
pipeline 级回滚（Meta-Optimizer 下调失败编辑类的权重）。未提及文件级 git 回滚；纠正是预防性的（自我质询 + anti-pattern）且基于门控，而非事后回滚。

#### 环境与基座

**测试环境**
真实生产力任务 — nomadically.work 产品（remote EU job classification，远程欧盟岗位分类）。晚于最初的通用 Skill Evolver：实现后来特化为一个目标驱动的「Classifier
Tuner」，针对 remote EU job classification 中的假阴性（false-negative）削减。

**底座模型**
Claude（由 .claude/ harness、CLAUDE.md、.claude/skills 及 Claude Code 约定所暗示）。optimizer/target 分离：Skill Evolver（optimizer
agent）编辑供其他 target agent 消费的指令文件；二者运行于同一 Claude backbone。未指定确切模型变体。

**部署域 (Where)**
specialized（job-posting 分类 / remote-EU-job 过滤领域，经 nomadically.work）。最初为 general 用途的指令编辑，后特化为 classifier-tuning 目标。

#### 评估指标

**评估指标**
success_rate（任务分数，其下降触发 evolution）+ 回归率/regression_risk（每编辑评级 none|low|medium|high，Gate 检查其他维度的回归）+
泛化（anti-over-specificity 门控，frequency>=2）+ 成本相关（有界编辑，每次运行最多 5
次）。expected_impact.magnitude（small|medium|large）是一个自报的效应量估计，由 Gate 核查。

#### 局限与挑战

**局限与挑战**
文档膨胀（instruction bloat — 首要 anti-pattern；文件可能增长直到 agent 截断/跳过）+ 回归风险（Gate 的存在正是因为编辑可能导致其他维度回归；逐编辑评级）+ eval-hacking
风险（prompt-engineering theater anti-pattern — 滥用 IMPORTANT/Critical 标记；由「改为精确表达」缓解）+ 可控性（依赖强 optimizer
backbone；cargo-cult anti-pattern 警告勿在不理解的情况下照搬模式）+ 可迁移性（范围局限于单一产品 pipeline；跨模型/跨 harness
迁移未被验证）。灾难性遗忘相关性较低（无权重训练），但「contradictory instructions」anti-pattern 是其文档空间的类比。

#### 可借鉴要点

**可借鉴要点**
- 范围边界是头号安全决策 — 将指令编辑 agent 限定在仅 Markdown/指令文件（不可触碰应用源码、schema、config、生成文件）。理由：能同时修改自身指令与代码库的 agent 具有无界爆炸半径；将编辑限定在 Markdown 意味着最坏情况是一个糟糕的 prompt，可被 Verification Gate 拦截。这一条规则把「令人恐惧的自我修改」转变为「枯燥、有界的自我改进」。可直接移植到任何 SKILL.md-evolver：定义一个显式的 CAN-edit / CANNOT-edit 清单（EvoConfig 式）。
- 证据门控编辑 + 强制自我质询迫使最简单干预 — 每条提议的编辑必须引用一个具体的失败签名（trigger_patterns/trigger_findings，frequency >= 2），且一个强制的编辑前自我质询步骤会问「是否有更简单的修复 — 例如在重写整份技能文件前，先在 CLAUDE.md 里改一行？」。这阻止了指令 evolver 最常见的单一失败模式：当一行全局 prompt 微调就足够时却重写整份技能文件。将硬性证据要求与「最简优先」自我质询结合，以保持编辑最小化且可解释。
- 负反馈记忆作为 anti-pattern 否决 + Generator-verifier 协同进化 — 仅在分数下降时行动（CASTER 式：失败比成功更具信息量），并将编辑器自身的反复失败模式编纂为显式 anti-pattern（instruction bloat、contradictory instructions、over-specificity、prompt-engineering theater、cargo cult），作为 rejected-edit-direction buffer。将编辑器与一个独立的 Verification Gate（coherence / 跨技能 / consistency / fail-open 检查）配对，其拒绝反馈给一个下调失败编辑类权重的 Meta-Optimizer — 从而闭合一个 generator-verifier 协同进化循环，学习哪类技能改动真正有效。

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
独立/社区作者（GitHub 用户 'venotyh'）。无所属机构；个人/实验性开源项目（1 star、8 commits、Python）。README 自嘲式开篇写道 '# No!!! This project is absolute bullshit.'

**发布时间**
2026（仓库活跃时间约 2026-05；CHANGELOG 处于 'Unreleased' 区段；未发布任何 tag/release/version）。

**代码链接**
https://github.com/venotyh/evoskill

**类型**
blog_practice / industry (small open-source experimental CLI tool, pip-installable via `pip install -e .`). Not an
academic paper. Unrelated to and predates/confuses naming with sentient-agi/EvoSkill (arXiv:2603.02766) despite the
identical command name `evoskill`.

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能。可进化的对象是 Skill GENOME = system_prompt (str) + instructions (list[str]) + tool_bindings (list[str])
+ parameters (dict)，定义于 core/genome.py:SkillGenome。模型权重冻结（FROZEN）；单 agent
架构固定。工具本身是一组固定的内置集合（read_file、write_file、shell_exec、web_search、search_files）——只有它们的 BINDINGS（一个技能使用哪些工具）会进化，工具实现不变。

**技能是否独立制品**
是。每个技能是一个独立可复用的制品，但不是 markdown 文件——它是一个序列化的 dataclass，以 JSON 持久化于
~/.evoskill/（storage.py：save_skill/list_skills/load_skill/delete_skill）。制品形态 = JSON 记录 {id, name,
genome{system_prompt,instructions,tool_bindings,parameters}, parent_ids, generation, fitness, fitness_history,
mutation_type, mutation_desc, created_at, task_count}。无技能文件夹、无辅助脚本、无 SKILL.md——纯结构化数据。

**是否文档载体**
否（纯结构化数据，非可读的指令文档）。技能的 'instructions' 作为一串短字符串存放于 JSON 序列化的 dataclass 内部；不存在 markdown/SKILL.md 指令文件。在 agent 运行时，genome
被展平注入 LLM system prompt（system_prompt + '\n\nKey instructions:\n- ...'）——该文档只短暂存在于 LLM context 中，从不在磁盘上落盘为 .md
制品。（注：仓库树中存在一个 .claude/skills/ 目录但为空——从未在那里写入任何 SKILL.md。）

#### 技能表示

**技能编码方式**
结构化字段（dataclass -> JSON）+ 自然语言 SOP（instructions list）。SkillGenome 是一个带 4 个类型化字段的 Python
@dataclass（system_prompt:str、instructions:list[str]、tool_bindings:list[str]、parameters:dict），通过 to_dict/from_dict 与 JSON
dict 互转。agent 运行时将其重组为一条 LLM system message。无向量嵌入、无图、无 .md 文件、无多文件包。

**技能粒度**
策略规则 / 完整技能包。每个技能编码一个完整的 agent persona/策略（一个 system prompt + 若干行为规则 + 一个工具子集 + 采样参数）——比原子动作粗，比多 agent workflow 细。种子技能携带
4 条通用指令；进化后的技能携带 2-10 条简短可执行规则。粒度 ≈「whole-agent configuration as one genome」。

#### SKILL.md_专属维度

**文档形态**
JSON 序列化的 dataclass（非文档）。每个技能的具体形态：{system_prompt: <2-5 句的 str>, instructions: [<short actionable rule>, ...]（≤10 条，每条约
10-15 tokens），tool_bindings: [<tool name>, ...]（5 个内置工具的子集），parameters: {temperature: 0.1-1.0, max_tool_calls: int,
verbose: bool}}。以每个技能一个 JSON 对象的形式持久化于 ~/.evoskill/（data_dir）。无 YAML frontmatter、无 markdown 正文、无代码块。装配后的 system
message（prompt + instructions）典型 token 长度 ≈ 100-300 tokens[估算；agent 调用除 max_tokens=2048 外无显式上限，instructions 上限 10 条]。

**编辑粒度**
整字段重写 + 有界 add/delete/replace（field-level，非整文档）。mutation 算子定向具体的 genome 字段：(a) mutate_guided 重写 system_prompt 和/或整体替换整个
instructions 列表（LLM 输出新的 SYSTEM_PROMPT + INSTRUCTIONS 区段，由 _apply_guided_response 解析）；(b) mutate_prompt 要么替换
system_prompt、要么替换 instructions、要么追加一条 instruction；(c) mutate_tools 增加或删除一个 tool binding；(d) mutate_params 微调一个数值参数；(e)
crossover 重组两个 parent 的字段（system_prompt 取自其中一个 parent，instructions 交错合并，tool_bindings 取并集，params 逐键随机选取）。无
minimal-diff/PATCH、无行级编辑——最小单位是一个字段。

**版本与门控**
DAG 血脉（仅用于追踪/查询）+ 生成代际剪枝（generational pruning，非留出验证）。每一代：population + children 合并、按 fitness 排序、截断到 population_size（默认
10）——最弱者被剪枝（save_skill 持久化 children，但活跃 population 为 top-N）。Elitism：top-2 精英在 task_count<6
时获得额外深度评估（max_tasks=3）。Lineage DAG 为每个技能记录 parent_ids/generation/mutation（可查询 ancestors/descendants），但它是描述性账本，而非准入门控。无留出
train/val 划分、无 git branching、无 Pareto 前沿、无 review-gate、无 staging+backup——准入完全依据同一套 10 个内置任务上的样本内 fitness。

**文档来源**
人工初始化 + LLM 一次性生成。原始种子技能为人工编写（core/skill.py:create_seed_skill——固定的通用 persona）。所有后代由 LLM 引导的算子产生（mutate_guided 在零失败上下文下请求
LLM 给出「改进版本」）或由随机结构性 mutation 产生（增/删 instruction、微调 prompt 后缀、调参）。无失败轨迹蒸馏、无轨迹回放、无会话经验抽取——guided mutation 是无上下文的单次 LLM
重写。

**技能库治理**
生成代际剪枝（generational pruning / 最弱者隐式退役）。每一代合并 population+children 并仅按 fitness 保留 top population_size——库规模天然有界。tournament
selection（k=3）挑选 parent。无显式 dedup/merge、无 similarity-retrieval-edit-targeting、无 curator loop、无 Lotka-Volterra/archival
动力学。mutation 多样性由随机方式（25% random mutation）维持，而非由治理机制维持。所有被持久化的技能即使被逐出活跃 population 也仍累积于 ~/.evoskill/ JSON store（仅内存中的
population 被剪枝，磁盘记录单调增长——长 sleep 运行中存在无界磁盘增长的潜在风险）。

**失败记忆**
否（无 anti-pattern / rejected-edit / failure-signature 记忆）。每个技能的 fitness history 被跟踪（fitness_history list +
滚动平均），但仅用于排序，从不作为负反馈回传。guided-mutation 的 prompt（_build_guided_mutation_prompt）只向 LLM 展示「当前」genome——无过往失败、无被拒 mutation、无
anti-pattern。无 feedback_history、无 related-iterations 引用、无 rejected-edit buffer。降低 fitness 的 mutation 会在下一代被静默剪枝，不向未来
mutation 显式呈现任何记录的原因。

**编辑安全**
沙箱执行（sandboxed tool execution）是首要护栏。(a) SkillAgent.run 将所有工具调用（file ops、shell_exec、web_search）在
tempfile.TemporaryDirectory(prefix='evoskill_') 内执行，并 os.chdir 进入、退出时自动清理——shell 命令与文件写入无法触及真实文件系统。(b) MAX_TOOL_ROUNDS=8
限制 agent 循环长度（耗尽时返回 success=False）。(c) 每个 genome 的 max_tool_calls 参数约束工具使用。无编辑前备份/回滚（JSON 原地覆写）、无 git isolation、无用于检测
eval-hacking/过拟合的留出验证、无人工在环、无关于哪些 genome 字段可被编辑的范围边界、无 secret/injection 扫描、无抵御破坏性 prompt 重写的 bounded-edit 保护（guided
mutation 可整体替换 system_prompt）。API 密钥在 `config show` 输出中被掩码、.mcp.json 被 gitignore（仅 config 层有 secret 卫生）。

**协同进化**
skill-only + skill-prompt 联合 + skill-tool-binding（弱）。genome 将 system_prompt 与 instructions 与 tool_bindings 与 parameters
作为一个原子单元联合进化，故按构造即为 skill-prompt 协同进化（四个字段一起 mutation）。tool BINDINGS 协同进化（增/删工具），但工具本身是固定内置——非强意义上的 skill-tool 协同进化。无
skill-skill 生态交互（技能仅通过排序竞争，互不调用/引用）、无 generator-verifier 协同进化、无独立的 verifier 进化（judge LLM 与 agent/mutator 是同一模型）。

#### 自进化机制_How

**进化方法范式 (How)**
population_evolutionary + reward-based（LLM-as-judge）。经典代际进化循环：initialize_population -> tournament-select parents（k=3）->
通过加权 mutation portfolio 创建 children -> 评估 fitness -> merge+sort+prune 到 population_size -> 下一代。mutation
portfolio（engine.py:_create_child）：Crossover 20%（双亲重组）、Guided mutation = guided_weight（默认 55%，LLM 重写 prompt）、Random
mutation = 余下 25%（在 prompt_mutate/tool_add-drop/param_tune 上均匀分布）。Elitism：top-2 存活者获得更深的二次评估。无
gradient/SFT/RL——权重冻结，纯文本空间进化搜索在 genome 字段上进行。

**学习信号来源**
LLM-as-judge + 工具成功率指标（structural）。fitness = 0.8 * judge_score + 0.2 *
structural_score（fitness.py:_score_single_task）。Judge：一次独立的 LLM 调用按严格 rubric 与 reference_answer_hint 对 agent 输出打 1-10
分。Structural：base 5.0，若 agent 失败（达到 max rounds / 无输出）-2.0，若 output>20 chars +1.0，expected_tools 与实际使用工具的重叠最多 +2.0。无环境
reward、无 self-reflection、无 held-out 分、无人工反馈。

**奖励粒度**
outcome（结果）。每任务一个 1-10 的标量分，在随机任务样本上取平均（quick_fitness 对 children 用 num_tasks=2，evaluate_skill 对 elites 用
max_tasks=3-5）。无 process/step-level reward；单次运行内唯一的信号是二值 success flag（agent 是否在 MAX_TOOL_ROUNDS 内、且未出现无 tool_calls
的轮次而完成）。

**学习范式**
offline + sleep-time + on-policy。进化以离线批处理运行（不在用户实时任务执行期间）。显式的「sleep mode」（simulator.py:SleepSimulator，`evoskill sleep`
CLI）设计用于在空闲时段运行代际循环（idle_seconds 阈值，但实现注释指出它「并不真正 block——只是记一笔」）。on-policy：每个候选通过实际实例化一个全新 SkillAgent 并对冻结 LLM 运行来打分。无
off-policy replay buffer、无 experience replay。

#### 进化时机_When

**进化时机 (When)**
sleep-time（夜间/空闲离线）+ inter-test-time（手动批处理）。主打框架是 sleep-time 模拟（「通过 sleep-time 模拟来繁殖、mutate 并改进的技能」）。两个入口：(1) `evoskill
evolve -g N` 按需同步运行 N 代（inter-test-time 批处理）；(2) `evoskill sleep -g N` 运行面向空闲时段的 SleepSimulator 循环。无 intra-test-time
进化（agent 不在实时任务期间自我编辑）。

**触发方式**
周期性（generation loop）+ 手动（CLI）+ 空闲触发（idle threshold，名义上）。`evolve` 为手动按需；`sleep` 运行固定的 max_generations 循环并带一个名义上的
idle_seconds 门控（被检查但不强制——代码注释：「Don't actually block — just note it」）。无失败触发进化、无 cron/launchd
调度器集成、无课程驱动、无使用驱动触发、无工具退化触发。触发模型 =「用户启动一个有界的 generation loop」。

#### 存储与检索

**技能库结构**
DAG 血脉 + 扁平（flat JSON store）。所有技能以独立 JSON 记录持久化于 ~/.evoskill/（扁平目录，storage.py）。LineageTree（evolution/lineage.py）从
parent_ids 构建内存中的 DAG，带预构建的 _children 索引与 _roots 列表；lineage.json 存储节点映射。非 git branches、非向量库、非层级目录、非云端注册中心。该 DAG 支持
ancestors/descendants/children/by_generation 查询及 ASCII 树渲染。

**检索/复用方式**
排序选择（rank-based selection）+ tournament。任务执行（`evoskill run`）：列出所有技能、按 fitness 降序排序、取 skills[0]。parent 选择：tournament
selection（采样 k=3、取最优、去重）。无语义相似度、无 embeddings、无 BM25、无 description-matching、无 generation-as-retrieval——检索是纯 fitness
排序截断。「best skill」就是 fitness 最高的 JSON 记录。

#### 验证与反馈

**验证方式**
执行验证（execution-based）+ LLM-judge。每个候选技能通过实际运行 SkillAgent 对抗采样的内置任务（真实 LLM 调用 + 真实沙箱工具执行）、并以 LLM-as-judge rubric（1-10）混合
structural 启发式来给输出打分进行验证。无留出验证集、无 surrogate verifier、无多模型辩论、除 judge 的主观打分外无正式的功能正确性检查。10
个内置任务（core/tasks.py）是唯一的验证面（file_summary、web_research、shell_investigation、logical_reasoning、code_explain、error_debug、data_processing、search_organize、planning_task、system_analysis）。

**错误纠正**
剪枝淘汰（pruning）——唯一的纠正机制。低 fitness 的 children 每代被逐出活跃 population；无自我修订、无 rollback（JSON 覆写，除 fitness_history 外无历史）、无
bounded-edit 重试、无定向 diff 修复、无重规划。坏的 mutation 直接被丢弃、parent 存活；下一代可能随机产生更好的 child。guided-mutation 解析失败会优雅降级（回退为把
response[:500] 追加到 system_prompt 或回退到局部 structural mutation），但在「学习」意义上并未被「纠正」。

#### 环境与基座

**测试环境**
通用（general-purpose 玩具任务）。10
个手工编写的内置任务，横跨若干类别：tool_use（file_summary、shell_investigation、search_organize、system_analysis）、multi_step（web_research、code_explain、data_processing、planning_task）、reasoning（logical_reasoning、error_debug）。非标准
benchmark（无 SWE-bench、无 SkillsBench、无 GDPVal、无 Minecraft/Web/GUI 环境）——合成 mini-task，锻炼 file/shell/search 工具与基本推理。

**底座模型**
Claude / GPT / 开源 LLM（经统一 LLMClient 的多 provider）。支持 Anthropic（默认 claude-sonnet-4-20250514）、OpenAI（默认 gpt-4o）、DeepSeek（默认
deepseek-v4-flash）。provider 由模型名前缀自动探测；另暴露一个 OpenAI 兼容的本地 gateway（`evoskill gateway`）。无 optimizer/target 分离——（a）被评估的目标
agent、（b）guided-mutation 算子、（c）LLM-as-judge 打分器使用「同一个」已配置模型。全程权重冻结。

**部署域 (Where)**
general（通用）。一个通用的 agent-skill 进化玩具：未专门面向 coding/GUI/office/document 领域。任务横跨 file ops、shell、web search、logic puzzles、code
explanation——一种横向的「让通用助手在杂项任务上更好」的框架。部署制品 = 由 `evoskill run` 加载、用以处理任意 pipe-in 任务的最佳 fitness 技能 genome（JSON）。

#### 评估指标

**评估指标**
success_rate（fitness 分 1-10）+ skill_library_growth（total_skills、max_generation、roots 计数，经 lineage.stats()）+ 每代
best_fitness/avg_fitness 趋势。SleepSimulator 打印逐代 fitness 趋势柱状图与一个最终 delta（improved/unchanged/decreased）。无泛化指标、无样本效率跟踪、无
cost/token 核算、无经济价值捕获、无跨运行的回归率监测。mutation 分布（每个 MutationType 的计数）作为库统计上报。

#### 局限与挑战

**局限与挑战**
scalability（玩具级 10-task 套件；population_size=10 偏小；仅样本内 fitness）+ eval-hacking/过拟合（judge LLM 对「同一批」用于驱动选择的 10 个任务打分——无
held-out 划分；judge 与 agent/mutator 是同一模型，存在 confirmation bias 与 reward hacking 风险）+ regression_risk（无验证门控；一个「更 fit」的
child 可能过拟合 10 个任务、在真实工作上回归；无 rollback）+ optimizer_quality（guided mutation 是无上下文的单次 LLM
重写、无失败分析；质量完全依赖所配置模型；DeepSeek/gpt-4o 行为可能差异很大）+ doc_bloat N/A（JSON genome，非散文）+ transferability（未测试；结构性可移植性被假定但未
benchmark）+ 无界磁盘增长（所有 children 即使被逐出活跃 population 也被永久持久化）+ catastrophic_forgetting N/A（权重冻结）+
controllability（全自动循环，无人工在环，对 prompt 重写无范围限制）。项目自述为实验性/低质量。

#### 可借鉴要点

**可借鉴要点**
(1) Skill-as-typed-GENOME（system_prompt + instructions[] + tool_bindings[] + parameters{}）而非
skill-as-markdown-document：将可进化技能编码为一个带具名类型化字段的小型结构化 dataclass，使每个进化算子可定向到「特定」字段（mutate_prompt / mutate_tools /
mutate_params / crossover），得到一个干净、类型安全的 mutation 空间，远比自由形式的 markdown diff 更易推理与序列化。这是最具可移植性的单一想法——任何 SKILL.md
自进化系统都可受益于把文档分解为具名 genome 字段、逐字段 mutation，而非把整个 .md 当作不透明字符串。(2) 加权三算子 mutation portfolio，带一个显式的 exploitation/diversity
旋钮：Guided 55%（LLM 驱动的 exploitation，挑选「最优」parent）、Random 25%（多样性维持，挑选「随机」parent）、Crossover 20%（双亲重组）——以单一 `guided_weight`
旋钮暴露，便于用户调整平衡。教训：不要依赖单一 mutation 算子；把 LLM 引导的改进（exploit）与随机结构性 mutation（explore）及重组结合，并让配比可调。(3) 带预构建 child 索引的 Lineage
DAG，支持 O(depth) 的 ancestor/descendant 查询 + ASCII 树渲染：让每个技能携带 parent_ids/generation/mutation_type 并构建倒排 children
索引，把进化历史变成可查询、可可视化的制品（`evoskill lineage`），这对信任并调试自主技能进化至关重要——你能把任一技能追溯回原始种子，并看清是哪个算子产生了它。即便是基于 SKILL.md 的系统也应嵌入这种
lineage 元数据（frontmatter parent_ids + generation）并渲染家族树，因为可检查性是安全自进化的前提。

#### 不确定字段

- paper_link（无论文；项目仅有 code+README）
- release_date（无 git tags/releases；据仓库活跃时间约 2026-05 与 CHANGELOG 'Unreleased' 区段推断）
- institution（独立作者；未披露正式所属机构）
- key_results（仓库中任何地方均未报告实验或量化结果）
- cross_transfer（跨 Anthropic/OpenAI/DeepSeek 的结构性可移植性存在于代码中，但无任何迁移实验被记录）
- doc_form token 长度（无显式上限；据 seed-skill 字段大小估算每个装配后 system message 约 100-300 tokens）

---

### TextGrad

> `idea_text_opt` · Stanford, Nature 2025(arXiv:2406.07496)。用 LLM 文本反馈做「自动微分」：把复合 AI 系统建模为计算图，对任意变量(prompt/code/分子/方案)反传 textual gradient 进行优化。 PyTorch 风格 API。GPQA 51%→55%，LeetCode-Hard +20%。是 SkillOpt「reflection=backwar

#### 基础信息

**名称**
TextGrad

**提出机构**
Stanford University（Zou Group / James Zou Lab）。作者：Mert Yuksekgonul、Federico Bianchi、Joseph Boen、Sheng Liu、Pan Lu、Zhi Huang、Carlos Guestrin、James Zou。

**发布时间**
arXiv 预印本：2024-06-11（arXiv:2406.07496）。发表于 Nature：2025-03-19（Nature vol. 639, pp. 609-616；Nature 标题：'Optimizing
generative AI by backpropagating language model feedback'）。

**论文链接**
https://arxiv.org/abs/2406.07496 ；Nature：https://www.nature.com/articles/s41586-025-08661-4

**代码链接**
https://github.com/zou-group/textgrad（MIT license；pip/conda install textgrad）

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context 记忆与提示（Context/Prompts）。TextGrad 不触碰模型权重；它把复合 AI
系统中的文本取值组件视为可学习的「变量」（tg.Variable，requires_grad=True），并在文本空间中优化它们。可优化的变量包括：system/user 提示、思维链解、代码片段、few-shot
示例、分子结构（SMILES）以及放射治疗计划。复合 AI 系统被建模为一个计算图，其节点是（不一定可微的）函数调用的输入/输出；反向传播把自然语言「文本梯度」（批评）从目标/loss
流回每个叶子变量。这是「prompts-as-parameters」的基础范式。

**技能是否独立制品**
部分是。每个被优化的对象都是一个一等公民 tg.Variable（value + role_description + requires_grad + gradients + gradients_context），最终优化值（如改进后的
system prompt）是一个可保存/导出的普通可复用字符串。但 TextGrad 不提供任何持久化的 skill-library / artifact-management
抽象：变量仅存在于优化运行期间的记忆体内计算图中。没有版本化的 skill-pack、没有跨运行 registry、没有 skill-file 格式。因此：制品 = 一段文本字符串（prompt/solution），而非受管理的
SKILL.md 风格文件。

**是否文档载体**
否。被优化对象是一个原始文本字符串（自然语言提示、代码或如 SMILES 的结构化字符串），而非人类可读的指令文档。没有 markdown/SKILL.md 载体，也没有结构化的 YAML-frontmatter
正文。最接近的类比是「优化一个 system-prompt 字符串」，这是纯指令文本而非结构化文档。（仅在变量值可能内含代码块的平凡意义上属于「混合」。）

#### 技能表示

**技能编码方式**
自然语言文本字符串（提示、推理、批评）/ 可执行代码（LeetCode 解）/ API 调用图（BlackboxLLM、FormattedLLMCall）/ 结构化字符串（SMILES 分子、放射治疗计划参数）。变量是带
role_description 标注的普通 Python 字符串；其「编码」只是字符串 + 角色元数据，封装在一个类 PyTorch autograd 图中（Function/Module，含 forward+backward）。

**技能粒度**
策略规则 / 完整 system-prompt 级（典型用例是为某个 QA 任务优化一整个 system prompt）。也支持整体解粒度（一道题的完整 CoT 解）、整体代码片段粒度（一整个 LeetCode 解）以及分子/计划粒度。粒度较粗 = 整个变量是一个优化单元；变量内部没有原子动作或子步骤的分解。

#### SKILL.md_专属维度

**文档形态**
纯文本 system-prompt 字符串（无 frontmatter，无结构化字段）。典型长度：几百 tokens 到约 1-2k tokens 的 system prompt（如 BBH 任务描述 + 累积指令）。改进后的提示由 TGD
optimizer 在 <IMPROVED_VARIABLE></IMPROVED_VARIABLE> 标签之间输出。对于代码/分子/计划优化，「文档」即对应的代码/SMILES/计划字符串。无多文件打包。

**编辑粒度**
整变量重写（whole-variable regeneration）。TextualGradientDescent optimizer 让 optimizer-LLM 输出一个全新的 <IMPROVED_VARIABLE>
替换整个旧值；核心中没有 minimal-diff / PATCH / add-delete-replace 原语。（string_based_ops.py 提供少量字符串操作，但标准路径是整体重写。）具体地
optimizer.step() 解析 new_value = response.split('<IMPROVED_VARIABLE>')[1].split('</IMPROVED_VARIABLE>')[0] 并调用
parameter.set_value(new_value)。

**版本与门控**
留出验证门控 + 在 dev 划分上的贪心爬山选择。在 evaluation/prompt_optimization.py 中，run_validation_revert() 在每次 optimizer step 之后于 val_set
上评估候选提示；若 val 准确率跌破此前最佳，则把变量回滚到上一个值（system_prompt.set_value(previous_prompt)）并记录被拒提示。额外的稳定性机制：gradient_memory（保留最近 N
条文本梯度）与 TextualGradientDescentwithMomentum（保留过去 {value, gradient} 对的动量窗口）。无 git/DAG/Pareto-front 版本管理。

**文档来源**
初始值由人工/种子初始化（如 STARTING_SYSTEM_PROMPT = train_set.get_task_description()）。后续版本由文本梯度反馈经 LLM 生成：反向产生自然语言批评，TGD optimizer
LLM 重写该变量。因此 provenance = 人工种子 + 由 LLM-critic 反馈驱动的迭代式 LLM 再生（一种失败轨迹/批评蒸馏）。

**跨载体迁移**
跨模型：设计上很强——引擎抽象（OpenAI/Anthropic/Gemini/Together/Bedrock/Cohere/Groq/vLLM/local/litellm）与显式的 optimizer/target
分离（前向「test」引擎如 gpt-3.5-turbo 可用更强的反向引擎如 gpt-4o 来优化）。跨任务：框架与任务无关（同一 API 适用于 QA、代码、分子、放射治疗）。跨用户/跨 harness：未涉及（无
agent-harness 概念）。未对单一优化提示的跨模型迁移做实证研究。

**技能库治理**
在 skill-library 层面不存在——TextGrad 不维护技能库。类似治理的有界机制：(1) gradient_memory 对每个变量只保留最近 N 条梯度（有界 buffer，防止无界增长）；(2) 动量窗口限制历史；(3)
验证回滚丢弃回归候选。无去重/合并、无退役/归档、无分层索引、无 curator loop。

**失败记忆**
部分有。(1) 验证回滚在候选于 dev 划分上表现不佳时记录「rejected prompt」——这是一种弱的负信号，但未被作为可复用的 anti-pattern 存储。(2) gradient_memory
把过去的文本梯度（往往描述错误）留到下一次 optimizer step。(3) momentum_storage 存储过去的 {value, gradients}。然而没有显式的失败特征库、没有归因+补救的 anti-pattern
库，也没有被复用以否决未来编辑的 rejected-edit buffer。因此：通过回滚给出隐式负反馈，而非持久的 failure-memory 制品。

**编辑安全**
轻量。(1) 留出验证回滚（run_validation_revert）是首要保障——拒绝回归编辑并恢复上一个值。(2) optimizer 的自然语言 constraints
参数（constraints=[...]）让用户用规则约束编辑器；(3) in_context_examples 引导重写方向；(4) gradient_memory/momentum
抑制失稳编辑。除回滚外无自动的编辑前备份+回滚、无范围边界强制（任意字符串都可被重写）、无 eval-hacking 防御、无人工在环门控、默认无注入/密钥检查。

**协同进化**
generator-verifier 协同进化（前向模型 vs 反向/评估引擎）是核心架构：前向 LLM（目标）产出输出，独立的反向引擎（LLM-as-critic）产出梯度，loss/eval 模块充当验证器——optimizer 与
target 显式可分离（set_backward_engine）。此外也支持 skill-prompt 联合优化（一个 optimizer.parameters() 列表中含多个 Variable，如 system_prompt +
few-shot 示例一起更新）。它不是 skill-tool 或 skill-skill 的生态协同进化（无工具 registry、无多 agent 技能生态）。

#### 自进化机制_How

**进化方法范式 (How)**
reward-based 的文本反馈驱动的文本空间 rollout_optimization（非梯度）——这是文本空间优化范式的奠基性 How-idea。机制：(1) 前向——运行复合系统（LLM 调用 / 工具）产出输出；(2)
Loss——一个 TextLoss/MultiFieldEvaluation/MultiChoiceTestTime/ImageQALoss 模块（给定自然语言目标的 LLM 评估器）对输出打分并发出文本「loss」；(3) 反向——沿
autograd 图执行链式法则：每个 LLMCall.backward() 在给定对话 + 下游梯度的情况下，让反向引擎批评每个 requires_grad 的前驱变量；aggregate()/Sum 跨 batch
合并梯度（aggregate = 对多条反馈的 LLM 摘要，见 reduce_prompts.py 的 REDUCE_MEAN_SYSTEM_PROMPT）；(4)
Optimizer.step()——TextualGradientDescent 把 {变量值, 角色, 文本梯度, 约束, in-context 示例, 梯度记忆} 喂给 optimizer LLM，输出一个
<IMPROVED_VARIABLE>。无权重梯度、无 SFT、无 RL 策略更新——纯文本空间重写，把 LLM-as-judge 的批评当作「文本梯度」。比喻：把 autograd/backprop 应用到文本变量。

**学习信号来源**
LLM-as-judge（loss/eval 函数本身就是一个带自然语言评估指令的 LLM 调用——如 TextLoss、MultiChoiceTestTime 的 'Investigate the reasoning and
answer... be very critical'）；对代码任务，是基于执行的信号（LeetCode 测试通过/失败）；对 QA，是真值准确率。留出验证分（val_set 准确率）驱动贪心回滚决策。「文本梯度」= LLM critic
对某变量应如何改变的自然语言描述。

**奖励粒度**
混合，以 process 为主。TextLoss/反向引擎批评推理过程（'Investigate the reasoning and answer... raise potential issues and mistakes'），故梯度是
process 级批评。outcome 信号（对/错、测试通过/失败）用于 eval/val 层。即 process（批评）+ outcome（准确率）混合。

**学习范式**
离线、跨 minibatch 的迭代优化循环（基于 epoch，batch_size 默认 3，max_epochs 默认 3）。实质上 on-policy（每 batch 从当前变量值新生成响应）且离线（在部署前于固定的
train/val/test 划分上运行，而非在实时服务期间）。test-time-loss 变体更接近在线 intra-test-time（在 context 内改进单条响应），但头条的提示优化范式是离线 batch 优化。

#### 进化时机_When

**进化时机 (When)**
以 inter-test-time 为主（任务执行之间/前后的离线优化：在 train batch 上跑 optimizer，在 val 上验证，在 test 上评估）。MultiChoiceTestTime /
test-time-loss 用例属于 intra-test-time（推理期精修单条响应）。无 sleep-time/overnight replay 调度。

**触发方式**
周期性 / 课程驱动：一个固定的优化循环（在 train_loader batch 上跑 max_epochs），即 epoch 驱动。也按 batch 事件触发（每 batch 反向后执行 optimizer.step()）。框架本身无
cron/launchd、无失败触发的再优化、无基于使用量或工具退化的触发（由用户手动启动优化脚本）。

#### 存储与检索

**技能库结构**
无技能库。变量构成一个临时的记忆体内 DAG（由带前驱与 grad_fn 的 Function/Module 节点构成的计算图）。对提示优化而言，结构实质上是扁平的（一个被优化的 system_prompt Variable）。无向量库、无文件目录、无 git 分支、无云端 registry。

**检索/复用方式**
在「库」意义上不适用——被优化的变量被直接使用（字符串替换进下一次前向调用）。在一次运行内，gradient_context 元数据把每条梯度链接到产生它的对话/context（gradients_context 字典），optimizer
据此检索以构造更新提示。无语义相似度 / BM25 / generation-as-retrieval。

#### 验证与反馈

**验证方式**
留出验证（val_set）+ 验证门控（run_validation_revert 在回归时回滚）+ LLM-judge（eval_fn / loss 本身是 LLM 评估器）+ 代码的执行正确性（LeetCode 隐藏测试）与 QA
的真值准确率。未使用多模型辩论；代理验证器 = 反向引擎自身。代码做功能正确性检查；由 load_task 返回任务特定的 eval_fn。

**错误纠正**
回滚 / 恢复（run_validation_revert 在 val 回归时恢复上一个提示）+ 自我修订（optimizer LLM 依文本梯度重写变量）。通过 constraints + gradient_memory +
momentum 做有界编辑。无定向 diff patch、无显式重规划模块——纠错即由验证门控的整变量重生。

#### 环境与基座

**测试环境**
通用 / 多领域：QA（GPQA、MMLU、BBH、GSM8K）、编程（LeetCode-Hard）、经复合系统的工具使用、分子优化（类药小分子，in silico 结合）、放射治疗计划。textgrad/tasks
中提供的任务加载器：big_bench_hard、gpqa、gsm8k、leetcode、mmlu、multimodal。

**底座模型**
以 GPT 系列为主（GPT-4o 作为反向/评估引擎，gpt-3.5-turbo 作为提示优化示例中的前向 test 引擎）。显式 optimizer/target 分离：set_backward_engine() 把
critic（强）与前向模型（目标）解耦。支持 OpenAI、Anthropic、Gemini、Together、Bedrock、Cohere、Groq、vLLM、local（LM Studio/OpenAI 兼容）以及基于 litellm
的实验性引擎——任意 LLM 都可作前向或反向引擎。多模态经 OrderedFieldsMultimodalLLMCall（GPT-4o vision）。

**部署域 (Where)**
general——TextGrad 是面向任意复合 AI 系统的通用优化框架，横跨推理、编程、化学与医学得到验证；不专用于单一垂直领域。

#### 评估指标

**评估指标**
success_rate / accuracy（test_set 上的 QA 准确率、LeetCode 通过率）、泛化（优化后的提示在留出 test 划分上评估并显示改进了 GPT-4o 的
zero-shot）、相对性能增益（LeetCode-Hard 上 +20% 相对）、成本（LLM 前向+反向调用次数——报告不多）、样本效率（在几个 epoch / 3
步内收敛）。还有领域内指标：分子对接分数、放射治疗计划特异性。skill-library 增长与经济价值指标不适用。

**关键结论**
(1) GPT-4o GPQA zero-shot 准确率开箱即从 51% 提升到 55%，无需改动框架。(2) LeetCode-Hard 编程解优化上 +20% 相对增益。(3) 改进了推理任务的提示（BBH 物体计数示例：一次 TGD
step 后错答 7 -> 正确 10）。(4) 设计出具有理想 in silico 结合的全新类药小分子。(5) 设计出高特异性的放射肿瘤治疗计划。(6) 在异构变量类型（文本、代码、分子、计划）上以单一类 PyTorch API
工作，且无需逐任务调框架——用户只需提供目标函数。

#### 局限与挑战

**局限与挑战**
optimizer_quality（高度依赖一个强的反向/optimizer LLM——代码在 optimizer「无法遵循指令」时显式警告 IndexError 并建议「using a stronger
model」）；在未见数据上的回归风险（由 val 回滚缓解但未消除——会过拟合 dev 划分）；成本/可扩展性（每一步 = 多次前向 + 反向 LLM 调用；计算图深度会倍增反向调用）；eval-hacking
风险（LLM-as-judge 的 loss 可能被冗长/长度利用型输出钻空子）；单一优化提示的跨模型迁移性无保证；无灾难性遗忘概念（无状态变量）但也无持久记忆；doc_bloat 未被专门处理，但优化后的提示可能跨步骤无界增长。

#### 可借鉴要点

**可借鉴要点**
- 1. 把 Prompts/SKILL.md 当作可学习参数——在计算图内把 SKILL.md 包装为一个 requires_grad=True 的 Variable；agent 执行的每一步都是一个可微的「Function」，含前向（运行）与反向（反思）。这是「反思 = 反向」的概念源头：agent 的自然语言自我批评本身就是文本梯度。
- 2. 反向即反思，且 optimizer/target 分离——用一个强且独立的「反向引擎」（可以是同一模型的 critic 模式，或更强的 judge）读取执行轨迹 + 结果，并对 SKILL.md 的每个可编辑组件发出自然语言梯度（「做 X 的指令是错的，因为……改成……」），然后一步 TGD 风格的 optimizer 重写该段。批评经链式法则按变量（按段）局部化，而非一次全局重写。
- 3. 留出验证门控 + 贪心回滚（run_validation_revert）作为实用的安全网——每次 SKILL.md 编辑后，在留出的 dev 任务 batch 上重新评估，若准确率/回归下降则回滚该编辑；外加 gradient_memory + momentum 让编辑器保持稳定。三者合起来给出一个即插即用、PyTorch 风味的「autograd for skills」循环：前向=运行，loss=LLM-judge+执行，反向=逐段批评，optimizer=有界重写，gate=dev-split 回滚。

---

### GEPA

> `idea_text_opt` · Agrawal et al., 2025。Reflective textual evolution 的 Genetic-Pareto 优化器：反射→ 精炼模式，从发展集选候选系统并优化 prompt。证明比标量奖励 RL 更样本高效；Pareto 前沿 选择保留多样候选，比 TextGrad 贪心爬山收敛更快。是 EvoSkill/SkillSmith 的直接母体。 openreview RQm2

#### 基础信息

**名称**
GEPA (Genetic-Pareto)

**提出机构**
UC Berkeley、Stanford、BespokeLabs.ai、Notre
Dame、Databricks、MIT（Agrawal、Tan、Soylu、Ziems、Khare、Opsahl-Ong、Singhvi、Shandilya、Ryan、Jiang、Potts、Sen、Dimakis、Stoica、Klein、Zaharia、Khattab）

**发布时间**
2025；以 conference paper 发表于 ICLR 2026

**论文链接**
https://openreview.net/pdf?id=RQm2KQTM5r

**代码链接**
https://github.com/gepa-ai/gepa

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示。GEPA 仅进化复合 AI 系统 Phi=(M,C,X,Y) 的模块提示集合 Pi_Phi；底层 LLM 权重 Theta_Phi 保持冻结。每个语言模块 M_i=(pi_i, theta_i, X_i, Y_i)
的系统提示 pi_i（指令 + 可选 few-shot 示范）被变异；控制流 C 与工具 API 不被触碰。

**技能是否独立制品**
是。每个候选提示都是一个独立、可复用的文本制品（一个完整实例化的 <Pi, Theta_frozen> 系统版本），存放在候选池 P 中并带有显式血缘记录（父-子边构成遗传树/DAG）。候选项被序列化、比较并作为一等对象进行重组。

**是否文档载体**
是。优化后的制品本质上是一份人类可读的自然语言指令文档（声明式规则、目的/上下文、分步策略、输出格式——见图 2）。提示自身不内嵌可执行代码；该「技能」完全以类 markdown 指令文本的形式喂给 LLM 模块。

#### 技能表示

**技能编码方式**
自然语言 SOP 编码为系统提示（声明式指令 + 可选 few-shot 示范）。GEPA 学到的提示是丰富的声明式文档：输入理解、目的/上下文、关键观察与经验教训、构建策略、输出规范（图 2）。不是代码、不是向量、不是图谱——每个模块都是纯指令文本。

**技能粒度**
子任务 workflow + 策略规则。粒度为复合 AI 系统中的模块级：每个模块的提示是一条子任务 workflow 指令（如第二跳查询生成、答案抽取）。进化出的内容编码高层声明式策略规则/经验（如「第一跳文档通常覆盖单一实体；目标是缺失的关联文档」），而非原子动作。

#### SKILL.md_专属维度

**文档形态**
纯指令文档（声明式自然语言指令，无 YAML frontmatter，无内嵌可执行代码块）。典型长度：种子提示为 1-2 行（约 30 tokens）；GEPA 进化后的提示增长为数百到约 1k+ tokens
的结构化散文，含若干区段（Input Understanding、Purpose/Context、Key Observations/Lessons、How-to-Build、Output）。形式为每个模块一整块扁平的指令，而非多文件包。

**编辑粒度**
每个模块每次变异为整文档重写（reflection LM 输出一个完整修订后的提示 pi_i，而非 patch/diff）。两种提案策略：(1) Reflective Prompt Mutation——单亲重写并累积经验；(2)
System-Aware Merge（GEPA+Merge）——遗传交叉，合并来自两个祖先的互补模块级提示（一种跨模块的 bundle-like 联合编辑）。无 minimal-diff/PATCH 编辑。

**版本与门控**
Pareto 前沿 + 留出验证门控。多级门控：(a) 先做 minibatch 评估；仅当分数超过父代时，(b) 再做完整 D_pareto 验证评估；仅当候选有改进时才加入池 P。下一次变异的选择采用 Pareto 前沿过滤（保留在
>=1 个任务实例上最优的候选，剪除严格被支配者），并以 #tasks-led 为权重的随机采样。血缘 DAG 记录谱系；Merge 跳过直系血缘与已尝试过的配对。

**文档来源**
由执行 + 评估轨迹经 LLM 迭代生成。来源信号：(1) 人工初始化的种子提示（简单基线）；(2) rollout 执行轨迹（模块输入/输出/推理）；(3) 评估轨迹（编译错误、失败的 rubric 项、经反馈函数 mu_f
的人工评分解释）；(4) LLM 的反思式归因。非一次性生成——而是从众多失败/成功轨迹中迭代蒸馏而来。

**跨载体迁移**
跨模型 + 跨基准。跨模型迁移强：在弱模型 Qwen3-8B 上优化的提示（'GEPA-Qwen-Opt'）原样在 GPT-4.1-Mini 上评估时获得 +9pp，击败直接在 GPT-4.1-Mini 上优化的基线。跨基准：同一
optimizer 应用于 6 个多样的基准（AIME-2025、LiveBench-Math、HotpotQA、IFBench、HoVer、PUPA）。推理期搜索内的跨任务迁移（一个 kernel 问题的经验应用到其他问题）。

**技能库治理**
Pareto 剪枝 = 被支配候选的退役（类似于按实例的 Lotka-Volterra 适者生存）；血缘 DAG 防止冗余的 Merge 尝试（血缘条件跳过直系血缘与先前尝试过的配对）；无显式的基于相似度的去重、无分层索引、无 curator loop。池规模由 Pareto 支配剪枝隐式约束。

**失败记忆**
是，强烈。失败信号是一等公民：执行轨迹（失败的推理/工具调用）与评估轨迹（编译错误、失败的 rubric 项、人工评分的理由）被 mu_f 捕获为 feedback_text，并喂入 reflection meta-prompt
以做显式信用归因。候选自身的血缘累积经验。被拒绝的候选（在 minibatch 上未超过父代）被丢弃——它们不会喂入持久的 anti-pattern buffer，但其轨迹为下一次 reflection 提供信息。

**编辑安全**
通过两阶段验证门控（minibatch -> 完整 D_pareto）实现有界编辑，确保仅超过父代的改进被提交；留出验证集（验证实例内容对 optimizer 不可见）；预算上限 B 约束总 rollout
数；范围限于提示（权重、控制流、工具源码不被触碰）；对抗/探测模式通过奖励反转实现（PUPA/AIME 对抗搜索）。无显式人工在环、无编辑前备份/回滚、未记录 eval-hacking 防御（系统原则上可能过拟合验证集的特殊性——图 15
分析了泛化差距）。

**协同进化**
skill-prompt 联合（一个复合 AI 系统内的多模块联合提示进化）。GEPA 同时进化全部 |M| 个模块的提示（轮询式模块选择），System-Aware Merge
对来自不同祖先的模块提示做交叉。Generator-verifier 风格：reflection LM 充当目标系统的 meta-optimizer。非 skill-tool 协同进化（工具冻结），非 skill-skill
生态（单一系统，无独立技能库）。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（文本空间、非梯度）与 population_evolutionary（遗传算法：变异 + 交叉 + Pareto 选择）以及 reward-based 文本反馈相结合。具体地：(1)
Reflective Prompt Mutation = 利用来自 rollout 的自然语言反馈做 LLM reflect-and-refine；(2) System-Aware Merge = 对 Pareto
最优祖先做遗传交叉；(3) 基于 Pareto 的「illumination」候选选择（quality-diversity，参见 Mouret & Clune 2015）。无梯度更新、无 SFT、无 RL
策略梯度——学习完全发生在语言空间。

**学习信号来源**
成败轨迹（推理/工具调用的执行轨迹）+ 评估轨迹（经 mu_f 的编译/rubric/人工评分反馈）+ 留出验证分（D_pareto 留出分）+ LLM-as-judge（reflection LM 归因信用并提出更新）。辅助信号：可用时每个实例附人工撰写的解释。

**奖励粒度**
hybrid。Outcome：用于选择的标量指标 mu（exact match / F1 / pass rate）。Process：来自 mu_f 的文本 feedback_text（编译错误、rubric 失败、多跳中的模块级反馈），用于反思式学习。

**学习范式**
offline + on-policy。优化是部署前在 D_train 上的离线 sleep-time 阶段（inter-test-time）。采样相对当前候选为 on-policy（rollout 从正被变异的候选中抽取）。存在一个在线推理期搜索的变体（D_val = D_train，过拟合目标任务）。

#### 进化时机_When

**进化时机 (When)**
inter-test-time（部署前在 D_train 上的离线优化循环，受 rollout 预算 B 约束）。次要模式：推理期搜索（查询时按任务过拟合，用于 NPUEval/KernelBench 上的代码优化）。非 intra-test-time 的单任务执行期在线适配。

**触发方式**
周期性 / budget-driven 迭代（循环持续「While Budget > 0」）。无事件/失败/课程触发；optimizer 运行至预算耗尽。当池中存在两个共享共同祖先、互补的 Pareto 最优候选时，条件性触发 Merge。

#### 存储与检索

**技能库结构**
候选池 P = 带血缘 DAG 的 Pareto 前沿。每个节点 = 一个具体的 <Pi, Theta_frozen> 实例化，带父边与每任务分数矩阵（行=候选，列=任务实例）。过滤后的池仅保留非支配候选。无向量库、无分层索引、无云端注册中心、无 git 分支——内存中的遗传树。

**检索/复用方式**
基于 Pareto 的随机采样：从过滤后（非支配）的池中，按其领先的任务实例数为权重采样候选。对变异目标模块：轮询策略。对 Merge：采样 2 个具有有效血缘的不同候选。非语义相似度、非 BM25——按任务覆盖度加权的采样。

#### 验证与反馈

**验证方式**
基于执行（rollout 由 mu 打分）+ 留出评估（D_pareto 留出验证集，内容对 optimizer 不可见）+ 验证门控（两阶段：minibatch 后完整 D_pareto；仅当有改进才提交）+ 功能正确性（每个基准的
exact match / F1 / pass rate）。reflection LM 充当代理验证器，提出属性级信用归因。

**错误纠正**
有界编辑（经 minibatch 门控提交的有界编辑）+ 定向 diff 修补（reflection LM 输出定向修订，将失败归因到具体提示元素）+ 回滚（被拒候选直接丢弃，保留父代）。除提出新子代外，无对已提交候选的显式自我修订；遗传结构本身就是纠错记忆。

#### 环境与基座

**测试环境**
通用 NLP reasoning + coding。六个基准：多跳
QA（HotpotQA）、数学（AIME-2025、LiveBench-Math）、指令遵循（IFBench）、隐私感知委派（PUPA）、检索增强验证（HoVer）。作为推理期搜索扩展到 coding（NPUEval AMD NPU
kernel、KernelBench CUDA kernel）。在 AIME-2025 上的对抗提示搜索。

**底座模型**
开源 LLM（Qwen3-8B）与专有 GPT-4.1 Mini 作为 TARGET 系统骨干（权重冻结）。optimizer/target 分离：一个 reflection LM（同族、通常更强）充当提出提示变异的
meta-optimizer。推理期搜索使用 GPT-4o。对抗探测使用 GPT-5 Mini。无 VLM。

**部署域 (Where)**
general（通用复合 AI workflow：QA、数学、指令遵循、验证、隐私委派、代码生成）。非专门面向单一领域。

#### 评估指标

**评估指标**
success_rate（每基准测试集分数）+ sample_efficiency（达到 GRPO 最佳验证所需的 rollout；仅训练 rollout）+ 泛化（留出测试集，跨模型 GEPA-Qwen-Opt ->
GPT-4.1-Mini）+ 成本（附录 G.3 报告的金钱成本）+ generalization_gap（验证-测试差，图 15）。

**关键结论**
在 Qwen3-8B 上，GEPA 以平均 +6pp、最高 +19pp 击败 GRPO（24k rollout），且最多使用 35 倍更少的 rollout（达到最优测试性能少 4-35 倍）；以 78 倍更高的样本效率匹配 GRPO
的最佳验证（仅需 243-1179 个 rollout）。聚合上击败 MIPROv2 +13pp（对比 MIPROv2 的 +5.6pp），在 AIME-2025 上 +12pp。在 GPT-4.1-Mini 上，击败
TextGrad（+12.19pp 对 +6.11pp）、Trace/OptoPrime、MIPROv2。跨模型：Qwen 优化的提示在 GPT-4.1-Mini 上获 +9pp。Pareto 选择击败
SelectBestCandidate +6.4pp、击败 BeamSearch +7.33pp（表 3）。推理期搜索：NPUEval 平均向量利用率 4.25% -> 30.52%；KernelBench 超越 PyTorch 的
CUDA 从约 0% 提升到 >20%。

#### 局限与挑战

**局限与挑战**
optimizer_quality（依赖强 reflection LM 提出好的变异；更弱的 optimizer 会退化）。regression_risk（在 AIME-2025 上用 Qwen3-8B 时，GEPA 不及
GRPO；IFBench 上 GEPA+Merge 相对 GEPA 出现回归）。scalability（多数 rollout 预算花在验证/选择而非学习上——仅训练 rollout 为 79-737，但完整 pipeline
需要数千）。doc_bloat（进化后的提示变长；无压缩）。transferability（强但在任务/模型间有差异）。controllability（无人工在环；无显式 eval-hacking
防御——提示可能过拟合验证集的特殊性，尽管泛化差距很小）。

#### 可借鉴要点

**可借鉴要点**
- Pareto 前沿版本管理胜过贪婪爬山：维护一个非支配候选 SKILL.md 版本的池（每个至少在某一任务实例 / 用户 / 场景上最优），而非始终编辑单一全局最优。按覆盖度为权重随机采样下一次变异目标。这逃离了困住 TextGrad 式贪婪单最优编辑的局部最优——GEPA 显示相对 SelectBestCandidate +6.4pp、相对 BeamSearch +7.33pp。对 SKILL.md 自我进化：保留多份竞争草稿，仅剪除严格被支配者，让多样场景保留多样的胜者存活。
- 用执行 + 评估双轨迹做 reflect-and-refine：喂给 meta-prompt 的不仅是（当前提示、标量分数），而是完整序列化轨迹（agent 的推理、工具调用、工具输出）以及评估轨迹（编译错误、失败的 rubric 项、人工评分理由），作为 feedback_text。reflection LM 执行隐式信用归因并输出整文档重写。这比标量奖励 RL 的样本效率高得多（比 GRPO 少 4-35 倍 rollout），因为语言是比稀疏标量梯度更丰富的学习介质。对 SKILL.md：记录执行轨迹 + 结构化评估反馈，让 LLM 提出归因到具体失败模式的完整重写。
- 两阶段留出验证门控作为廉价安全保障：每个提案编辑先在 minibatch 上评估，仅当它在留出 D_pareto 验证集（内容对 optimizer 不可见）上超过父代时才晋升入候选池。这在无需人工审查的情况下约束回归风险——被拒编辑直接丢弃，保留父代。配合硬 rollout/时间预算 B 以防失控。对 SKILL.md：保留一个自我编辑器读不到的留出评估集，每次提交都在其上做门控，在子代可证明胜出之前绝不覆写父代。

---

### OPRO / PromptBreeder / EvoPrompt

> `idea_text_opt` · LLM-as-optimizer 三部曲。OPRO(Yang, Google, ICLR 2024)：LLM 用自然语言描述+评分 迭代优化 prompt。PromptBreeder(Meta)：prompt 作为可进化种群，用 mutation operators 自我进化「进化策略」。EvoPrompt：遗传算法/DE 思想演化 prompt。共同点：把 prompt/ 指令当作可进化文本基因

#### 基础信息

**名称**
OPRO / PromptBreeder / EvoPrompt (LLM-as-optimizer trilogy)

**提出机构**
OPRO: Google DeepMind (Yang, Wang, Lu, Liu, Le, Zhou, Chen)。PromptBreeder: Google DeepMind (Fernando, Banarse,
Michalewski, Osindero, Rocktaschel)。EvoPrompt: Microsoft Research + Tsinghua University (Guo, Wang, J.Guo, Li, Song,
Tan, G.Liu, Bian, Y.Yang)。

**发布时间**
三者均为 2023 年 9 月: OPRO arXiv:2309.03409 (2023-09-07; v3 2024-04-15); PromptBreeder arXiv:2309.16797 (2023-09-28);
EvoPrompt arXiv:2309.08532 (2023-09-15; v3 2025-05-01)。OPRO 与 EvoPrompt 均发表于 ICLR 2024; PromptBreeder 发表于 ICML 2024
(PMLR v235 fernando24a)。

**论文链接**
OPRO: https://arxiv.org/abs/2309.03409 ; PromptBreeder: https://arxiv.org/abs/2309.16797 ; EvoPrompt: https://arxiv.org/abs/2309.08532

**代码链接**
OPRO 官方: https://github.com/google-deepmind/opro ; EvoPrompt 官方: https://github.com/beeevita/EvoPrompt (镜像于
microsoft/EvoPrompt) ; PromptBreeder: 无官方发布, 仅社区实现 (如 vaughanlove/PromptBreeder)。

**类型**
academic (three peer-reviewed papers, ICLR 2024 x2 + ICML 2024)

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示。三者都仅进化施加于冻结 LLM 之上的自然语言 instruction/prompt 文本; 模型权重 Theta、工具与 agent 架构均不动。OPRO 优化单一 instruction 字符串,
前置/后置于任务输入 (Q_begin/Q_end/A_begin)。PromptBreeder 进化 task-prompts 的 POPULATION, 且独特地进化决定 task-prompts 如何变异的
mutation-prompts。EvoPrompt 通过 GA 或 DE 算子(经 LLM 调用实例化)进化离散 prompts 的种群。三者的优化变量都是文本, 而非参数。

**技能是否独立制品**
是 (partial)。每个候选 prompt/instruction 都是独立的、可复用的文本制品, 可作为一等对象被序列化、打分、比较与重组。OPRO 维护一个 (prompt, score) 对的轨迹列表; PromptBreeder
维护显式的「进化单元」= {task-prompts, mutation-prompt, 可选 few-shot context} 并带有谱系; EvoPrompt 维护一个带 fitness 的 prompt 染色体种群。然而,
三者都不把 prompt 视作具库治理的长生命、具名、版本化的 SKILL 文档——制品是一段短 instruction 字符串, 而非多区段技能文件。

**是否文档载体**
是。被进化的对象本质上是人类可读的自然语言 instruction 文本。被进化的制品中不内嵌任何可执行代码; 「技能」是纯声明式指令。典型进化出的 prompts 为 1-3 个短句 (OPRO 的「Take a deep breath
and work on this problem step-by-step.」; PromptBreeder 的 GSM8K 胜者「SOLUTION」或更长的多规则 prompts; EvoPrompt 的 instruction
模板)。并非结构化的 markdown/SKILL.md 文档——只是扁平的 instruction blob。这是奠基性范式: instruction = 可进化文本基因, 早于将 SKILL.md 整文档进化的做法。

#### 技能表示

**技能编码方式**
自然语言 SOP 被编码为 instruction 字符串 (声明式句子), 前置/后置于任务输入。PromptBreeder 额外编码 (a) mutation-prompts = 描述如何变异 task-prompt 的自然语言指令,
(b) thinking-styles = 自然语言认知启发式描述, (c) few-shot context = 存储的正确 workings-out。EvoPrompt 将 prompts 编码为离散文本染色体 (手写或 APE
生成的种子)。无向量嵌入、无图谱、无代码——全程纯文本。

**技能粒度**
策略规则 (每个制品一条策略级指令/规则)。比完整技能包更细, 比原子动作更粗。PromptBreeder 的单元捆绑了少量协同进化的规则 (2 个 task-prompts + 1 个 mutation-prompt + few-shot
示例), 接近最小的「技能包」; OPRO 与 EvoPrompt 每个候选进化单一整体 instruction。

#### SKILL.md_专属维度

**文档形态**
纯指令 (pure instruction 文本, 无 YAML frontmatter, 无内嵌可执行代码块)。典型 token 长度短: OPRO 指令 ~5-25 tokens (如「Take a deep breath and
work on this problem step-by-step.」~10 tokens), 而 OPRO meta-prompt 自身达到数百 tokens (20 个最佳 instruction-score 对 + 3 个任务样本 +
meta-instructions)。PromptBreeder 的 task-prompts 从单词 (「SOLUTION」) 到多子句规则 (~50-150 tokens); mutation-prompts 是短祈使句 (~10-30
tokens)。EvoPrompt prompts 为模板式指令 (~20-100 tokens)。无一达到数 KB 的 SKILL.md 规模。

**编辑粒度**
整文档重写 (每次变异整体重写指令; 无 PATCH/diff)。OPRO: optimizer LLM 每步发出一条全新的 instruction 字符串, 以过去 (prompt, score)
对的轨迹为条件——明确地不是在编辑单条输入 prompt。PromptBreeder: 每次复制施加 9 个 mutation 算子之一 (均匀采样), 通过 LLM 续写产出全新 task-prompt 或
mutation-prompt; Prompt Crossover (变异后 10% 概率) 用来自 fitness-proportionate-selected 同侪的一条替换某个
task-prompt——一种捆绑式联合编辑。EvoPrompt(GA): 双亲 crossover + mutation, 二者均实现为来自模板 (template_ga) 的 LLM 生成重写; EvoPrompt(DE): 三亲
donor (a + F(b-c)) 随后与目标 x 做二项 crossover, 全部表达为 LLM 指令 (template_de)。三者均无 minimal-diff 编辑。

**版本与门控**
留出验证门控 (held-out development set) + greedy/top-k 选择。OPRO: 每步在小训练子集上对 8 条新指令打分 (GSM8K 3.5%, BBH 20%); meta-prompt
仅保留按训练准确率排序的前 20 条轨迹; 最终最优 prompt 由训练准确率选出并在留出测试集上评估。PromptBreeder: binary-tournament GA——采样 2 个单元, 变异更优者, 覆写失败者;
fitness = 在每次评估时新鲜采样的随机 100-Q&A 批上的准确率 (随机重采样提供隐式留出); elite 谱系历史按单元保留。EvoPrompt(GA): 每代后按 development-set 分保留 top-N
prompts; EvoPrompt(DE): 一对一替换——新 prompt p' 仅当在 development set 上得分更高时才替换 p。无 Pareto 前沿, 无 git branching, 无 DAG 血统版本化, 无
human-in-the-loop。

**文档来源**
LLM 迭代生成 from execution + evaluation traces, 由人工初始化作为种子。OPRO: 从人工种子 (如「Let's solve the problem.」或空字符串) 出发, 通过以分排序轨迹为条件的
optimizer LLM 迭代重写。PromptBreeder: 从 (problem-description D, 采样的 thinking-style T, 采样的 mutation-prompt M) 的随机组合中播种出初始
task-prompts; 随后经 9 个 mutation 算子跨代进化。EvoPrompt: 从手写 prompts 与/或 APE 生成 prompts (prompts.txt, prompts_auto.txt)
初始化种群。三者均迭代地从 fitness 反馈中提炼改进, 而非一次性生成。

**跨载体迁移**
跨任务 + 跨模型 (within-benchmark 且横跨 LLM)。OPRO: 在 GSM8K 上优化的指令迁移到 MultiArith 与 AQuA; OPRO 还展示了 cross-optimizer 迁移 (PaLM
2-L-IT vs gpt-3.5-turbo vs gpt-4 找到的 prompts 风格各异但都能提升 scorer); cross-scorer 迁移亦被研究。PromptBreeder: 同一系统适配算术 (GSM8K,
MultiArith, SingleEq, AddSub, SVAMP, AQuA-RAT)、常识 (SQA, CSQA)、instruction induction (APE tasks) 与仇恨言论分类 (ETHOS)——一种通用机制,
多个领域。EvoPrompt: 在跨语言理解、生成与 BBH 的 31 个数据集上优化; 报告了 cross-LLM (GPT-3.5 <-> Alpaca)。三者均未涉及 cross-agent-harness
(Claude/Codex/Cursor) 或 cross-user/team 迁移。

**技能库治理**
Minimal。OPRO: 通过保留 top-20 实现隐式去重 (低质 prompts 从轨迹中淘汰); 无显式基于相似度的去重, 无分层索引, 无 curator loop。PromptBreeder: EDA mutation
算子施加 BERT-embedding 余弦相似度过滤 (>0.95 相似度被剪枝) 以维持种群多样性——一种 quality-diversity 式 curator; 无 retirement/archival,
除固定种群规模外无库增长上限。EvoPrompt: 固定种群规模配合 top-N (GA) 或一对一替换 (DE) 隐式地约束增长; 无相似度去重。三者均未实现 Lotka-Volterra、分层索引或显式的 dust-cleaning
loops。

**失败记忆**
弱 / 隐式。OPRO: 低分 prompts 留在轨迹中 (升序排序) 以便 optimizer LLM 看到什么无效——一种软 anti-pattern 信号, 但无显式 failure-signature buffer;
被拒候选并未被隔离为负反馈存储。PromptBreeder: lineage-based mutation 算子暴露按时间的 elite 历史 (bad->good 梯度), 隐式编码了失败恢复; Lamarckian 算子从成功的
workings-out 反向工程 task-prompts (仅正向信号); 无 anti-pattern 存储。EvoPrompt: 被拒后代被直接丢弃; 无 rejected-edit buffer。三者均未维护显式的
failure-signature+attribution+remedy memory。

**编辑安全**
Minimal——这些是研究原型, 而非生产级编辑器。范围: 编辑局限于 prompt 文本字符串 (模型权重、源码、工具不动)——一种隐式范围边界。有界编辑: PromptBreeder 的 binary-tournament GA 与
EvoPrompt(DE) 的「仅当更好时替换」提供隐式 bounded-edit 安全性 (回归者被丢弃); OPRO 的 top-20 保留同理。留出评估集 (OPRO 测试集, PromptBreeder 随机批 fitness,
EvoPrompt development set) 充当软验证门控。无编辑前备份/回滚, 无显式 eval-hacking 防御 (OPRO Section 5.4 明确分析了对训练子集 idiosyncrasies 的过拟合), 无
human-in-the-loop, 无 secret/注入检查, 无限定到特定文件的范围约束 (完全无文件系统交互——纯文本优化)。

**协同进化**
skill-prompt 联合 (仅 PromptBreeder) / skill-only (OPRO, EvoPrompt)。PromptBreeder 是突出者: 它在自指循环中将 task-prompts 与
mutation-prompts (生成策略的策略) 协同进化——这是「进化那个进化 SKILL.md 的 SKILL.md」最接近的先例。OPRO 仅进化任务指令 (单基因); meta-prompt
结构为手工设计并冻结。EvoPrompt 仅进化 task prompts; GA/DE 算子模板 (template_ga.py, template_de.py) 冻结。三者均不与外部工具或独立的 generator-verifier
对协同进化 (LLM 既是 generator 又是 mutation 算子)。

#### 自进化机制_How

**进化方法范式 (How)**
population_evolutionary + rollout_optimization (文本空间, non-gradient) + reward-based 文本反馈。无梯度, 无 SFT, 无 RL policy
更新——所有学习发生在语言空间。OPRO: 黑盒文本空间 optimizer——optimizer LLM 从包含优化轨迹 (过往 solutions + 分数, 升序排序) 的 meta-prompt 生成新的候选 solutions;
每步多条 solutions (8) 配合调过的采样温度 (默认 1.0) 以平衡探索-利用; 可证明地通用 (线性回归、TSP、prompt 优化)。PromptBreeder: 完整的 binary-tournament GENETIC
ALGORITHM (Harvey 2011), 跨 5 类共 9 个 mutation 算子——(1) Direct Mutation [zero-order prompt generation, first-order prompt
generation], (2) Estimation-of-Distribution Mutation [EDA mutation, EDA rank/index mutation, lineage-based mutation],
(3) Hyper-Mutation [zero-order hyper-mutation, first-order hyper-mutation]——该类变异 mutation-prompts 自身 = evolvability 的进化,
(4) Lamarckian Mutation [working-out -> task-prompt 从成功表型反向工程], (5) Prompt Crossover (变异后 10%, fitness-proportionate 同侪)
+ Context Shuffling; 每次复制对 9 个算子均匀随机选择。EvoPrompt: 通过 LLM 调用实例化两种经典 EAs——EvoPrompt(GA): selection
(wheel/random/tournament) -> crossover (LLM template_ga) -> mutation (LLM template_ga) -> 保留 top-N; EvoPrompt(DE): 变异向量
y = a + F(b-c) 实现为 LLM 指令, 与目标 x 二项 crossover, greedy 替换。共同主线: prompt/instruction = 可进化文本基因, LLM = optimization/mutation
算子。

**学习信号来源**
环境奖励 (训练/dev 集上的任务准确率) 在三者中都是主导信号。OPRO: scorer-LLM 贪婪解码在训练子集 (GSM8K 3.5% / BBH 20%) 上的准确率。PromptBreeder: fitness =
每次评估时从完整训练集抽出的随机 100-Q&A 批上的任务准确率 (随机重采样提供类似课程的效果)。EvoPrompt: development-set 指标 (分类用 accuracy, 生成用 BLEU/ROUGE, BBH 用
exact-match)。无 LLM-as-judge 作为奖励 (LLM 是 optimizer 而非 judge——奖励来自 ground-truth 任务标签)。无 self-reflection 作为学习信号
(PromptBreeder 的 Lamarckian 算子使用成功 workings-out, 但仅为正向)。无显式 failure attribution。

**奖励粒度**
outcome (结果级)。三者均优化每个候选 prompt 的单一标量任务准确率 (或任务指标) 分数。OPRO 或 EvoPrompt 中无 process 级奖励分解。PromptBreeder 的
Lamarckian「working-out -> task-prompt」算子使用中间推理轨迹 (一种准 process 信号), 但仅来自成功 rollout; 选择信号本身是 outcome 级准确率。

**学习范式**
offline + on-policy。三者均作为部署前在固定 train/dev 集上的离线优化循环运行 (inter-test-time / sleep-time 风格); 任务执行期间无在线适配。采样相对当前候选种群为
on-policy (每条新 prompt 从当前种群状态生成并据此评估)。PromptBreeder 每次评估的随机批重采样引入了轻微 off-policy 味道 (fitness 跨代在不同批上估计)。

#### 进化时机_When

**进化时机 (When)**
inter-test-time (部署前的离线优化阶段)。三者都是批量优化过程, 运行至收敛 (或步数/时间预算) 后输出单条最优 prompt (或种群) 供下游使用。非 intra-test-time——优化后的 prompt
在任务执行期间冻结。非 sleep-time 调度——优化由实践者显式启动, 而非由空闲周期或 cron 触发。

**触发方式**
周期性 / budget-driven 迭代。OPRO: 循环持续直至「LLM 无法提出更优优化分的 solutions, 或达到最大优化步数」——convergence-or-budget 终止。PromptBreeder: 运行固定代数
n (CLI 参数)。EvoPrompt: 固定迭代/代数。无事件触发 (无失败触发的再进化, 无课程驱动触发, 无 usage 驱动触发, 无工具退化触发)。进化是一次性离线批作业, 而非持续生命周期——这与后来的 SKILL.md
self-evolution 工作(其中进化由任务结果在环触发)形成关键对比。

#### 存储与检索

**技能库结构**
内存中种群/轨迹, 无持久库。OPRO: (prompt, score) 对的轨迹列表 (升序排序, 保留 top-20)——实质是扁平排行榜, 无向量 DB, 无文件系统。PromptBreeder: 固定规模的「进化单元」种群 (每个
= task-prompts + mutation-prompt + few-shot context) 带按单元的 elite 谱系历史——扁平种群带隐式谱系边, 无 DAG 持久化。EvoPrompt: 固定规模的 prompt
染色体种群 (size = init popsize 参数), 无谱系追踪, 无分层索引。三者均不使用 git branches、云端注册中心、图谱或持久技能文件目录——「库」是进程局部列表, 优化结束即消亡。

**检索/复用方式**
从种群中按分数加权 / fitness-proportionate 采样 (非语义相似度, 非 generation-as-retrieval)。OPRO: meta-prompt 显式包含分排序轨迹, 使 optimizer LLM
关注高分模式; 本质无采样, 完整 top-20 被呈现。PromptBreeder: binary tournament 采样 2 个随机单元并选更优者; EDA mutation 对多样性过滤后的种群采样; Prompt
Crossover 使用 fitness-proportionate (roulette) 选择。EvoPrompt: selection mode 参数——「wheel」(fitness-proportionate,
默认)、「random」、「tour」(tournament)。无 BM25, 无嵌入检索, 无 description-match 触发——种群足够小, 可穷举扫描。

#### 验证与反馈

**验证方式**
execution-based (任务上的 rollout) + 留出评估 (held-out test set 仅用于最终报告, 优化期间不用) + 功能正确性 (exact-match / accuracy / BLEU)。OPRO:
scorer LLM 在优化期间对训练子集贪婪解码答案; 测试准确率仅在优化后报告; Section 5.4 有过拟合分析。PromptBreeder: fitness = 随机 100-Q&A 批上的准确率 (每次评估重采样);
留出测试在优化后报告。EvoPrompt: optimization 期间用 development set 做选择; 留出 test set 优化后报告。无 LLM-judge, 无 surrogate verifier, 无多模型辩论,
无带 reject-and-retry 的验证门控——全程简单的 score-then-select。

**错误纠正**
有界编辑 (经种群级选择的 bounded edits——坏候选直接不被选中, 亲本保留) + 定向 diff 修补 (PromptBreeder 的 first-order hyper-mutation「Please summarize
and improve the following instruction」是对 mutation-prompt 的定向修订; PromptBreeder 的 lineage-based mutation 提供显式的 bad->good
梯度供跟随)。无对已提交候选的 self-revision (种群即记忆)。无回滚 (无已提交状态可回滚——一切都在种群中)。无重规划。OPRO 与 EvoPrompt 缺乏显式 error correction——它们纯粹依赖
generate-and-select。

#### 环境与基座

**测试环境**
通用 NLP 推理 + 分类 + 生成。OPRO: GSM8K (小学数学)、Big-Bench Hard (23 tasks)、MultiArith、AQuA, 加上动机性的线性回归与 TSP 研究。PromptBreeder: 算术推理
(GSM8K, MultiArith, SingleEq, AddSub, SVAMP, AQuA-RAT)、常识推理 (SportsQA, CommonsenseQA)、仇恨言论分类 (ETHOS)、APE
instruction-induction tasks (23 个子任务)。EvoPrompt: 31 个数据集——语言理解 (分类)、生成 (摘要、翻译)、BBH。无 coding agent, 无 GUI, 无 Minecraft,
无工具使用环境——这些是纯 NLP 基准。

**底座模型**
闭源 + 开源 LLM 作为冻结 scorer; optimizer/target 分离。OPRO: optimizer LLM = PaLM 2-L, PaLM 2-L-IT, text-bison, gpt-3.5-turbo,
gpt-4; scorer LLM = 预训练 PaLM 2-L, text-bison (optimizer 与 scorer 可不同)。PromptBreeder: PaLM 2-L 同时充当 optimizer 与
scorer。EvoPrompt: GPT-3.5 (闭源) 与 Alpaca (开源) 作为 target scorer; GPT-3.5 作为进化算子 LLM。无 VLM, 无任何 backbone 的 fine-tuning。

**部署域 (Where)**
general (通用 NLP 推理: 数学、常识、分类、生成、instruction induction)。非专门用于 coding/GUI/office。该范式可泛化——作者将其定位为通用 prompt optimizer——但实证范围限于 NLP 基准。

#### 评估指标

**评估指标**
success_rate (每个基准的 test 准确率) 是三者的主指标。OPRO 另含: optimization-convergence 曲线 (逐步最优/平均训练准确率带 std-dev 阴影)、transferability
(GSM8K-optimized -> MultiArith/AQuA)、对 meta-prompt 组件的消融 (#exemplars, #trajectory-prompts, temperature)。PromptBreeder: 在
8 个算术+常识基准上 vs CoT / Plan-and-Solve / APE / OPRO 的跨方法比较; 按算子消融 (Appendix J.4); 进化出的 mutation-prompt 质量分析。EvoPrompt: 跨 31
个数据集 vs APE / human prompts 比较 (BBH 高达 +25%)、GA-vs-DE 消融、GPT-3.5-vs-Alpaca 消融。无技能库增长指标 (无持久库)。无经济价值指标。无
sample-efficiency-vs-RL 基线 (那要等后来的 GEPA)。

**关键结论**
OPRO (PaLM 2-L scorer): GSM8K 80.2% zero-shot (用「Take a deep breath and work on this problem step-by-step.」, PaLM 2-L-IT
optimizer) vs 人工「Let's think step by step」的 71.8% (+8.4pp); 在 BBH 上相对人工 prompts 提升高达 +50%; GSM8K->MultiArith/AQuA
迁移。PromptBreeder (PaLM 2-L): GSM8K 83.9% zero-shot (vs OPRO 的 80.2%), 使用出乎意料地极简的 prompt「SOLUTION」; 在算术 (MultiArith 99.7,
SingleEq 96.4, AddSub 87.8, SVAMP 90.2) 与常识 (SQA 71.8, CSQA 85.4, AQuA-RAT 62.2) 上击败 CoT、Plan-and-Solve、APE; 在 ETHOS
上进化出复杂的仇恨言论分类器。EvoPrompt: 在 BBH 上相对人工工程 prompts 高达 +25%; 跨 31 个数据集优于 APE 与其他自动 prompt 生成基线; 展示 GA/DE 与 LLM 的协同; GPT-3.5
与 Alpaca 均受益。集体意义: 确立了 LLM 可充当自然语言 instruction 上的文本空间 optimizer, 奠定了后来的 SKILL.md self-evolution
所继承的「prompt-as-evolvable-gene」范式。

#### 局限与挑战

**局限与挑战**
optimizer_quality (三者都依赖一个强 LLM 充当 optimizer/mutator——OPRO 的 gpt-4 在 TSP 上轻松击败 gpt-3.5-turbo 与 text-bison; 较弱 optimizer
停滞)。scalability (OPRO 的 context-window 上限使大规模优化困难——高维数据的线性回归与大 TSP 实例失败; PromptBreeder 的大量 rollout 代价高——论文提到批量化/线程化
mutation 为工程工作)。eval-hacking / 过拟合 (OPRO Section 5.4 明确分析了对训练子集 idiosyncrasies 的过拟合; 语义相似的 prompts 可产生差异巨大的准确率——一种
optimizer 可能 latch 上去的噪声底)。regression_risk (EvoPrompt GA 的 top-N 与 DE 的 replace-only-if-better 约束了这一点,
但无形式化保证)。transferability (cross-task/cross-model 迁移已展示但波动)。doc_bloat (PromptBreeder 进化出的 prompts 可能变冗长; OPRO 与 EvoPrompt
较少)。controllability (三者均无 human-in-the-loop; optimizer 的创作方向不透明)。catastrophic_forgetting (N/A——无权重更新)。

#### 可借鉴要点

**可借鉴要点**
- META-PROMPT = OPTIMIZATION TRAJECTORY (OPRO 的核心可复用思想): 与其让 LLM「帮我编辑这条 prompt」, 不如向 LLM 呈现过往候选 (prompt, score) 对的完整分排序历史外加少量任务样本, 并要求它生成得分更高的新候选。轨迹本身承载了梯度——LLM 在好例 vs 坏例上执行 in-context 模式识别。这是 prompt 优化文献中被复制最多的设计选择, 并直接映射到 SKILL.md self-evolution: 维护一个 (SKILL.md 草稿, eval 分) 的版本化历史, 在提出下一稿时将整条轨迹喂给 meta-LLM, 而非孤立编辑。OPRO 在仅 3.5% 训练子集上的实证胜利 (GSM8K 34% 空字符串 -> 80.2%) 证明, 一段带分注释的轨迹是极为样本高效的学习媒介。
- CO-EVOLVE THE MUTATION OPERATOR, NOT JUST THE ARTIFACT (PromptBreeder 的自指 hyper-mutation): PromptBreeder 相对 OPRO/EvoPrompt 的决定性创新在于, 它不仅进化 task-prompts, 还进化决定 task-prompts 如何变异的 mutation-prompts (first-order hyper-mutation: 「Please summarize and improve the following instruction」)。这是「evolvability 的进化」——系统改进了它自我改进的方式。对 SKILL.md self-evolution 而言, 这是最深刻可借鉴的思想: 在 SKILL.md 草稿之外, 维护一个不断进化的小型 EDIT STRATEGIES 池 (如「压缩失败处理区段」、「为最棘手的步骤加一个 worked example」、「重写触发条件以更具体」), 并让 meta-LLM 基于哪些策略产出了获胜草稿而周期性地精炼这些编辑策略。PromptBreeder 的 9 个 mutation 算子 (direct、EDA、hyper-、Lamarckian、crossover+context-shuffle) 是任何 SKILL.md 进化者都可采纳的具体起始分类法——尤其是从成功轨迹反向工程出 prompt 的 Lamarckian 算子, 它直接翻译为「从一条成功任务轨迹蒸馏出一次 SKILL.md 修订」。
- POPULATION + DIVERSITY MAINTENANCE BEATS GREEDY HILL-CLIMBING (EvoPrompt + PromptBreeder 共识): EvoPrompt 表明 GA (种群 + crossover + top-N) 与 DE (种群 + 3 亲 donor + greedy 替换) 均胜过单线程 optimizer; PromptBreeder 在其 EDA 算子中通过 BERT-cosine-similarity 过滤 (>0.95 剪枝) 与随机批 fitness 重采样添加了显式多样性维护。给 SKILL.md self-evolution 的启示: 维护一个竞争草稿的 POPULATION (而非单一正典版本), 按相似度剪枝以避免 mode collapse, 并使用 binary-tournament 或 fitness-proportionate 选择, 使多样的 niche 获胜者 (在不同任务类型 / 用户画像上最优) 共存。EvoPrompt 的 DE 模板 (y = a + F(b-c)) 也值得试点: 让 meta-LLM 产出一份草稿, 把一个强亲本「a」与另外两个亲本「b」「c」之间缩放后的「差」结合——一种出奇有效的向量算术的文本空间类比。

---

### ExpeL

> `idea_distill` · THU LeapLab, AAAI 2024(arXiv:2308.10144)。从成败轨迹蒸馏可复用 NL 见解/规则，带 重要性计数(ADD/UPVOTE/DOWNVOTE/EDIT，降至0裁剪)；成功轨迹存 Faiss 向量库做 RAG。 思想可迁移到 SKILL.md 的「见解沉淀+裁剪治理」。github LeapLabTHU/ExpeL

#### 基础信息

**名称**
ExpeL (Experiential Learning agent)

**提出机构**
清华大学、LeapLab（THU）。作者：Andrew Zhao、Daniel Huang、Quentin Xu、Matthieu Lin、Yong-Jin Liu、Gao
Huang（通讯作者）。受国家重点研发计划（2022ZD0114900）、国家自然科学基金（62022048, U2336214, 62332019）及清华大学国强研究院资助。

**发布时间**
arXiv v1 提交于 2023-08-20；v2 2023-12-18；v3 2024-12-20。被 AAAI-24（第 38 届 AAAI 人工智能会议）录用。[Oral 身份据 task note；具体 session 未验证]

**论文链接**
https://arxiv.org/abs/2308.10144

**代码链接**
https://github.com/LeapLabTHU/ExpeL（项目主页：https://andrewzh112.github.io/expel）

**类型**
academic (AAAI-24 paper). Model weights never trained; method is purely prompt/experience-based and runs on closed-source API LLMs.

#### 进化对象_What

**进化对象 (What)**
仅 Context记忆与提示。Agent 的 context 经以下内容增强：(a) 由抽取出的自然语言 insight 拼接而成的列表，以及 (b) 检索得到的 top-k 成功轨迹，作为 in-context fewshot
示例。无模型权重更新（显式面向 GPT-4/Claude 等 API-only 模型设计）、无工具进化、无架构改动。论文将其类比为从经验池中行为策略（behavior policy）轨迹进行的 off-policy 学习。

**技能是否独立制品**
是。两个可复用的非参数制品：(1) 一组 NL insight（每条带一个整数 importance count），充当可迁移规则；(2) 一个由成功轨迹构成的 Faiss 向量库，可作为 fewshot 示范复用。形式 = memory
entries / NL 规则 + 向量索引的轨迹，而非磁盘上的 .md/SKILL.md 文件。用户可检查/修改/移除 insight（相对于 finetuning 被解读为一种优势）。

**是否文档载体**
是（偏向）。主要载体是注入提示的可读自然语言 insight 规则；不含内嵌可执行代码。它在精神上是「指令文档中心」的（NL SOP 规则），尽管字面载体是内存中的 insight 列表而非磁盘上的 markdown 文件。故：形式上是（NL 指令），字面的磁盘 SKILL.md 打包方式上是否。

#### 技能表示

**技能编码方式**
自然语言SOP/见解（NL insight 规则，每条是一条简短准则，如「考虑答案可能已在已做出的 observations 中」）+ 向量嵌入（以 all-mpnet-base-v2 嵌入的成功轨迹构成的 Faiss
向量库）。insight 以 NL 文本形式存储，并带有一个整数 importance-count 侧状态；轨迹以原始文本 + 稠密嵌入形式存储。

**技能粒度**
见解（insight）/ 策略规则。处于策略规则层面的原子化 NL 准则（小于完整技能包，大于单个动作）：例如跨任务最佳实践与常见失败模式规避规则。轨迹是作为 fewshot 示范使用的完整子任务 workflow。

#### SKILL.md_专属维度

**文档形态**
形式 = 一份扁平的 NL insight 字符串列表，每条带一个整数 importance count；推理时将完整列表拼接（ι̂ = concat(ι1,ι2,...)）并前置于任务说明（图 3 的 prompt 模板）。insight
受 LLM context window 容量约束（论文明确指出「抽取的 insight 不超过当前 LLM token 上限」）；终身学习范式将需要 insight 检索（被列为 future work）。无 YAML
frontmatter，无 markdown 文件，无多文件包。典型单条 insight 长度 = 1-3 句；典型列表规模 = [uncertain，每个环境约数十条 insight 量级]。

**编辑粒度**
有界增删替换，通过对 insight 集合施以四种原子操作实现：ADD（新 insight，初始 importance count=2）、EDIT（重写既有 insight
的内容）、UPVOTE（同意，+1）、DOWNVOTE（不同意，-1）。无整文档重写，无 PATCH/diff 格式；每次抽取步骤对每条 insight 施加一个操作。轨迹库通过仅追加地吸收整条轨迹而增长（不编辑轨迹）。

**版本与门控**
仅基于计数的隐式门控：当某条 insight 的 importance count 降到 0 时（被 DOWNVOTE 主导）自动剪枝。无 held-out 验证门控，无 git 分支前沿，无 Pareto/DAG 谱系，无人工评审门控，无
staging+backup。importance count 充当一个基于投票的软流行度门控；对单条 insight 没有独立的 held-out 打分步骤（仅端到端的 4 折任务 success_rate 验证整个库）。

**文档来源**
成功轨迹归纳 + 失败轨迹蒸馏 + 执行录像回放 + session 经验提取。insight 离线地从经验池中抽取的两个对比源蒸馏而来：(a) 同一任务的成对成功/失败（失败轨迹蒸馏），以及 (b) 来自不同任务的 L
条成功片段（成功轨迹归纳 / 最佳实践模式挖掘）。轨迹通过试错自主采集，并在失败时以 Reflexion 式自我反思重试（每个训练任务最多 Z 次重试）。

**跨载体迁移**
跨任务 + 跨基准（已验证）。HotpotQA（源）-> FEVER（目标）的正向迁移：源域 insight 通过一个用少量目标任务示范来适配它们的 prompt 模板被「finetune」到目标域（图 4）。带任务示范的 agent
优于不带示范的。跨模型（原则上声称：「不限于特定语言模型」；并展示 gpt-4 extractor > gpt-3.5 extractor）。跨 agent-harness / 跨 user：未验证（它是研究型 agent，而非可移植
harness 的制品）。

**技能库治理**
importance-count 退役（count->0 剪枝某条 insight）+ 轨迹上的 Faiss 向量索引。这是核心治理机制：一个简单、自清洁、有界增长的规则库，由抽取期间的 UPVOTE/DOWNVOTE
投票驱动。无对语义相似 insight 的显式去重/合并，无 curator loop，无 Lotka-Volterra 动力学，无分层索引（insight 列表是扁平的；对 insight 的检索被明确列为 future
work）。轨迹库单调增长（不退役轨迹）。

**失败记忆**
是（对比对形式）。失败轨迹并不作为独立的 anti-pattern 存储；而是把每个失败与同一任务上的一次成功配对，送入 LLM_insights 以抽取/修订那些编码「常见失败模式」与纠正性最佳实践的 insight（prompt
明确强调「抽取常见的失败模式或最佳实践」）。DOWNVOTE 充当负反馈，退役有误导性的 insight。无显式的失败签名+归因+补救结构化，也无 rejected-edit buffer；负向信号被折叠进 insight 的投票计数。

**编辑安全**
可解释性 + 用户可编辑性 + 有界增长（count 剪枝）。论文明确把 NL insight/轨迹定位为可由用户检查/修改/移除（相对于 finetuned
权重是一种安全性/可控性优势）。有界的编辑算子（ADD/EDIT/UP/DOWN）防止破坏性的整库重写。无编辑前 backup/rollback，无显式的 eval-hacking 防护（insight 抽取与评估之间无 held-out
划分），无密钥/注入扫描，无人工在环门控，无作用域边界强制（insight 是纯文本，故源码作用域无从谈起）。

**协同进化**
skill-only，带有角色分离。单一 agent 的 context（insight + 检索到的轨迹）是唯一进化的东西；工具（Wikipedia Docstore API、WebShop/ALFWorld
动作空间）固定，无其他技能协同进化，无独立的验证器协同进化。不过 LLM 之间确实存在清晰的角色分离：LLM_ReAct（policy/actor，gpt-3.5-turbo）、LLM_reflect（Reflexion
反思器）、LLM_insights（extractor，gpt-4-0613）——一种软性的 generator/extractor 分工，但不是协同进化循环。

#### 自进化机制_How

**进化方法范式 (How)**
reward-based（来自二元成败结果的文本反馈）+ imitation_demonstration（将检索到的成功轨迹作为 fewshot in-context 示范注入）。不是对权重的 gradient/SFT/RL，不是
population-evolutionary，不是 prompt-tuning 意义上的 rollout-optimization。论文中最接近的框架是「从行为策略的经验池进行 off-policy
学习」，完全在文本/提示空间实现。insight 抽取是针对对比轨迹对的一个 LLM 驱动的抽象步骤。

**学习信号来源**
成败轨迹（来自环境的成功/失败轨迹结果）+ 自我反思（采集期间 Reflexion 式 LLM_reflect 输出）。环境为每条轨迹提供一个确定性的二元成功信号；insight 通过比较同一任务上的成功与失败、并在成功轨迹间进行模式挖掘而导出。

**奖励粒度**
outcome（结果）。每条轨迹二元成功/失败（HotpotQA/FEVER 为 exact-match，ALFWorld 为任务完成，WebShop 为全部属性匹配）。无 process/step 级 reward；无密集
reward。WebShop 额外报告 [0,1] 区间的平均 reward r 作为软 outcome 指标。

**学习范式**
offline + off-policy。一个独立的离线 TRAINING 阶段（在训练任务上采集轨迹 -> 抽取 insight -> 构建向量库）先于一个单次 EVALUATION 阶段（部署时无重试）。off-policy：agent
从行为策略产生的轨迹（包括失败尝试与 Reflexion 重试尝试）中学习，类似于 replay-buffer 学习。非 online，非 on-policy，非 sleep-time 调度（尽管离线训练阶段在概念上与 sleep-time
兼容）。

#### 进化时机_When

**进化时机 (When)**
inter-test-time（任务间离线）。insight 抽取与库构建发生一次、离线进行，位于训练任务经验采集与评估任务部署之间——明确不在测试期的单个任务内进行（部署为单次，无重试，无在线学习）。论文将其与 Reflexion 的 intra-task 基于重试的改进作对比。

**触发方式**
事件触发（在经验采集循环跑完 N 个训练任务之后）+ 失败触发（采集期间每训练任务最多 Z 次 Reflexion 重试，由任务失败触发）。它是一个一次性的批训练触发器，非周期性/cron，非课程驱动，部署时也非用量驱动。

#### 存储与检索

**技能库结构**
向量库（由成功轨迹构成的 Faiss 向量库）+ 扁平 insight list（一组带 importance count 的扁平、无序 NL insight）。无层级，无 git 分支，无 DAG 谱系，无云端注册中心。经验池 B
保存全部轨迹（成功+失败）用于 insight 抽取；仅成功轨迹在 Faiss 中建立索引以供检索。

**检索/复用方式**
语义相似度（Faiss kNN，使用 all-mpnet-base-v2 嵌入器；按评估任务与已存成功轨迹之间的最大内积任务相似度排序；top-k 作为 fewshot in-context 示例检索出）。对 insight：无检索——完整
insight 列表被拼接进 prompt；论文明确将 insight 检索标记为终身学习的 future work。消融显示：任务相似度排序 > 原因相似度排序 > 随机采样。

#### 验证与反馈

**验证方式**
执行验证（execution-based）+ 留出评估（在基准上做 4 折交叉验证，报告 mean+std）。无针对单条 insight 的 LLM-judge 门控，无代理验证器，无决定某条 insight
是否被采纳的验证门控（采纳仅由抽取期间的 importance-count 投票决定）。insight 仅通过端到端任务 success_rate
提升来间接验证。功能正确性指标：exact-match（HotpotQA/FEVER）、任务完成（ALFWorld）、属性匹配（WebShop）。

**错误纠正**
自我修订 + 定向 diff 修补（insight 级的 EDIT 操作重写有误导性的 insight；DOWNVOTE 通过计数衰减使其退役；采集期间的 Reflexion 自我反思为下一次重试产出纠正性反思）。无
rollback（一旦加入的 insight 不可回退，只能被投下去）、无整库重写、部署时无重规划（单次）。推理时观测到涌现的自我纠正行为：agent 在轨迹中途撤销错误动作（如在 ALFWorld 中放回拿错的物体）。

#### 环境与基座

**测试环境**
通用 / Web + tool-call + text-GUI。HotpotQA（经 Wikipedia Docstore 搜索 API 的多跳
QA）、ALFWorld（基于文本的家务具身任务）、WebShop（基于文本的在线购物多步决策）、FEVER（事实验证，迁移目标）。四个均为遵循 ReAct benchmark 套件的文本观测确定性环境。

**底座模型**
GPT（闭源）。Policy/actor = gpt-3.5-turbo-0613（所有 agent 含基线在评估时均用此模型，temperature 0，贪心）。insight extractor LLM_insights =
gpt-4-0613（消融显示 gpt-4 > gpt-3.5-turbo，在遵循 ADD/EDIT/UPVOTE/DOWNVOTE 操作指令方面更好且幻觉更少）。Reflector LLM_reflect =
同一家族。Optimizer（extractor）与 target（policy）是分离的，并使用不同模型档位。Embedder = all-mpnet-base-v2（Song et al. 2020），用于 Faiss 检索。

**部署域 (Where)**
general（通用）。横跨多样决策领域测试（QA、具身家务、网页购物、事实验证）；不专精于单一垂直领域。该方法在设计上是领域无关的（任何带二元成功信号的 ReAct 式任务）。

#### 评估指标

**评估指标**
success_rate（主指标，4 折 mean+std-error）+ generalization（跨任务正向迁移 HotpotQA->FEVER）+ sample_efficiency（消融：采集经验的数量/多样性对下游 SR
的影响）+ skill_library_growth（隐式：insight 集合规模与投票动态）。附加：WebShop 的 [0,1] 区间平均 reward r、ALFWorld 的按任务类型拆分。无显式的成本/token 经济指标。

**关键结论**
主结果（图 5）：ExpeL 在全部三个领域上一致地胜过 ReAct 与 Act。HotpotQA SR：ExpeL 39% vs ReAct 28.0 +/-1.4（仅 insight 36% / 仅检索 31% ->
协同）。ALFWorld SR：ExpeL 59%（仅 insight 50% / 仅检索 55%）。WebShop：insight/检索接近均衡（37%/38% SR，0.675/0.67 reward）。在无重试下匹敌/胜过
Reflexion R3（HotpotQA 39% vs Reflexion R3 40%；ALFWorld 59% vs Reflexion R3 54%）。消融：(1) 经验数量+多样性重要（仅 fewshot = 相对 ReAct
无增益；Reflexion 采集 > ReAct 采集）；(2) 学到的 insight > 手工 insight（39% vs 32%）；(3) 将 Reflexion 反思加入 insight 抽取会变差（29%，幻觉）；(4)
gpt-4 extractor > gpt-3.5-turbo extractor；(5) 任务相似度检索 > 原因相似度 > 随机。迁移：HotpotQA->FEVER
正向迁移为正，带目标任务示范时更大（「finetuning」）。涌现能力：分析性演绎、世界模型信念更新（如 ALFWorld 中 pan 现已在 stoveburners 上搜索过）、轨迹中途自我纠正。

#### 局限与挑战

**局限与挑战**
迁移性（仅测试了 HotpotQA->FEVER 迁移；WebShop SR 接近 Reflexion 范围的下端）+ optimizer_quality（依赖强 insight-extractor LLM；gpt-4 明显优于
gpt-3.5-turbo）+ 可扩展性/doc_bloat（insight 必须装入 context window；终身/长程学习需要 insight 检索，明确列为 future work）+ 模态（仅文本观测；无 VLM/图像支持）+
闭源依赖（API-only LLM；开源 LLM 变体未探索）+ 可控性/理论（基于 prompting，缺乏 RL 的理论基础）。无灾难性遗忘风险（权重冻结）。无显式 eval-hacking 防护（insight 抽取与最终评估之间无
held-out 划分）。

#### 可借鉴要点

**可借鉴要点**
(1) 基于 importance-count 的 insight 沉淀 + count 归零自动剪枝，作为库治理：每条 SKILL.md 规则带一个整数投票计数，配四种原子操作（ADD 时 count=2 / UPVOTE +1 /
DOWNVOTE -1 / EDIT 重写），并在计数归 0 时自动退役。这给出一个简单、自清洁、有界增长、完全可解释的规则库，从对比的成功/失败对中学习，而无需任何 held-out 验证门控或人工评审——可直接移植到 SKILL.md
治理。(2) 两种相互协同、互补的记忆模式：抽象出的 NL insight（泛化，在 HotpotQA 这类推理任务上占主导）+ 一个由过去成功轨迹构成、作为 fewshot 示范检索的 Faiss 向量库（模仿，在 ALFWorld
这类执行密集任务上占主导）。一个自我进化的 SKILL.md 系统应同时维护两者：文档中的蒸馏规则，以及一个可检索的成功运行记录归档，并按任务类型选择平衡。(3) 离线跨任务经验采集（带 Reflexion 重试）->
对比的成功/失败对驱动 insight 抽取 -> 单次部署、无重试：把一个专门的离线「学习 session」（采集经验、抽取/修订
insight）与快速的单次推理部署分离；不要在面向用户的任务中在线学习。加上一条廉价但影响深远的经验：即便部署的策略是更便宜的模型（gpt-3.5），也用更强的 LLM（gpt-4）作为离线 insight EXTRACTOR。

#### 不确定字段

- release_date（AAAI-24 oral/poster 身份——task note 称为 Oral；arXiv 日期已确认但会议 session 未验证）
- doc_form（每个环境下抽取 insight 集合的确切典型 token 长度 / 列表规模——论文未报告计数）

---

### Agent Workflow Memory (AWM)

> `idea_distill` · CMU+MIT, ICML 2025(arXiv:2409.07429)。归纳模块从经验轨迹提取通用子例程(workflow) 文本块，抽象掉示例特有上下文，注入提示记忆。在线(流式测试从成功轨迹归纳)+离线两种。 仅~40 示例即见效。思想≈「把验证过的行动链固化为可复用文档」。github zorazrw/ agent-workflow-memory

#### 基础信息

**名称**
Agent Workflow Memory (AWM)

**提出机构**
Carnegie Mellon University (CMU) + Massachusetts Institute of Technology (MIT)。作者：Zora Zhiruo Wang、Jiayuan Mao (MIT)、Daniel Fried、Graham Neubig (CMU)。

**发布时间**
2024-09-11 (arXiv v1)；发表于 ICML 2025 (Poster)，PMLR 267:63897-63911。

**论文链接**
https://arxiv.org/abs/2409.07429

**代码链接**
https://github.com/zorazrw/agent-workflow-memory

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示。workflow 是从经验轨迹归纳出的文本块，并被整合进 agent 的 prompt/context 记忆（system prompt 或辅助 context）。无模型权重更新、无工具/动作空间创建、无架构变更。纯非参数化的 in-context 记忆进化。

**技能是否独立制品**
是。每个 workflow 是一个独立、可复用的文本制品，存储在扁平的 workflow memory 中。形式 = 一个文本块，配对 (1) 自然语言 workflow 描述（目标/子目标摘要）与 (2)
一个有序的步骤轨迹，其中每个步骤包含自然语言环境状态描述、自然语言推理，以及一个可执行动作程序（如 click('42')、fill('130','{RepositoryName}')）。workflow 以双换行符分段并分别存储。

**是否文档载体**
混合。workflow 是一份人类可读的指令文档（自然语言目标 + 状态 + 推理），其中嵌入了可执行的动作代码调用。它相当于一个 mini-SOP，其动作层是对环境执行的可执行程序。主要载体是可读的指令文本并辅以动作代码，因此更偏向「文档式技能」而非纯代码或纯向量。

#### 技能表示

**技能编码方式**
自然语言 SOP（子例程风格），内嵌可执行动作程序。一个 workflow = 自然语言描述 + 步骤列表 [(自然语言状态, 自然语言推理, 动作程序), ...]。基于 LM 的归纳模块通过单次 prompt 通路产出这些内容；输出被分段为独立的 workflow 文本块。不是向量嵌入、不是图、不是多文件包。

**技能粒度**
子任务 workflow（可复用子例程）。workflow 被有意提取得比完整任务指令更细粒度（如「在 Amazon 上搜索商品」而非「买干猫粮……」）。每个 workflow 有 >=2 个步骤。新的复杂 workflow 由更早的原始 workflow 组合而成（如「按名称找一个地方」->「获取一个地方的邮编」）。

#### SKILL.md_专属维度

**文档形态**
指令 + 内嵌代码块（混合）。每个 workflow 是一个结构化文本块：标题行（## domain: workflow_name）+ 自然语言目标描述 + 编号/分段的步骤列表。每个步骤混合 (a) 自然语言环境状态描述、(b)
自然语言推理/依据、(c) 可执行动作程序调用。具体值被抽象为描述性变量名（{product-name}、{RepositoryName}）。典型长度：每个 workflow 若干步骤（约 2-5 步）。每个网站的 workflow
数量较少（WebArena 上约 7.4，Mind2Web 上约 7.3）。记忆是扁平的（无 YAML frontmatter、无多文件打包）。

**编辑粒度**
整段生成 + 仅追加（append-only）的添加。LM 归纳模块在单次 prompt 中从一个或多个经验生成整个 workflow；归纳出的 workflow 被追加到扁平记忆（M + W）中。无有界
add/delete/replace diff、无 PATCH、无破坏性编辑、无原地重写。复杂 workflow 在更早的 workflow 之上组合式地构建（snowball），但每个新 workflow
是一个全新生成的制品，而非对既有制品的编辑。

**版本与门控**
最小。(1) 在线模式：一个 LM-evaluator（Pan et al. 2024 AutoEval）输出二元成功标签；仅被判为成功的轨迹才被转化为 workflow（成功门控的归纳）。(2) 离线模式：workflow
从金标准标注的训练样本归纳（假定正确）。无 held-out 验证、无 Pareto 前沿选择、无 git 分支、无 DAG lineage、无暂存+备份、无人工 review 门控、无回滚。一个 workflow
一旦被添加，就永不被版本化或回退。

**文档来源**
两种模式。离线 = 从标注训练样本归纳成功/金标准轨迹（离线 benchmark 训练）。在线 = 从流式测试会话中抽取的自生成成功轨迹（会话经验抽取）。两种情况下来源都是成功的动作轨迹；归纳 LM 抽象掉样本特定的 context。非人工初始化、非执行视频回放、非社区共享。

**跨载体迁移**
在 benchmark 内部明确评估了跨任务、跨网站与跨领域迁移（Mind2Web 跨任务/网站/领域划分；WebArena 跨模板子集）。随着训练-测试分布差距增大，在线 AWM 泛化更好（+8.9 至 +14.0
绝对分）。未演示跨模型迁移（仅使用 GPT-3.5/GPT-4），也未演示跨 agent harness 迁移。workflow 按 website 作用域划分（按网站记忆），因此跨完全不同站点的迁移有限；当领域差距较大时离线 AWM
性能下降。

**技能库治理**
最小 / 软去重。扁平的按网站 workflow 记忆（一个网站的所有 workflow 共存）。归纳 prompt 指示「不要生成相似或重叠的 workflow」，这是唯一的去重机制。论文将 function-overlap
作为质量指标度量（WebArena 上 0.08，Mind2Web 上 0.20），但不执行主动合并/淘汰/归档。无 Lotka-Volterra 动态、无 curator loop、无层级索引、无淘汰策略。技能库增长无界（仅追加）。

**失败记忆**
无显式 anti-pattern / 失败记忆。失败仅通过排除来处理：不成功的轨迹不被归纳为 workflow（在线模式下被 LM-evaluator 成功门控过滤）。失败被丢弃而非保留；无失败特征库、无归因/补救 buffer、无
rejected-edit buffer、无否决未来相似 workflow 的负反馈。论文承认在线 AWM 仍可能从被误判的自轨迹中归纳出错误 workflow。

**编辑安全**
最小/无。无范围边界强制（workflow 是文本而非源码，故不存在 .md 与代码的分离问题）、无编辑前备份或回滚、无 anti-eval-hacking
措施、无确认门控、无人工在环、无有界编辑保护（仅追加是唯一的结构性保障）。唯一门控是在线模式下 LM-evaluator 的二元成功判定。仅追加记忆带来的 context-length 溢出风险未被主动防护。

**协同进化**
skill-only（带有弱的涌现 skill-skill 效应）。workflow 独立进化；工具/动作空间固定（内置 CLICK、TYPE、FILL 等）且从不创建或修改。LM evaluator 是一个固定的外部模块（无
generator-verifier 协同进化）。存在一个涌现的组合效应（新的复杂 workflow 建立在更早的简单 workflow 之上），但这不是结构化的 skill-skill 协同进化机制。

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration + 非梯度文本空间 rollout 优化。LM 归纳模块将成功轨迹泛化为可复用的文本 workflow（对成功的抽象模仿）。无 reward-based
RL、无梯度/SFT、无种群/进化搜索。它最好被刻画为基于 LM 的经验泛化为文本记忆 prompt 增强（agent context 的非梯度、文本空间优化）。

**学习信号来源**
成功/失败轨迹（二元）。离线：金标准标注的规范样本（假定正确）。在线：一个 LM-as-judge evaluator（AutoEval，Pan et al. 2024）对自生成轨迹输出二元成功标签。无环境 reward shaping、无自我反思、无 held-out 验证分、无任务成功之外的工具成功指标。

**奖励粒度**
outcome（结果级）。成功判定在整条轨迹/任务级别（轨迹是否解决了指令？），而非逐步骤的 process reward。

**学习范式**
离线与在线兼具。离线 = 在推理前从训练样本归纳（off-policy、类 sleep-time）。在线 = 在流式测试查询期间从 agent 自生成的成功轨迹归纳（on-policy、inter-test-time）。非基于梯度；纯 prompt/context 空间。

#### 进化时机_When

**进化时机 (When)**
两者皆有。离线 = sleep-time / inter-test-time（在服务测试查询前从训练样本一次性归纳）。在线 = inter-test-time（在完成一个流式测试任务并判定成功后，归纳 workflow(s)
并在下一个任务前加入记忆）。非 intra-test-time（单个任务执行过程中不发生归纳）。

**触发方式**
事件触发（成功后）+ 课程驱动。在线：每个测试任务完成后，若被判为成功，则归纳 workflow(s)。涌现出 snowball/课程效应：越来越复杂的 workflow 建立在更早归纳的 workflow
之上（如「找一个地方」使能「获取一个地方的邮编」）。非周期/cron、非失败触发（失败不触发归纳）、非使用驱动的检索。离线：对每个网站的所有训练样本做一次性批量归纳。

#### 存储与检索

**技能库结构**
扁平的、按网站的 workflow 记忆。给定网站的所有归纳 workflow 被拼接到 agent 的辅助记忆/context 中。无层级、无向量库、无图/DAG lineage、无云端注册中心。论文显式地按网站对样本分组，以保持每个局部 workflow 集合小而相关。

**检索/复用方式**
无 / 全 context 注入（不使用 generation-as-retrieval）。AWM 将为相关网站归纳的所有 workflow 加载到该网站上每个测试任务的 prompt 中；无逐查询语义相似度检索、无
BM25+embedding 重排、无 workflow 匹配。唯一的作用域划分是网站级分组。这是与 Synapse/ExpeL 等基于检索的样本方法的刻意对比。（摘要中「selectively providing
workflows」一语指网站级选择，而非逐查询检索。）

#### 验证与反馈

**验证方式**
LLM-judge（在线）+ 金标准假设（离线）。在线：LM-evaluator（AutoEval）提供一个二元成功门控，决定一条轨迹是否有资格被蒸馏为 workflow。WebArena 另外提供基于执行的功能正确性评估用于报告。无对归纳
workflow 本身的 held-out 验证门控、无成功判定之外的代理 verifier、无多模型辩论。workflow 质量事后通过 #workflows、coverage、function-overlap 与
utility-rate 指标评估。

**错误纠正**
有限 / 归纳时过滤。错误通过排除处理：仅成功轨迹被蒸馏，故噪声在上游被过滤。一个 workflow 一旦被归纳，就永不被修订、回滚、diff-patch 或有界编辑。论文指出在线 AWM 仍可能注入错误
workflow（当自预测轨迹被误判为成功时），且 agent 有时难以偏离 workflow 指导（action F1 略低于 MindAct）。

#### 环境与基座

**测试环境**
Web 导航（WebArena + Mind2Web）。WebArena：5 个网站上 812 个基于执行的任务（电商/CMS/Reddit/GitLab/Maps）。Mind2Web：跨 200+ 领域的任务/网站/领域划分。

**底座模型**
GPT（闭源）。GPT-4 (gpt-4-0613) 与 GPT-3.5-turbo，temperature 0.0。同一模型同时用于 workflow 归纳与 agent 动作生成（无 optimizer/target 分离）。纯文本输入（accessibility-tree 网页表示）；无视觉语言模型。

**部署域 (Where)**
Specialized（Web 导航 / 数字 GUI agent 领域）。通用 Web 任务（旅行、购物、社交媒体、开发协作、内容管理）。

#### 评估指标

**评估指标**
success_rate（任务级与步骤级 SR、元素准确率、action F1）；泛化（跨任务 / 跨网站 / 跨领域 / 跨模板）；样本效率（从约 40 个样本中快速学习）；skill_library_growth（workflow
数量、coverage、function-overlap、utility rate）；成本（每个成功任务的平均步数）。

**关键结论**
WebArena：35.5% 总 SR，对比 BrowserGym_ax-tree 23.5%（+12.0 绝对、+51.1% 相对）以及对比 AutoEval 20.2%；在无任何人工监督下相对 SteP（14 个人工编写
workflow）领先 +7.6% 相对；每个成功任务的步数相比基线减少约 2.0（比 AutoEval 少约 40.8）。Mind2Web 跨任务：+24.6% 相对步骤 SR（AWM_4 步骤 SR 45.1 对比 MindAct
36.2）。跨模板子集：33.2% SR（仍为最佳）。在线 AWM 泛化：在跨任务/网站/领域上相对 MindAct +8.9 至 +14.0（最高 +16.9）绝对分，且随分布差距增大而优势扩大。样本效率：大部分增益在前约 40
个流式样本内获得。workflow 质量：每个网站约 7.4 个 workflow（WebArena），utility rate 0.94，function overlap 0.08。

#### 局限与挑战

**局限与挑战**
可迁移性（当训练-测试领域差距扩大时离线 AWM 性能下降；workflow 按 website 作用域划分）；回归风险 / optimizer 质量（在线 AWM 从模型预测轨迹归纳
workflow，这些轨迹「并非总是正确」，故被误判的成功会注入错误 workflow 从而降低性能）；doc_bloat / 可扩展性（仅追加的扁平记忆无淘汰；所有 workflow 加载进 context 且无检索，规模化时有
context 溢出风险）；可控性（当状态偏离时 agent 有时无法脱离 workflow 指导，降低 action F1）；单一闭源 backbone 家族（GPT-3.5/4）；纯文本观测（无视觉）；归纳与生成均依赖一个足够强的
LM。

#### 可借鉴要点

**可借鉴要点**
- 蒸馏技能时抽象掉样本特定的 context。AWM 的归纳 prompt 刻意用描述性变量名替换具体值（如「干猫粮」-> '{product-name}'），并提取比完整任务指令更细的子例程。这使得一个技能可跨许多任务复用，并在经验上胜过检索具体的整轨迹样本（Synapse）：+5.0 元素准确率、+4.0 步骤 SR。对 SKILL.md 的启示：将技能写成泛化、参数化的 SOP，而非字面记录。
- 在提交技能前用二元成功判定为自进化设门控。在无监督的在线模式下，LM-evaluator 判定每条轨迹成功/失败，仅成功者被蒸馏进记忆。这是一个廉价、免标签的质量门控，使 agent 能从自身验证的胜利中自主增长其 SKILL.md，同时过滤大部分噪声。（他们注明的告诫：判定器可能出错，故仍有少量不良技能混入。）
- 通过仅追加的组合式记忆实现 snowball。AWM 从不破坏性地编辑 workflow；它只追加新的，后续复杂 workflow 通过组合更早的原始 workflow 构建（「找一个地方」->「获取一个地方的邮编」）。这产生了课程效应，带来快速的早期增益（约 40 个样本）。启示：对于自进化的 SKILL.md，优先选择非破坏性地追加新的、可组合的技能，而非有风险的原地重写，从而使能力累积而不发生回归。
- 全 context 注入在小规模下胜过检索但无法扩展。AWM 将每个网站全部（约 7 个）workflow 加载进 prompt 而不使用检索，仍然获胜。这表明对于一个规模小、作用域明确的 SKILL.md 库，简单的全 context 加载即可；但仅追加、不去重、无淘汰的设计是一个公认的可扩展性上限，未来的 SKILL.md 系统应通过检索 + 技能库治理来解决。

---

### MUSE (Learning on the job)

> `idea_distill` · 2025(arXiv:2510.08002)。层次化记忆 M={战略洞见, 过程层 SOP 文档(≈过程型 SKILL.md), 工具层动态指令}。Plan-Execute-Reflect-Memorize 循环。仅~10% 任务即累积记忆。SOP 文档 形态与 SKILL.md 高度同构。github KnowledgeXLab/MUSE

#### 基础信息

**名称**
MUSE (Memory-Utilizing and Self-Evolving)

**提出机构**
Central South University；Shanghai Artificial Intelligence Laboratory；Fudan University；Shanghai Innovation
Institute；Zhejiang University（通讯作者：Haifeng Li、Botian Shi）

**发布时间**
2025-10-09（arXiv v1）

**论文链接**
https://arxiv.org/abs/2510.08002

**代码链接**
https://github.com/KnowledgeXLab/MUSE

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context 记忆与提示。无模型权重更新、无微调；进化完全发生在一个层次化的自然语言 Memory Module M = {strategic, procedural, tool} 中，该模块注入 agent 的 system prompt 与观测流，从而扩展超越静态预训练参数的能力。

**技能是否独立制品**
是。记忆以独立的可复用 JSON 制品持久化（procedural_memory.json、strategic_memory.json、tool_memory.json），在启动时加载、每个任务后更新，并跨运行/迭代携带。形式：记忆条目 + SOP 文档（结构化自然语言），而非代码。

**是否文档载体**
是（结构上）。Procedural Memory 是一份可读的 SOP（'Standard Operating Procedure'）指令文档，含 preconditions/steps/notes，与过程化的 SKILL.md
同源；但它是用结构化 JSON 而非 markdown 编码的。Strategic Memory = Dilemma->Strategy 键值指导；Tool Memory =
description+instruction。因此精神上是「是」（以指令文档为中心），但以 JSON 序列化而非 .md 文件。

#### 技能表示

**技能编码方式**
自然语言 SOP（procedural：platform->{operation->{preconditions, steps 形如 'A -> B -> C', notes}}）+ 键值对（strategic：pattern_key ->
pattern+rationale）+ 结构化 JSON 字段（tool：tool_description / tool_instruction）。全部内容为 LLM 无关的自然语言；无向量嵌入，无可执行代码作为技能载体。

**技能粒度**
跨粒度的层次化：Strategic = 策略规则/insights（最多 10 条高层 resolution patterns）；Procedural = 子任务 workflow SOPs（按应用索引的多步操作指南）；Tool = 原子动作（单工具使用指导）。

#### SKILL.md_专属维度

**文档形态**
三个 JSON 文件。Procedural SOP = 嵌套 dict {<platform_or_application>: {<operation_name>: {preconditions, steps（'Open -> Select
-> Save -> Verify'）, notes}}}；启动时仅将一个轻量的 outline index 加载进 system prompt（dict_to_outline_str），完整内容按需经专用 memory
工具获取（索引/内容分离以尊重 context 上限）。Strategic = {<pattern_key>: '<pattern_statement + short rationale>'}，上限 10 条，全量加载进 system
prompt。Tool = {<tool_name>: {tool_description, tool_instruction}}，静态 description 在 system prompt 中 + 动态 instruction
在工具使用后追加到观测。纯自然语言指令内容（无内嵌代码块、无 YAML frontmatter）。典型 token 长度未报告；strategic 保持精简（<=10 条），procedural 索引保持轻量以避免
context-window 膨胀。

**编辑粒度**
有界增量更新 + 任务后全局精炼合并。Procedural memory 经 deep_update 更新（成功的子任务后立即对新 SOP 条目做有界 add/replace）；整个任务结束后，一个 LLM 'Merge Expert'
prompt 执行去重、平台规范化、操作聚类与整合。Strategic memory 先抽取再经 'Resolution Patterns Merge Expert' 合并，整合新+旧并强制 <=10 条的硬上限。非整文档重写、非
minimal-diff PATCH；最接近有界 add/delete/replace + merge 整合。

**版本与门控**
无 git-branch / DAG / Pareto / held-out 验证门控。质量门控为：(a) success-gated 蒸馏：只有经 Reflect Agent 验证为成功的子任务轨迹才被蒸馏进 Procedural
Memory；(b) 一个使用 3 轴 checklist 的独立验证器（Reflect Agent）充当采纳门控；(c) LLM-merge-expert prompt 执行去重 + size-cap 作为软治理。对 TAC 完整
benchmark，累积记忆在 3 轮持续学习后被冻结。无显式的编辑前 backup/rollback 或版本历史。

**文档来源**
主要是成功轨迹归纳（成功子任务轨迹经 Reflect Agent 蒸馏为 SOP）+ session 经验提取（任务后将困境蒸馏进 Strategic Memory、将工具用法蒸馏进 Tool Memory）。失败轨迹产出一份
session 内的 failure-cause-analysis 报告 R_fail 用于重规划（不直接写入持久化的 anti-pattern 存储）。无人工初始化；全自动生成。

**跨载体迁移**
跨模型 + 跨任务。记忆为自然语言且 LLM 无关：演示了由 Gemini-2.5-Flash 累积的记忆迁移到 DeepSeek-V3（S_partial 28.01%->36.75%），以及对未见 hard
任务的零样本泛化（23.65%->33.41%）和完整 175 任务 TAC benchmark。未测试跨 harness（Claude/Codex/Cursor）或跨用户/社区共享；全部评估在单一 TAC benchmark 内。

**技能库治理**
去重合并 + 灰尘清理（curator/merge-expert loop）+ 层次化索引 + size cap。merge_application_prompt 规范化平台名、按操作意图聚类、整合重复项、补充
preconditions/notes；merge_methodology_prompt 强制 strategic patterns 硬上限 10 条并合并重叠观点。层次化索引：platform -> operation ->
{preconditions, steps, notes}。无 retirement/archive/Lotka-Volterra/种群剪枝；procedural 增长除此以外无界（潜在膨胀风险）。

**失败记忆**
部分。失败时 Reflect Agent 产出一份 failure-cause-analysis 报告 R_fail 反馈给 PE Agent 用于重规划（session 内负反馈），summarize prompt 也捕获
'Reflections on Failures' 教训；retry 路径额外禁用 procedural-memory 检索以强制新颖探索（一种隐式的 anti-overfitting-to-bad-skill 机制）。但没有专用的持久化
anti-pattern / rejected-edit buffer / failure-signature 存储作为结构化记忆跨运行携带。

**编辑安全**
显式安全机制有限。无人工在环（框架明确 'without human intervention'）；无编辑前 backup/rollback；无 git 版本管理。隐式边界：编辑仅限于三个 memory JSON
文件（绝不碰源码），success-gating 阻止垃圾 SOP 被采纳，每子任务 max-action 上限 N=20 防止失控循环，retry 可绕过记忆以逃离错误知识。未提及 eval-hacking
防御、密钥/注入检查或破坏性重写防护。

**协同进化**
skill-tool + generator-verifier 协同。三种记忆类型（strategic/procedural/tool）在每任务后由同一 Reflect Agent 协同蒸馏、协同精炼（Tool Memory 随技能 SOP
一起进化）。架构上是 generator-verifier 对：PE Agent（generator/executor）对 Reflect Agent（独立 verifier/supervisor）共享同一工具集，由 verifier
产生学习信号。

#### 自进化机制_How

**进化方法范式 (How)**
imitation_demonstration（将验证成功的动作轨迹蒸馏为可复用 SOP）+ 基于 LLM 的自我反思（Reflect Agent）。非梯度、文本空间的经验累积/去重，经 prompt 驱动的 merge expert
完成。无 RL、无 SFT、无种群进化。最接近带 LLM-judge 门控的 trajectory-to-memory 蒸馏。

**学习信号来源**
成败轨迹（子任务的成败由 Reflect Agent 判定）+ 自我反思（Reflect Agent 的自主 checklist）+ 环境反馈（主动验证：Reflect Agent 使用相同工具与环境交互并交叉核对关键信息，而非采信执行者的声称）。无外部 reward model。

**奖励粒度**
混合。process 级信号：Reflect Agent 按 3 轴 checklist（truthfulness/deliverable/data-fidelity）评估每个子任务及 checkpoint 进度；outcome 级信号：二元任务完整完成标志 S_full 喂入官方 S_partial 指标。

**学习范式**
on-policy + online（intra-test-time）在任务执行期间累积，并在跨顺序任务与 3 轮持续学习间做 inter-test-time 的记忆携带。无 off-policy replay buffer；无专用 sleep-time/offline replay 阶段（所有学习实时发生在循环中）。

#### 进化时机_When

**进化时机 (When)**
intra-test-time（每个子任务尝试后 Reflect+Memorize -> 立即复用 SOP）+ inter-test-time（跨任务与跨 3 轮持续学习迭代携带累积记忆；冻结快照用于完整 benchmark/泛化评估）。非 sleep-time（无夜间空闲 replay）。

**触发方式**
事件触发。每个子任务完成或达 max-action-limit 后 -> Reflect Agent 评估/蒸馏；整体任务完成后 -> 全 memory 升级（strategic 困境抽取、tool 编纂、去重/merge 精炼）。非周期/cron/课程/工具退化驱动。

#### 存储与检索

**技能库结构**
层次化 + 技能文件目录。Procedural = 层次化 platform->operation->{preconditions,steps,notes} 存于 procedural_memory.json；Strategic = 扁平
key-value dict（<=10）存于 strategic_memory.json；Tool = tool_name->{description,instruction} 存于 tool_memory.json。三者均为
memory/ 目录下的扁平 JSON 文件，procedural 层做索引/内容分离。

**检索/复用方式**
混合：description/index 匹配触发加载 + 经专用工具的 generation-as-retrieval。Strategic Memory + Procedural SOP INDEX 在启动时全量加载进 system
prompt（outline 形式）；完整 Procedural SOP CONTENT 按需经专用 memory_retriever 工具 a_mem 获取（prompt engineering 鼓励 agent
在子任务开始时查询）；Tool Memory 静态 description 始终在 prompt 中，动态 instruction 随每次工具观测内联返回。无向量/BM25 相似度检索；匹配是经 outline index 的 LLM
驱动。

#### 验证与反馈

**验证方式**
代理验证器（Reflect Agent 作为无 ground truth 的独立第三方 supervisor）+ 基于执行的主动验证（用工具与环境交互并交叉核对）+ 经有序 3 轴 checklist
的功能正确性检查：Truthfulness Verification（结论扎根于真实环境反馈以抑制幻觉）、Deliverable Verification（输出文件的存在性/完整性/正确性）、Data
Fidelity（无丢失/截断/篡改）。已采纳记忆无 held-out 评估门控。

**错误纠正**
经 replan 的自我修订 + 重规划（PE Agent 在每次 Reflect 评估后自适应刷新子任务队列 Q）+ 重试（子任务失败/达 max-actions 时给予一次重试，期间 procedural-memory
使用被禁用以鼓励探索而非利用可能错误的知识）。无对记忆的有界 diff-patch 编辑；纠错经重规划/重试完成，而记忆自纠由 merge-expert 去重步骤处理。

#### 环境与基座

**测试环境**
真实生产力任务：TheAgentCompany（TAC），一个长视野的企业生产力 benchmark，含跨 6 个角色（HR/PM/SDE 等）的 175 个任务，运行于全功能 OS 中，使用
chat、云存储、项目管理、代码编辑器与浏览器；平均 >40 动作步/任务，常跨 2+ 应用。跨应用 GUI + 工具调用 + web。

**底座模型**
PE Agent 与 Reflect Agent 均用 Gemini-2.5 Flash（同一模型、无 optimizer/target 分离）；TAC 中的 NPC 由 GPT-4o 驱动；视觉抽取器用 GPT-4o。迁移实验将两个
agent 都换成开源 DeepSeek-V3-250324。以闭源 Gemini 为主；任何 backbone 均无微调。

**部署域 (Where)**
general（横跨 chat/storage/PM/coding/browser 的通用跨应用办公/生产力自动化；未专门化于单一垂直领域）。

#### 评估指标

**评估指标**
success_rate（官方 TAC S_partial = 0.5*ckpt_ratio + 0.5*S_full；聚合 S_ckpt；Perfect Completion Rate PCR）+ 泛化（对未见 hard
任务的零样本、完整 benchmark 迁移）+ 样本效率（仅从 ~10% 任务获取记忆）+ 跨轮次的持续学习改进 + skill_library_growth（记忆累积）+ 成本（轻量 Flash 模型）。

**关键结论**
在 TAC 完整 175 任务 benchmark 上取得新 SOTA：平均 S_partial 51.78%（首次突破 50%）、S_ckpt 59.92%、PCR 41.14%（Gemini-2.5-Flash），较先前
SOTA（OpenHands-versa/Claude-4-Sonnet 43.19%）高约 20%。持续学习：3 轮单调改进，末轮较无记忆基线高 >10%。12 个 hard 任务上的零样本泛化：带累积记忆的 S_partial
23.65%->33.41%（对比 OpenHands/Gemini-2.5-Pro 3%、Claude-4-Sonnet 2%）。模型无关迁移：记忆将 DeepSeek-V3 从 S_partial 28.01%->36.75% /
S_ckpt 34.12%->50.59% 提升，击败所有其他开源框架。Reflect-Agent 消融：移除后 T_cl 上 S_partial 55.85%->43.21%。在官方 TAC 排行榜位列 #1。

#### 局限与挑战

**局限与挑战**
可迁移性（仅在单一 TAC benchmark 内验证；无跨 harness/跨用户/跨领域证据）；回归风险（新合并记忆无 held-out 验证门控——采纳仅依赖逐任务 Reflect 成功 + LLM merge，故错误 SOP
可能持续存在，且冻结的 3 轮快照从不被重新验证）；文档膨胀/可扩展性（procedural 库增长无界——仅 strategic 层硬上限 10；加载进 prompt 的索引可能增长）；optimizer 质量（蒸馏 + merge
质量严重依赖 Gemini/Reflect-LLM 能力）；可控性（全自动、无人工在环、无 backup/rollback）；eval-hacking 风险未明确处理。

#### 可借鉴要点

**可借鉴要点**
1) 带 INDEX/CONTENT SEPARATION + 按需检索的层次化 3 层记忆——仅将一个轻量 SOP outline 加载进 system prompt，完整正文经工具按需获取；这使 prompt 保持紧凑同时支持深度
procedural 召回。procedural SOP 形态 {platform:{operation:{preconditions, steps('A->B->C'), notes}}} 在结构上与过程化 SKILL.md
同源，是可直接复用的模板。2) 经由使用 3 轴 checklist（truthfulness/deliverable/data-fidelity 含主动环境交叉核对）的独立验证器（Reflect Agent）的 SUCCESS-GATED
蒸馏——只有验证成功的轨迹才能成为持久记忆；这是阻止垃圾技能累积的质量门控，也是对自进化 SKILL.md 最可迁移的单点思想（一个 workflow 被采纳前，独立验证器必须确认它确实奏效）。3) LLM 无关的自然语言记忆 +
MERGE-EXPERT 治理 prompt（去重、平台规范化、操作聚类，以及 strategic patterns 的 <=10 硬上限）——这使跨模型迁移成为可能并对抗技能库膨胀；带硬条目上限的 'Resolution Patterns
Merge Expert' 是保持 strategic SKILL.md 简洁的可直接复用治理模式，而 retry-with-memory-disabled 技巧是一种廉价的防过拟合保险。

#### 不确定字段

- doc_form——论文/repo 未报告每条 SOP 的确切 token 长度（procedural_memory.json 以空文件发布，作为运行时填充的占位符）；结构形态据方法论 + summarize_prompt.py / merge_application_prompt.py 模板推断
- version_gating——在 deep_update 覆写前是否存在任何内部 staging/backup 的 memory JSON；未描述（据 memory_manager.py 中 save-in-place 模式假定无）

---

### Reflexion / Self-Refine

> `idea_distill` · Reflexion(Northeastern/Princeton/MIT, NeurIPS 2023, arXiv:2303.11366)：verbal RL， 把稀疏奖励放大为 NL 反思存入情景记忆滑窗。Self-Refine(CMU/AllenAI, arXiv:2303.17651)： 同一 LLM 的 FEEDBACK→REFINE 任务内循环。两者是「反思驱动自改进」的根源范式，区别在

#### 基础信息

**名称**
Reflexion / Self-Refine

**提出机构**
Reflexion: Northeastern University (Shinn, Cassano, Berman), MIT (Gopinath), Princeton University (Narasimhan,
Yao)。Self-Refine: Carnegie Mellon University (Madaan, Gupta, Gao, Alon, Yang), Allen Institute for AI (Tandon,
Wiegreffe, Dziri, Gupta, Clark), University of Washington (Hallinan, Welleck), NVIDIA (Prabhumoye), UC San Diego
(Majumder), Google DeepMind (Hermann, Yazdanbakhsh)。

**发布时间**
Reflexion: arXiv v1 2023-03-20, v4 2023-10-10, NeurIPS 2023。Self-Refine: arXiv v1 2023-03-30, v2 2023-05-25, NeurIPS 2023。

**论文链接**
Reflexion: https://arxiv.org/abs/2303.11366 ; Self-Refine: https://arxiv.org/abs/2303.17651

**代码链接**
Reflexion: https://github.com/noahshinn/reflexion ; Self-Refine: https://github.com/madaan/self-refine（demo: https://selfrefine.info/）

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context 记忆与提示。两种方法均不更新模型权重、工具或架构。Reflexion 进化一个由 NL 反思构成的 episodic memory buffer（基于记忆的 verbal RL）。Self-Refine 迭代地精炼
in-context 的输出草稿。策略被参数化为 {LLM, memory/context}——优化纯粹发生在 text/prompt 空间。

**技能是否独立制品**
否。无持久可复用的制品。Reflexion：反思是作用域限于单个任务实例（问题 / AlfWorld env / 编程项）的临时 NL memory
条目，任务结束即丢弃。Self-Refine：精炼后的输出是一次生成调用的临时草稿；不存储任何内容供复用。关键在于，两者都不是跨任务的「技能」制品——仅是任务内部的临时「技能」。

**是否文档载体**
否。两者均不使用可读的指令文档（SKILL.md / markdown）作为核心载体。Reflexion = memory 列表中的自由格式 NL 反思字符串；Self-Refine = NL 反馈文本 + 精炼后的输出草稿。无
markdown 指令、无 YAML frontmatter、无 doc-as-skill 形态。（这是与 SKILL.md 自进化这条研究线的核心区别：它们是反思驱动的自我改进的根范式，但缺乏持久、可审查的文档载体。）

#### 技能表示

**技能编码方式**
自然语言 SOP / NL 反思文本。Reflexion：自由格式的第一人称自然语言自我反思字符串（如「我应该先搜索抽屉……」），追加到一个 episodic memory 列表。Self-Refine：结构化的多维度 NL 反馈（如
positivity、conciseness 等维度）+ NL 精炼输出。无可执行代码制品、无向量嵌入、无图、无多文件技能包。

**技能粒度**
insight / 策略规则。Reflexion：从失败轨迹中蒸馏出的逐试次口头经验/策略提示（如针对某个 AlfWorld env 的「新计划」）。Self-Refine：对当前草稿的逐迭代 critique 点。粒度是 insight/反馈级，而非原子动作、非完整技能包、非子任务 workflow。

#### SKILL.md_专属维度

**文档形态**
N/A——无 markdown 文档形态。Reflexion 的 memory 条目：简短 NL 反思（约 1-3 句，第一人称，如「New plan: check the drawer before the
fridge」）。Self-Refine：一段简短 NL 反馈块 + 精炼后的输出草稿。典型 token 长度：Reflexion 的反思很小（受 Ω=1-3 条目限制）；Self-Refine 的反馈约数百 token。无 YAML
frontmatter、无结构化字段、无作为载体的内嵌代码块（Self-Refine 的代码优化任务会精炼代码，但那是被改进的输出，而非技能文档）。

**编辑粒度**
逐试次/迭代全新生成（regenerate）。Reflexion：每次试次追加一条新生成的反思；memory 是一个有界滑动窗口（Ω=1-3），故旧反思被丢弃——实质上是 append + window-trim，而非对固定文档的
diff/patch。Self-Refine：每次迭代完整重新生成基于新反馈条件化的精炼输出。无对持久制品的有界 add/delete/replace、无 minimal diff、无 PATCH、无 bundle 编辑。

**版本与门控**
无——无留出验证门控、无 git 分支、无 Pareto 前沿、无评审门控采纳、无 staging+backup。Reflexion：对 memory 条目做简单的滑动窗口替换（一种原始的强制退役规则，上限
Ω）。Self-Refine：仅停止准则——模型自身判定「无需进一步精炼」或命中固定迭代上限。被接受的反思/精炼不在留出集上验证；一条错误的自我反思仍可能条件化下一次试次（无 rejection buffer）。

**文档来源**
失败轨迹蒸馏 + 成功轨迹归纳（test-gen 变体中）。Reflexion：自我反思由 Self-Reflection 模型从 {失败轨迹 τ_t, 稀疏奖励 r_t} → 口头经验 sr_t
蒸馏而来。Self-Refine：反馈从当前（常有缺陷的）草稿生成。两者皆是：轨迹 → NL。均不使用会话经验抽取、社区共享或离线 benchmark 训练作为文档来源。

**跨载体迁移**
跨任务：否——memory 在任务间重置（这是相较 SKILL.md 技能库方法的标志性局限）。跨模型：概念上可行（纯 prompt，与模型无关）但未作为迁移轴线研究。跨 agent harness / 跨用户 /
跨基准：未涉及。Reflexion 明确指出 memory 作用域限于任务实例；Self-Refine 是 intra-output 的。这种不可迁移性正是后来的 SKILL.md
进化工作（SkillOpt、EvoSkill、OpenSpace）在这些范式之上叠加持久、可移植文档的原因。

**技能库治理**
N/A——无技能库。Reflexion 唯一的治理原语是滑动窗口上限 Ω（1-3），这是一条粗略的强制退役/遗忘规则以尊重 context 限制——是文档膨胀控制的雏形，但非 curator
loop，无去重/合并、无基于相似度的编辑定向、无分层索引、无 Lotka-Volterra 生态。Self-Refine 仅保留最新草稿。

**失败记忆**
是，但是临时且任务局部的。Reflexion：反思明确源于失败（anti-pattern + 补救：「我做错了 X，应该做 Y」）。这是一个 failure-signature + attribution + remedy
三元组——但它仅存活于当前任务实例、之后即丢弃；无持久 anti-pattern 存储，无作为跨任务负反馈的 rejected-edit buffer。Self-Refine：反馈指出草稿中的缺陷（一种临时负信号），无持久失败记忆。

**编辑安全**
最小。Reflexion：用有界 memory Ω 防止 context 溢出；对编程，要求隔离的执行环境（作者「强烈建议为自主代码编写使用隔离的执行环境」），且自生成的单元测试在使用前经 AST
校验语法有效性。Self-Refine：一个停止准则以避免无限反馈循环。两者均无编辑前备份/回滚、无范围边界（无文档可界定）、无人工在环、无 eval-hacking 防御、无有界编辑的破坏性重写保护——因为不存在需要保护的持久制品。

**协同进化**
skill-only / generator-verifier 协同（在一个任务内）。Reflexion：Actor + Evaluator + Self-Reflection 是三个协同进化同一 memory 的不同
prompt/角色（一个 generator-verifier-reflector 三元组），但全部作用于任务实例——无 skill-tool 协同进化，无 skill-skill 生态。Self-Refine：generator /
critic / refiner 是同一个配以不同 prompt 的 LLM（skill-prompt 联合、self-collaboration）。两者均不与外部工具或其他技能协同进化。

#### 自进化机制_How

**进化方法范式 (How)**
reward-based（文本反馈 / 自我反思放大）+ rollout_optimization（非梯度、文本空间优化）。Reflexion（「verbal RL」）：一个稀疏奖励 r_t（二元 pass/fail、标量或自测结果）由
Self-Reflection 模型放大为 NL 口头反馈 sr_t，存入 episodic memory，条件化下一次
rollout——这是语言空间中的策略优化，无需梯度更新。Self-Refine：自生成的多维度反馈充当隐式奖励，引导输出的迭代文本空间精炼。两者均明确回避梯度/SFT/RL：「不需要任何有监督训练数据、额外训练或强化学习」（Self-Refine）；「不是通过更新权重，而是通过语言反馈来强化语言
agent」（Reflexion）。

**学习信号来源**
Reflexion：环境奖励（AlfWorld 的启发式成功信号、HotpotQA 的 exact-match 评分）+ 工具成功率指标（自写的单元测试作为 HumanEval/MBPP 的代理验证器）+ 自我反思（用于决策的 LLM
自评估/分类）。Self-Refine：LLM-as-judge（同一 LLM 沿任务特定维度评判自身输出）+ 成败轨迹（当前草稿作为轨迹）。两种来源均为 test-time，无离线训练标签。

**奖励粒度**
hybrid（混合）。Reflexion：每次试次的 outcome 级二元/标量奖励（pass/fail）被放大为 process 级 NL 反思（即 outcome → process）。Self-Refine：对草稿的 process 级多维度 critique（直接的 process reward）。

**学习范式**
online；on-policy；intra-test-time（非 sleep-time / 离线）。两者均在推理期生成并从自身 rollout 中学习，无 replay buffer、无离线 sleep-time
巩固。Reflexion 在技术上是一个 episode 内迭代的 on-policy；Self-Refine 是单次调用的迭代精炼。

#### 进化时机_When

**进化时机 (When)**
intra-test-time。Reflexion：跨试次但在单个任务实例之内（memory 在同一问题 / AlfWorld env / 编程项的多次尝试间持久、在项间重置）。Self-Refine：在单次生成任务之内（迭代
feedback-refine 循环直至停止）。两者均不做持久制品的 inter-test-time sleep-time 离线进化。

**触发方式**
失败触发 + 事件触发。Reflexion：反思在评估器失败时触发（环境判定失败，或一个手写启发式检测到 agent 卡住——同一动作重复 >3 个周期，或在 AlfWorld env 中 >30
个动作——「低效规划」）。Self-Refine：每次迭代触发一个反馈步骤，直至模型的停止准则被满足（模型表示无需更多精炼）或命中固定迭代上限。两者均非周期性/cron、非课程驱动、非工具退化触发。

#### 存储与检索

**技能库结构**
无。Reflexion：一个扁平列表（memory buffer）持有最近 Ω（1-3）条 NL 反思，作用域限于单个任务实例——无向量库、无分层索引、无 DAG、无
git、无云端注册中心、无图。Self-Refine：完全没有技能库；只有当前草稿 + 最新反馈存在于 context 中。作者明确将其标为未来工作：「我们鼓励未来工作用更先进的结构（如向量嵌入数据库或传统 SQL 数据库）来扩展
Reflexion 的 memory 组件。」

**检索/复用方式**
同实例直接复用——无语义检索。Reflexion：当前任务实例的全部已存储反思都被前置于下一次试次的 prompt（无嵌入、无 BM25、无 LLM rerank、无 description-match
触发；定向依据是任务实例的身份，而非相似度）。Self-Refine：最新反馈直接条件化下一个精炼步骤。无 generation-as-retrieval 或
workflow-match。通行的评审查证确认：「无全局向量库、语义检索层或跨任务 memory 索引。」

#### 验证与反馈

**验证方式**
execution-based + LLM-judge + 代理验证器（无 ground truth）。Reflexion：AlfWorld 使用环境执行成功 + 一个 LLM/启发式自评估器；HotpotQA 使用 exact-match
执行评分；编程使用自写的单元测试作为代理验证器（经 AST 过滤，n≤6）——这是一种无 ground truth 的验证门控，使其符合 pass@1
资格。Self-Refine：LLM-as-judge（同一模型产出充当验证的反馈）。无留出验证集、无多模型辩论。

**错误纠正**
自我修订 + 重规划。Reflexion：基于新反思重新生成完整轨迹（对 AlfWorld，是一个「新计划」）；对代码，在测试/编译反馈引导下调试后重写实现。Self-Refine：在多维度反馈引导下对草稿做局部编辑。两者均不对持久文档使用有界 diff-patch，也无显式回滚（不存在可回退到的持久制品）。

#### 环境与基座

**测试环境**
Reflexion：编程（HumanEval、MBPP、LeetcodeHardGym——一个新的 40 题难题 benchmark）、序列决策（AlfWorld，134 个 env / 6 种任务类型；WebShop 消融）、推理
QA（HotpotQA）。Self-Refine：7 项多样的生成任务——对话回复生成、数学推理、代码优化、缩写生成、故事生成、情感反转、毒性去除 / 受约束生成。总体：general。

**底座模型**
GPT 系列。Reflexion：GPT-3（AlfWorld few-shot）、GPT-3.5 / GPT-4（推理 + 编程，包括 text-davinci-003 与 gpt-3.5-turbo）；Reflexion 的 actor
角色还探索了 Chain-of-Thought 与 ReAct 作为动作生成器。Self-Refine：GPT-3.5（text-davinci-003、gpt-3.5-turbo）、GPT-4 与
Codex（code-davinci-002，用于代码）。optimizer/target 分离：Self-Refine 明确使用单个 LLM 同时充当 generator + feedback provider +
refiner（无分离）。Reflexion 使用三个不同的 prompt（Actor / Evaluator / Self-Reflection）但同一底层模型家族——是逻辑角色分离，而非模型权重分离。

**部署域 (Where)**
general。两者均面向通用推理、编程、决策与语言生成——而非 specialized 垂直领域（非仅 GUI、非仅 office）。Reflexion 是 agentic（环境交互）；Self-Refine 是输出精炼；两者均为 general 领域。

#### 评估指标

**评估指标**
success_rate（HumanEval/MBPP/LeetcodeHard 的 pass@1；AlfWorld 134 个 env 的 solve-rate；HotpotQA 的 exact-match）+ 样本效率（至多 12
次试次的收敛曲线）+ 泛化（跨任务鲁棒性，跨 actor 类型 / 反馈信号 / 反馈纳入方式的消融）。Self-Refine 另加人工偏好率 + 任务特定自动指标（如
constraint-accuracy、BLEU）+「每迭代精炼率」。无 skill_library_growth 指标（无技能库）。无成本/经济价值捕获指标（早于该框架）。

**关键结论**
Reflexion：HumanEval Python pass@1 91%（对比先前 SOTA GPT-4 的 80%）；AlfWorld 解出 130/134（在 12 个迭代学习步内较 ReAct 基线绝对提升
+22%；ReAct-only 在约 22% 幻觉率处平台化）；HotpotQA 绝对 +20%（CoT-GT 经反思 +14%，自我反思在仅 episodic-memory 消融之上再加 +8%）；HumanEval Rust
68%（对比 GPT-4 的 60%），MBPP Rust 75.4%，LeetcodeHard 15%（对比 GPT-4 的 7.5%）；MBPP Python 77.1%（略低于 GPT-4 的 80.1%——归因于 16.3%
的自测假阳性率，而 HumanEval 为 1.4%）。消融：在 HumanEval-Rust 上移除 test-gen → 52%，移除自我反思 → 60%（无基线之上的提升）。Self-Refine：跨 7 项任务约 20%
的绝对平均改进（范围 5-40%）；输出在人工与自动指标上均优于 one-shot GPT-3.5/GPT-4；在 Codex 代码任务上最高 +13%。

#### 局限与挑战

**局限与挑战**
可扩展性（滑动窗口 memory Ω=1-3 限制 context，无向量/SQL 库）+ 灾难性遗忘/无跨任务迁移（memory 在任务实例间重置——这是相较 SKILL.md 技能库的标志性差距）+ 可迁移性（无跨模型/跨
harness 研究）+ 可控性（无正式成功保证；「可能陷入非最优局部最优」）+ optimizer_quality（完全依赖 LLM 自评估质量；弱自评估 → 弱反思）+ 代码上的 eval-hacking 风险（不稳定的自写测试 →
假阳性 pass@1，如 MBPP-Python 回归所示）+ 在探索密集任务上的局部最优失败（Reflexion 在 WebShop 上未能改进——4
次试次后终止；「无法解决需要大量多样性与探索的任务」）。Self-Refine：当自反馈不可靠时会过度精炼/放大自身错误；成本随迭代线性增长。两者：文档膨胀 N/A（无文档）。

#### 可借鉴要点

**可借鉴要点**
三条可直接迁移的工程洞见，用于让 agent 自进化其 SKILL.md，源自这两个根范式：(1) 在写入制品前将稀疏奖励放大为 NL 反思——Reflexion 的核心动作是把二元/标量信号转化为第一人称的口头经验（「我做错了 X；下次做
Y」）。对 SKILL.md 进化而言，这是每一次编辑的种子：失败轨迹 → 蒸馏出的 insight → 追加/修订文档，而非从原始奖励盲目编辑。(2) 有界滑动窗口
memory（Ω=1-3）作为最简单可行的防膨胀/强制退役治理——Reflexion 表明即便粗略的上限也能防止 context 爆炸同时保持近期经验鲜活；SKILL.md 系统在引入 Lotka-Volterra
式生态之前，应继承此作为最低编辑预算/条目退役规则。(3) Self-Refine 的单 LLM 兼 generator/critic/refiner 配以多维度 process 级反馈，是最廉价的 test-time
循环（无需训练、无需额外模型）——可直接用于让一个 agent 沿 clarity / coverage / safety / regression-risk 等维度评判自身的 SKILL.md 并做局部编辑。移植到 SKILL.md
时需弥合的关键差距：两种范式都是任务内的、且在任务间丢弃 memory——跃迁到自进化的 SKILL.md 需要 (a) 把任务局部的反思提升为持久、可审查的 markdown 制品，(b) 补上它们所缺乏的验证门控（留出 / Pareto
/ 评审门控采纳），使一条糟糕的反思无法毒化文档，以及 (c) 加入跨任务检索以让 insight 迁移——这正是 SkillOpt / EvoSkill / OpenSpace 在 Reflexion 的 verbal-RL
原语之上叠加的内容。

---

### Voyager (对照)

> `contrast` · NVIDIA/Caltech/UT Austin/Stanford, 2023(arXiv:2305.16291)。技能=可执行 JavaScript 代码 (非文档)，向量嵌入检索，自动课程+迭代提示+自我验证门控。作为「代码技能库」对照项， 论证文档载体(SKILL.md)在可读性/可审查性/可迁移性上的差异。github MineDojo/Voyager

#### 基础信息

**名称**
Voyager

**提出机构**
NVIDIA、Caltech、UT Austin、ASU（MineDojo 团队）。作者：Guanzhi Wang、Yuqi Xie、Yunfan Jiang、Ajay Mandlekar、Chaowei Xiao、Yuke Zhu、Linxi Fan、Anima Anandkumar。

**发布时间**
2023-05-25（arXiv v1）；v2 修订于 2023-10-19

**论文链接**
https://arxiv.org/abs/2305.16291

**代码链接**
https://github.com/MineDojo/Voyager

**类型**
academic

#### 进化对象_What

**进化对象 (What)**
Context记忆与提示 + Tools技能。不更新任何模型权重（纯黑盒 GPT-4 查询，无微调）。进化的制品是：(a) agent 不断增长的、由可执行 JavaScript 程序组成的技能库，以及 (b) 提出下一个探索任务的 in-context 自动课程。二者完全位于 LLM 权重之外。

**技能是否独立制品**
是。每个技能是一个独立可复用的制品，存储在磁盘上：(1) `skill/code/<name>.js`——面向 Mineflayer bot API 的可执行 JavaScript 程序；(2)
`skill/description/<name>.txt`——一个由 LLM 生成的自然语言描述，仅用于检索；(3) `skills.json` 中的一行，以及 Chroma 向量库中一个以描述 embedding
为键的向量。一小批手写的
`control_primitives/*.js`（mineBlock、craftItem、killMob、exploreUntil、placeItem、smeltItem、useChest、shoot）作为原子构件被播种，生成的技能在其之上组合。

**是否文档载体**
否。技能载体是可执行代码（JavaScript），而非可读的 markdown 指令文档。自然语言描述仅作为索引/检索条目存在（以 `//` 注释头形式内嵌于 .js 文件中），并非主制品。这正是将 Voyager 作为本调研中对比 SKILL.md 的反例纳入的原因。

#### 技能表示

**技能编码方式**
可执行代码（JavaScript 程序）+ 作为注释头的自然语言描述，用于基于 embedding 的检索。每个技能是多文件技能包：代码文件、描述文件，外加 JSON 注册表与 Chroma 向量库。原子原语（control_primitives）是手写 JS；学习到的技能是调用原语的 GPT-4 生成 JS。

**技能粒度**
子任务 workflow / 完整技能。每个技能是一个命名的、时间上延展的行为（如「craft wooden pickaxe」「hunt cows for leather」），实现为 JS 函数 `async function
<name>(bot) { ... }`。复杂技能通过调用先前存储的技能函数来组合更简单的技能——一个层次化、可组合的技能库。

#### SKILL.md_专属维度

**文档形态**
在 SKILL.md 的意义上不适用——Voyager 没有 markdown 文档载体。最接近的类似物是 .js 技能文件，其「文档形式」= 一个 async 函数，包含：(a) 一个由 LLM 生成的多行 `//
description` 头（用于 embedding 与检索），以及 (b) 调用 Mineflayer 原语的函数体。典型程序长度为数十行 JS。描述很短（几句话）。token 长度主要由可执行代码占据，而非散文。

**编辑粒度**
全新生成（full regeneration）。当一个技能被添加时，整个 .js 程序由 GPT-4 端到端一次性生成，随后通过 iterative-prompting 循环，利用环境反馈 + 执行错误 +
self-verification 整体重写（而非 patch）直至通过。重新添加已存在的技能名会触发版本化重写：旧文件被归档为 `<name>V2.js`、`V3.js`……而 skills.json
中的活动条目被覆写——一种粗粒度的整文件替换，而非有界的 add/delete/replace diff。

**版本与门控**
验证门控（留出、基于执行的 self-verification）——而非 git 分支 / Pareto / DAG。只有通过 GPT-4 self-verification（verifier agent 通过箱子库存 + 附近实体 +
状态检查最新环境状态）的技能才会被提交到技能库；未通过的程序停留在 iterative-prompting 循环中（最多 4 轮），若仍失败则被丢弃。仅有软版本控制：同名重新生成的技能以 V2/V3/...
备份形式转储到磁盘，但不会在它们之间主动选择。无暂存、无回滚、无人工审查门控。

**文档来源**
LLM 一次性生成 + 失败轨迹蒸馏（通过执行错误迭代重生成）+ 执行录像回放（self-verification 读取执行后环境状态）。原子原语（control_primitives）是人工初始化（手写种子代码）。新技能由 GPT-4 从（课程任务 + 检索到的相关技能 + 原语上下文 + 环境反馈）中产出。

**跨载体迁移**
跨任务（Minecraft 内部）是头条结果：一个学习到的技能库可在全新的 Minecraft 世界中零样本复用以解决未见任务，而基线（ReAct、AutoGPT、ReSP）无法泛化。跨模型——未验证；紧密绑定于 GPT-4（提示假设具备
GPT-4 级代码生成与验证能力）。跨 agent harness——不适用；技能载体是 Mineflayer 特定的 JS，故不重写则无法迁移到 Claude/Codex/Cursor 或非 Minecraft
harness。跨用户/团队——仅通过仓库中开源的 skill_library/ 目录。

**技能库治理**
层次化索引（向量库）+ 相似度检索编辑目标（retrieval_top_k=5，按描述 embedding）+ minimal 灰尘清理。明确的 anti-bloat 规则：deposit-chest 技能永不被添加（「No need to
reuse the deposit skill」）。同名技能被版本化（V2.js、V3.js）而非去重/合并。无 Lotka-Volterra 退休、无 curator loop、除磁盘版本备份外无过时技能归档。

**失败记忆**
部分。在单个技能学习 episode 内，执行错误与环境反馈被回馈到 iterative-prompting 循环（最多约 4 轮重生成）——一个短视界的负信号。Critic/curriculum agent
记录过往进展（新物品、生物群系、怪物、方块）以避免重新提出已完成的任务。然而，无持久的 anti-pattern 存储、无失败签名 + 修复库、无跨 episode 存活以否决未来有害编辑的 rejected-edit buffer。

**编辑安全**
最小 / 仅执行层。范围被限定在 Minecraft 沙箱内——破坏性编辑无法逃出游戏世界（隐式收容）。Self-verification 充当软性的预提交门控。无编辑前备份+回滚（仅有事后 V2.js
版本转储用于意外的同名覆写）、无人工在环、无 eval-hacking 防御、无密钥/注入检查。安全性实际上依赖封闭的 Minecraft 环境而非文档编辑护栏（因为制品是程序而非文档）。

**协同进化**
skill-skill 生态 + generator-verifier 协同。新技能组合并调用旧技能（skill-skill 生态，能力复合）。一个独立的 verifier agent（GPT-4 作为
critic）与技能生成器协同进化：同一个 GPT-4 既充当代码生成器又充当 self-verifier。自动 curriculum agent（同为 GPT-4）根据当前技能清单与发现状态提出下一个要学习的技能——一种
curriculum-skill 协同进化。无 skill-tool 联合编辑（原语工具 API 固定/手写）。

#### 自进化机制_How

**进化方法范式 (How)**
rollout_optimization（非梯度，文本/代码空间优化，经迭代提示）+ imitation_demonstration（提示中的 few-shot 种子原语）。具体而言：GPT-4 生成一个 JS 程序；在
Mineflayer 中运行；环境反馈 + 执行错误 + self-verification 被折回提示，程序被重新生成，循环直至验证通过。对 LLM 无梯度/SFT/RL——仅黑盒 API 查询。curriculum 组件执行
in-context 新颖性搜索（LLM 根据迄今进展提出下一个最具探索价值的任务）。

**学习信号来源**
成败轨迹（执行成功/失败）+ 环境奖励（隐式：程序是否在 Minecraft 中产生了预期的状态改变）+ 自我反思（GPT-4 self-verification 读取箱子库存、附近实体与 bot
状态以判断任务是否达成）。curriculum agent 额外将发现新颖性（新物品/生物群系/怪物）作为探索信号。无外部奖励模型、无留出验证集。

**奖励粒度**
outcome（每技能：验证过的任务是否成功？）。self-verification 对最终环境状态是二元 outcome 级的，而非逐步的 process credit。

**学习范式**
online（在终身学习过程中）+ on-policy（每个技能由当前 GPT-4 在当前检索到的上下文下新鲜生成，而非来自旧轨迹的 replay buffer）。风格上属 inter-test-time：早期 episode
中学到的技能被持久化并在后续 episode 中复用，但无离线 sleep-time replay——所有学习都在运行中的 Minecraft 会话内实时发生。

#### 进化时机_When

**进化时机 (When)**
inter-test-time + intra-test-time 混合。技能库在任务之间进化（inter-test-time：每个课程任务完成后，一个新技能可能被提交），并且在单个技能学习 episode 内
intra-test-time 进化（iterative-prompting 循环将程序重新生成最多约 4 次直至验证通过）。

**触发方式**
curriculum（课程）驱动 + 失败触发。自动 curriculum agent 提出每个下一个任务（= 新技能生成的显式课程驱动触发）。在技能学习 episode 内，执行失败 / 验证失败触发迭代重生成。整个循环由
curriculum 提出下一个探索任务以及对当前任务的环境反馈事件驱动——而非周期性 cron、非使用驱动。

#### 存储与检索

**技能库结构**
扁平 + 向量库 hybrid。技能以扁平文件存储于 `skill/code/*.js` + `skill/description/*.txt` + 一个 `skills.json` 注册表，由一个扁平的 Chroma
向量库（`skill/vectordb/`）索引，以描述 embedding 为键。层次结构通过组合隐式体现（一个技能的代码可以调用另一个技能导出的函数），而非磁盘上显式的树/DAG。`skill_library/trialN/`
下的检查点目录快照一个已学习的库以供迁移。

**检索/复用方式**
语义相似度（基于描述 embedding 的语义相似度，top_k=5，经 Chroma OpenAIEmbeddings similarity_search_with_score）。检索到的技能代码与 control primitives
拼接，作为 few-shot 上下文注入生成提示。不使用 generation-as-retrieval；检索仅基于描述 embedding，无 BM25、无 LLM rerank、无 workflow 匹配。

#### 验证与反馈

**验证方式**
基于执行的 self-verification（验证门控）。在一个候选技能运行后，一个单独的 GPT-4 verifier 调用检查产生的 Minecraft 状态（箱子内容、附近实体、bot
库存/状态、已完成的子目标）并发出接受/拒绝决定。只有被接受的技能被提交到库；被拒绝的重新进入 iterative-prompting 循环。无留出 benchmark、无代理 verifier、无多模型辩论。

**错误纠正**
自我修订（self-revision），经迭代重生成。每次失败/验证失败的尝试将执行错误信息 + 环境反馈 + self-verification 批评回馈到提示；同一技能从头重新生成（而非 patch）最多约 4 轮。无回滚、无有界
diff 编辑、无定向 patch——修正 = 用更丰富的上下文做整体重生成。重规划发生在 curriculum 层（若进展停滞，curriculum agent 重新选择下一个任务）。

#### 环境与基座

**测试环境**
Minecraft（具体为经 Mineflayer 无头 bot 的 MineDojo 风味 Minecraft，带 fabric mod 与一个 1.19 fabric-loader 实例）。仅单一具身游戏环境。

**底座模型**
GPT-4（闭源，经 OpenAI 黑盒 API）用于全部三个 agent：自动 curriculum、技能代码生成与 self-verification。无 optimizer/target 分离——GPT-4 既是策略又是
verifier。代码生成假设 GPT-4 级能力；消融显示 gpt-3.5-turbo 急剧退化。Mineflayer bot 运行时是执行器，而非学习到的模型。

**部署域 (Where)**
specialized（单一游戏域：Minecraft 开放式探索）。技能库、提示模板与原语都是 Minecraft 特定的；方法论模式（终身学习的代码技能库 + 自动 curriculum + self-verification）可泛化，但制品不可。

#### 评估指标

**评估指标**
skill_library_growth（终身获取的技能数）+ sample_efficiency（达到里程碑的 episode / 迭代数）+ generalization（在全新 Minecraft 世界中对未见任务的零样本成功率）+
functional correctness（解锁的科技树里程碑）+ exploration coverage（获得的独特物品、移动距离、发现的生物群系）。成本（GPT-4 API token）被定性报告，但非头条指标。

**关键结论**
相对先前 SOTA（ReAct、AutoGPT 风格、ReSP），获得的独特物品多 3.3x、移动距离长 2.3x、科技树里程碑快达 15.3x。强终身学习：持续获取技能而无灾难性遗忘（归因于显式的外部技能库 vs
基于权重的记忆）。零样本迁移：在一个世界训练的技能库可从零开始解决新世界中所有未见任务，而基线无法泛化。消融显示移除技能库、自动 curriculum 或 self-verification 各自都显著降低性能——三个组件均不可少。

#### 局限与挑战

**局限与挑战**
optimizer_quality（依赖前沿 GPT-4 级 LLM；gpt-3.5-turbo 消融崩溃）+ transferability（技能紧密绑定于 Mineflayer/Minecraft bot API，无法迁移到其他
harness 或非游戏域）+ controllability（curriculum 由新颖性驱动，可能追求无关任务；无人工引导）+ catastrophic_forgetting 被缓解但以库膨胀为代价（V2/V3 转储，无真正退休）+
eval-hacking 风险（self-verification 由生成代码的同一 GPT-4 完成——无独立裁判）+ scalability（每个技能 = 一次完整 GPT-4 生成 + 执行轮次；成本随库大小线性增长）+
regression_risk（当同名新技能覆写旧技能时，对先前获取的技能无留出回归测试）。值得注意的是，制品形式本身（可执行代码）使人工审计昂贵——评审者必须阅读 JS + Mineflayer 语义，不像 markdown 指令那样。

#### 可借鉴要点

**可借鉴要点**
- BORROW (1)——提交前的 self-verification 门控。Voyager 的 verifier 检查执行后状态，仅提交通过的技能；对于 SKILL.md 演化，一个类似的 verifier（LLM-as-judge 对照文档所述效果与实际 rollout，或一个留出任务通过率门控）应当在每次编辑落地到技能目录前对其门控。缺少这一步，SKILL.md 文件会累积未经验证的散文。
- BORROW (2)——基于 NL 描述的 embedding 索引检索 + 组合式复用。尽管 Voyager 的主制品是代码，它仍为每个技能单独生成一个 NL 描述，纯粹用于向量库检索（top-k=5），并将检索到的技能作为 in-context 示例注入。SKILL.md 应采取同样做法：保留一个为 embedding 检索优化的简洁描述字段（YAML frontmatter），即便正文是丰富的指令散文，并让复杂的 SKILL.md 技能引用/组合更简单的技能。
- BORROW (3)——带执行反馈的迭代重生成，而非一次性写入。iterative-prompting 循环（环境反馈 + 执行错误 + 自我批评，最多 N 轮）可直接移植：当文档的 dry-run/sandbox 可用时，SKILL.md 编辑同样应是 regenerate-with-feedback 循环，而非单次 LLM 写入。
- BORROW (4)——anti-bloat 规则 + 同名版本控制。Voyager 明确拒绝存储「deposit useless items」技能，并为同名覆写转储 V2/V3 备份。SKILL.md 治理同样应当 (a) 维护一个低价值文档类型的拒绝列表，永不提交，以及 (b) 在覆写时保留版本化备份以从回归中恢复。
- CONTRAST（SKILL.md 胜出的地方）——可读性：SKILL.md 是人类可读的指令；Voyager 的 .js 技能需要 Mineflayer + JS 专业知识才能审计。可审计性：SKILL.md 可在部署前经人工审查或批准（人工在环是自然的）；Voyager 的 verifier 是编写代码的同一个 GPT-4（无独立检查）。可迁移性：SKILL.md 指令对 agent harness 可移植（Claude/Codex/Cursor 都能读 markdown）；Voyager 的技能锁定于 Mineflayer/Minecraft。组合性在性质上不同：Voyager 通过 JS 中的函数调用组合（精确、确定、可重放），而 SKILL.md 通过引用 + 计划组合（灵活，但丧失确定性重放）。结论：借鉴 Voyager 的验证 + 检索 + anti-bloat 工程，但保留 SKILL.md 的散文载体以在可读性、可审计性与跨 harness 迁移上取胜——接受确定性可重放性较弱的权衡。

#### 不确定字段

- library_governance——除 V2.js 备份外，确切的退休/归档策略未文档化；仅从源码推断
- failure_memory——检查点中除 skills.json 与 curriculum 的进展记录外，是否有任何跨 episode 的失败信号持久化
- release_date——arXiv v1（2023-05-25）与 v2（2023-10-19）之间存在轻微歧义；以 v1 为准
- reward_granularity——论文将 self-verification 描述为 outcome 级；无逐步 credit assignment，但 curriculum 新颖性带有 process 风味

---
