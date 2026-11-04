**Hi student, let's get you uncooked.**

Your answer is **incorrect: Q4 produces 6 rows**. The first error is assuming that each right-table row matches only once. Under the packet’s inner-join rule, **every matching pair of left and right rows produces an output row**.

Label the two left rows L1 and L2, and the three right rows R1, R2, and R3. All have key K, so the matching pairs are:

- L1 with R1, R2, and R3: **3 pairs**.
- L2 with R1, R2, and R3: **3 more pairs**.

That gives \(2\times3=\mathbf{6}\) output rows.

**Instructor key:** [materials/packet.md](materials/packet.md), S3, Q4 confirms 6. S3 states that a key appearing \(L\) times on the left and \(R\) times on the right contributes \(L\times R\) rows.

The corrective rule is: **count matching pairs for each key**.

Quick check: if the left table had three K rows and the right still had three, how many matching pairs would there be?