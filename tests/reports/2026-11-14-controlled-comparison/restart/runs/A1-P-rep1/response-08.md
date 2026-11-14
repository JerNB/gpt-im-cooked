**Big-O describes how the work an algorithm does grows as its input gets larger.** Let `n` represent the input size—for example, the number of elements in a list.

Your outline includes Big-O, but says the lecture notes aren’t posted yet. This is a general introduction using your course’s rule of counting element-to-element comparisons.

For the adjacent-pair loop you traced:

- With 4 elements, it makes 3 comparisons.
- With 8 elements, it makes 7 comparisons.
- With 100 elements, it makes 99 comparisons.

The exact count is **n − 1**. Its Big-O is **O(n)**, called *linear*: doubling the list length roughly doubles the work.

Big-O ignores constant factors and smaller terms when describing growth. Thus `n − 1`, `2n`, and `3n + 5` are all **O(n)**.

| Big-O | Name | Example pattern |
|---|---|---|
| **O(1)** | Constant | Compare the first two elements once, regardless of list length |
| **O(n)** | Linear | Compare each adjacent pair in one pass |
| **O(n²)** | Quadratic | For each of n elements, compare it with all n elements |

Strictly, Big-O gives an **asymptotic upper bound**: a growth ceiling for sufficiently large inputs. We usually report the tightest useful bound—so your single pass is described as O(n).

Keep these two answers distinct: **“n − 1 comparisons” is an exact count; “O(n)” describes its growth.**

Quick check: if a loop makes exactly `2n + 3` element comparisons, what Big-O would you report?