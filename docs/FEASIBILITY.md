# skill-self-evolution 落地可行性评估

> 基于全部源码审读 + 实际运行产出 + 代码成熟度逐模块评估

---

## 一、逐模块成熟度评估

### 1.1 L1 distill.py — 工具级蒸馏（1125 行）

| 维度 | 状态 | 说明 |
|---|:-:|---|
| transcript 解析 | ✅ 可用 | parse_transcript 正确解析 CC JSONL 格式，两遍扫描提取 tool_use + tool_result |
| 模式检测 | ✅ 可用 | 三种模式：fail_to_success / multi_attempt / user_correction，含相似度过滤 |
| 低价值错误过滤 | ✅ 可用 | 过滤权限错误、command not found、no module named |
| 启发式规则提取 | ⚠️ 质量一般 | shlex diff 产出的规则含路径碎片，质量过滤器已加但仍有噪声 |
| LLM 规则提取 | ✅ 可用 | 调 `claude -p` 做 LLM 提取，有 60s timeout + fallback |
| 规则去重 | ✅ 可用 | SequenceMatcher > 0.75 判重复 |
| 验证门控 | ✅ 可用 | pending → verified（2nd obs）→ trusted（3+ obs），error fingerprint 匹配 |
| CLAUDE.md 安全写入 | ✅ 可用 | 保护块 `<!-- BEGIN AGENT-EXPERIENCE -->`，自动备份 |
| transcript 发现 | ✅ 可用 | 按项目路径匹配 + 时间窗口过滤 |
| **实际产出** | ⚠️ | **1 条 verified 规则**（从 55 个 tool call 中检测到 2 个模式） |

**结论：代码成熟，能跑。实际产出率低（55 calls → 2 patterns → 1 rule）。**

产出率低的原因不是 bug，而是**检测条件严格**（相似度 > 0.15 + 过滤低价值错误 + 去重）。这是设计决策不是缺陷——宁缺毋滥。

### 1.2 L3 sleep 引擎 — 离线学习（六阶段）

| 阶段 | 文件 | 行数 | 状态 | 说明 |
|---|---|---|:-:|---|
| **harvest** | harvest.py | 235 | ✅ 可用 | 正确解析 transcript → SessionDigest，过滤 headless replay 自身 |
| **mine** | mine.py | 124 | ✅ 可用 | 启发式提取 TaskRecord，train/val 自动划分（34% holdout） |
| **replay** | replay.py | 136 | 🔴 **空壳** | 只有 MockBackend（5 条硬编码假规则），无真实 LLM 调用 |
| **consolidate** | consolidate.py | 125 | ✅ 设计完整 | reflect → edit → gate 逻辑完整，但依赖 replay 的打分 |
| **gate** | gate.py | 73 | ✅ 严谨 | SkillOpt 式 strict-improvement（平手拒绝） |
| **staging** | staging.py | 96 | ✅ 可用 | manifest + report + proposed_skill/memory + backup |
| **state** | state.py | 77 | ✅ 可用 | SleepState 持久化 night 计数 + last_harvest |

**实际运行结果（night 3）：**
```
sessions harvested: 34
tasks mined: 34
held-out score: 0.545 → 0.545
gate: reject (accepted=False)
```

**结论：pipeline 骨架完整且正确运行。但 replay 用的是 MockBackend——分数 0.545 是假的。**

### 1.3 L2 任务级蒸馏

| 组件 | 状态 | 说明 |
|---|:-:|---|
| on-stop.sh | ✅ 可用 | 调 analyze_turn.py 分析复杂度 |
| analyze_turn.py | ✅ 263 行 | 统计 tool_calls + file_edits + session_length，超阈值时触发 nudge |
| skill-distiller agent | ⚠️ 未验证 | agents/skill-distiller.md 定义了 prompt，但产出质量未验证 |

**结论：触发机制能跑，蒸馏产出质量未知。**

### 1.4 Hooks 机制

| Hook | 用途 | 状态 |
|---|---|:-:|
| postToolUse | L1 实时 trace + 模式检测 | ✅ 能跑，非阻塞，后台 Popen 调 distill.py online |
| Stop | L2 触发 | ✅ 能跑，15s timeout |
| SessionStart | 注入 advisory | ✅ 能跑 |
| PreToolUse | pre-edit 备份 | ✅ 能跑 |
| PostToolUse_Edit | post-edit 记录 | ✅ 能跑 |

