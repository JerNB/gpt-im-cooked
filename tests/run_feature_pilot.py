#!/usr/bin/env python3
"""Opt-in fresh-model feature pilot. Default invocation performs no model calls."""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time, uuid

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/feature-pilot'
REPORT_DEFAULT = ROOT / 'tests/reports/2026-11-18-feature-pilot'
NEW, OLD = '74dceec', '20bb271'
MODEL, EFFORT = 'gpt-6-luna', 'medium'
CALENDAR = [
    "Today is Wednesday 2026-11-18. My STA and CS finals are coming up (folders are here). Can you make me a study calendar?",
    "Exams: STA Dec 8, 9am-12pm; CS Dec 10, 2-5pm. I can study weekdays 7-10pm and weekends 2-6pm, not Nov 25-27 (Thanksgiving). At most 3 hours a day.",
    "Yes, please also add HIST 101: exam Dec 11 at 9am, about 2 hours a week."
]
SHEET = [
    "Today is Wednesday 2026-11-18. Can you make me a study guide for my STA final?",
    "It's a cheat sheet I can bring into the exam: one sheet, both sides.",
    "Please replace the abstract interpretation rules with one worked example, and use the space you save to make it easier to read. Don't add new information.",
    "Today is Thursday 2026-11-19. Make me a cheat sheet for my STA final."
]

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def dump(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def scrub(text, roots):
    for root in sorted({str(Path(x).resolve()).replace('\\','/') for x in roots if x},key=len,reverse=True):
        text=re.sub(re.escape(root),'<ROOT>',str(text),flags=re.I)
    return re.sub('[\u3400-\u9fff]','\ufffd',str(text))

def archive(rev,dest):
    dest.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['git','archive',rev,'plugins/gpt-im-cooked/skills/gpt-im-cooked'],cwd=ROOT)
    import io,tarfile
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:') as tf:
        prefix='plugins/gpt-im-cooked/skills/gpt-im-cooked/'
        for member in tf.getmembers():
            if not member.isfile() or not member.name.startswith(prefix): continue
            rel=member.name[len(prefix):]; out=dest/rel; out.parent.mkdir(parents=True,exist_ok=True)
            with tf.extractfile(member) as src: out.write_bytes(src.read())
    return {p.relative_to(dest).as_posix():sha(p) for p in sorted(dest.rglob('*')) if p.is_file()}

def events(text):
    out=[]
    for line in text.splitlines():
        try: out.append(json.loads(line))
        except json.JSONDecodeError: pass
    return out

def usage_delta(previous,current):
    delta={k:int(v)-int(previous.get(k,0)) for k,v in current.items() if isinstance(v,(int,float))}
    if any(v<0 for v in delta.values()): raise RuntimeError(f'cumulative usage decreased: {delta}')
    return delta

def cli_prefix(cli): return [sys.executable,str(cli)] if str(cli).lower().endswith('.py') else [str(cli)]

