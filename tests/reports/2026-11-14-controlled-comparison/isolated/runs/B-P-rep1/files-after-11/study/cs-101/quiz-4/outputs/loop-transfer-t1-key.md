# Loop tracing transfer check T1 - separate solution

Original synthetic practice; CS 101 Quiz 4, P2.
Scope/style basis: materials/notes.md sections 2.1-2.3; materials/outline.md Reporting rule; materials/practice.md Q1-Q4 comparison-count format.
Personal target: distinguish complete adjacent-pair passes from a deliberately shortened pass; trace changed values. Prior Q3/Q4 successes used the same full-pass counting structure.

Question: Start with [6, 2, 5, 1]. Compare positions 0 and 1, swapping if the left value is larger. Then compare positions 1 and 2 in the updated list, swapping if the left value is larger. Stop immediately. Positions start at 0. Give the list after each step and the runtime comparison count under the course convention; state which operations you counted.

Solution: First compare 6 with 2; swap gives [2, 6, 5, 1]. Next compare current values 6 with 5; swap gives [2, 5, 6, 1]. Stop. Count 2 element-to-element comparisons. Assignments, index updates, and loop-condition checks do not contribute. The n-1 count for a complete adjacent-pair pass does not apply because the final adjacent pair is never compared.

Answer evidence: Verified computation using a controlled Python synthetic snippet, with explicit comparison counter and asserted final list/count; manual trace agrees. No instructor key for this original question.
Assistance at delivery: Independent transfer prompt; no solution/hint included in student-facing question. Earlier teaching and Q1-Q4 feedback already exposed. No student attempt yet.
