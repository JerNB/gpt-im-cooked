**Hi student, let's get you uncooked.**

Your answer is **incorrect for Q2: the output has 8 rows**. Your reasoning describes a grouped scalar **summary**, but Q2 specifies a grouped **mutate-style transformation**.

Grouping identifies which observations belong together. The operation performed within those groups determines the output’s row count:

- A **scalar summary** returns one row per nonempty group: here, **2 rows**.
- A **mutate-style transformation** attaches each region’s mean to every original observation: here, **8 rows** remain.

For example, if five observations belong to one region and three to the other, all five receive their region’s mean, and all three receive theirs. No observations are collapsed.

**Instructor key:** [materials/packet.md](materials/packet.md), S2, Q2 confirms 8 rows.

The corrective rule is: **check the operation after grouping—summary reduces to group rows; mutate retains original rows.**

Quick check: if those eight observations belonged to four regions, how many rows would the grouped mutate return, and why?