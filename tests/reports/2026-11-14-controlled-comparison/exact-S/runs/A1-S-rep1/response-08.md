**Bayes’ rule lets you reverse the direction of a conditional probability:** from \(P(A\mid B)\) to \(P(B\mid A)\).

\[
P(B\mid A)=\frac{P(A\mid B)\,P(B)}{P(A)}
\]

The reference group changes when you reverse the condition, so you can’t simply swap the letters and keep the same answer.

Use our club example:

- **40.0% of members are seniors:** 20 out of 50.
- **40.0% of seniors volunteer:** 8 out of 20.
- **32.0% of members volunteer:** 16 out of 50.

Bayes’ rule gives:

\[
P(\text{senior}\mid\text{volunteer})
=\frac{P(\text{volunteer}\mid\text{senior})\,P(\text{senior})}
{P(\text{volunteer})}
=\frac{(8/20)(20/50)}{16/50}
=\frac{8}{16}.
\]

So **50.0% of volunteers are seniors**, exactly as you calculated earlier.

Here’s why it works: multiplying \(P(A\mid B)\) by \(P(B)\) gives the share of the whole population in **both groups**. Dividing by \(P(A)\) then changes the reference group to \(A\).

Your outline includes Bayes’ rule, but says the lecture notes are still to be posted; this is the standard rule.