**Hi student, let's get you uncooked.**

I’ll check Q1’s exact loop and the practice feedback guidance before reviewing your answer.

**Hi student, let's get you uncooked.**

Q1 has **3 comparisons**. You counted the elements; the question asks how many adjacent pairs are compared:

- `4` with `1`
- `1` with `7`
- `7` with `3`

The last element has no next neighbor, so it doesn’t start another comparison. For this pass, **\(n\) elements give \(n-1\) comparisons**. ([Notes §2.2](materials/notes.md))

Your answer could be: “3 element-to-element comparisons, counting each adjacent pair once.” This matches the **Instructor key, Q1**. ([Practice key](materials/practice-key.md))

Quick check: if you append one element to the list, how many **additional** adjacent comparisons would the pass need, and why?