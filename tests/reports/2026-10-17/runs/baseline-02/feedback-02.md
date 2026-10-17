# Export revision feedback

Reviewed 2026-10-17. This supplements [feedback-01.md](feedback-01.md); the original correctness judgment remains valid.

## What changed

| File | Attempt identity within evidence-session | Review outcome |
|---|---|---|
| [before.json](before.json) | evidence-session:1 | Exact file hash matches the previously reviewed import. No duplicate attempt or success added. Q4 B and its correct explanation are preserved. |
| [after.json](after.json) | evidence-session:1 | Same attempt, additional assistance-history revision. Responses are unchanged. History retains the first export and a before-key-access snapshot; current items record key access. This is not a new success or a corrected answer. |
| [retry.json](retry.json) | evidence-session:2 | A distinct retry following the recorded key opening and retry event. Q4 repeats the same correct answer and explanation. Count as assisted/repeated practice after key exposure, not a new independent transfer context. |

All exports have schema 1.0, package 0.4.1, artifact `cooked-stats-mock-a` v0.3.1, and the same course/exam and item mappings already checked against [worksheet.html](worksheet.html). The earlier snapshots are preserved as prefixes in the later histories; there are no contradictory answers or artifact-identity conflicts.

## Preserved original answer and judgment

Attempt 1 Q4 selection: `["B"]`.

Original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70."

This same answer and explanation appear in every supplied Q4 snapshot and in attempt 2. They are **correct**: the requested population is all 40 Plus-plan tickets, of which 28 had short waits. Basis: [course-packet.md S3](course-packet.md#s3-denominators), [worksheet.html Q4](worksheet.html#q4), and answer-key.html Question 4. Answer evidence: **Reasoned solution**, with arithmetic verified in the prior review using Python 3.13.12. No new calculation or R execution was needed or performed for this revision review. No instructor rubric is supplied.

## Assistance and timing

In after.json, attempt-history positions 0 and 1 preserve Q4 with `key_opened_in_page: false`; position 1 is explicitly labeled `before key access`. The following `key_opened` event and position 2/current items have key access recorded. In retry.json, positions 0-2 preserve that history, position 3 is `before retry`, and position 4/current items belong to attempt 2 with key access still true. The worksheet exporter snapshots before opening the key and retains the key flag across retries, consistent with these files.

Thus later key access does **not** retroactively make attempt 1's preserved pre-key answer assisted by that later key opening. It also does not prove attempt 1 was fully independent: external help remains untracked, and no item response time is supplied. Attempt 2 is after known key exposure and cannot establish unaided recall or independent transfer. Key exposure does not establish whether the student read or used a particular line of the key.

Every supplied export, snapshot, and event uses the same timestamp, 2026-10-17T02:00:00.000Z. The sequence above relies on explicit snapshot labels, history order, attempt order, and exporter behavior, not elapsed-time claims. P01's undated response cannot be placed precisely relative to these exports.

## Record decision and next step

The concept remains **Improving**: retain P01's correct explained response with its no-help self-report; retain attempt 1's correct pre-key work with outside assistance unresolved; add attempt 2 as correct assisted repetition. There is no new misconception, confirmed independent transfer, or basis for Demonstrated status. Q1-q3 and Q5-q8 are still blank in every supplied snapshot: unattempted, not wrong.

The original JSON exports, prior feedback, original responses, and [pending transfer question](next-question-01.md) are preserved. No response to that new question has been supplied. Try it before opening its separate solution if you have not already done so, and report any assistance when submitting. The [learning record](learning-record.md) now distinguishes the revisions and retry.

## File provenance

| Original file | SHA-256 |
|---|---|
| before.json | 8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6 |
| after.json | 81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1 |
| retry.json | 9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318 |
