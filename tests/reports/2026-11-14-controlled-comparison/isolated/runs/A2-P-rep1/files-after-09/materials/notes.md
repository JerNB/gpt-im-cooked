# CS 101 (synthetic) — Unit 4 notes

## §1 List references and aliasing

§1.1 A variable holding a list refers to a list object; it does not contain a separate copy of every element.

§1.2 Assignment such as `b = a` makes both names refer to the same list object. Mutating through either name is visible through the other.

§1.3 A shallow copy such as `b = a.copy()` creates a new outer list, but nested mutable lists inside it may still be shared.

## §2 Loop tracing

§2.1 Trace a loop by recording the current index, values read, and each state change in order. Do not infer the result from the variable names.

§2.2 For a loop comparing each pair of adjacent elements from left to right, a list of length n has n−1 element-to-element comparisons when n is at least 1.

§2.3 The course runtime convention counts only element-to-element comparisons. Exclude assignments, index updates, and loop-condition checks from the reported count.

## §3 Nested data summaries

§3.1 A nested list can represent groups, with each inner list holding one group's observations.

§3.2 To summarize by group, compute the requested statistic separately for each inner list; do not combine groups unless asked.

§3.3 A mean is the sum of a group's values divided by that group's number of values. State the group represented by each result.
