"""Reproduce local PR3 checks; --phase model opts into real Codex quota usage.

All inputs are synthetic. Existing releases/reports are never overwritten.
Record timings are warm-process helper timings, not model latency or token cost.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import platform
import statistics
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKILL = 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
REPORT = ROOT / 'tests/reports/2026-11-11-update'
REFS = {'baseline': '0dc295bf7fc9f6bc614f659d819676bf0a53b6de',
        'candidate': '97be1720f890745b3b59be52ad9ec3dea740393e'}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8', newline='\n')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean(text):
    for path, label in [(str(ROOT), '<REPO>'), (str(Path.home()), '<USER_HOME>')]:
        text = text.replace(path, label).replace(path.replace('\\', '/'), label).replace(path.replace('\\', '\\\\'), label)
    return text


def freeze(ref, target):
    archive = subprocess.check_output(['git', 'archive', '--format=zip', ref, SKILL], cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(archive)) as files:
        for name in files.namelist():
            if not name.endswith('/'):
                path = target / Path(name).relative_to(SKILL)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(files.read(name))


def synthetic_record(rows):
    history = ''.join(f'| 2026-11-01 | historic-{i:05} / Q1 | C1 | 2/8 with denominator explanation | '
                      'Correct | Earlier teaching | Instructor key | Synthetic archived attempt; retain original reasoning. |\n'
                      for i in range(rows))
    return ('# Learning record\n\n## Concepts\n\n'
            '| Concept ID | Concept | Status | Evidence | Next task |\n|---|---|---|---|---|\n'
            '| C1 | Conditional probability | Improving | Same-structure successes | Transfer check |\n\n'
            '## Attempt history\n\n| Date | Attempt | Concept | Answer | Outcome | Assistance | Evidence | Feedback |\n'
            '|---|---|---|---|---|---|---|---|\n' + history + '\n## Next session\n\n- Retain the original plan.\n')


def record_trials(sources, repeats, sizes):
    modules = {arm: load('record_' + arm, path / 'scripts/record_io.py') for arm, path in sources.items()}
    samples = []
    fragment = '| C1 | Conditional probability | Improving | More same-structure successes | Changed-demand transfer |'
    for size in sizes:
        old = synthetic_record(size).encode()
        with tempfile.TemporaryDirectory(prefix='cooked-record-timing-') as temp:
            base = Path(temp)
            record, part = base / 'record.md', base / 'fragment.md'
            record.write_bytes(old)
            part.write_bytes(fragment.encode())
            modules['candidate'].update_section(record, 'Concepts', part, hashlib.sha256(old).hexdigest(),
                                                'upsert-rows', 'Concept ID')
            expected = record.read_bytes()
            assert expected.split(b'## Attempt history')[1] == old.split(b'## Attempt history')[1]
            for repetition in range(-1, repeats):  # one unreported warmup per arm/size
                order = ['baseline', 'candidate'] if repetition % 2 == 0 else ['candidate', 'baseline']
                for arm in order:
                    module = modules[arm]
                    record.write_bytes(old)  # fixture reset and supplied-input preparation excluded from timing
                    candidate = base / 'candidate.md'
                    candidate.write_bytes(expected if arm == 'baseline' else fragment.encode())
                    start = time.perf_counter_ns()
                    read = module.read_record(record) if arm == 'baseline' else module.read_section(record, 'Concepts')
                    after_read = time.perf_counter_ns()
                    result = (module.commit_record(record, candidate, read['sha256']) if arm == 'baseline' else
                              module.update_section(record, 'Concepts', candidate, read['sha256'], 'upsert-rows', 'Concept ID'))
                    finish = time.perf_counter_ns()
                    assert record.read_bytes() == expected
                    assert Path(str(record) + '.bak').read_bytes() == old
                    assert not Path(str(record) + '.lock').exists()
                    if repetition >= 0:
                        # Paths omitted from payload size so random temporary names do not affect the proxy.
                        read = {k: v for k, v in read.items() if k != 'backup'}
                        result = {k: v for k, v in result.items() if k != 'backup'}
                        response_bytes = len(json.dumps(read).encode()) + len(json.dumps(result).encode())
                        samples.append({'arm': arm, 'history_rows': size, 'repetition': repetition,
                                        'order': order, 'record_bytes': len(old), 'read_ns': after_read - start,
                                        'write_ns': finish - after_read, 'total_ns': finish - start,
                                        'supplied_content_bytes': candidate.stat().st_size,
                                        'response_json_bytes_without_paths': response_bytes,
                                        'payload_proxy_bytes': candidate.stat().st_size + response_bytes,
                                        'record_and_backup_match': True})
    return samples


def regression_checks():
    checks = []
    commands = [[sys.executable, '-B', 'tests/' + name] for name in
                ['check_state_io.py', 'check_mock_render.py', 'check_run_evidence.py', 'check_evidence_archive.py',
                 'validate_package.py']]
    commands += [['node', 'tests/' + name] for name in
                 ['check_mock_template.cjs', 'check_demo_state.cjs', 'check_concept_retry.cjs', 'check_evidence_chain.cjs']]
    for index, cmd in enumerate(commands, 1):
        start = time.perf_counter()
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        log = clean(proc.stdout + proc.stderr)
        path = REPORT / 'regressions' / f'{index:02}-{Path(cmd[-1]).stem}.txt'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(log, encoding='utf-8', newline='\n')
        checks.append({'command': ['python' if v == sys.executable else v for v in cmd],
                       'exit_code': proc.returncode, 'wall_seconds': time.perf_counter() - start,
                       'log': path.relative_to(REPORT).as_posix()})
        print('CHECK', cmd[-1], proc.returncode, flush=True)
    return checks


def renderer_trials(repeats):
    revisions = ['dac1bad', 'a32e170', 'f019ba2', 'cccacaf', 'a1265ff']
    behavior, timing = [], []
    cases = {'svg_embedded_document': '<svg></svg><iframe srcdoc="&lt;script&gt;alert(1)&lt;/script&gt;"></iframe>',
             'svg_tab_url': '<svg><a href="java&#x09;script:alert(1)">x</a></svg>',
             'svg_reserved_id': '<svg id="artifact-data"><text>Figure</text></svg>',
             'svg_quoted_angle_id': '<svg data-label="a > b" id="artifact-data"><text>Figure</text></svg>'}
    with tempfile.TemporaryDirectory(prefix='cooked-render-history-') as temp:
        for rev in revisions:
            source = Path(temp) / rev
            freeze(rev, source)
            module = load('renderer_' + rev, source / 'scripts/render_mock_exam.py')
            example = json.loads((source / 'assets/mock-exam-example.json').read_text(encoding='utf-8'))
            for name, markup in cases.items():
                exam = copy.deepcopy(example)
                exam['questions'][0]['prompt'].append({'svg': markup, 'alt': 'Synthetic test figure'})
                try:
                    module.render(exam)
                    outcome, error = 'accepted', None
                except module.ExamError as exc:
                    outcome, error = 'rejected', str(exc)
                behavior.append({'revision': rev, 'case': name, 'outcome': outcome, 'error': error})
            exam = copy.deepcopy(example)
            exam['questions'][0]['id'] = 'artifact-data'
            try:
                module.render(exam)
                outcome, error = 'accepted', None
            except module.ExamError as exc:
                outcome, error = 'rejected', str(exc)
            behavior.append({'revision': rev, 'case': 'question_reserved_id', 'outcome': outcome, 'error': error})
            if rev not in ('dac1bad', 'a1265ff'):
                continue
            for count in (5, 25, 100):
                exam = copy.deepcopy(example)
                exam['questions'] = [copy.deepcopy(example['questions'][i % 5]) for i in range(count)]
                for i, q in enumerate(exam['questions']):
                    q['id'] = f'item-{i + 1}'
                for repetition in range(-1, repeats):
                    start = time.perf_counter_ns()
                    worksheet, key, warnings = module.render(exam)
                    elapsed = time.perf_counter_ns() - start
                    if repetition >= 0:
                        timing.append({'revision': rev, 'questions': count, 'repetition': repetition,
                                       'render_ns': elapsed, 'worksheet_bytes': len(worksheet.encode()),
                                       'key_bytes': len(key.encode()), 'warnings': warnings})
    assert all(r['outcome'] == 'rejected' for r in behavior if r['revision'] == 'a1265ff')
    return behavior, timing


def summary(samples, keys, metric):
    groups = {}
    for row in samples:
        group = tuple(row[k] for k in keys)
        groups.setdefault(group, []).append(row[metric])
    return [{**dict(zip(keys, group)), 'metric': metric, 'n': len(values),
             'median': statistics.median(values), 'min': min(values), 'max': max(values),
             'p95_nearest_rank': sorted(values)[max(0, (95 * len(values) + 99) // 100 - 1)]}
            for group, values in groups.items()]


def local(repeats, sizes):
    if (REPORT / 'local-results.json').exists() or (REPORT / 'protocol-local.json').exists():
        raise SystemExit('Refusing to replace existing local results; choose a new report directory')
    sources = {}
    for arm, ref in REFS.items():
        sources[arm] = REPORT / 'sources' / arm
        freeze(ref, sources[arm])
    protocol = {'date_label': '2026-11-11 America/New_York', 'started_at': datetime.now(timezone.utc).isoformat(),
                'refs': REFS, 'python': sys.version, 'platform': platform.platform(),
                'node': subprocess.check_output(['node', '--version'], text=True).strip(),
                'repetitions_per_cell': repeats, 'warmups_per_cell': 1, 'sizes_history_rows': sizes,
                'record_design': 'Matched final bytes, full read/commit vs Concepts read/upsert; serial alternating AB/BA; setup excluded.',
                'timing_scope': 'Warm-process stdlib helper runtime on temporary local disk, includes lock/backup/fsync/write verification.',
                'payload_proxy': 'UTF-8 supplied content plus JSON read/write response bytes (backup paths omitted); not measured model tokens.',
                'disk_writes': 'Both methods rewrite the complete record and previous-byte backup. No reduced disk-write claim.',
                'renderer_comparator': 'First renderer dac1bad vs hardened a1265ff; pre-PR3 has no renderer, so no pre-PR3 render-speed claim.',
                'limits': 'Synthetic data, one host, repeated local timings not independent users; no learning, billing, or model-latency claim.'}
    dump(REPORT / 'protocol-local.json', protocol)
    checks = regression_checks()
    records = record_trials(sources, repeats, sizes)
    behavior, renders = renderer_trials(repeats)
    dump(REPORT / 'local-results.json', {'regressions': checks, 'record_trials': records,
                                       'renderer_behavior': behavior, 'renderer_trials': renders})
    dump(REPORT / 'local-summary.json', {'records': summary(records, ['arm', 'history_rows'], 'total_ns'),
                                       'payloads': summary(records, ['arm', 'history_rows'], 'payload_proxy_bytes'),
                                       'renderer': summary(renders, ['revision', 'questions'], 'render_ns')})
    print('LOCAL COMPLETE', len(records), 'record trials;', len(renders), 'render trials;',
          len(behavior), 'historical probes; regression failures:', sum(r['exit_code'] != 0 for r in checks))
    if any(r['exit_code'] != 0 for r in checks):
        raise SystemExit('Regression failures recorded; inspect the logs before interpreting benchmarks')


def model(pairs, directory='model', start_arm='baseline'):
    """Extend the repository's real CLI runner without changing old reports or its serial scheduling."""
    runner = load('record_benchmark', ROOT / 'tests/benchmark_record_cost.py')
    runner.REPORT = REPORT / directory
    runner.REVISIONS = {'baseline': REFS['baseline'], 'v2': REFS['candidate']}
    # A modest historical record exposes whole-file vs section saves without a huge artificial context.
    history = ''.join(f'| 2026-11-01 | archived-{i:03} / Q1 | C1 | See materials/packet.md Q1; synthetic earlier attempt | '
                      'Incorrect | Instructor explanation seen | Instructor key | Denominator used full sample. |\n'
                      for i in range(100))
    runner.RECORD = runner.RECORD.replace('## Import ledger', history + '\n## Import ledger')
    runner.TURNS = [runner.TURNS[0] + ' Save this reviewed attempt now.',
                    runner.TURNS[2] + ' Save this reviewed attempt now.',
                    runner.TURNS[4] + ' Save this reviewed attempt now.',
                    'Please create a short original 5-question mock exam from this course packet, with a mix of '
                    'choice and written/code questions, plus a separate checked answer key. Personalize from my '
                    'saved record while keeping course breadth. After creating the files, save a brief next-session '
                    'handoff and end this session.']
    sys.argv = [sys.argv[0], '--pairs', str(pairs), '--start-arm', start_arm]
    runner.main()
    # Preserve the original analyzer's validated cumulative-counter semantics.
    analyzer = load('record_analyzer', ROOT / 'tests/analyze_record_cost.py')
    analyzer.REPORT = runner.REPORT
    analyzer.main()


