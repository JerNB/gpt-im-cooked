I’ll check the course materials for loop-tracing examples, then walk through one step by step.

**Loop tracing means following a loop one step at a time**, recording the index, values read, and any changes. Use the current values at each step—especially if the loop changes the list.

For Quiz 4, your course counts **only element-to-element comparisons**. Don’t count assignments, index updates, or loop-condition checks.

Consider one left-to-right pass comparing adjacent elements in `[6, 2, 9, 4, 7]`, without changing the list:

| Index `i` | Elements compared | Comparison number |
|---|---|---|
| 0 | 6 and 2 | 1 |
| 1 | 2 and 9 | 2 |
| 2 | 9 and 4 | 3 |
| 3 | 4 and 7 | 4 |

We stop at index 3 because index 4 has no next element. So a list of length **n has n − 1 adjacent comparisons** in one complete pass, when n ≥ 1.

A quiz-ready answer would be: “**4 element-to-element comparisons**, counting each adjacent pair once.” This rule applies to this particular loop pattern; other loops may need a different count.

Try **Practice Q1**: a pass compares each adjacent pair in `[4, 1, 7, 3]`. Which pairs are compared, and how many comparisons are there?