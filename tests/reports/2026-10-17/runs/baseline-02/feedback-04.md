# Feedback on the clinic transfer question

Reviewed 2026-10-17. Question: [next-question-01.md](next-question-01.md). Original response: [attempt-transfer-01.md](attempt-transfer-01.md). Basis: [course-packet.md S3](course-packet.md#s3-denominators). The [separate solution](next-question-01-solution.md) remains consistent with the question.

**Your fraction 3/5 is correct, but your denominator population and the rule you stated are incorrect.** The task asks both for a fraction and for the reference population; the response is therefore not a fully correct explained application. No numerical grade is assigned because no instructor rubric is supplied.

The first error is treating every proportion as a proportion of the entire dataset. S3 distinguishes within-group proportions from entire-dataset proportions: the words **among late arrivals** restrict the reference population to late arrivals only.

There are `6 + 9 = 15` late arrivals. Of those, 9 are afternoon arrivals. Thus the requested fraction is `9/15 = 3/5`.

There really are 45 arrivals overall: `18 + 6 + 12 + 9 = 45`. But that is the denominator for the different question, "What fraction of all arrivals are afternoon arrivals that were late?" With the matching count 9, that fraction would be `9/45 = 1/5`. Your stated denominator 45 does not support your stated answer 3/5. You did not show how you obtained 3/5, so no calculation method, guess, or cause of the mismatch is assumed.

Corrective rule: **Name the group the question says to consider; count everyone in that group for the denominator, then count those in it meeting the requested condition for the numerator.** Here that group is all late arrivals, regardless of morning or afternoon.

Answer evidence: **Reasoned solution** from packet S3 and the exact clinic question; **Verified computation** in Python 3.13.12 using exact Fraction arithmetic: `9/15 = 3/5` and `9/45 = 1/5`, with totals 15 and 45 checked.

Your no-hints/no-key/no-outside-help statement is retained as explicit student-reported independence for this attempt. This attempt supports a specific difficulty in selecting the denominator population, even though its final fraction is correct. It does not establish successful independent transfer.

The concept moves from Improving to **Recheck**, with high priority, because this explicit population rule contradicts the earlier correct explanations in P01 and worksheet Q4. Those earlier successes remain valid and preserved; the new evidence changes the current assessment. The worksheet retry remains assisted repetition, and the seven blank worksheet items remain unattempted.

Next: rewrite only the population sentence for this same clinic question, explaining why on-time arrivals are excluded. That revision will follow this feedback and must be recorded as assisted, rather than counted as a new independent transfer. A later fresh task can check whether the rule transfers independently. The original clinic question is now answered and reviewed; it is no longer pending. Earlier feedback files are historical, while this file supplies the current next step. No prior study guide requires correction.

Saved record: [learning-record.md](learning-record.md).
