# Separate solution

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| Delivery pipeline | EX1-DPLYR; packet comparison T2 | Short row-count explanation plus unit of observation | Packet L2 and E1 Q2 | Distinguish observation rows from group rows in a sequence after an assisted correction | Reasoned solution; manual trace; R unexecuted |

After grouped **mutate: 7 rows**. Each row still represents a delivery observation; its depot's count is attached to it. Grouping alone does not remove rows.

After grouped **summarise: 3 rows**. Each row represents one depot, with one scalar summary for that depot.

Manual check: start with seven observations; mutate preserves seven; there are still three distinct depots, so a scalar summary per depot produces three rows. This deduction uses [course-packet.md](course-packet.md), L2, and agrees with Instructor key K1 Q2's analogous 20-row/two-group example. No R code was run. Both counts and the change in what a row represents are needed for a complete explanation.

This is original synthetic practice, not an instructor question or an exam prediction. It changes the reasoning demand to a two-operation sequence and the output's unit of observation. Opening this file before responding counts as solution exposure; merely receiving the question supplies no new learning evidence.