**结论：hooks 机制完整可用。**

### 1.5 nightly.sh

```bash
# 1. distill offline --llm  （调 CC API）
# 2. distill apply            （写 CLAUDE.md）
# 3. run-sleep.sh run         （sleep cycle，但 MockBackend）
```

**结论：第一步行得通（有真实产出）。第三行跑的是假数据。**

---

## 二、关键缺口与实现成本

### 缺口 1：replay.py 只有 MockBackend 🔴

**这是从"学术玩具"到"可用产品"的唯一硬障碍。**

需要实现的 CCBackend：

```python
class CCBackend(Backend):
    def attempt(self, task, skill, memory):
        # 调 claude -p 重做任务
        # 输入：task.intent + task.context_excerpt 作为 user prompt
        #       skill + memory 作为 system context
        # 输出：CC 的回复文本
        
    def judge(self, task, response):
        # 判分：task.outcome 是已知的（从 transcript 挖出来的）
        # 如果 task 有明确参考答案 → exact match
        # 否则 → 用 task.outcome (success/fail) 做粗粒度判分
        
    def reflect(self, failures, successes, skill, memory, *, edit_budget):
        # 调 CC 分析失败模式 → 提议 skill/memory 编辑
```

**实现成本估算：~200 行 Python，1-2 天**

核心挑战不是代码量，而是**判分质量**——transcript 挖出来的 task 大多没有标准答案（reference_kind="none"），只能用 outcome（success/fail）做粗粒度判分。这意味着 gate 的信号很弱。

### 缺口 2：判分信号弱 🟡

**现状：** mine.py 从 transcript 挖任务时，`reference_kind` 全是 `"none"`，`reference` 全空。判分只能靠 `outcome`（基于用户反馈 "thanks"/"wrong" 推断的粗标签）。

**问题：**
- 用户不说 "thanks"，success 任务会被标 "unknown"
- 用户说 "wrong" 但其实只是小问题，被标 "fail"
- 没有 ground truth → gate 的"严格改进"可能是在拟合噪声

**可选改进：**
1. **用 exit code 做判分**——如果 task 涉及 Bash 命令（编译/测试），用 exit code 判分最客观
2. **LLM judge**——用另一个 CC 调用做裁判，打分 0-1
3. **两者结合**——有 exit code 的用 exit code，没有的用 LLM judge

**成本：~100 行，但需要额外的 CC API 调用（成本）**

### 缺口 3：规则产出率低 🟡

55 个 tool call → 2 个 pattern → 1 条规则。如果用户一天用 CC 做 200 个操作，一周 1000 个操作，产出 ~18 条规则/周。

**问题：** 18 条规则里有多少是真正有用的？sed 转义这种规则非常特定，泛化性差。

**可选改进：**
1. LLM 提取作为默认（而非可选）——成本更高但泛化更好
2. 扩展检测范围——不只检测 Bash fail→success，也检测 Edit 的 diff 模式
3. 跨项目规则聚合——不同项目的同类错误合并

### 缺口 4：L2 蒸馏产出未验证 🟢

skill-distiller agent 定义了，但从未验证过产出质量。这是"锦上添花"的部分，不影响 L1+L3 的核心闭环。

### 缺口 5：仓库混乱 🟢

```
skill-self-evolution/
├── agent-experience/        ← 旧版，已被 skill-evolution 替代
├── evolving-skills/         ← 旧版，已被 skill-evolution 替代
├── skill-evolution/         ← 当前版本 ✅
├── reference/               ← SkillOpt + 其他参考项目（200+ 文件）
├── opencode-self-improving-skills/  ← OpenCode 版本
├── skill-md-evolution/      ← 调研报告
└── .opencode/               ← OpenCode 配置 + node_modules
```

用户 clone 后无法理解哪个目录是产品。需要清理。

---

## 三、可行性评估总结

### 3.1 能跑 vs 能用 vs 能卖

