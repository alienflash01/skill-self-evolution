---
description: Pin a skill so the curator never archives it
argument-hint: "<skill-name>"
allowed-tools: Bash
---

# /pin-skill

Pin skill: $ARGUMENTS

```bash
python3 -c "
import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
import usage_store
usage_store.set_fields('$ARGUMENTS', pinned=True)
print('Pinned: $ARGUMENTS')
"
```

Also add `pinned: true` to the skill's SKILL.md frontmatter if not present.
