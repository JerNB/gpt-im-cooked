I’ll read the study skill and your course materials, then use them to explain conditional probability.

Your notes explain conditional probability as “the probability of A among B.” Your outline also requires every answer to name that reference group and give a percentage to one decimal place. I’m using the study skill to keep the explanation and later practice aligned with those rules.

**Hi student, let's get you uncooked.**

That opening is the study skill’s greeting marker. We’ll start with your notes and build toward practice.

**Conditional probability means asking for a share within a particular group.** Your notes read \(P(A\mid B)\) as “the probability of A among B.” The vertical bar means “given”: we know the case belongs to B, so we restrict our attention to B. ([Notes §1.1–1.2](materials/notes.md))

For equally weighted cases and a nonempty group B:

\[
P(A\mid B)=
\frac{\text{number of cases in both A and B}}
{\text{number of cases in B}}.
\]

Here’s a new example applying that rule. Suppose a class has 100 students:

- 40 are commuters.
- 16 of those commuters ride a bike.
- 20 students altogether ride a bike.

What is the probability that a student rides a bike **given that they commute**?

We focus on the **40 commuters**. Of those, 16 ride a bike:

\[
P(\text{bike}\mid\text{commuter})
=\frac{16}{40}\times100\%
=\boxed{40.0\%\text{ of commuters}}.
\]

The denominator is 40 because the question restricts us to commuters. The other students are outside our reference group.

Now reverse the question: what share of **bike riders** are commuters? There are 20 bike riders, and 16 commute:

\[
P(\text{commuter}\mid\text{bike})
=\frac{16}{20}\times100\%
=\boxed{80.0\%\text{ of bike riders}}.
\]

**Reversing the condition changes the reference group**, so it can change the answer. That is the distinction in [Notes §1.3](materials/notes.md).

Your midterm requires percentages rounded to **one decimal place**, with the reference group named in words. ([Outline, reporting rule](materials/outline.md))

A useful cue: **Identify the group after “given,” then count the target cases within it.**

Quick check: if a question asks, “Among students who ride a bike, what percentage commute?”, which group supplies the denominator?

I saved your [study setup](study/stat-110/midterm-1/learning-record.md). Future learning evidence normally saves after five meaningful turns, or sooner when your progress status changes; until then, recent evidence stays in this chat.