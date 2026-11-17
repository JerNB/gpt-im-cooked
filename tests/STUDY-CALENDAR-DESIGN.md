# Multi-course study calendar — design (T010)

Status: **design for human approval; nothing implemented.** Author: cc. Base: `origin/main` at `627bca5` (v2.0.1). Branch: `cc/T010-T011-design`. Decisions marked *(human)* were made by the maintainer in conversation on 2026-11-15/16; everything else is cc's proposal and can be overruled.

## 1. Why

Students in the final-exam window review several courses at once. The hard question is not "what is conditional probability" but "with three exams in two weeks, what do I do on Tuesday evening?" The skill already holds the evidence that answers it — per course, the in-scope topics, their status (Unassessed / Needs practice / Improving / Demonstrated / `Recheck before exam`) and each concept's next task — but nothing turns that evidence into a schedule. Today `practice-and-feedback.md` only says "suggested recheck dates are a study plan, not scheduled notifications".

This is also the lead feature for the next public post (planned 2026-11-20), so it must produce real, screenshot-able output on a synthetic course by Thursday 2026-11-19.

## 2. Goals, non-goals, anti-goals

Goals:

- G1. From the saved records of **several courses** *(human)*, produce one study calendar in which every block names the course, the concrete task, its minutes, and the record entry that motivated it.
- G2. Deliver a **`.ics` file plus a printable, self-contained HTML calendar** by default *(human)*. Where the host exposes a calendar connector, **offer** to write the events directly, and write only after the student confirms *(human)*.
- G3. Place blocks only inside the student's stated **availability windows** *(human, option C)*; if the student declines to give windows, fall back to one all-day "today's review" event per day.
- G4. Courses with a learning record come first *(human)*. After building their tasks, ask once whether to add courses without records; those get time blocks only, labelled as having no record — no invented topic content.
- G5. Layout, slotting and validation are done by a script, not rewritten by the model each time (lesson from the T011 PDF timing: 14.7 min for one hand-built layout).

Non-goals:

- Reminders, notifications, background services, or tracking whether a block was done. No `VALARM` in the `.ics`.
- Reading the student's existing calendar is optional and only through a host connector; the default path needs no account access.
- An "optimal" study schedule. Spacing and ordering rules are stated defaults, not claimed learning science.
- Changing the learning-record or course-profile formats.

Anti-goals (a failure even if the files open):

- A calendar that teaches or tests topics the course materials do not support, or that fills unrecorded courses with guessed topics.
- Ticking a block, or the passage of a planned date, changing any status. Completion is not mastery.
- Writing to the student's real calendar without an explicit yes in the current turn.
- A plan that silently drops tasks because they did not fit; overflow must be reported.

## 3. Constraints

- Python 3.10+ standard library only for the script (same as `record_io.py`, `render_mock_exam.py`). Windows often lacks the IANA time-zone database, so `zoneinfo` cannot be relied on: event times are written as **floating local times** (no `TZID`, no `Z`). Calendars import floating times in the calendar's own zone. This is stated to the student once.
- Student data stays in the student's study directory, never in the package.
- Courses stay separate (`state.md`): the planner **reads** several records but never copies evidence between them or writes a combined record.
- The package build uses an explicit allowlist (`scripts/build_packages.py` `SKILL_FILES`), so every new file must be added there.

## 4. Approaches considered

| | How | Trade-off |
|---|---|---|
| A | Model reads records, writes the timed schedule itself; script only validates and renders | Model does the fiddly packing of minutes into windows across several courses — slow, error-prone, many retries on validation failures |
| **B (chosen)** | **Model decides *what* (tasks, minutes, priority, earliest/latest dates) from records; script decides *when* (packs tasks into windows), validates, writes `.ics` + HTML** | Packing is deterministic and testable; model output is a short task list. Cost: a scheduling algorithm to write and test |
| C | Model writes `.ics`/HTML text directly | Same failure mode as today's hand-built PDFs: long outputs, inconsistent layout, unverifiable |

B mirrors the mock-exam split (model writes JSON content; `render_mock_exam.py` renders and checks).

## 5. Design

### 5.1 Conversation flow

