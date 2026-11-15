"""T007 adapter for the frozen T004 script. Real CLI calls; smoke is diagnostic only."""
from contextlib import contextmanager
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

import run_controlled_comparison as frozen

ROOT = Path(__file__).resolve().parents[1]
REVISIONS = {'C': frozen.C_REV, 'D': '9938d36d8538cc4476b0fcf3e37db9e8faa79d59'}
TEXT = {'.md', '.json', '.jsonl', '.txt', '.bak'}


def scrub(text, work):
    variants = set()
    for root in (work, ROOT, Path.home(), Path(tempfile.gettempdir()), Path('C:/Program Files')):
        variants.add(str(root).replace('\\', '/'))
        for n in (1, 2, 4, 8):
            variants.add(str(root).replace('\\', '\\' * n))
    for root in sorted(variants, key=len, reverse=True):
        text = re.sub(re.escape(root), lambda _: '<ROOT>', text, flags=re.I)
    return re.sub('[\u3400-\u9fff]', '\ufffd', text)


def scrub_tree(folder, work):
    for p in folder.rglob('*'):
        if p.is_file() and p.suffix in TEXT:
            old = p.read_text(encoding='utf-8-sig', errors='replace')
            new = scrub(old, work)
            if new != old:
                p.write_text(new, encoding='utf-8', newline='')


