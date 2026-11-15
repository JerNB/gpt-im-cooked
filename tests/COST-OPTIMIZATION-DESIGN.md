# Skill cost optimization — design (T006)

Status: **D1-D5 implemented on `cc/T006-cost-optimization` as arm D; not yet measured with a model.** See "Implementation status" at the end. Author: cc. Base: `cc/T003-skill-revision` at `656b5f7` (skill tree = arm C, `4d102f6`). Evidence: T004 controlled comparison at `79f3676` (`tests/reports/2026-11-14-controlled-comparison/` on `codex/T004-controlled-comparison`).

## 1. Problem

The T003 revision (arm C) fixed three behaviours but costs more than the released skill (arm B), which already costs more than a well-prompted plain model (A2).

| Arm | Input + output tokens, 4 sessions | Mean per session |
|---|---:|---:|
| A1 naive | 1,444,967 | 0.36M |
| A2 strong prompt | 3,298,156 | 0.82M |
| B skill at `97be172` | 4,238,431 | 1.06M |
| C skill at `4d102f6` | 5,539,385 | 1.38M |

C is +31% over B and +68% over A2. Tokens are CLI counters (mostly cached input), not a bill, and how cached tokens draw down a subscription quota was not measured.

## 2. Where the tokens go

Every model call re-reads the whole context, so cost is roughly *calls x context size*. From the per-turn usage deltas and event logs of the selected B and C sessions (call counts are estimated as commands + 1; they are not logged directly):

1. **Saves explain essentially all of C minus B.** Mean input tokens per turn, in thousands:

   | Turn | Event | B | C |
   |---|---|---:|---:|
   | 2 | first error, Needs practice | 56 | 198 |
   | 4 | correct, Improving | 31 | 95 |
   | 5 | correct again | 71 | 105 |
   | 6 | check question posed | 44 | 87 |
   | 7 | transfer answered | 236 | 153 |
   | 10 | readiness review | 49 | 195 |

   C's extra on these turns sums to about 350k per session; the whole C-B gap is about 320k. One save costs 60-150k, i.e. two to three extra calls at a 35-55k context. B does not avoid the cost, it pays once at turn 7.
2. **The model rebuilds a save tool every time.** `record_io.py` offers `read`, `update` (one section per call, needs a fragment file and the current hash) and `commit`. In every inspected C save the model wrote a fresh inline Python wrapper of 2-5k characters that loops over sections, writes fragment files, calls the helper and reads back. Those wrappers failed 7 times in 4 C sessions (3 in B); each failure is another full-context call.
3. **Turn 1 is 22-34% of a session** (about 300k for skill arms): the model reads `SKILL.md`, `state.md`, `concept-tutoring.md`, `practice-and-feedback.md` and three templates, then creates the course profile and learning record before the student has attempted anything. Turn-1 totals are noisy even for A1 (44k-241k), so this estimate is the least reliable.
4. **Standing context.** The skill text read on turn 1 is about 13k tokens and rides along on every later call (a command-free turn costs about 20k for A1 and 31-36k for B/C, rising to about 50k late in the session as record read-backs accumulate). Over thirty-odd calls this is roughly a third of C's total.

## 3. Goals and non-goals

Goals, in priority order:

- G1. Keep every behaviour T004 observed in C: status-change and readiness saves (readiness saved 4/4, no stale resume), same-session recheck marker (4/4), labelled gap offer (4/4), and no new failures on M1-M10.
- G2. Bring mean session cost to **at or below B (1.06M)** on the T004 script; stretch target 0.9M.
- G3. At most one failed tool command per session.

Non-goals: fewer saves (that was the v2.0 saving and it lost evidence in the pilot), weaker source grounding, any change to the learning-record format, shorter student-facing replies, or beating A2 on cost.

## 4. Proposed changes

### D1. One-command save (`record_io.py save`) — largest effect

Add a subcommand that performs a whole checkpoint in one call. The model sends only the changes as JSON on standard input; the script does everything the model's ad-hoc wrappers do today.

```text
python <skill>/scripts/record_io.py save --dir <study dir> [--expected-sha256 <hash from last save>]
```

Standard input:

```json
{"record": {
   "Concepts": {"mode": "upsert-rows", "rows": ["| T1 | ... |"]},
   "Attempt history": {"mode": "upsert-rows", "key_columns": ["Attempt ID / item locator"], "rows": ["| ... |"]},
   "Next session": {"mode": "replace", "text": "- Current activity: ..."}},
 "profile": {"Course scope": {"mode": "upsert-rows", "rows": ["| T3 | ... |"]}},
 "create": {"course": "STAT 110", "exam": "Midterm 1"}}
```

