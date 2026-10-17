# Learning record

## Study setup
- Quick start shown: Yes
- Language: English

## Active course and exam
Fictional intro statistics / Mock Exam A; [course-profile.md](course-profile.md).

## Concepts
| Concept ID | Concept | Status | Evidence | Next task |
|---|---|---|---|---|
| within-group-denominator | Reference population | Improving | P01: correct explained fiction-loan versus all-loan denominators after an earlier error; explicit no-help self-report. Q4 attempt 1: correct B and explained 28/40, preserved before recorded key opening; external help untracked. after.json is the same attempt revision. Q4 attempt 2: correct repeated response after key exposure (assisted), not independent transfer. P01 plus worksheet Q4 remain two contexts with only P01 explicitly self-reported independent; not Demonstrated. Basis: course-packet.md S3. No new denominator error observed. | transfer-01 in next-question-01.md: select the population when the requested group changes to late arrivals; obtain assistance context with the response. |

## Attempt history
P01 original response: "Six overdue fiction loans out of 15 fiction loans: 6/15; out of all 40 loans: 6/40. The requested population sets the denominator." Reviewed correct; independence is student-reported. Prior wrong original response: "6/40 in both because always use all rows." Corrected in prior feedback. Date unknown.

Q4, session `evidence-session`, attempt `evidence-session:1`, artifact `cooked-stats-mock-a` v0.3.1; [before.json](before.json), top-level q4 and matching attempt-history snapshot. Original answer: `["B"]`. Original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Reviewed 2026-10-17: correct answer and reasoning. Assistance: hint_used false; key_opened_in_page false; external_help untracked, so independent success is not established. Answer evidence: Reasoned solution, course-packet.md S3 / worksheet.html Q4 / answer-key.html Question 4; arithmetic verified in Python 3.13.12. Feedback: [feedback-01.md](feedback-01.md). Q1-q3 and Q5-q8 are unattempted, not errors. No item response time supplied.

Revision review, 2026-10-17: [after.json](after.json) adds the key-opening history to the existing attempt `evidence-session:1`, not a new attempt. Its first two snapshots preserve the original B and explanation before recorded key access; later key access does not retroactively taint that preserved response. The external-help uncertainty remains. The unchanged resubmitted before.json adds no evidence. No earlier correctness judgment is reversed. [feedback-02.md](feedback-02.md) supplements feedback-01.md.

New retry, reviewed 2026-10-17: [retry.json](retry.json), session `evidence-session`, attempt `evidence-session:2`, order 2, same artifact/version and same Q4 context. Original answer: `["B"]`. Original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct, with the same packet S3 / worksheet Q4 / separate-key basis as attempt 1. Assistance: hint_used false, key_opened_in_page true carried across the explicit retry after key opening, external_help untracked. Record as correct assisted repetition after key exposure, not independent transfer or another distinct application context. All other items remain unattempted. The retry's inherited attempt-1 snapshots are not additional attempts. Every supplied event/snapshot has the same timestamp; sequence is supported by history labels/order and exporter behavior, not measured elapsed time.

## Import ledger
- Reviewed 2026-10-17: [before.json](before.json), SHA-256 `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6`; schema 1.0, package 0.4.1, course Fictional intro statistics, exam Mock Exam A, artifact `cooked-stats-mock-a` v0.3.1, identity `(evidence-session, evidence-session:1)`, order 1. Exported at 2026-10-17T02:00:00.000Z. The sole history snapshot matches the top-level responses; counted once. Worksheet metadata and q1-q8 mappings verified; packet.html section aliases resolved to course-packet.md S1-S5; actual Q4 key checked against the worksheet and packet. Only Q4 attempted and reviewed. No prior ledger identity to duplicate; original export unchanged. Feedback saved in feedback-01.md.

- Revision review 2026-10-17: before.json SHA-256 still `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6`; identical import, no new attempt/evidence entry. Original ledger entry retained.
- Reviewed 2026-10-17: [after.json](after.json), SHA-256 `81a325fe5f37ee071c46fe98d43502939c11556539a564a428e206294cec40e1`; schema 1.0, package 0.4.1, artifact `cooked-stats-mock-a` v0.3.1, same course/exam, identity `(evidence-session, evidence-session:1)`, order 1. Exported-at 2026-10-17T02:00:00.000Z. A revision with unchanged answers and new recorded key access. The first snapshot exactly matches the previously reviewed before.json snapshot; its additional before-key snapshot and post-key export do not add successes. Version/item mapping and preserved answer history consistent with worksheet/packet/key already inspected. Feedback: feedback-02.md.
- Reviewed 2026-10-17: [retry.json](retry.json), SHA-256 `9e5cf6d1aea68e29e717dc770d0527c4df53d90dd801984e82164e2ad50da318`; schema 1.0, package 0.4.1, artifact `cooked-stats-mock-a` v0.3.1, same course/exam, identity `(evidence-session, evidence-session:2)`, order 2. Exported-at 2026-10-17T02:00:00.000Z. Its first three history snapshots equal after.json's history; before-retry and attempt-2 export follow. Exactly one distinct retry added; inherited attempt-1 snapshots deduplicated. Q4 correct after key exposure; all other items blank. No identity/history conflict. Feedback: feedback-02.md. All original JSON files retained unchanged.

## Student-reported difficulties
Previously choosing denominators in word problems. Retained as historical difficulty; current reviewed Q4 reasoning is correct.

## Open questions
- No item time for P01; do not infer its chronology relative to exports.
- Q4 attempt 1's external-help history is untracked despite its preserved pre-key response. Attempt 2 is after known key exposure. Obtain assistance context with the next new transfer response; do not infer independence from false in-page flags or from a new attempt ID.
- No performance evidence for Q1-q3 or Q5-q8; blanks do not indicate weaknesses.

## Next session
Active course: Fictional intro statistics / Mock Exam A. Current feedback: [feedback-02.md](feedback-02.md), supplementing [feedback-01.md](feedback-01.md). before.json is unchanged and deduplicated; after.json revises attempt 1's assistance history; retry.json introduces attempt 2 after key exposure. Preserve attempt 1's correct pre-key Q4 answer and attempt 2's correct assisted repetition separately. Status remains Improving, no new error or independent transfer demonstrated. No source gap blocks the current review; all other worksheet questions remain unattempted. P01 chronology and Q4 attempt-1 external help remain unresolved. Next: answer the pending original [transfer-01](next-question-01.md), with assistance context; no answer to it is yet supplied. Its [solution](next-question-01-solution.md) remains separate. If it has already been read, record that assistance when reviewing the response. No new question or guide replaces it in this turn.
