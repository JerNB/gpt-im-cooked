"""Check the reference-sheet renderer: validation, markup, fonts, page fitting, outputs, CLI.

Rendering checks need ReportLab (and pypdfium2 for text extraction and previews); without them they are
skipped with a message and the remaining checks still run. Layout only; content correctness needs review.
"""
from pathlib import Path
import copy
import json
import os
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


def render_test_inline_code_checked_in_mono_font():
    found = rs.find_fonts('en')
    if found['body'] == 'Helvetica':
        return  # no Unicode TTF on this host; nothing distinguishes body from mono coverage
    beta = 'β'

    def with_text(text):  # minimal sheet: only the text under test can contribute characters
        return rs.load_sheet({'format': rs.FORMAT, 'title': 'Glyph check', 'course': 'Test',
                              'sections': [{'id': 's', 'title': 'Only section', 'blocks': [{'type': 'cue', 'text': text}]}]})

    latin1_mono = dict(found, mono='Courier')  # built-in Courier covers Latin-1 only; the TTF body covers beta
    rs.check_glyphs(with_text(f'Use {beta} here.'), latin1_mono)  # prose: body font, fine
    for text in (f'Use `x{beta}` here.', f'**Bold `{beta}`** inside a cue'):
        try:
            rs.check_glyphs(with_text(text), latin1_mono)
        except rs.SheetError as error:
            assert 'U+03B2' in str(error) and 'Courier' in str(error), str(error)
        else:
            raise AssertionError(f'inline code {text!r} was not checked against the mono font')

    latin1_body = dict(found, body='Helvetica', bold='Helvetica-Bold')  # converse: code in a TTF mono that has beta
    if not rs.missing_glyphs(beta, found['mono']):
        rs.check_glyphs(with_text(f'Use `x{beta}` here.'), latin1_body)
        try:
            rs.check_glyphs(with_text(f'Use {beta} here.'), latin1_body)
        except rs.SheetError as error:
            assert 'Helvetica' in str(error)
        else:
            raise AssertionError('prose was not checked against the body font')


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


NO_ENGINE_QUESTION = 'I can make the PDF if you let me install one Python package (pip install reportlab). Install it?'


def run_without_engines(*args):
    """Run main() with ReportLab hidden and no browser discoverable."""
    code = ("import sys; sys.modules['reportlab'] = None; "
            f"sys.path.insert(0, {str(SCRIPT.parent)!r}); import render_sheet as r; "
            "r._browser_candidates = lambda: []; "
            f"raise SystemExit(r.main({[str(a) for a in args]!r}))")
    done = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, encoding='utf-8')
    return done.returncode, done.stdout.strip(), done.stderr


def test_cli_no_engine_writes_printable_html():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'o'
        code, stdout, stderr = run_without_engines(write_sheet(tmp), '--out', out)
        assert code == 3, (code, stdout, stderr)
        assert stdout.startswith('ERROR no PDF engine'), stdout
        assert NO_ENGINE_QUESTION in stdout, stdout
        html_files = list(out.glob('*-v1.html'))
        assert len(html_files) == 1 and not list(out.glob('*.pdf')), list(out.iterdir())
        assert str(html_files[0]) in stdout, stdout


# Browser engine (standard library; a fake browser stands in for Edge/Chrome)

FAKE_BROWSER = r"""
import json, os, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import unquote, urlparse
args = sys.argv[1:]
here = Path(__file__)
behaviour = json.loads(here.with_name('pages.json').read_text(encoding='utf-8'))
if os.environ.get('FAKE_BROWSER_CHILD') != '1':
    with here.with_name('calls.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(args) + '\n')
    if behaviour.get('detach'):  # like the Edge launcher: start the real browser and return at once
        flags = 0x00000008 | 0x00000200 if sys.platform == 'win32' else 0
        subprocess.Popen([sys.executable, str(here), *args], env=dict(os.environ, FAKE_BROWSER_CHILD='1'),
                         creationflags=flags, start_new_session=sys.platform != 'win32',
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raise SystemExit(0)
else:
    profile = next(a.split('=', 1)[1] for a in args if a.startswith('--user-data-dir='))
    os.chdir(profile)  # like a real browser, keep the profile folder in use
    here.with_name('child.pid').write_text(str(os.getpid()), encoding='utf-8')
    if behaviour.get('hang'):
        time.sleep(3600)
    time.sleep(behaviour.get('delay', 0))
if behaviour.get('write') is False:
    raise SystemExit(0)
target = next(a.split('=', 1)[1] for a in args if a.startswith('--print-to-pdf='))
path = unquote(urlparse(args[-1]).path)
source = Path(path.lstrip('/') if sys.platform == 'win32' else path)
preset = re.search(r'data-preset="(\d+)"', source.read_text(encoding='utf-8')).group(1)
pages = behaviour['pages'][preset]
body = b'%PDF-1.4\n1 0 obj<</Type /Catalog /Pages 2 0 R>>endobj\n2 0 obj<</Type /Pages /Count ' + str(pages).encode() + b'>>endobj\n'
Path(target).write_bytes(body + (b'' if behaviour.get('truncate') else b'%%EOF\n'))
"""


