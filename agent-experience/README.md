# Agent Experience Distiller

> 让 Claude Code 从自己的试错中学习——自动检测"失败→重试→成功"模式，提取可复用经验规则，沉淀到 CLAUDE.md。

## 它做什么

每次 Claude Code 执行任务时，如果某个命令失败了、换了个参数重试成功了，这里面就藏着有价值的经验。这个插件自动：

1. **采集**工具调用的完整 trace（命令、输出、错误）
2. **检测**三种试错模式：单步修正、多次换思路、用户纠正
3. **提取**通用可复用的经验规则
4. **沉淀**到结构化规则库和 CLAUDE.md

## 快速开始

### 安装

```bash
# 方式一：本地安装（开发推荐）
cd /path/to/agent-experience
ln -s "$(pwd)" ~/.claude/plugins/agent-experience

# 方式二：Claude Code 插件市场（如果已发布）
# /plugin marketplace add <repo-url>
# /plugin install agent-experience
```

安装后，Claude Code 会自动加载 hooks 和 `/distill` 命令。

### 验证

```bash
# 在 Claude Code 中：
/distill status    # 查看当前状态

# 或直接在终端：
python3 ~/.claude/plugins/agent-experience/scripts/distill.py status
```

## 两种工作模式

### 在线模式（自动，实时）

安装后**无需任何操作**。PostToolUse hook 在每次工具调用后自动运行：

- 记录工具调用到 `data/traces/`
- 检测到 fail→success 序列时，自动提取规则
- 使用启发式提取（无 API 花费）

### 离线模式（手动或定时）

深度扫描历史会话转录，提取更多模式：

```bash
# 扫描最近 72 小时的会话
python3 scripts/distill.py offline --project "$(pwd)"

# 用 LLM 提取更精确的规则（消耗 API）
python3 scripts/distill.py offline --project "$(pwd)" --llm

# 预览模式（不保存）
python3 scripts/distill.py offline --dry-run

# 查看所有规则
python3 scripts/distill.py report

# 写入 CLAUDE.md（自动备份）
python3 scripts/distill.py apply --project "$(pwd)"
```

在 Claude Code 中：
```
/distill offline
/distill report
/distill apply
```

### 夜间定时

```bash
# 每天凌晨 3:17 自动蒸馏
(crontab -l 2>/dev/null; echo "17 3 * * * python3 /path/to/scripts/distill.py offline --project /your/project --llm >> /tmp/distill.log 2>&1") | crontab -
```

## 检测的三种模式

| 模式 | 示例 | 提取的规则 |
|------|------|-----------|
| **单步修正** | `pip install X` 失败 → `pip install X --force-reinstall` 成功 | "pip 卸载失败时加 --force-reinstall" |
| **多次换思路** | 方案A 失败 → 方案B 失败 → 方案C 成功 | "用方案C 更可靠" |
| **用户纠正** | Agent 用了 requests → 用户说"用 httpx" | "本项目用 httpx" |

## 数据流

```
Claude Code 会话
    │
    ├── PostToolUse Hook ──→ Trace Store ──→ 在线检测 ──→ 规则库
    │                                          │
    └── 会话结束 ──→ 转录持久化 ──→ 离线批量扫描 ──→ 规则库
                                                     │
                                        ┌────────────┤
                                        ▼            ▼
                                   rules.json    CLAUDE.md
                                  (结构化)     (自动备份)
```

## 安全保证

- **只读转录**：绝不修改 ~/.claude 下的原始转录文件
- **分阶段写入**：规则先进 rules.json，CLAUDE.md 只在 `apply` 时更新
- **自动备份**：每次 apply 先备份 CLAUDE.md 到 `.md.bak`
- **去重**：基于 75% 相似度阈值自动去重
- **过滤噪音**：权限拒绝错误自动跳过
- **零阻塞**：hook 异步处理，不影响正常使用

## 文件结构

```
agent-experience/
├── .claude-plugin/
│   └── plugin.json              # 插件元数据
├── hooks/
│   ├── hooks.json               # Hook 注册配置
│   ├── post-tool-use.py         # PostToolUse hook（在线采集+检测）
│   └── on-session-end.sh        # SessionEnd hook（标记活动）
├── commands/
│   └── distill.md               # /distill 斜杠命令
├── skills/
│   └── experience-distill/
│       └── SKILL.md             # 技能文档（触发条件）
├── scripts/
│   └── distill.py               # 核心引擎（解析+检测+提取+存储）
├── data/                        # 运行时数据（gitignore）
│   ├── traces/                  # 工具调用 trace
│   ├── rules.json               # 结构化规则库
│   └── staging/                 # 报告
└── README.md
```

## 配置

### 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `DISTILL_LLM` | off | 设为 `1` 时在线 hook 也使用 LLM 提取 |

### CLAUDE.md 中的标记

规则写入 CLAUDE.md 时使用注释块标记：
```html
<!-- BEGIN AGENT-EXPERIENCE -->
...自动蒸馏的规则...
<!-- END AGENT-EXPERIENCE -->
```

多次 `apply` 只替换这个块，不影响手写内容。

## 技术细节

### 试错检测算法

回溯窗口：最多向前看 8 步。只有同一工具类型、命令相似度 >15%、非权限错误的失败才算有效前序。

### Delta 计算

对 Bash 命令使用 `shlex.split` 拆分为参数级 diff，对其他工具使用 JSON 序列化后的 token diff。

### 去重

基于规则文本的 Jaccard 相似度（阈值 75%），使用 `difflib.SequenceMatcher`。

## 与 SkillOpt-Sleep 的关系

| | 本方案 | SkillOpt-Sleep |
|---|---|---|
| 粒度 | 工具调用级 | 任务级 |
| 触发 | 实时 + 离线 | 仅离线 |
| 验证 | 去重 | held-out gate |
| 格式 | 结构化 + 文本 | 纯文本 |

两者互补：本方案做微观操作级，SkillOpt-Sleep 做宏观任务级。

## License

MIT
