# skill-self-evolution：从学术调研到产品落地

> 核心洞察：客户的痛点不是"我想要 AI 自进化"，而是"我的服务器集群夜间空跑，电费和人力的沉没成本让我肉疼"。skill-self-evolution 的产品价值 = **把夜间闲置算力转化为 AI 生产力提升**。

---

## 一、重新定义产品定位

### 不要说

"让 Claude Code 自动学习技能的插件"

### 要说

**"服务器集群夜间学习系统——白天你的 AI 团队干活，晚上 AI 自己复盘提升，第二天效率更高。"**

```
客户买的不是"skill 自进化"
客户买的是"闲置算力变现"——夜间电费/折旧已经花了，
与其空跑不如让 AI 自己变强
```

### 与已有调研的关系

你的 `skill-md-evolution/report.zh.md`（22 个研究对象）已经清楚地证明了：

1. **SkillOpt（Microsoft）**——文本空间 SGD，留出验证门控 ✅ 你的 gate.py 已实现
2. **ExpeL**——fail→success 模式蒸馏 ✅ 你的 distill.py L1 已实现
3. **SkillOpt-Sleep**——夜间 sleep cycle ✅ 你的 cycle.py 框架已有
4. **Homunculus / OpenSpace**——eval→improve→rollback 循环 ✅ 已参考

**你不需要再调研了。你需要的是选一条路走到黑。**

---

## 二、选哪条路？——基于"夜间闲置算力"场景

### 2.1 三个候选路径

| 路径 | 基于 | API 成本 | 验证成熟度 | 匹配场景 |
|---|---|---|:-:|---|
| **A. L1 distill 增强** | ExpeL + 你已有代码 | 零（纯启发式）/ 低（LLM 可选） | ✅ 已跑通 1 条规则 | 单机开发者 |
| **B. L3 sleep + 真实 replay** | SkillOpt-Sleep | **高（夜间批量 CC 调用）** | ⚠️ 只有 MockBackend | **服务器集群** |
| **C. L1+L3 融合** | ExpeL + SkillOpt | 中（L1 免费，L3 夜间批量） | ✅ L1 已跑通，L3 需接 | **最佳路径** |

### 2.2 推荐：路径 C——"夜间自习课"

```
白天（实时）：
  L1 distill 零成本运行
    PostToolUse hook → 记录 fail→success 模式
    零 API 调用（启发式提取）
    产出：pending 规则 → rules.json

夜间（批量）：
  L3 sleep 利用闲置算力
    harvest 白天的 transcript → mine 任务
    用真实 CC 调用 replay → 计算 baseline 分
    反思失败 → 提议技能/规则编辑
    gate 验证 → 只接受严格改进
    stage → 等用户确认 adopt

第二天早上：
  用户 /sleep status → 看到提升报告
  /sleep adopt → 采纳（带备份）
  AI 带着更强的技能继续干活
```

### 2.3 为什么这个路径对客户有吸引力

| 客户顾虑 | 我们的回答 |
|---|---|
| "夜间算力浪费" | 正好用来自进化，零额外成本 |
| "AI 生成的规则靠谱吗" | gate.py 严格验证——平手都拒绝 |
| "会不会改坏 CLAUDE.md" | 保护块 + 暂存机制 + 自动备份 |
| "怎么知道有没有效果" | baseline → candidate 分数对比报告 |
| "API 费用呢" | 夜间批量调用，利用闲置服务器上的 API 额度 |

---

## 三、需要做的关键改造

### 3.1 L1 distill.py：从"能跑"到"好用"（优先级最高）

**现状：** 1125 行，1 条规则产出，启发式提取质量一般。

**改造方向：**

```
1. 扩展模式检测
   - 现在：只检测 Bash fail→success
   - 扩展：Edit/Write 的 diff 模式（写了→改了→过了）
   - 扩展：Read 失败→Bash 查找→Read 成功（查找路径模式）

2. 启发式提取增强
   - 现在：shlex diff → 简单 "add: xxx" 规则
   - 扩展：按错误类型分类的模板
     - 编译错误 → "编译失败时检查 xxx"
     - import 错误 → "找不到模块时检查 xxx"
     - 权限错误 → 过滤（已有）
     - 超时 → "超时时改用 xxx"

3. 规则质量评分
   - 现在：confidence 固定 0.8
   - 改进：基于 pattern_type × similarity × delta_complexity 动态评分
```

