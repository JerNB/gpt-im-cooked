# Learning record

## Study setup
- Quick start shown: Yes
- Preferred review output: English conversation

## Active course and exam
Synthetic statistics mini-course / practice-only. Profile: course-profile.md

## Concepts
| Concept ID / topic ID | Concept | Status | Priority and evidence | Corrective rule | Next task |
|---|---|---|---|---|---|
| C1 | Conditional probability | Improving | Q1 denominator error; Q3 correctly uses 12 residents and explains why, without a question-specific hint (student report), after Q1 feedback. One correct new application; lower priority than C2 | Use the conditioned population (S1); Q3 correctly applies this rule | Recheck in a context requiring a changed reasoning demand, such as adding nonresidents |
| C2 | Grouped row counts | Needs practice | Q2: answered 2 rows; believes grouping always gives one row per group | S2: grouped mutate retains original rows; scalar summary returns one row per nonempty group | Contrast mutate and scalar summary on a changed row/group count |
| C3 | Inner joins | Unassessed | No attempts | Count matching pairs | Review an attempt |

## Attempt history
| Date when known | Attempt ID / item locator | Concept ID | Student answer or link | Outcome | Assistance | Answer evidence | Feedback |
|---|---|---|---|---|---|---|---|
| 2026-10-31 | Q1-attempt-1 / materials/packet.md, S1 Q1 | C1 | "2/10 = 20%." Reason: "I used all ten students as the denominator because the question starts with ten students." | Incorrect denominator; arithmetic correct | Submitted before tutor feedback; other assistance unspecified | Instructor key: S1 Q1, 2/8 = 1/4 | Use the 8 commuters: 1/4 = 25%. 2/10 counts commuter cyclists among all students. |
| 2026-10-31 | Q2-attempt-1 / materials/packet.md, S2 Q2 | C2 | "2 rows because there are two regions." Reason: "I think grouping means the result always has one row per group." | Incorrect; conflates grouped mutate with scalar summary | Submitted before Q2 tutor feedback; other assistance unspecified | Instructor key: S2 Q2, 8 rows | Grouped mutate attaches each region mean to every original observation, retaining 8 rows. A grouped scalar summary would return 2. |
| 2026-10-31 | Q3-attempt-1 / materials/packet.md, S1 Q3 | C1 | "3/12 = 25%." Reason: "We are considering residents, so the denominator is the 12 residents, not all 20 students." | Correct answer and explanation; improvement after Q1 error | Student reports no question-specific hint; prior Q1 explanation received; independent new application as reported | Instructor key: S1 Q3, 3/12 = 1/4 | Correctly selects the conditioned population and converts to 25%; one success supports Improving, not Demonstrated. |

## Import ledger
No imports.

## Student-reported difficulties
None recorded.

## Open questions
None recorded.

## Next session
- Current activity: Review packet attempts
- Concepts to revisit: C2 grouped mutate versus scalar summary (priority); C1 improving, recheck with a changed reasoning demand
- Next action: Compare output row counts for grouped mutate and scalar summary on 12 observations in 3 nonempty regions, with reasons (S2-based transfer). C1 Q3 is correct with reasoning; a later transfer check about adding nonresidents remains useful. Prior follow-ups are unanswered, not errors.
