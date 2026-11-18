#!/usr/bin/env python3
"""Fake-CLI harness and deterministic saved-output checks; no model calls."""
from pathlib import Path
import importlib.util, json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('feature_pilot',ROOT/'tests/run_feature_pilot.py')
runner=importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
FAKE=r'''from pathlib import Path
import json,os,sys
if sys.argv[1:]==['--version']:
 print('fake-codex-cli 1.0'); raise SystemExit
assert os.environ.get('CODEX_HOME')
assert not any(k.startswith('CODEX_') and k!='CODEX_HOME' for k in os.environ)
assert '--ignore-user-config' in sys.argv and 'skills.bundled.enabled=false' in sys.argv
assert 'windows.sandbox="unelevated"' in sys.argv, 'Windows sandbox must be unelevated or every shell command is blocked (T016 smoke 1)'
prompt=sys.stdin.read()
print(json.dumps({'type':'thread.started','thread_id':'fake-thread'}))
print(json.dumps({'type':'item.completed','item':{'type':'command_execution','id':'read','command':'Get-Content skills/gpt-im-cooked/SKILL.md STA/materials/outline.md','aggregated_output':"name: gpt-im-cooked\n# STAT 110 (synthetic) materials"}}))
print(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'Fake tutor response.'}}))
print(json.dumps({'type':'turn.completed','usage':{'input_tokens':100,'cached_input_tokens':20,'output_tokens':10}}))
'''

def check_outputs(root):
    root=Path(root); data=json.loads((root/'checks-input.json').read_text(encoding='utf-8-sig'))
    results={}
    # C2: logged planner command and delivered files.
    results['C2']=('plan_study.py' in data['calendar']['commands'] and (root/'plan.ics').is_file() and (root/'calendar.html').is_file())
    # C3-C4: every basis names known concepts and kinds match ground truth.
    expected_data=json.loads((ROOT/'tests/fixtures/feature-pilot/expected.json').read_text(encoding='utf-8-sig'))
    expected={cid for course in expected_data.values() if 'concepts' in course for cid in course['concepts']}
    tasks=data['calendar']['tasks']; known=set(expected)
    results['C3']=all(any(cid in task.get('basis','') for cid in known) for task in tasks if task.get('course') in ('STA','CS'))
    kind_map={'recheck':('recheck',),'variant':('variant',),'source-gap':('source-gap',),
              'transfer practice':('practice',),'learn then practice':('learn','practice'),'none':()}
    results['C4']=True
    for course,record in expected_data.items():
        for cid,concept in record['concepts'].items():
            matching=[t for t in tasks if t.get('course')==course and t.get('concept_id')==cid]
            kinds=kind_map[concept['kind']]
            results['C4'] &= (all(any(t.get('kind')==kind for t in matching) for kind in kinds) if kinds else not matching)
    t1=[t for t in tasks if t.get('concept_id')=='T1' and t.get('course')=='STA']
    t4=[t for t in tasks if t.get('concept_id')=='T4' and t.get('course')=='STA']
    results['C4']=results['C4'] and bool(t1) and all(t.get('not_before','')>='2026-11-18' for t in t1) and any(t.get('kind')=='practice' for t in t4)
    hist=[t for t in tasks if t.get('course')=='HIST 101']
    results['C5']=data['calendar']['hist_offer_count']==1 and bool(hist) and all(t.get('kind')=='review' and t.get('basis')=='No learning record' for t in hist)
    sheet=data['sheet']
    results['S2']=sheet['first_draft_pdf'] and sheet['pages']<=2 and 'render_sheet.py' in sheet['commands']
    results['S4']=sheet['revision_applied'] and not sheet['new_topics']
    results['S5']=sheet['preference_saved'] and sheet['fresh_turn_followed_preference']
    return results

