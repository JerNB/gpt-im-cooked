# Clinic follow-up feedback — review 04

Reviewed 2026-10-17. Original response: [clinic-attempt-01.md](clinic-attempt-01.md). Task: [next-question.md](next-question.md), Follow-up 01. Basis: [course-packet.md](course-packet.md), S3.

## Judgment
**Partially correct:** 3/5 is the correct numerical fraction, but the named denominator population and stated rule are incorrect. The question explicitly requests both fraction and population, so this is not a fully correct explained transfer.

You wrote: "My denominator population is all 40 clinic appointments, since every proportion uses everybody." The first error is treating every proportion as a proportion of the entire dataset. S3 distinguishes within-group proportions from whole-dataset proportions: the requested population sets the denominator.

Here, "among all late arrivals" identifies the group. There are 4 morning late arrivals and 6 afternoon late arrivals: 10 late arrivals total. Of those, 6 were afternoon appointments. Thus 6/10 = 3/5. The 5 in the simplified fraction represents a reduced ratio; the actual reference-population count is 10, not 40.

Your final fraction and your explanation are inconsistent: using the six afternoon late arrivals over all 40 appointments would yield 6/40 = 3/20, not 3/5. That different fraction would answer what fraction of all appointments were both afternoon and late. A correct number alone does not settle which population was used. How you obtained 3/5 is not yet explained; no guessing or copying is inferred.

## Corrective rule and next action
First name the group after "among" or "of"; count everyone in that group; then count the matching members within it. Packet S3 supplies this rule. For this clinic item, explain in your own words why both the 4 morning late arrivals and 6 afternoon late arrivals belong in the denominator. A revision after this feedback is coached; assess a fresh independent transfer later before promoting the status.

## Evidence and learning record
- Solution evidence: **Reasoned solution**, using packet S3 and the clinic question's counts; agrees with [the separate generated key](next-solution.md), not an instructor key.
- **Verified computation:** exact rational calculations in Python 3.13.12 confirmed `Fraction(6,10) == Fraction(3,5)` and `Fraction(6,40) == Fraction(3,20)`; total appointments checked as 40.
- Assistance: student explicitly reports no hints, key, or outside help before this response. Preserve that report; earlier worksheet key exposure is a different task and does not contradict it.
- Status changes from Improving to **Recheck**, high priority: the new independent-by-report explanation contradicts earlier correct population reasoning and repeats the prior whole-table-denominator rule. Earlier correct P01 and worksheet Q4 evidence remains preserved; this review does not invalidate their correctness or erase progress.
- The clinic task is now attempted, with correct fraction / incorrect population reasoning. The seven blank worksheet items remain unattempted and supply no new weakness evidence.
- [Feedback 01](feedback-01.md) and [feedback 02](feedback-02.md) remain historical reviews. Their prior status snapshots are superseded by this current Recheck decision. The original clinic question/key remain mathematically valid; only the old record pointer saying the task is pending is superseded. No guide requires revision.
