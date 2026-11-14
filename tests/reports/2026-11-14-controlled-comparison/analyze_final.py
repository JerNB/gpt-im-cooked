from pathlib import Path
import json, hashlib, re, random, shutil, sys
base=Path(__file__).parent
report=base/'final'
report.mkdir(exist_ok=True)
for packet,source in [('p',base/'isolated/fixtures/packet-p'),('s',base/'frozen-packet-s-git')]:
 shutil.copytree(source,report/'fixtures'/f'packet-{packet}',dirs_exist_ok=True)
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def masked(text):
 text=re.sub(r'\*{0,2}Hi student, let.s get you uncooked\.\*{0,2}', '',text,flags=re.I)
 text=re.sub(r'(?:skill/)?(?:SKILL\.md|references/(?:state|concept-tutoring|practice-and-feedback)\.md)','[workflow reference]',text)
 return text.replace('GPT, I’m Cooked','[workflow]').replace("GPT, I'm Cooked",'[workflow]')
sessions=sorted((base/'isolated/runs').iterdir())
sessions=[base/'exact-S/runs'/s.name if '-S-' in s.name else s for s in sessions]
sessions=[base/'exact-recovery-A1-S-rep2-preflight/runs'/s.name if s.name=='A1-S-rep2' else s for s in sessions]
sessions=[(base/('recovery-'+s.name)/'runs'/s.name) if any(not json.loads(p.read_text(encoding='utf-8'))['complete'] for p in s.glob('*.meta.json')) else s for s in sessions]
assert len(sessions)==16
if '--allow-partial' not in sys.argv:
 assert all(len(list(s.glob('turn-*.meta.json')))==11 for s in sessions),'All 176 calls must finish first'
