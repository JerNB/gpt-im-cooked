I’ll check the materials folder so the explanation matches your course’s notation and examples.

The file listing is taking longer than expected. The key idea is that conditioning restricts the outcomes you consider to those consistent with the information you’re given.

**Conditional probability** is the probability of an event \(A\) when you know that another event \(B\) occurred. We write it as \(P(A\mid B)\), read “the probability of \(A\) given \(B\).”

The key idea: **restrict your attention to outcomes in \(B\)**, then ask what fraction also belong to \(A\).

\[
\boxed{P(A\mid B)=\frac{P(A\cap B)}{P(B)}}\qquad\text{when }P(B)>0.
\]

Here, \(A\cap B\) means that **both** events occur.

For example, roll a fair six-sided die. Let:

- \(A\): the result is greater than 3.
- \(B\): the result is even.

Given \(B\), the possible outcomes are \(\{2,4,6\}\). Two of these—4 and 6—are greater than 3, so

\[
P(A\mid B)=\frac{2}{3}.
\]

Using the formula gives the same result:

\[
P(A\mid B)=\frac{P(\{4,6\})}{P(\{2,4,6\})}
=\frac{2/6}{3/6}=\frac23.
\]

Two useful midterm takeaways:

- **Order matters:** \(P(B\mid A)=2/3\) also happens to hold in this example, but conditional probabilities generally differ when reversed.
- **Independence means the information doesn’t change the probability:** if \(A\) and \(B\) are independent, \(P(A\mid B)=P(A)\).

**Try it:** For that same die, what is the probability the result is greater than 3, given that it is odd?

*I couldn’t finish accessing the materials folder, so this is a general explanation rather than one drawn from your course files.*