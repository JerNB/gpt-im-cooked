# Learning record

## Study setup
- Quick start shown: Yes
- Language: English

## Active course and exam
Fictional intro statistics / Mock Exam A; [course profile](course-profile.md).

## Concepts
| Concept ID | Concept | Status | Evidence | Next task |
|---|---|---|---|---|
| within-group-denominator | Reference population | Recheck (high priority) | Clinic transfer 01: 3/5 numerically correct but explicitly says all 40 appointments are the denominator because every proportion uses everybody; independence explicitly student-reported. Contradicts earlier correct P01 and pre-key worksheet Q4 explanations; repeats prior whole-table rule. Original successes retained; post-key worksheet retry adds no independent transfer. Basis: packet S3; clinic-attempt-01.md; feedback-04.md. | Explain why all late arrivals (4 morning + 6 afternoon) form the population; any immediate revision is coached. Later use a fresh independent transfer with consistent count/fraction/reasoning. |

Corrective rule retained: name the reference population, then divide the matching count by that population's total (course-packet.md S3). Blank worksheet items supply no assessed evidence about their topics.

## Attempt history
P01 original response: "Six overdue fiction loans out of 15 fiction loans: 6/15; out of all 40 loans: 6/40. The requested population sets the denominator." Reviewed correct; independence is student-reported. Prior wrong original response: "6/40 in both because always use all rows." Corrected in prior feedback. Date unknown.

Reviewed 2026-10-17: [before.json](before.json), session `evidence-session`, attempt `evidence-session:1`, Q4 (within-group-denominator). Original answer `["B"]`; original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct against worksheet.html Q4, answer-key.html Question 4, and course-packet.md S3. Solution evidence: Reasoned solution and Verified computation (Python 3.13.12). Assistance: no in-page hint/key recorded; external help untracked. Actual item answer time unknown. Current items and attempt-history snapshot duplicate the same response and count once. Q1–Q3/Q5–Q8 unattempted. Full review: [feedback-01.md](feedback-01.md).


Review 02, 2026-10-17: before.json reimport is byte-identical and adds no performance evidence. after.json is a revision of `evidence-session:1`, not a new attempt. It preserves Q4's original B and explanation in a `before key access` snapshot, then records key access with the answer unchanged. This supplements review 01's assistance account; its original correct, pre-recorded-key judgment stands, with external help unknown. Later key access does not retroactively mark the preserved original response assisted.

Retry `evidence-session:2` in [retry.json](retry.json), order 2: Q4 original answer `["B"]`; original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct under packet S3 / worksheet Q4 / key Question 4. Assistance: no hint recorded, key flag true carried from the same session, external help untracked. Distinct explicit retry, same question following recorded key access: assisted/exposed-context correct practice, not independent transfer. No evidence of reading a particular answer or copying. Seven other items still unattempted. Answer evidence remains Reasoned solution / Verified computation as in review 01. Full revision review: [feedback-02.md](feedback-02.md).

No response was changed by the tutor; original exports are preserved unchanged. Repeated first-attempt snapshots across all files are deduplicated. Two worksheet attempt IDs cover the same Q4 context; no status promotion from snapshots, re-export, or key access. Equal timestamps prevent exact duration/answer timing claims; the explicit before-key/before-retry history and retry event supply structural order.


Clinic transfer 01, received/reviewed 2026-10-17 (actual response time unknown), source: student message preserved verbatim in [clinic-attempt-01.md](clinic-attempt-01.md); question [next-question.md](next-question.md). Original answer: "3/5." Original reasoning: "My denominator population is all 40 clinic appointments, since every proportion uses everybody." Assistance report: "I used no hints, key or outside help before this response." Independence explicitly student-reported for this new task, not inferred from worksheet activity.

