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
