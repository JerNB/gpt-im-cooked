# Unseen learner item candidates -- not yet validated parallel forms

These items and their separate key were not supplied to any tutoring agent.
They target the primary grouped-transformation concept. A teacher must review
scope, ambiguity and difficulty, then select/equate and freeze forms before
recruitment. The labels below are proposed administrations, not measured
difficulty or established equivalent tests. Do not use the unequal draft forms
to claim a learning effect without that review.

Learner instructions: use the supplied course model. Grouping alone keeps rows;
mutate adds a computed column while retaining current input rows; summarise with
one scalar per group returns one row per group. Explain what a row represents,
as well as giving its count. Work without notes, tutor, hints or solutions.

## Candidate pretest pool A

A1. Twelve clinic visits belong to four clinics. A grouped mutate attaches each
clinic's mean wait to every visit. How many output rows are there? What does one
row represent, and why does four clinics not force four output rows?

A2. A report needs one mean wait per clinic, then a computed label on each clinic
summary. Starting with the same twelve visits/four clinics, choose mutate or
scalar summarise for each of the two steps. Give the row count after each step.

A3. A colleague says "Once a six-row table is grouped into two groups, every
subsequent grouped computation must have two rows." Give a source-supported
counterexample and explain the incorrect assumption.

## Candidate immediate-test pool B

B1. Nine observations belong to three regions. An output still contains all nine
original observations, with a region mean attached. Which of grouped mutate or
one-scalar-per-region summarise matches this output under the supplied model?
Explain the observation represented by each output row.

B2. A five-row table has two teams. A scalar summarise produces one row per team.
A mutate then adds a computed column to that result. Give both intermediate row
counts. Why does the last mutate not restore five original observations?

B3. Starting separately from the same ten-row/two-group table, pipeline X uses
grouped mutate and pipeline Y uses one-scalar-per-group summarise. Compare the
counts and meanings of their output rows. Identify the step that changes the
observation unit.

## Candidate seven-day test pool C

C1. Three observations each have a different group label. Both grouped mutate
and scalar summarise return three rows. Can row count alone identify the
operation in this special case? Explain why and what information you would
inspect instead.

C2. Twenty-four deliveries belong to six depots. The pipeline applies grouped
mutate, then a scalar summarise per depot, then another mutate. Give all three
row counts and explain which input table controls the final count.

C3. The requested output must preserve every original state observation while
adding its region's mean. A proposed pipeline instead returns one scalar summary
per region. Explain the mismatch and choose a correction using the supplied
operations. Do not merely report a number.

Record per item: pseudonymous ID, form/item, original answer/reasoning, start/end
time if observed, permitted assistance deviations, blinded rater, provisional
score, and adjudicated score/reason. Blanks remain unattempted; do not diagnose
a misconception from a blank alone.
