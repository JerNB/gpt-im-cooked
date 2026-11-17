"""Turn a model-written study plan into a timed schedule, an iCalendar file and a printable HTML calendar.

The model decides what to study (tasks, minutes, priority, date bounds, record basis).
This script decides when: it packs tasks into the student's availability windows,
validates the result, and writes schedule.json, plan.ics and calendar.html.
Times are floating local times (no time zone); calendars import them in their own zone.
It sends no notifications and tracks no completion.

Usage:
  python plan_study.py PLAN.json --out DIR [--force]
  python plan_study.py PLAN.json --check

Requires Python 3.10+ and only its standard library.
"""
from datetime import date, datetime, timedelta
from pathlib import Path
import html
import re

FORMAT = 'gpt-im-cooked-study-plan/1'
KINDS = {'learn', 'practice', 'variant', 'recheck', 'mock', 'review', 'source-gap'}
WEEKDAYS = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
DEFAULTS = {'max_minutes_per_day': 120, 'min_block': 25, 'max_block': 90}
SLUG = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$')
WINDOW = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)-([01]\d|2[0-4]):([0-5]\d)$')
NO_RECORD = 'No learning record'


class PlanError(ValueError):
    """The plan cannot be scheduled as written."""


def _need(condition, message):
    if not condition:
        raise PlanError(message)


def _date(value, where):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise PlanError(f'{where}: expected a date YYYY-MM-DD, got {value!r}') from None


def _datetime(value, where):
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise PlanError(f'{where}: expected a date and time YYYY-MM-DDTHH:MM, got {value!r}') from None
    _need(parsed.tzinfo is None, f'{where}: use local time without a time zone')
    return parsed


def _text(value, where, required=True):
    if value is None and not required:
        return ''
    _need(isinstance(value, str) and value.strip(), f'{where}: missing text')
    return value.strip()


def _positive(value, where):
    _need(isinstance(value, int) and not isinstance(value, bool) and value > 0, f'{where}: must be a positive whole number of minutes')
    return value


def _windows(weekly):
    _need(isinstance(weekly, dict), 'availability.weekly: expected an object of weekday -> windows')
    windows = []
    for day, spans in weekly.items():
        _need(day in WEEKDAYS, f'availability.weekly: unknown weekday {day!r} (use {", ".join(WEEKDAYS)})')
        _need(isinstance(spans, list), f'availability.weekly.{day}: expected a list of windows')
        for span in spans:
            match = WINDOW.match(span) if isinstance(span, str) else None
            _need(match, f'availability.weekly.{day}: window {span!r} must look like 19:00-22:00')
            h1, m1, h2, m2 = (int(g) for g in match.groups())
            start, end = h1 * 60 + m1, h2 * 60 + m2
            _need(end <= 24 * 60 and start < end,
                  f'availability.weekly.{day}: window {span!r} must end after it starts on the same day')
            windows.append((WEEKDAYS.index(day), start, end))
    windows.sort()
    for a, b in zip(windows, windows[1:]):
        _need(a[0] != b[0] or a[2] <= b[1], f'availability.weekly.{WEEKDAYS[a[0]]}: windows overlap')
    return windows


