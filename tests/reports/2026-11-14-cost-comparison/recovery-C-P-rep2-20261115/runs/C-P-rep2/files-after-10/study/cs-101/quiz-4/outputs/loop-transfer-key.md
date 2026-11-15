# Loop transfer T1 — separate solution

Question: A loop makes two complete passes over [0,-1,3], comparing each adjacent pair once per pass. How many element-to-element comparisons in total, and why?

Answer evidence: Reasoned solution, manually checked; no code execution claimed.
Answer: Each pass compares (0,-1) and (-1,3), so 2 comparisons per pass and 4 total. Exclude assignments, index updates, and loop-condition checks.
Basis: materials/notes.md §§2.1–2.3; materials/outline.md Reporting rule.
Authorship: Original course-based transfer question. Changed demand: combine two complete passes and explain why n−1 applies to each pass rather than the entire procedure.
Personal target: Determine which operations actually occur rather than applying a memorized single-pass answer.
