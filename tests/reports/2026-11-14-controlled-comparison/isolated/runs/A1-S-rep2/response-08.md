I’ll check the course files for Bayes’ rule notes or examples.

**Bayes’ rule lets you reverse a conditional probability:** use \(P(B\mid A)\) to find \(P(A\mid B)\).

Your outline lists it, but the course files don’t yet include Bayes’ rule notes. Here’s the standard explanation, building on the reference-group idea you’ve mastered.

\[
\boxed{P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}}
\]

The reference group for the answer is still **B**, the group after the bar.

For example, suppose a club has 100 members:

- 40 are seniors and 60 are non-seniors.
- **50.0% of seniors volunteer**, so 20 seniors volunteer.
- **25.0% of non-seniors volunteer**, so 15 non-seniors volunteer.

We know the percentage of **seniors who volunteer**. Now reverse the question: **What percentage of volunteers are seniors?**

There are \(20+15=35\) volunteers, including 20 seniors. Therefore:

\[
\frac{20}{35}\times100\% = 57.1\%
\]

**57.1% of volunteers are seniors.**

Bayes’ rule performs that same calculation using probabilities. With \(S=\text{senior}\) and \(V=\text{volunteer}\):

\[
P(S\mid V)=\frac{P(V\mid S)\,P(S)}{P(V)}
\]

The numerator gives the probability of being **both a senior and a volunteer**. Dividing by the probability of volunteering restricts the reference group to **all volunteers**.

The key lesson: **knowing the percentage of seniors who volunteer does not directly tell you the percentage of volunteers who are seniors.** You also need to account for the sizes of the groups and volunteers from the other group.