Review: partially correct. Fraction 3/5 equals 6/10, but the reference population is the 10 late arrivals, not all 40 appointments. Six over 40 would equal 3/20 and answer a different question. Clear denominator misconception in the stated rule; route used to obtain 3/5 is unknown. Solution evidence: Reasoned solution from packet S3 / clinic counts; Verified computation using exact fractions in Python 3.13.12. Full feedback: [feedback-04.md](feedback-04.md). New, distinct conversational transfer attempt; not an export revision and no invented worksheet attempt ID. Status changed Improving to Recheck, high priority, because current reasoning contradicts earlier explanations and repeats the documented whole-table rule. Earlier successful responses remain evidence; no Demonstrated claim.

## Import ledger
| Export and SHA-256 | Course / artifact | Attempt identity | Timing | Review |
|---|---|---|---|---|
| [before.json](before.json); `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6` | Fictional intro statistics / Mock Exam A; cooked-stats-mock-a v0.3.1; package 0.4.1; schema 1.0 | Session evidence-session; attempt evidence-session:1; order 1 | Exported 2026-10-17T02:00:00.000Z; snapshot time identical; actual Q4 answer time unknown; reviewed 2026-10-17 | First import; worksheet identity and Q4/key match checked. Q4 correct, assistance partly unknown; seven blanks unattempted. One attempt, no duplicate evidence from history. Original preserved; feedback-01.md. |
| [after.json](after.json); `81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1` | Same course/exam; cooked-stats-mock-a v0.3.1; package 0.4.1; schema 1.0 | Session evidence-session; attempt evidence-session:1; order 1 | Exported 2026-10-17T02:00:00.000Z; reviewed 2026-10-17 | Revision of existing attempt; adds pre-key preservation and later key access, no answer changes. Not a new success. feedback-02.md. |
| [retry.json](retry.json); `9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318` | Same course/exam; cooked-stats-mock-a v0.3.1; package 0.4.1; schema 1.0 | Session evidence-session; new retry evidence-session:2; order 2; also preserves attempt 1 history | Exported 2026-10-17T02:00:00.000Z; reviewed 2026-10-17 | Explicit retry after recorded key access. Q4 correct, assisted/exposed context; seven blanks. History overlaps deduplicated; feedback-02.md. |

Reimport check, review 02: before.json SHA-256 remains the existing ledger value; no new attempt/evidence entry. All original export hashes unchanged after review. All snapshots/events have the same timestamp, so infer only structural sequence from reasons/events, not precise elapsed time. Current answers and explanations are unchanged across every snapshot. No identity/history contradictions found.

## Student-reported difficulties
Previously choosing denominators in word problems. Current clinic attempt adds reviewed evidence of the repeated whole-table rule; keep this distinct from the earlier self-report.

## Open questions
- Clinic fraction is correct but inconsistent with the stated denominator; the student has not explained how 3/5 was obtained. Do not infer guessing.
- No item time for P01; do not infer its chronology relative to exports.
- Original Q4 external help is untracked. The before-key snapshot preserves its pre-recorded-key status; complete independence remains unconfirmed. Retry 2 follows key access and is not independent transfer.
- All export/event times coincide; precise answer chronology and elapsed time are unknown. P01 remains undated.
- Original export source links name packet.html; reviewed corresponding supplied source course-packet.md S3.

## Next session
Active course: Fictional intro statistics / Mock Exam A. Latest review: [feedback-04.md](feedback-04.md), original clinic response [clinic-attempt-01.md](clinic-attempt-01.md). Clinic Follow-up 01 is now attempted: fraction 3/5 correct; all-40 population explanation incorrect; no hints/key/outside help explicitly reported. Status Recheck, high priority, supersedes the earlier Improving pointer without removing prior correct explanations. Seven worksheet items remain unattempted. Worksheet exports and duplicate-import decisions are unchanged.

Next activity: have the student explain why the clinic denominator combines 4 morning and 6 afternoon late arrivals, then assess a fresh independent population-selection transfer later. Any immediate corrected response after this feedback is coached, not a fresh independent success. Ask for a consistent original count, reference-population description, and fraction. Existing clinic question/key remain valid; no new guide or source gap. Historical feedback 01/02 status snapshots are superseded only for current planning, not their correctness judgments.
