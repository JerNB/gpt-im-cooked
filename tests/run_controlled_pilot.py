"""Controlled-comparison pilot: plain model (A1 naive, A2 strong prompt) vs. skill (B, C).

Makes REAL model calls through the existing Codex CLI login and its quota.
Two phases because turn 7 answers the tutor's own turn-6 question:

  python tests/run_controlled_pilot.py phase1 --work <new dir outside the repo, cloud-synced folders and Temp>
  # read runs/<arm>/response-06.md, write <work>/turn7-answers.json {"A1": "...", ...}
  python tests/run_controlled_pilot.py phase2 --work <same dir>

This is the single-replicate pilot runner. Replicated comparisons use the T004
runner (tests/run_controlled_comparison.py); do not extend this file for them.

Safety properties (added after the T003 review):
- User-global skills are disabled per call and any command that touches a
  global skill directory invalidates the session, so plain arms stay plain.
- Copied credentials exist only while a phase is running; every exit path,
  including setup failures, removes them.
- Phase 2 only writes to the report that phase 1 initialised (run id check)
  and refuses a completed report.
- Raw CLI output is sanitised and saved before it is parsed; failed calls keep
  their output and a file snapshot. Only this run's own files are rewritten.
"""
from contextlib import contextmanager
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'tests/fixtures/controlled-comparison/packet-s'
REPORT = ROOT / 'tests/reports/2026-11-13-controlled-pilot'
SKILL = 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
SKILL_REV = 'a1265ff'
MODEL = 'gpt-6.1-sol'
EFFORT = 'medium'
ARMS = ['A1', 'A2', 'B']
AUTH = Path.home() / '.codex/auth.json'
GLOBAL_SKILL_DIRS = [Path.home() / '.agents/skills', Path.home() / '.codex/skills']
TEXT_SUFFIXES = ('.md', '.json', '.jsonl', '.txt', '.bak')
BS = chr(92)
AGENTS = ('This is an isolated synthetic study directory for one student. Use only files in this '
          'directory. Do not browse the web, read other directories, or delegate.\n')


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='')


def scrub(text, work):
    """Replace every permitted root with <ROOT> and drop mis-decoded localized text."""
    variants = set()
    for base in (str(work), str(ROOT), tempfile.gettempdir(), str(Path.home())):
        variants.add(base.replace(BS, '/'))
        for level in (1, 2, 4, 8):  # raw, JSON-escaped, and JSON-inside-JSON escaped paths
            variants.add(base.replace(BS, BS * level))
    for a in sorted(variants, key=len, reverse=True):
        text = text.replace(a, '<ROOT>')
    # After path replacement: a permitted root may itself contain such characters.
    return re.sub('[' + chr(0x3400) + '-' + chr(0x9fff) + ']', chr(0xfffd), text)


def scrub_tree(folder, work):
    """Sanitise text files under one directory this run just created."""
    for p in folder.rglob('*'):
        if p.is_file() and p.suffix in TEXT_SUFFIXES:
            old = p.read_text(encoding='utf-8-sig', errors='replace')
            new = scrub(old, work)
            if new != old:
                p.write_text(new, encoding='utf-8', newline='')


def cli_command(cli):
    return [sys.executable, cli] if cli.endswith('.py') else [cli]


@contextmanager
def credentials(state):
    """Copy the login into each arm home for the duration of one phase only."""
    homes = [Path(a['home']) for a in state['arms'].values()]
    try:
        for home in homes:
            home.mkdir(parents=True, exist_ok=True)
            shutil.copy2(state['auth'], home / 'auth.json')
        yield
    finally:
        for home in homes:
            (home / 'auth.json').unlink(missing_ok=True)


def skill_isolation_flags():
    disabled = sorted({p.resolve().as_posix() for d in GLOBAL_SKILL_DIRS if d.is_dir() for p in d.rglob('SKILL.md')})
    selectors = 'skills.config=[' + ','.join('{path=' + json.dumps(p) + ',enabled=false}' for p in disabled) + ']'
    return ['-c', selectors, '-c', 'skills.bundled.enabled=false'], disabled


