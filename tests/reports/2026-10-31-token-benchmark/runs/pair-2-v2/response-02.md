**Hi student, let's get you uncooked.**

Your answer of **2 rows is incorrect for Q2**. You correctly identified two groups, but grouping alone does not determine the number of output rows—the operation applied to those groups matters.

Q2 uses a **grouped mutate-style transformation**. It calculates each region’s mean and attaches that mean to every original observation in that region. All eight observations remain, so the answer is **8 output rows**. Observations in the same region receive the same regional mean.

Your reasoning would apply to a **grouped scalar summary**, which produces one result row per nonempty group: two regions would give **2 rows**. These rules and the answer appear in [packet S2, Q2](materials/packet.md).

The corrective rule is: **grouping defines which observations belong together; summary versus mutate determines whether rows collapse or remain.**

**Answer evidence: Instructor key.**

Quick check: If the eight observations belonged to three regions, how many rows would grouped mutate return, and why?

*Pending evidence (2/5 turns; unsaved): Q2—“2 rows” because grouping always gives one row per group; distinguish summary from mutate. Q1 evidence remains pending.*