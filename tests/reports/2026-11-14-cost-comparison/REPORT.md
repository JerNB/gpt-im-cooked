# T007 C-versus-D controlled comparison

Completed 2026-11-15; Agent: codex. Test/report complete, pending cc cross-review. No source approval or main merge is implied.

## Finding

On two synthetic packets, D used **3,364,701 input-plus-output tokens** and concurrent/recovery C used **4,032,907**, a difference of **668,206**. D was lower in **4 matched pairs out of4** and below the registered historical-B ceiling of4,238,431 by873,730. The registered acceptance gates are met under the documented M6 adjudication. This is a descriptive resource finding, not a bill, learning-gain result or proof of broad quality equivalence.

D preserved the tested saved-state behavior: readiness saved in4 cases out of4, stale resume0 out of4, and same-turn saves for12 status assignments out of12. M13 markers and M14 labelled offers passed4 times out of4. The strict M1 value-overlap screen and M9 reply-checklist rule failed4 times out of4 in both arms; these absolute weaknesses are not hidden by the relative acceptance rule.

## Design and controls

- C=`4d102f6` (16 source files); D=`9938d36` (18 files), already source-reviewed. Older D3edde3b and later T003 tips were excluded.
- Model `gpt-6.1-sol`, medium, CLI0.162.1; Windows workspace-write/unelevated, non-login shell for both arms. Same B/C opener, T00479f3676 packets/scripts/rubric-v2.
- C/D × S/P ×2replicates:8 fresh selected sessions,11 turns each,88 valid student calls. S is statistics; P is programming. Packet/skill bytes were checked against frozen fingerprints, and runtime skill sources remained unchanged.
- Four paired batches were explicitly quota-confirmed: S1 C→D, P1 C→D, S2 D→C, P2 D→C. Global/bundled skills disabled; inherited CODEX variables stripped; actual first-turn materials/skill reads and no global-skill commands verified in all8 cases.
- Each turn7 answers its own question6 correctly. Answers were written before phase2 and match actual turn7 prompts verbatim8 times out of8. Separate turn11 thread IDs differ from tutor threads in all8 cases.
- One separate D/S smoke completed turns1–2 and passed all8 gates before the batches. One harmless connection probe is separate. Neither enters selected-session statistics.

## Session resource data

Cached input is a subset of input. Reasoning output is a subset of output; it is not added again. Thread-cumulative counters use the turn10 final value plus the independent turn11 value. All8 totals also match original local session token ledgers; token-only ledger projections are archived.

| Session | Input | Cached subset | Output | Input + output | Commands / nonzero exits |
|---|---:|---:|---:|---:|---:|
| C-S-rep1 | 941,204 | 875,264 | 10,063 | 951,267 | 18 / 1 |
| D-S-rep1 | 921,148 | 858,624 | 8,501 | 929,649 | 17 / 2 |
| C-P-rep1 | 924,616 | 859,392 | 11,576 | 936,192 | 18 / 2 |
| D-P-rep1 | 694,785 | 635,008 | 7,619 | 702,404 | 13 / 0 |
| D-S-rep2 | 776,060 | 691,968 | 7,820 | 783,880 | 15 / 1 |
| C-S-rep2 | 1,145,174 | 1,046,400 | 11,380 | 1,156,554 | 20 / 1 |
| D-P-rep2 | 939,877 | 835,200 | 8,891 | 948,768 | 15 / 0 |
| C-P-rep2 | 978,977 | 868,608 | 9,917 | 988,894 | 23 / 0 |

| Arm (4 sessions) | Input | Cached subset | Uncached input | Output | Input + output | Commands | Nonzero exits |
|---|---:|---:|---:|---:|---:|---:|---:|
| C | 3,989,971 | 3,649,664 | 340,307 | 42,936 | 4,032,907 | 79 | 4 |
| D | 3,331,870 | 3,020,800 | 311,070 | 32,831 | 3,364,701 | 60 | 3 |

Command counts are completed `command_execution` events. Nonzero exits are counted even when the last operation is an empty `rg` search after a successful read. D's3 nonzero exits are such composite searches; no D save failed or conflicted. Active CLI sums: C1,474.13seconds; D1,343.64seconds. They exclude between-phase/quota idle time and are not a controlled skill-speed estimate.

