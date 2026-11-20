# STAT 110 Final Cheat Sheet — Study Draft

**Exam-use rules and final coverage are unconfirmed.** The supplied outline is for Midterm 1 only; it does not establish the final's cumulative scope or reference-sheet allowance/format. This draft covers supported material from lecture notes §§1–3. Bayes' rule appears in the outline, but its method is not in the supplied notes, so it is flagged below rather than reconstructed.

## Side A — Conditional probability and two-way tables

### Conditional probability: choose the reference group first

\[
P(A\mid B)=\frac{\#(A\text{ and }B)}{\#(B)}
\]

- Read **“A given B”** as: among cases in **B**, what share are also in **A**?
- **Denominator = the group after the bar** (the condition/reference group), not automatically the whole sample.
- Order matters: \(P(A\mid B)\) and \(P(B\mid A)\) generally use different denominators and can differ.
- Course assumptions: cases are equally weighted; reference group is nonempty.

**Quick example.** Of 25 commuters, 10 cycle. The question asks “what percentage of commuters cycle?” Reference group = commuters, so \(10/25=0.400=\mathbf{40.0\%\ of\ commuters}\). Do not divide by the full class size.

### Two-way tables: percentage direction sets denominator

| Asked for | Divide each cell by | Check |
|---|---|---|
| Row percentage | That cell's **row total** | Percentages across each row sum to 100% |
| Column percentage | That cell's **column total** | Percentages down each column sum to 100% |

Translate the question into a reference group: “among [group]” tells you which row/column total should be the denominator. Row percentages across different rows need not be comparable as a single distribution; likewise, column percentages across columns need not add to 100%.

### Required reporting format (from the supplied outline)

Report every proportion as a **percentage rounded to one decimal place** and name the reference group: **“40.0% of commuters.”** Do not report only a decimal, an unrounded fraction, or a percent with no group. The outline says omitting the reference group loses one point.

## Side B — Grouped summaries and scope checks

### Grouped summaries

- Split cases by a categorical variable; compute the chosen summary (for example, a mean or count) separately for each group.
- **Output rows = number of non-empty groups**, not number of original cases.
- Compare like with like: use the same summary measure for every group; do not compare a group mean with a group total.

**Fast check.** Four non-empty course sections → four summary rows, even if there are 120 students.

### Bayes' rule — source gap

The Midterm 1 outline lists Bayes' rule as covered in lecture, but the supplied notes do not provide its formula, conditions, or an example. **Add the instructor's version from your notes before relying on this sheet for Bayes' rule.**

### Final-scope check before using in the exam

- Confirm which topics from the course are on the final; this sheet only verifies Midterm 1 topics T1, T2, and T4.
- Confirm whether Bayes' rule is on the final and obtain the missing teaching material.
- Confirm whether hypothesis testing is on the final. It is excluded from **Midterm 1** in the supplied outline only; that does not establish its final status.
- Confirm whether a reference sheet is allowed and the permitted page/side, size, handwriting/typing, and content rules.

### Last-pass checklist

1. What is the reference group? Use it as the denominator.
2. For a table percentage, does the row/column direction match that group?
3. Is the result a percent to one decimal place, with the group named?
4. For a grouped summary, did I count non-empty groups and compare the same summary?

**Sources:** STAT 110 Midterm 1 outline (reporting rule and stated scope); lecture notes §§1.1–1.4, 2.1–2.3, 3.1–3.3; Practice set A Q1–Q4 and instructor key. The 2025 paper is historical and does not establish current final coverage.
