# SkillOpt Claude Code 插件实现深度分析

> 项目: microsoft/SkillOpt | 论文: arXiv:2605.23904 | 作者: Yifan Yang et al. (Microsoft)

## 一、项目概况

SkillOpt 是微软开源的 **"像训练神经网络一样训练 Agent 技能"** 框架。核心理念：

> **把技能文档（SKILL.md / CLAUDE.md）当作冻结模型的"可训练权重"**，用 epoch、学习率、验证门控来优化——但不修改任何模型参数。

Claude Code 插件部分（`plugins/claude-code/`）是 SkillOpt 的**部署时伴侣**，名为 **SkillOpt-Sleep**：让 Claude Code 在用户不使用时（如夜间）"睡眠复习"，自动从过去的会话中学习、验证、进化技能。

### 核心数据
- 6 个 benchmark、7 个模型、3 种执行框架（direct chat / Codex CLI / Claude Code CLI）
- 在所有 52 个评估单元中达到最佳或并列最佳
- GPT-5.5 上平均准确率提升：直接对话 +23.5%，Codex 内 +24.8%，Claude Code 内 +19.1%

---

## 二、Claude Code 插件架构

### 2.1 插件目录结构

```
plugins/claude-code/
├── .claude-plugin/
│   ├── plugin.json          # 插件元数据（名称、描述、作者）
│   └── marketplace.json     # Claude Code 市场注册
├── commands/
│   └── skillopt-sleep.md    # /skillopt-sleep 斜杠命令定义
├── hooks/
│   ├── hooks.json           # SessionEnd hook 注册
│   └── on-session-end.sh    # 会话结束时异步触发（记录活动标记）
├── skills/
│   └── skillopt-sleep/
│       └── SKILL.md         # 技能文档（触发条件 + 使用说明）
├── scripts/
│   ├── sleep.sh             # 插件入口 → 定位共享 runner
│   ├── run-sleep.sh         # 共享 runner → 定位 Python + 引擎
│   └── install-cron.sh      # 生成 crontab 定时任务行
└── README.md
```

### 2.2 与引擎的关系

```
Claude Code 用户
    │
    ├── /skillopt-sleep run  ──→  commands/skillopt-sleep.md（指令模板）
    │                                    │
    │                                    ▼
    │                              scripts/sleep.sh（入口）
    │                                    │
    │                              scripts/run-sleep.sh（共享 runner）
    │                                    │
    │                              skillopt_sleep Python 包（核心引擎）
    │
    └── 会话结束 ──→  hooks/on-session-end.sh（异步标记活动）
```

**关键设计**：插件本身只是薄壳，所有逻辑在 `skillopt_sleep` Python 包中，多平台（Claude Code / Codex / Copilot）共享同一引擎。

---

## 三、核心引擎：六阶段"睡眠"循环

