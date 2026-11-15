"""Fake-CLI checks for T007; never calls a real model or uses a real login."""
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
import run_cost_comparison as runner

FAKE = r'''
from pathlib import Path
import json,os,sys
if sys.argv[1:]==['--version']:
 print('fake-cli');raise SystemExit
home=Path(os.environ['CODEX_HOME']);assert (home/'auth.json').exists()
assert not any(k.startswith('CODEX_') and k!='CODEX_HOME' for k in os.environ)
assert 'skills.bundled.enabled=false' in sys.argv
counter=home/'counter';n=int(counter.read_text())+1 if counter.exists() else 1;counter.write_text(str(n))
mode=os.environ.get('FAKE_MODE','ok');sys.stdin.read()
print(json.dumps({'type':'thread.started','thread_id':'fake-thread'}))
def command(c,o):
 print(json.dumps({'type':'item.completed','item':{'type':'command_execution','id':'cmd','command':c,'aggregated_output':o,'exit_code':0,'status':'completed'}}))
if n==1:
 command('Get-Content skill/SKILL.md materials/outline.md',Path('skill/SKILL.md').read_text(encoding='utf8')+Path('materials/outline.md').read_text(encoding='utf8'))
if n==2 or mode=='early':
 for f in ['course-profile.md','learning-record.md']:Path(f).write_text('synthetic record')
if n==2:
 command('python skill/scripts/record_io.py '+('read' if mode=='fallback' else 'save')+' --dir . --create','{"saved":true}')
if mode=='external':command(r'cat C:\\Users\\example\\.AGENTS\\Skills\\x\\SKILL.md','external')
if mode=='malformed':print('{invalid');raise SystemExit(3)
print(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'synthetic reply'}}))
print(json.dumps({'type':'turn.completed','usage':{'input_tokens':n*10,'cached_input_tokens':0,'output_tokens':n*2}}))
'''


def main():
    scratch=Path.home()/'codex-runs/T007-review'
    with tempfile.TemporaryDirectory(prefix='fake-check-',dir=scratch) as folder:
        t=Path(folder);cli=t/'fake_cli.py';cli.write_text(FAKE,encoding='utf8')
        auth=t/'auth.json';auth.write_text('{"dummy":true}',encoding='utf8')
        packet=ROOT/'tests/reports/2026-11-14-controlled-comparison/frozen-packet-s-git'
        def run(name,mode='ok',phase='smoke',arm='D'):
            cmd=[sys.executable,str(ROOT/'tests/run_cost_comparison.py'),'--phase',phase,'--arm',arm,'--packet','S',
                 '--replicate','1','--report',str(t/name/'report'),'--work',str(t/name/'work'),
                 '--packet-source',str(packet),'--cli',str(cli),'--auth',str(auth),'--nonlogin-shell']
            r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',env=dict(os.environ,FAKE_MODE=mode,CODEX_EXTRA='strip'))
            assert not list((t/name/'work').rglob('auth.json')),(name,r.stderr)
            return r
        r=run('good');assert r.returncode==0,r.stderr
        gate=json.loads((t/'good/report/smoke-gate.json').read_text(encoding='utf8'));assert all(gate.values())
        assert len(list((t/'good/report/runs/D-S-rep1').glob('*.meta.json')))==2
        before=(t/'good/report/runs/D-S-rep1/turn-01.stdout.txt').read_bytes()
        r=run('good');assert r.returncode!=0
        assert before==(t/'good/report/runs/D-S-rep1/turn-01.stdout.txt').read_bytes()
        for mode in ('early','fallback','external','malformed'):
            r=run(mode,mode);assert r.returncode!=0,(mode,r.stdout)
            assert (t/mode/'report/runs/D-S-rep1/turn-01.stdout.txt').is_file()
        r=run('phases',phase='phase1');assert r.returncode==0,r.stderr
        (t/'phases/report/turn7-answers.json').write_text('{"D":"my own correct answer"}',encoding='utf8')
        r=run('phases',phase='phase2');assert r.returncode==0,r.stderr
        assert len(list((t/'phases/report/runs/D-S-rep1').glob('*.meta.json')))==11
        r=run('phases',phase='phase2');assert r.returncode!=0
        r=run('concurrent-C',phase='phase1',arm='C');assert r.returncode==0,r.stderr
        assert len(list((t/'concurrent-C/report/runs/C-S-rep1').glob('*.meta.json')))==6
        state=json.loads((t/'good/work/state.json').read_text(encoding='utf8'))
        args=SimpleNamespace(report=t/'timeout-report',work=t/'good/work',arm='D',packet='S',replicate=1,cli=str(cli),nonlogin_shell=True)
        with patch.object(runner.subprocess,'run',side_effect=subprocess.TimeoutExpired('fake',900,output=b'{partial',stderr=b'timed out')):
            try:
                with runner.credentials(Path(state['home']),auth):
                    runner.call(args,state,{'context':'','openers':{'B':''}},{'id':99,'text':'fake timeout'})
            except RuntimeError:
                pass
            else:
                raise AssertionError('timeout accepted')
        assert not list((t/'good/work').rglob('auth.json'))
        assert (t/'timeout-report/runs/D-S-rep1/turn-99.stdout.txt').read_text()=='{partial'
        assert not json.loads((t/'timeout-report/runs/D-S-rep1/turn-99.meta.json').read_text())['complete']
        events=[{'item':{'type':'command_execution','id':'x','command':r'cat C:\\Users\\example\\.AGENTS\\Skills\\x'}}]
        assert runner.external_commands(events)==['x']
        for n in (1,2,4,8):
            variant=str(Path.home()).swapcase().replace('\\','\\'*n)
            assert '<ROOT>' in runner.scrub(variant,t)
    print('PASS: smoke gates, exact two turns, C/D phases, repeat refusal, auth cleanup, raw failure evidence, escaped/case access audit and path scrub. Fake CLI only.')


if __name__=='__main__':
    main()
