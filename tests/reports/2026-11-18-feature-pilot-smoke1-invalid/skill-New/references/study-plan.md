# Study plan and calendar

Use this when the student asks for a study plan, schedule, or calendar (for example "plan my finals"), or accepts the offer made once after a readiness review. The plan can cover several courses. You decide **what** to study from the records; `scripts/plan_study.py` decides **when**, checks the result, and writes the files.

## Gather

1. Save pending evidence for the current course first (artifact checkpoint in [state.md](state.md)).
2. Find courses: the current study directory and sibling folders that contain a course profile. Ask the student to confirm which to include and to give paths for any you cannot see. Read each included course profile (exam date, scope) and learning record (Concepts, Next session). Read other courses' records only; never copy evidence between courses or write a combined record.
3. Ask **one** combined question for what the records do not answer: each exam's date and time if missing, the weekly times the student can study (for example weekday evenings 19:00-22:00, weekends 14:00-18:00), days off, and a maximum number of study minutes per day. Offer the alternative in the same message: "or I can put one all-day review list on each day instead."
4. After planning the recorded courses, ask once: "Want me to also reserve time for courses without a record here? I'd only block time for them, not plan topics." If yes, ask for each such course's exam date and time and minutes per week.

## Write the plan

Copy the shape of [assets/study-plan-example.json](../assets/study-plan-example.json). Every task needs a `basis` that cites a record row: a concept or topic ID with its status, or an attempt ID. Courses without a record have `"record": null` and `weekly_minutes`; do not write tasks for them, the script adds labelled review blocks.

Default tasks per record state (defaults, not proven learning science; adjust to the student's request and remaining time):

| Record state | Default tasks |
|---|---|
| In scope, Unassessed, teaching notes available | `learn`, then `practice` with a later `not_before` |
| In scope, teaching notes missing | one short `source-gap` block to find or request the notes |
| Needs practice with a corrective rule | `variant`: new setting or changed condition, not just new numbers |
| Improving | one transfer-style `practice` |
| Demonstrated with `Recheck before exam` | `recheck`, `not_before` at least one day after the session that promoted it |
| Demonstrated without a recheck note | optional light `recheck` near the exam |
| Excluded or unconfirmed scope | nothing |
| Each course, when time allows | one `mock` sitting 2-4 days before its exam (`not_before` and `due` dates); a mock is never split |

Priority 1 is for recorded errors and rechecks, 2 for untested in-scope topics, 3 for everything else. Use realistic minutes; the script splits long tasks into blocks between `min_block` and `max_block`.

## Run and react

```text
python <skill>/scripts/plan_study.py PLAN.json --out <study root>/plans/<plan_id> [--force]
```

Keep `PLAN.json` in the same folder. The script prints one line: `OK placed=… unplaced=… minutes=… out=…` or `ERROR <reason>`. On `ERROR`, fix the plan and rerun. If `unplaced` is above zero, do not hide it: shorten or merge low-priority tasks, or tell the student how many minutes did not fit and ask whether to add study time. Regenerating into the same folder needs `--force` and keeps event IDs, so a re-import updates rather than duplicates in calendars that honour IDs.

## Deliver

Link `plan.ics` and `calendar.html`. Summarise in three to five lines: per course, the number of blocks, the planned minutes, and the first block. Then say:

- Import `plan.ics` into a **separate calendar**, so the whole plan can be removed or replaced at once.
- Times have no time zone; the calendar app shows them in its own zone.
- The calendar sends no reminders, and finishing a block does not change recorded progress; progress changes only from reviewed work.

At the next save of each included course, add the plan folder under *Artifacts to reopen* in its learning record. When statuses change later, offer to regenerate the plan; do not regenerate automatically.

## Writing to the student's calendar

Only when the host provides a calendar tool. Before writing, state the target calendar, the number of events and the date range, and ask. Write only after a clear yes in the current conversation. Never modify or delete events this workflow did not create. With the student's consent, a host tool that reads free/busy time may be used read-only to suggest study times in the Gather step. Without such a tool, deliver the files and do not suggest workarounds that need the student's account access.
