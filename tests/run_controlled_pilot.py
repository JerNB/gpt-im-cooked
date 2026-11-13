"""Controlled-comparison pilot: plain model (A1 naive, A2 strong prompt) vs. skill (B).

Makes REAL model calls through the existing Codex CLI login and its quota.
Two phases because turn 7 answers the tutor's own turn-6 question:

  python tests/run_controlled_pilot.py phase1 --work <dir outside the repo>
  # read runs/<arm>/response-06.md, write <work>/turn7-answers.json {"A1": "...", ...}
  python tests/run_controlled_pilot.py phase2 --work <same dir>

Credentials are copied only into <work>/home-*/ and deleted after phase 2.
Run directories never live inside the repository (OneDrive sync).
"""
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
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'tests/fixtures/controlled-comparison/packet-s'
REPORT = ROOT / 'tests/reports/2026-11-13-controlled-pilot'
SKILL = 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
SKILL_REV = 'a1265ff'
MODEL = 'gpt-6.1-sol'
EFFORT = 'medium'
ARMS = ['A1', 'A2', 'B']
AGENTS = ('This is an isolated synthetic study directory for one student. Use only files in this '
          'directory. Do not browse the web, read other directories, or delegate.\n')


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='')


def scrub(text, work):
    # Localized Windows error text in raw tool output arrives mis-decoded; keep logs English-only.
    text = re.sub('[' + chr(0x3400) + '-' + chr(0x9fff) + ']', chr(0xfffd), text)
    variants = set()
    for base in (str(work), str(Path.home())):
        variants.add(base.replace(chr(92), '/'))
        for level in (1, 2, 4, 8):  # raw, JSON-escaped, and JSON-inside-JSON escaped paths
            variants.add(base.replace(chr(92), chr(92) * level))
    for a in sorted(variants, key=len, reverse=True):
        text = text.replace(a, '<ROOT>')
    return text


def setup(work):
    script = json.loads((PACKET / 'script.json').read_text(encoding='utf-8'))
    assert not REPORT.exists(), 'Report exists; refusing to overwrite pilot evidence'
    assert not work.exists(), 'Work directory must be new'
    assert ROOT not in work.resolve().parents, 'Work directory must be outside the repository'
    assert 'temp' not in str(work).lower(), 'Codex sandbox helpers refuse temp directories; use a non-temp path'
    cli = shutil.which('codex')
    auth = Path.home() / '.codex/auth.json'
    assert cli and auth.is_file(), 'Codex CLI and an existing login are required'
    work.mkdir(parents=True)
    state = {'cli': cli, 'arms': {}}
    archive = subprocess.check_output(['git', 'archive', '--format=zip', SKILL_REV, SKILL], cwd=ROOT)
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
        home = work / f'home-{arm}'
        home.mkdir()
        shutil.copy2(auth, home / 'auth.json')
        state['arms'][arm] = {'cwd': str(run), 'home': str(home), 'session': None}
    fixtures = {p.relative_to(PACKET).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(PACKET.rglob('*')) if p.is_file()}
    dump(REPORT / 'protocol.json', {
        'model': MODEL, 'reasoning_effort': EFFORT, 'arms': ARMS, 'skill_revision_B': SKILL_REV,
        'cli_version': subprocess.check_output([cli, '--version'], text=True).strip(),
        'design': 'Pilot: one session per arm, 10 scripted turns + 1 new-session resume turn; arms run in parallel, turns serial within an arm.',
        'fixture_sha256': fixtures,
        'skill_C_source': 'working tree on top of ' + subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip() if 'C' in ARMS else None,
        'skill_C_sha256': {p.relative_to(REPORT / 'skill-C').as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted((REPORT / 'skill-C').rglob('*')) if p.is_file()} if 'C' in ARMS else None,
        'limits': 'Synthetic packet, one model, one replicate, scripted student; not a learning-outcome study.',
    })
    shutil.copytree(PACKET, REPORT / 'fixture', dirs_exist_ok=True)
    dump(work / 'state.json', state)
    return script, state


def opener_key(arm):
    return 'B' if arm == 'C' else arm  # both skill arms get the identical student message


