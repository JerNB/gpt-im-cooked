I’ll look through your course files, explain loop tracing using their notation, and keep a short progress file here for next time.

Loop tracing means following a loop **one step at a time**, recording the current index, the values it reads, and any changes it makes—in execution order. Your [course notes](materials/notes.md) emphasize following the actual operations rather than guessing from variable names.

For Quiz 4, focus on a pass that compares **adjacent elements from left to right**. Think of placing a finger between two neighboring elements, comparing them, then moving one position right. Stop after comparing the last two elements.

For a list of length `n`, that pass makes **`n − 1` element-to-element comparisons**, provided `n ≥ 1`: each comparison corresponds to a gap between neighbors.

Your course counts **only element-to-element comparisons**. Exclude assignments, index updates, and loop-condition checks, and state what you counted.

Try **Q1** from your [practice set](materials/practice.md):

A pass compares each adjacent pair in `[4, 1, 7, 3]`. **How many element-to-element comparisons occur, and which pairs are compared?**

I’ve saved [your progress](study-progress.md). We haven’t assessed your understanding yet; your explanation will give us our first evidence.