---
description: Run the curator to consolidate, merge, or archive stale learned skills
allowed-tools: Bash, Read, Edit
---

# /curate-skills

You are running skill curation. Steps:

1. **Preview** what the curator would do:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curator_transitions.py" --dry-run
   ```

2. **Review the output.** Show the user what will be archived/marked stale.

3. **Propose consolidation** — if there are narrow skills that could be merged
   into broader umbrella skills, propose a plan. Wait for approval.

4. **After approval**, execute:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/curator_transitions.py"
   ```

5. **Report** what was done. Never touch user-authored or pinned skills.
