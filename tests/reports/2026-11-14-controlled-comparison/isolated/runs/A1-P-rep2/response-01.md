I’ll check the course materials for loop tracing examples and use them to explain the process.

**Loop tracing means following a loop one step at a time**, recording the index, values read, and any changes. Your [course notes](materials/notes.md) emphasize following the actual operations rather than guessing from variable names.

For Quiz 4, count **only element-to-element comparisons**. Leave out assignments, index updates, and loop-condition checks.

Take practice Q1: one pass compares adjacent elements in `[4, 1, 7, 3]`.

| Step | Index | Elements compared | Running count |
|---|---:|---|---:|
| 1 | 0 | 4 and 1 | 1 |
| 2 | 1 | 1 and 7 | 2 |
| 3 | 2 | 7 and 3 | 3 |

The answer is **3 element-to-element comparisons**. Comparing two values does not itself change the list; record changes only if the instructions perform them.

For this kind of pass, a list with \(n \ge 1\) elements has **\(n-1\) adjacent pairs**. That formula applies to one complete pass comparing each neighboring pair once.

Try [practice Q2](materials/practice.md): a pass compares each adjacent pair in `[8, 2, 5, 6, 1, 4]`. **How many comparisons occur, and which operations are you counting?**