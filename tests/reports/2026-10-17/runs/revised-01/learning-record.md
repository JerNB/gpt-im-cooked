# Learning record

## Study setup

- Quick start shown: Yes — concise task-specific orientation and marker explanation provided on 2026-10-17.
- Language: English default. Requested outputs: saved feedback, learning record, one short next question and a separate solution.

## Active course and exam

[Course profile](course-profile.md): matching page/export identity is STA 199CCL / Exam 1. The supplied STA-DEMO / Midterm packet is a separate scope authority until linkage is confirmed.

## Concepts

| Concept ID / topic ID | Concept | Status | Priority and evidence | Corrective rule | Next task |
|---|---|---|---|---|---|
| EX1-DPLYR; packet T2 conceptual overlap | Row counts under grouped mutate and scalar summarise | Improving | Focused recheck: first response incorrectly predicted 2 rows; second correctly explained 4 after the page had revealed the answer. Not independent transfer or mastery. | Grouping does not remove rows; mutate preserves observations; summarise with one scalar per group gives one row per group. C1 transfer task; P1 L2. | Answer next-01 without opening its key; choose operation from desired output unit and explain alternative. |

No performance claims for packet T1, T3, or T4; no useful attempts were supplied for those concepts. Exploration settings are not performance evidence.

## Attempt history

| Occurred-at UTC | Attempt / item | Concept | Original response | Outcome | Assistance judgment | Answer evidence | Feedback |
|---|---|---|---|---|---|---|---|
| 2026-10-14T16:42:32.829Z | mv8c5njy-qg5zcp / transfer-region-mean-rows | EX1-DPLYR | “2”; “There are two regions, so I expected one result row per region.” | Incorrect for intended four-state mutate question; confuses scalar summarise row structure with mutate | Pre-first-feedback submission in this page session; outside assistance unknown | Reasoned solution from C1 task and P1 L2; no R execution | [feedback.md](feedback.md) |
| 2026-10-14T16:43:07.812Z | mv8c973g-40rtr5 / transfer-region-mean-rows | EX1-DPLYR | “4”; “mutate attaches the region mean to every existing state row, so all four states remain.” | Correct explanation after feedback; useful correction, same question | Assisted retry after first check revealed 4 rows and explanation; exported stage/flags are not adopted as tutor judgment | Reasoned solution from C1 task and P1 L2; no R execution | [feedback.md](feedback.md) |

Both responses use East/Pine, East/Lake, West/Mesa, West/Cedar and the intended grouped-mutate mean task. Original JSON remains unchanged. Literal operation field references tax_rate despite data field rate; artifact defect is separate from student reasoning.

## Import ledger

No prior record or import ledger existed at review. Schema and exact page item/conditions matched before review. The packet's different course label is not used to reidentify the artifact.

| Course / artifact / versions | Session / attempt | Original path / SHA-256 | Reviewed snapshot or revision | Review date / feedback | Supersedes / reason |
|---|---|---|---|---|---|
| STA 199CCL Exam 1 / sta199-ex1-grouped-mutate-vs-summarize / package 1.0.0, artifact 1.0.0, schema 1.0 | mv8c5njy-1xx0jk / mv8c5njy-qg5zcp | [attempt.json](attempt.json); 19aa3be22e9c4b83f9424b3fd7ee4c2f9354323365207b44fba5014eeba8e548 | transfer_history[0]; first review | 2026-10-17 / [feedback.md](feedback.md) | No prior tutor review; original incorrect prediction retained |
| STA 199CCL Exam 1 / sta199-ex1-grouped-mutate-vs-summarize / package 1.0.0, artifact 1.0.0, schema 1.0 | mv8c5njy-1xx0jk / mv8c973g-40rtr5 | [attempt.json](attempt.json); 19aa3be22e9c4b83f9424b3fd7ee4c2f9354323365207b44fba5014eeba8e548 | transfer_history[1]; distinct explicit retry, not a re-export success | 2026-10-17 / [feedback.md](feedback.md) | Qualifies exported independent_transfer / false reveal flag: C1 check reveals solution before retry; preserve original flags and correct later assistance judgment only |

Exported-at: 2026-10-14T16:43:14.915Z. Reviewed-at: 2026-10-17 (review time unspecified). Attempt times are occurrence times, not review times. A later unchanged import must not append these attempts again. No earlier guides were found to reconcile. Current unsubmitted response is null.

## Student-reported difficulties

None separately reported. The first response is reviewed evidence of confusion, not a self-report or a broad diagnosis.

## Open questions

- Confirm whether the STA-DEMO packet is meant to define STA 199 Exam 1 scope before planning broader exam work. No clarification is required to review the matched page's intended row-count question.
- Exported tax_rate expression versus rate data field is an artifact inconsistency; literal R validity unresolved.
- External slides/Lab 2 remain unread; skewness notes absent. Do not teach T4 from its name.
- Packet E1/K1 Q4 denominator population remains ambiguous; no student error assigned.

## Next session

- Current activity: Reviewed two attempts with chronology-sensitive assistance correction.
- Revisit: EX1-DPLYR row counts; current status Improving after assisted correction.
- Artifacts: [feedback](feedback.md), [original export](attempt.json), [page](concept.html), [course profile](course-profile.md).
- Next action: Submit one or two sentences for [next-01](next-question.md) before opening its separate key; record any hint/key exposure. This new item is currently unattempted.
- Persistence: Saved here in learning-record.md; bring this directory into a new chat for continuity.
