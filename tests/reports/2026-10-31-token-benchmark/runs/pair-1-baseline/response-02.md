**Hi student, let's get you uncooked.**

I’ll use the frozen study skill to check Q2 against the packet and update your learning record.

**Hi student, let's get you uncooked.**

Q2’s answer is **8 rows**. Your answer of two rows would fit a **grouped scalar summary**, but this question specifies a **grouped mutate**. This matches the **Instructor key** in [packet.md, S2, Q2](materials/packet.md).

The first error is assuming that grouping always determines the output row count. Grouping determines which observations are used together to calculate each region’s mean. The operation then determines how that mean appears in the output:

- **Scalar summary:** produces one result row per nonempty region, giving two rows.
- **Mutate:** attaches each region’s mean to every original observation in that region, keeping all eight rows.

There are two regional means, but each mean can appear on several observation rows. Under S2’s assumptions, including no filtering, adding those means does not remove observations.

Remember: **grouping defines the calculation groups; mutate retains the original rows.**

Quick check: with nine observations in three nonempty groups, how many rows would grouped mutate and scalar summary each return, and why?

Saved your answer and reasoning in [learning-record.md](learning-record.md).