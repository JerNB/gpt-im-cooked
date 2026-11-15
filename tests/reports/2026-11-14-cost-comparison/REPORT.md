# T007 C-versus-D comparison — work in progress

Agent: codex. The comparison is incomplete; no improvement or acceptance verdict is available.

## Frozen inputs and method

C is `4d102f6` (16 skill files); D is the source-reviewed `9938d36` (18 files). Both fingerprint sets match. Packets S/P, scripts and rubric-v2 come from T004 `79f3676`'s exact executed-input archive. The newer T003 skill tip and older D revision are excluded. The adapter uses the identical B/C opener, `gpt-6.1-sol`, medium effort and CLI `0.162.1`. Global and bundled skills are disabled, command accesses audited, and inherited CODEX environment variables removed. Both arms use non-login shells.

The isolated worktree and an empty Git commit verified Git writes. A separate harmless connection probe completed once and returned `T007_OK`. It is excluded from student-session costs.

## Step 1 diagnostic

One D/S session completed exactly turns 1–2. All eight gate checks passed: actual materials and skill read, no global-skill access, no record files after turn 1, both record files after turn 2, one successful `record_io.py save` invocation, no separate read/update/commit invocation, and no inline save wrapper. The save uses a PowerShell here-string JSON pipeline. The two earlier turn-2 commands read instructions/materials; they are not separate record-update calls.

Turn 1 opened first-use guidance but neither record template nor core state.md. Turn 2 opened state.md and state-reference.md. The diagnostic has two student calls, one save and no fallback; copied auth files remaining: zero. It is not a selected comparison session. See [gate](smoke-001/smoke-gate.json), [summary](smoke-summary.json) and [events](smoke-001/runs/D-S-rep1/turn-02.jsonl).

## Step 2 plan and quota gates

Eight fresh sessions /88 student calls: C/D × S/P × two replicates. Four paired batches: S-rep1 C→D; P-rep1 C→D; S-rep2 D→C; P-rep2 D→C. Each batch requires a separate explicit human quota confirmation. Batch 01 (S-rep1, 22 calls) completed. C used 951,267 input-plus-output tokens and D used 929,649, a difference of 21,618. D was lower in this one pair; three pairs remain, so no acceptance conclusion follows. Failed commands: C one, D two (empty-search composite exits are counted). No quota failures occurred. Batch 02 (P-rep1) also completed: C936192 tokens, D702404, difference233788. Across the two completed pairs, D is lower twice out of two. Four selected sessions/44calls are complete; the four-session-per-arm acceptance remains unevaluated. Batch03 S-rep2 D→C completed: D783880 tokens, C1156554, difference372674. Six sessions/66calls are complete; D is lower in three completed matched pairs out of three. Batch04 P-rep2 D→C is awaiting quota confirmation. Independent Luna blind review has been explicitly authorized for the complete eight-case dataset.

Each session uses its own turn-6 question to produce a correct turn-7 answer, recorded verbatim before phase 2. Failures remain separate, with no splicing. A quota failure stops the batch; no automatic recovery is authorized. Smoke and connection costs are separate from selected sessions.

Final analysis must use turn-10 thread-final counters plus the separate turn-11 thread, with per-turn deltas. Cached input is part of input, and reasoning output is part of output. `analyze_resources.py` requires eight completed sessions unless explicitly run in partial mode. Final semantic scores, saved-state audits and acceptance checks remain pending. A record hash change alone does not establish readiness or sound calibration.

## Pre-registered acceptance

D must save readiness after turn 10 in four cases out of four, have zero stale resumes out of four, and save on every status-change turn. Applicable M13 recheck and M14 labelled-offer checks must pass four times out of four. No M1–M10 check may be worse than concurrent C by more than one case. Failed tool commands across D must be at most four. D must cost less in at least three matched pairs out of four and use no more than 4,238,431 total input-plus-output tokens across its four sessions.

## Limits and publication

Synthetic packets, one model alias, scripted student, four planned sessions per arm. This does not measure learning gains, real students, other models, artifacts or billing. Timing includes host-tool delays and may cross quota windows; it is not a skill-speed effect. Original environment failures are retained in shared handoff history. No skill edits, release ZIP rebuild, self-approval or main merge.

Executed input/record snapshot bytes are preserved in executed-evidence.zip with raw/preview hashes. Further calls consume an immutable external frozen-packets copy, not LF-converted Git previews. Archive display-link corrections are logged separately; original message events remain. The final report will include blind rubric-v2 review, resource and command counts, save mechanics, record-byte/readiness/resume audits, privacy/auth/fingerprint checks and a manifest written last. Evidence ZIPs preserve executed input bytes separately from portable text previews.
