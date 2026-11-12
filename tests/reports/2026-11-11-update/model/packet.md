# Synthetic statistics mini-course

## Scope
Only conditional probability, grouped row counts, and duplicate-key inner joins.
This packet supplies all teaching rules. No external packages or sources needed.

## S1: Conditional probability
P(A given B) counts A-and-B outcomes divided by B outcomes. The denominator
is the conditioned population B, not the full sample. Assume equally weighted
observations and positive B counts. A percentage is the fraction times 100.
Q1: There are 10 students, 8 commuters, and 2 commuter cyclists. Find the
fraction of commuters who cycle. Instructor key: 2/8 = 1/4.
Q3: There are 20 students, 12 residents, and 3 resident cyclists. Find the
fraction of residents who cycle. Instructor key: 3/12 = 1/4.
Q5: There are 50 employees, 20 remote workers, and 5 remote trainees. Find
the fraction of remote workers who are trainees. Instructor key: 5/20 = 1/4.

## S2: Grouped transformations
A grouped scalar summary returns one result row per nonempty group. A grouped
mutate-style transformation attaches the group result to every original row and
retains all original rows. Assume no filtering, missing groups, or vector outputs.
Q2: Eight observations belong to two regions. A grouped mutate attaches each
region's mean to its original observations. How many output rows? Instructor
key: 8; a scalar summary of those groups would return 2.

## S3: Duplicate-key inner joins
An inner join returns every matching pair of left and right rows for each key.
If one key occurs L times on the left and R times on the right, that key
contributes L times R output rows. Unmatched rows contribute zero.
Q4: The left table has two rows for key K. The right table has three rows for K.
No other keys exist. How many inner-join output rows? Instructor key: 6.
