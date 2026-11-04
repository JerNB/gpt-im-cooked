**Hi student, let's get you uncooked.**

I’ll check Q4 against the packet’s join rule and save the feedback in your learning record.

**Hi student, let's get you uncooked.**

Q4’s answer is **6 rows**. Your reasoning misses that each right-table row matches **both** left-table rows carrying K. An inner join returns every matching pair, as stated in [packet.md, S3](materials/packet.md).

Label the left rows L1 and L2, and the right rows R1, R2, and R3. The matches are:

- L1 with R1, R2, and R3: three output rows.
- L2 with R1, R2, and R3: three more output rows.

That gives \(2 \times 3 = 6\), agreeing with the **Instructor key: S3, Q4**.

Your count of three accounts for only one left-row match per right row. Matching a row once does not prevent it from forming another valid pair. The useful rule is: **for each key, multiply its left-row count by its right-row count; unmatched keys contribute zero.**

Quick check: if M occurs three times on the left and twice on the right, while N occurs only on the left, how many output rows result, and why?

Saved your answer and reasoning in [learning-record.md](learning-record.md).