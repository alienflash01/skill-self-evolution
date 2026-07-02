# self-improving-skills（opencode 版）

> 把 Claude Code 的 [claude-self-improving-skills](https://github.com/UniM0cha/claude-self-improving-skills)（作者 이정윤，移植自 Nous Research 的 [Hermes Agent](https://github.com/NousResearch/hermes-agent)）改造为 **opencode 可用版本**。
>
> 核心思想不变：**复杂任务 → 蒸馏出可复用技法 → 写进 SKILL.md → 下次会话自动复用**。

opencode 已经有 hooks、subagent、命令、skills 等原语。本项目把这些原语接成一个闭环学习循环：

```text
复杂任务 → 蒸馏出有用的东西 → 保存/patch 一个技能 → 下次会话重新发现
```

## 为什么需要它

大多数编码代理能解决一次难题，但很少有能可靠**记住**其中可复用的部分并在之后应用的。Hermes Agent 通过 skills 和 curator 循环拥有一流的「过程记忆」。本项目把这一思路移植到 opencode：

- **检测**复杂工作（通过会话消息里的工具调用信号）。
- **在合适时机提醒**代理把可复用技法蒸馏出来。
- 通过专门的子代理**写入或 patch** `~/.config/opencode/skills/<name>/SKILL.md`。
- **校验并回滚**结构错误的技能编辑。
- **追踪用量**，让过时的生成技能可被归档而非无限堆积。

## 与 Claude 版的关键差异（诚实说明）

opencode 与 Claude Code 的原语不完全对应，本移植做了有意识的取舍：

| Claude 版 | opencode 版 |
|---|---|
| `Stop` 钩子能**阻塞并强制续轮**强制蒸馏 | opencode 无此能力 → 改为 `session.idle` 时弹 **toast + 预填 `/distill-skill`**（非侵入、无循环风险） |
| `SessionStart` 注入 additionalContext | `experimental.chat.system.transform` 注入系统提示 |
| `PreToolUse`/`PostToolUse` 钩子 + Python 脚本 | `tool.execute.before`/`after` + **纯 TypeScript 插件**（零外部依赖，无需 Python） |
| 解析 `~/.claude/projects` 的 JSONL transcript | 调用 `client.session.messages()` SDK 读消息 |
| `~/.claude/skills` | `~/.config/opencode/skills`（opencode 全局技能目录） |
| 团队技能共享 / 上游 PR 贡献 | **本版本不含**（聚焦核心自改进环；可后续补） |

### 已知限制

- **蒸馏提醒是「建议」而非「强制」。** opencode 没有 Claude 的阻塞式 Stop 钩子，因此 idle 后只会弹 toast、把 `/distill-skill` 预填进输入框，是否执行由你决定。这正是选择的稳健方案，但自动性弱于 Claude 版。
- **`use` 计数信号缺失。** Claude 版靠 `Skill` 工具调用计「使用」次数；opencode 的 skills 是常驻系统提示的，没有「技能被调用」的离散事件。本版本只统计 **view**（读 SKILL.md）和 **patch**（编辑 SKILL.md）。一个静默生效的技能可能拿不到新鲜度更新而走向 stale —— 对有价值的技能请用 `/pin-skill` 保护。
- **toast 仅在 TUI 在线时有效。** headless（SDK/server）模式下无 TUI，提醒会静默跳过（fail-safe）。
- 这只处理**过程记忆**（SKILL.md），不处理事实记忆。

## 安装

### 方式一：安装脚本（推荐）

```bash
cd opencode-self-improving-skills
chmod +x install.sh
./install.sh             # 安装到全局 ~/.config/opencode/（所有项目可用）
# 或
./install.sh --project   # 仅安装到当前项目 .opencode/
```

脚本用**符号链接**把插件、子代理、命令链入 opencode 配置目录。卸载用 `./install.sh --uninstall`。

### 方式二：手动

把对应文件复制/链接到 opencode 的配置目录（全局 `~/.config/opencode/` 或项目 `.opencode/`）：

```text
plugin/self-improving-skills.ts  →  ~/.config/opencode/plugins/self-improving-skills.ts
agent/skill-distiller.md         →  ~/.config/opencode/agents/skill-distiller.md
commands/*.md                    →  ~/.config/opencode/commands/*.md
```

> 本插件**零运行时依赖**：仅 `import type { Plugin }`（类型导入，运行时被擦除）和 Node 内置模块（`node:fs/promises`）。因此**无需**为它单独准备 `package.json`，装上即用。

**安装后务必重启 opencode**（配置仅在启动时加载，不热重载）。

## 使用方法

日常使用基本零干预：正常工作即可。当一段复杂工作结束（会话空闲），若插件判定它「复杂且尚未蒸馏」，会弹一个 toast 并把 `/distill-skill` 预填进输入框。按回车运行，或忽略。

### 命令一览

| 命令 | 作用 |
|---|---|
| `/distill-skill` | **手动触发蒸馏**：委派 skill-distiller 子代理，把本轮可复用技法写入 SKILL.md |
| `/curate-skills` | LLM 整理：把窄技能合并成伞型技能、压缩过长 description（先出计划，批准后才执行） |
| `/curator-status` | 查看循环状态：各技能用量/状态、距上次使用天数、上次整理记录 |
| `/prune-skills [天数]` | 批量归档超期未用技能（先 dry-run 预览，确认后才归档） |
| `/archive-skill <名字>` | 归档单个技能（移到 `.archive/`，可恢复） |
| `/pin-skill <名字>` | pin 住技能，使其不参与自动 stale/archive |
| `/restore-skill <名字>` | 把归档的技能恢复为活跃 |

### 典型流程

1. **正常工作** → 完成一段复杂调试/迁移后，看到 toast 提醒。
2. `/distill-skill` → 子代理判断是否可复用；能 patch 现有技能就 patch，否则新建 class 级技能，一次性内容则放弃（正常）。
3. 技能被写入 `~/.config/opencode/skills/<name>/SKILL.md`，经校验+provenance 盖章。
4. **下次会话** opencode 自动发现该技能并纳入系统提示。
5. 定期 `/curate-skills` 合并冗余、`/curator-status` 查看健康度。

## 配置（环境变量，均可选）

在 shell 或 opencode 配置中设置：

| 变量 | 默认 | 含义 |
|---|---:|---|
| `SIS_DISTILL_THRESHOLD` | `12` | 自上次蒸馏以来累计工具调用数达此值才可能触发提醒 |
| `SIS_MIN_FILE_EDITS` | `2` | 自上次蒸馏以来的最少文件编辑次数；防止纯探查/问答触发 |
| `SIS_CURATE_MIN_SKILLS` | `8` | agent 蒸馏技能数达此值才开始自动 curator |
| `SIS_CURATE_INTERVAL_DAYS` | `7` | 自动 curator 间隔（天） |
| `SIS_STALE_AFTER_DAYS` | `30` | 未活动达此天数标记 stale |
| `SIS_ARCHIVE_AFTER_DAYS` | `90` | 未活动达此天数移到 `.archive/`（`use_count ≥ 3` 翻倍） |

## 工作原理

```text
复杂任务结束 → 会话空闲(session.idle)
   ↓
插件读 client.session.messages()，测量自上次蒸馏以来的工具调用/编辑数
   ↓
若复杂且未蒸馏 → 弹 toast + 预填 /distill-skill（一次/段，已提醒过的不再重复）
   ↓
/distill-skill 委派 skill-distiller 子代理（隔离上下文）
   ↓
patch 现有技能 / 新建 class 级技能 / 一次性则放弃
   ↓
tool.execute.after 校验 frontmatter + 盖 provenance；结构破损则自动回滚
   ↓
下次会话：opencode 自动发现该技能 → 复用
```

学习技能存在用户目录（`~/.config/opencode/skills`），与本项目代码分离 —— 升级本插件不会丢失已积累的过程知识。

## 目录结构

```text
opencode-self-improving-skills/
├── plugin/
│   └── self-improving-skills.ts   # 全部逻辑：hooks + 遥测 + curator + 复杂度分析（纯 TS）
├── agent/
│   └── skill-distiller.md         # 蒸馏子代理（patch > 新建 优先级）
├── commands/                      # 7 个斜杠命令
│   ├── distill-skill.md
│   ├── curate-skills.md
│   ├── curator-status.md
│   ├── prune-skills.md
│   ├── archive-skill.md
│   ├── pin-skill.md
│   └── restore-skill.md
├── install.sh                     # 符号链接安装到 opencode 配置目录
└── README.zh.md                   # 本文档
```

运行期数据（自动生成）：

```text
~/.config/opencode/
├── skills/<name>/SKILL.md         # 学习技能库
│   └── .archive/                  # 归档的技能（可恢复）
└── self-improve/
    ├── skill_usage.json           # 用量遥测
    ├── curator_state.json         # curator 运行状态
    ├── skill_backups/             # 编辑前 SKILL.md 快照（回滚用）
    └── curator_backups/           # 归档前 tar.gz 快照
```

## 设计原则（沿用原项目）

原项目建立在对同类 dev-log 钩子「396 个真实会话一次都没触发」的失败分析之上，本移植沿用这些护栏：

1. **用真实消息结构解析。** 工具调用是 `part.type === "tool"`、`part.tool` 为工具名、`part.state.input` 为参数 —— 不靠字符串猜测。
2. **「是否已蒸馏」按真实行为判定。** 以「向 skill-distiller 的 Task 委派」或「对 SKILL.md 的 write/edit」为锚点，而非字符串匹配插件名（会自触）。
3. **阈值用真实工作量信号**（累计工具调用 + 文件编辑数），而非关键词计数。
4. **每段工作最多提醒一次。** 已提醒过的段不重复提醒，只有再积累一阈值的新工作才会再提醒。
5. **fail-safe。** 任何插件错误都静默放过，绝不阻塞/打断会话。
6. **保守的 curator。** 只归档 agent 蒸馏的技能；用户手写 / pinned / 团队技能永不碰；归档可恢复。

## 许可证

MIT（沿用原项目）。