def run_turn(cli,work,report,run,home,session,arm,kind,rep,turn,prompt,new_session=False):
    label=f'{kind}-{arm}-rep{rep}'
    out=report/'runs'/label; out.mkdir(parents=True,exist_ok=True)
    stem=f'turn-{turn:02}'
    if (out/f'{stem}.meta.json').exists(): raise RuntimeError(f'refusing repeat of existing turn {label}/{turn}')
    if new_session: session=None
    disabled=sorted({str(p.resolve()).replace('\\','/') for base in (Path.home()/'.agents/skills',Path.home()/'.codex/skills') if base.exists() for p in base.rglob('SKILL.md')})
    selectors='skills.config=['+','.join('{path='+json.dumps(p)+',enabled=false}' for p in disabled)+']'
    args=['--json','--skip-git-repo-check','--ignore-user-config','-c',selectors,'-c','skills.bundled.enabled=false','-m',MODEL,'-c',f'model_reasoning_effort="{EFFORT}"','-c','approval_policy="never"','-c','sandbox_mode="workspace-write"']
    cmd=cli_prefix(cli)+['exec']+(['resume']+args+[session,'-'] if session else args+['-C',str(run),'-'])
    env={k:v for k,v in os.environ.items() if not k.startswith('CODEX_')}; env.update(CODEX_HOME=str(home),PYTHONUTF8='1')
    (out/f'prompt-{turn:02}.md').write_text(prompt,encoding='utf-8')
    start=time.perf_counter(); err=None
    try:
        p=subprocess.run(cmd,input=prompt,cwd=run,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=900)
        stdout,stderr,rc=p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:
        stdout=e.stdout.decode('utf-8','replace') if isinstance(e.stdout,bytes) else (e.stdout or '')
        stderr=e.stderr.decode('utf-8','replace') if isinstance(e.stderr,bytes) else (e.stderr or '')
        rc=124; err='timeout'
    elapsed=round(time.perf_counter()-start,2); ev=events(stdout)
    for e in ev:
        if e.get('type')=='thread.started': session=e.get('thread_id')
    done=[e for e in ev if e.get('type')=='turn.completed']
    external=[e.get('item',{}).get('id') for e in ev if e.get('item',{}).get('type')=='command_execution' and re.search(r'\.(agents|codex)/skills',e.get('item',{}).get('command','').replace('\\','/').lower())]
    complete=(rc==0 and len(done)==1 and not external and err is None)
    if external: err='external_skill_access'
    elif not complete and err is None: err='incomplete_or_malformed'
    (out/f'{stem}.jsonl').write_text(scrub('\n'.join(json.dumps(e,ensure_ascii=False) for e in ev)+'\n',[work,run,home,ROOT,Path.home()]),encoding='utf-8')
    (out/f'{stem}.stderr.txt').write_text(scrub(stderr,[work,run,home,ROOT,Path.home()]),encoding='utf-8')
    reply='\n\n'.join(e.get('item',{}).get('text','') for e in ev if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message')
    (out/f'response-{turn:02}.md').write_text(scrub(reply,[work,run,home,ROOT,Path.home()]),encoding='utf-8')
    snap=out/f'files-after-{turn:02}'
    shutil.copytree(run,snap,ignore=shutil.ignore_patterns('skill','materials','__pycache__'))
    for f in snap.rglob('*'):
        if f.is_file() and f.suffix in {'.md','.txt','.json','.html','.ics'}:
            old=f.read_text(encoding='utf-8-sig',errors='replace'); f.write_text(scrub(old,[work,run,home,ROOT,Path.home()]),encoding='utf-8')
    usage=done[0].get('usage',{}) if len(done)==1 else {}
    row={'arm':arm,'workflow':kind,'replicate':rep,'turn':turn,'wall_seconds':elapsed,'returncode':rc,'usage_cumulative':usage,'complete':complete,'error':err,'external_skill_commands':external}
    dump(out/f'{stem}.meta.json',row)
    if not complete: raise RuntimeError(f'{label} turn {turn} failed ({err}); stopped without retry')
    return session,row,ev

def prepare(report,work,cli):
    if report.exists() or work.exists(): raise RuntimeError('Report/work already exists. Reruns require fresh whole-session paths.')
    report.mkdir(parents=True); work.mkdir(parents=True)
    skills={}
    for arm,rev in [('New',NEW),('Old',OLD)]: skills[arm]=archive(rev,report/f'skill-{arm}')
    ver=subprocess.check_output(cli_prefix(cli)+['--version'],text=True,encoding='utf-8').strip()
    fixture_hashes={p.relative_to(FIXTURES).as_posix():sha(p) for p in sorted(FIXTURES.rglob('*')) if p.is_file()}
    protocol={'model':MODEL,'reasoning_effort':EFFORT,'cli_version':ver,'new_revision':NEW,'old_revision':OLD,'old_tag':'v2.0.1','skill_sha256':skills,'fixture_sha256':fixture_hashes,'sessions':'calendar New x2; sheet Old x2 and New x2; sheet turn 4 starts a new thread','isolation':'CODEX_HOME per session; --ignore-user-config; bundled=false; enumerated global skill selectors disabled; inherited CODEX_* removed; serial; no retries; fresh report/work paths required for reruns.'}
    dump(report/'protocol.json',protocol)
    return ver

def session(cli,report,work,arm,kind,rep,turns,auth):
    run=work/f'{kind}-{arm}-rep{rep}'; home=work/f'home-{kind}-{arm}-rep{rep}'
    run.mkdir(parents=True); home.mkdir(parents=True)
    course='STA' if kind=='sheet' else None
    if kind=='calendar':
        shutil.copytree(FIXTURES/'STA',run/'STA'); shutil.copytree(FIXTURES/'CS',run/'CS')
    else:
        shutil.copytree(FIXTURES/'STA',run/'STA')
        run=run/'STA'
    skill_dest=home/'skills'/'gpt-im-cooked'; skill_dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(report/f'skill-{arm}',skill_dest)
    (run/'AGENTS.md').write_text('Use the available $gpt-im-cooked skill for this tutoring request. Read and follow its SKILL.md and referenced files. Use only supplied local course files; do not browse, delegate, or contact services.\n',encoding='utf-8')
    cli=Path(cli).resolve()
    prompts=CALENDAR if kind=='calendar' else SHEET
    sid=None; usage_prev={}; rows=[]
    for t in turns:
        fresh=(kind=='sheet' and t==4)
        if fresh: usage_prev={}
        msg=prompts[t-1]
        # Each session begins with the fixed opening message, no hidden generated context.
        if not auth or not Path(auth).is_file(): raise RuntimeError('Codex auth file not found; pass --auth')
        auth_dest=home/'auth.json'; shutil.copy2(auth,auth_dest)
        try: sid,row,ev=run_turn(cli,work,report,run,home,sid,arm,kind,rep,t,msg,new_session=fresh)
        finally: auth_dest.unlink(missing_ok=True)
        cur=row['usage_cumulative'] or {}
        row['usage_delta']=usage_delta(usage_prev,cur)
        usage_prev=cur; rows.append(row)
        dump(report/'runs'/f'{kind}-{arm}-rep{rep}'/f'turn-{t:02}.meta.json',row)
        if t==1:
            content='\n'.join(e.get('item',{}).get('aggregated_output','') for e in ev if e.get('item',{}).get('type')=='command_execution').lower()
            ok_mat='stat 110 (synthetic)' in content; ok_skill='name: gpt-im-cooked' in content
            row['material_read']=ok_mat; row['skill_read']=ok_skill
            dump(report/'runs'/f'{kind}-{arm}-rep{rep}'/'turn-01.meta.json',row)
            if not ok_mat or not ok_skill: raise RuntimeError(f'{kind}/{arm} smoke/read gate failed: materials={ok_mat}, skill={ok_skill}')
    dump(report/f'results-{kind}-{arm}-rep{rep}.json',rows)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run-smoke',action='store_true',help='make exactly 3 diagnostic model turns')
    ap.add_argument('--run-main',action='store_true',help='make all 22 frozen study turns')
    ap.add_argument('--cli',default=shutil.which('codex')); ap.add_argument('--auth',type=Path,default=Path.home()/'.codex'/'auth.json'); ap.add_argument('--report',type=Path,default=REPORT_DEFAULT); ap.add_argument('--work',type=Path)
    a=ap.parse_args()
    if a.run_smoke and a.run_main: raise SystemExit('Choose one phase per invocation; smoke and main runs cannot share a report.')
    if not a.run_smoke and not a.run_main:
        print('NO MODEL CALLS: pass --run-smoke or --run-main explicitly.'); return 0
    if not a.cli: raise SystemExit('Codex CLI not found')
    a.report=a.report.resolve(); a.work=(a.work or Path(tempfile.gettempdir())/f'feature-pilot-{uuid.uuid4().hex}').resolve()
    version=prepare(a.report,a.work,a.cli)
    print(f'CLI {version}; report={a.report}; work={a.work}')
    if a.run_smoke:
        session(a.cli,a.report,a.work,'New','calendar',99,[1],a.auth)
        session(a.cli,a.report,a.work,'Old','sheet',99,[1],a.auth)
        session(a.cli,a.report,a.work,'New','sheet',99,[1],a.auth)
        print('SMOKE COMPLETE (diagnostic; excluded from statistics)')
    if a.run_main:
        for rep in (1,2):
            for arm in ('New',): session(a.cli,a.report,a.work,arm,'calendar',rep,[1,2,3],a.auth)
            for arm in (('Old','New') if rep==1 else ('New','Old')): session(a.cli,a.report,a.work,arm,'sheet',rep,[1,2,3,4],a.auth)
    return 0
if __name__=='__main__': raise SystemExit(main())
