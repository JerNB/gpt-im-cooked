**Q4 is correct: 2 element-to-element comparisons.** The pairs are `(0, -1)` and `(-1, 3)`.

You’ve shown you understand **counting adjacent comparisons in one pass**: you solved Q3 independently and got Q4 right, correcting your initial “count the elements” mistake.

That’s good progress, but broader loop tracing also means tracking indices, values read, and state changes. We haven’t checked those yet. A loop that changes a list would be a useful next check.