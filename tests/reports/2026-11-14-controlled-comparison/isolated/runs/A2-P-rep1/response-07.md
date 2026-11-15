I’ll record this as a correct explanation of the runtime convention, while keeping tracing state changes marked as untested.

Correct. You explained both **why the count is 4** and **why tracing state involves operations excluded from the runtime count**.

This supports understanding of the course’s runtime convention. Carrying out a trace with state changes is still untested. I’ve updated your progress file.

One follow-up: **why could ignoring index updates while tracing lead to an incorrect result, even though they contribute nothing to the reported runtime count?**