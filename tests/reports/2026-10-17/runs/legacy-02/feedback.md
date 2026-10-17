# Attempt review

Reviewed 2026-10-17. Original export preserved at [attempt.json](attempt.json). Page: [concept.html](concept.html); teaching basis: [course-packet.md](course-packet.md), L2; feedback behavior: concept.html, `check` and `retry` handlers.

## Identity and item limits

The schema is 1.0, package/artifact versions are 1.0.0, artifact is `sta199-ex1-grouped-mutate-vs-summarize`, and the page and export contain the same transfer item, `transfer-region-mean-rows`, data, and responses. The export labels its course STA 199CCL / Exam 1 / EX1-DPLYR. The supplied packet instead identifies STA-DEMO / Midterm / T2. Their row-count rules agree, but these are not confirmed to be the same course or exam. This review retains the artifact's identity and records the packet's rule as a compatible comparison, not a course mapping or merged performance history. Course-specific grading remains provisional pending identity confirmation. The page's external slides and lab were not opened or verified.

The export's operation is `group_by(region) |> mutate(mean_tax = mean(tax_rate))`, but its table has `rate`, not `tax_rate`. As self-contained code it cannot support the claimed numeric output without repairing that name (and supplying the input table). The page's prose nevertheless explicitly asks about adding the regional mean to four existing state rows. The conceptual judgments below apply to that intended prose task. Literal execution is unresolved and is not a student error. No R execution was performed.

## Your two submissions

1. **Initial submission, 2026-10-14T16:42:32.829Z**, attempt `mv8c5njy-qg5zcp`: “2”; “There are two regions, so I expected one result row per region.” For the intended row-count question this is incorrect. The first error is using the number of groups as the number of output rows for mutate. Grouping organizes the calculation; mutate retains the observations. Two regions would produce two rows under a scalar grouped summarise instead (packet L2; page Remember and comparison panels). The export reports no hint or reveal before this first submission. The exploration area already displayed the rule, so this is an initial transfer attempt after instructional exposure, not a cold diagnostic.

2. **Retry, 2026-10-14T16:43:07.812Z**, attempt `mv8c973g-40rtr5`: “4”; “mutate attaches the region mean to every existing state row, so all four states remain.” This is correct with a clear explanation for the intended prose task. It directly repairs the initial confusion.

**Assistance correction:** Although both exported entries say `independent_transfer`, `hint_used: false`, and `reveal_before_submission: false`, the first Check displays “The output has 4 rows” plus the explanation. The retry button clears the response but repeats the same item and data. That answer exposure precedes the second response within the same session. Record the second response as a correct retry after a full reveal, not independent transfer. This is useful improvement, but one repeated item does not establish demonstration across distinct contexts.

## Rule to carry forward

For the supplied scalar-summary setting: count input observations for grouped mutate; count distinct groups for grouped summarise. Grouping alone does not remove rows. Source: packet L2; compatible with E1 Q2 and K1 Q2. Evidence label: **Reasoned solution**, checked against the supplied text and page logic; unexecuted. K1 is an instructor key for the packet's Q2, not an official key for this page's transfer item.

Next: attempt [one short new question](next-question.md) before opening its [separate solution](next-solution.md). It asks you to choose a pipeline and explain an observation-versus-group distinction with unequal group sizes.
