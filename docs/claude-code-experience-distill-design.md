# Claude Code Agent 执行经验蒸馏方案设计

> 目标：在 Claude Code 上实现工具调用级别的"试错自纠正"经验蒸馏，支持在线和离线两种模式

---

## 一、Claude Code 原生支持什么

### ✅ 已有的基础设施

| 能力 | 具体支持 | 蒸馏用途 |
|------|---------|---------|
| **Hooks 系统** | `PreToolUse` / `PostToolUse` / `SessionEnd` 等 18 种事件 | **采集时机**：每次工具调用都能捕获 |
| **结构化转录** | `~/.claude/projects/*/<sessionId>.jsonl` | **数据源**：完整的工具调用 input/output/error |
| **CLAUDE.md** | 项目级记忆文件，每会话自动加载 | **沉淀位置**：项目约定 |
| **SKILL.md** | 技能文档，可通过插件加载 | **沉淀位置**：操作技能 |
| **Plugin 系统** | 命令 + hooks + skills 三件套 | **分发载体**：打包为 Claude Code 插件 |
| **Headless 模式** | `claude -p "..."` 非交互执行 | **离线重放**：夜间批量处理 |

### ❌ 不支持的

| 缺失 | 影响 |
|------|------|
| **无自动记忆** | CLAUDE.md 不会自动更新，必须手动写入 |
| **无试错检测** | 不会自动识别"失败→重试→成功"模式 |
| **无经验提取** | 不会从工具调用历史中蒸馏规则 |
| **无验证门控** | 没有自动验证新规则是否有效 |

**结论：Claude Code 原生有数据采集能力（hooks + 转录），但完全没有经验蒸馏能力。需要自己实现。**

---

## 二、转录数据结构（已验证）

每次 Claude Code 会话都在 `~/.claude/projects/<slug>/<sessionId>.jsonl` 留下完整记录：

```jsonl
// 用户消息
{"type":"user", "message":{"role":"user","content":"修复测试"},
 "cwd":"/home/fanwei/project", "timestamp":"..."}

// 助手消息（含工具调用）
{"type":"assistant", "message":{"role":"assistant","content":[
  {"type":"tool_use", "id":"call_abc123",
   "name":"Bash", "input":{"command":"npm test"}}
]}}

// 工具结果（含错误标记）
{"type":"user", "message":{"role":"user","content":[
  {"type":"tool_result", "tool_use_id":"call_abc123",
   "is_error":true,
   "content":[{"type":"text","text":"ERESOLVE unable to resolve..."}]}
]}}

// 助手重试
{"type":"assistant", "message":{"role":"assistant","content":[
  {"type":"tool_use", "id":"call_def456",
   "name":"Bash", "input":{"command":"npm install --legacy-peer-deps"}}
]}}

// 工具结果（成功）
{"type":"user", "message":{"role":"user","content":[
  {"type":"tool_result", "tool_use_id":"call_def456",
   "is_error":false,
   "content":[{"type":"text","text":"added 42 packages"}]}
]}}
```

**关键字段**：
- `tool_use_id`：串联请求和响应
- `is_error`：标记失败的工具调用
- `input.command`：完整的命令/参数
- `content[].text`：stderr/stdout 全文

---

## 三、架构设计

### 整体架构

