"""Check the study-plan script: validation, packing, iCalendar and HTML output, CLI.

Structure and scheduling rules only; it cannot judge whether the chosen tasks are pedagogically right.
"""
from pathlib import Path
import copy
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.dont_write_bytecode = True
import plan_study as ps  # noqa: E402

EXAMPLE = json.loads((SKILL / 'assets/study-plan-example.json').read_text(encoding='utf-8'))


def plan_with(mutate=None):
    data = copy.deepcopy(EXAMPLE)
    if mutate:
        mutate(data)
    return data


def task(data, task_id):
    return next(t for t in data['tasks'] if t['id'] == task_id)


def rejects(mutate, expected):
    try:
        ps.load_plan(plan_with(mutate))
    except ps.PlanError as error:
        assert expected in str(error), f'Expected {expected!r} in: {error}'
        return
    raise AssertionError(f'load_plan accepted an invalid plan ({expected})')


# Task 1: format and validation

def test_example_valid():
    plan = ps.load_plan(plan_with())
    assert plan['availability']['max_minutes_per_day'] == 180


def test_defaults_filled():
    def strip(d):
        for key in ('max_minutes_per_day', 'min_block', 'max_block'):
            del d['availability'][key]
    plan = ps.load_plan(plan_with(strip))
    assert (plan['availability']['max_minutes_per_day'], plan['availability']['min_block'],
            plan['availability']['max_block']) == (120, 25, 90)


def test_rejects_format():
    rejects(lambda d: d.update(format='other/1'), 'format')


def test_rejects_missing_basis():
    rejects(lambda d: d['tasks'][0].pop('basis'), 'basis')


def test_rejects_unknown_course():
    rejects(lambda d: d['tasks'][0].update(course='bio100'), 'unknown course')


def test_rejects_kind():
    rejects(lambda d: d['tasks'][0].update(kind='cram'), 'kind')


def test_rejects_minutes():
    rejects(lambda d: d['tasks'][0].update(minutes=0), 'minutes')


def test_rejects_bad_window():
    rejects(lambda d: d['availability']['weekly'].update(mon=['22:00-19:00']), 'window')
    rejects(lambda d: d['availability']['weekly'].update(mon=['22:00-01:00']), 'window')
    rejects(lambda d: d['availability']['weekly'].update(mon=['7pm-9pm']), 'window')
    rejects(lambda d: d['availability']['weekly'].update(funday=['19:00-20:00']), 'weekday')


def test_rejects_not_before_after_exam():
    rejects(lambda d: task(d, 'sta199-t3-recheck').update(not_before='2026-12-20'), 'not_before')


def test_rejects_duplicate_task():
    rejects(lambda d: d['tasks'].append(copy.deepcopy(d['tasks'][0])), 'duplicate')


def test_rejects_unrecorded_kind():
    def add(d):
        d['tasks'].append({'id': 'hist-x', 'course': 'hist101', 'kind': 'learn', 'minutes': 30,
                           'title': 'x', 'due': 'exam', 'priority': 1, 'basis': 'No learning record'})
    rejects(add, 'no learning record')


def test_rejects_block_sizes():
    rejects(lambda d: d['availability'].update(min_block=60, max_block=30), 'block')


def test_rejects_unsplittable_task():
    def tight_blocks(d):
        d['availability'].update(min_block=60, max_block=90)
        d['tasks'] = [t for t in d['tasks'] if t['kind'] != 'mock' and t['minutes'] <= 90 or t['id'] == 'cs201-t4-practice']
        task(d, 'cs201-t4-practice')['minutes'] = 91
    rejects(tight_blocks, 'cannot be split')


def test_rejects_unsplittable_weekly_review():
    def tight(d):
        d['availability'].update(min_block=60, max_block=90)
        d['tasks'] = [t for t in d['tasks'] if t['minutes'] <= 90 and t['kind'] != 'mock']
        d['courses'][2]['weekly_minutes'] = 100
    rejects(tight, 'cannot be split')


def test_rejects_bad_date():
    rejects(lambda d: d.update(start='17 Nov 2026'), 'date')


# Task 2: free slots and packing

from datetime import date, datetime, timedelta  # noqa: E402


def scheduled(mutate=None):
    plan = ps.load_plan(plan_with(mutate))
    return plan, ps.schedule(plan)


