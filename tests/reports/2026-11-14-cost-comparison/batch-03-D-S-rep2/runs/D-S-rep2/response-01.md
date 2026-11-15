I’ll read the study skill and course materials, then use them to explain conditional probability.

**Hi student, let's get you uncooked.**

I’m using your study skill and course notes. That opening line is the skill’s study-session marker; we’ll start with explanations and use your answers to guide later practice.

**Conditional probability means finding a probability within a particular group.** Your notes read \(P(A\mid B)\) as “the probability of A among B.” The vertical bar means we restrict attention to group B. [Notes §1.1](materials/notes.md)

For example, suppose a class has 30 students:

- 10 are commuters.
- Of those 10 commuters, 6 have jobs.

Let A mean “has a job” and B mean “is a commuter.” To find \(P(A\mid B)\), ask: **Among commuters, what share have jobs?**

\[
P(A\mid B)
=\frac{\text{number in both A and B}}{\text{number in B}}
=\frac{6}{10}
\]

Report the answer as **60.0% of commuters have jobs**.

The denominator is 10 because the question restricts us to commuters. The other students are outside that reference group. Your notes assume equally weighted cases and a nonempty reference group. [Notes §§1.2–1.4](materials/notes.md)

**Reversing the order changes the question.** Suppose 15 students in the class have jobs. Then \(P(B\mid A)\) asks: among students with jobs, what share commute? The same 6 students belong to both groups, but now we divide by 15: **40.0% of students with jobs are commuters**. [Notes §1.3](materials/notes.md)

Remember: **Choose the reference group first; count the target cases inside it second.** On your midterm, every proportion must be reported as a percentage rounded to one decimal place, with the reference group named. [Outline, reporting rule](materials/outline.md)

Quick check: For “Among students with jobs, what percentage commute?”, which group belongs in the denominator—and why?