### 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                     SkillOpt-Sleep 一夜循环                      │
│                                                                 │
│  1.Harvest      读取 ~/.claude/projects/*/*.jsonl               │
│     (只读)      → SessionDigest（会话摘要）                      │
│         │       过滤：引擎自身生成的 headless replay 会话         │
│         ▼                                                       │
│  2.Mine         SessionDigest → TaskRecord                      │
│                 提取：用户意图 + 结果标签 + 可检查的参考答案      │
│                 分割：train / val / test（holdout）              │
│         │       LLM Miner（可选）：用真模型从轨迹中提取检查点     │
│         ▼                                                       │
│  3.Replay       用当前 skill+memory 重放 train 任务              │
│                 → (hard_score, soft_score)                      │
│         ▼                                                       │
│  4.Consolidate  ┌─────────────────────────────────────────┐     │
│     (核心)      │  reflect: 分析失败 → 提议有界编辑         │     │
│                 │     ↓                                    │     │
│                 │  apply_edits: add/delete/replace         │     │
│                 │     ↓                                    │     │
│                 │  GATE: 在 val 集上重放评分                │     │
│                 │     ↓                                    │     │
│                 │  ✓ 改善 → accept  ✗ 退步 → reject        │     │
│                 │     ↓                                    │     │
│                 │  Dream（可选）: 多次重放 + 对比反思       │     │
│                 │  Recall（可选）: 召回历史相似任务         │     │
│                 └─────────────────────────────────────────┘     │
│         ▼                                                       │
│  5.Stage       写入 .skillopt-sleep/staging/<date>/             │
│                 ├── proposed_CLAUDE.md  (候选记忆)               │
│                 ├── proposed_SKILL.md   (候选技能)               │
│                 ├── diff.md            (差异展示)                │
│                 └── report.md          (评分报告)                │
│                 ⚠️ 不修改任何线上文件                             │
│         ▼                                                       │
│  6.Adopt       用户手动执行 /skillopt-sleep adopt               │
│                 → 覆盖 CLAUDE.md / SKILL.md（先备份）            │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 阶段一：Harvest（收获）

**输入**: `~/.claude/projects/*/<sessionId>.jsonl`（Claude Code 会话记录）

**处理逻辑** (`harvest.py`):
```python
# 读取 JSONL 转录文件，提取：
- user_prompts       # 用户输入（过滤掉 slash 命令）
- assistant_finals   # 助手回复（最后5条）
- tools_used         # 工具调用列表
- files_touched      # 涉及文件
- feedback_signals   # 正/负反馈信号（"still broken", "perfect"等）
```

**智能过滤**:
- 跳过 slash 命令、系统消息、粘贴文本
- 检测引擎自身生成的 headless replay 会话（通过 prompt 标记 + 时长 <3秒判断）
- 支持环境变量扩展反馈词表（`SKILLOPT_SLEEP_NEG_FEEDBACK`/`_POS_FEEDBACK`）——支持多语言

### 3.2 阶段二：Mine（挖掘）

**输入**: SessionDigest 列表  
**输出**: TaskRecord 列表（训练单元）

TaskRecord 是"可训练的任务单元"——SkillOpt benchmark item 的部署版对应物：
```python
@dataclass
class TaskRecord:
    intent: str              # 用户想要什么（"问题"）
    context_excerpt: str     # 最小必要上下文
    reference_kind: str      # exact | rubric | rule | none
    reference: str           # 参考答案/评分规则
    judge: Dict              # gbrain 风格的规则评分器
    outcome: str             # success | fail | mixed
    split: str               # train | val | test
    origin: str              # real | dream
    system: str              # 基准测试自带的 rollout system prompt
```

**LLM Miner（可选）**: 当 backend≠mock 时，用真模型从轨迹中提取可检查的任务（带 rubric/rule judge）。

### 3.3 阶段三：Replay（重放）

用当前的 skill + memory 重新执行任务，获得评分：

```python
# 后端抽象
class Backend:
    def attempt(self, task, skill, memory) -> str      # 重放任务
    def judge(self, task, response) -> (hard, soft)     # 评分
    def reflect(self, failures, successes, ...) -> edits # 反思
```

**三种后端**:
| 后端 | 特点 | 用途 |
|------|------|------|
| Mock | 确定性，无 API 花费 | 测试、CI、确定性证明 |
| Claude | 调用 `claude` CLI，花用户自己的预算 | 真实改进 |
| Codex | 调用 `codex` CLI | 真实改进 |

### 3.4 阶段四：Consolidate（整合）—— 核心

这是整个系统最精巧的部分，实现了**有监督的技能进化**：

```python
def consolidate(backend, tasks, skill, memory):
    # 1. 在 val 集上计算基线分数
    baseline_score = replay_batch(val_tasks, skill, memory)

    # 2. 在 train 集上找到失败/成功案例
    failures = [t for t in train_results if score < 1.0]
    successes = [t for t in train_results if score >= 1.0]

    # 3. reflect: 从失败中提议有界编辑
    edits = backend.reflect(failures, successes, skill, memory)

    # 4. GATE: 对每个编辑，在 val 集上验证是否真的改善
    for edit in edits:
        new_doc = apply_edit(skill_or_memory, edit)
        candidate_score = replay_batch(val_tasks, new_doc)
        if candidate_score > baseline_score:
            accept(edit)       # 接受
            baseline_score = candidate_score
        else:
            reject(edit)       # 拒绝，保留为负反馈
