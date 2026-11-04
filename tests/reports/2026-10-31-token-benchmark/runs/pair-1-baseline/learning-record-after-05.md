# Learning record

## Study setup
- Quick start shown: Yes
- Preferred review output: English conversation

## Active course and exam
Synthetic statistics mini-course / practice-only. Profile: course-profile.md

## Concepts
| Concept ID / topic ID | Concept | Status | Priority and evidence | Corrective rule | Next task |
|---|---|---|---|---|---|
| C1 | Conditional probability | Improving | Q1 denominator error; Q3 correct guided recheck; Q5 correct explained independent application after general instruction, with no Q5-specific cue in tutor history | Use the conditioned population (S1); Q5 correctly uses 20 remote workers and 5 remote trainees | One further independent explained application in a distinct context, preferably with a different proportion; not yet Demonstrated |
| C2 | Grouped row counts | Needs practice | Q2: answered 2 rows; assumes grouping always returns one row per group | Grouped mutate retains original rows; scalar summary returns one row per nonempty group (S2) | Explain row counts for mutate versus scalar summary with changed group sizes |
| C3 | Inner joins | Needs practice | Q4: answered 3 rows; assumes each right row matches once despite duplicate left key | Count every matching pair; a key with L left rows and R right rows contributes L times R rows (S3) | Explain a fresh join count with duplicate keys and an unmatched key |

## Attempt history
| Date when known | Attempt ID / item locator | Concept ID | Student answer or link | Outcome | Assistance | Answer evidence | Feedback |
|---|---|---|---|---|---|---|---|
| 2026-10-31 | chat-Q1-1 / materials/packet.md S1 Q1 | C1 | 2/10 = 20%. "I used all ten students as the denominator because the question starts with ten students." | Incorrect denominator; correct numerator and conversion | Submitted before tutor feedback; no hints reported. Correct answer revealed in review; no subsequent student correction yet | Instructor key: S1 Q1, 2/8 = 1/4 | The reference group is 8 commuters; 2/8 = 25%. First number mentioned does not determine denominator. |
| 2026-10-31 | chat-Q2-1 / materials/packet.md S2 Q2 | C2 | 2 rows because there are two regions. "I think grouping means the result always has one row per group." | Incorrect; applies scalar-summary row count to grouped mutate | Submitted before Q2 feedback; no hints reported. Answer revealed in review; no subsequent correction yet | Instructor key: S2 Q2, 8 rows; scalar summary would return 2 | Grouping sets where means are calculated; mutate attaches each mean to every original row and retains all 8 rows under S2 assumptions. |
| 2026-10-31 | chat-Q3-1 / materials/packet.md S1 Q3 | C1 | 3/12 = 25%. "We are considering residents, so the denominator is the 12 residents, not all 20 students." Reports working without a question-specific hint. | Correct answer and explicit reference-group reasoning; improvement from Q1 | Student reports no question-specific hint. Earlier Q1 tutor follow-up explicitly cued Q3 residents and denominator choice between 20 students and 12 residents; reviewed as guided recheck, not independent transfer. Q3 key was not previously shown in tutor feedback | Instructor key: S1 Q3, 3/12 = 1/4 | Correct numerator, conditioned denominator, and percent conversion; one guided success does not establish demonstrated proficiency. |
| 2026-10-31 | chat-Q4-1 / materials/packet.md S3 Q4 | C3 | 3 rows. "I thought each right-table row matches once, even though K occurs twice on the left." | Incorrect; overlooks the second matching left row for each right row | Submitted before Q4 feedback; no hints reported. Answer revealed in review; no subsequent correction yet | Instructor key: S3 Q4, 6 rows | Each of 3 right rows matches both left rows; count all pairs, 2 times 3 = 6. |
| 2026-10-31 | chat-Q5-1 / materials/packet.md S1 Q5 | C1 | 5/20 = 25%. "The conditioned population is remote workers, and five of those twenty are trainees." Reports working without a question-specific hint. | Correct answer and explicit conditioned-population reasoning; first reviewed independent success after Q1 difficulty | Independent application following general Q1 teaching; no Q5-specific hint or answer reveal in prior tutor feedback; no additional help reported | Instructor key: S1 Q5, 5/20 = 1/4 | Correct numerator, denominator, and percentage. Retain Improving: Q3 was guided, so two distinct independent explained successes are not yet established. |

## Import ledger
No imports.

## Student-reported difficulties
None recorded.

## Open questions
None recorded.

## Next session
- Current activity: Review packet attempts
- Concepts to revisit: Prioritize C2 grouped mutate versus scalar summary and C3 duplicate-key matching pairs; C1 improving, with one further independent explained application needed
- Next action: Return to C2: 9 observations in 3 nonempty groups, ask output row counts and reasoning for grouped mutate versus scalar summary. C3 transfer remains pending: M occurs 3 times left and 2 right; N only left. C1 Q5 independent application completed correctly; later recheck with a distinct context and different proportion, without a task-specific cue.
