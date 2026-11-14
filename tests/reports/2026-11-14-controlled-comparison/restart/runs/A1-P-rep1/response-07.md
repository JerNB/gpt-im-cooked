**Correct throughout.** Your trace uses the updated list each time, ending with `values = [1, 3, 2, 4]` and `swaps = 3`.

The reported runtime count is **3 element-to-element comparisons**: `4 > 1`, `4 > 3`, and `4 > 2`. Your exclusions match the course convention.

This demonstrates both state tracing and comparison counting. Here, swaps and comparisons happen to total 3; a comparison still counts even when it causes no swap.