**Bayes’ rule lets you reverse a conditional probability:** from “the probability of \(B\) among \(A\)” to “the probability of \(A\) among \(B\).”

Your outline includes it, though the lecture notes say the Bayes section hasn’t been posted yet.

The rule is:

\[
P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}
\]

Use our club example: 50 members, 20 seniors, and 18 volunteers, including 12 seniors. Suppose we know:

- **60.0% of seniors volunteer:** \(P(V\mid S)\).
- **40.0% of all members are seniors:** \(P(S)\).
- **36.0% of all members volunteer:** \(P(V)\).

To find the percentage **of volunteers who are seniors**, Bayes’ rule gives:

\[
P(S\mid V)
=\frac{P(V\mid S)P(S)}{P(V)}
=\frac{60.0\%\times40.0\%}{36.0\%}
\approx66.7\%
\]

So **66.7% of volunteers are seniors**, matching your count-based answer.

Here’s why it works: multiplying \(P(V\mid S)\) by \(P(S)\) finds the share of **all members who are both seniors and volunteers**. Dividing by \(P(V)\) then changes the reference group to **volunteers**.

The key distinction: **60.0% of seniors volunteer** and **66.7% of volunteers are seniors** answer different questions. Bayes’ rule connects them.