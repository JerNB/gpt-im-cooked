# Course and learning state

## Storage and continuity

Reuse the student's chosen course directory. Otherwise, in a writable workspace create `study/<course-slug>/<exam-slug>/` with `course-profile.md`, `learning-record.md`, and `materials/` and `outputs/` only when needed. Create records only after the course is identified and there is something to save: a reviewed attempt, a specific self-reported difficulty, a status change, a scope correction, or an explicit save request. Until then keep the scope summary in the reply and the pending summary; a first explanation creates no files. If the exam is unnamed, use a neutral exam slug until it is clarified. Follow the host's output-directory requirements if they differ. Keep one exam record per course/exam; carry relevant prior learning forward with provenance, not by merging unrelated courses.

Read existing records at session start/resume; the save command checks for outside changes itself, so no reread is needed before a save. The first save creates new records from the bundled templates. Update relevant entries in place, append attempt history, and preserve prior student statements. Do not overwrite an existing course directory with blank templates. Record confirmed file paths/URLs, not guesses. Follow a supplied handoff when the old directory is inaccessible, marking its evidence as student-provided.

At the first save, initialize a usable profile from the sources actually inspected; unknown fields and unread resources may remain unresolved until needed. Do not build an exhaustive course register before answering a supported question. Merge pending updates once per save checkpoint, including the next-step pointer. Leave unchanged files untouched. Apply the conflict checks below at each actual write.

If the host cannot write files, maintain state in the current conversation and supply a handoff on request or at the end of a substantial session. Say that the student must bring it to a new conversation. If a previous file is inaccessible, report the limit rather than claim to have loaded it. Do not discover other students' records or search unrelated personal directories.

## Read and save checkpoints

Reuse records and references already loaded in the current conversation. Ordinary explanations, follow-up questions, and short practice use that state plus pending evidence; they need no file refresh. Refresh when starting/resuming, when an external change is known or suspected, and immediately before a commit. If context is missing or uncertain, reload the relevant state rather than assume it is remembered.

Keep a compact pending summary in the current conversation: concept/attempt identity, new evidence and original reasoning or locator, assistance, changed judgment, and next task. Merge repeated evidence without losing distinct attempts. Count each tutoring turn with a meaningful change once, even if it contains several items. Greetings, unchanged explanations, and requests to continue do not increment the count. Default to saving after five such turns since the last successful save; honor an explicit student preference for another interval or immediate saving.

Save earlier when the student asks to save, delete, or correct a record; when a concept's status changes (promotion, demotion, or Recheck); after answering a readiness or "what's left" question; when course/exam scope changes or courses are switched; before delivering a personalized guide, sheet, substantial practice set, or mock exam; after reviewing an imported attempt file; and at an explicit session close or requested handoff. Use pending evidence in feedback immediately while waiting for the checkpoint. At an artifact checkpoint, refresh once, reconcile pending evidence, commit changes if any, and use the reconciled state. Reuse already-current state when there is nothing pending and no reason to suspect changes.

After a successful save, clear only committed pending items and reset the counter. If saving fails, retain pending evidence and say it remains unsaved. During setup, explain briefly that batching leaves recent changes in the current chat until saved, and an abrupt close may leave them unavailable to a new chat. Sessions often end without an explicit close, so status changes and readiness reviews are saved when they happen rather than left for the next batch. Do not promise an automatic close hook or background save. Mention pending status when it matters to a save/resume question, rather than adding a storage notice to every answer.

Keep pending summaries and saved concept entries concise. Preserve long original attempts in their existing files with precise locators; write only meaningful deltas into the merged record, not a chat transcript. Large records may be read by relevant sections for tutoring; every write still checks the hash of the current complete file. Fewer saves or tool calls do not establish a proportional reduction in total tokens or latency; measure those separately before claiming savings.

## Saving

When Python 3.10+ is available, save a checkpoint with one command. Do not read the record first, write fragment files, read it back afterwards, or write your own wrapper script around the helper.

```text
python <skill>/scripts/record_io.py save --dir <study directory> --expected-sha256 <record_sha256 from the last save>
```

Send the changes as JSON on standard input, for example `{"record": {"Concepts": {"mode": "upsert-rows", "rows": ["| T1 | ... |"]}, "Attempt history": {"mode": "upsert-rows", "rows": ["| ... |"]}, "Next session": {"mode": "replace", "text": "- ..."}}, "profile": {"Course scope": {"mode": "upsert-rows", "rows": ["| ... |"]}}}`. Include only sections that changed. Each row is a complete table row with that section's existing columns; a row whose key matches an existing row replaces it, otherwise it is added. `replace` and `append` take `text` for prose or list sections. Leave out `profile` unless scope, sources, or preferences changed. On the first save for a course add `--create` and omit `--expected-sha256`: missing files start from the bundled templates, so do not open or copy the templates yourself.

