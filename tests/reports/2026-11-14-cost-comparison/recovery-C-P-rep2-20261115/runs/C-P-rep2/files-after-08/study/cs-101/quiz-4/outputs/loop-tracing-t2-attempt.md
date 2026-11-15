# T2 original attempt and review

## Original student response

The final values are a = [2, 2, 3, 3] and changes = 2. At i = 0, compare 2 > 1: true, so a becomes [2, 2, 3, 0] and changes becomes 1. At i = 1, compare the current 2 > 3: false, so neither changes. At i = 2, compare 3 > 0: true, so a becomes [2, 2, 3, 3] and changes becomes 2. I report 3 element-to-element comparisons, counting all three evaluations of a[i] > a[i + 1], including the false one. I exclude assignments to the list and to changes, the changes increment, index updates and loop-condition checks. The value changes = 2 counts successful updates, not all comparisons.

## Tutor review

Correct throughout; matches loop-tracing-t2-key.md (Verified computation). No task-specific hint or solution was shown before submission. Prior instruction and practice feedback were available. The transfer task changes the reasoning demand from counting pairs to following mutations and distinguishing successful updates from all comparisons. Combined with Q3/Q4, supports Demonstrated for the supplied P2 tracing/runtime convention. Recheck before exam; same-session evidence does not establish delayed retention.