```
┌──────────────────────────────────────────────────────────────┐
│                    Claude Code 插件                           │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │ PostToolUse  │   │ SessionEnd   │   │  /distill    │    │
│  │   Hook       │   │   Hook       │   │  Command     │    │
│  │  (在线采集)   │   │ (离线触发)    │   │ (手动触发)    │    │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘    │
│         │                  │                   │             │
│         ▼                  ▼                   ▼             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Trace Store (JSONL)                     │    │
│  │  ~/.claude-experience/traces/<project>/<date>.jsonl │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│         ┌──────────────┼──────────────┐                     │
│         ▼              ▼              ▼                     │
│  ┌────────────┐ ┌────────────┐ ┌──────────────┐            │
│  │ 在线蒸馏    │ │ 离线蒸馏    │ │  手动蒸馏     │            │
│  │ (实时)      │ │ (夜间)      │ │  (按需)       │            │
│  └──────┬─────┘ └──────┬─────┘ └──────┬───────┘            │
│         │              │              │                     │
│         ▼              ▼              ▼                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           经验提取引擎 (Reflect)                      │    │
│  │  1. 试错模式检测 (fail → retry → success)           │    │
│  │  2. 差异分析 (delta = diff(cmd_fail, cmd_success))  │    │
│  │  3. 规则生成 (LLM 提取通用规则)                      │    │
│  │  4. 去重检查 (与已有规则对比)                         │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           沉淀层                                      │    │
│  │  ├── CLAUDE.md  → 项目约定                           │    │
│  │  ├── SKILL.md   → 操作技能（含 pitfalls 段）          │    │
│  │  └── rules.json → 结构化规则（trigger→action）        │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## 四、两种模式详细设计

### 模式一：在线蒸馏（实时）

**触发时机**：每次工具调用结束后（PostToolUse hook）

**流程**：

```
PostToolUse Hook 触发
    │
    ├── 记录到 Trace Store
    │   {tool, input, output, is_error, timestamp, session_id}
    │
    ├── 检测：是否是"失败后的重试"？
    │   │
    │   │  判断逻辑：
    │   │  1. 当前 is_error = false（成功了）
    │   │  2. 同一 session 中，前一条同类型工具调用 is_error = true
    │   │  3. 两条调用的 input 有相似性（命令前缀相同）
    │   │
    │   ├── 否 → 结束（大多数调用不触发蒸馏）
    │   │
    │   └── 是 → 进入提取
    │
    ├── 提取规则（轻量，就地用 LLM）
    │   │
    │   │  Prompt:
    │   │  "你刚才在执行任务时经历了以下试错:
    │   │   尝试1: {failed_command}
    │   │   错误: {error_message}
    │   │   尝试2: {succeeded_command}
    │   │   结果: 成功
    │   │   请提取一条不超过两句话的通用经验规则。"
    │   │
    │   └── 输出: 一条经验规则
    │
    ├── 去重检查
    │   │  与 rules.json 和 CLAUDE.md 中已有规则对比
    │   │  如果已存在相似规则 → 跳过
    │
    └── 沉淀
        │  轻量规则 → 追加到 rules.json
        │  重要约定 → 建议写入 CLAUDE.md（不自动写）
        │
        └── 下次会话自动加载
```

**PostToolUse Hook 配置**（`settings.json`）：

```json
{
  "hooks": {
    "postToolUse": [
      {
        "matcher": {
          "toolName": ["Bash", "Write", "Edit"]
        },
        "action": "run",
        "command": "python3 ~/.claude-experience/hooks/post-tool-use.py",
        "env": {
          "TRACE_DIR": "~/.claude-experience/traces"
        }
      }
    ]
  }
}
```

**优势**：
- 即学即用，下次会话就有效
- 只在检测到试错时触发 LLM，不浪费 API
- 对用户透明（不干扰正常使用）

**劣势**：
- 每次 PostToolUse 都有轻量开销（记录 trace）
- LLM 调用增加少量延迟（仅试错时）

---

### 模式二：离线蒸馏（夜间）

**触发时机**：SessionEnd hook 标记 + cron 定时批量处理

**流程**：

```
SessionEnd Hook
    │
    └── 标记 session 有新数据（追加到 session-end.log）

