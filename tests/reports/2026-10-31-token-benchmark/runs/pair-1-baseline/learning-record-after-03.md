# Learning record

## Study setup
- Quick start shown: Yes
- Preferred review output: English conversation

## Active course and exam
Synthetic statistics mini-course / practice-only. Profile: course-profile.md

## Concepts
| Concept ID / topic ID | Concept | Status | Priority and evidence | Corrective rule | Next task |
|---|---|---|---|---|---|
| C1 | Conditional probability | Improving | Q1 denominator error; Q3 correct answer and explanation after Q1 teaching and an earlier Q3-specific denominator cue | Use the conditioned population (S1); Q3 correctly uses 12 residents | Recheck in a fresh context without a question-specific cue; not yet demonstrated |
| C2 | Grouped row counts | Needs practice | Q2: answered 2 rows; assumes grouping always returns one row per group | Grouped mutate retains original rows; scalar summary returns one row per nonempty group (S2) | Explain row counts for mutate versus scalar summary with changed group sizes |
| C3 | Inner joins | Unassessed | No attempts | Count matching pairs | Review an attempt |

## Attempt history
| Date when known | Attempt ID / item locator | Concept ID | Student answer or link | Outcome | Assistance | Answer evidence | Feedback |
|---|---|---|---|---|---|---|---|
| 2026-10-31 | chat-Q1-1 / materials/packet.md S1 Q1 | C1 | 2/10 = 20%. "I used all ten students as the denominator because the question starts with ten students." | Incorrect denominator; correct numerator and conversion | Submitted before tutor feedback; no hints reported. Correct answer revealed in review; no subsequent student correction yet | Instructor key: S1 Q1, 2/8 = 1/4 | The reference group is 8 commuters; 2/8 = 25%. First number mentioned does not determine denominator. |
| 2026-10-31 | chat-Q2-1 / materials/packet.md S2 Q2 | C2 | 2 rows because there are two regions. "I think grouping means the result always has one row per group." | Incorrect; applies scalar-summary row count to grouped mutate | Submitted before Q2 feedback; no hints reported. Answer revealed in review; no subsequent correction yet | Instructor key: S2 Q2, 8 rows; scalar summary would return 2 | Grouping sets where means are calculated; mutate attaches each mean to every original row and retains all 8 rows under S2 assumptions. |
| 2026-10-31 | chat-Q3-1 / materials/packet.md S1 Q3 | C1 | 3/12 = 25%. "We are considering residents, so the denominator is the 12 residents, not all 20 students." Reports working without a question-specific hint. | Correct answer and explicit reference-group reasoning; improvement from Q1 | Student reports no question-specific hint. Earlier Q1 tutor follow-up explicitly cued Q3 residents and denominator choice between 20 students and 12 residents; reviewed as guided recheck, not independent transfer. Q3 key was not previously shown in tutor feedback | Instructor key: S1 Q3, 3/12 = 1/4 | Correct numerator, conditioned denominator, and percent conversion; one guided success does not establish demonstrated proficiency. |

## Import ledger
No imports.

## Student-reported difficulties
None recorded.

## Open questions
None recorded.

## Next session
- Current activity: Review packet attempts
- Concepts to revisit: C1 conditioned population / denominator selection; C2 grouped mutate versus scalar summary
- Next action: C1 Q3 reviewed correctly with prior denominator cue; use a fresh uncued context for independent transfer. C2 transfer remains pending: 9 observations in 3 nonempty groups, row counts and reasoning for grouped mutate versus scalar summary.
