**Hi student, let's get you uncooked.**

I’ll check Q1’s exact wording and comparison rule before reviewing your answer.

**Hi student, let's get you uncooked.**

Q1 has **3 element-to-element comparisons**. You counted the elements, but the loop compares **adjacent pairs**:

- `4` with `1`
- `1` with `7`
- `7` with `3`

After the last pair, there’s no next element to compare. For this single pass, \(n\) elements give \(n-1\) comparisons: \(4-1=3\).

This matches the **Instructor key**, [practice-key.md](materials/practice-key.md), Q1, and the rule in [notes.md](materials/notes.md), §2.2.

Try a boundary check: if a list contains just **one element**, how many adjacent-pair comparisons can it make?