| 层次 | 能跑 | 能用 | 能卖 |
|---|:-:|:-:|:-:|
| **L1 distill（实时规则提取）** | ✅ | ✅ | ⚠️ 产出率待验证 |
| **L3 sleep（夜间学习循环）** | ✅ 跑通了 | 🔴 MockBackend 假数据 | ❌ 需接真实 backend |
| **L2 蒸馏（任务级技能）** | ⚠️ 触发能跑 | ❌ 产出未验证 | ❌ |
| **nightly.sh（定时编排）** | ✅ | ⚠️ sleep 段假数据 | ❌ |

### 3.2 到"可用产品"的最短路径

```
当前状态 ────────────────────→ 可用产品

  L1 能跑，有产出               L1 产出率提升
  L3 跑通但假数据      ──────→  L3 接真实 CCBackend
  无测试                        加基础测试
  仓库混乱                      清理仓库
                                
  预计工作量：1-2 周
```

### 3.3 到"能卖给客户"的路径

```
可用产品 ────────────────────→ 能卖

  L3 单机版能跑                 L3 集群版（分布式 harvest + 并行 replay）
  命令行交互                    部署文档 + 配置文件
  无监控                        每日学习报告（邮件/IM 推送）
  无量化指标                    ROI 仪表盘（效率提升可量化）
                                
  预计工作量：额外 3-4 周
```

### 3.4 技术风险矩阵

| 风险 | 概率 | 影响 | 缓解 |
|---|:-:|:-:|---|
| CCBackend 判分太弱，gate 永远不通过 | 中 | 高 | 先用 exit-code 判分（编译/测试类任务），LLM judge 做兜底 |
| transcript 数据量不够（小团队） | 高 | 中 | 支持跨项目聚合；sleep 可按周而非按天跑 |
| CC 原生功能蚕食 | 中 | 高 | 不比通用记忆，比验证驱动进化；gate.py 的留出验证是学术级壁垒 |
| 规则泛化性差（太特定） | 高 | 中 | LLM 提取做泛化，启发式做兜底 |
| 用户不信任自动写入 CLAUDE.md | 中 | 中 | staging + adopt 两步确认 + 自动备份 + diff 预览 |

---

## 四、建议的行动优先级

### P0 — 必须做才能称为"可用"

1. **实现 CCBackend（2 天）** — 用 `claude -p` 做真实 replay，exit-code + outcome 判分
2. **端到端验证（1 天）** — 真实跑一次 nightly，看 gate 是否能正常 accept/reject
3. **加 distill.py 基础测试（1 天）** — transcript 解析 + 模式检测 + 去重的核心路径
4. **清理仓库（半天）** — 删旧版目录，移 reference 到单独分支

### P1 — 做了才能称为"好用"

5. **判分增强（2 天）** — LLM judge 作为 fallback，混合 exit-code + outcome + LLM
6. **L1 产出率提升（2 天）** — LLM 提取作为默认，扩展 Edit diff 模式检测
7. **`/sleep report` 增强（1 天）** — 可读的学习报告，含 baseline→candidate 对比

### P2 — 做了才能称为"能卖"

8. **集群版 harvest（1 周）** — 多服务器各自扫描 transcript
9. **配置文件（2 天）** — YAML 配置：夜间窗口、模型、gate 阈值
10. **监控报告（2 天）** — 每日学习摘要 → Markdown / IM 推送

---

## 五、最终判断

**能不能落地？能。**

核心代码已经跑通——L1 有真实规则产出，L3 pipeline 六阶段完整且 gate 逻辑严谨。唯一的硬障碍是 replay.py 从 Mock 换成真实 CCBackend。这不复杂（~200 行），但需要真实 API 调用来验证端到端效果。

**最大不确定性：** 不是技术问题，是**判分质量问题**。从 transcript 挖出来的 task 大多没有标准答案，gate 的"严格改进"可能拟合的是噪声。这个需要实际跑几轮夜间循环，看 gate 的 accept/reject 决策是否合理。

**建议：先花 3 天做 P0（CCBackend + 端到端验证 + 基础测试），然后跑一周真实夜间循环看效果。如果 gate 能正常工作（偶尔 accept，大多 reject），说明核心逻辑成立，可以继续投入。如果 gate 永远 reject 或总是 accept，说明判分信号有问题，需要先解决判分再继续。**
