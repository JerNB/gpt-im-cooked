# Learning record

## Study setup
- Quick start shown: Yes
- Language: English

## Active course and exam
Fictional intro statistics / Mock Exam A; [course-profile.md](course-profile.md).

## Concepts
| Concept ID | Concept | Status | Evidence | Next task |
|---|---|---|---|---|
| within-group-denominator | Reference population | Improving; focused transfer recheck | P01: after an earlier whole-table denominator error, correctly explained 6/15 fiction loans versus 6/40 all loans; explicitly reported no hints, solutions or outside help. Attempt 1 Q4: B with correct population explanation, 28/40 = 0.70, already present in its preserved pre-key snapshot; outside help unknown. after.json is the same attempt after key access, without answer changes. Distinct attempt 2 repeats the correct response after key exposure (assisted). Two contexts including P01; independent transfer is not established. Basis: course-packet.md S3. | N01 in next-question-01.md: choose an outcome-defined population spanning two categories; explain denominator and report assistance. |

## Attempt history
P01 original response: "Six overdue fiction loans out of 15 fiction loans: 6/15; out of all 40 loans: 6/40. The requested population sets the denominator." Reviewed correct; independence is student-reported. Prior wrong original response: "6/40 in both because always use all rows." Corrected in prior feedback. Date unknown.

Before-export review, 2026-10-17: [before.json](before.json), session `evidence-session`, attempt `evidence-session:1`, artifact `cooked-stats-mock-a` version `0.3.1`, Q4. Original answer: `["B"]`. Original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct, including reasoning; Reasoned solution checked against worksheet Q4, packet S3 and supplied reasoned answer key Q4; arithmetic verified with Python. Assistance: hint_used=false; key_opened_in_page=false; external_help="not tracked; tell your tutor". Independence unresolved. Exported at 2026-10-17T02:00:00.000Z; answer-entry time unknown. The identical history snapshot is the same attempt. [Feedback](feedback-01.md).

History review, 2026-10-17: repeated before.json matches its recorded hash and adds no duplicate evidence. after.json is a revision of evidence-session:1: identical original answers/explanations, newly recorded key access, and a matching before-key-access snapshot preserving the correct pre-key Q4 response. Later key access does not retroactively invalidate that snapshot; outside help remains unknown. retry.json contains evidence-session:2 (order 2), a distinct explicit retry after key access, retaining key_opened_in_page=true. Attempt 2 original Q4 answer: `["B"]`. Original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct after key exposure; assisted repetition on the same item, not independent transfer. No new contexts or errors. Evidence: Reasoned solution, same worksheet Q4 / packet S3 / key Q4 basis. [Feedback 02](feedback-02.md) supplements assistance/history in feedback-01.md without changing correctness or creating an extra attempt from snapshots.

Questions 1, 2, 3, 5, 6, 7 and 8 remain blank/unattempted in both worksheet attempts, consistent with the student's request; no weakness inferred. N01 is assigned, not attempted or counted as learning evidence.

## Import ledger
| Source and SHA-256 | Identity/version | Revision and review |
|---|---|---|
| before.json; `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6` | Course Fictional intro statistics / Mock Exam A; schema 1.0; package 0.4.1; artifact cooked-stats-mock-a v0.3.1; session evidence-session; attempt evidence-session:1; order 1 | Reviewed 2026-10-17. Initial import. Exported 2026-10-17T02:00:00.000Z. Current items and export history snapshot match; one attempt, one Q4 success. Worksheet metadata/item mapping verified. Original export preserved. Feedback in feedback-01.md. Reimported 2026-10-17 with identical hash; no added attempt or duplicate concept evidence. |

| after.json; `81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1` | Same course/artifact/schema/package/session as before.json; attempt evidence-session:1; order 1 | Reviewed 2026-10-17. Revision: unchanged responses, added key_opened event and preserved pre-key snapshot. Current key flag true; original pre-key Q4 retained. No extra success or new attempt. feedback-02.md. |
| retry.json; `9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318` | Same course/artifact/schema/package/session; attempt evidence-session:2; order 2 | Reviewed 2026-10-17. New explicit retry after key access; correct Q4 is assisted repetition, not independent transfer. Prior attempt snapshots match after.json; no duplicate counting. feedback-02.md. |

Export source locator packet.html#s3 maps to the supplied course-packet.md S3 through the worksheet's matching S3/table. No packet.html content was assumed. No correctness judgment is superseded. feedback-02.md supplements the earlier assistance account with explicit key access and retry history; preserves the first pre-key answer and its unknown outside-help status. Original JSON files remain unchanged.

## Student-reported difficulties
Previously choosing denominators in word problems. Retain this history alongside current improvement; blanks create no new difficulty entries.

## Open questions
No item time for P01; do not infer its chronology relative to exports. All three exports and their events/snapshots share 2026-10-17T02:00:00.000Z: sequence is supported by snapshot reasons, ordered events, explicit attempt orders and worksheet behavior, not elapsed-time claims. Outside help for attempt 1 Q4 is untracked; its pre-key snapshot supports no recorded in-page assistance but does not establish full independence. Attempt 2 follows key exposure. Other topics remain unassessed by these exports.

## Next session
Active course: Fictional intro statistics / Mock Exam A. Review the student's response to [N01](next-question-01.md), including its denominator explanation and assistance history, against the separate [solution](next-solution-01.md). This targets an outcome-defined population after category-defined successes. Current reviewed sources: before.json, after.json and retry.json; Q4 feedback in feedback-01.md and feedback-02.md. Preserve the two explicit attempt identities; before/after and repeated snapshots of evidence-session:1 are revisions, while evidence-session:2 is an assisted retry. No new independent transfer evidence from this turn. N01 remains pending; avoid upgrading status from repeated Q4 success. No teaching-source gap for this task; external-help uncertainty remains. Pending worksheet questions stay unattempted.
