Not quite—there are **3 comparisons**. Count adjacent pairs, rather than elements:

1. `4` and `1`
2. `1` and `7`
3. `7` and `3`

The last element has no next neighbor, so one full pass makes **n − 1 = 4 − 1 = 3 element-to-element comparisons**.

Try Q2: with `[8, 2, 5, 6, 1, 4]`, how many adjacent comparisons would one pass make?