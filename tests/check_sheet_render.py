"""Check the reference-sheet renderer: validation, markup, fonts, page fitting, outputs, CLI.

Rendering checks need ReportLab (and pypdfium2 for text extraction and previews); without them they are
skipped with a message and the remaining checks still run. Layout only; content correctness needs review.
"""
from pathlib import Path
import copy
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.dont_write_bytecode = True
import render_sheet as rs  # noqa: E402

EXAMPLE = json.loads((SKILL / 'assets/sheet-example.json').read_text(encoding='utf-8'))


def sheet_with(mutate=None):
    data = copy.deepcopy(EXAMPLE)
    if mutate:
        mutate(data)
    return data


def rejects(mutate, expected):
    try:
        rs.load_sheet(sheet_with(mutate))
    except rs.SheetError as error:
        assert expected in str(error), f'Expected {expected!r} in: {error}'
        return
    raise AssertionError(f'load_sheet accepted invalid content ({expected})')


# Task 1: format, validation, inline markup (standard library only)

def test_example_valid():
    sheet = rs.load_sheet(sheet_with())
    assert sheet['allowance']['sides'] == 2 and sheet['revision']['round'] == 1


def test_defaults_filled():
    def strip(d):
        del d['allowance'], d['language'], d['revision']
        del d['sections'][0]['weight']
    sheet = rs.load_sheet(sheet_with(strip))
    assert sheet['allowance'] == {'status': 'unconfirmed', 'sheets': 1, 'sides': 2, 'paper': 'letter', 'rules': None,
                                  'min_body': None}
    assert sheet['language'] == 'en' and sheet['revision']['round'] == 1
    assert sheet['sections'][0]['weight'] == 'normal'


def test_rejects_format():
    rejects(lambda d: d.update(format='x/1'), 'format')


def test_rejects_block_type():
    rejects(lambda d: d['sections'][0]['blocks'].append({'type': 'poem', 'text': 'x'}), 'block type')


def test_rejects_ragged_table():
    rejects(lambda d: d['sections'][2]['blocks'][0]['rows'].append(['only one cell']), 'table')


def test_rejects_empty_sections():
    rejects(lambda d: d.update(sections=[]), 'sections')


def test_rejects_kind():
    rejects(lambda d: d.update(kind='poster'), 'kind')


def test_rejects_duplicate_section():
    rejects(lambda d: d['sections'].append(copy.deepcopy(d['sections'][0])), 'duplicate')


def test_rejects_weight():
    rejects(lambda d: d['sections'][0].update(weight='huge'), 'weight')


def test_rejects_sides():
    rejects(lambda d: d['allowance'].update(sides=3), 'sides')


def test_rejects_paper():
    rejects(lambda d: d['allowance'].update(paper='tabloid'), 'paper')


def test_inline_markup():
    out = rs.inline('**R²** uses `tidy()` and e^{0.4}, x_{i}')
    assert '<b>R²</b>' in out and '<font face="{mono}">tidy()</font>' in out
    assert '<super>0.4</super>' in out and '<sub>i</sub>' in out


def test_inline_escaping():
    assert rs.inline('a < b & **c') == 'a &lt; b &amp; **c'
    assert rs.inline('<b>x</b>') == '&lt;b&gt;x&lt;/b&gt;'


# Task 3: fonts (rendering group; functions named render_test_* need ReportLab)

import os  # noqa: E402

CANDIDATE_FILES = [Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/segoeui.ttf',
                   Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/arial.ttf',
                   Path('/System/Library/Fonts/Supplemental/Arial.ttf')]


def render_test_fonts_found():
    fonts = rs.find_fonts('en')
    if any(p.exists() for p in CANDIDATE_FILES) or list(Path('/usr/share/fonts').rglob('DejaVuSans.ttf')):
        assert fonts['body'] != 'Helvetica' and fonts['files'], fonts
        assert fonts['mono'] != fonts['body']
    else:
        assert rs.missing_glyphs('β', fonts['body']) == {'β'}


