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


def test_inline_code_is_literal():
    mono = '<font face="{mono}">'
    assert rs.inline('`x**2 + y**2`') == f'{mono}x**2 + y**2</font>'
    assert rs.inline('`x_{i}` and `e^{x}`') == f'{mono}x_{{i}}</font> and {mono}e^{{x}}</font>'
    assert rs.inline('`a < b && c`') == f'{mono}a &lt; b &amp;&amp; c</font>'
    assert rs.inline('**fit** uses `y ~ x**2` then e^{2}') == f'<b>fit</b> uses {mono}y ~ x**2</font> then e<super>2</super>'


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
    """Add copied sections one at a time until the best fit is tighter than the most spacious preset."""
    base = sheet_with()
    for extra in range(1, 3 * len(base['sections'])):
        data = sheet_with()
        for n in range(extra):
            section = copy.deepcopy(base['sections'][n % len(base['sections'])])
            section['id'] = f"{section['id']}-extra-{n}"
            data['sections'].append(section)
        try:
            result = fitted(copy.deepcopy(data))
        except rs.Overflow:
            break
        if result['preset'] > 0:
            return data, result
    raise AssertionError('no content size needed a tighter preset before overflowing')


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


def render_test_code_too_wide():
    def wide(d):
        d['sections'][5]['blocks'][0]['text'] = 'x <- ' + 'very_long_identifier_' * 8
    try:
        fitted(sheet_with(wide))
    except rs.Overflow as error:
        assert error.sections[0][0] == 'code' and 'wider' in error.reason, (error.sections, error.reason)
        return
    raise AssertionError('a code line wider than a column was accepted')


def render_test_chosen_preset_fits_code_width():
    from reportlab.pdfbase.pdfmetrics import stringWidth
    line = 'x' * 55  # too wide at 9.5 pt Consolas in a sheet column, fits at a smaller preset
    for kind in ('exam-sheet', 'study-guide'):
        data = sheet_with(lambda d: d['sections'][5]['blocks'][0].update(text=line))
        data['kind'] = kind
        if kind == 'study-guide':
            data['sections'][5]['blocks'][0]['text'] = 'x' * 107  # too wide at the guide's 9.25 pt default
        sheet = rs.load_sheet(data)
        fonts = rs.find_fonts('en')
        result = rs.fit(sheet, fonts)
        assert result['preset'] > (0 if kind == 'exam-sheet' else 1), (kind, result)
        col_w = rs._geometry(sheet)[3]
        width = stringWidth(sheet['sections'][5]['blocks'][0]['text'], fonts['mono'], result['code'])
        assert width <= col_w + 0.5, (kind, result, width, col_w)
    widest = max(stringWidth('x' * 55, rs.find_fonts('en')['mono'], p['code']) for p in rs.PRESETS)
    smallest = min(stringWidth('x' * 55, rs.find_fonts('en')['mono'], p['code']) for p in rs.PRESETS)
    sheet_col = rs._geometry(rs.load_sheet(sheet_with()))[3]
    assert smallest <= sheet_col < widest, 'fixture must be too wide at the largest preset only'


def render_test_titles_stay_with_content():
    for data in (sheet_with(), dense_content()[0]):
        sheet = rs.load_sheet(data)
        fonts = rs.find_fonts('en')
        preset = rs.PRESETS[rs.fit(sheet, fonts)['preset']]
        placements = rs._build(sheet, fonts, preset)['placements']
        first = {}
        for section_id, role, where in placements:
            first.setdefault((section_id, role), where)
        for section in sheet['sections']:
            assert first[(section['id'], 'title')] == first[(section['id'], 'block')], (
                section['id'], first[(section['id'], 'title')], first[(section['id'], 'block')])


def render_test_study_guide_unbounded():
    result = fitted(multiplied(12, kind='study-guide'))
    assert result['pages'] > 2, result


# Task 5: outputs and command line

import re  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402

SCRIPT = SKILL / 'scripts/render_sheet.py'


def run(*args, python=None):
    done = subprocess.run([python or sys.executable, str(SCRIPT), *map(str, args)], capture_output=True,
                          text=True, encoding='utf-8')
    return done.returncode, done.stdout.strip(), done.stderr


def write_sheet(folder, data=None, name='sheet.json'):
    path = Path(folder) / name
    path.write_text(json.dumps(data if data is not None else EXAMPLE), encoding='utf-8')
    return path


