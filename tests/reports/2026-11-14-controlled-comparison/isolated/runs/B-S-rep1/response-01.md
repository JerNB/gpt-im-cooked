I’ll read the study skill and your course materials, then use them to explain conditional probability.

**Hi student, let's get you uncooked.**

I’m using your study skill and course notes. That opening line is the skill’s study-session marker; meaningful progress stays in this chat until saved, normally after five turns with new learning evidence.

**Conditional probability means looking within a specified group.** Your notes read \(P(A\mid B)\) as “the probability of A among B”: among the cases in group B, what share also belong to A? The vertical bar means “given” or “among.” ([Notes §1.1](materials/notes.md))

The calculation is:

\[
P(A\mid B)=
\frac{\text{number of cases in both A and B}}
{\text{number of cases in B}}
\]

**B is the reference group, so B supplies the denominator.** Your notes assume equally weighted cases and a nonempty reference group. ([Notes §1.2–1.4](materials/notes.md))

For example, suppose a class has 100 students:

- 40 are commuters.
- 20 drink coffee.
- 10 are both commuters and coffee drinkers.

“What is the probability a student drinks coffee **given that they commute**?” restricts our attention to the 40 commuters. Of those, 10 drink coffee:

\[
P(\text{coffee}\mid\text{commuter})=\frac{10}{40}
\]

Report this as **25.0% of commuters drink coffee**.

Now reverse the question: “What is the probability a student commutes **given that they drink coffee**?” We’re looking within the 20 coffee drinkers:

\[
P(\text{commuter}\mid\text{coffee})=\frac{10}{20}
\]

That is **50.0% of coffee drinkers commute**. The overlap stays the same, but the denominator changes—so the order matters. ([Notes §1.3](materials/notes.md))

For your midterm, every proportion must be reported as a **percentage rounded to one decimal place, with the reference group named**. ([Outline, reporting rule](materials/outline.md))

Remember: **first identify “among whom?” Then count the target cases within that group.**

Try a quick check: Of 60 students who live on campus, 18 drink coffee. What percentage **of students who live on campus** drink coffee?