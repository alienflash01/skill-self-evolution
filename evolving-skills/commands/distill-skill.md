---
description: Manually trigger skill distillation from the current session
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /distill-skill — Manual online distillation

You are the **skill-distiller**. Review the current session's work and decide
whether it produced a reusable, class-level technique worth capturing.

## Steps

1. **Understand what happened.** Read the transcript or ask the user what was accomplished.

2. **Check existing skills.** Glob `~/.claude/skills/**/SKILL.md`. Read any that
   might be relevant to what was learned.

3. **Decide using this priority:**
   - **Patch** an existing skill if one fits (Edit its SKILL.md)
   - **Extend** a broader umbrella skill with a new subsection
   - **Add** a supporting file under an existing skill
   - **Create** a new class-level skill (LAST resort — check for name collisions)

4. **Do NOT capture** one-off tasks, env-specific workarounds, or things already
   covered by existing skills/docs.

5. **SKILL.md format:**
   ```markdown
   ---
   name: <lowercase-hyphenated, class-level, <=64 chars>
   description: <third-person, include trigger phrases, <=500 chars>
   metadata:
     provenance: evolving-skills
     origin: online-distill
   ---
   # <Title>
   ## When this applies
   ## The technique
   ## Gotchas
   ```

6. **Report** one line: what you did (patched/created/declined), skill name, technique.
