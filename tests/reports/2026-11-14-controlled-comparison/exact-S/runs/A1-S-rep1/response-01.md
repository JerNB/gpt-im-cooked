I’ll check the materials folder and use your course’s notation and examples to explain conditional probability.

Conditional probability means updating a probability after learning that some event happened. The key idea is to treat that event as your new set of possible outcomes. I’m still waiting for the local file listing so I can connect this to your materials.

**Conditional probability asks: within a particular group, what percentage have the characteristic we care about?**

Your [notes, §1](materials/notes.md) write this as \(P(A\mid B)\), read “the probability of A **among B**.” The group after the bar, \(B\), is your **reference group**—it determines the denominator.

For equally weighted cases:

\[
P(A\mid B)=\frac{\text{number in both A and B}}{\text{number in B}}
\]

Consider Q1 in your practice set: a class has 40 students, 25 commute, and 10 of those commuters cycle. What percentage **of commuters** cycle?

We restrict attention to the 25 commuters. Of those, 10 cycle:

\[
\frac{10}{25}\times100\%=40.0\%
\]

So the answer is **40.0% of commuters cycle.** The full class size, 40, isn’t the denominator because the question restricts us to commuters.

Two things to remember:

- **Order matters:** “cycle among commuters” and “commute among cyclists” use different reference groups.
- **Name the group:** your midterm outline requires percentages rounded to **one decimal place**, with the reference group stated in words.

Try Q2: A company has 60 employees, 24 work remotely, and 6 remote workers are trainees. **What percentage of remote workers are trainees?** First identify your reference group, then calculate.