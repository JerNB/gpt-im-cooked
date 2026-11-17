# Multi-course Study Calendar Implementation Plan (T010)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn several courses' saved learning records into a study calendar delivered as `.ics` plus a printable self-contained HTML page.

**Architecture:** The model writes a short plan JSON (what to study, minutes, priority, date bounds, record basis). A stdlib script `plan_study.py` validates it, packs tasks into the student's availability windows, and writes `schedule.json`, `plan.ics` and `calendar.html`. A new reference tells the model how to derive tasks and talk to the student.

**Tech Stack:** Python 3.10+ standard library only; plain-script tests in the repo's style (`python tests/check_*.py`, asserts, prints `PASS`).

**Spec:** `tests/STUDY-CALENDAR-DESIGN.md` (approved by human 2026-11-16).

## Global Constraints

- Python 3.10+ standard library only; no `zoneinfo` (Windows lacks tzdata).
- Event times are floating local times: no `TZID`, no trailing `Z`.
- No `VALARM` anywhere; no browser-side state in the HTML; no external URLs/assets in the HTML.
- Every task has a `basis`; unrecorded courses only produce `kind: "review"` blocks with `basis: "No learning record"`.
- Unplaced tasks are reported, never dropped.
- Result line on stdout: `OK placed=<n> unplaced=<m> minutes=<x> out=<dir>` or `ERROR <reason>`; no Python traceback for bad input.
- Package files are allowlisted in `scripts/build_packages.py` `SKILL_FILES`; release ZIPs in `docs/downloads/` are not rebuilt in this task.
- Repo content is English.
- Lock before editing: claim implementation locks in `.collab/LOCKS.md` for every path below (protocol §2 rule 2).

## Review Focus

1. A day that is both in `days_off` and has a weekly window → no blocks that day (covered in Task 2 `test_days_off`).
2. A course whose exam is earlier than `start` or with no free time before it → its tasks all appear in `unplaced`, run still exits `OK` (Task 2 `test_no_time_before_exam`).
3. Task text containing `<script>`, `&`, commas, semicolons and newlines → escaped in HTML and ICS (Tasks 3, 4).
4. Regenerating into the same folder → same UIDs, `SEQUENCE` incremented, needs `--force` (Task 5 `test_regenerate`).
5. Windows that cross midnight (`"22:00-01:00"`) → rejected with a clear error rather than mis-scheduled (Task 1 `test_rejects_bad_window`).

---

### Task 1: Plan format and validation

**Files:**
- Create: `plugins/gpt-im-cooked/skills/gpt-im-cooked/scripts/plan_study.py`
- Create: `plugins/gpt-im-cooked/skills/gpt-im-cooked/assets/study-plan-example.json`
- Test: `tests/check_study_plan.py`

**Interfaces:**
- Produces: `class PlanError(ValueError)`; `load_plan(data: dict) -> dict` (returns a normalised copy: dates as `datetime.date`, exam start/end as naive `datetime`, windows as `(weekday:int, start_min:int, end_min:int)` tuples, defaults filled: `max_minutes_per_day=120`, `min_block=25`, `max_block=90`); constants `FORMAT = 'gpt-im-cooked-study-plan/1'`, `KINDS = {'learn','practice','variant','recheck','mock','review','source-gap'}`.

The example JSON is the spec §5.2 example extended to two recorded courses (`sta199`, `cs201`) and one unrecorded (`hist101`), with at least one task of each kind except `review`, availability `mon`–`fri` `19:00-22:00`, `sat`/`sun` `14:00-18:00`, three days off.

