"""T004 frozen, resumable controlled comparison runner; makes real Codex CLI calls."""
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
REPORT = ROOT / 'tests/reports/2026-11-14-controlled-comparison/isolated'
SKILL = 'plugins/gpt-im-cooked/skills/gpt-im-cooked'
B_REV = '97be1720f890745b3b59be52ad9ec3dea740393e'
C_REV = '4d102f605260559af16d2f6620cd926bf0b8f6fd'
MODEL = 'gpt-6.1-sol'
EFFORT = 'medium'
ARMS = ['A1', 'A2', 'B', 'C']
PACKETS = ['S', 'P']


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='')


def scrub(text, work):
    text = re.sub('[' + chr(0x3400) + '-' + chr(0x9fff) + ']', chr(0xfffd), text)
    variants = set()
    for base in (str(work), str(Path.home())):
        variants.add(base.replace(chr(92), '/'))
        for n in (1, 2, 4, 8):
            variants.add(base.replace(chr(92), chr(92) * n))
    for item in sorted(variants, key=len, reverse=True):
        text = text.replace(item, '<ROOT>')
    return text


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_archive(revision, dest):
    data = subprocess.check_output(['git', 'archive', '--format=zip', revision, SKILL], cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for name in zf.namelist():
            if name.endswith('/'):
                continue
            rel = Path(name).relative_to(SKILL)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))


def verify_fingerprint():
    proto = json.loads(subprocess.check_output(
        ['git', 'show', 'origin/cc/T003-skill-revision:tests/reports/2026-11-13-controlled-pilot-armC/protocol.json'],
        cwd=ROOT, text=True, encoding='utf-8'))
    expected = proto['skill_C_sha256']
    scratch = REPORT.parent / '_t004-skill-check'
    if scratch.exists():
        raise RuntimeError(f'refusing existing scratch directory: {scratch}')
    scratch.mkdir()
    try:
        skill_archive(C_REV, scratch)
        got = {p.relative_to(scratch).as_posix(): sha(p) for p in scratch.rglob('*') if p.is_file()}
    finally:
        shutil.rmtree(scratch)
    if got != expected:
        raise RuntimeError(f'Arm C frozen-skill fingerprint mismatch; missing={set(expected)-set(got)}, extra={set(got)-set(expected)}, changed={[k for k in set(got)&set(expected) if got[k] != expected[k]]}')
    return expected


def packet_files(packet):
    return ROOT / f'tests/fixtures/controlled-comparison/packet-{packet.lower()}'


def prepare(work, packet, rep):
    if work.exists():
        raise RuntimeError('work directory exists; refusing to overwrite evidence')
    if REPORT.exists() and not (REPORT / 'protocol.json').is_file():
        raise RuntimeError('report directory exists without this run protocol; refusing to overwrite evidence')
    if 'temp' in str(work).lower() or str(ROOT).lower() in str(work).lower() or 'onedrive' in str(work).lower():
        raise RuntimeError('work path must be outside repository, OneDrive, and Temp')
    source = packet_files(packet)
    script_path = source / 'script.json'
    rubric_path = source / 'rubric-v2.json' if packet == 'P' else source / 'rubric.json'
    script = json.loads(script_path.read_text(encoding='utf-8'))
    cli = shutil.which('codex')
    auth = Path.home() / '.codex/auth.json'
    if not cli or not auth.is_file():
        raise RuntimeError('Codex CLI login required')
    work.mkdir(parents=True)
    runmeta = {'packet': packet, 'replicate': rep, 'arms': {}}
    for arm in ARMS:
        label = f'{arm}-{packet}-rep{rep}'
        run = work / f'run-{label}'
        shutil.copytree(source / 'materials', run / 'materials')
        (run / 'AGENTS.md').write_text(
            'Isolated synthetic study directory. Use only local files; do not browse, delegate, or contact services.\n',
            encoding='utf-8', newline='')
        if arm in ('B', 'C'):
            skill_archive(B_REV if arm == 'B' else C_REV, run / 'skill')
        home = work / f'home-{label}'
        home.mkdir()
        shutil.copy2(auth, home / 'auth.json')
        runmeta['arms'][arm] = {'cwd': str(run), 'home': str(home), 'session': None, 'failed': False}
    dump(work / 'state.json', runmeta)
    fixture_hashes = {p.relative_to(source).as_posix(): sha(p) for p in sorted(source.rglob('*')) if p.is_file()}
    (REPORT / 'fixtures' / f'packet-{packet.lower()}').parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, REPORT / 'fixtures' / f'packet-{packet.lower()}', dirs_exist_ok=True)
    return script, runmeta, fixture_hashes, cli


