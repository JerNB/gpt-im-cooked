I’ll look through your course materials for loop tracing, then explain it using the course’s approach and give you a question to try. I’ll also keep a short progress file here for next time.

**Loop tracing means following a loop one step at a time**, recording the current index, values read, and any changes in order. Your [notes, §2](materials/notes.md) emphasize following what happens rather than guessing from variable names.

For example, suppose a pass compares adjacent elements from left to right in `[6, 2, 9]`:

| Step | Indices read | Values compared |
|---|---|---|
| 1 | 0 and 1 | 6 and 2 |
| 2 | 1 and 2 | 2 and 9 |

That makes **2 element-to-element comparisons**. Comparing values alone doesn’t change the list; record changes only if the loop instructs you to make them.

For this kind of pass, a list of length `n` has `n − 1` comparisons when `n ≥ 1`. Your course counts **only element-to-element comparisons**—exclude assignments, index updates, and loop-condition checks.

Try **Practice Q1**: A pass compares each adjacent pair in `[4, 1, 7, 3]`. How many element-to-element comparisons occur? List the pairs you counted.

I’ve started [progress.md](progress.md). We’ll assess your understanding from your attempts.