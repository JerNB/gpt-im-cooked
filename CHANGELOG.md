# Changelog

## v2.0.2 — Finals: study calendar and exam cheat sheets — November 19, 2026

**Plan several courses on one calendar, and get an exam cheat sheet as a real PDF without installing anything.**

Download the [standalone skill](docs/downloads/gpt-im-cooked-skill-v2.0.2.zip) or [plugin package](docs/downloads/gpt-im-cooked-plugin-v2.0.2.zip) ([checksums](docs/downloads/SHA256SUMS-v2.0.2.txt)). Earlier archives, including v2.0.1, remain available unchanged. Skill and plugin identities are preserved; existing course directories and learning records work without migration.

### Added: a study calendar across courses

- Ask for a study plan or calendar and the tutor reads each included course's learning record. It derives tasks from what is recorded (`references/study-plan.md`):
  - Needs practice → a changed-condition variant.
  - Improving → one transfer practice.
  - Demonstrated with a recheck note → an unaided recheck.
  - In scope but teaching notes missing → a short block to find them.
  - Each course → one mock sitting 2–4 days before its exam.

  Every task cites the record row it came from.
- `scripts/plan_study.py` (standard library) places the tasks into the study windows you give once: weekly times, days off and a daily cap. It writes `plan.ics` and a printable `calendar.html`. Without windows it makes one all-day review list per day.
  - The `.ics` has stable event IDs, so a regenerated plan updates rather than duplicates. Its times are floating (no time zone) and it sends no reminders.
  - Courses without a record get labelled review blocks only.
  - An exam with no end time is assumed to last 3 hours, and both files say so.
  - Nothing is written to a connected calendar without an explicit yes in the conversation.

### Added: exam cheat sheets and study guides from a template renderer

- **One question, then a draft.** A guide or cheat-sheet request gets a single question ("Is this a cheat sheet you'll bring into the exam? How many sheets, and one- or two-sided?"). The tutor then ends the turn and waits. If the answer is unknown, it makes one two-sided sheet marked *exam use unconfirmed*. There is no content plan to approve before the first draft.
- **Content rules.** The rules come from one student's revision history, for example: tier each topic as worked, cue or omit; use one running example per cluster; stage multi-step conversions; make the important things prominent; no generic reminders; empty space is allowed; a student's "leave it off" is not an instructor exclusion.
- **Rendering.** The tutor writes content only (JSON), and `scripts/render_sheet.py` lays it out.
  - It uses ReportLab when installed, and otherwise the new built-in writer `scripts/sheet_pdf.py`. That writer uses only the standard library, embeds subsets of the computer's TrueType fonts, keeps text extractable and works inside the Codex sandbox.
  - A browser engine (`--engine browser`) is available on request.
  - With no usable engine, it writes printable HTML and gives the exact install question to ask.
- **Fitting.**
  - It picks the most spacious layout that fits the allowed pages (9–11 pt body).
  - An exam sheet with spare room grows to 12–14 pt without adding pages.
  - Overflow is reported per section, never fixed by shrinking below the minimum.
  - Table and label columns are at least as wide as their longest word, measured in the font each word is printed in.
  - Characters the fonts cannot draw are reported before anything is written.
- **Revisions.** Rounds are kept as `-v<round>`. Standing constraints such as "no new information" carry over. Lasting preferences are saved in a new `Reference-sheet preferences` section of the course profile and reused in later sessions.

### Changed

- When the tutor needs your answer (calendar availability, sheet allowance), it asks in the reply and ends the turn instead of continuing with a default.
- The offer to add courses without a record is made once, at the end of the plan delivery.
- `record_io.py save` accepts the optional `Reference-sheet preferences` section.

### Evidence for this release

Exploratory, synthetic courses, one scripted student, one smaller model (`gpt-6-luna`, Codex CLI 0.162.1). Earlier benchmarks used `gpt-6.1-sol`, so numbers are not comparable across those reports. Tokens are CLI counters, not billing.

- **Calendar** ([pilot report](tests/reports/2026-11-18-feature-pilot/REPORT.md), 2 sessions).
  - Tasks derived per the table: 2/2. Every task cited a record row: 12/12 per session.
  - `plan_study.py` ran and the `.ics` and HTML were delivered: 2/2. No calendar writes.
  - Gaps found there: the tutor did not wait for the availability answer (1/2), made the unrecorded-course offer 0/2 times, and in one session invented an exam end time. The wording and the 3-hour default above respond to these and were **not** re-run with a model.