### 3.2 L3 sleep：接真实 Backend（核心突破）

**现状：** `replay.py` 只有 MockBackend（5 条硬编码假规则），`cycle.py:86` 写着 `# TODO: real backends`。

**改造方案——CCBackend：**

```python
class CCBackend(Backend):
    """用真实 Claude Code CLI 做 replay"""
    
    def attempt(self, task, skill, memory):
        """
        用 skill + memory 作为 system prompt
        用 task.intent 作为 user prompt
        调用 claude -p --model <model> 获取回复
        """
        full_prompt = f"{skill}\n\n{memory}\n\n---\nTask: {task.intent}"
        result = subprocess.run(
            ["claude", "-p", full_prompt, "--output-format", "text",
             "--model", self.model],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout
    
    def judge(self, task, response):
        """
        判分策略（按 task.reference_kind 分支）：
        
        1. exact（有标准答案）：
           - hard: 精确匹配 → 1.0/0.0
           - soft: 关键词覆盖率
           
        2. outcome（基于成败标签）：
           - 直接用 task.outcome（success/fail/mixed）
           
        3. llm_judge（无标准答案）：
           - 用另一个 CC 调用做裁判
           - prompt: "给定任务和回复，打分 0-1"
        """
```

### 3.3 从 transcript 到 TaskRecord：mine.py 增强

**现状：** `mine.py` 把 transcript 摘要成 TaskRecord（intent + reference + tags）

**增强方向：**

```python
# 现在的 mine.py 基本是简单摘要
# 需要增强为：

1. 从 transcript 提取结构化任务
   - 用户请求（intent）
   - 最终产出（reference）
   - 成功/失败标签（outcome）
   - 涉及的工具序列（tags）

2. 任务分类
   - 编译/构建类 → 可用 make/gcc exit code 判分
   - 测试类 → 可用 pytest exit code 判分
   - 代码编辑类 → 可用 git diff 质量判分
   - 调查/分析类 → 只能用 LLM judge

3. train/val 自动划分
   - 按时间切：最近 70% train，30% val
   - 按类型分层：确保 val 中各类型都有
```

---

## 四、产品形态

### 4.1 单机版（开发者用）

```bash
# 安装
ln -s /path/to/skill-evolution ~/.claude/plugins/skill-evolution

# 白天：自动运行（零成本）
# PostToolUse hook 自动记录模式
# /distill offline  手动扫描

# 夜间：cron 定时
17 3 * * * bash /path/to/nightly.sh /your/project

# 早上：查看结果
/sleep status
/sleep adopt
```

### 4.2 集群版（企业用——你说的场景）

```
┌──────────────────────────────────────────────────┐
│              服务器集群（夜间 22:00-06:00）          │
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Server A │  │ Server B │  │ Server C │  ...   │
│  │ 白天：CC │  │ 白天：CC │  │ 白天：CC │        │
│  │ 夜间：   │  │ 夜间：   │  │ 夜间：   │        │
│  │ harvest  │  │ replay   │  │ reflect  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │               │
│       └─────────────┼─────────────┘               │
│                     ▼                             │
│            ┌──────────────┐                       │
│            │  Gate 验证    │                       │
│            │  (中央服务器)  │                       │
│            └──────┬───────┘                       │
│                   │                               │
│            ┌──────▼───────┐                       │
│            │  Stage 提议   │                       │
│            │  (等待人工   │                        │
│            │   adopt)     │                       │
│            └──────────────┘                       │
└──────────────────────────────────────────────────┘
```

**集群版的关键设计：**

1. **分布式 harvest**——每台服务器各自扫描自己的 transcript
2. **并行 replay**——多台服务器并行跑 replay（加速）
3. **集中 gate**——结果汇总到中央服务器做门控决策
4. **统一 staging**——提议的技能更新统一暂存，管理员审批

### 4.3 客户价值量化

