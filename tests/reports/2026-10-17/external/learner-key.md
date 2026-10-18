# Draft research key -- teacher approval outstanding

Keep separate from teaching and learner administration. These are author-derived
solutions from supplied packet L2, not an instructor rubric or externally
validated instrument. No student has answered these items in this project run.

| Item | Reference answer / required reasoning |
|---|---|
| A1 | 12; each row is a visit. Grouping partitions calculation; mutate retains observation rows. |
| A2 | Scalar summarise then mutate; 4 then 4. After the first step, rows represent clinics, and mutate retains its four-row input. |
| A3 | Grouped mutate on the six-row table yields 6 rows. Grouping alone preserves rows; the operation, not just the number of groups, determines output count. Accept other fully specified valid counterexamples under L2. |
| B1 | Mutate. Output rows remain observations, with repeated group summaries attached. Scalar summary would give 3 region rows. |
| B2 | 2 then 2. The second operation receives the two-row team-summary table; it does not reconstruct the five observation rows. |
| B3 | X:10 observation rows; Y:2 group-summary rows. Summarise changes the unit; grouping alone does not. |
| C1 | No: with one observation in every group both counts are 3. Inspect the operation, retained original columns/rows and the meaning of output rows. Do not equate equal counts with identical operations. |
| C2 | 24,6,6. Final mutate preserves its current six-row summary input. |
| C3 | Scalar summary condenses states into region rows, violating required observation preservation. Use grouped mutate to attach a region mean to each original state row. |

Proposed research scoring per item (must be reviewed and frozen by teacher):
2 = all requested counts/choices and source-consistent row-unit reasoning;
1 = a substantive correct component but missing or contradictory requested
reasoning; 0 = no supported correct component. Preserve separate numeric/choice
and reasoning fields, so a correct number with wrong reasoning cannot hide in
an overall total. Treat unattempted as missing evidence for diagnosis; prespecify
its assessment-score treatment before administration. Accept equivalent language
and valid alternative constructions. The item pools have not been equated;
their totals must not be compared as if difficulty were already controlled.