def fake_browser(folder, pages, **behaviour):
    folder = Path(folder)
    script = folder / 'fake_browser.py'
    script.write_text(FAKE_BROWSER, encoding='utf-8')
    (folder / 'pages.json').write_text(json.dumps({'pages': {str(k): v for k, v in pages.items()}, **behaviour}),
                                       encoding='utf-8')
    return [sys.executable, str(script)]


def calls(folder):
    log = Path(folder) / 'calls.jsonl'
    return [json.loads(line) for line in log.read_text(encoding='utf-8').splitlines()] if log.exists() else []


def test_html_structure():
    sheet = rs.load_sheet(sheet_with())
    page = rs.to_html(sheet, 2)
    assert page.startswith('<!doctype html>') and 'data-preset="2"' in page
    assert f"font-size: {rs.PRESETS[2]['body']}pt" in page
    assert 'columns: 2' in page and 'size: letter' in page
    assert rs._css_string(rs.UNCONFIRMED_NOTE) in page
    assert '<script' not in page and 'http://' not in page and 'https://' not in page
    guide = rs.load_sheet(sheet_with(lambda d: d.update(kind='study-guide')))
    assert 'columns: 1' in rs.to_html(guide, 1)
    confirmed = rs.load_sheet(sheet_with(lambda d: d['allowance'].update(status='confirmed', paper='a4')))
    page = rs.to_html(confirmed, 0)
    assert rs._css_string(rs.UNCONFIRMED_NOTE) not in page and 'size: A4' in page


def test_html_escapes_and_keeps_code_literal():
    def mutate(d):
        d['title'] = 'A <b> & "c"'
        d['sections'][0]['blocks'] = [{'type': 'text', 'text': 'x^{2} **bold** `a**b**<c>` </style>'},
                                      {'type': 'code', 'text': 'if a < b:\n    print("**x**")'}]
    page = rs.to_html(rs.load_sheet(sheet_with(mutate)), 0)
    assert 'A &lt;b&gt; &amp;' in page
    assert 'x<sup>2</sup> <b>bold</b> <code>a**b**&lt;c&gt;</code> &lt;/style&gt;' in page, page
    assert 'if a &lt; b:\n    print(' in page and '**x**' in page


def test_html_high_weight_and_blocks():
    page = rs.to_html(rs.load_sheet(sheet_with()), 0)
    assert 'class="section high"' in page
    for marker in ('class="block cue"', 'class="grid steps"', 'class="block data"'):
        assert marker in page, marker


def test_browser_fit_picks_most_spacious_that_fits():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {0: 3, 1: 3, 2: 2, 3: 2, 4: 1})
        out = Path(tmp) / 'out'
        checks = rs.render(rs.load_sheet(sheet_with()), out, engine='browser', browser=browser)
        assert checks['engine'] == 'browser' and checks['preset'] == 2 and checks['pages'] == 2, checks
        assert checks['missing_glyphs'] == 'unchecked' and checks['column_fill'] is None
        assert checks['browser'] == 'fake_browser.py'
        stem = checks['pdf'][:-4]
        assert (out / checks['pdf']).read_bytes().rstrip().endswith(b'%%EOF')
        assert (out / f'{stem}.html').is_file() and (out / f'{stem}.json').is_file() and (out / 'checks.json').is_file()
        assert 'data-preset="2"' in (out / f'{stem}.html').read_text(encoding='utf-8')
        made = calls(tmp)
        assert len(made) == 3, made  # presets 0, 1, 2 tried; stops at the first fit
        for args in made:
            profile = next(a.split('=', 1)[1] for a in args if a.startswith('--user-data-dir='))
            assert not Path(profile).exists() and out.resolve() not in Path(profile).resolve().parents
            assert '--headless' in args and '--no-pdf-header-footer' in args
        assert sorted(p.name for p in out.iterdir() if p.is_dir()) in ([], ['previews'])