def load_plan(data):
    """Validate a plan and return a normalised copy (dates parsed, windows as minute tuples, defaults filled)."""
    _need(isinstance(data, dict), 'plan: expected a JSON object')
    _need(data.get('format') == FORMAT, f'format: expected {FORMAT!r}')
    plan_id = data.get('plan_id')
    _need(isinstance(plan_id, str) and SLUG.match(plan_id), 'plan_id: use lowercase letters, digits and hyphens')
    start = _date(data.get('start'), 'start')
    generated = _date(data.get('generated_on'), 'generated_on')

    avail = data.get('availability')
    _need(isinstance(avail, dict), 'availability: missing')
    settings = {key: _positive(avail.get(key, value), f'availability.{key}') for key, value in DEFAULTS.items()}
    _need(settings['min_block'] <= settings['max_block'], 'availability: min_block must not exceed max_block')
    days_off = avail.get('days_off', [])
    _need(isinstance(days_off, list), 'availability.days_off: expected a list of dates')
    availability = {
        'windows': _windows(avail.get('weekly', {})),
        'days_off': {_date(d, 'availability.days_off') for d in days_off},
        **settings,
    }

    courses = {}
    raw_courses = data.get('courses')
    _need(isinstance(raw_courses, list) and raw_courses, 'courses: expected at least one course')
    for i, course in enumerate(raw_courses):
        where = f'courses[{i}]'
        _need(isinstance(course, dict), f'{where}: expected an object')
        cid = course.get('id')
        _need(isinstance(cid, str) and SLUG.match(cid), f'{where}.id: use lowercase letters, digits and hyphens')
        _need(cid not in courses, f'{where}.id: duplicate course {cid!r}')
        exam = course.get('exam')
        _need(isinstance(exam, dict), f'{where}.exam: missing start and end')
        exam_start = _datetime(exam.get('start'), f'{where}.exam.start')
        exam_end = _datetime(exam.get('end'), f'{where}.exam.end')
        _need(exam_end > exam_start, f'{where}.exam: end must be after start')
        record = course.get('record')
        _need(record is None or (isinstance(record, str) and record.strip()), f'{where}.record: path or null')
        weekly_minutes = course.get('weekly_minutes', 0)
        _need(isinstance(weekly_minutes, int) and not isinstance(weekly_minutes, bool) and weekly_minutes >= 0,
              f'{where}.weekly_minutes: must be a whole number of minutes')
        courses[cid] = {
            'id': cid, 'title': _text(course.get('title'), f'{where}.title'),
            'exam_start': exam_start, 'exam_end': exam_end, 'location': course.get('location') or '',
            'record': record, 'weekly_minutes': weekly_minutes,
        }

    tasks, seen = [], set()
    raw_tasks = data.get('tasks')
    _need(isinstance(raw_tasks, list), 'tasks: expected a list')
    for i, item in enumerate(raw_tasks):
        where = f'tasks[{i}]'
        _need(isinstance(item, dict), f'{where}: expected an object')
        tid = item.get('id')
        _need(isinstance(tid, str) and SLUG.match(tid), f'{where}.id: use lowercase letters, digits and hyphens')
        _need(tid not in seen, f'{where}.id: duplicate task {tid!r}')
        seen.add(tid)
        where = f'task {tid}'
        cid = item.get('course')
        _need(cid in courses, f'{where}: unknown course {cid!r}')
        course = courses[cid]
        kind = item.get('kind')
        _need(kind in KINDS, f'{where}: kind must be one of {sorted(KINDS)}')
        if course['record'] is None:
            _need(kind == 'review', f'{where}: course {cid} has no learning record, so only review blocks are allowed')
        basis = _text(item.get('basis'), f'{where}.basis')
        priority = item.get('priority', 2)
        _need(priority in (1, 2, 3), f'{where}.priority: use 1, 2 or 3')
        due = item.get('due', 'exam')
        if due == 'exam':
            due_at = course['exam_start']
        else:
            due_at = min(datetime.combine(_date(due, f'{where}.due'), datetime.min.time()) + timedelta(days=1),
                         course['exam_start'])
        not_before = item.get('not_before')
        not_before = _date(not_before, f'{where}.not_before') if not_before is not None else None
        _need(not_before is None or datetime.combine(not_before, datetime.min.time()) < due_at,
              f'{where}.not_before: must be before the task is due (its due date or the exam)')
        tasks.append({
            'id': tid, 'course': cid, 'kind': kind, 'minutes': _positive(item.get('minutes'), f'{where}.minutes'),
            'title': _text(item.get('title'), f'{where}.title'), 'basis': basis,
            'details': _text(item.get('details'), f'{where}.details', required=False),
            'priority': priority, 'due_at': due_at, 'not_before': not_before,
        })

    return {'plan_id': plan_id, 'start': start, 'generated_on': generated,
            'availability': availability, 'courses': courses, 'tasks': tasks}


