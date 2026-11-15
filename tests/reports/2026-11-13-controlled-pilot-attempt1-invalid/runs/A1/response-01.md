I’ll check your course materials and use their notation to explain conditional probability.

I couldn’t read `materials/` because local file access was blocked, so I’ll start with a standard explanation.

**Conditional probability means finding a probability after receiving information.** We write \(P(A\mid B)\) for “the probability of \(A\), given that \(B\) occurred.”

The key idea: **restrict attention to outcomes in \(B\), then ask what fraction also belong to \(A\).**

\[
P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0.
\]

Here, \(A\cap B\) means both events occur. Dividing by \(P(B)\) makes \(B\) your new universe of possibilities.

For example, roll a fair six-sided die. Let:

- \(A\): the result is greater than 3.
- \(B\): the result is even.

Once you know \(B\), the possible results are \(\{2,4,6\}\). Two of those three results—4 and 6—satisfy \(A\), so

\[
P(A\mid B)=\frac{2}{3}.
\]

Using the formula gives the same answer:

\[
P(A\mid B)=\frac{P(\{4,6\})}{P(\{2,4,6\})}
=\frac{2/6}{3/6}=\frac23.
\]

Two common exam traps:

- **Order matters:** \(P(A\mid B)\) generally differs from \(P(B\mid A)\). Always identify the event after the bar first.
- **Independence is a special case:** if knowing \(B\) leaves the probability of \(A\) unchanged, then \(P(A\mid B)=P(A)\).

Try this with the same die: **given that the result is greater than 3, what is the probability it is odd?** Start by listing the outcomes still possible.