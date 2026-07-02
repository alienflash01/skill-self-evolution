# skill-self-evolution：价值、场景、前景与业界对比

> 核心命题：AI agent 的"记忆"和"自进化"到底有什么不同？谁在做？我们怎么做才能不一样？

---

## 一、业界"记忆 vs 自进化"全景

### 三层能力，别混淆

很多人把"记忆"和"自进化"混为一谈。实际上它们是三个不同的层次：

| 层次 | 做什么 | 谁在做 | 持久化 |
|---|---|---|---|
| **L0 记忆** | 记住事实（用户偏好、构建命令、项目结构） | CC auto-memory / Hermes memory | 文本文件 |
| **L1 反思** | 任务后分析成败，提取可复用的经验 | Hermes issue #483 / claude-meta | 结构化日志 |
| **L2 进化** | 系统性优化技能/规则，**用验证门控保证改进** | SkillOpt / Homunculus / 你的项目 | 版本化技能文档 |

**关键区别：**
- L0 记忆是"存了就完了"——下次加载进来，好坏不管
- L1 反思是"分析完存起来"——比记忆结构化，但不验证效果
- L2 进化是"改完要验证，不比原来好就不采纳"——**这是唯一有质量保证的层次**

### 业界方案详细对比

#### 1. Claude Code auto-memory（Anthropic 官方）

**机制：**
- 每个 git 仓库一个 `~/.claude/projects/<project>/memory/MEMORY.md`
- CC 自己决定写什么：构建命令、调试经验、代码风格偏好
- 每次会话加载前 200 行 / 25KB
- 纯文本，无结构化，无验证

**优势：** 零配置，官方原生，CC 自己维护
**劣势：**
- **无验证**——CC 觉得有用就写了，可能写了个错的
- **无结构**——纯 markdown，无法程序化检索/更新
- **被动记录**——只在 CC 工作时顺手记，不会主动反思
- **无版本管理**——改了就改了，回不了旧版

**vs 你的项目：** CC auto-memory 是 L0。你的项目做的是 L1+L2——有 fail→success 模式检测（L1）和 gate 验证（L2）。

#### 2. Hermes Agent memory（Nous Research）

**机制：**
- 内置 `MEMORY.md` + `USER.md`（§分隔，2200/1375 字符上限）
- 8 个外部 memory provider 插件可选：
  - **Honcho**——辩证式用户建模 + 会话级上下文注入
  - **Mem0**——服务端 LLM 事实提取 + 语义搜索
  - **Hindsight**——知识图谱 + 跨记忆综合推理（reflect）
  - **Holographic**——本地 SQLite + HRR 代数查询 + 信任评分
  - **Supermemory**——语义搜索 + 会话图 + 防递归污染

**优势：** 生态丰富，选择多，跨会话持久
**劣势：**
- **全是 L0**——没有任何 provider 做验证门控
- 存了就完了，下次注入进来，不管对不对
- **issue #483（Post-Task Reflection）还没实现**——Hermes 官方承认："目前无结构化反思、无 missing affordance 检测"
- **issue #337（Evolutionary Self-Improvement）还是提案**——官方还没开始做

**vs 你的项目：** Hermes 有最好的记忆**存储**层（8 个 provider），但完全没有**进化**层（L2 gate 验证）。你做的是 Hermes 缺的那块。

#### 3. Hermes issue #483（Post-Task Reflection）—— 提案阶段

这个提案最能说明业界方向。它提出了：

```
ReflectionFrame schema:
  failure_mode: 错误分类（5 类）
  task_state: 任务状态摘要
  world_model_updates: 世界模型更新（带证据）
  tool_insights: 工具洞察（合约/约束形式）
  context_forget: 过时信息清理
  open_questions: 开放问题

+ Missing Affordance Detection:
  失败 → 分类 → 记录能力缺口 → 建议创建技能
```

**vs 你的项目：** 你的 distill.py L1 已经做了类似的 fail→success 模式检测。Hermes 的提案更系统化（5 类错误分类 + affordance 缺口检测），但**还没实现**。

#### 4. Cognitive Workbench（Bruce D'Ambrosio）

