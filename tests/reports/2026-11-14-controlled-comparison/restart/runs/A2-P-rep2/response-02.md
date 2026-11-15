**Hi student, let's get you uncooked.**

Not quite—Q1 has **3 element-to-element comparisons**. You counted the elements, but the question asks for comparisons between adjacent pairs:

1. `4` and `1`
2. `1` and `7`
3. `7` and `3`

The last element has no next neighbor, so there’s no fourth pair. This matches Notes §2.2: for `n ≥ 1`, an adjacent-pair pass makes `n − 1` comparisons.

Your answer shows we should practice distinguishing **elements** from **pairs**; this attempt doesn’t yet demonstrate that distinction.

To check your understanding: **if a list contains just one element, how many adjacent-pair comparisons occur, and why?**