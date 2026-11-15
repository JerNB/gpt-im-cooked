I’ll check the materials folder and use your course’s notation and examples to explain conditional probability.

I couldn’t open `materials/` because the local file reader failed, so this explanation uses standard probability notation rather than your course files.

**Conditional probability means updating a probability using information you’re given.** We write

\[
P(A\mid B)
\]

and read it as “the probability of \(A\), given that \(B\) occurred.”

The key idea: **once you know \(B\) happened, restrict your attention to outcomes in \(B\).** Then ask how much of that probability belongs to \(A\) too:

\[
\boxed{P(A\mid B)=\frac{P(A\cap B)}{P(B)}} \qquad P(B)>0.
\]

Here, \(A\cap B\) means “both \(A\) and \(B\).” Dividing by \(P(B)\) makes the total probability within \(B\) equal to 1.

For example, roll a fair six-sided die. Let:

- \(A\): the result is greater than 3.
- \(B\): the result is even.

Given \(B\), the possible results are \(\{2,4,6\}\), all equally likely. Two of those—4 and 6—are greater than 3. Therefore,

\[
P(A\mid B)=\frac{2}{3}.
\]

Using the formula gives the same result:

\[
P(A\mid B)
=\frac{P(\{4,6\})}{P(\{2,4,6\})}
=\frac{2/6}{3/6}
=\frac23.
\]

For your midterm, watch for these distinctions:

- **“Given” versus “and”:** \(P(A\mid B)\) uses \(B\) as the new reference group; \(P(A\cap B)\) measures both events within the original sample space.
- **Order matters:** \(P(A\mid B)\) generally differs from \(P(B\mid A)\), because the reference group changes.
- **Independence:** If knowing \(B\) leaves the probability of \(A\) unchanged, then \(P(A\mid B)=P(A)\).

**Try one:** Draw one card uniformly from a standard 52-card deck. Given that it is a face card (jack, queen, or king), what is the probability it is a king? Explain which cards belong in your denominator.