**机制：** 18K 行 Python，实现了 Hermes #483 提案的所有内容：
- 任务后 `_reflect()` 生成 ReflectionFrame
- missing affordance 检测 → 自动记录 + 建议技能创建
- 滑动窗口压缩长 trace → 反思时不爆 context

**优势：** 最完整的 L1 反思系统
**劣势：** 纯研究框架，18K 行，不针对 CC，无 L2 验证门控

**vs 你的项目：** 你的 distill.py 是轻量版（1125 行）的反思系统。他们的错误分类和 trace 压缩值得借鉴。

#### 5. Homunculus /hm-night（nightly agent）

**机制：**
- 夜间 cron 触发，eval → improve → rollback 循环
- 技能必须在验证集上达到 100%（含 5pp 噪声容忍）
- 回归时自动 rollback

**优势：** 夜间无人值守，验证驱动
**劣势：** 单机，100% 目标可能过于严格

**vs 你的项目：** 你的 sleep cycle 是同类设计，但 gate 条件是"严格改进"（>而非≥），更保守。

#### 6. claude-meta（社区最小方案）

**机制：** 一个 prompt 指令——"每次犯错后自动更新 CLAUDE.md"
**优势：** 极简，5 分钟部署
**劣势：** 零验证，CLAUDE.md 会膨胀变垃圾

**vs 你的项目：** claude-meta 是你的 L0 版本——无模式检测、无验证、无版本管理。

---

## 二、差异矩阵

| 能力 | CC auto-memory | Hermes memory | claude-meta | Homunculus | Cognitive Workbench | **skill-self-evolution（你）** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| **L0 记忆存储** | ✅ | ✅✅ 8 providers | ✅ | ✅ | ❌ | ✅ rules.json |
| **L1 fail→success 检测** | ❌ | ❌ 提案中 | ⚠️ 手动 | ⚠️ | ✅ | ✅ distill.py |
| **L1 错误分类** | ❌ | ❌ | ❌ | ❌ | ✅ 5 类 | ⚠️ 3 类 |
| **L2 gate 验证** | ❌ | ❌ | ❌ | ✅ 100% 阈值 | ❌ | ✅ 严格改进 |
| **L2 留出验证集** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ train/val split |
| **版本管理** | ❌ 覆盖写 | 取决于 provider | ❌ | ✅ git | ❌ | ✅ staging+adopt |
| **夜间无人值守** | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ cron+nightly |
| **分布式/集群** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌（待做） |
| **实时 hook** | ✅ 被动 | ✅ 被动 | ❌ | ❌ | ❌ | ✅ PostToolUse |

**你的独占区（别人都没有的）：**

1. **L1 实时 + L2 验证 同时存在**——CC auto-memory 和 Hermes 只有 L0；Homunculus 有 L2 但没有实时 L1
2. **留出验证集（train/val split）**——连 Homunculus 都不做 train/val 划分，你从 SkillOpt 继承了这个学术上最严谨的设计
3. **strict-improvement gate**——平手拒绝，比 Homunculus 的 100% 阈值更保守但更通用

---

## 三、重新定义价值——从客户场景出发

### 3.1 客户真实痛点

你说的"服务器集群夜间利用率低"——这不是技术问题，是**财务问题**。

```
10 台服务器 × 8 小时夜间空闲 × 22 天/月 = 1760 机器小时/月浪费

如果这些机器在跑 CC：
  - 每台每晚 ~50 次 CC replay 调用
  - 每月 ~11000 次夜间学习调用
  - 产出：每周 ~3-5 条经过验证的经验规则
  - 效果：AI 团队减少重复错误，编译/测试一次通过率提升

客户算账：
  "夜间电费/折旧我已经花了 → 加点 API 费让 AI 自己变强 → 白天效率更高"
  这是纯赚的。
```

### 3.2 谁会买单

| 角色 | 痛点 | 你的回答 |
|---|---|---|
| **CTO / 技术总监** | AI 编程效率提升缓慢，ROI 难量化 | "夜间自动学习，白天效率可测量提升" |
| **运维负责人** | 服务器夜间空跑，资源浪费 | "利用闲置算力做 AI 自进化" |
| **开发团队 Lead** | 同样的错误 AI 反复犯 | "gate 验证的规则，不会再犯" |
| **嵌入式/C 团队** | 没有现成的 AI 测试框架 | "针对 dtest/gcov 的定制规则学习" |