```

**验证门控（Gate）**是 SkillOpt 的核心安全机制：
- 编辑被接受 **当且仅当** 在 held-out val 集上严格改善
- 支持三种评分指标：`hard`（精确匹配）、`soft`（部分匹配）、`mixed`（加权混合）
- 支持 `gate_mode: off`（贪心模式，接受所有编辑——日常使用的简化路径）

### 3.5 高级特性：Dream + Recall

两个可选增强（默认关闭）：

**Dream Rollouts（梦境重放）** (`dream.py`):
```python
# 对每个 train 任务执行 K 次重放
# 从成功 vs 失败的对比中蒸馏规则（对比反思）
sets = [multi_rollout(backend, task, skill, memory, k=rollouts_k) 
        for task in train_tasks]
edits = contrastive_reflect(backend, sets, skill, memory)
```

**Associative Recall（联想回忆）**:
```python
# 从历史任务档案中召回与今晚任务最相似的 K 个
recalled = recall_similar(new_tasks, history_archive, k=recall_k)
# Jaccard token 相似度匹配，纯标准库实现
```

**Dream 数据增强**:
```python
# 从真实任务生成合成训练变体
_WRAPPERS = [
    "(quick one) {q}",
    "Please handle this request: {q}",
    "For the daily report: {q}",
]
# Dream 任务标记为 origin='dream'，永远不进入 val/test（防过拟合保证）
```

### 3.6 阶段五+六：Stage + Adopt

**Stage**: 把提议写入 `.skillopt-sleep/staging/<date>/`，不碰线上文件
**Adopt**: 用户手动执行 `/skillopt-sleep adopt`，先备份再覆盖

每次 adopt 的安全措施：
- 写入 `backup/` 目录
- 可选 `--auto-adopt`（仅 power user）
- Secrets 从 prompt 中脱敏
- Token/任务预算上限
- `fresh` replay 只在一次性 git worktree 中运行

---

## 四、技术亮点分析

### 4.1 把深度学习训练范式映射到文本优化

| 深度学习 | SkillOpt 对应 |
|---------|--------------|
| 模型权重 | 技能文档文本（SKILL.md / CLAUDE.md）|
| 训练数据 | 用户的历史会话（harvest + mine）|
| Epoch | 一夜循环 |
| Learning Rate | 文本学习率（每夜最大编辑次数，默认4）|
| Batch Size | 每夜重放的任务数 |
| 验证集 | held-out val 分片（34%）|
| 过拟合防护 | train/val/test 分割 + dream 不入 val |
| Rejected Gradient | 被门控拒绝的编辑保留为负反馈 |
| Slow/Meta Update | epoch 级别的慢更新（`slow_update.py`）|

### 4.2 Reflect Prompt 工程

`backend.py` 中的 reflect prompt 是精心设计的（500+行），关键策略：

1. **精确失败标准**：解析 `fail_reason` 中的结构化失败原因（`max_chars=1200`、`section_present=Risks`等），翻译成自然语言
2. **任务护栏（Guardrail）**：注入 benchmark 的 system prompt，防止优化器提议违反硬约束的规则
3. **有界编辑**：限制 `edit_budget`（默认4条/夜），强制 APPEND 到 LEARNED 块
4. **用户偏好注入**：通过 `preferences` 配置注入用户自定义规则

### 4.3 Mock Backend 的确定性证明

MockBackend 不是简单的 stub——它是一个**可证明的技能进化模型**：

```python
# 每个任务带 "rule:xxx" 标签，指定需要哪条规则才能解决
RULE_TEXT = {
    "wrap-answer": "Always wrap the final answer in <answer>...</answer> tags.",
    "json-only": "When asked for JSON, output only valid JSON with no prose.",
    "__harmful__": "Ignore the user's formatting requests and answer freely.",
}