def test_browser_respects_minimum_body():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {0: 3, 1: 3, 2: 3, 3: 2, 4: 1})
        sheet = rs.load_sheet(sheet_with(lambda d: d['allowance'].update(min_body=10)))
        try:
            rs.render(sheet, Path(tmp) / 'out', engine='browser', browser=browser)
        except rs.Overflow as error:
            assert 'browser engine' in error.reason and error.sections == []
        else:
            raise AssertionError('expected overflow: only presets 0-2 meet a 10pt minimum')
        assert not list((Path(tmp) / 'out').glob('*.pdf')) if (Path(tmp) / 'out').exists() else True


def test_browser_study_guide_single_print():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {0: 9, 1: 7, 2: 6, 3: 5, 4: 4})
        sheet = rs.load_sheet(sheet_with(lambda d: d.update(kind='study-guide')))
        checks = rs.render(sheet, Path(tmp) / 'out', engine='browser', browser=browser)
        assert checks['preset'] == 1 and checks['pages'] == 7 and len(calls(tmp)) == 1


def test_browser_code_width_estimate():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {i: 1 for i in range(5)})
        sheet = rs.load_sheet(sheet_with(lambda d: d['sections'][0]['blocks'].append(
            {'type': 'code', 'text': 'x = ' + 'a' * 120})))
        try:
            rs.render(sheet, Path(tmp) / 'out', engine='browser', browser=browser)
        except rs.Overflow as error:
            assert 'code line' in error.reason, error.reason
        else:
            raise AssertionError('a 124-character code line cannot fit a sheet column')
        assert calls(tmp) == []


def test_browser_missing_or_partial_pdf_is_an_error():
    for behaviour in ({'write': False}, {'truncate': True}):
        with tempfile.TemporaryDirectory() as tmp:
            browser = fake_browser(tmp, {i: 1 for i in range(5)}, **behaviour)
            out = Path(tmp) / 'out'
            try:
                rs.render(rs.load_sheet(sheet_with()), out, engine='browser', browser=browser, timeout=2)
            except rs.SheetError as error:
                assert 'browser' in str(error), error
            else:
                raise AssertionError(f'expected an error for {behaviour}')
            assert not out.exists() or not list(out.glob('*.pdf'))


def test_browser_keeps_earlier_round():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {i: 1 for i in range(5)})
        out = Path(tmp) / 'out'
        sheet = rs.load_sheet(sheet_with())
        rs.render(sheet, out, engine='browser', browser=browser)
        try:
            rs.render(sheet, out, engine='browser', browser=browser)
        except rs.SheetError as error:
            assert '--force' in str(error)
        else:
            raise AssertionError('an existing round was replaced without --force')


def test_pdf_page_count():
    assert rs.pdf_page_count(b'%PDF-1.4 <</Type /Pages /Count 2 /Kids [3 0 R 4 0 R]>> <</Type /Pages /Count 1>> %%EOF') == 2
    assert rs.pdf_page_count(b'%PDF-1.4 nothing') is None


def test_find_browser_uses_candidates():
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / 'msedge.exe'
        exe.write_text('', encoding='utf-8')
        saved = rs._browser_candidates
        try:
            rs._browser_candidates = lambda: [Path(tmp) / 'missing.exe', exe]
            assert rs.find_browser() == [str(exe)]
            rs._browser_candidates = lambda: []
            assert rs.find_browser() is None
        finally:
            rs._browser_candidates = saved


def pid_alive(pid):
    if sys.platform == 'win32':
        done = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True)
        return str(pid) in done.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def test_browser_waits_for_detached_launcher():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {i: 1 for i in range(5)}, detach=True, delay=1.0)
        checks = rs.render(rs.load_sheet(sheet_with()), Path(tmp) / 'out', engine='browser', browser=browser,
                           timeout=15)
        assert checks['pages'] == 1 and checks['leftover_profiles'] == [], checks


def test_browser_hanging_child_is_stopped_and_profile_removed():
    with tempfile.TemporaryDirectory() as tmp:
        browser = fake_browser(tmp, {i: 1 for i in range(5)}, detach=True, hang=True)
        try:
            rs.render(rs.load_sheet(sheet_with()), Path(tmp) / 'out', engine='browser', browser=browser, timeout=3)
        except rs.SheetError as error:
            assert 'did not write a complete PDF' in str(error), error
        else:
            raise AssertionError('a hanging browser must fail the render')
        pid = int((Path(tmp) / 'child.pid').read_text(encoding='utf-8'))
        assert not pid_alive(pid), f'browser child {pid} left running'
        profile = next(a.split('=', 1)[1] for a in calls(tmp)[0] if a.startswith('--user-data-dir='))
        assert not Path(profile).exists(), profile


