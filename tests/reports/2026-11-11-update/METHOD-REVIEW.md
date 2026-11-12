# Independent pre-run method review

Two read-only Codex subagents reviewed the benchmark driver before the real-model phase. This is agent review, not external statistical or educator review. Neither reviewer executed model calls or edited the implementation.

The reviewers found no execution blocker: versions are frozen; local record workflows have equal final bytes and backup checks; warmup/setup are excluded; order alternates for record timings; payload bytes are explicitly distinguished from model tokens and disk writes. The real-model extension preserves paired continued sessions, matched prompts, save triggers, raw events and cumulative-accounting verification.

Required qualifications retained in METHOD.md:

- Renderer timing order is not balanced. Report first-renderer versus hardened cost without claiming a controlled small speed difference or assigning pre-PR3 a renderer runtime.
- Refresh the final manifest after derived model summaries/reports are written; the inherited runner creates its own earlier manifest.
- Inspect individual regression exit codes. The new driver was tightened to exit unsuccessfully when any stored regression check fails; the measured run had zero failed checks.
- Independently review records, assistance/progress judgments, generated questions and separate keys before interpreting resource differences as improvement.
- The byte proxy is a workflow-content measurement, not actual model tokens or billing.

Review scope: tests/benchmark_update.py and the reused tests/benchmark_record_cost.py / tests/analyze_record_cost.py. Initial review occurred before the later report-generation routine was added; final code review remains a separate completion step.
