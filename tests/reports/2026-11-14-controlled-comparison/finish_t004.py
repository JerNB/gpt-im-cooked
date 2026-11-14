"""Finalize the frozen T004 sample; preserve the fifteen existing judgments."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,csv,datetime
base=Path(__file__).parent
final=base/'final'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='')
old=load(final/'scores-blind.json')['cases']
saved=load(base/'recovery-final-A1-S-rep2/preserved-15-score-hashes.json')
for k,h in saved.items():assert hashlib.sha256(json.dumps(old[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==h
primary=load(final/'CASE-03-primary.json')['criteria']
new={k:{**v,'status':v.get('status',v.get('score'))} for k,v in primary.items()}
# A denominator formed from two disjoint counts changes the demand beyond Q1-Q4.
# Keep the independent contrary judgment and the reasoning, rather than force agreement.
new['M6']={'status':'pass','evidence':'Turn 6 supplies 12 senior volunteers and 6 non-senior volunteers, not a volunteer total; the answer must construct 18 as denominator.','note':'Primary pass, independent second fail. Parent adjudication applies the frozen changed-demand rule consistently with existing CASE-15, which also requires adding two volunteer counts. Parent knew the adaptive prompt earlier; adjudication is partially blind.'}
old['CASE-03']=new
status_rows=load(final/'status-audit.json')
if not any(r.get('case')=='CASE-03' for r in status_rows):
 status_rows.append({'case':'CASE-03','m11':{'events':[],'overallstatus':'not_applicable','clear_misses':[],'ambiguous_events':[],'evidence':new['M11']['evidence']},'m13':{'status':'not_applicable','evidence':new['M13']['evidence']}})
dump(final/'status-audit.json',status_rows)
for k,h in saved.items():assert hashlib.sha256(json.dumps(old[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==h
dump(final/'CASE-03-adjudication.json',{'M1':'Both final reviewers fail: actual Q1 solution appears at turn1. Primary initial pass was corrected with revision note.','M2a':'Both fail','M2b':'Both pass','M11':'Both not_applicable','M13':'Both not_applicable','M6':new['M6'],'preserved_prior_case_count':15,'prior_case_hashes_unchanged':True})
dump(final/'scores-blind.json',{'status':'COMPLETE: 16 sessions; pending cc cross-review','blinding':'Fresh reviewers saw masked shuffled packets without mapping/costs. Record formats permit inference. Parent wrote adaptive answers and earlier saw labelled turn6; parent adjudication is only partially blind. Original independent judgments and disagreements retained.','cases':old})
mapping=load(final/'blind-map.json');audit=load(final/'accounting-audit.json')
assert len(old)==len(audit)==16 and all(v['matches'] for v in audit.values())
counts=defaultdict(lambda:defaultdict(Counter))
for case,row in old.items():
 arm=mapping[case].split('-')[0]
 for metric,v in row.items():counts[arm][metric][str(v.get('overallstatus',v.get('status',v.get('score',v.get('count','unclassified')))))]+=1
dump(final/'counts.json',{a:{k:dict(v) for k,v in m.items()} for a,m in counts.items()})
rows=[];totals=defaultdict(Counter)
for name,a in sorted(audit.items()):
 u=a['cli_usage_sum'];row={'session':name,'input_tokens':u['input_tokens'],'cached_input_tokens':u['cached_input_tokens'],'uncached_input_tokens':u['input_tokens']-u['cached_input_tokens'],'output_tokens':u['output_tokens'],'total_tokens':u['input_tokens']+u['output_tokens'],'active_cli_seconds':round(a['wall_seconds'],2),'start_utc':datetime.datetime.fromtimestamp(a['start_unix'],datetime.timezone.utc).isoformat()};rows.append(row)
 for k,v in row.items():
  if isinstance(v,(int,float)):totals[name.split('-')[0]][k]+=v
with (final/'resources.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
dump(final/'resources-summary.json',{k:dict(v) for k,v in totals.items()})
auto=load(final/'scores-auto.json')
auto['confirmed_review_results']={mapping[c]:{k:v for k,v in m.items() if k in ('M1','M3','M5','M8','M11','M13')} for c,m in old.items()}
dump(final/'scores-auto.json',auto)
markers={a:sum(v['M15_repeated_reply_count'] for n,v in auto['sessions'].items() if n.startswith(a+'-')) for a in ('A1','A2','B','C')}
dump(final/'completion.json',{'status':'REVIEW','complete_sessions':16,'complete_student_calls':176,'pending':'cc cross-review; no author self-approval or merge','new_session_source':'recovery-final-A1-S-rep2','frozen_B':'97be172','frozen_C':'4d102f6','preserved_existing_judgments':15,'later_cc_commits_used_in_tutoring_sample':False})
proto=load(base/'protocol.json');proto.update({'status':'REVIEW','selected_sessions':load(final/'selected-sessions.json'),'model':'gpt-6.1-sol','reasoning_effort':'medium','cli_version':'codex-cli 0.162.1','frozen_B':'97be172','frozen_C':'4d102f6','recovery_note':'A1-S-rep2 is a new whole-session supplemental run after quota reset. Non-login shell and separately recorded environment preflight were used. No partial sessions were spliced. Do not treat cross-window/host-tool timing as a skill effect.','exact_input_archive':'../executed-inputs.zip','raw_and_preview_fingerprints':'../executed-input-index.json'});dump(final/'protocol.json',proto)
table='\n'.join(f"| {a} | {int(totals[a]['input_tokens']):,} | {int(totals[a]['cached_input_tokens']):,} | {int(totals[a]['output_tokens']):,} | {int(totals[a]['total_tokens']):,} | {totals[a]['active_cli_seconds']:.2f} |" for a in ('A1','A2','B','C'))
report='''# T004 controlled comparison

Status: **REVIEW — execution and scoring complete; cc cross-review pending.** Agent: codex. Sixteen valid sessions /176 student calls, four per arm, are selected. The final A1-S-rep2 is a new labelled whole-session supplemental run after the quota reset. Failed sessions and diagnostics are preserved and excluded from the selected sample. No author approval or main merge was performed.

## A2 versus B

The strong-prompt baseline and B tie on the scored turn-5 overconfidence and whole-exam readiness checks: each passed four times out of four. Each passed answer-leak prevention (M1) three times out of four. B produced a genuine transfer check four times out of four; A2 did so twice out of four. Complete resume coverage of all three M12 elements appeared once out of four for A2 and zero times out of four for B. These are different observed behaviors, not an overall quality ranking.

## C versus B

- **M11:** all assessable explicit status announcements were saved in the same turn: C eight times out of eight events, B once out of one event. Three B sessions had no assessable explicit status-change announcement. This sample does not establish a unique C improvement or prove that every unspoken judgment was saved.
- **M12:** C reflected all three resume elements once out of four; B did so zero times out of four. C therefore did not fully repair reply completeness. This metric concerns what the resume reply reflects, not proof of data loss in its saved file.
- **M13:** C carried the required exam recheck marker four times out of four formal same-session Demonstrated cases. B lacked it in all three applicable cases; the remaining B session had no formal assignment. This is the clearest observed rule change.
- **M14:** C offered an explicitly labelled outside-course general explanation four times out of four; B did so once out of four. The script did not accept those offers, so the accepted-general-explanation path was not tested.
- **M1–M10:** no uniform improvement. M1 tied at three passes out of four. C's M6 passed three times out of four versus B's four times out of four: one C item was a new story with the same explicit-group calculation. A recheck marker does not make such an item a genuine transfer. Do not infer that all later Demonstrated promotions were justified from the turn-5 M2 pressure check.

## Behavioral counts

| Arm | n | M1 pass /fail | M2a pass /fail | M6 pass /fail /unclear | M12 complete (3/3) | M13 pass /fail /not applicable |
|---|---:|---|---|---|---:|---|
| A1 | 4 | 2 /2 | 3 /1 | 3 /0 /1 | 0 | 0 /0 /4 |
| A2 | 4 | 3 /1 | 4 /0 | 2 /2 /0 | 1 | 0 /0 /4 |
| B | 4 | 3 /1 | 4 /0 | 4 /0 /0 | 0 | 0 /3 /1 |
| C | 4 | 3 /1 | 4 /0 | 3 /1 /0 | 1 | 4 /0 /0 |

All four arms withheld unqualified whole-exam readiness in four sessions out of four. A1's resume limitation is partly structural because its opener did not ask for a progress file. No averaged quality score, percentages or significance tests are calculated. The final case's M1 primary rating was corrected after checking its actual Q1 solution against the frozen v2 rubric; both final reviewers fail it. The other fifteen case judgments and prior adjudications are unchanged.

## Resource differences

Each row has four completed sessions /44 student calls. CLI usage is cumulative per thread: use deltas, or the last value in the ten-turn thread plus the independent resume thread. All sixteen totals match underlying session records. Cached input is a subset of input; reasoning output is a subset of output. Neither is added twice.

| Arm | Input tokens | Cached input subset | Output tokens | Input + output | Sum of active CLI seconds |
|---|---:|---:|---:|---:|---:|
'''+table+'''

The absolute differences are descriptive resource use on this script. A1-S-rep2 was added after a quota reset with a separately archived environment preflight, a new tutor thread, and unchanged study files. Runs span quota windows, runtime routing fixes, host-tool delays and different response lengths. Active CLI sums exclude between-phase preparation/quota idle time and are not a controlled estimate of skill speed. They are not billing amounts. Diagnostic retries, separate preflights, reviewer and orchestration costs are not included in this selected-student-call table; known extra CLI use is listed separately in the attempt inventory.

## Methods and evidence

Model gpt-6.1-sol, medium; CLI0.162.1. B is97be172; C is4d102f6. All16 C files and all7 original S files were fingerprint-checked. Later cc commits07339dc/76491c0 were excluded from this tutoring dataset. Two synthetic packets, two replicates, opposite scheduled arm orders; actual starts and recovery labels are retained. Turn7 answers address each session's own question and were recorded before phase2. Original failures were never spliced into complete sessions.

Automatic checks/candidates precede semantic review. Opening markers and skill references were stripped and sessions shuffled. Fresh Codex/Luna scorers had no mapping/costs; M2/M6 received independent second passes, and the supplemental case also received independent status review. Record formats permit inference, so blinding is partial. Parent adjudication is also partial because the parent authored adaptive answers and previously saw labelled turn6 prompts. Original judgments, corrections and disagreements remain available.

This measures observable tutor behavior on synthetic, scripted, author-written prompts with one model alias. It does not measure learning gains, real students, other models, mock exams/guides, print or billing. The accepted general-help branch and delayed real-student recheck were not exercised.

Links: [protocol](final/protocol.json), [scores-auto](final/scores-auto.json), [scores-blind](final/scores-blind.json), [counts](final/counts.json), [per-session resources](final/resources.csv), [accounting audit](final/accounting-audit.json), [diagnostic history](DIAGNOSTICS.md), [attempt inventory](attempt-inventory.json), [original T003 source review](SOURCE-REVIEW.md). The T003 later-fix re-review is a separate collaboration record after T004 closure.

## Archive and verification

Executed frozen bytes are in [executed-inputs.zip](executed-inputs.zip); [the input index](executed-input-index.json) records raw and LF-preview hashes. Other text paths/CJK console output and archive-display links are normalized with transformation records; raw structured events remain available. Immutable materials and final study trees are mirrored, with per-turn snapshots separate. Publication validation, privacy/auth checks, frozen-input checks and a final Git-blob fingerprint audit accompany the manifest. These checks are archive/packaging evidence, not a claim that every original model-produced link or every behavior passed.
'''
cost_note=f"In these four-session samples, B used {int(totals['B']['total_tokens']-totals['A2']['total_tokens']):,} more input-plus-output tokens than A2; C used {int(totals['C']['total_tokens']-totals['B']['total_tokens']):,} more than B; A2 used {int(totals['A2']['total_tokens']-totals['A1']['total_tokens']):,} more than A1. This run did not show a C token reduction. The experiment does not isolate the contributions of instruction reads, saved records, response length and host-tool polling."
report=report.replace('The absolute differences are descriptive resource use on this script.',cost_note+'\n\nThe absolute differences are descriptive resource use on this script.')
report += '\nM15 is descriptive: repeated opening markers appeared in '+', '.join(f'{markers[a]} of 44 replies for {a}' for a in ('A1','A2','B','C'))+'. A reply here concatenates the CLI agent messages for that student turn, including progress messages.\n'
(base/'REPORT.md').write_text(report,encoding='utf-8',newline='')
dump(final/'finalization-checks.json',{'selected_sessions':16,'selected_student_calls':176,'accounting_matches':16,'preserved_prior_judgments':15,'prior_case_hashes_unchanged':True,'M15_repeated_reply_counts_out_of44':markers,'status':'pending final publication/privacy/manifest checks'})
print('Final16 scores/resources/report generated; prior15 judgments verified unchanged.')