def pdf_text(path):
    import pypdfium2 as pdfium
    document = pdfium.PdfDocument(str(path))
    try:
        return [document[i].get_textpage().get_text_range() for i in range(len(document))]
    finally:
        document.close()


def render_test_cli_ok():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        code, stdout, stderr = run(write_sheet(tmp), '--out', out)
        assert code == 0 and re.match(r'^OK pages=[12] preset=\d body=[\d.]+pt out=', stdout), (stdout, stderr)
        slug = 'regression-and-classification-exam-sheet-v1'
        assert (out / f'{slug}.pdf').is_file() and (out / f'{slug}.json').is_file()
        checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
        assert checks['pages'] in (1, 2) and checks['missing_glyphs'] == [] and checks['fonts']['body']
        assert checks['previews'] and all((out / p).is_file() for p in checks['previews'])


def render_test_footer_unconfirmed():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        assert run(write_sheet(tmp), '--out', out)[0] == 0
        pages = pdf_text(next(out.glob('*.pdf')))
        assert all('Exam use unconfirmed' in page for page in pages), pages
        confirmed = sheet_with(lambda d: d['allowance'].update(status='confirmed'))
        out2 = Path(tmp) / 'out2'
        assert run(write_sheet(tmp, confirmed, 'c.json'), '--out', out2)[0] == 0
        assert not any('Exam use unconfirmed' in page for page in pdf_text(next(out2.glob('*.pdf'))))


def render_test_versions_kept():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        assert run(write_sheet(tmp), '--out', out)[0] == 0
        second = sheet_with(lambda d: d['revision'].update(round=2))
        path = write_sheet(tmp, second, 'r2.json')
        assert run(path, '--out', out)[0] == 0
        assert {p.name for p in out.glob('*.pdf')} == {'regression-and-classification-exam-sheet-v1.pdf',
                                                       'regression-and-classification-exam-sheet-v2.pdf'}
        code, stdout, _ = run(path, '--out', out)
        assert code == 1 and 'force' in stdout, stdout
        assert run(path, '--out', out, '--force')[0] == 0


def render_test_missing_glyph_fails():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        assert run(write_sheet(tmp), '--out', out)[0] == 0
        pdf = out / 'regression-and-classification-exam-sheet-v1.pdf'
        before = pdf.read_bytes()
        broken = sheet_with(lambda d: d['sections'][0]['blocks'][0].update(text='Unassigned code point ͸ here'))
        path = write_sheet(tmp, broken, 'broken.json')
        for args in (('--check',), ('--out', out, '--force')):
            code, stdout, stderr = run(path, *args)
            assert code == 1 and stdout.startswith('ERROR missing glyphs') and 'U+0378' in stdout, (args, stdout)
            assert 'Traceback' not in stderr
        assert pdf.read_bytes() == before, 'a failed render must not replace the existing round'


def render_test_cli_overflow():
    with tempfile.TemporaryDirectory() as tmp:
        code, stdout, _ = run(write_sheet(tmp, multiplied(12)), '--out', Path(tmp) / 'out')
        assert code == 2 and re.match(r'^OVERFLOW over=\d+pt sections=interaction-0:[\d.]+', stdout), stdout
        assert not (Path(tmp) / 'out').exists() or not list((Path(tmp) / 'out').glob('*.pdf'))


def test_cli_errors():
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / 'bad.json'
        bad.write_text('{nope', encoding='utf-8')
        invalid = write_sheet(tmp, sheet_with(lambda d: d.update(format='x')), 'invalid.json')
        for path in (bad, invalid, Path(tmp) / 'missing.json'):
            code, stdout, stderr = run(path, '--out', Path(tmp) / 'out')
            assert code == 1 and stdout.startswith('ERROR '), stdout
            assert 'Traceback' not in stderr, stderr


def test_cli_no_reportlab():
    with tempfile.TemporaryDirectory() as tmp:
        wrapper = ("import sys, runpy; sys.modules['reportlab'] = None; "
                   f"sys.argv = [{str(SCRIPT)!r}, {str(write_sheet(tmp))!r}, '--out', {str(Path(tmp) / 'o')!r}]; "
                   f"runpy.run_path({str(SCRIPT)!r}, run_name='__main__')")
        done = subprocess.run([sys.executable, '-c', wrapper], capture_output=True, text=True, encoding='utf-8')
        assert done.returncode == 3, (done.returncode, done.stdout, done.stderr)
        assert 'ask the student before running pip install reportlab' in done.stdout, done.stdout


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
