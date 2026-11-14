# Loop convention check 1: separate solution

- Topic: P2 loop tracing and runtime convention.
- Original synthetic question; course basis: materials/notes.md sections 2.1-2.3; materials/outline.md Reporting rule.
- Target: distinguish accumulator state from element-comparison count. Changes reasoning demand from length-only counts to tracing conditional state changes and reporting the permitted operation.
- Input: values = [3, 1, 2], score = 0. For i = 0 then 1, compare values[i] > values[i+1]. Add 2 to score if true, otherwise add 1.
- Answer evidence: Verified computation using a controlled Python translation during question preparation.
- Trace: i=0 compares 3 > 1 (true), score becomes 2. i=1 compares 1 > 2 (false), score becomes 3.
- Final score: 3. Reported runtime: 2 element-to-element comparisons, namely 3 > 1 and 1 > 2.
- Exclude score initialization and updates, index updates, and loop-condition checks. The false comparison still counts.
- Feedback criteria: correct state trace plus correct operation count and exclusion reasoning. No numerical rubric supplied. A count alone does not establish state tracing; a score of 3 reported as runtime conflates accumulator output and comparison count.
- Assistance: question delivered without answer or task-specific hint; key kept separate.
