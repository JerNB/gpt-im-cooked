# Imported attempts and browser exports

Read this before reviewing an attempt file exported from a worksheet or concept page. Saving, progress labels, and resume rules are in [state.md](state.md).

## Import identity and revisions

Read the import ledger before reviewing an export. New exports use schema version `1.0`, a session ID, attempt IDs, and separate package/artifact versions. Match course, artifact/version, item IDs, and the actual key before grading; unknown schemas or mismatched questions require clarification, not guessed mappings. Preserve the original export. Record its actual path and SHA-256 when a hashing tool is available.

Use `(session_id, attempt_id)` as the attempt identity, scoped to its artifact and course. Multiple exports and snapshots of that attempt are revisions, not independent successes. An unchanged imported file or already-reviewed attempt adds no duplicate evidence. Additional answers in a later export can update the same attempt; retain prior answers and review revisions. If identical IDs refer to different artifacts or contradictory histories, flag the conflict before updating performance. A new explicit retry gets a new attempt ID; re-exporting does not. Legacy exports remain readable: use their session/item/order fields and file hash when present, label missing identity/version fields, and compare original answers before deciding uniqueness. Do not invent timestamps or count uncertain duplicates as distinct transfer evidence.

Keep original answers separate from review judgments. A corrected review records its reason and which earlier judgment it supersedes; it never creates a new student attempt. Distinguish occurred-at, exported-at, and reviewed-at times; dates or unknown times cannot establish precise chronology. Reconcile concept status and the next-session pointer after revised feedback, and identify older guides affected by the change.

Write import identity/hash/review entries in the record's Import ledger, and concept evidence in Concepts. Read back the section placement as well as the saved bytes; a successful file commit does not validate the record's structure.

## Reviewing browser exports

For browser exports, read the supplied attempt file and verify item identity, original response, hint/reveal flags, and timing only when available. Check questions against the actual key; check concept activities against their design brief, source-grounded model, task conditions, and evaluation criteria. Treat HTML auto-scores as provisional; free-text explanations need tutor review. An answer after a task-specific hint/reveal is assisted. Ordinary exploration feedback is learning context; record what was visible and evaluate independent transfer separately. Never treat an exported 'mastered' flag, clicks, slider movements, or time on page as evidence of mastery. Do not claim page activity was saved to the learning record until the export has been reviewed and the record actually written.

An export's assistance labels are claims to check, not a substitute for its response history. A numeric check that displays the task's solution is an answer reveal for later responses, even without a separate reveal-button event. When flags conflict with the inspected page's feedback path or known exposure, preserve the export and record a qualified review correction with its source; do not copy an `independent_transfer` label into the learning judgment. Apply exposure at response time, without retroactively changing an earlier pre-feedback answer. If the path or order cannot be established, leave assistance unresolved and do not count independent transfer. False page-help flags alone do not establish absence of outside help.
