# Smoke 2, stopped by a harness defect

Calendar/New turn 1 completed (materials and SKILL.md read, 225.7 s). Sheet/Old turn 1 then rendered its PDF with headless Edge, which left a browser profile under STA/outputs/; the per-turn snapshot copy failed on a locked cache file and the runner stopped. Fixed in the next commit (browser profiles/caches excluded from snapshots; copy errors recorded instead of aborting). Diagnostic only, unscored.

Observation kept for the report: in calendar/New turn 1 the tutor asked the combined availability question through the CLI question tool; in non-interactive exec it received no answer and built an all-day fallback calendar in the same turn instead of waiting.

The partial copy of the Edge browser profile was deleted from this record (browser cache, not study output; paths exceeded Windows limits).
