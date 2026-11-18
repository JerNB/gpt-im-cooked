# STAT 110 Final Review Starter

**Course-based starter.** The supplied outline is for Midterm 1, not the cumulative final, so this guide does not claim full final coverage. Exam use and the instructor's reference-sheet rules are unconfirmed. This draft is based only on the local outline, notes, practice set/key, past paper, and learning record.

## Scope and source gaps

- **Supported here:** conditional probability (notes §1; practice A Q1–Q4), two-way tables (notes §2), and grouped summaries (notes §3; 2025 midterm Q3).
- **Bayes' rule:** the outline lists it in scope and says it was covered in lecture, but its teaching notes are not supplied. Add the lecture explanation before studying this topic from the guide.
- **Final coverage is unconfirmed:** the supplied outline is for Midterm 1. Hypothesis testing is excluded from that midterm, though it appears on the 2025 paper; the files do not say whether it is on the final.

**Reporting rule (outline):** report each proportion as a percentage rounded to one decimal place and name the reference group: “40.0% of commuters.”

## T1. Conditional probability

`P(A | B)` means the share of group **B** that is also in **A**:

`count(A and B) / count(B)`

The group after the bar is the reference group and denominator. Order matters: `P(A | B)` and `P(B | A)` generally use different denominators. (Notes §1.1–1.4.)

**Example (practice A Q1):** 25 of 40 students commute; 10 commuters cycle. The question asks about commuters, so use the 25 commuters:

`10 / 25 = 0.40 = 40.0% of commuters`

## T2. Two-way tables: choose the denominator

Use one table to distinguish row and column percentages. Rows are commute status; columns are cycling status.

|  | Cycle | Do not cycle | Row total |
|---|---:|---:|---:|
| Commuters | 10 | 15 | 25 |
| Noncommuters | 5 | 20 | 25 |
| Column total | 15 | 35 | 50 |

For the cell **commuters who cycle**:

- **Row percentage:** `10 / 25 = 40.0% of commuters` cycle. Divide by the commuters row total.
- **Column percentage:** `10 / 15 = 66.7% of cyclists` are commuters. Divide by the cycling column total.

Before calculating, say the reference group in words. Its row or column total is the denominator. Row percentages add to 100% across each row; column percentages add to 100% down each column. (Notes §2.1–2.3.)

**Personalized correction:** the learning record shows a prior column-percentage attempt used a row total. For a column percentage, divide by the column total and name that column group.

## T4. Grouped summaries

Split cases by a categorical variable and compute the selected summary, such as a mean or count, for each group. The output has one row per non-empty group, not one per original case. Compare the same kind of summary (mean with mean, total with total). (Notes §3.1–3.3; 2025 midterm Q3.)

## What to add before the final

Get the final exam outline and the missing Bayes' rule lecture material. Confirm the sheet allowance before bringing this draft into the exam. Once those materials are available, the guide can be expanded to the confirmed cumulative scope.
