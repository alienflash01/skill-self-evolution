# evolving-skills — 双层蒸馏技能自进化系统

> Claude Code 插件 | 融合 self-improving-skills × SkillOpt-Sleep × evolving-skills

## 设计理念

**在线蒸馏**（实时）× **离线蒸馏**（深度）× **记忆整合**（Claude Code 原生）

```
┌─────────────────────────────────────────────────────────────────┐
│                    在线蒸馏（ONLINE）                              │
│            "工作时的即时学习 — 快速、轻量"                           │
│                                                                 │
│  Stop hook 检测复杂工作（≥12工具调用 + ≥2文件编辑）                   │
│    → 一次性 BLOCK，提醒委派 skill-distiller 子代理                  │
│    → 子代理：patch现有 > 补充umbrella > 新建                        │
│    → PreToolUse 备份 → PostToolUse 验证+盖章                       │
│    → 写入 ~/.claude/skills/<name>/SKILL.md                       │
│    → 标记 origin: online-distill                                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │ 积累
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    离线蒸馏（OFFLINE）                             │
│          "夜间深度复习 — 验证门控、进化树追踪"                        │
│                                                                 │
│  定时触发（cron / 手动 /sleep run）                                │
│    → harvest：读取 ~/.claude 会话转录（只读）                       │
│    → mine：提炼反复出现的任务模式                                    │
│    → replay：用当前 skill+memory 离线重放                           │
│    → reflect：分析失败 → 提议有界编辑                               │
│    → GATE：held-out 验证 — 改善才接受 ⭐                            │
│    → stage：暂存提议（不碰线上文件）                                 │
│    → adopt：用户确认后采纳（带备份）                                 │
│    → 写入 CLAUDE.md + SKILL.md 受保护区                            │
│    → 进化树更新（evolution-tree.jsonl）                            │
└───────────────────────┬─────────────────────────────────────────┘
                        │ 整合
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    记忆整合（MEMORY）                              │
│         "Claude Code 原生记忆 + 技能的统一管理"                      │
│                                                                 │
│  CLAUDE.md（项目记忆）                                             │
│    <!-- EVOLVING-SKILLS:LEARNED START -->                       │
│    受保护区：离线蒸馏产出的持久规则                                  │
│    <!-- EVOLVING-SKILLS:LEARNED END -->                          │
│                                                                 │
│  SKILL.md（技能文件）                                              │
│    metadata.provenance: evolving-skills                          │
│    metadata.origin: online-distill | offline-sleep               │
│                                                                 │
│  治理                                                             │
│    curator 状态机：active → stale(30d) → archived(90d)            │
│    pinned 技能永不清理                                             │
│    进化树：每次变更的 parent → child 追踪                           │
└─────────────────────────────────────────────────────────────────┘
```

## 双层对比

| 维度 | 在线蒸馏 | 离线蒸馏 |
|------|---------|---------|
| **触发** | Stop hook（实时） | cron / 手动命令 |
| **延迟** | 即时（秒级） | 深度（分钟级） |
| **成本** | 1次子代理调用 | 多次 replay + gate |
| **验证** | frontmatter 校验 | held-out 门控 |
| **写入** | 直接写 SKILL.md | stage → adopt |
| **来源** | 当前会话 | 历史所有会话 |
| **适合** | 鲜活的即时经验 | 反复出现的模式提炼 |

## 文件结构

```
evolving-skills/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── hooks/
│   ├── hooks.json               # Stop + SessionStart + PreToolUse + PostToolUse
│   ├── on-stop.sh               # 在线蒸馏触发
│   ├── on-session-start.sh      # 上下文注入
│   ├── on-pre-edit.sh           # 编辑前备份
│   └── on-post-edit.sh          # 编辑后验证
├── agents/
│   └── skill-distiller.md       # 在线蒸馏子代理
├── commands/
│   ├── distill-skill.md         # 手动触发在线蒸馏
│   ├── sleep.md                 # 离线蒸馏控制
│   ├── curator-status.md        # 治理状态
│   ├── curate-skills.md         # 手动整理
│   ├── prune-skills.md          # 清理过时技能
│   ├── pin-skill.md             # 固定技能
│   └── restore-skill.md         # 恢复归档技能
├── skills/
│   └── evolving-skills/
│       └── SKILL.md             # 插件自身说明技能
├── scripts/
│   ├── analyze_turn.py          # Stop hook 分析器
│   ├── validate_skill.py        # PostToolUse 验证器
│   ├── backup_skill.py          # PreToolUse 备份器
│   ├── session_init.py          # SessionStart 初始化
│   ├── usage_store.py           # 使用遥测存储
│   ├── curator_transitions.py   # curator 状态机
│   ├── curator_backup.py        # 归档前快照
│   ├── sleep/
│   │   ├── cycle.py             # 离线六阶段循环
│   │   ├── harvest.py           # 阶段1：收获
│   │   ├── mine.py              # 阶段2：挖掘
│   │   ├── replay.py            # 阶段3：重放
│   │   ├── consolidate.py       # 阶段4：整合（reflect→gate）
│   │   ├── gate.py              # 验证门控（纯函数）
│   │   ├── staging.py           # 阶段5：暂存
│   │   ├── memory.py            # 受保护区编辑
│   │   ├── state.py             # 跨夜持久状态
│   │   └── types.py             # 数据类型
│   ├── run-sleep.sh             # 离线蒸馏入口
│   └── install-cron.sh          # 定时安装
├── tests/
│   └── test_smoke.py            # 冒烟测试
├── README.md
└── install.sh
```

