**Bayes’ rule lets you reverse a conditional probability:** from “A among B” to “B among A.” The key is changing the reference group.

Using our club example:

- 50 members total.
- 20 seniors.
- 15 volunteers, including 8 seniors.

Among seniors, **40.0% volunteer**, because 8 of the 20 seniors volunteer. But among volunteers, **53.3% are seniors**, because 8 of the 15 volunteers are seniors.

Bayes’ rule connects those two directions:

\[
P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}
\]

Here, let \(A=\text{senior}\) and \(B=\text{volunteer}\):

\[
P(\text{senior}\mid\text{volunteer})
=
\frac{
P(\text{volunteer}\mid\text{senior})\,P(\text{senior})
}{
P(\text{volunteer})
}
\]

In this club, **40.0% of seniors volunteer**, **40.0% of all members are seniors**, and **30.0% of all members volunteer**. Using those percentages as decimal inputs:

\[
\frac{0.40\times0.40}{0.30}\times100\%
=53.3\%
\]

So **53.3% of volunteers are seniors**.

Why does it work? Multiplying \(P(B\mid A)\) by \(P(A)\) gives the probability of being in **both groups**. Dividing by \(P(B)\) then makes **B the reference group**.

Bayes’ rule is especially useful when you know the conditional probability in one direction, but the question asks for the reverse.