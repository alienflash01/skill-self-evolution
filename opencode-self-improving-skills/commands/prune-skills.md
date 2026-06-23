---
description: 批量归档超过 N 天未用的学习技能（先 dry-run 预览）
agent: build
---

批量清理长期未用的学习技能。这是人工触发的时间基 curator。

`$ARGUMENTS` 若给了天数就用它，否则用 `SIS_ARCHIVE_AFTER_DAYS`(默认 90) 作为阈值。

### 1. 预览（先执行，什么都不改）

用 read 读 `~/.config/opencode/self-improve/skill_usage.json`，对每个技能计算「距上次活动(use/view/patch 任一最新；无则从 created_at)的天数」，筛选出：**未 pinned + `created_by:agent` + 仍 active/stale + idle ≥ 阈值天数** 的技能（pinned、user 创作的排除）。

把候选（名字 + 未用天数 + use_count）做成表格给用户。use_count 高的要提醒：可能是「罕见但决定性」使用的技能。

### 2. 实施（用户确认后）

用户确认后，对每个候选：

1. 用 bash `mv ~/.config/opencode/skills/<name> ~/.config/opencode/skills/.archive/<name>`（移到 .archive，**不删除**，可 `/restore-skill` 恢复；若目标已存在则追加时间戳后缀）。
2. 用 edit 在 `skill_usage.json` 里把该技能的 `state` 设为 `"archived"`。

实施前用 bash 对整个 skills 目录打 tar.gz 快照到 `~/.config/opencode/self-improve/curator_backups/`（保留最近 5 个）。

> 只归档单个技能用 `/archive-skill <name>`；要保护某个技能用 `/pin-skill <name>`。
