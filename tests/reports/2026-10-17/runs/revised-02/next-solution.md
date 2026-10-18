# Separate solution

**After summarise: 3 rows. After mutate: 3 rows.**

There is one scalar summary for each of the three departments. The later mutate adds a column to those three summary rows and keeps them. It does not restore the original 12 observations.

**Answer evidence: Reasoned solution (unexecuted).** Direct application of [course-packet.md](course-packet.md), L2; checked against K1 Q2's distinction between row-preserving mutate and one-scalar-per-group summarise. This is conceptual row-count reasoning, not a claim of R execution.

| Item | Topic | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| next-01 | T2; provisional content correspondence to EX1-DPLYR | Short pipeline row-count explanation | Packet L2; E1 Q2/K1 Q2; original synthetic practice | Identify the input rows to a later mutate after summarise; recheck correction without this item's solution | Reasoned solution |

This new two-operation context is a next check, not a completed independent success. The course identity mismatch is retained in [course-profile.md](course-profile.md).
