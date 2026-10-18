# Worksheet feedback — before.json

Reviewed: 2026-10-17. Course: Fictional intro statistics / Mock Exam A.

## Result
Q4 is correct, including its explanation. Q1–Q3 and Q5–Q8 are unattempted; no errors or weaknesses are inferred from those blanks. No numerical score is assigned because no official rubric is supplied.

## Preserved response and review
- Source: [before.json](before.json), `items[item_id=q4]`; the same response also appears in its attempt-history snapshot. These are one attempt, not two successes.
- Original answer: `["B"]`.
- Original explanation: "The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70."
- Exact task: [worksheet.html](worksheet.html#q4), Q4 asks what fraction of Plus-plan tickets had a short wait. Its table gives Plus: 28 short, 12 long, 40 total. Option B is 28/40.
- Judgment: correct. You named the requested population and used its total. Continue naming the population before choosing the denominator.
- Teaching basis: [course-packet.md](course-packet.md), S3: within-group proportions divide by the total in the requested group.
- Solution evidence: **Reasoned solution** from packet S3 and worksheet Q4; agrees with the supplied [answer-key.html](answer-key.html), Question 4, which is a reasoned practice key, not an instructor key. **Verified computation:** Python 3.13.12 confirms `28 / 40 == 0.70`.

## Assistance and learning status
The export records `hint_used: false` and `key_opened_in_page: false`. External help is explicitly untracked, so complete independence is unknown. P01 already showed a correct, independently reported library-loan explanation after a prior denominator error. This new correct ticket explanation adds evidence in another context, but does not yet justify Demonstrated under the skill's independence criteria. Status remains Improving. P01's date is unknown; no chronology relative to this export is inferred.

## Import audit
- Schema: 1.0; package: 0.4.1.
- Course/exam, artifact `cooked-stats-mock-a` version `0.3.1`, item/topic IDs, prompt, option B, and key were checked against the supplied worksheet and packet. The worksheet declares these artifact/package versions.
- Session: `evidence-session`; attempt: `evidence-session:1`; order: 1.
- Exported at: `2026-10-17T02:00:00.000Z`. The attempt-history snapshot has this same timestamp; an actual Q4 answer time is not supplied.
- Original export preserved. SHA-256: `8cee9a19eec41ba1e7356ee64078fe8e3e7229db45a0f4b2d124e1e38b6eefe6`.
- Export links such as `packet.html#s3` refer to the original page naming; the corresponding supplied teaching section is course-packet.md S3.
- No other export files were imported or used for this review.

## Next step
Try [the short follow-up](next-question.md) before opening [its separate solution](next-solution.md). It changes the conditioning group: the requested population crosses the rows of a table. This is new synthetic course-based practice, not an instructor question or an assessed success.