- **PDF path.**
  - In that pilot the then-new renderer made 0/2 PDFs on a host without ReportLab.
  - A browser-print fallback also produced none inside the Codex Windows sandbox ([rerun](tests/reports/2026-11-19-sheet-rerun/REPORT.md)).
  - With the built-in writer, 2/2 sessions produced their sheets inside the sandbox ([native rerun](tests/reports/2026-11-19-sheet-native/REPORT.md)).
- **v2.0.1 vs this release** ([comparison](tests/reports/2026-11-19-sheet-compare/REPORT.md), 3 sessions per arm, the same 4 scripted turns).
  - Allowance question asked first: 3/3 vs 0/3. Sheets made by the renderer: 3/3. Preferences saved: 3/3; v2.0.1 has no such feature.
  - Means for a fresh-session sheet: 361,660 → 187,671 processed tokens (−48%) and 106.2 → 65.4 s (−38%). The whole 4-turn session: −27% tokens and −17% time.
  - Per-session spread is wide and ranges overlap.
  - On that host v2.0.1 made its PDFs with PyMuPDF, which happened to be installed.
- Not measured: sheet content quality (no blind scoring), learning gains, real students, other models, macOS and Linux, PDF viewers other than PDFium, paper printing, calendar-app imports and connector writes.

## v2.0.1 — Steadier progress records — November 15, 2026

**Progress is saved when it changes, "Demonstrated" asks for a later recheck, and saving takes one step.**

Download the [standalone skill](docs/downloads/gpt-im-cooked-skill-v2.0.1.zip) or [plugin package](docs/downloads/gpt-im-cooked-plugin-v2.0.1.zip) ([checksums](docs/downloads/SHA256SUMS-v2.0.1.txt)). Earlier archives, including v2.0.0, remain available unchanged. Skill and plugin identities are preserved; existing course directories and learning records work without migration.

### Changed: saving no longer waits for the five-turn batch when progress changes

A concept's status change (Needs practice, Improving, Demonstrated, Recheck) and an answer to "am I ready / what's left" are now saved in the same turn. The five-meaningful-turn default still applies to other evidence. In an earlier limited pilot ([report](tests/reports/2026-11-13-controlled-pilot/REPORT.md): one scripted session per arm, author scoring, plain-arm skill isolation not enforced), the previous version held four turns of evidence unsaved and a new session resumed from stale state. If a session ends without an explicit "save and close", same-turn saving keeps those changes.

### Changed: Demonstrated from one sitting carries a recheck

Demonstrated still requires a reviewed transfer task. When all of that evidence comes from the same session shortly after instruction, the record now says `Recheck before exam`, and the next task is a later unaided application. A readiness review lists it as due.

### Added: an honest path when your notes don't cover a topic

When a topic is in scope but its teaching notes are missing, the tutor still asks for the excerpt, and now also offers once a general explanation labelled **not from your course materials — check it against your notes**. It is given only if you accept, and never counts as course content or progress evidence.

### Added: one-command saves, and lighter loading

- `record_io.py save` applies a whole checkpoint to the course profile and learning record in one call, from JSON on standard input. It creates missing files from the bundled templates, uses the identity columns of Attempt history and Import ledger as row keys, and prints one result line. A two-file save takes every lock first, rechecks hashes under the locks, and restores already-written files if a later write fails; it is not a crash-durable transaction, and if restoring itself fails it reports which files need inspection. On a stale hash nothing is written and the current text of the affected sections is returned for merging. `read`, `update` and `commit` are unchanged.
- Record files are created at the first save that has evidence, not on a first explanation.
- `references/state.md` is split: imported-attempt rules move to `state-imports.md`, manual and structural procedures to `state-reference.md` (rules preserved; the imported-save verification wording now refers to the save result instead of a read-back). `SKILL.md` names which references a turn needs.
- The opening marker appears once per reply, never in progress notes.

### Evidence for this release

Exploratory, synthetic, scripted-student comparisons with one model (`gpt-6.1-sol`, Codex CLI 0.162.1); four sessions per arm; counts, not rates. Tokens are CLI counters, not billing.

