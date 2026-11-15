# Loop convention transfer check — solution

Original synthetic question: A pass compares each adjacent pair in [4, 1, 7, 3] once, then compares the first and last elements once more. It also performs four assignments and five loop-condition checks. Report the element-to-element comparison count and explain the treatment of the other operations.

- Topic: P2 loop tracing/runtime convention.
- Scope basis: materials/notes.md §§2.1–2.3; materials/outline.md, Reporting rule.
- Personal target: Transfer beyond the repeated complete-adjacent-pass pattern, following correct Q3 and Q4 attempts after Q1's element-count error.
- Changed reasoning demand: Account for an extra nonadjacent element comparison; apply n−1 only to the adjacent pass.
- Solution: 4 element-to-element comparisons. The adjacent pass compares (4,1), (1,7), and (7,3); the additional comparison is (4,3). Four assignments and five loop-condition checks are excluded.
- Evidence: Reasoned solution, manually enumerated; no code execution needed or performed.
- Assessment: An answer of 4 with the three-plus-one explanation and exclusion of assignments/condition checks supports this transfer. Assess actual student reasoning and assistance before updating progress. This one answer alone does not establish all loop-tracing skills.