def setup(work, cli, auth):
    script = json.loads((PACKET / 'script.json').read_text(encoding='utf-8'))
    assert not REPORT.exists(), 'Report exists; refusing to overwrite pilot evidence'
    assert not work.exists(), 'Work directory must be new'
    assert ROOT not in work.resolve().parents, 'Work directory must be outside the repository'
    assert 'temp' not in str(work).lower() or cli.endswith('.py'), 'Codex sandbox helpers refuse temp directories'
    assert cli and Path(auth).is_file(), 'Codex CLI and an existing login are required'
    work.mkdir(parents=True)
    state = {'cli': cli, 'auth': str(auth), 'report': str(REPORT), 'run_id': uuid.uuid4().hex,
             'phase1_complete': False, 'arms': {}}
    archive = subprocess.check_output(['git', 'archive', '--format=zip', SKILL_REV, SKILL], cwd=ROOT) if 'B' in ARMS else b''
    for arm in ARMS:
        run = work / f'run-{arm}'
        shutil.copytree(PACKET / 'materials', run / 'materials')
        (run / 'AGENTS.md').write_text(AGENTS, encoding='utf-8', newline='')
        if arm == 'B':
            with zipfile.ZipFile(io.BytesIO(archive)) as z:
                for name in z.namelist():
                    if not name.endswith('/'):
                        p = run / 'skill' / Path(name).relative_to(SKILL)
                        p.parent.mkdir(parents=True, exist_ok=True)
                        p.write_bytes(z.read(name))
            shutil.copytree(run / 'skill', REPORT / 'skill-B', dirs_exist_ok=True)
        if arm == 'C':
            # Revised skill from the working tree (may be uncommitted); fingerprinted below.
            shutil.copytree(ROOT / SKILL, run / 'skill', ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(run / 'skill', REPORT / 'skill-C', dirs_exist_ok=True)
        state['arms'][arm] = {'cwd': str(run), 'home': str(work / f'home-{arm}'), 'session': None}
    fixtures = {p.relative_to(PACKET).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(PACKET.rglob('*')) if p.is_file()}
    head = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip() if 'C' in ARMS else ''
    dump(REPORT / 'protocol.json', {
        'run_id': state['run_id'],
        'model': MODEL, 'reasoning_effort': EFFORT, 'arms': ARMS, 'skill_revision_B': SKILL_REV,
        'cli_version': subprocess.check_output(cli_command(cli) + ['--version'], text=True).strip(),
        'design': 'Pilot: one session per arm, 10 scripted turns + 1 new-session resume turn; arms run in parallel, turns serial within an arm.',
        'fixture_sha256': fixtures,
        'global_skills_disabled': len(skill_isolation_flags()[1]),
        'skill_C_source': ('working tree on top of ' + head) if 'C' in ARMS else None,
        'skill_C_sha256': {p.relative_to(REPORT / 'skill-C').as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted((REPORT / 'skill-C').rglob('*')) if p.is_file()} if 'C' in ARMS else None,
        'limits': 'Synthetic packet, one model, one replicate, scripted student; not a learning-outcome study.',
    })
    shutil.copytree(PACKET, REPORT / 'fixture', dirs_exist_ok=True)
    dump(work / 'state.json', state)
    return script, state


def opener_key(arm):
    return 'B' if arm == 'C' else arm  # both skill arms get the identical student message


def as_text(value):
    if value is None:
        return ''
    return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value


def external_skill_commands(events):
    hits = []
    for e in events:
        item = e.get('item') or {}
        if item.get('type') == 'command_execution':
            command = str(item.get('command', '')).replace(BS, '/')
            if '.agents/skills' in command or '.codex/skills' in command:
                hits.append(item.get('id') or command[:80])
    return hits


def call(state, arm, turn, script, work):
    a = state['arms'][arm]
    run, home = Path(a['cwd']), Path(a['home'])
    text = turn['text']
    if turn.get('new_session'):
        a['session'] = None
        text = script['context'] + script['resume_openers'][opener_key(arm)] + text
    elif a['session'] is None:
        text = script['context'] + script['openers'][opener_key(arm)] + text
    isolation, _ = skill_isolation_flags()
    common = ['--json', '--skip-git-repo-check', '--ignore-user-config'] + isolation + [
        '-m', MODEL, '-c', f'model_reasoning_effort="{EFFORT}"', '-c', 'approval_policy="never"',
        '-c', 'sandbox_mode="workspace-write"', '-c', 'windows.sandbox="unelevated"']
    cmd = cli_command(state['cli']) + ['exec']
    cmd += (['resume'] + common + [a['session'], '-']) if a['session'] else (common + ['-C', str(run), '-'])
    env = {k: v for k, v in os.environ.items() if not (k.startswith('CODEX_') and k != 'CODEX_HOME')}
    env.update(CODEX_HOME=str(home), PYTHONUTF8='1')
    out = Path(state['report']) / 'runs' / arm
    out.mkdir(parents=True, exist_ok=True)
    n = f'{turn["id"]:02}'
    (out / f'prompt-{n}.md').write_text(text, encoding='utf-8', newline='')
    print(f'START {arm} turn {turn["id"]}', flush=True)
    start = time.perf_counter()
    failure = None
    try:
        proc = subprocess.run(cmd, input=text, cwd=run, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, encoding='utf-8', errors='replace', timeout=900)
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, code = as_text(exc.stdout), as_text(exc.stderr), None
        failure = 'timeout'
    seconds = round(time.perf_counter() - start, 1)
    # Preserve sanitised raw output before any parsing can fail.
    (out / f'turn-{n}.stdout.txt').write_text(scrub(stdout, work), encoding='utf-8', newline='')
    (out / f'turn-{n}.stderr.txt').write_text(scrub(stderr, work), encoding='utf-8', newline='')
    snap = out / f'files-after-{n}'
    shutil.copytree(run, snap, ignore=shutil.ignore_patterns('skill', 'materials', '__pycache__', 'AGENTS.md'))
    scrub_tree(snap, work)
    events, malformed = [], 0
    for line in stdout.splitlines():
        if line.strip().startswith('{'):
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                malformed += 1
    (out / f'turn-{n}.jsonl').write_text(scrub(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events), work),
                                         encoding='utf-8', newline='')
    for e in events:
        if e.get('type') == 'thread.started':
            a['session'] = e['thread_id']
    done = [e for e in events if e.get('type') == 'turn.completed']
    external = external_skill_commands(events)
    if failure is None:
        if external:
            failure = 'external_skill_access_invalidates_session'
        elif 'blocked by policy' in stderr:
            failure = 'sandbox_blocked_commands'
        elif code or len(done) != 1 or malformed:
            failure = f'incomplete (exit {code}, turn.completed {len(done)}, malformed lines {malformed})'
    if failure:
        dump(out / f'turn-{n}.failure.json', {'arm': arm, 'turn': turn['id'], 'failure': failure, 'seconds': seconds,
                                              'external_skill_commands': external})
        raise RuntimeError(f'{arm} turn {turn["id"]}: {failure}; evidence kept in {out}')
    msgs = [e['item'].get('text', '') for e in events
            if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'agent_message']
    reply = scrub('\n\n'.join(msgs), work)
    for prefix in (f'/<ROOT>/{work.name}/{run.name}/', f'/<ROOT>/{run.name}/', f'<ROOT>/{run.name}/'):
        reply = reply.replace(prefix, '')  # make the model's absolute study-file links relative
    (out / f'response-{n}.md').write_text(reply, encoding='utf-8', newline='')
    row = {'arm': arm, 'turn': turn['id'], 'seconds': seconds, 'usage': done[0]['usage']}
    print(f'DONE {arm} turn {turn["id"]} {seconds}s {done[0]["usage"]}', flush=True)
    return row