def opener(arm, phase):
    key = 'B' if arm == 'C' else arm
    return key


def call(script, state, arm, turn, work, cli, phase):
    a = state['arms'][arm]
    run, home = Path(a['cwd']), Path(a['home'])
    prompt = turn['text']
    key = opener(arm, phase)
    if turn.get('new_session'):
        a['session'] = None
        prompt = script['context'] + script.get('resume_openers', {}).get(key, '') + prompt
    elif a['session'] is None:
        prompt = script['context'] + script['openers'][key] + prompt
    disabled = sorted({p.resolve().as_posix() for d in (Path.home() / '.agents/skills', Path.home() / '.codex/skills') for p in d.rglob('SKILL.md')})
    selectors = 'skills.config=[' + ','.join('{path=' + json.dumps(p) + ',enabled=false}' for p in disabled) + ']'
    common = ['--json', '--skip-git-repo-check', '--ignore-user-config', '-c', selectors,
              '-c', 'skills.bundled.enabled=false', '-m', MODEL,
              '-c', f'model_reasoning_effort="{EFFORT}"', '-c', 'approval_policy="never"',
              '-c', 'sandbox_mode="workspace-write"', '-c', 'windows.sandbox="unelevated"']
    cmd = [cli, 'exec'] + (['resume'] + common + [a['session'], '-'] if a['session'] else common + ['-C', str(run), '-'])
    env = dict(os.environ, CODEX_HOME=str(home), PYTHONUTF8='1')
    for key in ('CODEX_WINDOWS_REGISTERED_CORE', 'CODEX_APP_TOOLS_PIPE_PATH', 'CODEX_APP_RUNTIME_CLI_PATH'):
        env.pop(key, None)
    out = REPORT / 'runs' / f'{arm}-{state["packet"]}-rep{state["replicate"]}'
    out.mkdir(parents=True, exist_ok=True)
    n = int(turn['id'])
    stem = f'turn-{n:02}'
    (out / f'prompt-{n:02}.md').write_text(prompt, encoding='utf-8', newline='')
    started = time.time()
    mono = time.perf_counter()
    error = None
    try:
        proc = subprocess.run(cmd, input=prompt, cwd=run, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', timeout=900)
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode('utf-8', 'replace') if isinstance(exc.stdout, bytes) else (exc.stdout or '')
        stderr = exc.stderr.decode('utf-8', 'replace') if isinstance(exc.stderr, bytes) else (exc.stderr or '')
        rc, error = 124, 'timeout'
    elapsed = round(time.perf_counter() - mono, 2)
    events = []
    for line in stdout.splitlines():
        try:
            item = json.loads(line)
            events.append(item)
        except json.JSONDecodeError:
            pass
    (out / f'{stem}.jsonl').write_text(scrub(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events), work), encoding='utf-8', newline='')
    (out / f'{stem}.stderr.txt').write_text(scrub(stderr, work), encoding='utf-8', newline='')
    done = [e for e in events if e.get('type') == 'turn.completed']
    for e in events:
        if e.get('type') == 'thread.started':
            a['session'] = e.get('thread_id')
    msgs = [e.get('item', {}).get('text', '') for e in events if e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'agent_message']
    reply = scrub('\n\n'.join(msgs), work)
    reply = reply.replace(str(run).replace('\\', '/') + '/', '')
    (out / f'response-{n:02}.md').write_text(reply, encoding='utf-8', newline='')
    snap = out / f'files-after-{n:02}'
    if snap.exists():
        raise RuntimeError(f'snapshot exists: {snap}')
    shutil.copytree(run, snap, ignore=shutil.ignore_patterns('skill', 'materials', 'AGENTS.md', '__pycache__'))
    row = {'arm': arm, 'packet': state['packet'], 'replicate': state['replicate'], 'turn': n,
           'start_unix': started, 'wall_seconds': elapsed, 'returncode': rc,
           'usage': done[0].get('usage') if len(done) == 1 else None,
           'complete': rc == 0 and len(done) == 1, 'error': error}
    external_reads = []
    for event in events:
        item = event.get('item', {})
        command = item.get('command', '').replace('\\', '/').lower()
        if item.get('type') == 'command_execution' and ('.agents/skills' in command or '.codex/skills' in command):
            external_reads.append(item.get('id'))
    row['external_skill_commands'] = external_reads
    if external_reads:
        row['complete'] = False
        row['error'] = 'external_skill_access_invalidates_session'
    dump(out / f'{stem}.meta.json', row)
    if not row['complete']:
        a['failed'] = True
        dump(work / 'state.json', state)
        raise RuntimeError(f'{arm}/{state["packet"]}/rep{state["replicate"]} turn {n} incomplete; evidence retained')
    return row