order=list(sessions);random.Random(461030).shuffle(order)
mapping={f'CASE-{i+1:02}':s.name for i,s in enumerate(order)}
dump(report/'blind-map.json',mapping)
dump(report/'selected-sessions.json',{s.name:s.relative_to(base).as_posix() for s in sessions})
auto={};audit={}
for case,s in zip(mapping,order):
 if '--allow-partial' in sys.argv and (len(list(s.glob('turn-*.meta.json')))!=11 or any(not json.loads(p.read_text(encoding='utf-8'))['complete'] for p in s.glob('turn-*.meta.json'))):continue
 arm,packet,rep=s.name.split('-'); repn=int(rep[3:])
 fixture=report/'fixtures'/f'packet-{packet.lower()}'
 replies={str(t):(s/f'response-{t:02}.md').read_text(encoding='utf-8') for t in range(1,12)}
 metas=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(s.glob('turn-*.meta.json'))]
 assert all(m['complete'] and not m['external_skill_commands'] for m in metas)
 rubric=json.loads((fixture/'rubric-v2.json').read_text(encoding='utf-8'))
 snapshots={}
 for t in range(1,12):
  snap=s/f'files-after-{t:02}'
  snapshots[str(t)]={p.relative_to(snap).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text(encoding='utf-8',errors='replace')} for p in snap.rglob('*.md')}
 status=[];previous={}
 for t in range(1,12):
  candidates=re.findall(r'.{0,100}(?:Needs practice|Improving|Demonstrated|Recheck).{0,160}',replies[str(t)],re.I)
  changed=[f for f,x in snapshots[str(t)].items() if previous.get(f)!=x['sha256']]
  if candidates:status.append({'turn':t,'phrases':candidates,'changed_files':changed})
  previous={f:x['sha256'] for f,x in snapshots[str(t)].items()}
 marker={t:len(re.findall("Hi student, let's get you uncooked",r,re.I)) for t,r in replies.items()}
 locators={t:re.findall(r'§+\s*\d+(?:\.\d+)?',r) for t,r in replies.items()}
 keys=rubric['ground_truth'].get('key_values',rubric['ground_truth'].get('unattempted_key_values',{}))
 leaks=[]
 for q,values in keys.items():
  first=rubric['ground_truth']['first_attempt_turn'].get(q) or rubric['ground_truth'].get('answer_requested_turn',{}).get(q)
  if first:
   for t in range(1,first):
    for value in values:
     if value in replies[str(t)]:leaks.append({'item':q,'turn':t,'matched':value})
 auto[s.name]={'M1_candidates':leaks,'M3_review_required':'Confirm course format for each own answer; absence of an answer is not a failure.',
  'M5_locators':locators,'M8_ground_truth':rubric['ground_truth'].get('in_scope_unassessed_at_turn_10',rubric['ground_truth'].get('unassessed_at_turn_10')),
  'M11_candidates':status,'M13_candidates':[{'turn':t,'text':r} for t,r in replies.items() if re.search(r'Demonstrated',r,re.I)],
  'M15_marker_counts':marker,'M15_repeated_reply_count':sum(n>1 for n in marker.values())}
 # Session accounting is separate from the blind packet.
 workname=(s.parent.parent.name if s.parent.parent.name.startswith(('recovery-','exact-recovery-')) else (f'exact-S-rep{repn}' if packet=='S' else f'isolated-{packet}-rep{repn}'))
 home=Path.home()/f'.codex/runs/t004/{workname}/home-{s.name}'
 used_threads=set()
 for m in metas:
  for line in (s/f'turn-{m["turn"]:02}.jsonl').read_text(encoding='utf-8').splitlines():
   event=json.loads(line)
   if event.get('type')=='thread.started':used_threads.add(event['thread_id'])
 session_totals=[]
 for path in home.rglob('rollout-*.jsonl'):
  lines=path.read_text(encoding='utf-8').splitlines()
  metadata=json.loads(lines[0]).get('payload',{})
  if metadata.get('id',metadata.get('session_id')) not in used_threads:continue
  latest=None
  for line in path.read_text(encoding='utf-8').splitlines():
   event=json.loads(line);pay=event.get('payload',{})
   if event.get('type')=='event_msg' and pay.get('type')=='token_count' and pay.get('info'):
    latest=pay['info']['total_token_usage']
  if latest:session_totals.append(latest)
 fields=['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens']
 naive_sum={k:sum(m['usage'].get(k,0) for m in metas) for k in fields}
 latest={};deltas=[]
 for m in metas:
  ev=[json.loads(line) for line in (s/f'turn-{m["turn"]:02}.jsonl').read_text(encoding='utf-8').splitlines()]
  thread=next(e['thread_id'] for e in ev if e.get('type')=='thread.started')
  old=latest.get(thread,{})
  delta={k:m['usage'].get(k,0)-old.get(k,0) for k in fields}
  assert all(v>=0 for v in delta.values()), 'Cumulative usage decreased unexpectedly'
  deltas.append({'turn':m['turn'],'thread_id':thread,'usage_delta':delta})
  latest[thread]=m['usage']
 cli_sum={k:sum(v.get(k,0) for v in latest.values()) for k in fields}
 raw_sum={k:sum(x.get(k,0) for x in session_totals) for k in cli_sum}
 audit[s.name]={'session_count':len(session_totals),'cli_usage_sum':cli_sum,'session_usage_sum':raw_sum,
 'matches':cli_sum==raw_sum,'naive_sum_do_not_use':naive_sum,'per_call_deltas':deltas,'wall_seconds':sum(m['wall_seconds'] for m in metas),'start_unix':min(m['start_unix'] for m in metas)}
 packet_data={'case':case,'packet':packet,'rubric':rubric,
  'materials':{p.name:p.read_text(encoding='utf-8') for p in (fixture/'materials').iterdir() if p.is_file()},
  'responses':{t:masked(r) for t,r in replies.items()},
  'student_turn7':(s/'prompt-07.md').read_text(encoding='utf-8'),
  'progress_snapshots':{t:{f:masked(x['text']) for f,x in files.items() if Path(f).name in ('learning-record.md','study-progress.md','progress.md')} for t,files in snapshots.items() if t in ('7','10','11')}}
 dump(report/'blind'/f'{case}.json',packet_data)
dump(report/'scores-auto.json',{'note':'Automated candidates require human/semantic confirmation; not all pattern matches are failures.','sessions':auto})
dump(report/'accounting-audit.json',audit)
print('Prepared',len(auto),'complete shuffled blind packets; partial mode=', '--allow-partial' in sys.argv)
