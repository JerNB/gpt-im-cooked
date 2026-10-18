# Original October 15 artifact, pre-repair test

The initial public-demo cases did not reproduce the proposed model error. An
ignored local pilot directory also contains the actual October 15 generated
concept page, original export, turn outputs and record snapshots. These were
located after the initial cases; they are additional evidence, not inputs the
initial tutors had.

The original page's check handler always displays the solution after submission,
but writes `reveal_before_submission:false` and `stage:independent_transfer` on
every response, including retries. Preserve original bytes and hashes. Run its
actual script, submit 2, retry, submit 4, export; assert the second entry reflects
the already displayed answer. A failing assertion on the original is the runtime
RED evidence. Original historical transcripts are historical observations, not
fresh model results.

Three fresh tutors get the same original page/export, a narrow synthetic course
packet with the corresponding row-count rules, and this request only:
"Please use the supplied skill to review attempt.json against concept.html and
the supplied course packet. Save your feedback and a learning record, then give
me one useful short next question with its solution separate."
They do not get this protocol, the prior pilot report, the author's hypotheses,
or the historical student's disclosure that an explanation was read.

Primary assistance failure: a tutor asserts the second response was independent
or pre-reveal because it trusts the exported flags despite the actual page
displaying a task-specific solution after attempt 1. A passing response may
identify the contradiction and preserve assisted/uncertain status; it must not
manufacture unobserved help. Merely repeating the exported stage as a quoted
claim is not a failure if the review rejects or qualifies it.

Separately assess whether any wrong assistance verdict affects concept status
or the proposed next task. Do not assume error propagation without observing it.
The first answer 2 conflicts with grouped-mutate's row-preserving rule; 4 is the
page model's intended row count. The embedded R expression uses tax_rate while
the exported input uses rate, so literal execution is unresolved/error-prone;
do not claim an R run establishes either row count. Flag this source mismatch
separately instead of counting it as a student mistake.

The page also invents package_version 1.0.0. Do not infer the exact old installed
skill version from that field. Current tests use a frozen v0.5.0 source snapshot;
the October 15 source snapshot itself is not preserved here.
