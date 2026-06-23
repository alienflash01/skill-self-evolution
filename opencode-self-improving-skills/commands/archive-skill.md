---
description: 手动归档单个学习技能（可选记录并入的伞型技能）
agent: build
---

把指定的学习技能归档（移到 `~/.config/opencode/skills/.archive/`，**不删除**）。

`$ARGUMENTS` 第一个词是技能名。若未给，用 glob 列出 `~/.config/opencode/skills/*/SKILL.md` 让用户选要归档哪个。

**预览：** 先用 read 看该技能的 SKILL.md 概要，确认目标正确。

**实施：**

1. 用 bash `mv ~/.config/opencode/skills/<name> ~/.config/opencode/skills/.archive/<name>`（若目标已存在则追加时间戳后缀）。
2. 用 edit 在 `~/.config/opencode/self-improve/skill_usage.json` 里给该技能设 `state: "archived"`。

实施前用 bash 对 skills 目录打 tar.gz 快照到 `~/.config/opencode/self-improve/curator_backups/`。

若这个技能是**合并进**另一个伞型技能后归档的，把那个伞型名记下（用 edit 设 `absorbed_into: "<伞型名>"`，这样报告里留下的是「整合」而非「丢弃」）。

可用 `/restore-skill "<name>"` 恢复。
