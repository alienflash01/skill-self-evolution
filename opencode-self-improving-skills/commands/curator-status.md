---
description: 查看自改进循环状态 —— 各学习技能的用量、状态、上次整理
agent: build
---

把自改进循环的当前状态以易读形式展示。读取以下数据：

- 用 read 读 `~/.config/opencode/self-improve/curator_state.json`（若不存在则提示「尚未运行过整理」）
- 用 read 读 `~/.config/opencode/self-improve/skill_usage.json`（用量遥测；若不存在则提示「无遥测」）
- 用 glob 列出 `~/.config/opencode/skills/.archive/`（已归档技能）

然后把这些 JSON 解析成**表格**展示：

- 每个学习技能：名字 · state(active/stale/archived) · use/view/patch 次数 · 距上次使用天数 · 是否 pinned · created_by(agent/user)
- 上次整理时间、run_count、上次摘要(stale/archived/reactivated 数量)
- 点出最久未用的几个技能，作为即将 stale/archive 的候选

`$ARGUMENTS` 若是某个技能名，只展示该技能详情。

> 阈值：距上次活动 SIS_STALE_AFTER_DAYS(默认 30 天) → stale，SIS_ARCHIVE_AFTER_DAYS(默认 90 天) → archive。**累计 use_count ≥ 3 的技能 archive 阈值翻倍**（被验证过的技能老化更慢）。pinned 技能与 created_by=user 的技能不参与自动清理。
