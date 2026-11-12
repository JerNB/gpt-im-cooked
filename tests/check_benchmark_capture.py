"""Exercise actual benchmark failure paths with a fake CLI; no real login/quota used."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def check(mode):
    spec = importlib.util.spec_from_file_location('benchmark_capture_' + mode, ROOT / 'tests/benchmark_record_cost.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    with tempfile.TemporaryDirectory(prefix='capture-fixture-') as temp:
        home = Path(temp) / 'synthetic-home'
        (home / '.codex').mkdir(parents=True)
        (home / '.codex/auth.json').write_text('{"synthetic_fixture":true}', encoding='utf-8')
        runner.REPORT = Path(temp) / 'report'
        runner.TURNS = ['Synthetic fixture turn, not a model request.']
        runner.REVISIONS = {'baseline': '97be172', 'v2': '97be172'}
        original = subprocess.check_output
        original_run = subprocess.run

        def output(cmd, **kwargs):
            return 'synthetic-cli\n' if cmd[0] == 'synthetic-codex' else original(cmd, **kwargs)

        def execute(cmd, **kwargs):
            if cmd[0] != 'synthetic-codex':
                return original_run(cmd, **kwargs)
            (Path(kwargs['cwd']) / 'artifact.html').write_text('<p>Synthetic artifact before failure</p>', encoding='utf-8')
            if mode == 'timeout':
                raise subprocess.TimeoutExpired(cmd, 600, output=b'{"type":"partial"}\n', stderr=b'synthetic timeout')
            if mode == 'malformed':
                return subprocess.CompletedProcess(cmd, 0, 'synthetic non-JSON output\n', '')
            return subprocess.CompletedProcess(cmd, 1, json.dumps({'type': 'turn.failed', 'error': {'message': 'synthetic quota failure'}}) + '\n', 'synthetic stderr')

        with patch.object(Path, 'home', return_value=home), \
             patch.object(runner.shutil, 'which', return_value='synthetic-codex'), \
             patch.object(runner.subprocess, 'check_output', side_effect=output), \
             patch.object(runner.subprocess, 'run', side_effect=execute), \
             patch.object(sys, 'argv', ['benchmark', '--pairs', '1']):
            try:
                runner.main()
            except RuntimeError:
                pass
            else:
                raise AssertionError('Expected the synthetic failed call to fail')
            try:
                runner.main()
            except FileExistsError:
                pass
            else:
                raise AssertionError('Partial evidence must block a new run in the same directory')
        run = runner.REPORT / 'runs/pair-1-baseline'
        assert (run / 'final-study/artifact.html').read_text(encoding='utf-8') == '<p>Synthetic artifact before failure</p>'
        assert (run / 'turn-01.jsonl').read_text(encoding='utf-8').strip()
        assert (run / 'turn-01.execution.json').is_file()
        assert (runner.REPORT / 'partial-results.json').is_file()
        assert not list(runner.REPORT.rglob('auth.json')), 'Authentication must never be archived'
        assert not (runner.REPORT / 'results.json').exists(), 'Failed run must not masquerade as complete'


if __name__ == '__main__':
    for case in ('quota', 'timeout', 'malformed'):
        check(case)
    spec = importlib.util.spec_from_file_location('capture_sync', ROOT / 'tests/benchmark_record_cost.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix='capture-sync-') as temp:
        root = Path(temp)
        run, output = root / 'study', root / 'archive'
        run.mkdir()
        (run / 'draft.html').write_text('synthetic draft', encoding='utf-8')
        module.capture_study(run, output, root)
        (run / 'draft.html').unlink()
        (run / 'final.html').write_text('synthetic final', encoding='utf-8')
        module.capture_study(run, output, root)
        assert not (output / 'final-study/draft.html').exists()
        assert (output / 'final-study/final.html').is_file()
        assert json.loads((output / 'workspace-files.json').read_text())['files'] == ['final.html']
    print('PASS: synthetic quota/timeout/malformed CLI failures retain artifacts/raw output/metadata; no auth or false complete results.')
