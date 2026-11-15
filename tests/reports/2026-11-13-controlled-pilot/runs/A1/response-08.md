**Bayes’ rule lets you reverse the direction of a conditional probability.** Your outline includes it, although the supplied notes say the lecture notes for it are still to be posted.

In your last question, you found:

> **40.0% of students with a part-time job take evening classes.**

Bayes’ rule helps answer the reverse question:

> **What percentage of students who take evening classes have a part-time job?**

These questions use different reference groups, so their answers can differ.

The rule is:

\[
P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}
\]

Here, \(P(A)\) and \(P(B)\) describe each group’s share of the whole population. The denominator \(P(B)\) makes **B the reference group**.

Let’s extend our earlier example with some **invented extra information**:

- There are 100 students altogether.
- 30 have a part-time job.
- 12 of those students take evening classes.
- 20 students altogether take evening classes.

To reverse the conditional, focus on the **20 evening-class students**. Of them, 12 have a part-time job:

\[
12\div20\times100=60.0\%
\]

So **60.0% of evening-class students have a part-time job.**

Bayes’ rule produces the same answer: multiply the share taking evening classes **among job holders** by the share of **all students who have jobs**, then divide by the share of **all students taking evening classes**. That first multiplication identifies the overlap; the division changes the reference group.

**Key takeaway:** you cannot simply swap the words around and keep the same percentage. To reverse a conditional probability, you need information about the sizes of the groups.