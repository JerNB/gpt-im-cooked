# Loop tracing transfer check: solution

Original synthetic question based on materials/notes.md sections 2.1-2.3 and materials/outline.md Reporting rule. Changes reasoning demand from one-pass length counting to repeated passes with state changes.

Answer evidence: Verified computation using the controlled Python snippet; instrumentation counts each evaluation of a[i] > a[i + 1]. No instructor key for this original question.

Initial list: [3, 1, 2]. Two complete adjacent-pair passes. Each pass has 2 element-to-element comparisons, even when no swap occurs. Final list: [1, 2, 3]. Total: 4 element-to-element comparisons.

Trace (pass_number, i, left value, right value, list afterward):
(0, 0, 3, 1, [1, 3, 2])
(0, 1, 3, 2, [1, 2, 3])
(1, 0, 1, 2, [1, 2, 3])
(1, 1, 2, 3, [1, 2, 3])

Count only a[i] > a[i + 1]. Exclude assignments (including swaps), index updates, and loop-condition checks. len(a)-1 and range expressions are not element-to-element comparisons. A false comparison still counts.

Personal target: distinguish element comparisons from swaps, account for repeated passes, and carry updated list values into the next comparison. No student response yet.
