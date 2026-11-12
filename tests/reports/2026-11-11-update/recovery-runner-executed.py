"""Run a small, real CLI A/B benchmark; credentials stay in a temporary directory.

Uses the existing Codex login and its quota. Run from the repository root.
No API prices or learning gains are inferred from the reported token counts.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'tests/reports/2026-10-31-token-benchmark'
SKILL = 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
MODEL = 'gpt-6.1-sol'
REVISIONS = {'baseline': '4212af7', 'v2': 'a2d5d9b'}
PACKET = '''# Synthetic statistics mini-course

## Scope
Only conditional probability, grouped row counts, and duplicate-key inner joins.
This packet supplies all teaching rules. No external packages or sources needed.

## S1: Conditional probability
P(A given B) counts A-and-B outcomes divided by B outcomes. The denominator
is the conditioned population B, not the full sample. Assume equally weighted
observations and positive B counts. A percentage is the fraction times 100.
Q1: There are 10 students, 8 commuters, and 2 commuter cyclists. Find the
fraction of commuters who cycle. Instructor key: 2/8 = 1/4.
Q3: There are 20 students, 12 residents, and 3 resident cyclists. Find the
fraction of residents who cycle. Instructor key: 3/12 = 1/4.
Q5: There are 50 employees, 20 remote workers, and 5 remote trainees. Find
the fraction of remote workers who are trainees. Instructor key: 5/20 = 1/4.

## S2: Grouped transformations
A grouped scalar summary returns one result row per nonempty group. A grouped
mutate-style transformation attaches the group result to every original row and
retains all original rows. Assume no filtering, missing groups, or vector outputs.
Q2: Eight observations belong to two regions. A grouped mutate attaches each
region's mean to its original observations. How many output rows? Instructor
key: 8; a scalar summary of those groups would return 2.

## S3: Duplicate-key inner joins
An inner join returns every matching pair of left and right rows for each key.
If one key occurs L times on the left and R times on the right, that key
contributes L times R output rows. Unmatched rows contribute zero.
Q4: The left table has two rows for key K. The right table has three rows for K.
No other keys exist. How many inner-join output rows? Instructor key: 6.
'''
PROFILE = '''# Course profile

- Course: Synthetic statistics mini-course
- Exam: practice-only; date unknown
- Preferred language: English
- Quick start shown: Yes
- Source S: materials/packet.md, accessible; S1-S3 read as needed
- Confirmed scope: C1 conditional probability; C2 grouped row counts;
  C3 duplicate-key inner joins. No other topics.
- Practice is conversational; no artifact requested.
- Exam reference-sheet restrictions: unknown
'''
RECORD = '''# Learning record

## Study setup
- Quick start shown: Yes
- Preferred review output: English conversation

## Active course and exam
Synthetic statistics mini-course / practice-only. Profile: course-profile.md

## Concepts
| Concept ID / topic ID | Concept | Status | Priority and evidence | Corrective rule | Next task |
|---|---|---|---|---|---|
| C1 | Conditional probability | Unassessed | No attempts | Use the conditioned population | Review an attempt |
| C2 | Grouped row counts | Unassessed | No attempts | Mutate keeps original rows | Review an attempt |
| C3 | Inner joins | Unassessed | No attempts | Count matching pairs | Review an attempt |

## Attempt history
| Date when known | Attempt ID / item locator | Concept ID | Student answer or link | Outcome | Assistance | Answer evidence | Feedback |
|---|---|---|---|---|---|---|---|

## Import ledger
No imports.

## Student-reported difficulties
None recorded.

## Open questions
None recorded.

## Next session
- Current activity: Review packet attempts
- Concepts to revisit: Determine from evidence
- Next action: Review Q1
'''
TURNS = [
    'For packet Q1, my answer is 2/10 = 20%. I used all ten students as the denominator because the question starts with ten students. Please check my answer and reasoning.',
    'For packet Q2, my answer is 2 rows because there are two regions. I think grouping means the result always has one row per group. Please check my answer and reasoning.',
    'For packet Q3, my answer is 3/12 = 25%. We are considering residents, so the denominator is the 12 residents, not all 20 students. I worked this new question without a question-specific hint. Please check it.',
    'For packet Q4, my answer is 3 rows. I thought each right-table row matches once, even though K occurs twice on the left. Please check my answer and reasoning.',
    'For packet Q5, my answer is 5/20 = 25%. The conditioned population is remote workers, and five of those twenty are trainees. I worked it without a question-specific hint. Please check my answer and reasoning.',
    'I am ending this study session now. Please save my progress and give me a brief handoff for next time. Do not generate a guide, a webpage, or more questions.',
]
INTRO = '''Use the frozen study skill at skill/SKILL.md and its relevant references
to continue my course review. My existing profile is course-profile.md, learning
record is learning-record.md, and supplied teaching material is materials/packet.md.
The course and study directory are already established. Keep ordinary feedback
to about 120-180 words, excluding the opening marker and any short saved-state
note. Do not make additional artifacts unless I ask. Use only files in this
study directory and do not browse, invoke other skills, or contact services.

'''


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def safe(value, temporary):
    if isinstance(value, dict):
        return {k: safe(v, temporary) for k, v in value.items()}
    if isinstance(value, list):
        return [safe(v, temporary) for v in value]
    if isinstance(value, str):
        for a, b in [(str(temporary), '<BENCHMARK_ROOT>'), (str(Path.home()), '<USER_HOME>')]:
            value = value.replace(a, b).replace(a.replace('\\', '/'), b).replace(a.replace('\\', '\\\\'), b)
        return value
    return value


def capture_study(run, output, temporary):
    """Capture before temporary cleanup, including when a later call fails; never copy the separate login home."""
    for path in run.rglob('*'):
        rel = path.relative_to(run)
        if '__pycache__' in rel.parts or not path.is_file():
            continue
        if path.is_symlink():
            raise ValueError('A synthetic study workspace must not contain symlinks')
        data = path.read_bytes()
        if path.suffix in ('.md', '.txt', '.json', '.jsonl', '.py', '.yaml', '.bak', '.html', '.js'):
            data = safe(data.decode('utf-8-sig'), temporary).encode('utf-8')
        destinations = [output / rel]
        if 'skill' not in rel.parts:
            destinations.append(output / 'final-study' / rel)
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)


def execute_call(cmd, prompt, run, env, output, turn, temporary):
    start = time.perf_counter()
    started = datetime.now(timezone.utc).isoformat()
    try:
        try:
            proc = subprocess.run(cmd, input=prompt, cwd=run, env=env, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', timeout=600)
            elapsed = time.perf_counter() - start
            stdout, stderr, timed_out = proc.stdout, proc.stderr, False
        except subprocess.TimeoutExpired as error:
            elapsed = time.perf_counter() - start
            decode = lambda value: value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value or ''
            stdout, stderr, timed_out = decode(error.stdout), decode(error.stderr), True
            proc = None
        # Write before JSON parsing or completion checks, so malformed/partial output survives too.
        (output / f'turn-{turn:02}.jsonl').write_text(safe(stdout, temporary), encoding='utf-8')
        (output / f'turn-{turn:02}.stderr.txt').write_text(safe(stderr, temporary), encoding='utf-8')
        dump(output / f'turn-{turn:02}.execution.json', {'started_at': started, 'wall_seconds': round(elapsed, 3),
             'returncode': None if proc is None else proc.returncode, 'timed_out': timed_out})
        if timed_out:
            raise RuntimeError('CLI call timed out; partial output and workspace captured')
        return proc, elapsed
    finally:
        capture_study(run, output, temporary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pairs', type=int, default=2)
    parser.add_argument('--start-arm', choices=['baseline', 'v2'], default='baseline')
    args = parser.parse_args()
    assert 1 <= args.pairs <= 3
    assert not (REPORT / 'results.json').exists(), 'Existing results must not be overwritten'
    cli = shutil.which('codex')
    assert cli, 'Codex CLI is required'
    auth = Path.home() / '.codex/auth.json'
    assert auth.is_file(), 'Existing Codex login is required'
    REPORT.mkdir(parents=True, exist_ok=True)
    dump(REPORT / 'protocol.json', {
        'model': MODEL, 'reasoning_effort': 'medium', 'pairs': args.pairs,
        'turns_per_arm': len(TURNS), 'revisions': REVISIONS,
        'start_arm': args.start_arm,
        'cli_version': subprocess.check_output([cli, '--version'], text=True).strip(),
        'usage_source': 'turn.completed JSONL event, schema validated during execution',
        'design': 'Paired AB/BA, turn-interleaved, serial execution; same small initial record.',
        'limits': 'Whole-skill comparison, not batching-only causality; no API-dollar or compaction claim.',
    })
    for name, text in [('packet.md', PACKET), ('course-profile.md', PROFILE), ('initial-learning-record.md', RECORD)]:
        (REPORT / name).write_text(text, encoding='utf-8')
    dump(REPORT / 'prompts.json', {'initial_prefix': INTRO, 'turns': TURNS})
    rows = []
    with tempfile.TemporaryDirectory(prefix='cooked-token-bench-') as temporary:
        temporary = Path(temporary)
        runs = {}
        for pair in range(1, args.pairs + 1):
            for arm, rev in REVISIONS.items():
                run = temporary / f'pair-{pair}-{arm}'
                run.mkdir()
                archive = subprocess.check_output(['git', 'archive', '--format=zip', rev, SKILL], cwd=ROOT)
                with zipfile.ZipFile(io.BytesIO(archive)) as z:
                    for name in z.namelist():
                        if name.endswith('/'):
                            continue
                        rel = Path(name).relative_to(SKILL)
                        p = run / 'skill' / rel
                        p.parent.mkdir(parents=True, exist_ok=True)
                        p.write_bytes(z.read(name))
                frozen = REPORT / 'skills' / arm
                if not frozen.exists():
                    shutil.copytree(run / 'skill', frozen)
                (run / 'materials').mkdir()
                (run / 'materials/packet.md').write_text(PACKET, encoding='utf-8')
                (run / 'course-profile.md').write_text(PROFILE, encoding='utf-8')
                (run / 'learning-record.md').write_text(RECORD, encoding='utf-8')
                (run / 'AGENTS.md').write_text('This is an isolated synthetic course study directory. Use only the supplied frozen skill and course files. Write study records here only. Do not read other directories, use the web, delegate, or modify the skill.\n', encoding='utf-8')
                home = temporary / f'home-{pair}-{arm}'
                home.mkdir()
                shutil.copy2(auth, home / 'auth.json')
                runs[(pair, arm)] = {'cwd': run, 'home': home, 'session': None}
        for pair in range(1, args.pairs + 1):
            order = ['baseline', 'v2'] if pair % 2 else ['v2', 'baseline']
            if args.start_arm == 'v2':
                order.reverse()
            for turn, text in enumerate(TURNS, 1):
                for arm in order:
                    state = runs[(pair, arm)]
                    run = state['cwd']
                    output = REPORT / 'runs' / f'pair-{pair}-{arm}'
                    output.mkdir(parents=True, exist_ok=True)
                    common = ['--json', '--skip-git-repo-check', '--ignore-user-config',
                              '-m', MODEL, '-c', 'model_reasoning_effort="medium"',
                              '-c', 'approval_policy="never"', '-c', 'sandbox_mode="danger-full-access"']
                    cmd = [cli, 'exec']
                    if state['session']:
                        cmd += ['resume'] + common + [state['session'], '-']
                        prompt = text
                    else:
                        cmd += common + ['-C', str(run), '-']
                        prompt = INTRO + text
                    env = os.environ.copy()
                    env['CODEX_HOME'] = str(state['home'])
                    env['PYTHONUTF8'] = '1'
                    print(f'START pair={pair} arm={arm} turn={turn}', flush=True)
                    try:
                        proc, elapsed = execute_call(cmd, prompt, run, env, output, turn, temporary)
                    except RuntimeError:
                        dump(REPORT / 'partial-results.json', rows)
                        raise
                    events = []
                    for line in proc.stdout.splitlines():
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            dump(REPORT / 'partial-results.json', rows)
                            raise RuntimeError('CLI stdout was not JSONL')
                    cleaned = safe(events, temporary)
                    (output / f'turn-{turn:02}.jsonl').write_text(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in cleaned), encoding='utf-8')
                    (output / f'turn-{turn:02}.stderr.txt').write_text(safe(proc.stderr, temporary), encoding='utf-8')
                    for e in events:
                        if e.get('type') == 'thread.started':
                            state['session'] = e['thread_id']
                    completed = [e for e in events if e.get('type') == 'turn.completed']
                    if proc.returncode or len(completed) != 1:
                        dump(REPORT / 'partial-results.json', rows)
                        raise RuntimeError(f'Incomplete call pair={pair} arm={arm} turn={turn}: {proc.returncode}; inspect saved logs')
                    usage = completed[0]['usage']
                    assert {'input_tokens', 'cached_input_tokens', 'output_tokens'} <= usage.keys(), usage
                    assert 0 <= usage['cached_input_tokens'] <= usage['input_tokens']
                    row = {'pair': pair, 'arm': arm, 'turn': turn, 'wall_seconds': round(elapsed, 3), 'usage': usage}
                    rows.append(row)
                    dump(REPORT / 'partial-results.json', rows)
                    for name in ['learning-record.md', 'course-profile.md']:
                        p = run / name
                        if p.exists():
                            (output / f'{name.removesuffix(".md")}-after-{turn:02}.md').write_text(safe(p.read_text(encoding='utf-8-sig'), temporary), encoding='utf-8')
                    messages = [e['item'].get('text', '') for e in events if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'agent_message']
                    (output / f'response-{turn:02}.md').write_text(safe('\n\n'.join(messages), temporary).replace(f'<BENCHMARK_ROOT>/{run.name}/', ''), encoding='utf-8')
                    # Only the benchmark's own session log is inspected for accounting semantics.
                    rollouts = list((state['home'] / 'sessions').rglob(f'*{state["session"]}*.jsonl'))
                    accounting = []
                    for path in rollouts:
                        for line in path.read_text(encoding='utf-8').splitlines():
                            event = json.loads(line)
                            if event.get('type') == 'event_msg' and event.get('payload', {}).get('type') == 'token_count':
                                accounting.append(event['payload'].get('info'))
                    dump(output / f'accounting-after-{turn:02}.json', safe(accounting, temporary))
                    print(f'DONE pair={pair} arm={arm} turn={turn}: {usage}, seconds={elapsed:.1f}', flush=True)
        for (pair, arm), state in runs.items():
            target = REPORT / 'runs' / f'pair-{pair}-{arm}'
            capture_study(state['cwd'], target, temporary)
        dump(REPORT / 'results.json', rows)
    fingerprints = {}
    for p in sorted(REPORT.rglob('*')):
        if p.is_file() and p.name != 'manifest.json':
            if p.suffix in ('.md', '.txt', '.json', '.jsonl', '.py', '.yaml', '.bak'):
                p.write_text(safe(p.read_text(encoding='utf-8-sig'), temporary), encoding='utf-8')
            fingerprints[p.relative_to(REPORT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    dump(REPORT / 'manifest.json', fingerprints)
    print('COMPLETE: saved sanitized events, per-turn records, accounting, and fingerprints.', flush=True)


if __name__ == '__main__':
    main()