def events_in(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def external_commands(events):
    return [e['item'].get('id', 'unknown') for e in events
            if e.get('item', {}).get('type') == 'command_execution'
            and re.search(r'\.(?:agents|codex)/skills(?:/|\b)',
                          re.sub(r'[\\/]+', '/', e['item'].get('command', '')).lower())]


@contextmanager
def credentials(home, source):
    dest = home / 'auth.json'
    try:
        shutil.copy2(source, dest)
        yield
    finally:
        dest.unlink(missing_ok=True)


def call(args, state, script, turn):
    run, home, out = Path(state['cwd']), Path(state['home']), args.report / 'runs' / state['label']
    n = int(turn['id'])
    stem = f'turn-{n:02}'
    if (out / f'{stem}.meta.json').exists():
        raise RuntimeError('Refusing to repeat a completed or failed turn')
    prompt = turn['text']
    if turn.get('new_session'):
        state['session'] = None
        prompt = script['context'] + script['resume_openers']['B'] + prompt
    elif state['session'] is None:
        prompt = script['context'] + script['openers']['B'] + prompt
    disabled = sorted({p.resolve().as_posix() for d in (Path.home()/'.agents/skills', Path.home()/'.codex/skills')
                       for p in d.rglob('SKILL.md')})
    selectors = 'skills.config=[' + ','.join('{path='+json.dumps(p)+',enabled=false}' for p in disabled) + ']'
    common = ['--json', '--skip-git-repo-check', '--ignore-user-config', '-c', selectors,
              '-c', 'skills.bundled.enabled=false', '-m', frozen.MODEL,
              '-c', f'model_reasoning_effort="{frozen.EFFORT}"', '-c', 'approval_policy="never"',
              '-c', 'sandbox_mode="workspace-write"', '-c', 'windows.sandbox="unelevated"']
    if args.nonlogin_shell:
        common += ['--strict-config', '-c', 'allow_login_shell=false',
                   '-c', 'shell_environment_policy.experimental_use_profile=false']
    cmd = ([sys.executable, args.cli] if args.cli.endswith('.py') else [args.cli]) + ['exec']
    cmd += ['resume'] + common + [state['session'], '-'] if state['session'] else common + ['-C', str(run), '-']
    env = {k:v for k,v in os.environ.items() if not k.startswith('CODEX_')}
    env.update(CODEX_HOME=str(home), PYTHONUTF8='1')
    out.mkdir(parents=True, exist_ok=True)
    (out/f'prompt-{n:02}.md').write_text(prompt, encoding='utf-8', newline='')
    started = time.time()
    failure = None
    try:
        proc = subprocess.run(cmd, input=prompt, cwd=run, env=env, capture_output=True,
                              text=True, encoding='utf-8', errors='replace', timeout=900)
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        def as_text(v):
            return v.decode('utf-8', 'replace') if isinstance(v, bytes) else (v or '')
        stdout, stderr, rc = as_text(exc.stdout), as_text(exc.stderr), 124
        failure = 'timeout'
    (out/f'{stem}.stdout.txt').write_text(scrub(stdout,args.work), encoding='utf-8', newline='')
    (out/f'{stem}.stderr.txt').write_text(scrub(stderr,args.work), encoding='utf-8', newline='')
    snap = out/f'files-after-{n:02}'
    shutil.copytree(run, snap, ignore=shutil.ignore_patterns('skill','materials','AGENTS.md','__pycache__'))
    scrub_tree(snap, args.work)
    events, malformed = [], 0
    for line in stdout.splitlines():
        if line.strip().startswith('{'):
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                malformed += 1
    (out/f'{stem}.jsonl').write_text(scrub(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events),args.work), encoding='utf-8', newline='')
    done = [e for e in events if e.get('type') == 'turn.completed']
    for e in events:
        if e.get('type') == 'thread.started':
            state['session'] = e['thread_id']
    external = external_commands(events)
    if failure is None and (rc or len(done)!=1 or malformed or external):
        failure = 'external_skill_access' if external else 'incomplete_or_malformed'
    reply = '\n\n'.join(e['item'].get('text','') for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message')
    reply = scrub(reply,args.work)
    for prefix in (f'/<ROOT>/{run.name}/', f'<ROOT>/{run.name}/'):
        reply = reply.replace(prefix, '')
    (out/f'response-{n:02}.md').write_text(reply,encoding='utf-8',newline='')
    row = {'arm':args.arm,'packet':args.packet,'replicate':args.replicate,'turn':n,
           'start_unix':started,'wall_seconds':round(time.time()-started,2),'returncode':rc,
           'usage':done[0].get('usage') if len(done)==1 else None,'complete':failure is None,
           'error':failure,'external_skill_commands':external}
    frozen.dump(out/f'{stem}.meta.json',row)
    state['last_turn'] = n
    state['failed'] = failure is not None
    frozen.dump(args.work/'state.json',state)
    if failure:
        raise RuntimeError(f'{state["label"]} turn{n} failed: {failure}; STOP, evidence retained')
    print(f'DONE {state["label"]} turn{n}',flush=True)
    return row


def smoke_gate(out):
    first = events_in(out/'turn-01.jsonl')
    reads = [e['item'] for e in first if e.get('type')=='item.completed'
             and e.get('item',{}).get('type')=='command_execution']
    material = any('materials' in x.get('command','').lower() and '# stat 110 (synthetic)' in x.get('aggregated_output','').lower() for x in reads)
    skill = any('skill.md' in x.get('command','').lower() and "# gpt, i'm cooked" in x.get('aggregated_output','').lower() for x in reads)
    commands = [e['item'] for e in events_in(out/'turn-02.jsonl') if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
    save = [x for x in commands if re.search(r'record_io\.py[\"\x27]?\s+save\b',x.get('command',''))]
    fallback = [x for x in commands if re.search(r'record_io\.py[\"\x27]?\s+(?:read|update|commit)\b',x.get('command',''))]
    wrappers = [x for x in commands if 'record_io.py' in x.get('command','') and re.search(r'(?:python\s+-c|exec\(|subprocess\.)',x.get('command',''))]
    records = lambda n: {p.name for p in (out/f'files-after-{n:02}').rglob('*.md') if p.name in ('course-profile.md','learning-record.md')}
    return {'materials_read':material,'skill_read':skill,
            'no_global_access':not external_commands(first+events_in(out/'turn-02.jsonl')),
            'record_files_absent_turn1':not records(1),'both_record_files_present_turn2':records(2)=={'course-profile.md','learning-record.md'},
            'one_successful_save_command':len(save)==1 and save[0].get('exit_code')==0,
            'no_separate_read_update_commit':not fallback,'no_inline_save_wrapper':not wrappers}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase',choices=['smoke','phase1','phase2'],required=True)
    ap.add_argument('--arm',choices=['C','D'],required=True)
    ap.add_argument('--packet',choices=['S','P'],required=True)
    ap.add_argument('--replicate',type=int,choices=[1,2],required=True)
    for name in ('report','work','packet-source'):
        ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--nonlogin-shell',action='store_true')
    ap.add_argument('--cli',default=shutil.which('codex'))
    ap.add_argument('--auth',type=Path,default=Path.home()/'.codex/auth.json')
    args = ap.parse_args()
    args.work,args.report,args.packet_source = args.work.resolve(),args.report.resolve(),args.packet_source.resolve()
    script = json.loads((args.packet_source/'script.json').read_text(encoding='utf-8'))
    if args.phase=='smoke' and (args.arm,args.packet)!=('D','S'):
        raise RuntimeError('Smoke is exactly D/S turns1-2')
    if args.phase!='phase2':
        if args.report.exists() or args.work.exists():
            raise RuntimeError('New report AND work paths required')
        if 'onedrive' in str(args.work).lower() or 'temp' in str(args.work).lower() or ROOT in args.work.parents:
            raise RuntimeError('Work must be outside repo, OneDrive and Temp')
        version = subprocess.check_output(([sys.executable,args.cli] if args.cli.endswith('.py') else [args.cli])+['--version'],text=True).strip()
        if not args.cli.endswith('.py') and version!='codex-cli 0.162.1':
            raise RuntimeError('CLI differs from frozen comparison')
        label=f'{args.arm}-{args.packet}-rep{args.replicate}'
        run,home=args.work/f'run-{label}',args.work/f'home-{label}'
        home.mkdir(parents=True)
        shutil.copytree(args.packet_source/'materials',run/'materials')
        (run/'AGENTS.md').write_text('Isolated synthetic study directory. Use only local files; do not browse, delegate, or contact services.\n',encoding='utf-8')
        frozen.skill_archive(REVISIONS[args.arm],run/'skill')
        shutil.copytree(run/'skill',args.report/f'skill-{args.arm}')
        shutil.copytree(args.packet_source,args.report/'fixtures'/f'packet-{args.packet.lower()}')
        state={'run_id':uuid.uuid4().hex,'report':str(args.report),'cwd':str(run),'home':str(home),'label':label,
               'session':None,'failed':False,'last_turn':0,'arm':args.arm,'packet':args.packet,'replicate':args.replicate,
               'diagnostic':args.phase=='smoke','nonlogin_shell':args.nonlogin_shell}
        frozen.dump(args.work/'state.json',state)
        frozen.dump(args.report/'protocol.json',{'run_id':state['run_id'],'model':frozen.MODEL,'effort':frozen.EFFORT,
                    'cli':version,'C':REVISIONS['C'],'D':REVISIONS['D'],'diagnostic':state['diagnostic'],
                    'nonlogin_shell':args.nonlogin_shell,'skill_sha256':{p.relative_to(run/'skill').as_posix():frozen.sha(p) for p in (run/'skill').rglob('*') if p.is_file()},
                    'fixture_sha256':{p.relative_to(args.packet_source).as_posix():frozen.sha(p) for p in args.packet_source.rglob('*') if p.is_file()}})
    else:
        state=json.loads((args.work/'state.json').read_text(encoding='utf-8'))
        protocol=json.loads((args.report/'protocol.json').read_text(encoding='utf-8'))
        assert state['report']==str(args.report) and state['run_id']==protocol['run_id']
        assert not state['failed'] and not state['diagnostic'] and state['last_turn']==6
        assert all(state[k]==getattr(args,k) for k in ('arm','packet','replicate','nonlogin_shell'))
        answers=json.loads((args.report/'turn7-answers.json').read_text(encoding='utf-8'))
        assert set(answers)=={args.arm} and answers[args.arm].strip()
    ids = range(1,3) if args.phase=='smoke' else range(1,7) if args.phase=='phase1' else range(7,12)
    rows=[]
    with credentials(Path(state['home']),args.auth):
        for original in script['turns']:
            if original['id'] not in ids:
                continue
            turn=dict(original)
            if turn['text']=='ADAPTIVE':
                turn['text']=answers[args.arm]
            rows.append(call(args,state,script,turn))
            if turn['id']==1:
                first=events_in(args.report/'runs'/state['label']/'turn-01.jsonl')
                content='\n'.join(e.get('item',{}).get('aggregated_output','') for e in first)
                assert any(h in content.lower() for h in ('# stat 110 (synthetic)','# cs 101 (synthetic)')), 'No actual materials read; stop'
                assert "# gpt, i'm cooked" in content.lower(), 'No actual skill read; stop'
    frozen.dump(args.report/f'results-{args.phase}.json',rows)
    if args.phase=='smoke':
        gate=smoke_gate(args.report/'runs'/state['label'])
        frozen.dump(args.report/'smoke-gate.json',gate)
        if not all(gate.values()):
            raise RuntimeError('Smoke gate failed; STOP before comparison')
    print(args.phase.upper()+' COMPLETE; credentials removed.',flush=True)


if __name__=='__main__':
    main()
