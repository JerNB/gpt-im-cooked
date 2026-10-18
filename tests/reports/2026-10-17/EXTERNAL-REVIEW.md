# External acceptance materials (not executed)

No teacher, TA, or student has participated in this evaluation. Do not fill in
results below with tutor simulations. This packet separates content adjudication
from the later learning experiment.

## Blind content/record review

Give a course-qualified teacher/TA the cases below and the supplied source rules.
Do not give the reviewer our outcome labels, run condition, release name, or
author commentary. Obtain their independent adjudication first. Then provide
anonymized tutor feedback and resulting records as A/B, with order randomized.
A second reviewer adjudicates disagreements before unblinding the conditions.
Keep initial ratings and reasons, not just a consensus score.

Source rules: a within-group proportion uses that group's total; a whole-table
proportion uses the whole-table total. For "among A, what fraction B?", count A
in the denominator and both A and B in the numerator. Sources are the repository's
synthetic course packets, not actual instructor examinations.
For the primary repaired case, grouping alone keeps observation rows; mutate
preserves its current input rows; scalar summarise returns one row per group
(the existing packet L2). Inspect the supplied page's feedback path as well as
its exported labels.

| Case | Complete prompt / evidence | Student's original response |
|---|---|---|
| V1 | Basic tickets: 12 short, 8 long; Plus: 28 short, 12 long. What fraction of Plus tickets had short waits? Explain the population. | 28/40 = 0.70. The denominator is all 40 Plus tickets. |
| V2 | Same prompt and counts as V1. | 70%. The denominator is all 60 tickets, because every proportion uses the full table. |
| V3 | Same prompt and counts as V1. | 7/10. There are 28 short waits among 40 Plus tickets. |
| V4 | Class A: 8 students, 2 commuters; all classes: 20 students. "Find the commuter proportion." Supplied key says 2/20; intended population unspecified. | 2/8, interpreting the question as asking about Class A. |
| V5 | V1 response was exported before opening the key. Export records no page hint/key; outside help is explicitly untracked. One earlier different correct context has student-reported independence. | Same response as V1. |
| V6 | After V5's export, the student opened the key, reset the display and repeated the same question. Earlier snapshots retain V5; exports of attempt 1 repeat the same IDs. | Same response as V1 on the retry. |
| V7 | A prior tutor marked V3 wrong for not using decimal notation. Student requests a recheck against the source rule and original answer. | Original V3 answer remains 7/10 with the same explanation. |
| V8 | Four observations belong to two regions. First grouped-mutate prediction is checked, and the page displays four plus its explanation. Student retries the same item; both exported entries claim independent_transfer and no earlier reveal. | First: 2 because two regions. Retry: 4 because mutate preserves observation rows. Source/export: inputs/legacy-attempt.json and the preserved legacy page. |

For each case, complete:

| Case | Answer correctness | Reasoning correctness | Source/assumption | Assistance before response (known / unknown) | Independent evidence count | Warranted record change | Appropriate next task | Tutor error category / reason |
|---|---|---|---|---|---|---|---|---|
| V1 | | | | | | | | |
| V2 | | | | | | | | |
| V3 | | | | | | | | |
| V4 | | | | | | | | |
| V5 | | | | | | | | |
| V6 | | | | | | | | |
| V7 | | | | | | | | |
| V8 | | | | | | | | |

Record grading errors per adjudicated answer; diagnosis errors per reviewed
explanation; assistance errors per response; duplicate evidence per repeated
identity; propagation errors per concept/next-task decision. Report disagreement
counts and denominators separately. Unresolved source ambiguity is not a student
error. No high composite score can offset an assistance or propagation failure.

## Real-student pilot

Question: with equal source materials and study time, does the full evidence loop
improve later unaided grouped-transformation row-count reasoning compared with ordinary
review of the same packet and worked examples?

1. Recruit consenting students who did not design the project. Use pseudonymous
   IDs. Record prior topic knowledge and relevant concurrent study. Do not use
   synthetic tutors as participants.
2. An independent teacher validates parallel pretest, immediate and delayed forms
   against the same objectives. Balance reading/calculation demands; use new
   contexts and changed reasoning demands, not only new names/numbers. Keep all
   scored forms and their keys unavailable to the teaching tutor. V1-V8 above
   are behavior checks, not validated learner-test forms. The separate
   external/learner-forms.md and external/learner-key.md provide an unseen draft
   candidate pool; they are not yet equivalent or teacher-validated forms.
3. Use a parallel-group random assignment, balancing pretest performance where
   feasible. Both groups receive the same packet, allowed content, and a fixed
   study period (proposed pilot: 20 minutes). The intervention uses the project;
   the comparison uses packet/notes/worked examples. Log actual exposure, help,
   deviations and time in each group. This tests the whole loop; attributing an
   effect specifically to saved records requires a later randomized ablation.
4. Give closed-material, no-tutor immediate testing and a fresh parallel form
   seven days later. Agree on this interval before recruiting. Record intervening
   study and missing follow-ups. Do not treat attrition as zero performance.
5. Blind the teacher/TA grading to condition. Primary outcome: delayed correct
   row-count and unit-of-observation reasoning, using a prespecified partial-credit rubric. Secondary:
   immediate reasoning, numerical accuracy, assistance needed, and time. Record
   satisfaction separately. Set the rubric and minimum meaningful difference
   before outcomes are visible.
6. Report all recruited/completed counts, assignment, deviations, attrition,
   group scores and uncertainty. A small feasibility pilot supports usability
   and variance estimates, not efficacy or broad causal generalization. Plan
   the confirmatory sample size from a meaningful effect and power analysis;
   do not choose it after looking for a favorable result.

Participant data template: pseudonymous ID, condition, material/version hash,
prior knowledge, pretest original answers, actual study time, help/exposure log,
immediate original answers, delayed original answers, concurrent study, missing
follow-up reason, blinded scores, rater identity and disagreement resolution.

Current status: protocol prepared; recruitment, rubric validation, teacher
adjudication, student observations and learning outcomes are all unperformed.
