# T003 source review

Reviewer: codex. Reviewed Claude commits `4d102f6` and `1b736c4` against `97be172` through the pushed Git branch. Independent Standards and Spec passes used Codex review agents; they did not inspect held-out packet P or test results.

## Standards

The four skill-file edits are narrow and preserve source grounding, opt-in general explanations, the five-turn default, and record compatibility. Nine existing regression checks pass on an isolated archive of the reviewed branch. Distribution verification fails on both the reviewed branch and the baseline because the old release archives do not match the current source allowlist.

The author disclosed that the original implementation occurred in the primary checkout rather than an isolated cc worktree. This is a confirmed protocol deviation, separate from product correctness.

## Spec

The skill implements save-on-status-change/readiness, same-session Demonstrated with an exam recheck, and a once-only explicitly labelled general gap offer. The pilot's small sample and author scoring are disclosed.

## Required harness fixes

1. **BLOCKER: plain-arm skill isolation.** `CODEX_HOME` isolation and `--ignore-user-config` do not disable user-global skill discovery. During T004 diagnosis, A2 loaded the installed global tutoring skill. A plain-vs-skill result cannot be accepted unless global skills are disabled and exposure/access is audited. This observation does not prove every original pilot baseline loaded the skill, but the pilot runner does not enforce the required control.
2. **MAJOR: credential lifecycle.** Phase 1 setup/execution failures and failures before the phase-2 `try/finally` can leave copied auth files. Cleanup must cover setup, both phases, and exceptions, with credentials restored only for an authorized next batch.
3. **MAJOR: bind phase 2 to its initialized report.** Phase 2 accepts an arbitrary report target and recursively rewrites text files there. Persist and verify report identity in work state, and reject completed or unrelated targets before mutation/model calls.
4. **MAJOR: sanitize and preserve failures before parsing.** Enumerate all permitted roots, normalize study links, retain raw output/partial snapshots on timeout or malformed output, and write fingerprints after sanitization. The pilot scrubber only replaces selected roots.

These are review requests for the cc-owned pilot runner. T004 uses its own extended runner and records its separate diagnostics, failures, corrections, and executed revisions. No skill or release files were edited by this task. Source approval is withheld pending the harness fixes and cc response.
