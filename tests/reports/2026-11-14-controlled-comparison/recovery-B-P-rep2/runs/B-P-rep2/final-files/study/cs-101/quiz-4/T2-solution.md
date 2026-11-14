# T2: State-changing adjacent-pair pass — separate solution

Original synthetic practice. Basis: materials/notes.md §2.1–2.3 and materials/outline.md Reporting rule. Target: P2-state (unassessed), with a P2-count recheck. Changed demand: later comparisons read the list after earlier swaps.

Question: Start with [5, 2, 4, 1]. Visit index pairs (0,1), (1,2), (2,3), in that order, exactly once. At each pair, compare the current left and right elements using left > right. If true, swap those two elements before advancing. Otherwise leave them unchanged. Continue through all three pairs. Give the list after each pair and the number and type of operations counted under the course reporting rule.

Answer evidence: Reasoned solution, manually checked, unexecuted.

1. Compare 5 > 2: true; swap → [2, 5, 4, 1].
2. Compare 5 > 4: true; swap → [2, 4, 5, 1].
3. Compare 5 > 1: true; swap → [2, 4, 1, 5].

Three element-to-element comparisons. Swaps/assignments, index updates, and loop-condition checks are excluded from the reported count. The question explicitly supplies the swap and traversal behavior; it does not require unsupported sorting theory.

No student attempt yet. Keep solution separate until an attempt or explicit request for help.
