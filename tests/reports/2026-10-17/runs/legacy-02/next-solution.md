# Separate solution

## Blueprint and evidence

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| N1 | Artifact EX1-DPLYR; compatible packet T2, mapping unconfirmed | Choose a pipeline, compare row counts, explain | Packet L2, E1 Q2, K1 Q2 | Recheck observation rows versus groups after a revealed retry | Reasoned solution; manual deduction, no R execution |

Original synthetic practice, not an instructor question or an exam prediction. [Question](next-question.md).

Choose **grouped mutate**. It attaches the team's mean to each session while retaining all **7 rows**. Scalar grouped summarise would return **3 rows**, one for each of teams A, B, and C. Group sizes do not change the mutate row count; grouping alone does not remove sessions.

Manual check: 2 + 1 + 4 = 7 original sessions and three distinct team labels. Apply packet L2 to each operation. No mean values or additional statistical methods are needed. Compare the student's explanation as well as the counts; do not count this task as attempted until a response is supplied. Opening this solution before responding makes a subsequent answer assisted.
