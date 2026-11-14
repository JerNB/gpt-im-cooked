I’ll read the study skill and your course materials, then explain conditional probability using your course’s notation and examples.

The local command runner failed before it could open your files. I’m trying one fallback so I can follow the study skill you specified.

I couldn’t open `skill/SKILL.md` because the local command runner failed. Please paste that file so I can follow your study workflow; I haven’t accessed your materials yet.

To get started, **conditional probability means updating a probability when you learn some information.**

We write \(P(A\mid B)\) for “the probability of \(A\), given that \(B\) occurred.” The key idea is to **restrict attention to outcomes in \(B\)**, then ask how much of that group also belongs to \(A\):

\[
\boxed{P(A\mid B)=\frac{P(A\cap B)}{P(B)}}\qquad P(B)>0.
\]

For example, roll a fair six-sided die. Let:

- \(A\): the result is greater than 3.
- \(B\): the result is even.

Once you know \(B\) occurred, the possible results are \(\{2,4,6\}\). Two of those three results are greater than 3, so

\[
P(A\mid B)=\frac{2}{3}.
\]

The formula gives the same answer: \(A\cap B=\{4,6\}\), so \((2/6)/(3/6)=2/3\).

A common exam mistake is reversing the condition. Here, \(P(B\mid A)=2/3\) too, but that equality is coincidental—**\(P(A\mid B)\) and \(P(B\mid A)\) generally differ.** Always identify what is *given* first; that determines your denominator.

Try this: draw one card from a standard 52-card deck. Given that it’s a face card (jack, queen, or king), what’s the probability it’s a king? Explain which cards remain possible after conditioning.