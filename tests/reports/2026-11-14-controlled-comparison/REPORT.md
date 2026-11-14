# T004 controlled comparison

Status: **REVIEW — execution and scoring complete; cc cross-review pending.** Agent: codex. Sixteen valid sessions /176 student calls, four per arm, are selected. The final A1-S-rep2 is a new labelled whole-session supplemental run after the quota reset. Failed sessions and diagnostics are preserved and excluded from the selected sample. No author approval or main merge was performed.

## A2 versus B

The strong-prompt baseline and B tie on the scored turn-5 overconfidence and whole-exam readiness checks: each passed four times out of four. Each passed answer-leak prevention (M1) three times out of four. B produced a genuine transfer check four times out of four; A2 did so twice out of four. Complete resume coverage of all three M12 elements appeared once out of four for A2 and zero times out of four for B. These are different observed behaviors, not an overall quality ranking.

## C versus B

- **M11:** all assessable explicit status announcements were saved in the same turn: C eight times out of eight events, B once out of one event. Three B sessions had no assessable explicit status-change announcement. This sample does not establish a unique C improvement or prove that every unspoken judgment was saved.
- **M12:** C reflected all three resume elements once out of four; B did so zero times out of four. C therefore did not fully repair reply completeness. This metric concerns what the resume reply reflects, not proof of data loss in its saved file.
- **M13:** C carried the required exam recheck marker four times out of four formal same-session Demonstrated cases. B lacked it in all three applicable cases; the remaining B session had no formal assignment. This is the clearest observed rule change.
- **M14:** C offered an explicitly labelled outside-course general explanation four times out of four; B did so once out of four. The script did not accept those offers, so the accepted-general-explanation path was not tested.
- **M1–M10:** no uniform improvement. M1 tied at three passes out of four. C's M6 passed three times out of four versus B's four times out of four: one C item was a new story with the same explicit-group calculation. A recheck marker does not make such an item a genuine transfer. Do not infer that all later Demonstrated promotions were justified from the turn-5 M2 pressure check.

## Behavioral counts

| Arm | n | M1 pass /fail | M2a pass /fail | M6 pass /fail /unclear | M12 complete (3/3) | M13 pass /fail /not applicable |
|---|---:|---|---|---|---:|---|
| A1 | 4 | 2 /2 | 3 /1 | 3 /0 /1 | 0 | 0 /0 /4 |
| A2 | 4 | 3 /1 | 4 /0 | 2 /2 /0 | 1 | 0 /0 /4 |
| B | 4 | 3 /1 | 4 /0 | 4 /0 /0 | 0 | 0 /3 /1 |
| C | 4 | 3 /1 | 4 /0 | 3 /1 /0 | 1 | 4 /0 /0 |

All four arms withheld unqualified whole-exam readiness in four sessions out of four. A1's resume limitation is partly structural because its opener did not ask for a progress file. No averaged quality score, percentages or significance tests are calculated. The final case's M1 primary rating was corrected after checking its actual Q1 solution against the frozen v2 rubric; both final reviewers fail it. The other fifteen case judgments and prior adjudications are unchanged.

## Resource differences

Each row has four completed sessions /44 student calls. CLI usage is cumulative per thread: use deltas, or the last value in the ten-turn thread plus the independent resume thread. All sixteen totals match underlying session records. Cached input is a subset of input; reasoning output is a subset of output. Neither is added twice.

| Arm | Input tokens | Cached input subset | Output tokens | Input + output | Sum of active CLI seconds |
|---|---:|---:|---:|---:|---:|
| A1 | 1,435,938 | 1,267,200 | 9,029 | 1,444,967 | 783.65 |
| A2 | 3,278,812 | 3,073,664 | 19,344 | 3,298,156 | 1421.25 |
| B | 4,207,962 | 3,916,160 | 30,469 | 4,238,431 | 1870.32 |
| C | 5,494,047 | 5,090,176 | 45,338 | 5,539,385 | 2051.23 |

In these four-session samples, B used 940,275 more input-plus-output tokens than A2; C used 1,300,954 more than B; A2 used 1,853,189 more than A1. This run did not show a C token reduction. The experiment does not isolate the contributions of instruction reads, saved records, response length and host-tool polling.

The absolute differences are descriptive resource use on this script. A1-S-rep2 was added after a quota reset with a separately archived environment preflight, a new tutor thread, and unchanged study files. Runs span quota windows, runtime routing fixes, host-tool delays and different response lengths. Active CLI sums exclude between-phase preparation/quota idle time and are not a controlled estimate of skill speed. They are not billing amounts. Diagnostic retries, separate preflights, reviewer and orchestration costs are not included in this selected-student-call table; known extra CLI use is listed separately in the attempt inventory.

## Methods and evidence

Model gpt-6.1-sol, medium; CLI0.162.1. B is97be172; C is4d102f6. All16 C files and all7 original S files were fingerprint-checked. Later cc commits07339dc/76491c0 were excluded from this tutoring dataset. Two synthetic packets, two replicates, opposite scheduled arm orders; actual starts and recovery labels are retained. Turn7 answers address each session's own question and were recorded before phase2. Original failures were never spliced into complete sessions.

Automatic checks/candidates precede semantic review. Opening markers and skill references were stripped and sessions shuffled. Fresh Codex/Luna scorers had no mapping/costs; M2/M6 received independent second passes, and the supplemental case also received independent status review. Record formats permit inference, so blinding is partial. Parent adjudication is also partial because the parent authored adaptive answers and previously saw labelled turn6 prompts. Original judgments, corrections and disagreements remain available.

This measures observable tutor behavior on synthetic, scripted, author-written prompts with one model alias. It does not measure learning gains, real students, other models, mock exams/guides, print or billing. The accepted general-help branch and delayed real-student recheck were not exercised.

Links: [protocol](final/protocol.json), [scores-auto](final/scores-auto.json), [scores-blind](final/scores-blind.json), [counts](final/counts.json), [per-session resources](final/resources.csv), [accounting audit](final/accounting-audit.json), [diagnostic history](DIAGNOSTICS.md), [attempt inventory](attempt-inventory.json), [original T003 source review](SOURCE-REVIEW.md). The T003 later-fix re-review is a separate collaboration record after T004 closure.

## Archive and verification

Executed frozen bytes are in [executed-inputs.zip](executed-inputs.zip); [the input index](executed-input-index.json) records raw and LF-preview hashes. Other text paths/CJK console output and archive-display links are normalized with transformation records; raw structured events remain available. Immutable materials and final study trees are mirrored, with per-turn snapshots separate. Publication validation, privacy/auth checks, frozen-input checks and a final Git-blob fingerprint audit accompany the manifest. These checks are archive/packaging evidence, not a claim that every original model-produced link or every behavior passed.

M15 is descriptive: repeated opening markers appeared in 0 of 44 replies for A1, 0 of 44 replies for A2, 11 of 44 replies for B, 22 of 44 replies for C. A reply here concatenates the CLI agent messages for that student turn, including progress messages.
