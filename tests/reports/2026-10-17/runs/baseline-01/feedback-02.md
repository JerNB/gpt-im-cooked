# Export revision feedback — review 02

Reviewed 2026-10-17. Fictional intro statistics / Mock Exam A.

## What changed
| Export | Attempt identity | Answer changes | Assistance/history changes | Evidence treatment |
|---|---|---|---|---|
| [before.json](before.json), supplied again | evidence-session / evidence-session:1 | None; unchanged hash from review 01 | None | Duplicate import: no additional performance evidence |
| [after.json](after.json) | evidence-session / evidence-session:1 | None: Q4 B and the same explanation; seven blanks | Adds `before key access` snapshot, `key_opened` event, and post-access snapshot; current key flag true | Revision of the first attempt, not another success |
| [retry.json](retry.json) | evidence-session / evidence-session:2, order 2 | Same Q4 B and explanation again; seven blanks | Preserves first-attempt history, adds `before retry` snapshot and retry event, then second-attempt export; key flag remains true | Distinct retry, same question; correct following recorded key access, not independent transfer |

There are **two worksheet attempt identities**, not three successes and not five successes from retry.json's five snapshots. Repeated histories across files refer to the same events. The before.json reimport adds no duplicate ledger row or performance entry.

## Your original answer remains correct
Original Q4 answer in both attempts: `["B"]`.

Original explanation in both attempts: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70."

[Worksheet Q4](worksheet.html#q4) asks for the fraction of Plus-plan tickets with short waits. The reference population is all 40 Plus tickets; 28 match, so 28/40 = 0.70. Teaching basis: [course-packet.md](course-packet.md), S3. Solution evidence: **Reasoned solution**, agreeing with [answer-key.html](answer-key.html), Question 4; **Verified computation** from review 01 (Python 3.13.12). The supplied practice key is not an instructor key.

## Assistance reconciliation
The new later flag does **not** retroactively make the original response assisted: after.json's `attempt_history[1]` explicitly preserves that correct answer in a `before key access` snapshot with key flag false. It matches before.json. Original Q4 therefore remains correct before recorded in-page key access, with external help still unknown.

The key event records opening the separate key, not proof that any particular solution was read or copied. The worksheet script snapshots before key access and uses a session-wide `keyOpened` flag in `collect()`. Its retry handler increments the attempt number and resets the form without resetting that flag (worksheet.html script, lines 17, 22–25). Thus retry 2 remains exposed to previously opened solutions; classify the repeated correct answer as post-key/assisted-context practice, not a fresh independent success. No claim of copying is made.

All exports, snapshots, and events share `2026-10-17T02:00:00.000Z`. Structural history, explicit snapshot reasons, and the retry event support the sequence; equal timestamps alone cannot establish exact answer times, elapsed durations, or a timeline relative to undated P01.

## Learning decision and next step
Status remains **Improving**. Preserve P01's independently reported explanation and first-attempt Q4's pre-key explanation. Key access alone does not prove learning or deterioration; the same task repeated after access does not meet the independent-transfer requirement for Demonstrated. No answers were corrected and no new misconception was observed. Q1–Q3 and Q5–Q8 remain unattempted, with no weakness inferred.

Use the existing [short follow-up](next-question.md) for a different reference population and explain the denominator before opening [its solution](next-solution.md). That question remains unattempted; reading/exporting worksheet answers supplies no evidence about it. [Feedback 01](feedback-01.md) remains the historical review; this review supplements its assistance account and import history without changing its correctness judgment. The existing follow-up and key remain applicable; no older guide requires revision.

## Import audit
All three exports match schema 1.0, package 0.4.1, artifact `cooked-stats-mock-a` v0.3.1, course/exam, ordered item IDs, topic IDs, and source locators. Those identities were already checked against the worksheet in review 01. Programmatic comparisons now confirmed the original answer and explanation are identical in every current/history snapshot, preserved history prefixes match, and before.json's hash is unchanged. Exports remain byte-for-byte unchanged.

| File | SHA-256 | Exported at | Reviewed at |
|---|---|---|---|
| [before.json](before.json) | `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6` | 2026-10-17T02:00:00.000Z | 2026-10-17 (date only) |
| [after.json](after.json) | `81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1` | 2026-10-17T02:00:00.000Z | 2026-10-17 (date only) |
| [retry.json](retry.json) | `9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318` | 2026-10-17T02:00:00.000Z | 2026-10-17 (date only) |
