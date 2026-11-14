I’ll check the course files for loop tracing and Quiz 4, then explain the method and give you a question to try. I’ll keep a short progress file in this folder.

The file listing is taking longer than expected. I’ll wait for the course materials so the explanation uses your course’s terminology and examples.

Loop tracing means following a loop **one step at a time** and recording what it actually does. Your [notes, §2](materials/notes.md) say to track:

- The current index.
- The values read.
- Each state change, in order.

Use a small table to keep those steps straight:

| Step/index | Values read | State changes |
|---|---|---|

For Quiz 4, count **only element-to-element comparisons**. Don’t count assignments, index updates, or checks that decide whether the loop continues.

For one pass comparing adjacent elements from left to right, imagine moving along the gaps between neighboring elements. Each gap gives one comparison. Your notes state that a list of length `n ≥ 1` has `n − 1` such comparisons.

Try **Practice Q1**: a pass compares each adjacent pair in `[4, 1, 7, 3]`. Which pairs does it compare, in order, and how many element-to-element comparisons is that?

I’ve saved [progress.md](progress.md). Your understanding is still unassessed; we’ll use your attempt to see what needs more explanation.