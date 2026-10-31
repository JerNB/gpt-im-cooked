# Changelog

## v2.0.0 — V2 workflow update — October 31, 2026

**Less recordkeeping between questions. More practice built around how you learn.**

GPT, I'm Cooked now batches learning-record updates, carries a concise continuation summary between study sessions, and gives reviewed mistakes a clearer role in practice and study guides. New humanities guidance extends feedback beyond finding a single correct answer to evaluating claims, evidence, and interpretation.

V2 is released as package version `2.0.0`. Download the [standalone skill](docs/downloads/gpt-im-cooked-skill-v2.0.0.zip) or [plugin package](docs/downloads/gpt-im-cooked-plugin-v2.0.0.zip), or use the maintained [skill source](plugins/gpt-im-cooked/skills/gpt-im-cooked/SKILL.md). Earlier versioned archives remain available. Existing course directories and skill/plugin identities are preserved; no record migration is required.

### Changed: learning records save at meaningful checkpoints

Previously, a tutoring turn with new learning evidence required a record update. The new default collects a compact summary in the current conversation and saves after **five tutoring turns with meaningful changes**. Greetings and unchanged explanations do not count. Ordinary follow-up questions reuse already-loaded state rather than requiring another file read.

Progress saves earlier when the student requests it, corrects or removes a record, changes course or exam scope, switches courses, finishes an imported-attempt review, or explicitly ends a session or requests a handoff. Pending evidence also saves before a personalized guide, reference sheet, substantial practice set, or mock exam is delivered. Students can choose a different save interval.

The tutor uses new evidence immediately when teaching; batching changes when that evidence reaches the file. Existing conflict detection, backups, and write verification remain in place. Recent unsaved changes may be unavailable to a new chat after an abrupt close, so students can ask to **“Save my progress now.”**

### Added: a clearer way to continue in a new chat

The saved next-session summary now includes the current question or source location, the unresolved step, useful student reasoning, hints or solutions already shown, and the next activity. Long attempts and solutions stay in linked files.

This makes it easier to resume from selected learning state instead of relying on an entire previous conversation. Saving does not clear the current context or disable automatic context compaction. A new chat still needs access to the study files; saving progress and starting a new chat are separate decisions.

### Added: mistake review and targeted variants

Students can ask to **“Review my mistakes”** or **“Make a variant targeting this mistake.”** The tutor selects a small set using repeated reviewed errors, prerequisite dependencies, and unresolved rechecks.

Follow-up practice can take three forms:

- **Retry:** apply the same structure to check execution.
- **New setting:** use the same principle in a different situation.
- **Changed condition:** decide whether the original method still applies.

Changing numbers alone is treated as execution practice. Transfer practice changes the setting or reasoning demands. Rechecks distinguish assisted corrections, unaided original-question retries, and independent transfer, and learning priorities reflect improvement as well as recurring errors.

### Improved: study guides built around useful corrections

Personalized guides can now include selected mistakes alongside knowledge summaries: the necessary prompt, the student's original reasoning, the first error, and the corrected method with its conditions. An unanswered variant can extend the review into practice.

There is no fixed mistakes-to-concepts ratio. Page space follows the subject, exam format, learning stage, and available evidence while preserving topic coverage. Exam-room sheets follow confirmed instructor restrictions; worked questions and answers appear only when permitted. Independent practice keys remain separate from guide explanations.

### Added: humanities and interpretive-writing guidance

Practice and feedback now explicitly cover factual recall, contextual reading, source comparison, and argument construction. The tutor separates factual accuracy from interpretation and evaluates how a response connects its claim, evidence, reasoning, and context.

Different interpretations can be valid when supported by the supplied material. A model response is a reasoned example rather than the only acceptable conclusion. Records identify specific issues to revise, such as unsupported claims, misread passages, or gaps between evidence and conclusions. Guides can pair short original and revised excerpts with explanations of the changes.

### Try the update

> Review my recorded mistakes and give me a short practice set. Change the situation or conditions so I have to choose the method, and keep the answers separate.

> Make a study guide that combines the key concepts with selected mistakes and explains why each correction works.

> Save my progress and prepare a concise handoff so I can continue in a new chat.

### Validation and availability

Release checks cover skill-format validation, package metadata and relative links, byte-for-byte matching of both extracted downloads to source, record-write safety, existing demo and evidence regressions, and whitespace checks. Validation uses an isolated copy of the release file set; an unrelated untracked local reference is excluded from publication. See [validation status](VALIDATION.md).

These checks establish instruction and package consistency. They do not quantify response-time improvements, token savings, humanities grading reliability, or learning gains. The update is designed to reduce repeated record operations; measured performance claims require a separate comparison.

### Short announcement

GPT, I'm Cooked V2 brings checkpoint-based learning records, targeted mistake review, and clearer study-session handoffs. Turn reviewed errors into fresh practice, build guides around the corrections that matter, and review humanities through claims, evidence, and reasoning. Available now in the repository and the v2.0.0 standalone skill and plugin downloads.

