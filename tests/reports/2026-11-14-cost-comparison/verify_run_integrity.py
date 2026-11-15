"""Corroborate all eight completed sessions against local CLI ledgers and frozen bytes."""
from pathlib import Path
import json
import sys

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parents[1]))
import run_cost_comparison as runner


def main():
    selected=json.loads((BASE/'selected-completion.json').read_text(encoding='utf-8'))
    assert selected['completed_sessions']==8 and not selected['partial_mode']
    scratch=Path.home()/'codex-runs/T007-review'
    assert not list(scratch.rglob('auth.json'))
    original=json.loads((BASE/'input-verification.json').read_text(encoding='utf-8'))
    for packet,hashes in original['packet_sha256'].items():
        for name,digest in hashes.items():
            assert runner.frozen.sha(scratch/'frozen-packets'/('packet-'+packet)/name)==digest
    fields=('input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens')
    audit={};answers={};gates={}
    for label,relative in selected['selected'].items():
        out=BASE/relative;report=out.parents[1];work=scratch/report.name;home=work/f'home-{label}'
        protocol=json.loads((report/'protocol.json').read_text(encoding='utf-8'))
        skill=work/f'run-{label}'/'skill'
        assert {p.relative_to(skill).as_posix():runner.frozen.sha(p) for p in skill.rglob('*') if p.is_file() and '__pycache__' not in p.parts}==protocol['skill_sha256']
        latest={};deltas=[];external=[];first_events=None
        for n in range(1,12):
            meta=json.loads((out/f'turn-{n:02}.meta.json').read_text(encoding='utf-8'))
            events=runner.events_in(out/f'turn-{n:02}.jsonl')
            assert meta['complete']
            thread=next(e['thread_id'] for e in events if e.get('type')=='thread.started')
            prior=latest.get(thread,{})
            delta={k:meta['usage'].get(k,0)-prior.get(k,0) for k in fields}
            assert all(v>=0 for v in delta.values())
            latest[thread]=meta['usage'];deltas.append({'turn':n,'thread_id':thread,'usage_delta':delta})
            external+=runner.external_commands(events)
            if n==1:first_events=events;first_thread=thread
            if n==11:assert thread!=first_thread
        assert len(latest)==2 and not external
        reads=[e['item'] for e in first_events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
        actual_material=any('materials' in x.get('command','').lower() and any(h in x.get('aggregated_output','').lower() for h in ('# stat 110 (synthetic)','# cs 101 (synthetic)')) for x in reads)
        actual_skill=any('skill.md' in x.get('command','').lower() and "# gpt, i'm cooked" in x.get('aggregated_output','').lower() for x in reads)
        assert actual_material and actual_skill
        gates[label]={'actual_material_text_returned':True,'actual_skill_text_returned':True,'global_skill_accesses':[],'runtime_skill_hashes_unchanged':True}
        raw_totals=[];ledger_paths=[]
        for p in sorted(home.rglob('rollout-*.jsonl')):
            events=[json.loads(l) for l in p.read_text(encoding='utf-8').splitlines()]
            ident=events[0].get('payload',{});thread=ident.get('id',ident.get('session_id'))
            if thread not in latest:continue
            counts=[e for e in events if e.get('type')=='event_msg' and e.get('payload',{}).get('type')=='token_count' and e['payload'].get('info')]
            assert counts
            raw_totals.append(counts[-1]['payload']['info']['total_token_usage'])
            dest=BASE/'usage-ledgers'/label/f'thread-{len(raw_totals):02}.jsonl';dest.parent.mkdir(parents=True,exist_ok=True)
            # Keep token evidence, excluding unrelated account/rate-limit metadata.
            preserved=[{'type':'session_id','thread_id':thread}]+[
                {'type':'event_msg','timestamp':e.get('timestamp'),
                 'payload':{'type':'token_count','info':e['payload']['info']}} for e in counts]
            dest.write_text(''.join(json.dumps(e)+'\n' for e in preserved),encoding='utf-8',newline='')
            ledger_paths.append(dest.relative_to(BASE).as_posix())
        cli={k:sum(v.get(k,0) for v in latest.values()) for k in fields}
        raw={k:sum(v.get(k,0) for v in raw_totals) for k in fields}
        assert len(raw_totals)==2 and cli==raw
        audit[label]={'matches':True,'CLI_usage':cli,'session_ledger_usage':raw,'ledger_files':ledger_paths,'per_turn_deltas':deltas}
        answer=report/'turn7-answers.json';text=json.loads(answer.read_text(encoding='utf-8'))[label[0]]
        start=json.loads((out/'turn-07.meta.json').read_text(encoding='utf-8'))['start_unix']
        assert answer.stat().st_birthtime<=start and (out/'prompt-07.md').read_text(encoding='utf-8')==text
        answers[label]={'created_before_phase2':True,'answer_created_unix':answer.stat().st_birthtime,'turn7_start_unix':start,'prompt_matches_recorded_answer_verbatim':True}
    runner.frozen.dump(BASE/'accounting-audit.json',audit)
    runner.frozen.dump(BASE/'read-isolation-audit.json',gates)
    runner.frozen.dump(BASE/'adaptive-answer-audit.json',answers)
    print('Eight sessions: raw-ledger accounting, fresh resume threads, material/skill reads, isolation, frozen bytes and answer provenance PASS;auth0.')


if __name__=='__main__':
    main()
