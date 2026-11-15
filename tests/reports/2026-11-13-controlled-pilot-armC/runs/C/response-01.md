I’ll read the study skill and your course materials, then explain conditional probability using your course’s notation and examples.

I’m using the study skill at `skill/SKILL.md`. Your notes explain conditional probability as “the probability of A among B,” and your outline requires answers as percentages to one decimal place, with the reference group named. I’ll use that format throughout.

**Hi student, let's get you uncooked.**

I’ll use your course notes to explain concepts and shape later practice around your answers. That opening line is the study skill’s greeting.

**Conditional probability means finding a share within a particular group.** Your notes read \(P(A\mid B)\) as “the probability of A among B.” Once you know \(B\), you restrict your attention to that group. ([Notes §1.1–1.2](materials/notes.md))

\[
P(A\mid B)=\frac{\text{number in both A and B}}{\text{number in B}}
\]

The symbol \(\mid\) means “given” or “among.” **The group after the bar supplies the denominator.** Your notes assume equally weighted cases and a nonempty reference group.

For example, suppose there are 100 students:

- 40 are commuters.
- 10 of those commuters bike to campus.
- Altogether, 20 students bike to campus.

“What is the probability a student bikes, **given that they are a commuter**?”

We consider only the 40 commuters. Of those, 10 bike:

\[
P(\text{bikes}\mid\text{commuter})
=\frac{10}{40}\times100\%
=\boxed{25.0\%\text{ of commuters}}
\]

The denominator is 40 because the question restricts us to commuters. Using 100 would answer a different question: what share of *all students* both commute and bike?

Now reverse the question: “What share of cyclists are commuters?” The reference group becomes the 20 cyclists:

\[
P(\text{commuter}\mid\text{bikes})
=\frac{10}{20}\times100\%
=\boxed{50.0\%\text{ of cyclists}}
\]

The overlap is the same 10 students, but the denominator changes. This is why \(P(A\mid B)\) and \(P(B\mid A)\) usually differ. ([Notes §1.3](materials/notes.md))

Your exam requires **a percentage rounded to one decimal place and the reference group in words**, as shown above. ([Outline, reporting rule](materials/outline.md))

Try this quick check: **Among students who bike, what percentage are commuters—and why is 20 the denominator?**

I initialized your [study record](learning-record.md); understanding is still unassessed. Future learning updates normally save after five meaningful turns or earlier at checkpoints, so recent unsaved answers may remain only in this chat.