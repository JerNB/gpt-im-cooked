# STAT 110 Final — Exam Sheet Draft

**One sheet, two sides | Content rules and cumulative final scope unconfirmed**

## Side 1 — Conditional probability and two-way tables

### Conditional probability

“Probability of A among B” means restrict to group B, then find the share also in A.

**P(A | B) = count in both A and B ÷ count in B**

- Denominator = reference group after “among / of / given.” Not the whole sample.
- Order matters: P(A | B) and P(B | A) generally have different denominators.
- Course-note assumptions: equally weighted cases; reference group is non-empty.

**Example:** 10 of 25 commuters cycle → 10 ÷ 25 = 0.40 → **40.0% of commuters**.

### Two-way table percentages

| Asked “of…” | Divide cell by… | Percentages sum to 100%… |
|---|---|---|
| Row group | Its row total | Across each row |
| Column group | Its column total | Down each column |

Same decision as conditional probability: the reference group supplies the denominator. A row of column percentages need not add to 100%.

**Denominator check:** name the reference group in words first. If the question says “among column C,” divide by column C’s total, even if the cell sits in row R.

### Required answer format (supplied outline)

Report each proportion as a **percentage rounded to one decimal place**, and name the reference group: **“40.0% of commuters.”** Do not report only 0.4, 40%, or 2/5. The supplied outline says answers without the reference group lose one point.

## Side 2 — Grouped summaries, scope and checks

### Grouped summaries

- Split cases by a categorical variable; calculate a summary (e.g., mean or count) for each group.
- **Rows in result = number of non-empty groups**, not number of original cases.
- Compare like summaries: mean with mean, count with count. Do not compare a group mean with a group total.
- Example: means for 4 course sections → **4 result rows**.

### Bayes’ rule — source needed

Listed in the supplied Midterm 1 outline, but its teaching notes are missing. **Get the course method/notes before using a formula.** Whether it is on the cumulative final is unconfirmed.

### Scope caution

Available topic outline is labeled **Midterm 1**, while the course profile calls the Dec. 8 final cumulative. It confirms conditional probability, two-way-table percentages, Bayes’ rule, and grouped summaries for that midterm only. Check the current final review outline for all exam topics. Hypothesis testing is excluded from the supplied Midterm 1 outline; final status unconfirmed.

### Quick solve checklist

1. What group is the question asking about? Say it in words.
2. Use that group’s total as denominator (row, column, or stated group).
3. Divide cell / overlap count by reference-group total.
4. Convert to percent; round to **one decimal place**.
5. Label **“X.X% of [reference group]”**.
6. Grouped summary: count non-empty groups; compare the same summary type.

**Personal reminder:** Your reviewed table attempt used a row total for a column percentage. Pause to name the reference group before choosing a total.

**Use as an exam-room sheet only after confirming instructor content rules and full final scope.**

### Source basis

`materials/outline.md` (Midterm 1 scope/reporting rule); `materials/notes.md` §§1–3 (definitions, methods, assumptions); `materials/practice-key.md` Q1–Q4 (conditional probability format); `learning-record.md` (reviewed table denominator error). No Bayes’ rule method supplied.
