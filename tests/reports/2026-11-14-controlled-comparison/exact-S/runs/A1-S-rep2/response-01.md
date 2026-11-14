I’ll check the materials folder so the explanation matches your course’s notation and examples.

Conditional probability means updating a probability when you learn that some event has occurred. The key is to count only outcomes consistent with that information.

**Conditional probability is the probability of an event \(A\), given that another event \(B\) has occurred.** We write it \(P(A\mid B)\), read “the probability of \(A\) given \(B\).”

The key idea: **restrict the possible outcomes to \(B\)**, then determine which of those also belong to \(A\).

For example, roll a fair six-sided die. Let:

- \(A\): the roll is greater than 3, so \(A=\{4,5,6\}\).
- \(B\): the roll is even, so \(B=\{2,4,6\}\).

Once you know the roll is even, only \(2,4,6\) remain possible. Two of those three outcomes are greater than 3, so
\[
P(A\mid B)=\frac{2}{3}.
\]

In general,
\[
\boxed{P(A\mid B)=\frac{P(A\cap B)}{P(B)}}\qquad\text{when }P(B)>0.
\]
Here, \(A\cap B\) means “both \(A\) and \(B\) occur.” Dividing by \(P(B)\) makes \(B\) your new total.

Two common midterm pitfalls:

- **Reversing the condition:** \(P(B\mid A)\) is generally different. In our example, it happens to also equal \(2/3\), but that is a coincidence.
- **Assuming independence:** \(P(A\mid B)=P(A)\) only when learning \(B\) does not change the probability of \(A\).

**Try this:** Given that a fair die roll is greater than 3, what is the probability it is a 6? Start by listing the outcomes that remain possible.

*The local file check stalled, so I haven’t yet verified this against your course materials.*