def report():
    """Build the human-readable report solely from saved measurements; no model calls."""
    raw = json.loads((REPORT / 'local-results.json').read_text(encoding='utf-8'))
    stats = json.loads((REPORT / 'local-summary.json').read_text(encoding='utf-8'))
    protocol = json.loads((REPORT / 'protocol-local.json').read_text(encoding='utf-8'))
    lines = ['# Post-PR3 test and benchmark report', '',
             'Started November 11 and continued November 12, 2026 (America/New_York). Raw timestamps are UTC.', '',
             '**Synthetic engineering evaluation. No measured learning, billing, or general reliability claim.**', '',
             '## Changes under test', '',
             f'Baseline: `{protocol["refs"]["baseline"]}`. Candidate: `{protocol["refs"]["candidate"]}` (PR3 merge, same tracked tree as `a1265ff`). '
             'Both source checkpoints declare package version 2.0.0; existing published archives remain unchanged.', '',
             '- Mock exams: JSON-to-template rendering, separate answer key, mixed question types, versioned filenames, stable export identities and exposure-aware history.',
             '- Records: section read/replace/append/upsert, composite ledger keys, whole-file conflict hash, lock, prior-byte backup and verified atomic write.',
             '- Review fixes: dangerous SVG/URL handling, complete-page ID checks via HTMLParser, code-fence/section integrity, unsaved exposure/history warnings.', '',
             'See [the full method](METHOD.md), [local protocol/environment](protocol-local.json), '
             '[raw samples](local-results.json), and [derived distributions](local-summary.json).', '',
             '## Regression checks', '', '| Command | Exit code | Wall seconds | Raw log |', '|---|---:|---:|---|']
    for row in raw['regressions']:
        lines.append(f'| `{" ".join(row["command"])}` | {row["exit_code"]} | {row["wall_seconds"]:.3f} | [log]({row["log"]}) |')
    lines += ['', f'{len(raw["regressions"])} scripts executed; '
              f'{sum(r["exit_code"] != 0 for r in raw["regressions"])} nonzero exits. Script counts are not individual assertion counts.', '',
              '## Record workflow benchmark', '',
              f'{len(raw["record_trials"])} measured workflows; {protocol["repetitions_per_cell"]} samples per arm/size, '
              'plus excluded warmups. Both arms produce byte-identical final records and prior-byte backups.', '',
              '| History rows | Initial bytes | Full payload bytes | Section payload bytes | Payload reduction | Full median / p95 ms | Section median / p95 ms |',
              '|---:|---:|---:|---:|---:|---:|---:|']
    for n in protocol['sizes_history_rows']:
        pick = lambda collection, arm: next(r for r in stats[collection] if r['arm'] == arm and r['history_rows'] == n)
        a, b = pick('records', 'baseline'), pick('records', 'candidate')
        x, y = pick('payloads', 'baseline')['median'], pick('payloads', 'candidate')['median']
        size = next(r['record_bytes'] for r in raw['record_trials'] if r['history_rows'] == n)
        lines.append(f'| {n:,} | {size:,} | {x:,.0f} | {y:,.0f} | {100 * (1-y/x):.3f}% | '
                     f'{a["median"]/1e6:.3f} / {a["p95_nearest_rank"]/1e6:.3f} | '
                     f'{b["median"]/1e6:.3f} / {b["p95_nearest_rank"]/1e6:.3f} |')
    lines += ['', '**Interpretation:** section updates reduce the content transmitted for this one-row change. '
              'They do not reduce whole-record/backup disk writes. Extra section parsing and integrity checks can '
              'make local helper execution slower; read/write phase timings are retained in the raw samples. '
              'Payload bytes are not measured tokens, model latency, or fees.', '',
              '## Renderer timings and known-defect probes', '',
              '| Questions | First-renderer median ms | Hardened median ms |', '|---:|---:|---:|']
    for n in (5, 25, 100):
        values = {r['revision']: r['median']/1e6 for r in stats['renderer'] if r['questions'] == n}
        lines.append(f'| {n} | {values["dac1bad"]:.3f} | {values["a1265ff"]:.3f} |')
    lines += ['', f'{len(raw["renderer_trials"])} trials. The comparator is first-renderer `dac1bad`, '
              'because pre-PR3 source has no renderer. Hardened checks add local work. Timing order was first-renderer '
              'then hardened, not interleaved; host drift is a limitation. No model-generation speed claim follows.', '',
              '| Probe | dac1bad | a32e170 | f019ba2 | cccacaf | a1265ff |', '|---|---|---|---|---|---|']
    for case in dict.fromkeys(r['case'] for r in raw['renderer_behavior']):
        rows = {r['revision']: r['outcome'] for r in raw['renderer_behavior'] if r['case'] == case}
        lines.append('| ' + case + ' | ' + ' | '.join(rows[r] for r in ['dac1bad', 'a32e170', 'f019ba2', 'cccacaf', 'a1265ff']) + ' |')
    lines += ['', 'Accepted/rejected describes validator behavior, not executed browser exploitation. '
              'These are five known reproductions, not an exhaustive security test.', '', '## Real-model comparison', '']
    original_path = REPORT / 'original-batch-summary.json'
    if original_path.exists():
        original = json.loads(original_path.read_text(encoding='utf-8'))
        lines += [f'**Original batch incomplete:** {original["completed_calls"]}/{original["attempted_calls"]} calls completed; '
                  'the final baseline call hit a service usage limit. Failed-call usage and duration are not estimated. '
                  'All original logs remain; unequal-length pair 2 is not pooled. '
                  'See [failure and recovery](FAILURE-AND-RECOVERY.md) and [original measured data](original-batch-summary.json).', '',
                  '| Original complete pair 1 only | Baseline | Candidate | Reduction |', '|---|---:|---:|---:|']
        for name, row in original['complete_pair1_only'].items():
            lines.append(f'| {name} | {row["baseline"]:,.3f} | {row["candidate"]:,.3f} | {row["reduction_percent"]:.2f}% |')
        lines += ['', 'Original transient exam files were not retained by the legacy end-only capture. '
                  'Six HTML capture-loss notices are explicitly not original artifacts; record aliases are exact copies '
                  'of the last available snapshots. The separate recovery below retains generated files and is not '
                  'a replacement for this failure. Cross-window latency is not pooled.', '']
    summary_path = REPORT / 'model-recovery/summary.json'
    if not summary_path.exists():
        summary_path = REPORT / 'model/summary.json'
    if summary_path.exists():
        measured = json.loads(summary_path.read_text(encoding='utf-8'))
        model_dir = summary_path.parent
        model_rel = model_dir.relative_to(REPORT).as_posix()
        config = json.loads((model_dir / 'protocol.json').read_text(encoding='utf-8'))
        calls = json.loads((model_dir / 'results.json').read_text(encoding='utf-8'))
        lines += [f'**Separate batch: {model_rel}.** Configured model: {config["model"]}, reasoning {config["reasoning_effort"]}, CLI {config["cli_version"]}. '
                  f'{config["pairs"]} paired replicates, {config["turns_per_arm"]} continued turns per arm, '
                  f'{len(calls)} completed calls; first arm {config.get("start_arm", "baseline")}, serial turn-interleaving. '
                  'Three forced saves followed by a mock-exam/save/handoff request. '
                  'The legacy arm name `v2` means the candidate source, not a newly published version.', '',
                  '| Metric | Baseline | Candidate | Reduction (negative = increase) |', '|---|---:|---:|---:|']
        for name, row in measured['pooled'].items():
            fmt = lambda value: f'{value:,.3f}' if name == 'wall_seconds' else f'{value:,.0f}'
            lines.append(f'| {name} | {fmt(row["baseline"])} | {fmt(row["v2"])} | {row["reduction_percent"]:.2f}% |')
        lines += ['', '| Pair / arm | Total tokens | Wall seconds | Changed-record turns |', '|---|---:|---:|---|']
        for row in measured['sessions']:
            lines.append(f'| {row["pair"]} / {row["arm"]} | {row["total_tokens"]:,} | '
                         f'{row["wall_seconds"]:.3f} | {row["record_changed_after_turns"]} |')
        lines += ['', '| Pair | Total-token reduction | Wall-time reduction |', '|---:|---:|---:|']
        for row in measured['pairs']:
            values = row['reduction_percent']
            lines.append(f'| {row["pair"]} | {values["total_tokens"]:.2f}% | {values["wall_seconds"]:.2f}% |')
        lines += ['', f'Raw [usage and wall times]({model_rel}/results.json), [derived per-turn differences]({model_rel}/summary.json), '
                  f'[configuration]({model_rel}/protocol.json), [identical prompts]({model_rel}/prompts.json), '
                  f'and [initial record]({model_rel}/initial-learning-record.md) are archived. '
                  'The generic inherited protocol description calls the record small; this experiment explicitly '
                  'adds 100 historical rows. Use its actual bytes and METHOD.md to interpret the workload.', '',
                  '**Quality must be checked before claiming an improvement:** '
                  '[independent quality review](QUALITY-REVIEW.md). '
                  'Lower resource use is not automatically equal-quality savings. Whole-skill changes, generated '
                  'artifact size, command choices, caching, output length, server load and latency all contribute. '
                  'Two pairs of one packet cannot establish general reliability or causality.']
    else:
        lines += ['NOT COMPLETE / NOT PERFORMED. No model token or latency result is claimed. '
                  'If a partial-results.json exists, retain it as an incomplete run rather than an improvement.']
    lines += ['', '## Validation and evidence limits', '',
              '- Independent method review: [METHOD-REVIEW.md](METHOD-REVIEW.md).',
              '- Browser evidence and package checks, if executed: [VERIFICATION.md](VERIFICATION.md). '
              'DOM-stub regressions are not browser layout verification.',
              '- This task adds a reproducible opt-in runner, raw evidence and reports. It also installs the missing '
              'canonical collaboration entries/protocol and ignore rules as required by the human; the English-content '
              'validator exempts only that canonical protocol alongside the existing original student artifact.',
              '- The benchmark runner was corrected to capture failures and per-call workspaces, with deterministic '
              'fake-CLI regression tests. No product skill/helper, manifest version or published ZIP is modified.',
              '- No learner gains, dollar/subscription savings, compaction savings, automatic plugin discovery, '
              'physical-device support, accessibility certification, or broad course/model reliability was measured.', '',
              '## Reproduction', '', '```text',
              'python tests/benchmark_update.py --phase local --output <new-report-directory> --repeats 30',
              'python tests/benchmark_update.py --phase model --output <same-report-directory> --pairs 2',
              'python tests/benchmark_update.py --phase model --output <same-report-directory> --pairs 1 --model-directory model-recovery --start-arm v2',
              'python tests/benchmark_update.py --phase report --output <same-report-directory>', '```', '',
              'The model phase uses current login/quota. Existing result files are refused. '
              'The report phase reads archived measurements and makes no model calls. '
              'Preserve existing evidence; independent review files are not generated by the report command.']
    (REPORT / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    fingerprints = {p.relative_to(REPORT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(REPORT.rglob('*')) if p.is_file() and p != REPORT / 'manifest.json'}
    dump(REPORT / 'manifest.json', fingerprints)
    print('REPORT COMPLETE;', len(fingerprints), 'fingerprints')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['local', 'model', 'report'], default='local')
    parser.add_argument('--output', type=Path, default=REPORT)
    parser.add_argument('--repeats', type=int, default=30)
    parser.add_argument('--sizes', default='10,100,1000,5000')
    parser.add_argument('--pairs', type=int, choices=[1, 2], default=2)
    parser.add_argument('--model-directory', choices=['model', 'model-recovery'], default='model')
    parser.add_argument('--start-arm', choices=['baseline', 'v2'], default='baseline')
    args = parser.parse_args()
    REPORT = args.output.resolve()
    if args.repeats < 1:
        parser.error('--repeats must be positive')
    if args.phase == 'local':
        local(args.repeats, [int(n) for n in args.sizes.split(',')])
    elif args.phase == 'model':
        model(args.pairs, args.model_directory, args.start_arm)
    else:
        report()
