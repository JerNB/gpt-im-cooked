# Feedback 02: export history review

Reviewed 2026-10-17. Sources: [before.json](before.json), [after.json](after.json), [retry.json](retry.json); [worksheet.html](worksheet.html#q4), Q4 and its snapshot/key/retry/export implementation; [course-packet.md](course-packet.md), S3; [answer-key.html](answer-key.html), Q4. Original exports and [feedback-01.md](feedback-01.md) are preserved.

## What changed

| Export | Attempt | Response | Assistance/history | Interpretation |
|---|---|---|---|---|
| before.json, resubmitted unchanged | evidence-session:1 | Q4 B with correct explanation | Key flag false; no hints recorded; outside help untracked | Already reviewed; no duplicate learning evidence |
| after.json | evidence-session:1 | All answers and explanations unchanged | Key flag true; key_opened event; matching export and before-key-access snapshots retain Q4 with flag false | A revision of attempt 1 with new assistance history, not another attempt or success |
| retry.json | evidence-session:2 | Q4 B with the same correct explanation | Explicit retry event from attempt 1; before-retry snapshot preserved; key flag remains true for attempt 2 | A distinct retry, correct after key access; assisted/re-exposure practice, not independent transfer |

All three have schema 1.0, package 0.4.1, artifact cooked-stats-mock-a v0.3.1, session evidence-session, course Fictional intro statistics / Mock Exam A. Identities and item mappings match the worksheet. The histories are consistent prefixes, not contradictory versions. Duplicate snapshots count once within their attempt.

The original Question 4 selection is `["B"]`. Its explanation is unchanged in every snapshot and both attempts:

> The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70.

**Correct, including reasoning.** Packet S3 and worksheet Q4 require the Plus-plan population, so 40 is the denominator. Answer evidence: **Reasoned solution**, supported by the supplied reasoned key Q4; arithmetic was verified in the previous review. No new arithmetic execution is claimed in this review. No instructor points rubric is supplied.

The later true key flag does not erase the saved pre-key answer: the worksheet snapshots immediately before recording key access, and that snapshot already has the same correct response. Retain the original pre-key evidence, with outside help still unknown. The post-key revision is not a correction, because the answer did not change. The distinct retry is after key exposure and cannot count as a fresh independent demonstration, even though it is correct.

All export, snapshot and event timestamps are `2026-10-17T02:00:00.000Z`. The sequence above uses explicit snapshot reasons, event order, attempt order and worksheet behavior; tied timestamps do not establish elapsed time or precise answer-entry times. P01 remains undated and cannot be placed before or after the exports by time.

Questions 1, 2, 3, 5, 6, 7 and 8 remain **unattempted in both attempts**. Their blanks do not establish errors or weaknesses. No overall exam score is assigned.

## Record decision

Denominator selection remains **Improving**. P01 supplies the earlier documented correct explanation with student-reported independence; worksheet attempt 1 supplies one correct pre-key explanation with outside help unknown; attempt 2 supplies correct assisted repetition on the same item. No new independent context or transfer success has been established. This review supplements feedback-01's assistance history; its Q4 correctness judgment stands. No pending question or solution is changed.

Next: try the already assigned [N01](next-question-01.md) before opening its separate solution, and report any help or prior solution access. N01 is still unattempted.

## Import hashes

- `before.json`: `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6`.
- `after.json`: `81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1`.
- `retry.json`: `9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318`.