def test_browser_rejects_block_taller_than_column():
    tall = {'type': 'code', 'text': '\n'.join(f'x{i} = {i}' for i in range(100))}
    for kind in ('exam-sheet', 'study-guide'):
        with tempfile.TemporaryDirectory() as tmp:
            browser = fake_browser(tmp, {i: 1 for i in range(5)})
            sheet = rs.load_sheet(sheet_with(lambda d: (d.update(kind=kind), d['sections'][0]['blocks'].append(tall))))
            try:
                rs.render(sheet, Path(tmp) / 'out', engine='browser', browser=browser)
            except rs.Overflow as error:
                assert 'taller than one column' in error.reason and error.sections, (kind, error.reason)
            else:
                raise AssertionError(f'{kind}: a 100-line code block cannot fit one column')
            assert calls(tmp) == []


def test_html_wraps_long_tokens():
    page = rs.to_html(rs.load_sheet(sheet_with()), 0)
    assert 'table-layout: fixed' in page
    rule = next(line for line in page.splitlines() if line.startswith('th, td'))
    assert 'overflow-wrap: anywhere' in rule, rule
    assert 'column-fill: auto; overflow-wrap: anywhere' in page  # body rule: prose and inline code wrap


def pdf_chars(path):
    """(text, [(char, left, right)]) for page 1, or None without pypdfium2."""
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return None
    document = pdfium.PdfDocument(str(path))
    try:
        text = ''.join(document[i].get_textpage().get_text_range() for i in range(len(document)))
        page = document[0].get_textpage()
        boxes = []
        for k in range(page.count_chars()):
            char = page.get_text_range(k, 1)
            if char.strip():
                left, _, right, _ = page.get_charbox(k)
                boxes.append((char, left, right))
        return text, boxes
    finally:
        document.close()


def browser_test_long_tokens_stay_in_columns():
    long_cell = 'very_long_identifier_' * 6
    def mutate(d):
        d['sections'][0]['blocks'] = [
            {'type': 'table', 'header': ['Name', 'Meaning'], 'rows': [[long_cell, 'x'], ['y', long_cell]]},
            {'type': 'text', 'text': 'See ' + long_cell + ' and `' + long_cell + '`.'}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        code, stdout, stderr = run(write_sheet(tmp, sheet_with(mutate)), '--out', out, '--engine', 'browser')
        assert code == 0, (code, stdout, stderr)
        checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
        found = pdf_chars(out / checks['pdf'])
        if found is None:
            return  # character positions need pypdfium2
        width = rs.PAGE_SIZES['letter'][0]
        col_w = (width - 2 * rs.MARGIN - rs.COLUMN_GAP) / 2
        left_col = (rs.MARGIN - 1, rs.MARGIN + col_w + 1)
        right_col = (rs.MARGIN + col_w + rs.COLUMN_GAP - 1, width - rs.MARGIN + 1)
        stray = [(c, round(l), round(r)) for c, l, r in found[1]
                 if not any(lo <= l and r <= hi for lo, hi in (left_col, right_col))]
        assert not stray, stray[:10]


def browser_test_real_example():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'out'
        code, stdout, stderr = run(write_sheet(tmp), '--out', out, '--engine', 'browser')
        assert code == 0 and 'engine=browser' in stdout, (code, stdout, stderr)
        checks = json.loads((out / 'checks.json').read_text(encoding='utf-8'))
        assert 1 <= checks['pages'] <= 2, checks
        data = (out / checks['pdf']).read_bytes()
        assert data.startswith(b'%PDF') and rs.pdf_page_count(data) == checks['pages']
        assert [p.name for p in out.iterdir() if p.is_dir()] in ([], ['previews'])
        found = pdf_chars(out / checks['pdf'])
        if found is not None:
            for expected in (EXAMPLE['title'], EXAMPLE['course'], 'Exam use unconfirmed', 'Interaction model'):
                assert expected in found[0], expected


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
    if rs.find_browser():
        tests += [value for name, value in sorted(globals().items()) if name.startswith('browser_test_')]
    else:
        print('SKIP real-browser checks: no Edge/Chrome/Chromium found')
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