Cron 定时（如凌晨 3:17）
    │
    ├── Harvest：读取今天新增的所有 .jsonl 转录
    │
    ├── Trace 分析（比在线模式更深度）
    │   │
    │   │  扫描完整会话的工具调用序列:
    │   │
    │   │  call_1: npm install (fail)
    │   │  call_2: npm install --legacy-peer-deps (success)
    │   │  → 试错模式 A: 单步修正
    │   │
    │   │  call_3: approach_1 (fail)
    │   │  call_4: approach_2 (fail)
    │   │  call_5: approach_3 (success)
    │   │  → 试错模式 B: 多次换思路
    │   │
    │   │  call_6: wrong_output → user: "不对" → call_7: correct
    │   │  → 试错模式 C: 用户纠正
    │   │
    │   └── 输出: 试错事件列表
    │
    ├── 批量提取（LLM，一次性处理多条）
    │   │
    │   │  "以下是今天会话中的 5 个试错事件。
    │   │   请为每个提取一条通用规则，
    │   │   并标注类型（tool_fix / approach_switch / user_correction）。
    │   │   去重合并相似规则。"
    │   │
    │   └── 输出: 规则列表
    │
    ├── 验证门控（可选，借鉴 SkillOpt）
    │   │
    │   │  对每条规则，在历史失败任务上"重放":
    │   │  如果规则存在，相同命令是否一次成功？
    │   │
    │   └── 只保留有改善的规则
    │
    ├── 写入 staging 目录
    │   ~/.claude-experience/staging/<date>/
    │   ├── proposed_rules.json
    │   ├── proposed_CLAUDE.md.patch
    │   └── report.md
    │
    └── 用户采纳（/distill adopt）
        或 --auto-adopt 自动应用
```

**优势**：
- 更深度的分析（能看到完整会话上下文）
- 批量处理更省 API（一次调用处理多条）
- 可以做验证门控（在线模式做不到）
- 不影响正常使用的延迟

**劣势**：
- 延迟反馈（当晚学到的次日才生效）
- 需要额外的基础设施（cron + staging）

---

## 五、试错模式检测算法

这是核心——从工具调用序列中识别"有价值的错误"。

### 检测逻辑（伪代码）

```python
def detect_trial_error_patterns(tool_calls: List[ToolCall]) -> List[Experience]:
    """
    从一个会话的工具调用序列中检测试错模式。
    tool_calls 已按时间排序。
    """
    experiences = []
    
    for i, call in enumerate(tool_calls):
        if not call.is_error:
            # 模式 A: 失败→修正→成功
            # 回溯找最近的同类型失败调用
            for j in range(i-1, max(i-5, -1), -1):  # 最多回溯5步
                prev = tool_calls[j]
                if prev.is_error and same_tool_type(prev, call):
                    delta = compute_delta(prev, call)
                    if delta.is_meaningful():  # 不是随机变化
                        experiences.append(Experience(
                            pattern="fail_to_success",
                            failed=prev,
                            succeeded=call,
                            delta=delta,
                        ))
                    break
            
            # 模式 B: 多次失败→最终成功
            failures = collect_recent_failures(tool_calls, i, tool_name=call.name)
            if len(failures) >= 2:
                experiences.append(Experience(
                    pattern="multi_attempt",
                    failures=failures,
                    succeeded=call,
                    approaches=[f.input for f in failures] + [call.input],
                ))
    
    # 模式 C: 用户纠正（需要扫描 user messages）
    for i, msg in enumerate(messages):
        if msg.role == "user" and is_correction(msg.text):
            prev_assistant = find_prev_assistant(messages, i)
            experiences.append(Experience(
                pattern="user_correction",
                agent_wrong=prev_assistant,
                user_correction=msg.text,
            ))
    
    return experiences
```

### Delta 计算

```python
def compute_delta(failed: ToolCall, succeeded: ToolCall) -> Delta:
    """
    计算失败命令和成功命令之间的差异。
    """
    if failed.name == "Bash" and succeeded.name == "Bash":
        cmd1 = failed.input["command"]
        cmd2 = succeeded.input["command"]
        
        # 方法1: 字符串 diff
        added = diff_added(cmd1, cmd2)      # "新增了 --legacy-peer-deps"
        removed = diff_removed(cmd1, cmd2)   # "去掉了 -vcodec"
        changed = diff_changed(cmd1, cmd2)   # "libx264 → libx264-hwaccel"
        
        # 方法2: 参数级比较
        args1 = shlex.split(cmd1)
        args2 = shlex.split(cmd2)
        added_args = set(args2) - set(args1)
        removed_args = set(args1) - set(args2)
        
        return Delta(
            added=added_args,
            removed=removed_args,
            error_text=failed.output[:200],
        )