- **Against a plain model** ([T004 report](tests/reports/2026-11-14-controlled-comparison/REPORT.md), 16 sessions). This compared earlier skill versions, not v2.0.1. The skill at `97be172` (v2.0.0 plus the changes listed below as previously unreleased) matched a plain model given a strong one-paragraph prompt on overconfidence, readiness honesty, grounding and scope checks, and wrote a genuine transfer check in 4/4 sessions versus 2/4 or 3/4 for the strong prompt, depending on one disputed adjudication. The save/recheck/gap revision scored 3 passes and 1 unclear on that check. The strong prompt used fewer tokens than either. v2.0.1 itself was not paired with a plain model.
- **The behaviour changes** (same report, previous version vs. the save/recheck/gap revision): readiness review saved in the record 0/4 vs. 4/4; resume from stale state 1/4 vs. 0/4; recheck marker 0/3 vs. 4/4; labelled gap offer 1/4 vs. 4/4. That revision cost about 31% more tokens.
- **The cost changes** ([T007 report](tests/reports/2026-11-14-cost-comparison/REPORT.md), 8 sessions): this release used 3,364,701 input-plus-output tokens over four sessions against 4,032,907 for the save/recheck/gap revision without the cost changes, lower in 4 of 4 matched pairs. Behaviour counts tied on every rubric check under the selected adjudications; on the transfer check both arms scored 3 passes and 1 unclear, and one v2.0.1 pass is disputed (a secondary reviewer kept it unclear). The repeated opening marker went from 15/44 replies to 0/44. Every save used the one-command `save` (20/20, no failures). The first-turn reading list was not followed: `state.md` was still read on turn 1 in 4/4 sessions.
- The same frozen skill cost 27% less in the T007 run than in the T004 run, so comparisons across runs are weak; the within-run comparison is the evidence. Scoring was by model reviewers on masked, shuffled sessions, but record formats allow the arm to be inferred and the final compilation and adjudication were not blind. The accepted general-explanation path and a delayed unaided recheck were not exercised; the rules above describe intended behaviour, and only the listed counts were measured. Learning gains, real students, other models, mock-exam and guide workloads, and billing were not measured. Two strict checks (worked-example values overlapping a practice key, and resume replies reciting every open item) failed in every arm and remain open.

### Also in this release (previously listed as unreleased)

- **Mock exams render from a tested template.** The tutor writes the questions and checked key as JSON; `scripts/render_mock_exam.py` fills `assets/mock-exam-template.html` and writes a worksheet plus a separate key. The template carries the answer-status, revisit, print, and schema 1.0 export/exposure logic that previously had to be rebuilt per exam. The script checks structure only (IDs, answer counts, per-option explanations, evidence labels, unsafe SVG, key text leaking into the worksheet); it does not judge academic correctness. Covered by `tests/check_mock_render.py` and `tests/check_mock_template.cjs`, plus one manual browser check of the example at desktop and 375px widths. Not yet exercised by a fresh-model run.
  - Review fixes before release: the SVG check now also catches `<svg/onload=…>`, entity-encoded `javascript:`, `@import`, and embedded documents; image sources reject upper-case/space-prefixed network URLs and non-image `data:` URIs; malformed JSON shapes produce validation errors instead of a traceback. Output file names include `artifact_version`, so a new paper version no longer overwrites a delivered one. In the worksheet, starting a retry no longer clears the unsaved-attempt warning, and middle-clicking the key link is recorded as key access (opening the key file directly still is not detectable).
  - Second review: SVG URL attributes are entity-decoded and stripped of tab/newline/control characters before the scheme check (closes `java&#x09;script:`); question and shared IDs that collide with template or derived element IDs (e.g. `artifact-data`, `q1-answer`) are rejected; opening the key after an export now triggers the unsaved-change warning.
  - Third review: element IDs are checked in the final worksheet and key HTML, so an `id` inside author-supplied SVG (e.g. `<svg id="artifact-data">`) or the same marker id in two figures is rejected instead of breaking page initialisation.
  - Fourth review: tag attributes are read with the standard-library `HTMLParser` instead of a regular expression, so a quoted `>` (e.g. `data-label="x > y"`) no longer hides a following `id`, event handler, or link from the checks.
- **Section-level record updates.** `record_io.py` gains `read --section` and `update --section … --mode replace|append|upsert-rows [--key-column HEADER]`, so a save can send only the changed rows or section instead of rewriting the whole learning record. The whole-file hash check, lock, `.bak` backup, and write verification are unchanged; other sections stay byte-identical, and fragments cannot add or remove headings (ATX, indented, or underlined). Code fences are parsed by CommonMark rules; a record or fragment with an unclosed fence is refused, and a write is refused if the resulting section list would change. `--key-column` is repeatable for composite keys; Import ledger rows key on artifact and attempt ID together. Covered by new cases in `tests/check_state_io.py` against the shipped record template. Whether this lowers tokens or save errors in real sessions is not measured.
- Progress labels: Demonstrated now requires a named, reviewed transfer task. In the T004 comparison no skill session claimed mastery after two same-structure successes (8/8).

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