Behaviour:

- Creates `course-profile.md` / `learning-record.md` from the bundled templates when absent (`create`), so no candidate files or template reads are needed.
- Applies all section updates to each file in memory, then one locked atomic write per file with `.bak` and byte verification, profile first and learning record last (the existing ordering rule). Default key columns per known table are built in (Concepts: first column; Attempt history: attempt ID; Import ledger: both identity columns), removing the documented risk of omitting them.
- Conflict handling without an extra call: `--expected-sha256` is optional and comes from the previous save's output. On mismatch nothing is written and the reply contains the current text of only the sections the caller tried to change, so the model can merge and resend.
- Output is one short JSON line: `{"saved": true, "record_sha256": "...", "sections": [...], "statuses": {"T1": "Demonstrated"}}`. No full read-back into context; the script itself verifies placement of rows in the named sections.
- Rejects unknown sections, headings inside fragments, malformed rows, and a Demonstrated row whose evidence cell lacks a `Transfer:` note (optional, see open question 2).
- `read`, `update` and `commit` stay unchanged for compatibility and for structural rewrites.

Skill text: the "Verified record writes" paragraph in `state.md` (about 450 words of procedure) shrinks to a few lines: use `save`, pass the previous hash, on conflict merge and resend, without Python follow the manual fallback in the reference file.

Expected effect: one tool call per save instead of two to four, no generated wrapper code, far fewer failed commands. Rough estimate: -200k to -260k per session.

### D2. No record files before there is evidence

Today the first turn creates both files. Change: keep the scope summary in the reply and in the pending summary; create the files at the first save trigger (first reviewed attempt, self-reported difficulty, or an explicit save). `save --create` makes that one call.

Risk: a session that ends before any attempt leaves no files; the scope mapping is cheap to redo and nothing about the student is lost. Rough estimate: -50k to -100k (noisy).

### D3. Split `state.md`

`state.md` is 4.2k tokens and is read in every session. Keep a core file with what ordinary tutoring needs (storage location, save triggers, the `save` command, progress labels, resume/handoff; target about 1.5k tokens) and move the rest behind explicit pointers:

- `state-imports.md`: import identity, revisions, browser-export assistance rules. Read only when an attempt file is imported.
- `state-reference.md`: profile field list, manual no-Python procedure, `update`/`commit` details, lock recovery.

`scripts/build_packages.py` `SKILL_FILES` and the distribution checks must list the new files. Rough estimate: -80k to -120k.

### D4. First-turn reading list

`SKILL.md` already says "read only what the next activity needs" but the model still reads four references and three templates. Make it concrete in the "Start from a short request" section: for a concept question read the requested material and `concept-tutoring.md`; read `practice-and-feedback.md` only when grading or generating practice; do not open templates (D1 removes the need). Folded into D2/D3 estimates.

### D5. Opening marker once per reply (not cost, same edit pass)

T004 M15: the marker repeats in 22/44 C replies and 11/44 B replies because it is emitted in progress notes and again in the answer. Add one sentence: the marker opens the final answer only, never a progress or tool note.

### Not changed

S1 save triggers, R4, R6, grounding rules, progress labels, the six-column Concepts table, and the default five-turn batch for ordinary evidence.

## 5. Estimated result

| Change | Estimate per session | Confidence |
|---|---:|---|
| D1 one-command save | -200k to -260k | medium: save turns are measured, the per-save call reduction is assumed |
| D1 fewer failed commands | -40k to -60k | medium |
| D2 + D4 lighter first turn | -50k to -100k | low: turn 1 is noisy |
| D3 smaller standing context | -80k to -120k | medium |
| **C 1.38M →** | **about 0.85M-1.0M** | to be measured, not claimed |

## 6. Test plan

1. **Script regression (no model calls).** Extend `tests/check_state_io.py` for `save`: create-from-template, multi-section and two-file saves, default and explicit key columns, no-op save leaves bytes and `.bak` untouched, hash mismatch writes nothing and returns only the requested sections, lock present, malformed row / unknown section / heading in fragment rejected with bytes unchanged, write failure leaves the original, output is a single JSON line. Existing `read`/`update`/`commit` assertions stay.
2. **Package checks.** `validate_package.py`, rebuilt ZIPs under a new version only, `check_distribution.py` (currently failing on main for the v2.0.0 archives; fix by building the new version, never by overwriting v2.0.0).
3. **Smoke run before any batch.** Two turns of one skill session on packet S to confirm materials are read, `save` is used, and no global skill is touched. T004 lost 146 calls to defects a two-turn smoke run would have caught.
4. **Behaviour and cost comparison (real model calls, human approval, Codex runs it).** New arm **D** = optimized skill. Run C and D interleaved, packets S and P, two replicates: 8 sessions, 88 calls, same runner, script, rubric-v2 and model as T004. Rerun C rather than reuse T004's C so both arms share quota windows.
   - Acceptance, counts only: D saves on every status-change turn and after the readiness review in 4/4; resume from stale state 0/4; recheck marker 4/4; labelled gap offer 4/4; M1-M10 no worse than concurrent C; failed commands at most 4 over 4 sessions; mean D tokens at or below 1.06M and below concurrent C in at least 3 of 4 matched pairs.
   - Report per-turn tokens for the save turns (2, 4, 5, 7, 10) so the D1 effect is visible separately from D2-D4.
   - Blind scoring by Codex, cross-review by cc, as in T004.