The reply is one JSON line with `record_sha256` (pass it to the next save), the concept `statuses`, and any `warnings`. Treat it as the verification of the write. Exit status 3 means the record changed since that hash: nothing was written and `current_sections` holds the current text of the sections you sent; merge and resend with `current_sha256`. Any other failure also leaves both files as they were (a two-file save is all-or-nothing); correct the reported row or section name and resend once, then say the save failed and keep the evidence pending rather than retrying in a loop. The helper locks, writes atomically, keeps `<file>.bak`, and writes the profile before the learning record; it does not judge teaching content.

For a structural rewrite, a host without Python, lock recovery, or the full profile field list, read [state-reference.md](state-reference.md). Before reviewing an imported attempt file or browser export, read [state-imports.md](state-imports.md).

## Learning record

At the end of each tutoring turn, review whether anything meaningful changed. Retain only new or changed learning evidence and preferences for the next checkpoint. A greeting, a request to continue, seeing a solution, or an unrelated remark requires no new weakness entry. Do not append empty 'no change' events. A small saved-state note in the reply is enough when a record changed.

Keep one current entry per concept and merge repeated reports rather than duplicating them. Preserve short original reasoning and useful attempt provenance, not full chat transcripts. Capture self-reported difficulty in pending evidence immediately, even before an attempt, labelled self-report; persist it at the next checkpoint. Keep ambiguous grading and missing sources under open questions, not confirmed errors. Update improvement as well as mistakes, and reduce priority when the evidence warrants it. Student requests to remove or correct a record apply to future saved state.

Imported attempt files and browser exports have their own identity, revision, and assistance rules in [state-imports.md](state-imports.md); read them before judging an export.

Track `Quick start shown` when the welcome was actually presented. Reuse it to avoid repeated onboarding during resume. Do not infer account-wide or installation-wide state from one course record. An explicit request for help can show the guide again without clearing learning progress.

Keep stable concept IDs and append meaningful evidence. For each concept record:

- Topic ID and concept.
- Status and current priority, with a short reason.
- Observed mistake or student-reported difficulty, including original reasoning when available.
- A specific corrective rule and a contrasting example when helpful.
- Attempts: date when known, question/activity ID, source/file locator, attempted answer or link, feedback, outcome, assistance level, and answer evidence status. For concept activities, retain meaningful predictions, explanations, constructions, revisions, task conditions, and transfer responses; summarize useful evidence rather than logging every control movement.
- Next retrieval/transfer task and eventual recheck.

Keep summaries separate from original attempts. Student preferences are separate from performance. A student choosing Chinese explanations does not establish their English proficiency. A blank answer is unattempted, not automatically a misconception. Low confidence alone is not a wrong answer.

## Progress labels

| Status | Evidence |
|---|---|
| Unassessed | No useful attempt evidence yet |
| Needs practice | Reviewed error or explicit self-report; say which |
| Improving | Correct after assistance, or one or more correct independent same-structure applications after difficulty |
| Demonstrated | Correct independent explanation/application in at least two distinct contexts, at least one of which is a reviewed transfer task |
| Recheck | A later contradictory attempt or an unresolved inconsistency |

These are operational defaults, not claims of measured mastery. Before promoting to Demonstrated, name the transfer task and what it changed. A transfer task changes the setting or the reasoning demand (a new setting requiring the same principle, or a changed condition where the student must decide whether the method still applies). Same-structure applications, however many, stay Improving: new names, new numbers, or a new story around the same setup and steps are not distinct contexts. If no transfer task has been reviewed, keep Improving and record the transfer check as the next task. When all supporting contexts come from the same session shortly after instruction, Demonstrated is still allowed, but write `Recheck before exam` in its evidence and make a later unaided application (a later session, or after other topics intervene) the next task; a readiness review lists it as due. Immediate success after teaching is weaker evidence of retention. Never change a status only because an answer was displayed or a guide was read. A correct answer without reasoning supplies weaker evidence than a correct explained solution. If an assisted example is later answered unaided, record both events.

Prioritize repeated, well-supported errors and foundational dependencies. Keep uncertain diagnoses tentative. Recheck previously demonstrated concepts periodically when planning extended study, with frequency chosen to fit the exam timeline rather than a fixed scheduling promise. The skill does not schedule notifications by itself.

## Resume and handoff

At a substantial-session close, flush pending changes and save a compact next-step pointer: active course/exam, unresolved source gaps, recent attempts, concepts to revisit, current artifacts, and next activity. Include the current question locator, useful student reasoning, hints/solutions already exposed, and the unresolved step. Use the existing Next session section; long solutions stay in separate files. Include enough context to understand each question without needing inaccessible chat history. Answer files may contain solutions; a student-facing handoff should not accidentally reveal pending practice answers. At a natural review boundary or when a long conversation becomes hard to continue, offer a saved handoff for an optional new chat. Saving a local record does not remove existing messages, disable host compaction, or guarantee access from another chat. Saving frequency and new-chat timing are separate choices; the skill does not automatically create or switch chats.
