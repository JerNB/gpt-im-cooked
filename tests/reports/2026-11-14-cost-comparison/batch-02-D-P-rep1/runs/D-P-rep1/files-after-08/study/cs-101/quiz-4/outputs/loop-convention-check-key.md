# Loop convention transfer check — separate key

Original synthetic question: two complete adjacent-pair passes over [3, 1, 4, 2], with conditional swaps, as supplied in chat.

Topic: P2. Scope/style basis: materials/outline.md Reporting rule; materials/notes.md sections 2.1-2.3; materials/practice.md Q1-Q4 adjacent-pair format.

Personal target: distinguish element comparisons from other operations when the algorithm includes two passes and conditional state changes. This changes the reasoning demand from a single n-1 substitution.

Answer evidence: Verified computation with a controlled Python snippet during question creation. Each pass visits i = 0, 1, 2 and evaluates values[i] > values[i + 1] three times. Two passes give 6 element-to-element comparisons. Count the if comparison whether true or false. Exclude loop-condition checks, index updates, assignments and swaps from the reported count. No early stopping occurs in this code.

The learner has received prior explanations, Q1 correction, the Q2 answer, and feedback on Q3-Q4; this question's answer has not been revealed. No attempt or status change is established by generating the question.