def run_turns(state, script, work, turn_ids, answers=None):
    def arm_job(arm):
        rows = []
        for t in script['turns']:
            if t['id'] not in turn_ids:
                continue
            t = dict(t)
            if t['text'] == 'ADAPTIVE':
                t['text'] = answers[arm]
            rows.append(call(state, arm, t, script, work))
            dump(work / 'state.json', state)
        return rows
    with concurrent.futures.ThreadPoolExecutor(len(ARMS)) as pool:
        results = list(pool.map(arm_job, ARMS))
    return [r for rows in results for r in rows]


def load_bound_state(work, requested_report):
    """Phase 2 may only touch the report that phase 1 of this work directory created."""
    state = json.loads((work / 'state.json').read_text(encoding='utf-8'))
    report = Path(state['report'])
    assert requested_report is None or requested_report.resolve() == report.resolve(), \
        'This work directory belongs to another report: ' + scrub(str(report), work)
    protocol = json.loads((report / 'protocol.json').read_text(encoding='utf-8'))
    assert protocol.get('run_id') == state['run_id'], 'Report was not initialised by this work directory'
    assert state.get('phase1_complete'), 'Phase 1 did not complete; start a new run instead of resuming'
    assert not (report / 'results-phase2.json').exists() and not (report / 'manifest.json').exists(), \
        'Report is already complete; refusing to modify it'
    assert set(state['arms']) == set(ARMS), 'Arms differ from phase 1: ' + ','.join(state['arms'])
    return state, report