## 在线蒸馏流程（详细）

```
Claude Code 会话进行中
    │
    ├── 工具调用、文件编辑不断积累
    │
    ▼
会话停止（Stop 事件）
    │
    ▼
on-stop.sh → analyze_turn.py
    │
    ├── 读取 transcript JSONL
    ├── 找到"上次蒸馏锚点"（上次 distill 委派 或 SKILL.md 编辑）
    ├── 统计锚点之后的：工具调用数、文件编辑数
    ├── 检查 stop_hook_active（防循环）
    │
    ├── 工具调用 < 12 或 文件编辑 < 2 → approve（放行）
    │
    └── 达到阈值且未蒸馏 →
        emit {"decision":"block", "reason":"...提示委派 skill-distiller..."}
        记录 nudge（同一段不重复提醒）
            │
            ▼
        Claude 委派 skill-distiller 子代理
            │
            ├── 读 transcript 尾部，理解做了什么
            ├── Glob ~/.claude/skills/**/SKILL.md
            ├── 决策：patch > umbrella > references > 新建 > 放弃
            ├── Edit/Write SKILL.md
            │     ├── PreToolUse → backup_skill.py（备份原文件）
            │     └── PostToolUse → validate_skill.py（验证+盖章）
            │
            └── 报告：patched/created/declined + 一行说明
```

## 离线蒸馏流程（详细）

```
触发：/sleep run | cron 3:17am | /sleep dry-run
    │
    ▼
run-sleep.sh → python -m evolving_skills.sleep.cycle
    │
    ├── 1. HARVEST（只读）
    │   读 ~/.claude/projects/*/*.jsonl
    │   提取：user_prompts, assistant_finals, tools, feedback_signals
    │   过滤：slash命令、headless replay会话
    │   → SessionDigest[]
    │
    ├── 2. MINE
    │   SessionDigest → TaskRecord
    │   启发式：首次prompt=意图，反馈=标签，追问=上下文
    │   分割：train(66%) / val(34%)（稳定哈希）
    │   → TaskRecord[]
    │
    ├── 3. REPLAY
    │   用当前 skill+memory 重放 train 任务
    │   → (hard_score, soft_score)
    │
    ├── 4. CONSOLIDATE（核心）
    │   val集基线评分
    │   train集 reflect → 提议有界编辑（add/delete/replace）
    │   GATE：每个编辑在 val集上重放验证
    │     ✅ 改善 → accept
    │     ❌ 退步 → reject（保留为负反馈）
    │
    ├── 5. STAGE
    │   写入 .evolving-skills/staging/<date>/
    │   ├── proposed_CLAUDE.md
    │   ├── proposed_SKILL.md
    │   ├── report.md
    │   └── manifest.json
    │   ⚠️ 不碰线上文件
    │
    └── 6. ADOPT（用户确认）
        /sleep adopt
        → 备份原文件
        → 覆盖 CLAUDE.md / SKILL.md
        → 更新进化树
```

## 配置

```bash
# 在线蒸馏阈值
SIS_DISTILL_THRESHOLD=12        # 工具调用数阈值
SIS_MIN_FILE_EDITS=2            # 最小文件编辑数

# 离线蒸馏
ES_SLEEP_BACKEND=mock           # mock | claude | codex
ES_SLEEP_LOOKBACK_HOURS=72      # 收获回溯窗口
ES_SLEEP_EDIT_BUDGET=4          # 每夜最大编辑数
ES_SLEEP_GATE_MODE=on           # on | off
ES_SLEEP_AUTO_ADOPT=false       # 自动采纳

# 治理
SIS_STALE_AFTER_DAYS=30
SIS_ARCHIVE_AFTER_DAYS=90
SIS_CURATE_INTERVAL_DAYS=7
```

## 与 Claude Code 记忆机制的配合

### CLAUDE.md 分层

```markdown
# 项目记忆（用户手写 — 永不触碰）
...用户的原始内容...

<!-- EVOLVING-SKILLS:LEARNED START -->
## Learned preferences & procedures

_此区块由 evolving-skills 维护。离线蒸馏产出的规则，
经过 held-out 验证后写入此处。区块外的手写内容永不被修改。_

- Always use async/await for database calls in this project.
- Commit messages must follow conventional-commits format.
<!-- EVOLVING-SKILLS:LEARNED END -->
```

### SKILL.md provenance

```yaml
---
name: react-effect-cleanup
description: Use when cleaning up React useEffect to prevent memory leaks...
metadata:
  provenance: evolving-skills
  origin: online-distill     # 或 offline-sleep
  distilled_at: 2026-06-26T14:30:00Z
  parent_skill: react-patterns  # 如果是 patch 的
---
```

### 进化树

```jsonl
{"node_id":"sleep-20260626","parent_id":"sleep-20260625","date":"2026-06-26","source":"offline","changes":[{"target":"CLAUDE.md","op":"add","content":"...","gate":"accept","score_delta":0.15}],"metrics":{"tasks":12,"baseline":0.33,"candidate":0.67}}
{"node_id":"online-20260626-1","parent_id":null,"date":"2026-06-26","source":"online","changes":[{"target":"react-effect-cleanup","op":"create","content":"..."}]}
```