The per-session differences C−D are21,618 (S1),233,788 (P1),372,674 (S2),40,126 (P2). P2's C session is a fresh recovery after a quota window change; its D partner was retained from the earlier window. This limits temporal comparability.

## Requested per-turn deltas

Each row sums four sessions per arm. Full input/cached/output deltas for all88 turns are in per-turn-deltas.csv.

| Turn | C input + output | D input + output | C / D commands |
|---:|---:|---:|---:|
| 1 | 595,903 | 492,549 | 18 / 8 |
| 2 | 414,521 | 567,792 | 10 / 16 |
| 4 | 397,282 | 258,886 | 8 / 4 |
| 5 | 428,779 | 267,786 | 8 / 4 |
| 7 | 473,952 | 285,126 | 8 / 4 |
| 10 | 527,794 | 397,616 | 8 / 6 |

Turn2 is more expensive for D. Combined turns1–2 use1,010,424 tokens for C and1,060,341 for D: D uses49,917 more at the start. Later save/status turns4,5,7,10 are lower for D. The experiment does not isolate helper implementation from reference reads, response length, generated question/key differences or host-tool polling.

## Save mechanics and first-turn behavior

D made20 direct `record_io.py save` invocations. All20 exited successfully and final learning-record hashes matched helper output against preserved original snapshot bytes. Legacy read/update/commit helper invocations0; record-save inline wrappers0; record-save fallbacks0; conflict exits0; save-error exits0. Four manual-write candidates were separate practice answer-key artifacts, not record saves.

A direct helper invocation is one write command, not necessarily one total command in its tutoring turn. Instruction reads and other commands remain in D-save-audit.json; save-turn command totals are reported above.

D record files were absent afterturn1 and both present afterturn2 in4 cases out of4. No record templates were opened atturn1 (0 out of4), but `state.md` was read atturn1 in4 out of4. Deferred file creation worked; deferred state reading did not fully materialize. The diagnostic smoke happened not to read state atturn1; it is not substituted for these selected-session results.

## Behavior counts

Cells are pass /fail /unclear /not-applicable, except M8's count of complete three-topic coverage. No averaged quality score, percentages or significance tests are used.

| Check | C | D |
|---|---|---|
| M1 | 0 / 4 / 0 / 0 | 0 / 4 / 0 / 0 |
| M2a | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M2b | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M3 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M3b | 2 / 0 / 0 / 2 | 2 / 0 / 0 / 2 |
| M4 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M5 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M6 | 3 / 0 / 1 / 0 | 3 / 0 / 1 / 0 |
| M7 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M8 | 4 of4 complete | 4 of4 complete |
| M9 | 0 / 4 / 0 / 0 | 0 / 4 / 0 / 0 |
| M10 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M13 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |
| M14 | 4 / 0 / 0 / 0 | 4 / 0 / 0 / 0 |

- M11: C12 status assignments out of12 saved in the same turn; D12 out of12. Initial Needs practice is included; a Recheck-before-exam marker is not counted as a second status change.
- Saved readiness afterturn10: C4 out of4; D4 out of4. Functional stale resume: C0 out of4; D0 out of4. This is separate from a resume reply reciting the full checklist.
- M12 full three-element reply recap: C0 out of4; D0 out of4. C replies reflect1 element in each case; D reflects1 in three cases and2 in one. T1 retention recheck alone is not whole-assessment readiness review.
- M15 repeated opening markers: C15 of44 replies; D0 of44. A reply concatenates all agent messages for that student turn, including progress messages.

M1 sensitivity: all failures are explained worked examples whose values overlap a practice key, including different data/reference groups. The strict frozen value rule retains these collisions. LaTeX escaped percent signs are normalized for screening. These counts do not distinguish harmless numeric coincidence from practice-item-specific disclosure; they are not evidence that every practice question was solved for the student.

M9/M12 are narrow reply-content rules. Current saved evidence and a useful next lesson can coexist with missing gap/readiness recitation. The independent file-state audit found no stale recovery; do not describe those reply omissions as lost evidence.

M6: each arm has3 passes and1 unclear. The unresolved S overlap reverses a conditional while supplying an explicit denominator. The D count-only two-pass item (CASE04) is a narrow pass under the independent consistency review's literal changed-pass-count interpretation; the secondary review keeps it unclear. The latter would lower D's observed pass count by one. Original judgments and disputes remain archived. Recheck-marker compliance does not establish that every Demonstrated promotion was pedagogically justified.

