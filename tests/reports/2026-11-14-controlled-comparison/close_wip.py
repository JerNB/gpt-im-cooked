from pathlib import Path
from collections import Counter, defaultdict
import json, hashlib, re, csv, os, shutil, subprocess
base=Path(__file__).parent
final=base/'final'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='')
def cases(p):
 x=read(p)['cases']
 return x if isinstance(x,list) else [{'case':k,'criteria':v} for k,v in x.items()]
scores={}
for name in ('blind-primary-1.json','blind-primary-2.json'):
 for c in cases(next((base/'isolated').rglob(name))):
  key=c.get('case',c.get('case_id'))
  if read(base/'isolated/blind'/f'{key}.json')['packet']=='P':scores[key]=c.get('criteria',c.get('scores'))
for c in cases(next(final.rglob('S-primary.json'))):scores[c['case']]=c['scores']
for name in ('P-blind-adjudication.json','S-blind-adjudication.json'):
 for key,value in read(base/name)['M6_disagreements'].items():scores[key]['M6']=value
status=read(final/'status-audit.json')
if isinstance(status,dict):status=status['cases']
for c in status:
 key=c.get('case',c.get('case_id'))
 scores[key]['M11']=c['m11'];scores[key]['M13']=c['m13']
assert len(scores)==15
dump(final/'scores-blind.json',{'status':'PARTIAL: 15 complete sessions; CASE-03 missing','blinding':'Fresh Codex/Luna scorers saw anonymized packets only. Record formats permit inference. Parent wrote adaptive answers and saw labelled turn-6 prompts; adjudication is only partially blind.','cases':scores})
mapping=read(final/'blind-map.json');audit=read(final/'accounting-audit.json')
assert len(audit)==15 and all(x['matches'] for x in audit.values())
rows=[]
for name,a in sorted(audit.items()):
 u=a['cli_usage_sum'];rows.append({'session':name,'input_tokens':u['input_tokens'],'cached_input_tokens':u['cached_input_tokens'],'uncached_input_tokens':u['input_tokens']-u['cached_input_tokens'],'output_tokens':u['output_tokens'],'total_tokens':u['input_tokens']+u['output_tokens'],'active_cli_seconds':round(a['wall_seconds'],2)})