```

---

## 六、沉淀格式设计

### 结构化规则（rules.json）

```json
{
  "rules": [
    {
      "id": "rule_001",
      "pattern": "fail_to_success",
      "tool": "Bash",
      "trigger": {
        "error_pattern": "ERESOLVE unable to resolve dependency tree",
        "command_prefix": "npm install"
      },
      "action": "append --legacy-peer-deps",
      "full_rule": "当 npm install 报 ERESOLVE 时，加 --legacy-peer-deps 参数",
      "confidence": 0.95,
      "source": {
        "session_id": "abc123",
        "timestamp": "2026-06-26T10:30:00Z",
        "failed_command": "npm install package-a",
        "succeeded_command": "npm install package-a --legacy-peer-deps"
      },
      "times_observed": 3,
      "times_applied": 12,
      "last_updated": "2026-06-26T10:30:00Z"
    }
  ]
}
```

### CLAUDE.md 中的 Pitfalls 段

```markdown
## ⚠️ 已知陷阱（自动蒸馏）

### npm 依赖冲突
- **症状**: `npm install` 报 `ERESOLVE unable to resolve dependency tree`
- **解决**: 加 `--legacy-peer-deps` 参数
- **来源**: 2026-06-26 会话中 3 次遇到

### ffmpeg 编码器参数
- **症状**: `Unknown encoder 'libx264'`
- **解决**: 用 `-c:v libx264` 代替 `-vcodec libx264`
- **来源**: 2026-06-25 会话
```

---

## 七、插件目录结构

```
~/.claude/plugins/agent-experience/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── post-tool-use.py       # 在线采集 + 实时蒸馏
│   └── on-session-end.sh      # 离线标记
├── commands/
│   └── distill.md             # /distill 命令
├── skills/
│   └── experience-distill/
│       └── SKILL.md           # 技能文档
├── scripts/
│   ├── offline-distill.py     # 离线批量蒸馏
│   ├── detect-patterns.py     # 试错模式检测
│   ├── extract-rule.py        # 规则提取
│   └── install-cron.sh        # 安装定时任务
├── data/                       # 运行时数据（gitignore）
│   ├── traces/                 # 工具调用 trace
│   ├── rules.json              # 结构化规则库
│   └── staging/                # 提议暂存
└── README.md
```

---

## 八、与 SkillOpt-Sleep 的对比

| 维度 | SkillOpt-Sleep | 本方案 |
|------|---------------|--------|
| **蒸馏粒度** | 任务级（整个意图的成败） | 工具调用级（单条命令的试错） |
| **触发时机** | 离线（夜间 cron） | 在线（PostToolUse）+ 离线 |
| **数据源** | 会话转录（user/assistant 对话） | 工具调用 trace（含 stderr） |
| **提取方式** | 任务 replay → judge → reflect | trace 分析 → delta 计算 → LLM 提取 |
| **验证方式** | held-out gate（严格） | 历史重放验证（可选）+ 去重 |
| **沉淀格式** | 自由文本 CLAUDE.md | 结构化 rules.json + 文本 |
| **侧重点** | "Agent 整体能力提升" | "不再犯同样的操作错误" |
| **互补性** | 适合宏观策略 | 适合微观操作 |

**两者可以共存**：SkillOpt-Sleep 做宏观的任务级技能优化，本方案做微观的工具级经验沉淀。

---

## 九、实施路线

### Phase 1: MVP（最小可用）
1. PostToolUse hook 采集 trace
2. 基于规则的试错检测（字符串 diff）
3. 离线批量提取（单脚本，不用 LLM）
4. 写入 CLAUDE.md 的 pitfalls 段

### Phase 2: LLM 增强
5. LLM 规则提取（用 `claude -p` headless 调用）
6. 规则去重和合并
7. 结构化 rules.json

### Phase 3: 验证 + 自动化
8. 验证门控（历史重放）
9. 离线 cron 定时处理
10. /distill 命令（status / adopt / report）

### Phase 4: 高级特性
11. Dream replay（对比反思）
12. 跨项目规则迁移
13. 规则衰减和清理