- [ ] **Step 1: Write failing tests** in `tests/check_study_plan.py` (same scaffold as `tests/check_mock_render.py`: import the script from the skill's `scripts/`, `sys.dont_write_bytecode = True`, a `rejects(mutate, expected)` helper, `check()` called under `if __name__ == '__main__'`, print `PASS`):
  - `test_example_valid`: `load_plan(EXAMPLE)` returns; `plan['availability']['max_minutes_per_day'] == 180`.
  - `test_rejects_*` each asserting the substring in `PlanError`: wrong `format` → `"format"`; task without `basis` → `"basis"`; task `course` not in courses → `"unknown course"`; `kind` `"cram"` → `"kind"`; `minutes` 0 → `"minutes"`; window `"22:00-19:00"` and `"22:00-01:00"` → `"window"`; `not_before` after the course exam → `"not_before"`; duplicate task id → `"duplicate"`; unrecorded course task with kind other than `review` → `"no learning record"`; `min_block > max_block` → `"block"`.
- [ ] **Step 2:** Run `python tests/check_study_plan.py` → fails on import (`plan_study` missing).
- [ ] **Step 3:** Implement `PlanError`, `load_plan` and the example JSON.
- [ ] **Step 4:** Run `python tests/check_study_plan.py` → `PASS`.
- [ ] **Step 5:** Commit `feat: study-plan format and validation [T010]`.

### Task 2: Free slots and packing

**Files:**
- Modify: `.../scripts/plan_study.py`
- Test: `tests/check_study_plan.py`

**Interfaces:**
- Consumes: `load_plan`.
- Produces: `schedule(plan: dict) -> dict` returning `{'blocks': [block], 'unplaced': [{'task': id, 'minutes': int, 'reason': str}], 'all_day': bool}` where `block = {'id': f'{plan_id}-{task_id}-{n}', 'task': task_id, 'course': course_id, 'kind': str, 'title': str, 'start': datetime, 'end': datetime, 'basis': str, 'details': str}`; for `all_day` plans blocks have `start`/`end` as `date` and one entry per task chunk grouped by day.

Algorithm (spec §5.3, in this order): expand windows from `start` to the last exam, removing `days_off`, exam intervals and the rest of each exam day after its exam starts; sort tasks by `(due_date, priority, not_before or start, id)`; split tasks longer than `max_block` into chunks `>= min_block` (last chunk merged into the previous one if it would be shorter); place each chunk in the earliest slot `>= not_before` that ends before its due point, keeps the day `<= max_minutes_per_day`, and does not hold another chunk of the same task that day unless no other day fits; start times rounded up to 5 minutes; then spread each unrecorded course's `weekly_minutes` as `review` blocks per ISO week over remaining capacity; if `weekly` is empty, fill days up to the cap with the same order and mark `all_day: True`.

- [ ] **Step 1: Failing tests:**
  - `test_within_windows`: every block lies inside a window of its weekday.
  - `test_days_off`: no block on any `days_off` date (include one that also has a window).
  - `test_daily_cap`: per-day minutes `<= max_minutes_per_day`.
  - `test_before_exam`: every block of a course ends `<=` its exam start; no block on an exam day after the exam starts.
  - `test_not_before`: recheck task blocks start on/after its `not_before`.
  - `test_chunking`: a 200-minute task with `max_block` 90 / `min_block` 25 → chunk lengths each in `[25, 90]`, total 200, on different days.
  - `test_no_overlap` across all blocks.
  - `test_overflow`: shrink windows so a task cannot fit → it appears in `unplaced` with its minutes; nothing else lost (`placed + unplaced minutes == total task minutes`).
  - `test_no_time_before_exam`: exam before `start` → all that course's tasks unplaced, no exception.
  - `test_unrecorded_review`: `hist101` gets only `review` blocks, `basis == 'No learning record'`, about `weekly_minutes` per week (within one `min_block`).
  - `test_all_day_fallback`: empty `weekly` → `all_day` true, every block a `date`, per-day minutes `<= 120`.
  - `test_deterministic`: two runs give identical results; start minutes divisible by 5.
- [ ] **Step 2:** Run → FAIL (`schedule` missing).
- [ ] **Step 3:** Implement `schedule`.
- [ ] **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Commit `feat: pack study tasks into availability windows [T010]`.

### Task 3: ICS output

**Files:**
- Modify: `.../scripts/plan_study.py`
- Test: `tests/check_study_plan.py`

**Interfaces:**
- Consumes: `schedule`.
- Produces: `to_ics(plan: dict, result: dict, sequence: int, stamp: datetime) -> str`.

RFC 5545: `CRLF` line ends; lines folded at 75 octets (UTF-8 safe); `TEXT` escaping of `\`, `;`, `,`, newline; `PRODID:-//GPT I'm Cooked//study-plan//EN`; `X-WR-CALNAME:<plan_id> study plan (GPT, I'm Cooked)`; per block `UID:<block id>@gpt-im-cooked`, `DTSTAMP` (UTC, the only `Z` value), `DTSTART`/`DTEND` floating (`YYYYMMDDTHHMMSS`) or `;VALUE=DATE` for all-day, `SUMMARY:<course title> · <title>`, `DESCRIPTION:<details>\n\nBasis: <basis>\nCompleting this block does not change your recorded progress.`, `CATEGORIES:<kind>`, `SEQUENCE:<sequence>`; one exam event per course with `CATEGORIES:Exam`.

- [ ] **Step 1: Failing tests** (write a ~20-line unfolding parser in the test file):
  - `test_ics_parses`: counts of `VEVENT` == blocks + exams; every `UID` unique.
  - `test_ics_floating`: no `TZID`; only `DTSTAMP` values end with `Z`.
  - `test_ics_no_alarm`: `'VALARM' not in text`.
  - `test_ics_escaping`: task title `'A, B; C\nD <script>'` round-trips through the parser to the same string.
  - `test_ics_folding`: every physical line `<= 75` octets; a 300-char description unfolds intact, including multibyte characters.
  - `test_ics_all_day`: fallback plan emits `DTSTART;VALUE=DATE:`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implement. **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Commit `feat: write study plan as iCalendar [T010]`.

### Task 4: Printable HTML calendar

**Files:**
- Create: `.../assets/study-plan-template.html` (CSS + `{{TITLE}}`, `{{NOTES}}`, `{{WEEKS}}`, `{{LEGEND}}` placeholders; no script)
- Modify: `.../scripts/plan_study.py`
- Test: `tests/check_study_plan.py`

**Interfaces:**
- Produces: `to_html(plan: dict, result: dict, generated_on: date) -> str`.

Layout per spec §5.3: week grid (7 columns) above 768px, day list below; each block shows course title text, kind, title, minutes and basis; per-course colour from a fixed 6-colour list plus the course title in text; exams visually distinct and labelled "Exam"; header notes: generation date, list of source records, "Completing a block does not change your recorded progress.", the floating-time sentence; unplaced tasks listed in a visible "Did not fit" box; `@media print`: landscape, one week per page, an empty checkbox before each block.

- [ ] **Step 1: Failing tests:**
  - `test_html_self_contained`: no `http://`, `https://`, `src=`, `<link`, `<script` in output.
  - `test_html_escaping`: title `<script>alert(1)</script> & co` appears only escaped.
  - `test_html_blocks`: each block id appears once as `data-block="<id>"`; each course title appears in the legend.
  - `test_html_notes`: contains `does not change your recorded progress` and the generation date.
  - `test_html_unplaced`: overflow fixture shows the unplaced task title under "Did not fit".
  - `test_html_no_placeholders`: no `{{`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implement template + `to_html`. **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Manually open the example output at desktop width, 375px and print preview; note what was seen in the commit body.
- [ ] **Step 6:** Commit `feat: printable HTML study calendar [T010]`.

### Task 5: Command line

**Files:**
- Modify: `.../scripts/plan_study.py`
- Test: `tests/check_study_plan.py`

**Interfaces:**
- Produces: `main(argv: list[str] | None = None) -> int`; usage `plan_study.py PLAN.json --out DIR [--force]` and `plan_study.py PLAN.json --check`. Exit `0` on `OK` (including unplaced > 0), `1` on `ERROR`. Writes `schedule.json` (`{'format', 'sequence', 'generated_on', 'blocks', 'unplaced'}` with ISO strings), `plan.ics`, `calendar.html`. If `DIR/schedule.json` exists: without `--force` → `ERROR output exists; pass --force to regenerate`; with `--force` → `sequence = old + 1`.

- [ ] **Step 1: Failing tests** (run via `subprocess` with `sys.executable`):
  - `test_cli_ok`: example → exit 0, stdout matches `^OK placed=\d+ unplaced=\d+ minutes=\d+ out=`, three files exist.
  - `test_cli_check`: `--check` → exit 0 and writes nothing.
  - `test_cli_errors`: invalid JSON text and an invalid plan → exit 1, stdout starts `ERROR`, stderr has no `Traceback`.
  - `test_regenerate`: second run without `--force` → exit 1; with `--force` → same set of UIDs, `SEQUENCE:1`.
- [ ] **Step 2:** Run → FAIL. **Step 3:** Implement. **Step 4:** Run → `PASS`.
- [ ] **Step 5:** Commit `feat: plan_study command line [T010]`.

### Task 6: Skill instructions and packaging

**Files:**
- Create: `.../references/study-plan.md`
- Modify: `.../SKILL.md` (§7, one sentence), `.../references/review-artifacts.md` (output table row), `.../references/practice-and-feedback.md` (the "Suggested recheck dates…" sentence → pointer to the plan), `scripts/build_packages.py` (`SKILL_FILES` += `references/study-plan.md`, `scripts/plan_study.py`, `assets/study-plan-template.html`, `assets/study-plan-example.json`)

`study-plan.md` contents, from spec §5.1/§5.2: trigger; course discovery (current study directory and sibling folders with a course profile; ask to confirm; ask for paths it cannot see); save pending evidence first; the one combined question (exam date/time if missing, weekly windows, days off, max minutes per day) with the all-day fallback offered; the task-derivation table verbatim; the one-line unrecorded-course offer; how to run the script and react to `unplaced`; delivery summary and "import into a separate calendar"; connector rules (offer only if a host calendar tool exists, state calendar/count/date range, write only after yes, never modify events it did not create, read-only free/busy only with consent); save the plan path under *Artifacts to reopen*; regeneration is offered, not automatic; honesty lines (no notifications, completion ≠ mastery, defaults not science, floating-time note).

- [ ] **Step 1:** Write the files above.
- [ ] **Step 2:** In an isolated copy (`git archive HEAD` + working changes, excluding untracked unrelated files) run `python tests/validate_package.py` → `PASS`.
- [ ] **Step 3:** `python scripts/build_packages.py --output <scratch>` → succeeds; list the skill ZIP and confirm the four new files are inside. Do not write to `docs/downloads/`; `tests/check_distribution.py` is expected to fail until a release rebuild and is not run here.
- [ ] **Step 4:** Run every existing regression listed in `CLAUDE.md` "Development commands" except `check_distribution.py` and the benchmark → all `PASS`.
- [ ] **Step 5:** Manual: import the example `plan.ics` into one real calendar app (a separate calendar); record the app, whether times, titles, descriptions and the exam events appear correctly, and whether re-importing the `--force` output duplicated events. List other apps as untested.
- [ ] **Step 6:** Commit `feat: study calendar instructions and packaging [T010]`.

### Task 7: Handoff

- [ ] **Step 1:** Write `.collab/handoff/T010.md` (what changed, commands run with results, not verified: calendar-app import beyond the one app tried, connector path, fresh-model behaviour). Update `.collab/TASKS.md` T010 status to REVIEW, release locks, append `.collab/LOG.md`.
- [ ] **Step 2:** Push the branch only when the human asks.
