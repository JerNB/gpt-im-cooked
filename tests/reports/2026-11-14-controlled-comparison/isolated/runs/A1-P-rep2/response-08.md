**Big-O describes how the work an algorithm does grows as its input gets larger.** Let \(n\) mean the number of elements in the input.

Your outline lists Big-O for Quiz 4, but says the lecture notes haven’t been posted. This is a general introduction; we don’t yet have the course’s specific Big-O guidance.

Using the course convention of counting element-to-element comparisons:

| Algorithm | Comparisons | Big-O |
|---|---:|---|
| Compare just the first two elements | 1 | \(O(1)\) — constant |
| Compare every adjacent pair once | \(n-1\) | \(O(n)\) — linear |
| Compare every element with every other element | \(n(n-1)\) | \(O(n^2)\) — quadratic |

**Big-O captures the growth pattern, rather than the exact count.** For example, your adjacent-pair loop makes \(n-1\) comparisons. If you roughly double the list length, you roughly double the comparisons, so its growth is linear: \(O(n)\).

When expressing Big-O, we drop constant multipliers and lower-order terms:

- \(3n + 2\) → \(O(n)\)
- \(n^2 + 5n + 4\) → \(O(n^2)\)

Technically, Big-O is an **upper bound** on growth. In introductory exercises, you generally aim for the tightest useful bound, such as \(O(n)\) for that adjacent-pair pass.

To check your understanding: **if you run the adjacent-pair pass twice, making \(2(n-1)\) comparisons total, what is its Big-O?**