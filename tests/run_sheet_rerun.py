#!/usr/bin/env python3
"""T017 follow-up: rerun only the New-arm exam-sheet sessions of the T016 pilot on the fixed skill.

Same fixtures, prompts, model (gpt-6-luna), isolation and scoring as tests/run_feature_pilot.py; only the
skill revision changes (T017 browser print fallback, codex-approved c72a32a). The host keeps no ReportLab
in its system Python, as in T016, so the browser path is what gets exercised.
Default invocation performs no model calls.
"""
from pathlib import Path
import argparse, importlib.util, shutil, tempfile, uuid

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('feature_pilot', HERE / 'run_feature_pilot.py')
fp = importlib.util.module_from_spec(spec); spec.loader.exec_module(fp)
fp.NEW = 'c72a32a'  # T017 head approved by codex in review round 3
REPORT = fp.ROOT / 'tests/reports/2026-11-19-sheet-rerun'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run-smoke', action='store_true', help='make 1 diagnostic model turn (New sheet, turn 1)')
    ap.add_argument('--run-main', action='store_true', help='make 8 turns: New sheet reps 1-2, turns 1-4')
    ap.add_argument('--cli', default=shutil.which('codex'))
    ap.add_argument('--auth', type=Path, default=Path.home() / '.codex' / 'auth.json')
    ap.add_argument('--report', type=Path)
    ap.add_argument('--work', type=Path)
    a = ap.parse_args()
    if a.run_smoke == a.run_main:
        print('NO MODEL CALLS: pass exactly one of --run-smoke or --run-main.'); return 0
    if not a.cli: raise SystemExit('Codex CLI not found')
    report = (a.report or (REPORT.with_name(REPORT.name + '-smoke') if a.run_smoke else REPORT)).resolve()
    work = (a.work or Path(tempfile.gettempdir()) / f'sheet-rerun-{uuid.uuid4().hex}').resolve()
    version = fp.prepare(report, work, a.cli)
    print(f'CLI {version}; New={fp.NEW}; report={report}; work={work}')
    if a.run_smoke:
        fp.session(a.cli, report, work, 'New', 'sheet', 99, [1], a.auth)
        print('SMOKE COMPLETE (diagnostic; excluded from statistics)')
    else:
        for rep in (1, 2):
            fp.session(a.cli, report, work, 'New', 'sheet', rep, [1, 2, 3, 4], a.auth)
        print('MAIN COMPLETE: 8 turns')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
