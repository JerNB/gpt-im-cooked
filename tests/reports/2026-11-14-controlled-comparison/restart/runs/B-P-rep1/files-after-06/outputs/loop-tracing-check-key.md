# Loop-tracing transfer check — separate solution

Original synthetic question, ID P2-transfer-1. Not an instructor question.

| Item | Topic ID | Task/format | Scope/style basis | Personal target | Answer evidence |
|---|---|---|---|---|---|
| P2-transfer-1 | P2 | Trace changing adjacent values; distinguish resulting state from runtime count | materials/notes.md sections 2.1–2.3; materials/outline.md Reporting rule; practice Q1–Q4 calibrate comparison-count format only | Transfer from fixed-list pair counts to updating state; no transfer attempt reviewed yet | Verified computation: controlled Python snippet executed locally; manual trace agrees |

## Question identity

Start values=[4,1,3], changes=0. Visit i=0 then i=1. If values[i] > values[i+1], swap those two elements and increase changes by 1. Ask for final list, final changes, runtime comparison count, and which operations were counted/excluded.

## Checked solution

- i=0 reads 4 and 1: comparison true; swap gives [1,4,3]; changes=1.
- i=1 reads the updated values 4 and 3: comparison true; swap gives [1,3,4]; changes=2.
- Final list: [1,3,4]. Final changes: 2.
- Reported runtime: 2 element-to-element comparisons, specifically values[i] > values[i+1] at each of the two indices. Exclude swaps/assignments, changes increments, index updates, and loop-condition checks.
- Computation output: 0 [1,4,3] 1 1; 1 [1,3,4] 2 2; final [1,3,4], changes 2, comparisons 2.
- A correct comparison count alone does not establish correct state tracking. Review the second comparison's values and explanation. This task changes reasoning demands by making earlier updates affect later values read; it is a transfer candidate, not a reviewed success.

No student answer submitted. No hint or solution exposed in the question delivery.
