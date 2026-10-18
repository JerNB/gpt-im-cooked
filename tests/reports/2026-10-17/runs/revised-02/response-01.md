**Hi student, let's get you uncooked.**

Your first answer, **2 rows**, confused `mutate()` with `summarise()`. Grouping alone does not remove rows: `mutate()` keeps its input rows, so the four state observations remain (course packet L2).

Your retry, **4 rows**, gives the correct explanation. The page displayed the answer after your first submission, so I recorded this as **improving after feedback**, with an independent check still needed. The export's “independent” label misses that exposure.

Saved: [feedback](feedback.md), [learning record](learning-record.md), and [course profile](course-profile.md). The feedback also documents the differing course labels and the page's column-name mismatch; the conceptual result above does not claim successful R execution.

**Next question:** A 12-row table contains three departments. You group by department, `summarise()` one mean per department, then `mutate()` to add a computed column. How many rows remain after each operation, and why?

[Question file](next-question.md) · [Separate solution—open after trying](next-solution.md)
