#!/usr/bin/env python3
"""Old-vs-new exam-sheet comparison for the finals post (T017/T013): v2.0.1 versus the final T017 skill.

Reuses tests/run_feature_pilot.py unchanged (fixtures, 4 scripted turns, isolation, scoring inputs).
Arms: Old = v2.0.1 (20bb271), New = 453f74c (codex-approved, native PDF writer). gpt-6-luna, serial,
3 sessions per arm, alternating which arm runs first. On this host v2.0.1 makes PDFs with PyMuPDF, which is
installed in the system Python; that is the comparison a student on this machine would see.
Default invocation makes no model calls.
"""
from pathlib import Path
import argparse, importlib.util, shutil, tempfile, uuid

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('feature_pilot', HERE / 'run_feature_pilot.py')
fp = importlib.util.module_from_spec(spec); spec.loader.exec_module(fp)
fp.NEW, fp.OLD = '453f74c', '20bb271'
REPORT = fp.ROOT / 'tests/reports/2026-11-19-sheet-compare'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', action='store_true', help='make 24 turns: 3 sessions x 2 arms x 4 turns')
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--cli', default=shutil.which('codex'))
    ap.add_argument('--auth', type=Path, default=Path.home() / '.codex' / 'auth.json')
    ap.add_argument('--report', type=Path, default=REPORT)
    ap.add_argument('--work', type=Path)
    a = ap.parse_args()
    if not a.run:
        print(f'NO MODEL CALLS: --run would make {a.reps * 2 * 4} turns.'); return 0
    if not a.cli: raise SystemExit('Codex CLI not found')
    report = a.report.resolve()
    work = (a.work or Path(tempfile.gettempdir()) / f'sheet-compare-{uuid.uuid4().hex}').resolve()
    version = fp.prepare(report, work, a.cli)
    print(f'CLI {version}; Old={fp.OLD}; New={fp.NEW}; report={report}; work={work}', flush=True)
    for rep in range(1, a.reps + 1):
        for arm in (('Old', 'New') if rep % 2 else ('New', 'Old')):
            fp.session(a.cli, report, work, arm, 'sheet', rep, [1, 2, 3, 4], a.auth)
            print(f'done sheet-{arm}-rep{rep}', flush=True)
    print('COMPARE COMPLETE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