def call(state, arm, turn, script, work):
    a = state['arms'][arm]
    run, home = Path(a['cwd']), Path(a['home'])
    text = turn['text']
    if turn.get('new_session'):
        a['session'] = None
        text = script['context'] + script['resume_openers'][opener_key(arm)] + text
    elif a['session'] is None:
        text = script['context'] + script['openers'][opener_key(arm)] + text
    common = ['--json', '--skip-git-repo-check', '--ignore-user-config', '-m', MODEL,
              '-c', f'model_reasoning_effort="{EFFORT}"', '-c', 'approval_policy="never"',
              '-c', 'sandbox_mode="workspace-write"',
              '-c', 'windows.sandbox="unelevated"']
    cmd = [state['cli'], 'exec']
    cmd += (['resume'] + common + [a['session'], '-']) if a['session'] else (common + ['-C', str(run), '-'])
    env = dict(os.environ, CODEX_HOME=str(home), PYTHONUTF8='1')
    out = REPORT / 'runs' / arm
    out.mkdir(parents=True, exist_ok=True)
    print(f'START {arm} turn {turn["id"]}', flush=True)
    start = time.perf_counter()
    proc = subprocess.run(cmd, input=text, cwd=run, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, encoding='utf-8', errors='replace', timeout=900)
    seconds = round(time.perf_counter() - start, 1)
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip().startswith('{')]
    n = f'{turn["id"]:02}'
    (out / f'turn-{n}.jsonl').write_text(scrub(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events), work), encoding='utf-8', newline='')
    (out / f'turn-{n}.stderr.txt').write_text(scrub(proc.stderr, work), encoding='utf-8', newline='')
    (out / f'prompt-{n}.md').write_text(text, encoding='utf-8', newline='')
    for e in events:
        if e.get('type') == 'thread.started':
            a['session'] = e['thread_id']
    done = [e for e in events if e.get('type') == 'turn.completed']
    if proc.returncode or len(done) != 1:
        raise RuntimeError(f'{arm} turn {turn["id"]} incomplete (exit {proc.returncode}); see {out}')
    msgs = [e['item'].get('text', '') for e in events
            if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'agent_message']
    reply = scrub('\n\n'.join(msgs), work)
    for prefix in (f'/<ROOT>/{work.name}/{run.name}/', f'/<ROOT>/{run.name}/'):
        reply = reply.replace(prefix, '')  # make the model's absolute study-file links relative
    (out / f'response-{n}.md').write_text(reply, encoding='utf-8', newline='')
    snap = out / f'files-after-{n}'
    shutil.copytree(run, snap, ignore=shutil.ignore_patterns('skill', 'materials', '__pycache__', 'AGENTS.md'))
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


def main():
    global ARMS, REPORT
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['phase1', 'phase2'])
    ap.add_argument('--work', required=True, type=Path)
    ap.add_argument('--arms', default=','.join(ARMS), help='comma-separated subset of A1,A2,B,C')
    ap.add_argument('--report', type=Path, help='report directory (default: the 2026-11-13 pilot)')
    args = ap.parse_args()
    ARMS = args.arms.split(',')
    assert set(ARMS) <= {'A1', 'A2', 'B', 'C'}, ARMS
    if args.report:
        REPORT = (ROOT / args.report).resolve() if not args.report.is_absolute() else args.report
    work = args.work.resolve()
    if args.phase == 'phase1':
        script, state = setup(work)
        rows = run_turns(state, script, work, range(1, 7))
        dump(REPORT / 'results-phase1.json', rows)
        print('PHASE 1 COMPLETE: write turn7-answers.json in the work directory, then run phase2.')
        return
    script = json.loads((PACKET / 'script.json').read_text(encoding='utf-8'))
    state = json.loads((work / 'state.json').read_text(encoding='utf-8'))
    answers = json.loads((work / 'turn7-answers.json').read_text(encoding='utf-8'))
    assert set(answers) == set(ARMS)
    dump(REPORT / 'turn7-answers.json', answers)
    try:
        rows = run_turns(state, script, work, range(7, 12), answers)
        dump(REPORT / 'results-phase2.json', rows)
    finally:
        for arm in ARMS:
            auth = Path(state['arms'][arm]['home']) / 'auth.json'
            if auth.exists():
                auth.unlink()
    for arm in ARMS:
        run = Path(state['arms'][arm]['cwd'])
        shutil.copytree(run, REPORT / 'runs' / arm / 'final-files', dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('skill', 'materials', '__pycache__'))
        # Mirror the run layout so relative links in raw responses resolve (as in the 2026-10-31 benchmark).
        shutil.copytree(run, REPORT / 'runs' / arm, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('skill', '__pycache__', 'AGENTS.md'))
    for p in REPORT.rglob('*'):
        if p.is_file() and p.suffix in ('.md', '.json', '.jsonl', '.txt', '.bak'):
            p.write_text(scrub(p.read_text(encoding='utf-8-sig', errors='replace'), work), encoding='utf-8', newline='')
    manifest = {p.relative_to(REPORT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(REPORT.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
    dump(REPORT / 'manifest.json', manifest)
    print('PHASE 2 COMPLETE; credentials removed from work directory.')


if __name__ == '__main__':
    main()
