I’ll record your attempt and the point to work on: counting adjacent pairs.

Not quite—Q1 makes **3 comparisons**. You counted the elements, but we need to count the adjacent pairs:

1. `4` with `1`
2. `1` with `7`
3. `7` with `3`

That matches Notes §2: `n − 1 = 4 − 1 = 3`. We counted only element-to-element comparisons.

To check your understanding: **Why doesn’t the final element, `3`, start a fourth comparison?**