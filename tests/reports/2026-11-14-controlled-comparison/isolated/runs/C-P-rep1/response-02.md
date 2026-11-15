**Hi student, let's get you uncooked.**

I’ll check Q1’s exact loop and compare it with your reasoning.

**Hi student, let's get you uncooked.**

Q1 has **3 element-to-element comparisons**. You counted the elements; the loop compares adjacent **pairs**:

1. `4` with `1`
2. `1` with `7`
3. `7` with `3`

The final element has no right-hand neighbor, so there’s no fourth pair. For this pass, **4 elements → 4 − 1 = 3 comparisons**. This matches the [instructor key, Q1](materials/practice-key.md) and [Notes §2.2](materials/notes.md).

Quick check: how many adjacent-pair comparisons would a list containing just `[9]` have, and why?

I saved this reasoning in your [learning record](study/cs-101/quiz-4/learning-record.md) so we can revisit it.