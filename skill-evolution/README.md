# Skill-Evolution

> 统一的 Claude Code 技能自进化插件——三层学习闭环。

融合 agent-experience（工具级蒸馏）+ evolving-skills（任务级蒸馏 + 离线 sleep 循环）。

## 三层架构

| 层 | 触发 | 粒度 | 命令 |
|----|------|------|------|
| **L1 工具级** | PostToolUse（实时） | 单条命令试错 | `/distill offline` |
| **L2 任务级** | Stop hook（会话结束） | 整个工作段技能 | `/distill-skill` |
| **L3 离线** | cron / 手动 | 历史会话验证 | `/sleep run` |

## 安装

```bash
ln -s /path/to/skill-evolution ~/.claude/plugins/skill-evolution
```

## 命令

```
/distill offline     # 扫描转录，提取试错规则
/distill report      # 查看规则（★=已验证 ✓=可信 ·=待验证）
/distill apply       # 写入 CLAUDE.md（带备份）
/distill status      # 当前状态

/distill-skill       # 手动触发任务级蒸馏

/sleep dry-run       # 预览离线循环
/sleep run           # 完整离线循环
/sleep adopt         # 采纳提议
/sleep status        # 历史记录
```

## 规则生命周期

```
pending (·)  ──2nd observation──→  verified (★)  ──3+ observations──→  trusted (✓)
```

## 安全保证

- 转录只读
- CLAUDE.md 受保护块（手写内容永不修改）
- 每次 apply 自动备份
- 规则验证门控（pending → verified → trusted）

## License

MIT