def turn1_gate(row, arm, packet):
    out = REPORT / 'runs' / f'{arm}-{packet}-rep{row["replicate"]}'
    events = json.loads('[' + ','.join((out / 'turn-01.jsonl').read_text(encoding='utf-8').splitlines()) + ']')
    successful = [e['item'] for e in events if e.get('type') == 'item.completed'
                  and e.get('item', {}).get('type') == 'command_execution'
                  and e['item'].get('exit_code') == 0 and e['item'].get('status') == 'completed']
    reads = [x for x in successful if any(k in x.get('command', '').lower()
             for k in ('get-content', 'type ', 'cat ', 'read_text', 'read_bytes', 'open('))]
    material_read = any('materials' in x.get('command', '').lower() and x.get('aggregated_output', '').strip() for x in reads)
    skill_read = any('skill' in x.get('command', '').lower() and 'skill.md' in x.get('command', '').lower()
                     and x.get('aggregated_output', '').strip() for x in reads)
    return {'materials_content_read': material_read, 'skill_content_read': skill_read if arm in ('B', 'C') else True}



def run_session(packet, rep, arm_order, work, script, state, cli, turn_ids, answers=None, phase='phase1'):
    rows = []
    for arm in arm_order:
        for original in script['turns']:
            if int(original['id']) not in turn_ids:
                continue
            turn = dict(original)
            if turn['text'] == 'ADAPTIVE':
                turn['text'] = answers[arm]
            row = call(script, state, arm, turn, work, cli, phase)
            rows.append(row)
            dump(REPORT / f'partial-{packet}-rep{rep}-{phase}.json', rows)
            dump(work / 'state.json', state)
            if phase == 'phase1' and int(turn['id']) == 1:
                gate = turn1_gate(row, arm, packet)
                dump(REPORT / f'gate-{arm}-{packet}-rep{rep}.json', {'packet': packet, 'replicate': rep, 'arm': arm, 'gate': gate})
                if not all(gate.values()):
                    raise RuntimeError(f'turn-1 materials/skill read gate failed for {arm}; aborting before further calls')
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--packet', choices=PACKETS, required=True)
    ap.add_argument('--replicate', type=int, choices=[1, 2], required=True)
    ap.add_argument('--phase', choices=['phase1', 'phase2'], required=True)
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    work = args.work.resolve()
    cli = shutil.which('codex')
    if not cli:
        raise RuntimeError('codex CLI not found')
    version = subprocess.check_output([cli, '--version'], text=True).strip()
    fingerprint = verify_fingerprint()
    if version != 'codex-cli 0.162.1':
        raise RuntimeError(f'CLI version {version} differs from pilot; protocol requires aborting comparison')
    protocol_path = REPORT / 'protocol.json'
    if not protocol_path.exists():
        if args.phase != 'phase1' or args.packet != 'S' or args.replicate != 1:
            raise RuntimeError('first call must initialize S/rep1 phase1')
        (REPORT / 'skill-B').mkdir(parents=True)
        skill_archive(B_REV, REPORT / 'skill-B')
        (REPORT / 'skill-C').mkdir(parents=True)
        skill_archive(C_REV, REPORT / 'skill-C')
        protocol = {'model': MODEL, 'reasoning_effort': EFFORT, 'cli_version': version,
                    'baseline': B_REV, 'arm_c_revision': C_REV, 'arm_c_sha256': fingerprint,
                    'design': '4 arms x 2 packets x 2 replicates; serial within each session; arm order interleaved by replicate; phase1 turns 1-6 and phase2 turns 7-11.',
                    'sanitization': ['absolute work/user paths replaced with <ROOT>', 'study file links made relative', 'misdecoded CJK codepoints U+3400-U+9FFF replaced with U+FFFD'],
                    'limits': 'Synthetic packets, one model/CLI, scripted student, author-written prompts; no learning gains, real students, other models, artifacts, print or billing.'}
        dump(protocol_path, protocol)
    source = packet_files(args.packet)
    if args.phase == 'phase1':
        script, state, fixture_hashes, cli = prepare(work, args.packet, args.replicate)
        if args.packet == 'S':
            shutil.copytree(source, REPORT / 'fixtures' / 'packet-s', dirs_exist_ok=True)
        arm_order = ['A1', 'A2', 'B', 'C'] if args.replicate == 1 else ['C', 'B', 'A2', 'A1']
        try:
            rows = run_session(args.packet, args.replicate, arm_order, work, script, state, cli, range(1, 7))
        finally:
            for a in state['arms'].values():
                (Path(a['home']) / 'auth.json').unlink(missing_ok=True)
        dump(REPORT / f'results-{args.packet}-rep{args.replicate}-phase1.json', {'fixture_sha256': fixture_hashes, 'rows': rows})
        print(f'PHASE1 COMPLETE {args.packet}/rep{args.replicate}: inspect turn-06 responses; next write unique turn7 answers and invoke phase2.')
    else:
        state_path = work / 'state.json'
        state = json.loads(state_path.read_text(encoding='utf-8'))
        script = json.loads((source / 'script.json').read_text(encoding='utf-8'))
        answers = json.loads((REPORT / 'turn7-answers.json').read_text(encoding='utf-8'))
        key = f'{args.packet}-rep{args.replicate}'
        if key not in answers:
            raise RuntimeError('turn7 answers missing for this packet/replicate')
        order = ['A1', 'A2', 'B', 'C'] if args.replicate == 1 else ['C', 'B', 'A2', 'A1']
        rows = []
        for a in state['arms'].values():
            shutil.copy2(Path.home() / '.codex/auth.json', Path(a['home']) / 'auth.json')
        try:
            rows = run_session(args.packet, args.replicate, order, work, script, state, cli, range(7, 12), answers[key], 'phase2')
        finally:
            for arm in ARMS:
                auth = Path(state['arms'][arm]['home']) / 'auth.json'
                if auth.exists():
                    auth.unlink()
        dump(REPORT / f'results-{args.packet}-rep{args.replicate}-phase2.json', rows)
        for arm in ARMS:
            run = Path(state['arms'][arm]['cwd'])
            out = REPORT / 'runs' / f'{arm}-{args.packet}-rep{args.replicate}'
            if (out / 'final-files').exists():
                raise RuntimeError(f'final mirror exists: {out}')
            shutil.copytree(run, out / 'final-files', ignore=shutil.ignore_patterns('skill','materials','AGENTS.md','__pycache__'))
        print(f'PHASE2 COMPLETE {args.packet}/rep{args.replicate}; credentials removed.')


if __name__ == '__main__':
    main()
