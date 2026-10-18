# Feedback 04: late-arrivals question N01

Reviewed 2026-10-17. Original response: [attempt-n01.md](attempt-n01.md), preserved unchanged. Question: [next-question-01.md](next-question-01.md). Teaching basis: [course-packet.md](course-packet.md), S3. Checked key: [next-solution-01.md](next-solution-01.md). No official numerical rubric is supplied.

**Overall: partially correct. The fraction is correct; the denominator explanation is incorrect and contradicts that fraction.**

Original numerical answer: `3/4`.

Original explanation: "My denominator population is all 40 cyclists and walkers, since every proportion uses everybody."

The first error is choosing everybody as the reference population. The question says **among the late arrivals**, so the denominator counts only late arrivals: 6 cyclists + 2 walkers = 8. The matching count is 6 late cyclists. Thus **6/8 = 3/4**. In the simplified fraction, 4 is the reduced denominator; the actual reference population contains 8 late arrivals.

If you instead divided the 6 late cyclists by all 40 people, you would get 6/40 = 0.15. That answers a different question: the fraction of all people who were late cyclists. It does not justify 3/4 for the requested population.

Corrective rule from packet S3: **name the population specified by the wording, then divide the matching count by the total in that population.** Use the whole dataset only when the question asks about the whole dataset. Do not assume every proportion uses everybody.

Answer evidence: **Reasoned solution**, directly derived from packet S3 and the supplied N01 counts; Python verified `6/(6+2) == 3/4` and `6/40 == 0.15` in this review.

Assistance: you explicitly reported no hints, key or outside help before this response. Retain that as student-reported independence. The correct numerical result alone does not establish a successful independent transfer because its explanation explicitly uses the wrong population. We cannot infer how you obtained 3/4 from the inconsistent explanation.

## Learning decision

Reference-population status changes from **Improving** to **Recheck**, with high priority. The rule that every proportion uses everybody conflicts with your earlier correct P01 and worksheet Q4 explanations and repeats the previously recorded whole-table denominator error. Preserve those earlier successes; do not relabel them as wrong. There is no mastery claim or independent-transfer success for N01. Only this concept is affected; the unanswered worksheet items remain unassessed.

## Next step

Before calculating another fraction, say in words who is allowed into the denominator, then count that group. Next session should use a fresh population-switching problem to recheck this rule. An immediate revision of N01 now follows feedback and must be recorded as assisted, not as a new independent success. Earlier feedback files remain accurate for their earlier evidence; this review changes the current progress assessment, not those original judgments. No study guide was generated that needs revision.
