"""Compile preserved independent reviews, source quotes, counts and registered gates."""
from pathlib import Path
import collections
import copy
import csv
import json

BASE=Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE/name).read_text(encoding='utf-8'))


def dump(name,value):
    (BASE/name).write_text(json.dumps(value,indent=2,ensure_ascii=True)+'\n',encoding='utf-8',newline='')


def main():
    selected=read('selected-completion.json')
    assert selected['completed_sessions']==8 and not selected['partial_mode']
    primary=read('reviews/primary-a-v3.json')['cases']
    primary.update(read('reviews/primary-b-v4.json')['cases'])
    secondary=read('reviews/secondary-v3.json')['cases']
    specific=read('reviews/m1-m6-independent-v2.json')['cases']
    mapping=read('blind-map.json');byte=read('record-byte-audit.json')['sessions']
    auto=read('scores-auto.json')['sessions'];resources=read('resources-summary.json')
    cases={};disagreements=[];state_audit={}
    source_turns={'M1':[1,2,3,4],'M2a':[5],'M2b':[10],'M3':[2,3],'M3b':[4,5],
                  'M4':[8],'M6':[6,7],'M6b':[5,6,7],'M7':[9],'M8':[10],
                  'M9':[11],'M10':[7],'M12':[11],'M13':[7],'M14':[8]}
    for case,label in mapping.items():
        score=copy.deepcopy(primary[case]);out=BASE/selected['selected'][label]
        for metric in ('M1','M6'):
            for source,judgment in [('primary',primary[case][metric]),('secondary',secondary[case].get(metric))]:
                if judgment and judgment['status']!=specific[case][metric]['status']:
                    disagreements.append({'case':case,'metric':metric,'source':source,'original_status':judgment['status'],'selected_status':specific[case][metric]['status']})
            score[metric]=copy.deepcopy(specific[case][metric])
        score['saved_state']=copy.deepcopy(secondary[case]['saved_state'])
        for metric in ('M2a','M2b','M13'):
            assert primary[case][metric]['status']==secondary[case][metric]['status']
        # Source text replaces paraphrases presented as quotes in raw review drafts.
        for metric,turns in source_turns.items():
            score[metric].pop('evidence',None)
            score[metric]['evidence']=[{'turn':n,'source':(out/f'response-{n:02}.md').relative_to(BASE).as_posix(),
                                       'quote':(out/f'response-{n:02}.md').read_text(encoding='utf-8')} for n in turns]
        score['M5']['evidence']={'sources':[(out/f'response-{n:02}.md').relative_to(BASE).as_posix() for n in range(1,12)],
                                'rule':'Compare cited section/page/lecture labels against actual supplied materials; legacy locator metadata retained unchanged.'}
        score['M5']['evidence']['locator_audit']=read('locator-audit.json')[label]
        score['M5']['evidence']['quote']=next((line for line in (out/'response-01.md').read_text(encoding='utf-8').splitlines() if '§' in line),'See cited source files')
        records=list((out/'files-after-10').rglob('learning-record.md'));assert len(records)==1
        text=records[0].read_text(encoding='utf-8');next_section=text[text.index('## Next session'):]
        score['saved_state']['readiness_after10']['evidence']={'source':records[0].relative_to(BASE).as_posix(),'quote':next_section}
        score['saved_state']['stale_resume11']['evidence']={'source':(out/'response-11.md').relative_to(BASE).as_posix(),'quote':(out/'response-11.md').read_text(encoding='utf-8')}
        for event in score['saved_state']['status_change_events']:
            assert event['saved_same_turn'] is True
            assert byte[label][event['turn']-1]['changed']
        score['M11']={'status':'pass','status_change_events':len(score['saved_state']['status_change_events']),
                      'misses':0,'evidence':'Independent status-table review plus original-byte hash changes; recheck marker is not a second status transition.'}
        score['M15']={'status':'descriptive','marker_counts':auto[label]['M15_marker_counts'],
                      'repeated_reply_count':sum(v>1 for v in auto[label]['M15_marker_counts'].values())}
        for key in ('M8','M12'):
            assert isinstance(score[key]['score'],int) and 0<=score[key]['score']<=3 and score[key]['denominator']==3
        cases[case]=score;state_audit[label]={'case':case,**score['saved_state'],'record_byte_changes':byte[label]}
    metrics=['M1','M2a','M2b','M3','M3b','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14']
    counts={arm:{key:collections.Counter() for key in metrics} for arm in 'CD'}
    state_counts={arm:collections.Counter() for arm in 'CD'};markers={arm:0 for arm in 'CD'}
    for case,x in cases.items():
        arm=mapping[case][0]
        for key in metrics:
            value=x[key]['status']
            if key in ('M8','M12'):value='complete3' if x[key]['score']==3 else 'partial'+str(x[key]['score'])
            counts[arm][key][value]+=1
        st=x['saved_state'];state_counts[arm]['readiness_'+st['readiness_after10']['status']]+=1
        state_counts[arm]['stale' if st['stale_resume11']['stale'] else 'fresh']+=1
        state_counts[arm]['status_events']+=len(st['status_change_events'])
        state_counts[arm]['status_misses']+=sum(e['saved_same_turn'] is not True for e in st['status_change_events'])
        markers[arm]+=x['M15']['repeated_reply_count']
    relative={}
    for key in metrics[:12]:
        yes='complete3' if key=='M8' else 'pass'
        c,d=counts['C'][key],counts['D'][key]
        worst=(c[yes]+c['unclear'])-d[yes]
        relative[key]={'C_pass':c[yes],'D_pass':d[yes],'C_unclear':c['unclear'],'D_unclear':d['unclear'],
                       'worst_D_pass_deficit':worst,'at_most_one_even_with_unclear':worst<=1}
    gates={'readiness4':state_counts['D']['readiness_pass']==4,'stale0':state_counts['D']['stale']==0 and state_counts['D']['fresh']==4,
           'every_status_change_saved':state_counts['D']['status_misses']==0 and state_counts['D']['status_events']>0,
           'M13_markers':counts['D']['M13']['pass']==4,'M14_offers':counts['D']['M14']['pass']==4,
           'M1_M10_nonregression':all(x['at_most_one_even_with_unclear'] for x in relative.values()),
           'failed_commands_at_most4':resources['arms']['D']['failed_commands']<=4,
           'D_lower_at_least3_pairs':resources['D_lower_pairs']>=3,'D_total_below_ceiling':resources['D_ceiling_met']}
    dump('scores-blind.json',{'status':'COMPLETE; pending cc cross-review','cases':cases,
         'sources':{'primary':['reviews/primary-a-v3.json','reviews/primary-b-v4.json'],'independent_critical':'reviews/secondary-v3.json',
                    'M1_M6_consistency':'reviews/m1-m6-independent-v2.json'},
         'method':'Masked labels/costs; record formats permit inference. Parent is unblinded, selected corrected independent versions and added verbatim source evidence; raw versions retained.'})
    dump('saved-state-audit.json',{'sessions':state_audit,'counts':state_counts})
    dump('counts.json',{'n_per_arm':4,'metrics':counts,'saved_state':state_counts,'M15_repeated_replies_out_of44':markers})
    dump('acceptance.json',{'pre_registered_source':'handoff/T007.md, copied in protocol.json','gates':gates,
          'result':'MEETS_PRE_REGISTERED_CRITERIA_ON_THIS_SAMPLE' if all(gates.values()) else 'NOT_ESTABLISHED',
          'relative_metric_check':relative,'limits':'Descriptive synthetic sample only; not proof of learning gains, broad quality equivalence, billing savings or causal speed.'})
    dump('review-adjudication.json',{'disagreements':disagreements,
          'selection':'M1/M6 use fresh independent consistency review v2; status events use independently corrected v3; remaining metrics use latest primaries.',
          'corrections_preserved':['Wrong-case readiness quotes corrected','Recheck flag removed as duplicate status event',
             'Readiness source changed from reply to actual snapshot','M9/M12 reply-only audit separated from file freshness',
             'T1 recheck not counted as whole-exam readiness','CASE07 M3b/M6b case-specific correction',
             'LaTeX percent and actual CASE04 question corrected in consistency review'],
          'evidence_policy':'Raw review drafts preserved even when quotes paraphrased/inaccurate. Compiled evidence uses verbatim source text/paths; conclusions and unresolved M6 dissent are disclosed.'})
    print('Registered gates:',gates)
    print('Repeated marker replies:',markers)


if __name__=='__main__':
    main()