def minutes(block):
    return int((block['end'] - block['start']).total_seconds() // 60)


def test_example_all_placed():
    _, result = scheduled()
    assert result['unplaced'] == [], result['unplaced']
    assert result['all_day'] is False


def test_within_windows():
    plan, result = scheduled()
    for b in result['blocks']:
        day = b['start'].date()
        start = b['start'].hour * 60 + b['start'].minute
        end = start + minutes(b)
        assert any(w == day.weekday() and s <= start and end <= e for w, s, e in plan['availability']['windows']), b


def test_days_off():
    _, result = scheduled()
    off = {date(2026, 11, 25), date(2026, 11, 26), date(2026, 11, 27)}
    assert not [b for b in result['blocks'] if b['start'].date() in off]


def test_daily_cap():
    _, result = scheduled(lambda d: d['availability'].update(max_minutes_per_day=60))
    per_day = {}
    for b in result['blocks']:
        per_day[b['start'].date()] = per_day.get(b['start'].date(), 0) + minutes(b)
    assert max(per_day.values()) <= 60, per_day


def test_before_exam():
    plan, result = scheduled()
    exams = [(c['exam_start'], c['exam_end']) for c in plan['courses'].values()]
    for b in result['blocks']:
        assert b['end'] <= plan['courses'][b['course']]['exam_start'], b
        for exam_start, _ in exams:
            assert not (b['start'].date() == exam_start.date() and b['end'] > exam_start), (b, exam_start)


def test_not_before():
    _, result = scheduled()
    recheck = [b for b in result['blocks'] if b['task'] == 'sta199-t3-recheck']
    assert recheck and all(b['start'].date() >= date(2026, 11, 19) for b in recheck)
    mock = [b for b in result['blocks'] if b['task'] == 'sta199-mock']
    assert mock and all(date(2026, 12, 4) <= b['start'].date() <= date(2026, 12, 6) for b in mock)


def test_chunking():
    _, result = scheduled()
    chunks = [b for b in result['blocks'] if b['task'] == 'cs201-t4-practice']
    lengths = [minutes(b) for b in chunks]
    assert sum(lengths) == 200 and all(25 <= n <= 90 for n in lengths), lengths
    assert len({b['start'].date() for b in chunks}) == len(chunks)
    assert [b['id'] for b in chunks] == [f'fall-2026-finals-cs201-t4-practice-{n}' for n in range(1, len(chunks) + 1)]


def test_blocks_respect_max_block():
    for low, high in ((25, 90), (30, 45), (60, 90), (25, 88)):
        def limits(d, low=low, high=high):
            d['availability'].update(min_block=low, max_block=high)
            d['tasks'] = [t for t in d['tasks'] if ps._chunks(t['minutes'], low, high) or t['kind'] == 'mock']
        _, result = scheduled(limits)
        sizes = [b['minutes'] for b in result['blocks'] if b['kind'] != 'mock']
        assert sizes and max(sizes) <= high, (low, high, sizes)
    for total in range(1, 400):
        for low, high in ((25, 90), (60, 90), (25, 88), (40, 45)):
            chunks = ps._chunks(total, low, high)
            if chunks is None:
                assert not any(n * low <= total <= n * high for n in range(2, total // low + 1)), (total, low, high)
                assert total > high
            else:
                assert sum(chunks) == total and max(chunks) <= high, (total, low, high, chunks)
                assert len(chunks) == 1 or min(chunks) >= low, (total, low, high, chunks)


def test_mock_not_split():
    _, result = scheduled()
    for task_id in ('sta199-mock', 'cs201-mock'):
        sittings = [b for b in result['blocks'] if b['task'] == task_id]
        assert len(sittings) == 1 and minutes(sittings[0]) == 120, sittings


def test_chunks_whole_five_minutes():
    _, result = scheduled()
    assert all(minutes(b) % 5 == 0 for b in result['blocks']), [minutes(b) for b in result['blocks']]


def test_no_overlap():
    _, result = scheduled()
    blocks = sorted(result['blocks'], key=lambda b: b['start'])
    for a, b in zip(blocks, blocks[1:]):
        assert a['end'] <= b['start'], (a, b)


def test_overflow():
    def tight(d):
        d['availability']['weekly'] = {'sat': ['14:00-15:00']}
        for c in d['courses']:
            c['weekly_minutes'] = 0
    plan, result = scheduled(tight)
    placed = sum(minutes(b) for b in result['blocks'])
    missing = sum(u['minutes'] for u in result['unplaced'])
    assert result['unplaced'] and all(u['reason'] for u in result['unplaced'])
    assert placed + missing == sum(t['minutes'] for t in plan['tasks'])


def test_no_time_before_exam():
    def early(d):
        d['courses'][1]['exam'] = {'start': '2026-11-16T09:00', 'end': '2026-11-16T11:00'}
        for t in d['tasks']:
            if t['course'] == 'cs201':
                t.pop('not_before', None)
                t['due'] = 'exam'
    _, result = scheduled(early)
    assert not [b for b in result['blocks'] if b['course'] == 'cs201']
    assert {u['task'] for u in result['unplaced']} >= {'cs201-t2-variant', 'cs201-t4-practice', 'cs201-t7-gap', 'cs201-mock'}


def test_unrecorded_review():
    plan, result = scheduled()
    hist = [b for b in result['blocks'] if b['course'] == 'hist101']
    assert hist and all(b['kind'] == 'review' and b['basis'] == ps.NO_RECORD for b in hist)
    weeks = {}
    for b in hist:
        week = b['start'].isocalendar()[:2]
        weeks[week] = weeks.get(week, 0) + minutes(b)
    first = plan['start'].isocalendar()[:2]
    last = plan['courses']['hist101']['exam_start'].isocalendar()[:2]
    assert set(weeks) == {(2026, w) for w in range(first[1], last[1] + 1)}, weeks
    assert all(abs(total - 120) < 25 for total in weeks.values()), weeks


def test_all_day_fallback():
    def no_windows(d):
        d['availability']['weekly'] = {}
        del d['availability']['max_minutes_per_day']
    _, result = scheduled(no_windows)
    assert result['all_day'] is True and result['blocks']
    per_day = {}
    for b in result['blocks']:
        assert type(b['start']) is date, b
        per_day[b['start']] = per_day.get(b['start'], 0) + b['minutes']
    assert max(per_day.values()) <= 120, per_day


def test_deterministic():
    _, first = scheduled()
    _, second = scheduled()
    assert first == second
    assert all(b['start'].minute % 5 == 0 for b in first['blocks'])


# Task 3: iCalendar

STAMP = datetime(2026, 11, 16, 12, 0, 0)


def parse_ics(text):
    """Unfold RFC 5545 lines and return a list of events as {NAME: (params, unescaped value)}."""
    assert text.endswith('\r\n') and '\n' not in text.replace('\r\n', '')
    lines = []
    for raw in text.split('\r\n')[:-1]:
        if raw.startswith(' '):
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    events, current = [], None
    for line in lines:
        name_part, value = line.split(':', 1)
        name, *params = name_part.split(';')
        if line == 'BEGIN:VEVENT':
            current = {}
        elif line == 'END:VEVENT':
            events.append(current)
            current = None
        elif current is not None:
            unescaped = re.sub(r'\\([\\;,nN])', lambda m: '\n' if m.group(1) in 'nN' else m.group(1), value)
            current[name] = (params, unescaped)
    return lines, events


import re  # noqa: E402


def ics_for(mutate=None):
    plan, result = scheduled(mutate)
    return plan, result, ps.to_ics(plan, result, 0, STAMP)


def test_ics_parses():
    plan, result, text = ics_for()
    lines, events = parse_ics(text)
    assert lines[0] == 'BEGIN:VCALENDAR' and lines[-1] == 'END:VCALENDAR'
    assert len(events) == len(result['blocks']) + len(plan['courses'])
    uids = [e['UID'][1] for e in events]
    assert len(set(uids)) == len(uids)
    assert sum(1 for e in events if e['CATEGORIES'][1] == 'Exam') == len(plan['courses'])
    first = next(e for e in events if e['UID'][1] == result['blocks'][0]['id'] + '@gpt-im-cooked')
    assert 'Basis: ' + result['blocks'][0]['basis'] in first['DESCRIPTION'][1]
    assert 'does not change your recorded progress' in first['DESCRIPTION'][1]


def test_ics_floating():
    _, _, text = ics_for()
    assert 'TZID' not in text
    for line in parse_ics(text)[0]:
        if line.endswith('Z'):
            assert line.startswith('DTSTAMP:'), line


def test_ics_no_alarm():
    assert 'VALARM' not in ics_for()[2]


def test_ics_escaping():
    title = 'A, B; C\nD <script> \\ end'
    _, _, text = ics_for(lambda d: d['tasks'][0].update(title=title))
    events = parse_ics(text)[1]
    assert any(e['SUMMARY'][1].endswith(title) for e in events), [e['SUMMARY'][1] for e in events][:3]


def test_ics_folding():
    details = 'Long details with accents é and symbols ≤ → ' * 8
    _, _, text = ics_for(lambda d: d['tasks'][0].update(details=details))
    assert all(len(line.encode('utf-8')) <= 75 for line in text.split('\r\n'))
    events = parse_ics(text)[1]
    assert any(e['DESCRIPTION'][1].startswith(details.strip()) for e in events)  # load_plan trims text


def test_ics_all_day():
    _, _, text = ics_for(lambda d: d['availability'].update(weekly={}))
    assert 'DTSTART;VALUE=DATE:' in text and 'DTEND;VALUE=DATE:' in text


# Task 4: printable HTML

def html_for(mutate=None):
    plan, result = scheduled(mutate)
    return plan, result, ps.to_html(plan, result, date(2026, 11, 16))


def test_html_self_contained():
    page = html_for()[2].lower()
    for banned in ('http://', 'https://', 'src=', '<link', '<script'):
        assert banned not in page, banned


def test_html_escaping():
    title = '<script>alert(1)</script> & co'
    page = html_for(lambda d: d['tasks'][0].update(title=title))[2]
    assert '<script>' not in page and '&lt;script&gt;alert(1)&lt;/script&gt; &amp; co' in page


def test_html_blocks():
    plan, result, page = html_for()
    for b in result['blocks']:
        assert page.count(f'data-block="{b["id"]}"') == 1, b['id']
    legend = page.split('class="legend"', 1)[1].split('</ul>', 1)[0]
    for course in plan['courses'].values():
        assert course['title'] in legend


def test_html_notes():
    page = html_for()[2]
    assert 'does not change your recorded progress' in page
    assert '2026-11-16' in page
    assert 'STA199/learning-record.md' in page


def test_html_exams():
    plan, _, page = html_for()
    assert page.count('class="block exam"') == len(plan['courses'])


def test_html_unplaced():
    def tight(d):
        d['availability']['weekly'] = {'sat': ['14:00-15:00']}
    _, result, page = html_for(tight)
    box = page.split('Did not fit', 1)[1]
    assert result['unplaced'] and all(u['title'] in box for u in result['unplaced'] if '<' not in u['title'])


def test_html_all_day():
    _, result, page = html_for(lambda d: d['availability'].update(weekly={}))
    assert result['all_day'] and 'All-day review list' in page


def test_html_no_placeholders():
    assert '{{' not in html_for()[2]


# Task 5: command line

import subprocess  # noqa: E402
import tempfile  # noqa: E402

SCRIPT = SKILL / 'scripts/plan_study.py'


def run(*args):
    done = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True,
                          encoding='utf-8')
    return done.returncode, done.stdout.strip(), done.stderr


def write_plan(folder, data=None):
    path = Path(folder) / 'plan.json'
    path.write_text(json.dumps(data if data is not None else EXAMPLE), encoding='utf-8')
    return path


def test_cli_ok():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        code, stdout, _ = run(write_plan(tmp), '--out', out)
        assert code == 0 and re.match(r'^OK placed=\d+ unplaced=\d+ minutes=\d+ out=', stdout), stdout
        assert {p.name for p in out.iterdir()} == {'schedule.json', 'plan.ics', 'calendar.html'}
        saved = json.loads((out / 'schedule.json').read_text(encoding='utf-8'))
        assert saved['format'] == ps.FORMAT and saved['sequence'] == 0 and saved['blocks']


def test_cli_check():
    with tempfile.TemporaryDirectory() as tmp:
        plan = write_plan(tmp)
        code, stdout, _ = run(plan, '--check')
        assert code == 0 and stdout.startswith('OK '), stdout
        assert [p.name for p in Path(tmp).iterdir()] == ['plan.json']


def test_cli_errors():
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / 'bad.json'
        bad.write_text('{not json', encoding='utf-8')
        for path in (bad, write_plan(tmp, plan_with(lambda d: d['tasks'][0].pop('basis')))):
            code, stdout, stderr = run(path, '--out', Path(tmp) / 'out')
            assert code == 1 and stdout.startswith('ERROR '), stdout
            assert 'Traceback' not in stderr, stderr
        code, stdout, _ = run(Path(tmp) / 'missing.json', '--check')
        assert code == 1 and stdout.startswith('ERROR '), stdout


def test_regenerate():
    with tempfile.TemporaryDirectory() as tmp:
        plan, out = write_plan(tmp), Path(tmp) / 'out'
        assert run(plan, '--out', out)[0] == 0
        first = set(re.findall(r'UID:(\S+)', (out / 'plan.ics').read_text(encoding='utf-8')))
        code, stdout, _ = run(plan, '--out', out)
        assert code == 1 and 'force' in stdout, stdout
        assert run(plan, '--out', out, '--force')[0] == 0
        text = (out / 'plan.ics').read_text(encoding='utf-8')
        assert set(re.findall(r'UID:(\S+)', text)) == first
        assert 'SEQUENCE:1' in text and 'SEQUENCE:0' not in text


TESTS = [value for name, value in sorted(globals().items()) if name.startswith('test_')]


def check():
    failed = []
    for test in TESTS:
        try:
            test()
        except Exception as error:  # report every failing test, not just the first
            failed.append(f'{test.__name__}: {type(error).__name__}: {error}')
    if failed:
        print('FAIL\n' + '\n'.join(failed))
        raise SystemExit(1)
    print(f'PASS: {len(TESTS)} study-plan checks')


if __name__ == '__main__':
    check()
