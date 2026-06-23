---
description: 把已归档的学习技能恢复到 ~/.config/opencode/skills
agent: build
---

把 curator 归档的技能恢复为活跃状态。

先用 glob 列出 `~/.config/opencode/skills/.archive/` 下已归档的技能。

`$ARGUMENTS` 给了要恢复的技能名就用它，否则从上面的列表里问用户恢复哪个。然后：

1. 用 bash `mv ~/.config/opencode/skills/.archive/<name> ~/.config/opencode/skills/<name>`（移回，可恢复）。
2. 用 edit 在 `~/.config/opencode/self-improve/skill_usage.json` 里把该技能的 `state` 设回 `"active"`。

恢复后，若不想它再被自动归档，建议用 `/pin-skill <name>` pin 住。
