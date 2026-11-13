# STAT 110 (synthetic) — Lecture notes

## §1 Conditional probability

§1.1 P(A | B) is read "the probability of A among B". It answers: of the
cases in group B, what share are also in A?

§1.2 Compute it as (number of cases in both A and B) divided by (number of
cases in B). The denominator is the reference group B, not the whole sample.

§1.3 The order matters. P(A | B) and P(B | A) usually differ because they use
different reference groups. Before computing, decide which group the question
restricts you to; that group is the denominator.

§1.4 Assume every case is equally weighted and the reference group is not
empty.

## §2 Two-way tables

§2.1 A two-way table counts cases by two categorical variables at once, one in
the rows and one in the columns, with row totals and column totals.

§2.2 A row percentage divides a cell by its row total; a column percentage
divides a cell by its column total. Choosing row versus column percentages is
the same decision as choosing the reference group in §1.2.

§2.3 Row percentages in one row add to 100%; column percentages in one column
add to 100%. Percentages across a row of column percentages need not.

## §3 Grouped summaries

§3.1 A grouped summary splits the cases by a categorical variable and computes
one summary value (such as a mean or a count) per group.

§3.2 The result has one row per non-empty group, not one row per original case.

§3.3 Compare groups using the same summary; do not compare a group mean with a
group total.