```
假设：
  - 10 台服务器，夜间 8 小时空闲
  - 每天 harvest ~50 个任务
  - replay 每个任务 1 次 = 50 次 CC 调用
  - reflect 产出 ~5 条编辑
  - gate replay ~5 次 = 5 次 CC 调用
  - 总计：~55 次 CC 调用/夜

效果：
  - 每周 ~350 次夜间学习
  - 假设 10% 的编辑通过 gate = ~3.5 条改进/周
  - 一个月后 ~14 条经验规则
  - 覆盖编译/测试/调试等高频场景
  
ROI：
  夜间电费/折旧 = 已沉没（不花白不花）
  API 调用 = 55 次/夜 × token 成本 ≈ 几块钱
  效果 = AI 团队效率提升（减少重复错误）
```

---

## 五、与竞品的差异化

| 竞品 | 他们做了什么 | 你怎么做不同 |
|---|---|---|
| **SkillOpt** | 学术验证，需要 benchmark 数据集 | **不需要 benchmark**——从真实 transcript 学习 |
| **Homunculus** | nightly agent，单机 | **集群版**——分布式并行 replay |
| **claude-self-improving-skills** | 会话级蒸馏 | **+ gate 验证**——SkillOpt 式留出验证 |
| **OpenSpace** | DAG 版本化 + SQLite | **+ Git 原生**——用 git tag 做版本 |
| **SkillOpt-Sleep 插件** | 官方 sleep 插件 | **+ L1 实时**——白天也有免费学习 |

你的核心差异化：**唯一同时覆盖实时（L1 免费）+ 夜间（L3 闲置算力）+ 严格验证（gate.py）的产品**。

---

## 六、开发路线图

### Phase 1：L1 增强（2 周，零 API 成本）

- [ ] distill.py 加测试（transcript 解析、模式检测、规则去重）
- [ ] 扩展模式检测（Edit/Write diff 模式）
- [ ] 启发式提取增强（按错误类型分类模板）
- [ ] `/distill report` 可视化命令增强
- [ ] 清理仓库（删掉 agent-experience/ 和 evolving-skills/）

### Phase 2：L3 接真实 Backend（2 周，需要 API）

- [ ] 实现 CCBackend（用 `claude -p` 做真实 replay）
- [ ] mine.py 增强（结构化任务提取 + train/val 划分）
- [ ] LLM judge（无标准答案时的判分）
- [ ] 端到端验证：真实 transcript → sleep → gate → 可度量改进

### Phase 3：集群版（4 周）

- [ ] 分布式 harvest（每台服务器各自扫描）
- [ ] 并行 replay 协调（Redis/文件锁）
- [ ] 集中 gate + 统一 staging
- [ ] 管理员 dashboard（Markdown 报告 → Web UI）
- [ ] 客户部署文档

### Phase 4：产品化（2 周）

- [ ] 一键安装脚本（集群版）
- [ ] 配置文件（YAML：夜间时间窗口、API 模型、gate 阈值）
- [ ] 监控（每晚学习报告 → 邮件/IM 推送）
- [ ] README 重写（从"插件"改为"夜间学习系统"）

---

## 七、给客户讲的故事

### 一句话

> "你的服务器晚上在空转。我们让它利用夜间时间自动学习，白天 AI 团队效率更高。不需要额外投资硬件，不需要改变白天的工作流程。"

### 30 秒电梯演讲

> "你们有 10 台服务器跑 AI 编程，白天满负荷，晚上全闲着。我们的系统在夜间自动回放白天的 AI 操作记录，找出哪些地方犯了重复错误，提炼成经验规则，经过严格验证后更新到 AI 的'操作手册'里。第二天，你的 AI 团队就不会犯同样的错误了。成本就是夜间的 API 调用费——因为服务器电费和折旧你已经花了。"

### 量化指标（演示用）

```
部署前：
  - AI 重复犯错率：X%（基于 transcript 统计）
  - 编译/测试一次性通过率：Y%

部署 4 周后：
  - 新增经验规则：~14 条（经验证的）
  - 重复犯错率：X × 0.7（降低 30%）
  - 一次性通过率：Y + 15pp
  - 夜间算力利用率：0% → 85%
```
