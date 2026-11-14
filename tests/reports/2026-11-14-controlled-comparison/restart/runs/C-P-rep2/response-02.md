**Hi student, let's get you uncooked.**

I’ll check practice Q1 and its key against your reasoning.

**Hi student, let's get you uncooked.**

Not quite—Q1 has **3 element-to-element comparisons**. You counted the elements, but the loop compares neighboring pairs:

1. `4` and `1`
2. `1` and `7`
3. `7` and `3`

There’s no next element after `3`, so the pass ends. For this adjacent-pair pass, **4 elements → 4 − 1 = 3 comparisons**, matching the [instructor key, Q1](materials/practice-key.md).

Quick check: if the list contained **just one element**, how many adjacent comparisons would there be, and why?

I saved this correction in your [learning record](study/cs-101/quiz-4/learning-record.md).