"""Regression checks for tests/run_controlled_pilot.py using a fake CLI. No model calls, no real login."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / 'tests/run_controlled_pilot.py'

FAKE_CLI = r'''
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
if args == ['--version']:
    print('fake-cli 0.0'); sys.exit(0)
home = Path(os.environ['CODEX_HOME'])
with open(home / 'calls.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps({'argv': args, 'auth_present': (home / 'auth.json').exists(),
                        'extra_codex_env': sorted(k for k in os.environ if k.startswith('CODEX_') and k != 'CODEX_HOME')}) + '\n')
sys.stdin.read()
mode = os.environ.get('FAKE_MODE', 'ok')
print(json.dumps({'type': 'thread.started', 'thread_id': 'thread-fake'}))
if mode == 'external':
    print(json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution', 'id': 'cmd1',
          'command': 'cat ' + str(Path.home() / '.agents' / 'skills' / 'x' / 'SKILL.md')}}))
print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',
      'text': 'reply mentioning ' + str(Path.cwd() / 'progress.md')}}))
if mode == 'crash':
    print('{not json'); sys.exit(3)
print(json.dumps({'type': 'turn.completed', 'usage': {'input_tokens': 10, 'cached_input_tokens': 0, 'output_tokens': 2}}))
'''


def run(tmp, phase, name, report, mode='ok', extra=()):
    env = dict(__import__('os').environ, FAKE_MODE=mode, CODEX_SANDBOX='should-be-stripped', PYTHONUTF8='1')
    cmd = [sys.executable, str(HARNESS), phase, '--work', str(tmp / name), '--arms', 'A1',
           '--report', str(report), '--cli', str(tmp / 'fake_cli.py'), '--auth', str(tmp / 'auth.json'), *extra]
    return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)


def auth_copies(tmp):
    return [p for p in tmp.rglob('auth.json') if p.parent != tmp]


def main():
    spec = importlib.util.spec_from_file_location('pilot', HARNESS)
    pilot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pilot)
    home, bs = str(Path.home()), chr(92)
    for level in (1, 2, 4, 8):
        text = 'x ' + home.replace(bs, bs * level) + bs * level + 'file ' + str(ROOT).replace(bs, bs * level)
        cleaned = pilot.scrub(text, Path('C:/nowhere'))
        assert Path.home().name not in cleaned and ROOT.name not in cleaned, level
    flags, _ = pilot.skill_isolation_flags()
    assert 'skills.bundled.enabled=false' in flags and any(f.startswith('skills.config=[') for f in flags)

    with tempfile.TemporaryDirectory(prefix='cooked-pilot-check-') as t:
        tmp = Path(t)
        (tmp / 'fake_cli.py').write_text(FAKE_CLI, encoding='utf-8')
        (tmp / 'auth.json').write_text('{"dummy": true}', encoding='utf-8')

        # 1. Complete two-phase run.
        report = tmp / 'report-ok'
        r = run(tmp, 'phase1', 'work-ok', report)
        assert r.returncode == 0, r.stderr
        assert not auth_copies(tmp), 'credentials left after phase 1'
        calls = [json.loads(x) for x in (tmp / 'work-ok/home-A1/calls.jsonl').read_text(encoding='utf-8').splitlines()]
        assert len(calls) == 6 and all(c['auth_present'] for c in calls)
        assert all(not c['extra_codex_env'] for c in calls), 'inherited CODEX_* variables reached the CLI'
        assert all('skills.bundled.enabled=false' in c['argv'] for c in calls)
        assert (report / 'runs/A1/turn-01.stdout.txt').is_file()
        reply = (report / 'runs/A1/response-01.md').read_text(encoding='utf-8')
        assert Path.home().name not in reply and 'work-ok' not in reply, reply
        r = run(tmp, 'phase2', 'work-ok', report)
        assert r.returncode != 0 and 'turn7-answers' in r.stderr, 'phase 2 must need turn-7 answers'
        (tmp / 'work-ok/turn7-answers.json').write_text('{"A1": "my answer"}', encoding='utf-8')
        r = run(tmp, 'phase2', 'work-ok', report)
        assert r.returncode == 0, r.stderr
        assert not auth_copies(tmp), 'credentials left after phase 2'
        manifest = json.loads((report / 'manifest.json').read_text(encoding='utf-8'))
        assert 'runs/A1/response-11.md' in manifest and 'results-phase2.json' in manifest
        before = {p: p.read_bytes() for p in report.rglob('*') if p.is_file()}

        # 2. A completed report cannot be modified again.
        r = run(tmp, 'phase2', 'work-ok', report)
        assert r.returncode != 0 and 'already complete' in r.stderr
        # 3. Phase 2 cannot be pointed at another report.
        other = tmp / 'report-other'
        other.mkdir()
        (other / 'keep.md').write_text('untouched ' + home, encoding='utf-8')
        r = run(tmp, 'phase2', 'work-ok', other)
        assert r.returncode != 0 and 'another report' in r.stderr
        assert (other / 'keep.md').read_text(encoding='utf-8') == 'untouched ' + home
        assert before == {p: p.read_bytes() for p in report.rglob('*') if p.is_file()}, 'completed report changed'
        assert not auth_copies(tmp)

        # 4. Global-skill access invalidates the session, keeps evidence, removes credentials.
        report = tmp / 'report-external'
        r = run(tmp, 'phase1', 'work-external', report, mode='external')
        assert r.returncode != 0 and 'external_skill_access' in r.stderr
        failure = json.loads((report / 'runs/A1/turn-01.failure.json').read_text(encoding='utf-8'))
        assert failure['external_skill_commands'] == ['cmd1']
        assert (report / 'runs/A1/turn-01.stdout.txt').read_text(encoding='utf-8').strip()
        assert not auth_copies(tmp), 'credentials left after an invalidated session'
        r = run(tmp, 'phase2', 'work-external', report)
        assert r.returncode != 0 and 'Phase 1 did not complete' in r.stderr

        # 5. Malformed output and a non-zero exit keep raw output and remove credentials.
        report = tmp / 'report-crash'
        r = run(tmp, 'phase1', 'work-crash', report, mode='crash')
        assert r.returncode != 0 and 'incomplete' in r.stderr
        assert '{not json' in (report / 'runs/A1/turn-01.stdout.txt').read_text(encoding='utf-8')
        assert (report / 'runs/A1/files-after-01').is_dir()
        assert not auth_copies(tmp), 'credentials left after a failed call'

    print('PASS: path scrub levels, global-skill isolation flags and access gate, CODEX_* env stripping, '
          'credential removal on success and three failure paths, report binding, completed-report guard, '
          'raw output kept before parsing. Fake CLI only; no model behaviour is tested.')


if __name__ == '__main__':
    main()