def main():
    global ARMS, REPORT
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['phase1', 'phase2'])
    ap.add_argument('--work', required=True, type=Path)
    ap.add_argument('--arms', default=','.join(ARMS), help='comma-separated subset of A1,A2,B,C')
    ap.add_argument('--report', type=Path, help='report directory (default: the 2026-11-13 pilot)')
    ap.add_argument('--cli', help='CLI executable (tests pass a fake .py CLI); default: codex on PATH')
    ap.add_argument('--auth', type=Path, default=AUTH, help='login file to copy (tests pass a dummy file)')
    args = ap.parse_args()
    ARMS = args.arms.split(',')
    assert set(ARMS) <= {'A1', 'A2', 'B', 'C'}, ARMS
    requested = None
    if args.report:
        requested = args.report if args.report.is_absolute() else (ROOT / args.report)
        REPORT = requested.resolve()
    work = args.work.resolve()
    if args.phase == 'phase1':
        script, state = setup(work, args.cli or shutil.which('codex'), args.auth)
        with credentials(state):
            rows = run_turns(state, script, work, range(1, 7))
        dump(REPORT / 'results-phase1.json', rows)
        state['phase1_complete'] = True
        dump(work / 'state.json', state)
        print('PHASE 1 COMPLETE: write turn7-answers.json in the work directory, then run phase2.')
        return
    state, REPORT = load_bound_state(work, requested)
    script = json.loads((PACKET / 'script.json').read_text(encoding='utf-8'))
    answers = json.loads((work / 'turn7-answers.json').read_text(encoding='utf-8'))
    assert set(answers) == set(ARMS)
    dump(REPORT / 'turn7-answers.json', answers)
    with credentials(state):
        rows = run_turns(state, script, work, range(7, 12), answers)
    dump(REPORT / 'results-phase2.json', rows)
    for arm in ARMS:
        run = Path(state['arms'][arm]['cwd'])
        final = REPORT / 'runs' / arm / 'final-files'
        shutil.copytree(run, final, dirs_exist_ok=True, ignore=shutil.ignore_patterns('skill', 'materials', '__pycache__'))
        # Mirror the run layout so relative links in raw responses resolve (as in the 2026-10-31 benchmark).
        shutil.copytree(run, REPORT / 'runs' / arm, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('skill', '__pycache__', 'AGENTS.md'))
        scrub_tree(REPORT / 'runs' / arm, work)  # only this run's own arm directory
    manifest = {p.relative_to(REPORT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(REPORT.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
    dump(REPORT / 'manifest.json', manifest)
    print('PHASE 2 COMPLETE; credentials removed from work directory.')


if __name__ == '__main__':
    main()