1. **Trigger:** "make a study plan / schedule / calendar for my finals", or the readiness review ("what's left?") offering it once.
2. **Courses:** list the course directories the skill can see (current study directory and sibling course folders containing a course profile). Ask the student to confirm which to include and to supply paths for any it cannot see. Read each course profile (exam date, scope) and learning record (Concepts, Next session). Save any pending evidence for the current course first (existing artifact checkpoint rule).
3. **One combined question** for what records cannot answer: each exam's date and time if missing; weekly study windows; days off (for example Thanksgiving travel); maximum study minutes per day. Offer the fallback: "or I can put one all-day review list on each day instead."
4. **Unrecorded courses** (G4): one line — "Want me to also reserve time for courses without a record here? I'd only block time for them, not plan topics." If yes, ask for exam date and minutes per week per course.
5. Build the plan JSON (§5.2), run the script, read its result line. On overflow, reduce or merge tasks, or tell the student how many minutes do not fit and ask whether to extend windows; never silently drop.
6. Deliver links to `plan.ics` and `calendar.html`, a 3–5 line summary (per course: blocks, minutes, what the first block is), and the import note: import into a **separate calendar** so the whole plan can be removed or replaced at once.
7. **Connector path (optional):** only if the host provides a calendar tool. Before writing: state the target calendar, number of events and date range, and ask. After writing, report what was created. Never modify or delete events the skill did not create. If the host connector can read free/busy, it may be used read-only in step 3 to suggest windows, with the student's consent.
8. Record the plan path under *Artifacts to reopen* in each included course's learning record at its next save. Regenerating after progress changes is offered, not automatic.

### 5.2 Plan input (model-written JSON)

```json
{
  "format": "gpt-im-cooked-study-plan/1",
  "plan_id": "fall-2026-finals",
  "generated_on": "2026-11-16",
  "start": "2026-11-17",
  "availability": {
    "weekly": {"mon": ["19:00-22:00"], "sat": ["14:00-18:00"]},
    "days_off": ["2026-11-25", "2026-11-26", "2026-11-27"],
    "max_minutes_per_day": 180,
    "min_block": 25,
    "max_block": 90
  },
  "courses": [
    {"id": "sta199", "title": "STA 199", "exam": {"start": "2026-12-08T09:00", "end": "2026-12-08T12:00"},
     "record": "STA199/learning-record.md"},
    {"id": "hist101", "title": "HIST 101", "exam": {"start": "2026-12-10T14:00", "end": "2026-12-10T17:00"},
     "record": null, "weekly_minutes": 180}
  ],
  "tasks": [
    {"id": "sta199-t3-recheck", "course": "sta199", "kind": "recheck", "minutes": 30,
     "title": "Conditional probability: unaided recheck", "not_before": "2026-11-19",
     "due": "exam", "priority": 1,
     "basis": "Concepts T3 — Demonstrated, Recheck before exam",
     "details": "Answer one new two-way-table question without notes, then compare with the corrective rule."}
  ]
}
```

- `kind`: `learn` (Unassessed, in scope, teaching notes available), `practice`, `variant` (from a recorded mistake: retry / new setting / changed condition), `recheck`, `mock` (mock exam sitting), `review` (catch-all, unrecorded courses only), `source-gap` (ask for missing notes).
- `basis` must cite a record row (concept/topic ID and status, or attempt ID). Unrecorded-course blocks use `basis: "No learning record"` and `kind: "review"`.
- `due`: `"exam"` or a date; `not_before`: optional date. `priority` 1–3.

Task-derivation defaults (in `references/study-plan.md`, as defaults not science):

| Record state | Default tasks |
|---|---|
| In scope, Unassessed, notes available | `learn` then, on a later day, `practice` |
| In scope, notes missing | one short `source-gap` block (find/ask for the notes) |
| Needs practice with a corrective rule | `variant` (new setting or changed condition) |
| Improving | one transfer-style `practice` |
| Demonstrated + `Recheck before exam` | `recheck`, `not_before` ≥ 1 day after the session that promoted it |
| Demonstrated (no recheck note) | optional light `recheck` near the exam |
| Excluded / unconfirmed scope | nothing |
| Per course | one `mock` sitting 2–4 days before the exam when time allows |

### 5.3 Script: `scripts/plan_study.py`

```text
python plan_study.py PLAN.json --out DIR [--force]   # schedule, validate, write files
python plan_study.py PLAN.json --check               # validate only
```

Packing (deterministic, documented in the script):

