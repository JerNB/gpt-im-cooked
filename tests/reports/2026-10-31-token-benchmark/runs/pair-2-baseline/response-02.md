I’ll check Q2 against the packet’s grouped-transformation rule and save the feedback in your existing learning record.

**Hi student, let's get you uncooked.**

Your answer is incorrect: **Q2 returns 8 rows**. Your reasoning describes a grouped scalar summary, but Q2 specifies a grouped **mutate**.

Grouping determines which observations are used together to calculate each region’s mean. The operation then determines how that result appears:

- A **grouped scalar summary** returns one row per nonempty region: here, **2 rows**.
- A **grouped mutate** attaches the appropriate region’s mean to every original observation: here, **8 rows**.

For example, if five observations belonged to one region and three to the other, mutate would attach the first region’s mean to its five rows and the second region’s mean to its three rows. All eight observations remain.

The corrective rule is: **identify the operation before counting output rows**. These rules assume no filtering, missing groups, or vector outputs.

**Answer evidence: Instructor key — materials/packet.md, S2, Q2.**

Quick check: With 12 observations across three nonempty regions, how many rows would each operation return, and why?

Saved your answer, reasoning, and feedback in [learning-record.md](learning-record.md).