**Hi student, let's get you uncooked.**

Your answer of **3 rows is incorrect**. Each right-table row matches **both** left-table rows with key K, so each contributes two output rows.

The packet’s rule is that an inner join returns **every matching pair**. For a key appearing \(L\) times on the left and \(R\) times on the right, its contribution is \(L\times R\). Here:

\[
2\times3=\boxed{6\text{ output rows}}.
\]

To see the pairs, label the left rows L1 and L2 and the right rows R1, R2, and R3. L1 matches all three right rows; L2 also matches all three. That gives three pairs plus three pairs.

Your first error was assuming each right row could match only once. **Count matching pairs, rather than counting each input row once.** This follows [packet S3, Q4](materials/packet.md).

**Answer evidence: Instructor key**, which gives 6.

Quick check: With four left rows and three right rows, all carrying K, how many matching pairs would there be?

*Pending evidence (4/5 turns; unsaved): Q4—3 rows from assuming each right row matches once; C3 needs practice. Earlier evidence remains pending.*