1. Expand availability into free slots from `start` to the last exam, removing `days_off`, exam times, and any time on an exam day after the exam starts.
2. Sort tasks by (due date, priority, `not_before`, id). Split a task longer than `max_block` into chunks of at least `min_block`.
3. Place each chunk into the earliest free slot on or after `not_before` that ends before its due point and keeps the day under `max_minutes_per_day`. Prefer not to place two chunks of the same task on the same day.
4. Unrecorded-course `weekly_minutes` become `review` blocks spread over the remaining capacity.
5. Anything unplaced is listed in the result, never dropped.
6. Fallback without windows (G3): the same order fills days up to `max_minutes_per_day` (default 120), and each day becomes one all-day event listing its tasks.

Start times are rounded to 5 minutes.

Output in `DIR`:

- `schedule.json` — placed blocks with stable IDs (`<plan_id>-<task_id>-<n>`) and unplaced tasks.
- `plan.ics` — `VCALENDAR` with `X-WR-CALNAME`, one `VEVENT` per block plus one per exam (`CATEGORIES:Exam`), floating local times, `DESCRIPTION` with details and basis, stable `UID`s, `SEQUENCE` taken from a counter in `schedule.json` when regenerating into the same directory. No `VALARM`. Lines folded and text escaped per RFC 5545.
- `calendar.html` — self-contained (no external assets), week grid on wide screens and a day list on narrow screens; each block shows course (text label plus colour, never colour alone), kind, task, minutes and basis; exams highlighted; header states the generation date, the source records, "completing a block does not change your progress", and the floating-time note. Print CSS: one week per landscape page, empty checkboxes for paper use; no browser-side state.
- One result line on stdout: `OK placed=<n> unplaced=<m> minutes=<x> out=<dir>` or `ERROR <reason>`.

Validation (`--check` and before writing): schema and IDs; dates parse; every task's course exists; `basis` present; no block outside availability, on a day off, overlapping another block, after its due point, or beyond the daily cap; text escaped in HTML; no external URLs in HTML.

### 5.4 Skill text changes

- New `references/study-plan.md`: §5.1 flow, §5.2 task defaults, connector rules, and the honesty rules (no notifications, completion ≠ mastery, unrecorded courses get time only).
- `SKILL.md` §7: one routing sentence pointing to it.
- `review-artifacts.md` output table: new row "Make a study plan / calendar → `.ics` + printable HTML calendar".
- `practice-and-feedback.md`: replace the line about suggested recheck dates with a pointer to the plan.
- `assets/study-plan-example.json`; `scripts/build_packages.py` allowlist; version bump at release time only.

## 6. Verification

- `tests/check_study_plan.py` (no model calls), fixtures under `tests/fixtures/study-plan/`: packing respects windows, days off, daily cap, exam cut-off, `not_before`; overflow reported; UIDs stable across runs; `.ics` parses with a small RFC 5545 reader and round-trips descriptions with commas/semicolons/newlines; HTML self-contained and escaped; malformed JSON gives `ERROR`, not a traceback.
- Manual: import `plan.ics` into one real calendar app and record which app and what was seen; HTML checked at desktop and 375px widths and in print preview. Untested apps are listed as untested.
- Fresh-model run (codex, separate task, **requires human approval of model calls**): two synthetic courses built from existing packets S and P with prepared records containing each status, plus one unrecorded course. Checks: asks the combined question once; derives tasks matching §5.2 with correct `basis`; offers the unrecorded-course option once; uses the script; no writes to any calendar. Reports wall time, tool calls and tokens as descriptive numbers. Screenshots from this run feed T013.

## 7. Done when

- [ ] Human approves this design (scope, defaults, file list).
- [ ] Script, reference, example, routing lines and allowlist entries committed on a `cc/T010-*` branch; `python scripts/build_packages.py` and `python tests/check_distribution.py` pass on a scratch build (release ZIPs not overwritten).
- [ ] `python tests/check_study_plan.py` PASS; existing regressions still pass.
- [ ] Codex review APPROVE; fresh-model run reported with what was and was not verified (connector path, other calendar apps, real students).

## 8. Calls cc made (please check)

1. Floating local times instead of time-zone-aware events (Windows `zoneinfo` gap).
2. Script packs tasks (approach B) rather than the model.
3. One all-day event per day as the fallback when no windows are given.
4. The plan lives in a `plans/<plan_id>/` folder under the student's study root, and each course record only links to it.
5. Mock-exam sitting 2–4 days before each exam and recheck ≥ 1 day after promotion are defaults the student can change.
6. No browser-side checkbox state in the HTML (keeps it simple and avoids implying completion = progress).
