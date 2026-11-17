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


def test_rejects_bad_date():
    rejects(lambda d: d.update(start='17 Nov 2026'), 'date')


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
