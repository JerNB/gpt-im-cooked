# Demo course packet

Fictional introductory statistics course. This is the complete teaching basis for the public demo, not a real university syllabus. All datasets and question wording are original.

## S1: Observations and variables
A row is one observation; a column is one variable. A categorical variable records a label or group, whereas a numerical variable records a measured or counted quantity. `plan` is categorical; `wait_min` is numerical. A tibble with 60 rows and three columns has 60 observations and three variables.

## S2: Plot choice and interpretation
A histogram displays the distribution of one numerical variable. A bar chart compares counts or proportions across categories. Side-by-side boxplots compare one numerical variable across categorical groups. A scatterplot displays the relationship between two numerical variables. Similar histogram shapes do not imply identical spreads or centers. A scatterplot alone can show association but cannot establish causation.

## S3: Denominators
A within-group proportion divides the matching count by the total in that group. A proportion of the entire dataset divides by the overall total. Always name the reference population. In our fictional ticket table, Basic has 12 short and 8 long waits (20 total); Plus has 28 short and 12 long waits (40 total). Short means less than 5 minutes. Overall there are 60 tickets.

## S4: R summaries and missing values
Use `group_by(plan)` before `summarize()` for a separate summary for each plan. `summarize(avg_wait = mean(wait_min, na.rm = TRUE))` computes a mean from nonmissing waits within each group. `na.rm = TRUE` removes missing values from this calculation; it does not automatically edit the original dataset. The pipe `|>` sends the previous result into the next function. This packet uses dplyr syntax.

## S5: Factor order
`factor(priority, levels = c("Low", "Medium", "High"))` explicitly orders these categorical levels from Low to High. Levels follow the vector's supplied order; this is not an instruction to sort numeric values.

## Scope and practice style
Included: S1-S5 only. Excluded: joins, inference tests, regression fitting, and probability distributions. Fictional style blueprint: choose-all-that-apply, choose-one, interpretation, and R code completion. A 25-minute suggested practice time is an estimate, not an instructor's exam rule. No official point rubric or note allowance is supplied.
