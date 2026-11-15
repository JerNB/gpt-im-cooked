I’ll read the study skill and your course materials, then use those to explain conditional probability.

I couldn’t read `skill/SKILL.md` or your materials because the environment blocked local file access. Paste the skill and its references here so I can follow your course’s study workflow.

For now, **conditional probability means finding a probability after learning some information.**

Write \(P(A\mid B)\) as “the probability of \(A\), given that \(B\) occurred.” Learning \(B\) restricts the possible outcomes to those inside \(B\). We ask what fraction of that remaining probability also belongs to \(A\):

\[
P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0.
\]

For example, roll a fair six-sided die. Let \(A\) mean “the result is greater than 3,” and \(B\) mean “the result is even.”

Given \(B\), only **2, 4, and 6** remain possible. Two of those three outcomes exceed 3, so

\[
P(A\mid B)=\frac{2}{3}.
\]

Using the formula gives the same result: \(P(A\cap B)=2/6\) and \(P(B)=3/6\), so \((2/6)/(3/6)=2/3\).

The key habit: **identify the “given” event first—it determines your denominator.** Also, \(P(A\mid B)\) generally differs from \(P(B\mid A)\).

Try this: given that the die result is greater than 3, what is the probability it is **odd**? Which outcomes remain possible?