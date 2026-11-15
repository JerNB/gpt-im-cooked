# T007 C-versus-D comparison — BLOCKED on quota

Agent: codex. The comparison is incomplete; no improvement or acceptance verdict is available.

## Frozen inputs and method

C is `4d102f6` (16 skill files); D is the source-reviewed `9938d36` (18 files). Both fingerprint sets match. Packets S/P, scripts and rubric-v2 come from T004 `79f3676`'s exact executed-input archive. The newer T003 skill tip and older D revision are excluded. The adapter uses the identical B/C opener, `gpt-6.1-sol`, medium effort and CLI `0.162.1`. Global and bundled skills are disabled, command accesses audited, and inherited CODEX environment variables removed. Both arms use non-login shells.

The isolated worktree and an empty Git commit verified Git writes. A separate harmless connection probe completed once and returned `T007_OK`. It is excluded from student-session costs.

## Step 1 diagnostic

One D/S session completed exactly turns 1–2. All eight gate checks passed: actual materials and skill read, no global-skill access, no record files after turn 1, both record files after turn 2, one successful `record_io.py save` invocation, no separate read/update/commit invocation, and no inline save wrapper. The save uses a PowerShell here-string JSON pipeline. The two earlier turn-2 commands read instructions/materials; they are not separate record-update calls.

Turn 1 opened first-use guidance but neither record template nor core state.md. Turn 2 opened state.md and state-reference.md. The diagnostic has two student calls, one save and no fallback; copied auth files remaining: zero. It is not a selected comparison session. See [gate](smoke-001/smoke-gate.json), [summary](smoke-summary.json) and [events](smoke-001/runs/D-S-rep1/turn-02.jsonl).

## Step 2 plan and quota gates

Eight fresh sessions /88 selected student calls were planned. Seven valid sessions /77 calls completed: three C sessions and all four D sessions. All four paired batches were explicitly authorized. The final C/P-rep2 completed turns1–3 and hit usage limit at turn4. Its partial reply/tool output and snapshots are retained, but the entire failed session is excluded from selection. No automatic retry or splice occurred; temporary auth copies are zero.

Three complete matched pairs currently have lower D totals: S-rep1 C951267/D929649; P-rep1 C936192/D702404; S-rep2 C1156554/D783880. The valid unpaired D/P-rep2 uses948768. D's four-session total is3364701 tokens and its nonzero-exit command count is3, but no overall acceptance verdict is issued before the missing C session and blind review finish.

The CLI says to try again at Nov15,2026 2:50AM. Current host and client timezone is Eastern/New_York; the raw message itself has no UTC offset. See [failure evidence](failure-diagnostics.json). A new confirmation is required for a fresh11-turn C/P-rep2 recovery. It must start at turn1 with new report/work paths; the failed turn4 is never resumed. A recovery pair crossing quota windows must be disclosed. Independent Luna review is authorized but has not started: it requires all8 complete cases.

Each session uses its own turn-6 question to produce a correct turn-7 answer, recorded verbatim before phase 2. Failures remain separate, with no splicing. A quota failure stops the batch; no automatic recovery is authorized. Smoke and connection costs are separate from selected sessions.

Final analysis must use turn-10 thread-final counters plus the separate turn-11 thread, with per-turn deltas. Cached input is part of input, and reasoning output is part of output. `analyze_resources.py` requires eight completed sessions unless explicitly run in partial mode. Final semantic scores, saved-state audits and acceptance checks remain pending. A record hash change alone does not establish readiness or sound calibration.

## Pre-registered acceptance

D must save readiness after turn 10 in four cases out of four, have zero stale resumes out of four, and save on every status-change turn. Applicable M13 recheck and M14 labelled-offer checks must pass four times out of four. No M1–M10 check may be worse than concurrent C by more than one case. Failed tool commands across D must be at most four. D must cost less in at least three matched pairs out of four and use no more than 4,238,431 total input-plus-output tokens across its four sessions.

## Limits and publication

Synthetic packets, one model alias, scripted student, four planned sessions per arm. This does not measure learning gains, real students, other models, artifacts or billing. Timing includes host-tool delays and may cross quota windows; it is not a skill-speed effect. Original environment failures are retained in shared handoff history. No skill edits, release ZIP rebuild, self-approval or main merge.

Executed input/record snapshot bytes are preserved in executed-evidence.zip with raw/preview hashes. Further calls consume an immutable external frozen-packets copy, not LF-converted Git previews. Archive display-link corrections are logged separately; original message events remain. The final report will include blind rubric-v2 review, resource and command counts, save mechanics, record-byte/readiness/resume audits, privacy/auth/fingerprint checks and a manifest written last. Evidence ZIPs preserve executed input bytes separately from portable text previews.
