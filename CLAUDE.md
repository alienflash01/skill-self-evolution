

<!-- BEGIN AGENT-EXPERIENCE -->
## ⚠️ Known Pitfalls (Auto-distilled)

<!-- These rules were extracted from trial-and-error patterns. -->
<!-- Status: ✓=trusted(3+obs) ★=verified(2nd obs) ·=pending(1st obs) -->
<!-- To update, run: /distill offline -->

### Bash

- ★ Verify directory structure before accessing deeply nested files by using error-suppressed commands like `du 2>/dev/null` or `find` to discover what actually exists.
- ★ When checking for file/directory availability, use direct checks with conditional fallback instead of `sleep` delays that risk timeout.
- ★ Reduce build parallelism (try `-j 1`) when parallel compilation fails due to resource limits or race conditions.
- ★ When `ls` fails with 'Exit code 2
ls: cannot access '/home/fanwei/workspace/link_e_workspace/有限元/ogs-w', add: -5 -sh /home/fanwei/workspace/link_e_workspace/有限元/ogs-workspace/ogs-build 2>/dev/null du head | ~/ogs-build
- ★ When `sleep` fails with 'Exit code 143
Command timed out after 1m 0s', add: /home/fanwei/workspace/link_e_workspace/有限元/ogs-workspace/ogs-build/release/bin/ogs Still copying... echo ||
- ★ When `cd` fails with 'Exit code 1
[0/2] Re-checking globbed directories...
[1/260] Building CXX object', add: -100 1 tail |
- · After a build fails, search the source code for specific dependency patterns to diagnose the root cause before re-attempting compilation.
- · When `cmake` fails with 'Exit code 1
-- The C compiler identification is GNU 13.3.0
-- The CXX compiler i', add: -r /mnt/e/02.workspace/有限元/ogs/Applications/DataExplorer/ 2>/dev/null QXmlPatterns\|QtXmlPatterns grep

<!-- END AGENT-EXPERIENCE -->
