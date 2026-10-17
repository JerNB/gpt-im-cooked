# Separate solution — next question

Choose grouped **summarise()**, with one scalar summary per team. It returns **three rows**, one for A, B, and C. Grouped mutate() would keep all **nine original session rows**, so it would not produce the requested one-row-per-team structure.

Evidence: **Reasoned solution**, manually checked using packet L2: scalar grouped summarise returns one row per group, while grouped mutate keeps the original rows. There are three teams and 2 + 3 + 4 = 9 sessions. No R execution was performed or needed to establish this course-level row-count result.

| Item | Topic | Format and basis | Personal target | Verification |
|---|---|---|---|---|
| next-01 | EX1-DPLYR; packet T2 (conceptual alignment only) | Original short answer; packet L2, E1 Q2 | Choose an operation from a desired observation unit and explain the alternative; recheck after a same-item answer reveal | Reasoned solution; unexecuted R |

A correct explained response would add fresh evidence. Merely opening this key is not an attempt or a mastery event.