with (final/'resources.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
counts=defaultdict(lambda:defaultdict(Counter))
for case,criteria in scores.items():
 arm=mapping[case].split('-')[0]
 for metric,v in criteria.items():
  val=v.get('overallstatus',v.get('status',v.get('result',str(v.get('count','unclassified')))))
  counts[arm][metric][str(val)]+=1
dump(final/'counts-partial.json',{a:{k:dict(v) for k,v in m.items()} for a,m in counts.items()})
dump(final/'completion.json',{'status':'BLOCKED','complete_sessions':15,'target_sessions':16,'complete_selected_calls':165,'missing':'A1-S-rep2','latest_failed_attempt':'exact-recovery-A1-S-rep2-preflight, turn 8, quota failure after 7 completed turns','service_message':'Try again at 3:35 PM (2026-11-14; client America/New_York)','next_step':'After quota reset, rerun A1-S-rep2 from turn 1 under a new label. Never continue failed turn 8. Then replace final selection, regenerate all final scores/counts/accounting/manifest, review, commit and draft PR.'})
report='''# T004 controlled comparison — WIP

Status: **BLOCKED, not complete**. Agent: codex. Fifteen valid complete sessions (165 student calls) are retained; the target is sixteen sessions / 176 calls. A1-S-rep2 failed again at turn 8 because the service usage limit was reached. The service says to retry after 3:35 PM on November 14. Its seven completed calls are diagnostic only, not a complete selected session. A later run must start from turn 1 in a new labelled session.

## Source review

Claude's four skill-file edits implement save-on-status/readiness, same-session exam recheck markers, and a labelled optional general explanation for source gaps. Nine existing checks pass on the pushed T003 archive. Distribution verification fails on both T003 and baseline, matching the pre-existing release-archive mismatch. [Source review](SOURCE-REVIEW.md) requests changes to the cc-owned pilot harness for global-skill isolation, credential lifecycle, report binding and sanitization. No skill or release ZIP was edited here. No merge or approval was performed.

## Available evidence

- [Partial blinded scores](final/scores-blind.json), [partial counts](final/counts-partial.json), and [automatic candidates](final/scores-auto.json).
- [Per-session resources](final/resources.csv) and [session-accounting audit](final/accounting-audit.json). CLI usage is cumulative per thread; use deltas or the last value per thread, then add the independent resume thread. All 15 selected accounting totals match the underlying session records. Cached tokens are a subset of input; reasoning tokens are a subset of output. Neither is added twice.
- [Attempt history](DIAGNOSTICS.md), [completion/next step](final/completion.json), and separate raw report directories retain invalid, quota-failed and corrected runs.
- Frozen model: gpt-6.1-sol, medium; CLI 0.162.1. B: 97be172; C: 4d102f6, with all 16 skill fingerprints checked. The corrected S packet's seven original files match Git and supplied pilot fingerprints byte for byte. P was authored before its first call and retained under per-run fixture fingerprints.

## Interpretation limits

There are four completed sessions each for A2, B and C, but only three for A1. No percentages, significance tests or final sixteen-session conclusion are supplied. M2/M6 received independent blinded second passes; disagreements and partially blind parent adjudications are retained. C's additional recheck marker does not by itself prove that a generated question is a real transfer task; inspect M6 and the original question. Explicit status-announcement checks do not measure every unspoken change in judgment.

This is a synthetic, scripted, one-model study, not learning gains or real-student outcomes. Mock exams, guides, print and billing are not measured. Runs span quota windows, runtime routing fixes and host-tool delays. One A1 recovery used a separately archived fixed-file environment preflight, followed by a new tutor thread with unchanged study files; it still later failed quota and is excluded. Do not pool latency as a skill-only effect. Diagnostic/model-review/orchestration costs are not equivalent to the selected tutoring-call resource table.

## Archive handling

Known fixed source/skill copies retain their original bytes. Other text is sanitized for user/work paths, runtime drive prefixes and mis-decoded CJK output; changed-file pre/post hashes are recorded. Final study trees and immutable material files are mirrored where available. Per-turn snapshots remain separate from final state. A SHA-256 manifest covers this WIP archive; it is not an assertion that the experiment is done.
'''
(base/'REPORT.md').write_text(report,encoding='utf-8',newline='')
# Mirror actual synthetic study trees; credentials live in sibling homes and are never copied.
roots=[base]+[p for p in base.iterdir() if p.is_dir() and (p/'runs').is_dir()]
for reportroot in roots:
 runs=reportroot/'runs'
 if not runs.is_dir():continue
 for out in runs.iterdir():
  if not out.is_dir() or not re.fullmatch(r'(A1|A2|B|C)-(S|P)-rep[12]',out.name):continue
  arm,packet,rep=out.name.split('-')
  label=reportroot.name
  workname=(f'{packet}-{rep}' if reportroot==base else f'{label}-{packet}-{rep}' if label in ('restart','isolated') else f'exact-S-{rep}' if label=='exact-S' else label)
  work=Path.home()/'.codex/runs/t004'/workname/f'run-{out.name}'
  if not work.is_dir():continue
  for p in work.rglob('*'):
   rel=p.relative_to(work)
   if not p.is_file() or any(x in ('skill','__pycache__') for x in rel.parts) or rel.name=='AGENTS.md':continue
   for dest in (out/rel,out/'final-files'/rel):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():shutil.copy2(p,dest)
  for snap in out.glob('files-after-*'):
   if (work/'materials').is_dir() and not (snap/'materials').exists():shutil.copytree(work/'materials',snap/'materials')
# Privacy transformation; frozen inputs are excluded so their fingerprints stay exact.
variants=set()
taskbase=Path.home()/'.codex/runs/t004'
for root in [Path.home()]+[p for p in taskbase.iterdir() if p.is_dir()]:
 value=str(root)
 variants.add(value.replace('\\','/'))
 for n in (1,2,4,8):variants.add(value.replace('\\','\\'*n))
changes=[]
for p in sorted(base.rglob('*')):
 if not p.is_file() or p.suffix not in ('.md','.json','.jsonl','.txt','.py','.csv','.bak'):continue
 rel=p.relative_to(base)
 if any(x in ('fixtures','skill-B','skill-C','frozen-packet-s-git') for x in rel.parts):continue
 old=p.read_bytes()
 try:text=old.decode('utf-8-sig')
 except UnicodeDecodeError:continue
 for value in sorted(variants,key=len,reverse=True):text=text.replace(value,'<ROOT>')
 for n in (1,2,4,8):text=text.replace('C:'+('\\'*n)+'Program Files','<ROOT>')
 text=text.replace('<ROOT>','<ROOT>')
 text=re.sub('['+chr(0x3400)+'-'+chr(0x9fff)+']',chr(0xfffd),text)
 new=text.replace('\r\n','\n').encode('utf-8')
 if new!=old:
  p.write_bytes(new);changes.append({'path':rel.as_posix(),'original_sha256':hashlib.sha256(old).hexdigest(),'archived_sha256':hashlib.sha256(new).hexdigest()})
dump(base/'sanitization.json',{'policy':'Frozen input/skill bytes preserved; other text paths/CJK output normalized. Original byte fingerprints retained for transformed files.','changes':changes})
manifest={p.relative_to(base).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(base.rglob('*')) if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
dump(base/'manifest.json',manifest)
print('WIP archive:',len(manifest),'files; 15 complete sessions; quota BLOCKED.')