def main():
    assert runner.usage_delta({'input_tokens':10,'output_tokens':2},{'input_tokens':16,'output_tokens':5})=={'input_tokens':6,'output_tokens':3}
    try: runner.usage_delta({'input_tokens':10},{'input_tokens':9})
    except RuntimeError: pass
    else: raise AssertionError('decreasing cumulative usage was silently accepted')
    with tempfile.TemporaryDirectory(prefix='feature-pilot-check-') as td:
        t=Path(td); fake=t/'fake_cli.py'; fake.write_text(FAKE,encoding='utf-8-sig')
        # Three smoke cases: New calendar, Old sheet, New sheet. These are diagnostic fakes only.
        auth=t/'auth.json';auth.write_text('{"fake":true}',encoding='utf-8')
        cmd=[sys.executable,str(ROOT/'tests/run_feature_pilot.py'),'--run-smoke','--cli',str(fake),'--auth',str(auth),'--report',str(t/'report'),'--work',str(t/'work')]
        env=dict(os.environ,CODEX_INHERITED='must-be-stripped')
        p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8-sig',env=env)
        assert p.returncode==0,(p.stdout,p.stderr)
        proto=json.loads((t/'report/protocol.json').read_text(encoding='utf-8-sig'))
        assert proto['cli_version']=='fake-codex-cli 1.0' and proto['model']=='gpt-6-luna' and proto['reasoning_effort']=='medium'
        for label in ('calendar-New-rep99','sheet-Old-rep99','sheet-New-rep99'):
            meta=json.loads((t/f'report/runs/{label}/turn-01.meta.json').read_text(encoding='utf-8-sig'))
            assert meta['complete'] and meta['material_read'] and meta['skill_read']
            assert (t/f'report/runs/{label}/files-after-01').is_dir()
        assert len(list((t/'report/runs').glob('*/turn-01.meta.json')))==3
        assert not list((t/'work').rglob('auth.json'))
        # Saved-output checks use a compact deterministic evidence fixture; no student/model data.
        d=t/'saved';d.mkdir()
        fixture={'calendar':{'commands':'python plan_study.py','tasks':[
            {'course':'STA','concept_id':'T1','kind':'recheck','basis':'T1 conditional probability','not_before':'2026-11-18'},
            {'course':'STA','concept_id':'T2','kind':'variant','basis':'T2 tables'},
            {'course':'STA','concept_id':'T3','kind':'source-gap','basis':'T3 Bayes rule notes missing'},
            {'course':'STA','concept_id':'T4','kind':'learn','basis':'T4 grouped summaries'},
            {'course':'STA','concept_id':'T4','kind':'practice','basis':'T4 grouped summaries'},
            {'course':'CS','concept_id':'P1','kind':'practice','basis':'P1 list aliasing transfer'},
            {'course':'CS','concept_id':'P2','kind':'variant','basis':'P2 loop tracing'},
            {'course':'CS','concept_id':'P3','kind':'source-gap','basis':'P3 Big-O notes missing'},
            {'course':'CS','concept_id':'P4','kind':'learn','basis':'P4 nested data summaries'},
            {'course':'CS','concept_id':'P4','kind':'practice','basis':'P4 nested data summaries'},
            {'course':'HIST 101','kind':'review','basis':'No learning record'}], 'hist_offer_count':1},
            'sheet':{'first_draft_pdf':True,'pages':2,'commands':'python render_sheet.py','revision_applied':True,'new_topics':[],'preference_saved':True,'fresh_turn_followed_preference':True}}
        (d/'checks-input.json').write_text(json.dumps(fixture),encoding='utf-8')
        (d/'plan.ics').write_text('BEGIN:VCALENDAR\nEND:VCALENDAR\n',encoding='utf-8'); (d/'calendar.html').write_text('<html></html>',encoding='utf-8')
        checks=check_outputs(d); assert all(checks.values()),checks
        # Negative probes ensure material checks reject broken output.
        broken=json.loads((d/'checks-input.json').read_text(encoding='utf-8'));broken['sheet']['new_topics']=['extra'];(d/'checks-input.json').write_text(json.dumps(broken),encoding='utf-8')
        assert check_outputs(d)['S4'] is False
    print('PASS: fake CLI only; 3 isolated smoke turns; read gates, config isolation, snapshots, cumulative usage metadata, and automatic C2-C5/S2/S4/S5 checks.')
if __name__=='__main__': main()