def render_test_unicode_glyphs():
    fonts = rs.find_fonts('en')
    if fonts['body'] != 'Helvetica':
        assert rs.missing_glyphs('β ≤ → ² − ·', fonts['body']) == set()
        assert rs.missing_glyphs('β ≤ → ² − ·', fonts['bold']) == set()


def render_test_missing_glyph_reported():
    fonts = rs.find_fonts('en')
    assert rs.missing_glyphs('\U0001D4AE', fonts['body']) == {'\U0001D4AE'}  # mathematical script S


def render_test_cjk():
    fonts = rs.find_fonts('zh')
    sample = '\u6761\u4ef6\u6982\u7387'
    assert fonts['body'] == 'STSong-Light' and rs.missing_glyphs(sample + ' abc', fonts['body']) == set()


# Task 4: layout and auto-fit (rendering group)

def multiplied(times, kind='exam-sheet', data=None):
    """Repeat every section `times` times with fresh ids, to make dense content."""
    base = sheet_with() if data is None else data
    sections = []
    for n in range(times):
        for s in base['sections']:
            copy_ = copy.deepcopy(s)
            copy_['id'] = f"{s['id']}-{n}"
            sections.append(copy_)
    base['sections'], base['kind'] = sections, kind
    return base


def fitted(data):
    sheet = rs.load_sheet(data)
    return rs.fit(sheet, rs.find_fonts(sheet['language']))


def dense_content():
    """Smallest repetition whose best fit is tighter than the most spacious preset."""
    for times in range(2, 9):
        data = multiplied(times)
        try:
            result = fitted(copy.deepcopy(data))
        except rs.Overflow:
            break
        if result['preset'] > 0:
            return data, result
    raise AssertionError('no repetition count needed a tighter preset before overflowing')


def render_test_example_fits():
    result = fitted(sheet_with())
    assert result['pages'] <= 2 and result['preset'] == 0, result
    assert result['body'] == rs.PRESETS[0]['body']


def render_test_cut_content_grows_type():
    data, tight = dense_content()
    data['sections'] = data['sections'][: len(data['sections']) // 2]
    loose = fitted(data)
    assert loose['body'] > tight['body'], (loose, tight)


def render_test_overflow_reports_sections():
    try:
        fitted(multiplied(12))
    except rs.Overflow as error:
        ids = [sid for sid, _ in error.sections]
        assert 'interaction-0' in ids and all(h > 0 for _, h in error.sections)
        assert error.over_pt > 0
        return
    raise AssertionError('12x content fitted on two pages')


def render_test_minimum_sizes():
    assert all(p['body'] >= 9 and p['code'] >= 8.5 for p in rs.PRESETS)
    data, _ = dense_content()
    data['allowance']['min_body'] = 10
    try:
        result = fitted(data)
    except rs.Overflow:
        return
    assert result['body'] >= 10, result


def render_test_block_taller_than_column():
    def huge(d):
        d['sections'][2]['blocks'][0]['rows'] = [[f'r{i}', 'a', 'b'] for i in range(200)]
    try:
        fitted(sheet_with(huge))
    except rs.Overflow as error:
        assert error.sections and error.sections[0][0] == 'classify', error.sections
        return
    raise AssertionError('a 200-row table fitted inside one column')


def render_test_study_guide_unbounded():
    result = fitted(multiplied(12, kind='study-guide'))
    assert result['pages'] > 2, result


TESTS = [value for name, value in sorted(globals().items()) if name.startswith('test_')]


def reportlab_available():
    try:
        import reportlab  # noqa: F401
    except ImportError:
        return False
    return True


def check():
    failed = []
    tests = list(TESTS)
    if reportlab_available():
        tests += [value for name, value in sorted(globals().items()) if name.startswith('render_test_')]
    else:
        print('SKIP rendering checks: reportlab not installed')
    for test in tests:
        try:
            test()
        except Exception as error:
            failed.append(f'{test.__name__}: {type(error).__name__}: {error}')
    if failed:
        print('FAIL\n' + '\n'.join(failed))
        raise SystemExit(1)
    print(f'PASS: {len(tests)} sheet checks')


if __name__ == '__main__':
    check()
