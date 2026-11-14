# T004 controlled comparison — WIP

Status: **BLOCKED, not complete**. Agent: codex. Fifteen valid complete sessions (165 student calls) are retained; the target is sixteen sessions / 176 calls. A1-S-rep2 failed again at turn 8 because the service usage limit was reached. The service says to retry after 3:35 PM on November 14. Its seven completed calls are diagnostic only, not a complete selected session. A later run must start from turn 1 in a new labelled session.

## Source review

Claude's four skill-file edits implement save-on-status/readiness, same-session exam recheck markers, and a labelled optional general explanation for source gaps. Nine existing checks pass on the pushed T003 archive. Distribution verification fails on both T003 and baseline, matching the pre-existing release-archive mismatch. [Source review](SOURCE-REVIEW.md) requests changes to the cc-owned pilot harness for global-skill isolation, credential lifecycle, report binding and sanitization. No skill or release ZIP was edited here. No merge or approval was performed.

## Available evidence

- [Partial blinded scores](final/scores-blind.json), [partial counts](final/counts-partial.json), and [automatic candidates](final/scores-auto.json).
- [Per-session resources](final/resources.csv) and [session-accounting audit](final/accounting-audit.json). CLI usage is cumulative per thread; use deltas or the last value per thread, then add the independent resume thread. All 15 selected accounting totals match the underlying session records. Cached tokens are a subset of input; reasoning tokens are a subset of output. Neither is added twice.
- [Attempt history](DIAGNOSTICS.md), [completion/next step](final/completion.json), and separate raw report directories retain invalid, quota-failed and corrected runs.
- Frozen model: gpt-6.1-sol, medium; CLI 0.162.1. B: 97be172; C: 4d102f6, with all 16 skill fingerprints checked. The corrected S packet's seven original files match Git and supplied pilot fingerprints byte for byte. P was authored before its first call and retained under per-run fixture fingerprints.

## Interpretation limits

There are four completed sessions each for A2, B and C, but only three for A1. No percentages, significance tests or final sixteen-session conclusion are supplied. M2/M6 received independent blinded second passes; disagreements and partially blind parent adjudications are retained. C's additional recheck marker does not by itself prove that a generated question is a real transfer task; inspect M6 and the original question. Explicit status-announcement checks do not measure every unspoken change in judgment.

This is a synthetic, scripted, one-model study, not learning gains or real-student outcomes. Mock exams, guides, print and billing are not measured. Runs span quota windows, runtime routing fixes and host-tool delays. One A1 recovery used a separately archived fixed-file environment preflight, followed by a new tutor thread with unchanged study files; it still later failed quota and is excluded. Do not pool latency as a skill-only effect. Diagnostic/model-review/orchestration costs are not equivalent to the selected tutoring-call resource table.

## Archive handling

Executed frozen input/skill bytes are retained in [executed-inputs.zip](executed-inputs.zip); [the input index](executed-input-index.json) records executed and LF-preview hashes. Plaintext previews use LF for portable Git storage. Corrected S originals and C skill files already use LF and still match their supplied fingerprints. Other text is sanitized for user/work paths, runtime drive prefixes and mis-decoded CJK output; changed-file pre/post hashes are recorded. Final study trees and immutable material files are mirrored where available. Per-turn snapshots remain separate from final state. A SHA-256 manifest covers this WIP archive; it is not an assertion that the experiment is done.

## Provisional behavioral counts

These are counts from the 15 completed sessions, not a completed 16-session finding. No averaged quality score is calculated.

| Arm | n | M1 pass / fail | M6 pass / fail / unclear | M12 complete (3/3) | M13 pass / fail / not applicable |
|---|---:|---|---|---:|---|
| A1 | 3 | 2 / 1 | 2 / 0 / 1 | 0 | 0 / 0 / 3 |
| A2 | 4 | 3 / 1 | 2 / 2 / 0 | 1 | 0 / 0 / 4 |
| B | 4 | 3 / 1 | 4 / 0 / 0 | 0 | 0 / 3 / 1 |
| C | 4 | 3 / 1 | 3 / 1 / 0 | 1 | 4 / 0 / 0 |

All assessed turn-5 overconfidence and whole-exam readiness checks passed. This does not establish that every later Demonstrated promotion was justified: a before-exam marker is independent of whether the check was real transfer. Explicit M11 announcements that were assessable coincided with a saved-file change; many other replies used no formal change announcement, so absence of a failure is not proof of universal immediate saving. The C revisions did not eliminate every M1/M6 or resume-completeness weakness in this small sample. A1's resume limitation is partly structural because it was not instructed to keep a progress file.

[Attempt inventory](attempt-inventory.json) reports known completed-call resource use across diagnostics and retries, separately from the selected-session table. It excludes unobserved failed-call usage and orchestration/reviewer costs. [Archive link transformations](archive-link-transformations.json) records portability edits to rendered Markdown; original structured events retain the corresponding sanitized raw messages. Publication validation checks the archive, not original tutor-link quality.
