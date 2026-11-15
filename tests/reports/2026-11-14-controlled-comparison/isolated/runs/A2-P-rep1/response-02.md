I’ll record your attempt and the distinction to work on: counting adjacent pairs versus counting elements.

Not quite—there are **3 comparisons**. You counted the elements, but this pass counts adjacent pairs:

- `4` and `1`
- `1` and `7`
- `7` and `3`

That matches the rule in Notes §2.2: `n − 1 = 4 − 1 = 3`. We count only these element-to-element comparisons.

To check your understanding: **why doesn’t the final element, `3`, start another comparison?**