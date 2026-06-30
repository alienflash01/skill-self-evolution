
<!-- BEGIN AGENT-EXPERIENCE -->
## ⚠️ Known Pitfalls (Auto-distilled)

<!-- These rules were automatically extracted from trial-and-error patterns. -->
<!-- To update, run: /distill offline -->

### Bash

- Verify directory structure before accessing deeply nested files by using error-suppressed commands like `du 2>/dev/null` or `find` to discover what actually exists.
- When checking for file/directory availability, use direct checks with conditional fallback instead of `sleep` delays that risk timeout.
- After a build fails, search the source code for specific dependency patterns to diagnose the root cause before re-attempting compilation.
- Reduce build parallelism (try `-j 1`) when parallel compilation fails due to resource limits or race conditions.

<!-- END AGENT-EXPERIENCE -->
