"""Check the mock-exam renderer: validation, escaping, key separation, overwrite refusal.

Structure only; it cannot judge whether generated questions are academically correct.
"""
from pathlib import Path
import copy
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.dont_write_bytecode = True
import render_mock_exam as rm  # noqa: E402

EXAMPLE = json.loads((SKILL / 'assets/mock-exam-example.json').read_text(encoding='utf-8'))


def rejects(mutate, expected):
    exam = copy.deepcopy(EXAMPLE)
    mutate(exam)
    try:
        rm.render(exam)
    except rm.ExamError as error:
        assert expected in str(error), f'Expected {expected!r} in:\n{error}'
        return
    raise AssertionError(f'Renderer accepted an invalid exam ({expected})')


def check():
    worksheet, key, warnings = rm.render(copy.deepcopy(EXAMPLE))
    assert warnings == [], warnings
    assert '{{' not in worksheet and '{{' not in key
    assert worksheet.count('class="question"') == len(EXAMPLE['questions'])
    for q in EXAMPLE['questions']:
        secret = [q['key']['explanation'], q['key']['verification'], *q['key'].get('option_notes', {}).values()]
        if q.get('personal_target'):
            secret.append(q['personal_target'])
        if q['type'] not in rm.CHOICE:
            secret.append(q['key']['answer'])
        for value in secret:
            plain = rm.visible_text(rm.inline(value))
            if len(plain.strip()) >= 6:  # Short answers such as "2" can legitimately appear in prompts.
                assert plain.strip() not in rm.visible_text(worksheet), f'Key text leaked: {value[:40]}'
            assert plain.strip() in rm.visible_text(key), f'Key text missing from key: {value[:40]}'
    meta = json.loads(worksheet.split('id="artifact-data">')[1].split('</script>')[0])
    assert set(meta) == {'schema_version', 'package_version', 'artifact_id', 'artifact_version', 'artifact_type',
                         'course', 'exam', 'key_file'}, meta
    assert 'option_notes' not in worksheet and '"evidence"' not in worksheet and 'Answer key:' not in worksheet
    assert worksheet.count('data-shared') == 0 and worksheet.count('id="shared-tickets"') == 1
    assert 'Suggested practice time (estimate): 20 minutes' in worksheet

    plugin_version = json.loads((ROOT / 'plugins/gpt-im-cooked/plugin.json').read_text(encoding='utf-8'))['version']
    assert rm.PACKAGE_VERSION == plugin_version, 'render_mock_exam.PACKAGE_VERSION must match plugin.json'

    hostile = copy.deepcopy(EXAMPLE)
    hostile['title'] = '<script>alert(1)</script>'
    hostile['questions'][0]['options'][0]['text'] = '</script><img src=x onerror=alert(1)>'
    hostile['course'] = 'Course </script><script>alert(2)</script>'
    page, _, _ = rm.render(hostile)
    assert '<script>alert' not in page and '<img src=x' not in page
    assert page.count('<script') == 2, 'Only the data block and the template script may be scripts'

    rejects(lambda e: e['questions'][1]['key'].update(answer=['A', 'B']), 'exactly one correct option')
    rejects(lambda e: e['questions'][0]['key']['option_notes'].pop('C'), 'must explain every option')
    rejects(lambda e: e['questions'][2]['key'].update(evidence='Unresolved'), 'fix or omit')
    rejects(lambda e: e['questions'][2]['key'].update(evidence='Pretty sure'), 'key.evidence must be one of')
    rejects(lambda e: e['questions'][0].update(source='S9'), 'declared source IDs')
    rejects(lambda e: e['questions'][1].update(id='q1'), 'unique slug id')
    rejects(lambda e: e['questions'][1].update(shared_ref='missing'), 'not declared in shared')
    rejects(lambda e: e['questions'][1]['key'].update(answer=['Z']), 'option ids from this question')
    rejects(lambda e: e['questions'][3].update(options=[{'id': 'A', 'text': 'x'}]), 'only single/multi')
    rejects(lambda e: e['questions'][0]['prompt'].append({'svg': '<svg onload="x()"></svg>', 'alt': 'a'}), 'event handlers')
    rejects(lambda e: e['questions'][0]['prompt'].append({'svg': '<svg></svg>'}), 'needs alt text')
    rejects(lambda e: e['questions'][0]['prompt'].append({'image': 'https://example.com/a.png', 'alt': 'a'}), 'network URL')
    rejects(lambda e: e['questions'][0]['prompt'].append({'table': {'columns': ['a', 'b'], 'rows': [['1']]}}), 'same width')
    rejects(lambda e: e['questions'][2]['prompt'].append(e['questions'][2]['key']['explanation']), 'key-only text appears')
    rejects(lambda e: e['questions'][1]['prompt'].append(e['questions'][1]['personal_target']), 'key-only text appears')
    rejects(lambda e: e.update(time_estimate={'minutes': 20}), 'time_estimate')
    # Bypasses found in review of the first version.
    rejects(lambda e: e['questions'][0]['prompt'].append({'svg': '<svg/onload=alert(1)></svg>', 'alt': 'a'}), 'event handlers')
    rejects(lambda e: e['questions'][0]['prompt'].append(
        {'svg': '<svg><a href="java&#115;cript:alert(1)">x</a></svg>', 'alt': 'a'}), 'event handlers')
    rejects(lambda e: e['questions'][0]['prompt'].append(
        {'svg': '<svg><style>@import "https://x.test/a.css";</style></svg>', 'alt': 'a'}), 'external links')
    rejects(lambda e: e['questions'][0]['prompt'].append({'image': ' HTTPS://x.test/a.png', 'alt': 'a'}), 'network URL')
    rejects(lambda e: e['questions'][0]['prompt'].append({'image': 'data:text/html,<b>x</b>', 'alt': 'a'}), 'data:image/')
    rejects(lambda e: e['questions'].__setitem__(0, 'oops'), 'questions[0] must be an object')
    rejects(lambda e: e['questions'][0].update(options='A, B'), 'list of {id, text} objects')
    rejects(lambda e: e.update(artifact_version='1 final/2'), 'artifact_version must be')
    safe = copy.deepcopy(EXAMPLE)
    safe['questions'][0]['prompt'].append(
        {'svg': '<svg viewBox="0 0 10 10"><image href="data:image/png;base64,AA"/><use href="#m"/></svg>', 'alt': 'a'})
    rm.render(safe)  # data: images and in-document references stay allowed

    with tempfile.TemporaryDirectory(prefix='cooked-mock-') as temp:
        script = SKILL / 'scripts/render_mock_exam.py'
        example = SKILL / 'assets/mock-exam-example.json'
        run = lambda *extra: subprocess.run([sys.executable, '-B', str(script), str(example), '--out', temp, *extra],
                                            capture_output=True, text=True)
        first = run()
        assert first.returncode == 0, first.stderr
        assert json.loads(first.stdout)['valid'] is True
        second = run()
        assert second.returncode == 1 and 'Refusing to replace' in second.stderr
        assert run('--force').returncode == 0
        assert sorted(p.name for p in Path(temp).iterdir()) == ['fictional-stats-mock-a-v1.0-key.html', 'fictional-stats-mock-a-v1.0.html']
    print('PASS: example renders, key text stays out of the worksheet, escaping, 24 invalid-exam rejections, overwrite refusal.')
    print('Structure only; question correctness still needs the checked key and tutor review.')


if __name__ == '__main__':
    check()