### 3.3 商业模式

```
开源核心（免费）：
  - L1 distill.py（实时模式检测）
  - gate.py（验证逻辑）
  - 单机 nightly.sh

企业版（收费）：
  - 集群版分布式 harvest/replay
  - 管理员 dashboard
  - 多团队技能共享（team skills sync）
  - SLA + 部署支持
```

---

## 四、前景——三个可能的方向

### 方向 A：CC 插件赛道（最稳）

**定位：** 最好的 CC 自进化插件

```
竞品：claude-self-improving-skills, Homunculus, claude-evolving-skills
差异化：L1 实时 + L2 严格验证 + 夜间无人值守
目标用户：CC 个人开发者
商业模式：开源 + 企业版
天花板：CC 生态的头部插件
```

**优势：** 你已有代码基础，市场已被验证（Homunculus 有用户），CC 插件生态在增长
**风险：** CC 原生功能可能蚕食（如 auto-memory → 未来可能加 L1 反思）

### 方向 B：夜间学习平台（最值钱）

**定位：** AI agent 的夜间自习课

```
不只支持 CC——支持任何 LLM agent 的自进化
白天：agent 正常工作，记录操作日志
夜间：批量回放 → 模式挖掘 → gate 验证 → 技能更新
支持：CC, Codex, Copilot, Cursor, Hermes, 任意 agent
```

**优势：** 市场更大（不绑定 CC），解决闲置算力痛点
**风险：** 需要适配多种 agent 的日志格式，工程量大

### 方向 C：嵌入式 AI 测试专家（最聚焦）

**定位：** C/嵌入式领域的 AI 辅助测试学习系统

```
结合 cc-pipeline（你的另一个项目）：
白天：cc-pipeline 自动生成测试 + 跑覆盖率
夜间：skill-self-evolution 从测试结果中学习
      → 下次生成的测试质量更高
闭环：UT 生成 → 覆盖率验证 → 经验学习 → 更好的 UT
```

**优势：** 垂直场景深做，cc-pipeline + skill-self-evolution 双产品联动
**风险：** 市场较窄（嵌入式 C 团队）

### 推荐：A→C→B

```
Phase 1 (现在)：方向 A——做最好的 CC 自进化插件
  - 利用已有代码
  - 先有用户
  - 验证 L1+L2 价值

Phase 2 (3-6 月)：方向 C——结合 cc-pipeline
  - 在嵌入式 UT 场景验证闭环
  - 产出可量化的 case study

Phase 3 (6-12 月)：方向 B——平台化
  - 从 CC 扩展到多 agent
  - 企业版集群部署
```

---

## 五、核心结论

### 5.1 你做的东西有没有价值？

**有。** 理由：

1. **业界空白确实存在**——CC auto-memory 和 Hermes memory 都只做 L0（存了不管）。L1（fail→success 模式检测）+ L2（gate 验证）的组合，**没有任何主流产品同时做了**。

2. **Hermes 官方想做但还没做**——issue #337（Evolutionary Self-Improvement）和 #483（Post-Task Reflection）都还是提案。你比官方快。

3. **验证门控是核心壁垒**——SkillOpt 论文证明了"严格改进验证"的有效性。你已经在 gate.py 实现了。这是 claude-meta / CC auto-memory / Hermes memory 都没有的。

### 5.2 最大的风险

**CC 原生功能蚕食。** 如果 Anthropic 在 auto-memory 基础上加了 L1 反思 + L2 验证，你的插件价值归零。

**应对策略：**
- 不跟 CC 原生比"通用记忆"——比"**验证驱动的技能进化**"
- CC 原生不会做 gate.py 那样的留出验证集——太学术了，不适合通用产品
- 你可以成为 CC 原生功能的**补充**——auto-memory 做 L0，你做 L1+L2

### 5.3 最紧急的一步

**让 L3 sleep 从 Mock 变成 Real。** 你的 gate.py 和 consolidate.py 已经是 SkillOpt 论文的完整实现。唯一缺的是 `replay.py` 的真实 backend——用 `claude -p` 做真实 replay。

这一步走完，你就从"学术玩具"变成"可用产品"。