def _chunks(total, min_block, max_block):
    """Split a task into near-equal chunks no longer than max_block (each at least min_block when split)."""
    count = -(-total // max_block)
    while count > 1 and total // count < min_block:
        count -= 1
    unit = 5 if total % 5 == 0 else 1  # keep chunks in whole five-minute steps when the total allows
    parts = total // unit
    return [(parts // count + (1 if i < parts % count else 0)) * unit for i in range(count)]


def _round_up_5(moment):
    extra = (-moment.minute) % 5
    return moment.replace(second=0, microsecond=0) + timedelta(minutes=extra)


class _Calendar:
    """Free time per day, with a daily minute cap."""

    def __init__(self, plan, all_day):
        avail = plan['availability']
        self.cap = avail['max_minutes_per_day']
        self.all_day = all_day
        last = max(c['exam_start'] for c in plan['courses'].values()).date()
        exam_cut = {}
        for course in plan['courses'].values():
            day = course['exam_start'].date()
            exam_cut[day] = min(exam_cut.get(day, course['exam_start']), course['exam_start'])
        self.free, self.used = {}, {}
        day = plan['start']
        while day <= last:
            if day not in avail['days_off']:
                midnight = datetime.combine(day, datetime.min.time())
                spans = [] if all_day else [
                    [midnight + timedelta(minutes=s), midnight + timedelta(minutes=e)]
                    for w, s, e in avail['windows'] if w == day.weekday()]
                cut = exam_cut.get(day)
                if cut is not None:  # nothing on an exam day after the first exam starts
                    spans = [[s, min(e, cut)] for s, e in spans if s < cut]
                if all_day or spans:
                    self.free[day] = spans
                    self.used[day] = 0
            day += timedelta(days=1)

    def place(self, length, earliest, due_at, avoid, first_day=None, last_day=None):
        """Earliest fit on or after `earliest`, ending by `due_at`; days in `avoid` only as a last resort."""
        for allow_repeat in (False, True):
            for day in sorted(self.free):
                if day < earliest or (first_day and day < first_day) or (last_day and day > last_day):
                    continue
                if (day in avoid) != allow_repeat:  # first pass: new days only; second: repeat days
                    continue
                if self.used[day] + length > self.cap:
                    continue
                if self.all_day:
                    if day < due_at.date():
                        self.used[day] += length
                        return day, day
                    continue
                for span in self.free[day]:
                    start = _round_up_5(span[0])
                    end = start + timedelta(minutes=length)
                    if end <= span[1] and end <= due_at:
                        self.free[day].remove(span)
                        self.free[day] += [s for s in ([span[0], start], [end, span[1]]) if s[1] > s[0]]
                        self.free[day].sort()
                        self.used[day] += length
                        return start, end
        return None


def _place_task(cal, plan, task, earliest, first_day=None, last_day=None):
    avail = plan['availability']
    blocks, missing, days = [], 0, set()
    sizes = ([task['minutes']] if task['kind'] == 'mock'  # a mock exam is one sitting, never split
             else _chunks(task['minutes'], avail['min_block'], avail['max_block']))
    for size in sizes:
        spot = cal.place(size, earliest, task['due_at'], days, first_day, last_day)
        if spot is None:
            missing += size
            continue
        days.add(spot[0] if cal.all_day else spot[0].date())
        blocks.append({
            'id': f"{plan['plan_id']}-{task['id']}-{len(blocks) + 1}", 'task': task['id'],
            'course': task['course'], 'kind': task['kind'], 'title': task['title'],
            'start': spot[0], 'end': spot[1], 'minutes': size,
            'basis': task['basis'], 'details': task['details'],
        })
    return blocks, missing


def schedule(plan):
    """Pack tasks into free time; returns {'blocks', 'unplaced', 'all_day'}. Nothing is dropped silently."""
    all_day = not plan['availability']['windows']
    cal = _Calendar(plan, all_day)
    reason = ('no study day with capacity before it is due' if all_day
              else 'no free time in the availability windows before it is due')
    blocks, unplaced = [], []
    order = sorted(plan['tasks'], key=lambda t: (t['due_at'], t['priority'], t['not_before'] or plan['start'], t['id']))
    for task in order:
        placed, missing = _place_task(cal, plan, task, task['not_before'] or plan['start'])
        blocks += placed
        if missing:
            unplaced.append({'task': task['id'], 'course': task['course'], 'title': task['title'],
                             'minutes': missing, 'reason': reason})

    for course in plan['courses'].values():
        if course['record'] is not None or not course['weekly_minutes']:
            continue
        monday = plan['start'] - timedelta(days=plan['start'].weekday())
        while monday <= course['exam_start'].date():
            year, week, _ = monday.isocalendar()
            task = {'id': f"{course['id']}-review-{year}w{week:02d}", 'course': course['id'], 'kind': 'review',
                    'title': f"{course['title']} review", 'basis': NO_RECORD,
                    'details': 'General review time. This course has no learning record here, so plan the topics yourself.',
                    'minutes': course['weekly_minutes'], 'due_at': course['exam_start']}
            placed, missing = _place_task(cal, plan, task, max(monday, plan['start']), monday, monday + timedelta(days=6))
            blocks += placed
            if missing:
                unplaced.append({'task': task['id'], 'course': course['id'], 'title': task['title'],
                                 'minutes': missing, 'reason': reason})
            monday += timedelta(days=7)

    blocks.sort(key=lambda b: (b['start'], b['id']))
    return {'blocks': blocks, 'unplaced': unplaced, 'all_day': all_day}


PROGRESS_NOTE = 'Completing this block does not change your recorded progress.'


def _ics_text(value):
    return (value.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,')
            .replace('\r\n', '\n').replace('\n', '\\n'))


def _fold(line):
    """Fold to 75 octets per physical line without splitting a UTF-8 character."""
    out, current, size, limit = [], '', 0, 75
    for char in line:
        width = len(char.encode('utf-8'))
        if size + width > limit:
            out.append(current)
            current, size, limit = ' ', 1, 75
        current += char
        size += width
    out.append(current)
    return '\r\n'.join(out)


def _ics_time(value):
    if isinstance(value, datetime):
        return f':{value:%Y%m%dT%H%M%S}'
    return f';VALUE=DATE:{value:%Y%m%d}'


def to_ics(plan, result, sequence, stamp):
    """iCalendar text: one event per block and per exam, floating local times, no alarms."""
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', "PRODID:-//GPT I'm Cooked//study-plan//EN", 'CALSCALE:GREGORIAN',
             f"X-WR-CALNAME:{_ics_text(plan['plan_id'] + ' study plan (GPT, I' + chr(39) + 'm Cooked)')}"]

    def event(uid, start, end, summary, description, category):
        lines.extend([
            'BEGIN:VEVENT', f'UID:{uid}@gpt-im-cooked', f'DTSTAMP:{stamp:%Y%m%dT%H%M%S}Z',
            f'DTSTART{_ics_time(start)}', f'DTEND{_ics_time(end)}', f'SUMMARY:{_ics_text(summary)}',
            f'DESCRIPTION:{_ics_text(description)}', f'CATEGORIES:{_ics_text(category)}',
            f'SEQUENCE:{sequence}', 'TRANSP:OPAQUE', 'END:VEVENT'])

    for block in result['blocks']:
        course = plan['courses'][block['course']]
        end = block['end'] + timedelta(days=1) if not isinstance(block['end'], datetime) else block['end']
        details = f"{block['details']}\n\n" if block['details'] else ''
        event(block['id'], block['start'], end, f"{course['title']} · {block['title']}",
              f"{details}{block['minutes']} minutes · {block['kind']}\nBasis: {block['basis']}\n{PROGRESS_NOTE}",
              block['kind'])
    for course in plan['courses'].values():
        where = f"\nLocation: {course['location']}" if course['location'] else ''
        event(f"{plan['plan_id']}-{course['id']}-exam", course['exam_start'], course['exam_end'],
              f"{course['title']} exam", f"Exam time from your course profile.{where}", 'Exam')
    lines.append('END:VCALENDAR')
    return ''.join(_fold(line) + '\r\n' for line in lines)


COLOURS = ('#2f5d50', '#2a7f86', '#a8741a', '#7a4e7e', '#a24b3b', '#4b5d7a')
TEMPLATE = Path(__file__).resolve().parents[1] / 'assets' / 'study-plan-template.html'
FLOATING_NOTE = 'Times have no time zone; your calendar app shows them in its own zone.'


def _hm(moment):
    return f'{moment:%H:%M}'


def to_html(plan, result, generated_on):
    """Self-contained printable calendar (week grid, day list on narrow screens). No scripts, no external assets."""
    esc = html.escape
    courses = list(plan['courses'].values())
    colour = {c['id']: COLOURS[i % len(COLOURS)] for i, c in enumerate(courses)}
    last = max(c['exam_start'] for c in courses).date()
    planned = sum(b['minutes'] for b in result['blocks'])

    sources = [esc(c['record']) if c['record'] else f"{esc(c['title'])} (no learning record)" for c in courses]
    notes = [f"Generated {generated_on.isoformat()} from: {', '.join(sources)}.",
             'Completing a block does not change your recorded progress; your tutor updates progress from reviewed work.',
             FLOATING_NOTE if not result['all_day'] else 'No study windows were given, so each day lists its review tasks.',
             'Import plan.ics into a separate calendar so the whole plan can be removed or replaced at once.']

    summary, legend = [], []
    for c in courses:
        mine = [b for b in result['blocks'] if b['course'] == c['id']]
        record = f"Record: {esc(c['record'])}" if c['record'] else 'No learning record: time blocks only'
        summary.append(
            f'<article class="course-card" style="--c:{colour[c["id"]]}"><h2>{esc(c["title"])}</h2>'
            f'<p class="exam-when">Exam {c["exam_start"]:%a %b} {c["exam_start"].day}, {_hm(c["exam_start"])}</p>'
            f'<p>{len(mine)} blocks · {sum(b["minutes"] for b in mine)} min planned</p><p>{record}</p></article>')
        legend.append(f'<li><span class="swatch" style="--c:{colour[c["id"]]}"></span>{esc(c["title"])}</li>')

    def block_html(b):
        course = plan['courses'][b['course']]
        when = '' if result['all_day'] else f'<span class="time">{_hm(b["start"])}–{_hm(b["end"])}</span> '
        return (f'<div class="block" data-block="{esc(b["id"])}" style="--c:{colour[b["course"]]}">'
                f'<span class="check">&#9744; </span>{when}<span class="course">{esc(course["title"])}</span>'
                f'<span class="title">{esc(b["title"])}</span>'
                f'<span class="meta">{esc(b["kind"])} · {b["minutes"]} min</span>'
                f'<span class="basis">{esc(b["basis"])}</span></div>')

    def exam_html(c):
        return (f'<div class="block exam"><span class="time">{_hm(c["exam_start"])}–{_hm(c["exam_end"])}</span> '
                f'<span class="course">Exam</span><span class="title">{esc(c["title"])}</span></div>')

    by_day = {}
    for b in result['blocks']:
        day = b['start'] if result['all_day'] else b['start'].date()
        by_day.setdefault(day, []).append(b)
    exams = {}
    for c in courses:
        exams.setdefault(c['exam_start'].date(), []).append(c)

    weeks = []
    monday = plan['start'] - timedelta(days=plan['start'].weekday())
    while monday <= last:
        cells = []
        for offset in range(7):
            day = monday + timedelta(days=offset)
            items = [(b['start'] if not result['all_day'] else datetime.min, block_html(b)) for b in by_day.get(day, [])]
            items += [(c['exam_start'], exam_html(c)) for c in exams.get(day, [])]
            classes = ['day']
            tag = ''
            if day < plan['start'] or day > last:
                classes.append('outside')
            elif day in plan['availability']['days_off']:
                classes.append('off')
                tag = '<span class="tag">Day off</span>'
            if not items:
                classes.append('empty')
            heading = 'All-day review list' if result['all_day'] and by_day.get(day) else ''
            body = ''.join(h for _, h in sorted(items, key=lambda item: item[0]))
            cells.append(f'<div class="{" ".join(classes)}"><h3>{day:%a} {day.day}</h3>{tag}'
                         f'{f"<p class=tag>{heading}</p>" if heading else ""}{body}</div>')
        weeks.append(f'<section class="week"><h2>Week of {monday:%b} {monday.day}</h2>'
                     f'<div class="days">{"".join(cells)}</div></section>')
        monday += timedelta(days=7)

    unplaced = ''
    if result['unplaced']:
        rows = ''.join(f'<li>{esc(plan["courses"][u["course"]]["title"])} · {esc(u["title"])}: '
                       f'{u["minutes"]} min ({esc(u["reason"])})</li>' for u in result['unplaced'])
        unplaced = f'<section class="unplaced"><h2>Did not fit</h2><ul>{rows}</ul></section>'

    title = f"{' · '.join(c['title'] for c in courses)} study plan"
    subtitle = (f"{plan['start']:%b} {plan['start'].day} to {last:%b} {last.day}, {last.year} · "
                f"{len(result['blocks'])} blocks · {planned / 60:.1f} hours planned")
    page = TEMPLATE.read_text(encoding='utf-8')
    for key, value in {'TITLE': esc(title), 'SUBTITLE': esc(subtitle),
                       'NOTES': ''.join(f'<p>{n}</p>' for n in notes), 'SUMMARY': ''.join(summary),
                       'LEGEND': ''.join(legend), 'UNPLACED': unplaced, 'WEEKS': ''.join(weeks)}.items():
        page = page.replace('{{' + key + '}}', value)
    return page


def _iso(value):
    return value.isoformat(timespec='minutes') if isinstance(value, datetime) else value.isoformat()


def main(argv=None):
    import argparse
    import json
    from datetime import timezone

    parser = argparse.ArgumentParser(description='Schedule a study plan and write plan.ics and calendar.html.')
    parser.add_argument('plan', type=Path)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--out', type=Path, help='folder for schedule.json, plan.ics and calendar.html')
    target.add_argument('--check', action='store_true', help='validate and schedule without writing files')
    parser.add_argument('--force', action='store_true', help='regenerate into a folder that already has a plan')
    args = parser.parse_args(argv)
    try:
        try:
            data = json.loads(args.plan.read_text(encoding='utf-8'))
        except OSError as error:
            raise PlanError(f'cannot read {args.plan}: {error.strerror or error}') from None
        except json.JSONDecodeError as error:
            raise PlanError(f'{args.plan} is not valid JSON (line {error.lineno}: {error.msg})') from None
        plan = load_plan(data)
        result = schedule(plan)
        placed = sum(b['minutes'] for b in result['blocks'])
        summary = f"placed={len(result['blocks'])} unplaced={len(result['unplaced'])} minutes={placed}"
        if args.check:
            print(f'OK {summary} out=none')
            return 0
        out = args.out
        previous = out / 'schedule.json'
        sequence = 0
        if previous.exists():
            if not args.force:
                raise PlanError(f'output exists in {out}; pass --force to regenerate')
            try:
                sequence = int(json.loads(previous.read_text(encoding='utf-8')).get('sequence', -1)) + 1
            except (ValueError, OSError, AttributeError):
                sequence = 1
        out.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
        saved = {'format': FORMAT, 'plan_id': plan['plan_id'], 'sequence': sequence,
                 'generated_on': plan['generated_on'].isoformat(), 'all_day': result['all_day'],
                 'blocks': [{k: _iso(v) if isinstance(v, (date, datetime)) else v for k, v in b.items()}
                            for b in result['blocks']],
                 'unplaced': result['unplaced']}
        previous.write_text(json.dumps(saved, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        (out / 'plan.ics').write_text(to_ics(plan, result, sequence, stamp), encoding='utf-8', newline='')
        (out / 'calendar.html').write_text(to_html(plan, result, plan['generated_on']), encoding='utf-8')
        print(f'OK {summary} out={out}')
        return 0
    except PlanError as error:
        print(f'ERROR {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
