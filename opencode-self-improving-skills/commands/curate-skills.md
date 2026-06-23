---
description: 整理学习技能库 —— 伞型整合、压缩过长 description、归档冗余
agent: build
---

审查并整理学习技能库。这是自改进循环的**维护阶段**，是一次**伞型构建式整合**，不是简单的重复检测。

## 哲学（移植自 Hermes curator）

技能库的目标是**一个由 class 级指令和经验知识组成的图书馆**。几百个每个只装某个会话某个 bug 的窄技能的扁平堆，是图书馆的**失败**。代理按 description 而非名字匹配技能，所以 1 个带带标签小节的宽伞型技能比 5 个窄兄弟技能可发现性更好。正确目标形态：**内容丰富的正文 + `references/`/`templates/`/`scripts/` 支撑文件的 class 级技能**。

## 步骤

### 1. 收集学习技能 + 用量统计

读取这些数据：

- 用 glob 列出 `~/.config/opencode/skills/*/SKILL.md`
- 用 grep 找带 `provenance: self-improving-skills` 的（即 agent 蒸馏的）
- 用 read 读取用量遥测 `~/.config/opencode/self-improve/skill_usage.json`（含每个技能的 use/view/patch 计数、最后使用时间、state、created_by）

为每个学习技能的 `name`/`description` 与用量统计（use/view/patch、最后使用、state、created_by）制一张表。

### 2. 硬规则 —— 不可违反

1. **只动 `created_by: agent` 的技能。** 用户手写(user)、其它来源的技能绝不修改/归档/整合。
2. **禁止删除。** 归档（移到 `.archive/`，可 `/restore-skill` 恢复）是最大破坏动作。
3. **`pinned: true` 的技能整体跳过。**
4. **别把 use_count 当作整合或归档的依据。** 计数器是新引入的，多半为 0。`use=0` 是「证据缺失」而非「无价值」。重叠判断看**内容**不看频率。（时间基的未使用清理由 curator 状态机负责，不是本步骤的活。）但整合时「以哪个为准」可参考计数。
5. **别以「每个技能触发不同」为由拒绝整合。** 正确判据：**「人类维护者会把它写成 N 个独立技能，还是 1 个带 N 个带标签小节的技能？」** 若是后者，就整合。

### 3. 整合方法

1. 从全部候选里识别**前缀/领域簇**。
2. 对每个有 ≥2 成员的簇，问「这些技能共同服务的**伞型 class** 是什么？」
3. 每簇选一种整合方式：
   - **a. 并入现有伞型** —— 簇里某个已足够宽，把各兄弟的独特洞见作为带标签小节加进去，归档兄弟。
   - **b. 新建伞型** —— 没有足够宽的成员，就新写一个覆盖共享工作流的 class 级技能，吸收兄弟后归档它们。
   - **c. 降级为 references/templates/scripts** —— 窄但有价值的会话特定内容，移到伞型的对应子目录后归档原技能。
4. 吸收式归档要记录伞型名（用 edit 在 `skill_usage.json` 里给被归档技能设 `absorbed_into: "<伞型>"`、`state: "archived"`，并把目录移到 `~/.config/opencode/skills/.archive/`）。
5. 整合后更新伞型的 `description` 以准确反映合并后的范围。

### 4. 包完整性

降级/归档前把技能当作**完整目录包**检查，而非只看 SKILL.md。若原技能有 `references/`/`templates/`/`scripts/`/`assets/`，不要只撕走 SKILL.md。安全做法只有：保持独立 / 完整重定位所有支撑文件并修好正文路径的**完整合并** / 整包归档。绝不留下指向已移动文件的坏链。

### 5. description 压缩

学习技能的 description 会进入**每个会话**的系统提示。超 500 字符的，在保留触发短语的前提下作为压缩候选（具体触发短语和情境匹配要留下 —— 那是触发精度的核心）。

### 6. 两阶段执行：计划 → 批准 → 实施

**先只出变更计划**：每簇的整合方式、将被吸收的技能、归档对象、要压缩的 description。**用户批准后**才实际编辑/归档。

完成后把整合的簇、归档的技能、保持不动的技能数做个摘要。若无变更，回复「没有需要整理的东西」结束。同时用 edit 把 `~/.config/opencode/self-improve/curator_state.json` 的 `last_run` 更新为当前时间戳。

$ARGUMENTS 若有则聚焦该范围（例如只整理某个领域）。
