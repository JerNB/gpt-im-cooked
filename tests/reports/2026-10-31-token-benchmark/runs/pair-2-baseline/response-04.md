I’ll check Q4 against S3’s matching-pair rule and record the feedback in your existing learning record.

**Hi student, let's get you uncooked.**

Your answer is incorrect: **Q4 produces 6 rows**. The first error is assuming each right-table row can match only once. Under S3’s rule, an inner join returns **every matching pair** of left and right rows.

Label the two left rows L1 and L2, and the three right rows R1, R2, and R3. All have key K:

- L1 matches R1, R2, and R3: three output rows.
- L2 also matches R1, R2, and R3: three more output rows.

That gives \(2\times3=6\) rows. Equivalently, each right-table row matches **both** left-table rows, so each contributes two output rows.

Your answer of three would fit a table with only one left K row. The second left K row creates another three matching pairs.

**Answer evidence: Instructor key — materials/packet.md, S3, Q4.**

Quick check: If we added a right-table row with key J, but no left row had J, would the output count change? Why?

Saved your answer, reasoning, and feedback in [learning-record.md](learning-record.md).