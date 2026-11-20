# STAT 110 Final Cheat Sheet — study draft

**Use for studying until final rules are confirmed.** The available outline covers Midterm 1, not the cumulative final. Whether a reference sheet is allowed, and its paper size, side limit, and content rules, are unknown. Do not assume this draft is approved for the exam.

## SIDE A — Conditional probability and two-way tables

### Conditional probability

P(A | B) = count in both A and B / count in B

- Read (P(A| B)) as “the probability of A among B.”
- **Denominator = reference group B.** Name the group the question restricts to before calculating.
- Order matters: (P(A| B)) and (P(B| A)) usually differ.
- Assumptions in notes: equally weighted cases; reference group is non-empty.
- For a proportion: convert to percent, round to **one decimal place**, and name the group: “40.0% of commuters.” This is the Midterm 1 reporting rule; confirm for the final.

### Two-way table percentages

| Asked within… | Divide cell by… | Percentages sum to 100%… |
|---|---|---|
| A row category | That row total | Across that row |
| A column category | That column total | Down that column |

**Fast check:** identify the reference group in words → use its total as denominator → make sure the matching row or column sums to 100%. Rows of column percentages need not sum to 100% (and columns of row percentages need not either).

**Common trap from reviewed work:** using a row total for a column percentage. For a column percentage, use the column total.

## SIDE B — Grouped summaries and scope

### Grouped summaries

- Split cases by a categorical variable; calculate one summary (for example, a mean or count) per group.
- Output has **one row per non-empty group**, not per original case.
- Compare like with like: mean to mean, count/total to count/total.
- Example structure: 4 non-empty sections summarized → 4 rows.

### Topic coverage in supplied files

| Topic | What the available material establishes |
|---|---|
| Conditional probability | Midterm 1 scope; lecture notes §1; practice set A Q1–Q4 |
| Two-way table percentages | Midterm 1 scope; lecture notes §2 |
| Grouped summaries | Midterm 1 scope; lecture notes §3 |
| Bayes’ rule | Listed on Midterm 1 outline, but its explanation/formula is absent from the supplied notes. Get lecture notes before relying on a formula. |
| Hypothesis testing | Excluded from Midterm 1; whether it is on the cumulative final is unknown. |

### Last-minute checks

1. What group is the question asking about?
2. Is that group the denominator?
3. Does the requested row or column total 100%?
4. Is the percentage rounded to one decimal and labeled with its reference group?
5. For grouped output, are you counting non-empty groups?

**Scope source:** `materials/outline.md` is explicitly a Midterm 1 outline. **Method sources:** `materials/notes.md` §§1–3. **Reporting example/key:** `materials/practice.md` Q1 and `materials/practice-key.md`. **Historical only:** `materials/midterm-2025.md` Q2–Q3; it does not establish final scope or format.



