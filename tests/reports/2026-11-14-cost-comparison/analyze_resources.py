"""Analyze completed selected T007 sessions only; cumulative CLI counters, not billing."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent


def dump(name, value):
    (BASE/name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--allow-partial',action='store_true')
    args=ap.parse_args()
    index_path=BASE/'executed-evidence-index.json'
    archived=json.loads(index_path.read_text(encoding='utf-8'))['files'] if index_path.exists() else {}
    selected={}
    for batch,packet,rep,order in [(1,'S',1,'CD'),(2,'P',1,'CD'),(3,'S',2,'DC'),(4,'P',2,'DC')]:
        for arm in order:
            label=f'{arm}-{packet}-rep{rep}'
            selected[label]=BASE/f'batch-{batch:02}-{label}'/'runs'/label
    complete={}
    for label,path in selected.items():
        metas=sorted(path.glob('turn-*.meta.json'))
        if len(metas)==11 and all(json.loads(p.read_text(encoding='utf-8'))['complete'] for p in metas):
            complete[label]=path
    if not args.allow_partial:
        assert len(complete)==8,'All eight complete valid sessions required'
    summaries=[];turns=[];mechanics={};snapshots={}
    keys=('input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens')
    for label,path in complete.items():
        arm,packet,rep=label.split('-');previous={k:0 for k in keys};total={k:0 for k in keys}
        commands_total=failed_total=0;wall=0;mechanics[label]=[];snapshots[label]=[];last_hash=None
        for n in range(1,12):
            meta=json.loads((path/f'turn-{n:02}.meta.json').read_text(encoding='utf-8'))
            events=[json.loads(l) for l in (path/f'turn-{n:02}.jsonl').read_text(encoding='utf-8').splitlines()]
            done=[e for e in events if e.get('type')=='turn.completed'];assert len(done)==1
            assert done[0]['usage']==meta['usage'] and not meta['external_skill_commands']
            usage={k:meta['usage'].get(k,0) for k in keys}
            if n==11:previous={k:0 for k in keys}
            delta={k:usage[k]-previous[k] for k in keys};assert all(v>=0 for v in delta.values())
            for k in keys:total[k]+=delta[k]
            previous=usage
            commands=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
            failed=sum(x.get('exit_code')!=0 for x in commands);commands_total+=len(commands);failed_total+=failed;wall+=meta['wall_seconds']
            turns.append({'session':label,'turn':n,**delta,'commands':len(commands),'failed_commands':failed,'active_cli_seconds':meta['wall_seconds']})
            for index,x in enumerate(commands):
                c=x.get('command','')
                if 'record_io.py' in c or re.search(r'(?:write_text|Set-Content|Out-File)',c,re.I):
                    method=re.search(r'record_io\.py[\"\x27]?\s+(save|read|update|commit)\b',c)
                    mechanics[label].append({'turn':n,'command_index':index+1,'commands_in_turn':len(commands),'method':method.group(1) if method else 'manual_or_inline_candidate','exit_code':x.get('exit_code'),'command':c})
            records=list((path/f'files-after-{n:02}').rglob('learning-record.md'));assert len(records)<=1
            raw=records[0].read_bytes() if records else None
            digest=hashlib.sha256(raw).hexdigest() if raw is not None else None
            if records and records[0].relative_to(BASE).as_posix() in archived:
                digest=archived[records[0].relative_to(BASE).as_posix()]['executed_sha256']
            snapshots[label].append({'turn':n,'record_sha256':digest,'changed':digest!=last_hash,'record_file':records[0].relative_to(BASE).as_posix() if records else None})
            last_hash=digest
        ten=json.loads((path/'turn-10.meta.json').read_text(encoding='utf-8'))['usage'];eleven=json.loads((path/'turn-11.meta.json').read_text(encoding='utf-8'))['usage']
        assert all(total[k]==ten.get(k,0)+eleven.get(k,0) for k in keys)
        summaries.append({'session':label,'arm':arm,**total,'total_tokens':total['input_tokens']+total['output_tokens'],'uncached_input_tokens':total['input_tokens']-total['cached_input_tokens'],'commands':commands_total,'failed_commands':failed_total,'active_cli_seconds':round(wall,2)})
    for name,rows in [('resources.csv',summaries),('per-turn-deltas.csv',turns)]:
        if rows:
            with (BASE/name).open('w',encoding='utf-8',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    dump('save-mechanics.json',mechanics)
    dump('record-byte-audit.json',{'note':'Readiness/status-change/stale-resume semantics require blinded review; hashes alone do not establish them.','sessions':snapshots})
    dump('selected-completion.json',{'completed_sessions':len(complete),'student_calls':11*len(complete),'partial_mode':args.allow_partial,'selected':{k:p.relative_to(BASE).as_posix() for k,p in complete.items()},'note':'Probe/smoke excluded. Cached input is subset of input, reasoning subset of output; do not add twice.'})
    print(f'{len(complete)} completed selected sessions analyzed; cumulative accounting checks pass.')


if __name__=='__main__':
    main()
