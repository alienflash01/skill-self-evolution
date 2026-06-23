---
description: 把学习技能 pin 起来，使其不参与 curator 的自动 stale/archive
agent: build
---

把 `$ARGUMENTS` 指定的学习技能 pin 住。被 pin 的技能无论多久没用，curator 都不会标记 stale 或归档（用于保护有价值的伞型技能）。

技能名在 `$ARGUMENTS` 中给出；若未给，用 glob 列出 `~/.config/opencode/skills/*/SKILL.md` 让用户选。

**实施：** 用 edit 把 `~/.config/opencode/self-improve/skill_usage.json` 里该技能的 `pinned` 设为 `true`。若该技能还没有遥测记录，则新增一条并把 `pinned` 设为 `true`。

取消 pin 就把 `pinned` 设回 `false`。完成后用一行告知结果。