## Registered gate decision

D passes all recorded gates: readiness4/4; stale0/4; status saves12/12; M13 and M14 each4/4; no M1–M10 pass-count deficit greater than one; failed commands3 against cap4; lower tokens4 of4 pairs against required3; total3,364,701 against cap4,238,431. Under selected M6 judgments, even treating remaining unclear cases adversarially leaves at most one pass deficit. This conclusion depends on the stated rubric/adjudication and this small scripted sample. It does not erase M1/M9 failures or establish an overall tutoring ranking.

## Blind review and evidence quality

Human authorized independent Luna subagents. Two primaries reviewed four masked cases each; an independent secondary reviewed M2/M6/M13 and saved-state audits across8 cases. A fresh consistency reviewer assessed M1/M6. They saw only shuffled case material and the common guide, without mapping/costs; record formats can still permit inference. Parent authored adaptive answers and knew labels/costs, so parent compilation is not blind.

Source checking found draft citation/case-index errors, a duplicate Recheck-as-status interpretation, and confusion between reply checklist coverage and file freshness. Reviewers supplied separate corrected versions; originals were retained. Final evidence quotes are extracted verbatim from the source responses/snapshots rather than treating paraphrased draft quotes as actual quotations. Review selections, disagreements and corrections are in review-adjudication.json. These are model-assisted judgments, pending cc cross-review.

## Failures, extra calls and recovery

The original C/P-rep2 completed3 turns then hit quota atturn4. Its partial response/read operation and snapshots are retained but its whole session is excluded. The process stopped, removed credentials and did not auto-retry. After a new explicit quota confirmation, recovery-C-P-rep2-20261115 ran all11 turns from1 with a different thread and new work/report paths. No old partial conversation was spliced. The other7 selected sessions are unchanged.

Current execution:95 CLI invocations,94 completed turns =88 selected +3 excluded partial +3 diagnostic, and1 failed turn. Diagnostic tokens are274,675, separate from selected costs. Failed-turn additional ledger usage is preserved separately; totals are lower bounds on all work because orchestration/reviewer use and unreported partial usage are excluded. A still earlier routing probe completed0 turns and is historical environment evidence, not a selected session or established bill.

## Verification, reproduction and limits

The source review at9938d36 preceded live testing:10 regression scripts passed,1 pre-existing distribution mismatch also reproduced on656b5f7, and16 direct save expectations passed. Original sanitized logs are in source-verification. No release ZIP was rebuilt. The new fake-CLI adapter test passes (C/D phases, exactly2 smoke turns, timeout/malformed/global-access evidence, auth cleanup, repeat guards and case/escape audits).

Re-analysis: `python tests/reports/2026-11-14-cost-comparison/analyze_resources.py` (no partial flag), then verify_run_integrity.py, finalize_scores.py. The integrity verifier needs the retained external CLI homes; archived token-ledger projections provide public counter evidence. `python tests/check_cost_comparison.py` uses a fake CLI only. Real runner invocations are opt-in, require source commits/auth and explicit quota approval; do not casually replay them.

Source/packet fingerprints, runtime source equality, privacy/auth scanning, syntax, package links and final committed Git-blob manifest verification accompany this report. Executed input and pre-normalization record bytes live in executed-evidence.zip; LF previews and both hashes are indexed. Only display links/paths are normalized, with transformations logged. The final manifest is generated after evidence/check metadata.

Two synthetic packets, one model alias/CLI, scripted student, author-written prompts, four cases per arm; adaptive questions and response lengths differ. No learning gains, real students, other models, artifact-heavy workloads, delayed real-student recheck, print or billing are measured. One pair crosses quota windows; timing is not causal. Future work should refine M1 item-specific exposure and M9/M12 functional-resume criteria before new data, and improve D's first-turn state-reading compliance without changing this frozen dataset.

Evidence: [protocol](protocol.json), [resource summary](resources-summary.json), [per-turn data](per-turn-deltas.csv), [automatic candidates](scores-auto.json), [semantic scores](scores-blind.json), [counts](counts.json), [acceptance](acceptance.json), [saved-state audit](saved-state-audit.json), [save mechanics](D-save-audit.json), [accounting](accounting-audit.json), [source review](SOURCE-REVIEW.md), [review decisions](review-adjudication.json), [attempt inventory](attempt-inventory.json), [original failure](failure-diagnostics.json).
