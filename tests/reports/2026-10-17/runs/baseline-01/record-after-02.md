# Learning record

## Study setup
- Quick start shown: Yes
- Language: English

## Active course and exam
Fictional intro statistics / Mock Exam A; [course profile](course-profile.md).

## Concepts
| Concept ID | Concept | Status | Evidence | Next task |
|---|---|---|---|---|
| within-group-denominator | Reference population | Improving | P01 independently reported correct after an earlier error. Attempt evidence-session:1 Q4 correct with population explanation before recorded key access; external help unknown. after.json preserves this pre-key response and adds later key access without answer changes. Retry evidence-session:2 repeats the same correct Q4 after key access: distinct retry, assisted/exposed context, no new independent transfer. Not Demonstrated. Basis: course-packet.md S3; feedback-01.md; feedback-02.md. | Attempt next-question.md independently with a reference-population explanation before opening its solution; clarify prior external help when relevant. |

Corrective rule retained: name the reference population, then divide the matching count by that population's total (course-packet.md S3). Blank worksheet items supply no assessed evidence about their topics.

## Attempt history
P01 original response: "Six overdue fiction loans out of 15 fiction loans: 6/15; out of all 40 loans: 6/40. The requested population sets the denominator." Reviewed correct; independence is student-reported. Prior wrong original response: "6/40 in both because always use all rows." Corrected in prior feedback. Date unknown.

Reviewed 2026-10-17: [before.json](before.json), session `evidence-session`, attempt `evidence-session:1`, Q4 (within-group-denominator). Original answer `["B"]`; original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct against worksheet.html Q4, answer-key.html Question 4, and course-packet.md S3. Solution evidence: Reasoned solution and Verified computation (Python 3.13.12). Assistance: no in-page hint/key recorded; external help untracked. Actual item answer time unknown. Current items and attempt-history snapshot duplicate the same response and count once. Q1–Q3/Q5–Q8 unattempted. Full review: [feedback-01.md](feedback-01.md).


Review 02, 2026-10-17: before.json reimport is byte-identical and adds no performance evidence. after.json is a revision of `evidence-session:1`, not a new attempt. It preserves Q4's original B and explanation in a `before key access` snapshot, then records key access with the answer unchanged. This supplements review 01's assistance account; its original correct, pre-recorded-key judgment stands, with external help unknown. Later key access does not retroactively mark the preserved original response assisted.

Retry `evidence-session:2` in [retry.json](retry.json), order 2: Q4 original answer `["B"]`; original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct under packet S3 / worksheet Q4 / key Question 4. Assistance: no hint recorded, key flag true carried from the same session, external help untracked. Distinct explicit retry, same question following recorded key access: assisted/exposed-context correct practice, not independent transfer. No evidence of reading a particular answer or copying. Seven other items still unattempted. Answer evidence remains Reasoned solution / Verified computation as in review 01. Full revision review: [feedback-02.md](feedback-02.md).

No response was changed by the tutor; original exports are preserved unchanged. Repeated first-attempt snapshots across all files are deduplicated. Two worksheet attempt IDs cover the same Q4 context; no status promotion from snapshots, re-export, or key access. Equal timestamps prevent exact duration/answer timing claims; the explicit before-key/before-retry history and retry event supply structural order.

## Import ledger
| Export and SHA-256 | Course / artifact | Attempt identity | Timing | Review |
|---|---|---|---|---|
| [before.json](before.json); `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6` | Fictional intro statistics / Mock Exam A; cooked-stats-mock-a v0.3.1; package 0.4.1; schema 1.0 | Session evidence-session; attempt evidence-session:1; order 1 | Exported 2026-10-17T02:00:00.000Z; snapshot time identical; actual Q4 answer time unknown; reviewed 2026-10-17 | First import; worksheet identity and Q4/key match checked. Q4 correct, assistance partly unknown; seven blanks unattempted. One attempt, no duplicate evidence from history. Original preserved; feedback-01.md. |
| [after.json](after.json); `81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1` | Same course/exam; cooked-stats-mock-a v0.3.1; package 0.4.1; schema 1.0 | Session evidence-session; attempt evidence-session:1; order 1 | Exported 2026-10-17T02:00:00.000Z; reviewed 2026-10-17 | Revision of existing attempt; adds pre-key preservation and later key access, no answer changes. Not a new success. feedback-02.md. |
| [retry.json](retry.json); `9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318` | Same course/exam; cooked-stats-mock-a v0.3.1; package 0.4.1; schema 1.0 | Session evidence-session; new retry evidence-session:2; order 2; also preserves attempt 1 history | Exported 2026-10-17T02:00:00.000Z; reviewed 2026-10-17 | Explicit retry after recorded key access. Q4 correct, assisted/exposed context; seven blanks. History overlaps deduplicated; feedback-02.md. |

Reimport check, review 02: before.json SHA-256 remains the existing ledger value; no new attempt/evidence entry. All original export hashes unchanged after review. All snapshots/events have the same timestamp, so infer only structural sequence from reasons/events, not precise elapsed time. Current answers and explanations are unchanged across every snapshot. No identity/history contradictions found.

## Student-reported difficulties
Previously choosing denominators in word problems.

## Open questions
- No item time for P01; do not infer its chronology relative to exports.
- Original Q4 external help is untracked. The before-key snapshot preserves its pre-recorded-key status; complete independence remains unconfirmed. Retry 2 follows key access and is not independent transfer.
- All export/event times coincide; precise answer chronology and elapsed time are unknown. P01 remains undated.
- Original export source links name packet.html; reviewed corresponding supplied source course-packet.md S3.

## Next session
Active course: Fictional intro statistics / Mock Exam A. Latest review: [feedback-02.md](feedback-02.md), supplementing [feedback-01.md](feedback-01.md). Reviewed two worksheet attempt IDs: first correct Q4 preserved before recorded key access, then a post-key retry of the same response. External help remains untracked; Improving retained. Seven other questions remain unattempted, with no weaknesses inferred. Original before/after/retry exports preserved; duplicate snapshots and reimport counted once.

Next activity remains [next-question.md](next-question.md), the clinic reference-population transfer question. Collect an independent fraction and explanation, plus assistance information, before opening its separate solution. It is still unattempted; do not infer success from this import. No teaching-source gap for S3; existing follow-up/key remain valid, and no guide needs revision.