5. **Not measured by this plan:** learning gains, real students, other models, mock exams and guides, quota or billing impact.

## 7. Risks and open questions

1. **Quoting JSON through a Windows shell.** Standard input avoids command-line quoting; the model already pipes here-strings to Python. If that proves fragile, add `--changes-file`, at the cost of one more tool call.
2. **Should `save` enforce the Demonstrated evidence note?** It would make the transfer rule checkable by the script (review item R2) but could reject legitimate legacy rows. Proposal: warn in the output, do not reject, in this revision.
3. **Hosts without Python** keep the manual procedure; it moves to the reference file and is not optimized.
4. **Estimates are from 4 sessions per arm with wide spread** (B ranged 0.70M-1.49M). The plan may land short of G2; the comparison, not this table, decides.
5. **Dropping the read-back** removes the model's own visual check of the record. The script's structural verification replaces it; semantic errors in a row are caught only at the next resume, as today.

## 8. Sequencing

1. Human approves scope (which of D1-D5).
2. cc: `save` subcommand + regression tests (own branch, locks on `scripts/record_io.py`, `tests/check_state_io.py`).
3. cc: skill text (D1 wording, D2, D3 split, D4, D5) + allowlist; freeze as arm D.
4. Codex: source review, then the C-vs-D comparison under a new task card.
5. Version bump and new ZIPs only after cross-review; v2.0.0 archives untouched.

## 9. Implementation status (2026-11-14)

Implemented as designed, with these differences from the estimates above:

- **D1** `record_io.py save`: JSON on standard input or `--changes`; `--create` starts missing files from the templates; all changes are validated in memory before any write, so a bad change to one file never lets the other file change; exit status 3 with `current_sections` on a stale hash; one JSON result line with hashes, concept statuses and a non-blocking warning for a Demonstrated row that names no transfer task (open question 2: warn, do not reject). `read`, `update` and `commit` are unchanged; `update` now shares the section-apply code.
- **D2** records are created by the first save, not on a first explanation.
- **D3** `state.md` is split into `state.md` (core), `state-imports.md` and `state-reference.md`; moved paragraphs are verbatim. **The core file is about 3.2k tokens, not the 1.5k target**: the save triggers, learning-record rules, progress labels and handoff rules were kept whole rather than condensed, to avoid changing behaviour in the same revision. The D3 saving should be expected nearer -40k than -100k per session.
- **D4** explicit reading list in `SKILL.md` "Start from a short request"; **D5** marker once per reply.
- Package allowlist lists the two new reference files. No version bump and no ZIP rebuild: `check_distribution.py` still fails against the v2.0.0 archives, as on main.

Verified without model calls: `check_state_io.py` (extended for `save`: templates, default key columns, no-op, conflict merge data, all-or-nothing across both files, foreign lock, CLI exit codes), `validate_package.py`, and the eight other regression scripts. **Not verified:** that a model actually uses `save` in one call, the token effect of any change, and the absence of behaviour regressions. Those are the purpose of the C-versus-D comparison in section 6.

## 10. Review fixes (2026-11-15)

Codex source review of `3edde3b` (reviews/T006.md) found one blocker and two wording conflicts, fixed in the next commit:

- **B1 two-file atomicity.** `save` published the profile before attempting the learning record, so a foreign lock or failed write on the record left a half-saved checkpoint. `publish_checkpoint` now takes every lock first, rechecks hashes under the locks, and on a later failure restores each already-published file and its previous `.bak` (or removes a newly created file). Regression cases: foreign record lock with a valid two-file payload, failed replacement of the second file, a record edited between planning and publishing, and the same failure while creating a new course.
- **M1** imported saves now verify placement from the save result instead of a read-back; a read-back is required only for manual or structural writes.
- **N1** the reading list includes extracting patterns from papers and instructor review questions.
