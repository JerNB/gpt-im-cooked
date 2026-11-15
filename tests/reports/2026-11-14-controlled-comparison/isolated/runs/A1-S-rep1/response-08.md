**Bayes’ rule lets you reverse a conditional probability:** it connects \(P(A\mid B)\) with \(P(B\mid A)\).

Your outline includes it, but the supplied notes say the lecture notes for it haven’t been posted. Here’s the standard rule:

\[
P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}
\]

The reference group still matters: \(P(A\mid B)\) asks about **A among B**.

Using our class example:

- 20 of 50 students play a sport: **40.0% of all students**.
- 8 of 20 sport players play an instrument: **40.0% of sport players**.
- 16 of 50 students play an instrument: **32.0% of all students**.

Suppose we want the percentage of **instrument players who play a sport**. Bayes’ rule gives:

\[
P(\text{sport}\mid\text{instrument})
=\frac{P(\text{instrument}\mid\text{sport})P(\text{sport})}
{P(\text{instrument})}
=\frac{(20/50)(8/20)}{16/50}
=\frac{8}{16}.
\]

So **50.0% of instrument players also play a sport**, exactly as you found earlier.

The calculation has two steps: multiplying finds the share of the whole class who do **both**; dividing by the share who play an instrument changes the reference group to **instrument players**.

Bayes’ rule is especially useful when you’re given the conditional probability in one direction but asked for the other.