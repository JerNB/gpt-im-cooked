**Big-O describes how the amount of work grows as the input gets larger.** It focuses on growth rather than an exact operation count.

Your outline includes Big-O, but says the lecture notes haven’t been posted yet. Here’s the general idea, using your course’s convention of counting element-to-element comparisons.

For an adjacent-pair pass:

| Number of elements \(n\) | Comparisons \(n-1\) |
|---|---|
| 4 | 3 |
| 8 | 7 |
| 100 | 99 |

When the list roughly doubles in size, the comparisons roughly double. This is **linear growth**, written **\(O(n)\)**.

The exact count is \(n-1\); Big-O drops constant factors and lower-order terms:

| Comparison count | Big-O | Growth |
|---|---|---|
| \(1\) | \(O(1)\) | Constant |
| \(n-1\) | \(O(n)\) | Linear |
| \(3n+2\) | \(O(n)\) | Linear |
| \(n^2\) | \(O(n^2)\) | Quadratic |

With quadratic growth, doubling the input makes the work roughly **four times** as large.

Technically, Big-O gives an **upper bound** on growth; introductory exercises usually ask for the tightest useful bound.

For your earlier loop, you could report:

- **Exact runtime count:** \(n-1\) element-to-element comparisons, for \(n \geq 1\).
- **Big-O:** \(O(n)\).

Quick check: if a loop makes exactly \(2n+5\) element-to-element comparisons, what is its Big-O?