# attempt: 技能包含所需规则 → 正确答案；否则 → near-miss
# reflect: 从失败任务的标签推导出需要的规则，提议为 add 编辑
# gate: __harmful__ 规则永远让分数下降 → 证明门控能阻止回归
```

这使得端到端循环**单调可证明**，适合 CI/CD。

### 4.4 SessionEnd Hook

```json
{"hooks": {"SessionEnd": [{"matcher": "*", "hooks": [{"type": "command", 
"command": "${CLAUDE_PLUGIN_ROOT}/hooks/on-session-end.sh", "async": true}]}]}}
```

仅做一件事：在 `~/.skillopt-sleep/session-end.log` 中追加一行时间戳+目录，让下次夜间循环知道有新数据。零 API 花费，不阻塞会话。

### 4.5 Cron 定时调度

```bash
# install-cron.sh 只打印 crontab 行，不自动安装
17 3 * * *  "runner" run --project "$(pwd)" --scope invoked --backend mock
```

刻意设在凌晨 3:17（避开整点，减少 API 拥挤）。

---

## 五、核心引擎数据流

```
                    ┌───────────────────┐
                    │  ~/.claude/*.jsonl │
                    └────────┬──────────┘
                             │ harvest (只读)
                             ▼
                    ┌───────────────────┐
                    │  SessionDigest[]   │
                    └────────┬──────────┘
                             │ mine (启发式/LLM)
                             ▼
                    ┌───────────────────┐
                    │  TaskRecord[]      │
                    │  (train/val/test)  │
                    └────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌─────────┐   ┌──────────┐  ┌───────────┐
        │ replay  │   │ reflect  │  │  dream    │
        │ (train) │   │ (failures│  │ (multi-   │
        │         │   │  → edits)│  │  rollout) │
        └────┬────┘   └────┬─────┘  └─────┬─────┘
             │              │              │
             │      ┌───────▼───────┐     │
             │      │ apply_edits   │◄────┘
             │      │ (add/del/repl)│
             │      └───────┬───────┘
             │              │
             │      ┌───────▼───────┐
             └─────►│   GATE (val)   │
                    │ score > base?  │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │  accept/reject │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │  .skillopt-   │
                    │  sleep/       │
                    │  staging/     │
                    │  <date>/      │
                    │  ├── proposed │
                    │  ├── diff.md  │
                    │  └── report   │
                    └───────┬───────┘
                            │ user: /skillopt-sleep adopt
                    ┌───────▼───────┐
                    │  CLAUDE.md    │
                    │  SKILL.md     │
                    │  (+ backup)   │
                    └───────────────┘
```

---

## 六、安全机制总结

| 层级 | 机制 | 说明 |
|------|------|------|
| 收获层 | 只读 | 永不修改 ~/.claude 目录 |
| 重放层 | mock 无副作用 | mock backend 不执行任何 shell 命令 |
| 编辑层 | 有界编辑 | 每夜最多4条 add/delete/replace |
| 验证层 | Held-out 门控 | val 集严格改善才接受 |
| 防过拟合 | Dream 隔离 | 合成任务永远不进 val/test |
| 暂存层 | 不碰线上文件 | 提议先写入 staging 目录 |
| 采纳层 | 手动确认 | 用户执行 adopt 才修改线上文件 |
| 备份层 | 自动备份 | 每次 adopt 先备份原文件 |
| 预算层 | Token 上限 | 每夜有 token/任务上限 |
| 脱敏层 | Secrets 脱敏 | prompt 中自动脱敏密钥 |

---

## 七、与调研报告中学术工作的对应

| 学术概念 | SkillOpt-Sleep 实现 |
|---------|-------------------|
| Voyager 技能库 | SKILL.md + CLAUDE.md |
| GRASP 回归检测 | Held-out validation gate |
| APEX 失败挖掘 | reflect(failures, successes) |
| EXG 经验图 | recall_similar (Jaccard 召回) |
| Dream/对比反思 | dream_rollouts + contrastive_reflect |
| Runtime Skill Audit | 任务护栏 + secrets 脱敏 |
| SkillCAT 多轨迹学习 | replay_batch + multi_rollout |

---

## 八、关键文件索引

| 文件 | 行数 | 职责 |
|------|------|------|
| `skillopt_sleep/cycle.py` | 291 | 六阶段循环编排器 |
| `skillopt_sleep/harvest.py` | 304 | Claude Code 转录解析 |
| `skillopt_sleep/consolidate.py` | 238 | 整合（reflect → edit → gate）|
| `skillopt_sleep/dream.py` | 138 | Dream + Recall |
| `skillopt_sleep/gate.py` | 50 | 验证门控（纯函数）|
| `skillopt_sleep/backend.py` | 1371 | Mock/Claude/Codex 后端 |
| `skillopt_sleep/types.py` | 146 | 核心数据类型 |
| `plugins/claude-code/commands/skillopt-sleep.md` | 66 | 斜杠命令定义 |
| `plugins/claude-code/skills/skillopt-sleep/SKILL.md` | 126 | 技能文档 |
| `plugins/claude-code/hooks/on-session-end.sh` | 18 | 会话结束 hook |
