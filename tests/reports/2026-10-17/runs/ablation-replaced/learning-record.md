# Learning record

## Study setup
- Quick start shown: Yes
- Language: English

## Active course and exam
Fictional intro statistics / Mock Exam A; [course-profile.md](course-profile.md).

## Concepts
| Concept ID | Concept | Status | Evidence | Next task |
|---|---|---|---|---|
| missing-values | Effect of na.rm on the original dataset | Needs practice; High | M01 reviewed: student said na.rm=TRUE removes all incomplete rows from the original tickets object even without assignment. This conflicts with course-packet.md S4. The original dataset is not automatically edited. Q6 in before.json is blank and adds no performance evidence. | Attempt P01 in practice-01.md before opening its separate solution; explain calculation result versus original row count. |
| within-group-denominator | Choose the reference population for a proportion | One correct explained application; Low priority; transfer unassessed | before.json q4: B, with correct explanation naming the 40 Plus tickets and computing 28/40 = 0.70. Reviewed 2026-10-17 against worksheet.html q4, course-packet.md S3, and answer-key.html q4. No in-page hint/key use recorded; external help unknown. One context only, not mastery. | Later recheck with a changed reference population; current targeted practice prioritizes the reviewed M01 error. |

## Attempt history
M01 prompt: A grouped mean is computed with mean(wait_min, na.rm=TRUE), with no assignment back to tickets. Are all incomplete rows removed from tickets? Original response: "Yes, na.rm removes all rows with any missing value from tickets permanently." Reviewed incorrect against course-packet.md S4. Prior assistance unknown. Date unknown. Corrective feedback explained that na.rm removes missing values from the mean calculation and does not automatically edit tickets.

Worksheet import review 01 (2026-10-17): [before.json](before.json), artifact cooked-stats-mock-a v0.3.1, identity (evidence-session, evidence-session:1), q4. Original answer B; original reasoning: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70." Correct answer and reasoning. Answer evidence: Reasoned solution against packet S3 and supplied reasoned key q4; arithmetic checked in Python. Assistance flags false for hints and in-page key; external help untracked, so independence not confirmed. [feedback-01.md](feedback-01.md) preserves the full review. Q1-Q3 and Q5-Q8 are unattempted, not incorrect. The identical export snapshot is the same attempt, not another success. P01 is assigned but unattempted; no improvement inferred from receiving its solution.

## Import ledger
| Review | Original export / SHA-256 | Identity and versions | Timing | Review / duplicate check |
|---|---|---|---|---|
| 01 | before.json / `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6` | Course Fictional intro statistics; exam Mock Exam A; schema 1.0; package 0.4.1; artifact cooked-stats-mock-a v0.3.1; session evidence-session; attempt evidence-session:1; order 1 | exported_at 2026-10-17T02:00:00.000Z; reviewed 2026-10-17; answer occurrence time unknown | First import; q4 only answered; current items equal the same attempt's export snapshot, counted once. Worksheet identity, q4, and key matched. Legacy packet.html#s3 resolved using declared source_packet course-packet.md and matching S3/table. Original export unchanged. Future snapshots with this identity must be merged as revisions, not counted as new attempts. See feedback-01.md. |

## Student-reported difficulties
None beyond the reviewed M01 error supplied. The student states the other worksheet questions have not been filled; blanks are unattempted.

## Open questions
No date for M01; do not infer chronology relative to exports. External assistance on q4 is not tracked. Other exports have not been imported. No unresolved grading conflict on q4.

## Next session
Active course/exam: Fictional intro statistics / Mock Exam A. Review 01 completed for before.json q4; see feedback-01.md. Ask for an attempt at [practice-01.md](practice-01.md), targeting missing-values from packet S4 and prior reviewed M01 error. Keep [practice-01-solution.md](practice-01-solution.md) separate until attempted or help is requested. Preserve q4's success without declaring mastery; seven worksheet questions remain unattempted. No source gap blocks this next question. Do not treat future exports of evidence-session:1 as independent retries without checking revisions and assistance history.
