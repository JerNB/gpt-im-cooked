"""Apply disclosed report-only cc review corrections; never execute a tutor run.

Run after finish_t004.py when rebuilding the final publication. Original final
judgments come from the reviewed commit, so repeated application is idempotent.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import subprocess

BASE = Path(__file__).parent
FINAL = BASE / 'final'
PREFIX = 'tests/reports/2026-11-14-controlled-comparison/'
REVIEWED = '49f074b330a24acf23f6e9aa755862b9c6545d6b'


def original(name):
    return subprocess.check_output(['git', 'show', f'{REVIEWED}:{PREFIX}{name}']).decode('utf-8')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='')


scores = json.loads(original('final/scores-blind.json'))
before = json.loads(original('final/scores-blind.json'))['cases']
cases = scores['cases']
mapping = load(FINAL / 'blind-map.json')
adjudication = {
    'agent': 'codex', 'date': '2026-11-14', 'reviewed_head': REVIEWED,
    'disclosure': 'NEW post-review adjudication, unblinded, no reruns. Original primary/second judgments and prior adjudication files remain unchanged. Previous final entries are preserved below.',
    'M6_rule': 'Reversed conditional is an accepted example, but mere new names/numbers with an explicitly named reference group are excluded. Both items reverse direction while supplying/naming the denominator; the frozen rule does not resolve this overlap.',
    'changes': [],
}
for case in ('CASE-11', 'CASE-04'):
    old = before[case]['M6']
    new = {
        'status': 'unclear',
        'evidence': ('Turn 6: 50 members, 20 seniors, 8 senior volunteers, 16 volunteers; asks the percentage of volunteers who are seniors.' if case == 'CASE-11' else 'Turn 6: 50 members, 20 students, 15 borrowers including 9 students; asks the percentage of borrowers who are students.'),
        'note': 'New post-review adjudication: same outcome for structurally equivalent reversed-direction items with supplied reference-group totals and distractor groups. Frozen-rule overlap remains contested; see post-review-adjudication.json for the previous final judgment. This is not an established C regression.',
    }
    cases[case]['M6'] = new
    adjudication['changes'].append({'case': case, 'session': mapping[case], 'metric': 'M6', 'previous_final': old, 'new_final': new})

gap = (BASE / load(FINAL / 'selected-sessions.json')['A1-S-rep2'] / 'response-08.md').read_text(encoding='utf-8').splitlines()[0]
for metric, count in (('M8', 3), ('M12', 0), ('M14', 0)):
    old = before['CASE-03'][metric]
    new = {'count': count, 'evidence': gap if metric == 'M14' else old['evidence']}
    if metric == 'M14':
        new['note'] = 'Zero labelled offers; the reply directly teaches the gap topic as course content, despite acknowledging the missing notes. Original fail denotes unsupported teaching, not merely no offer. M4 remains fail.'
    cases['CASE-03'][metric] = new
    adjudication['changes'].append({'case': 'CASE-03', 'session': 'A1-S-rep2', 'metric': metric, 'previous_final': old, 'new_final': new})
old = before['CASE-03']['M4']
cases['CASE-03']['M4'] = {**old, 'evidence': gap}
adjudication['changes'].append({'case': 'CASE-03', 'session': 'A1-S-rep2', 'metric': 'M4', 'previous_final': old, 'new_final': cases['CASE-03']['M4']})
allowed = {('CASE-11', 'M6'), ('CASE-04', 'M6'), *[('CASE-03', k) for k in ('M8', 'M12', 'M14', 'M4')]}
assert {(c, k) for c in cases for k in cases[c] if cases[c][k] != before[c][k]} == allowed
scores['post_review'] = 'See post-review-adjudication.json. All other final judgments unchanged.'
dump(FINAL / 'post-review-adjudication.json', adjudication)
dump(FINAL / 'scores-blind.json', scores)
counts = defaultdict(lambda: defaultdict(Counter))
for case, row in cases.items():
    for metric, value in row.items():
        counts[mapping[case].split('-')[0]][metric][str(value.get('overallstatus', value.get('status', value.get('score', value.get('count', 'unclassified')))))] += 1
dump(FINAL / 'counts.json', {a: {k: dict(v) for k, v in ms.items()} for a, ms in counts.items()})
auto = load(FINAL / 'scores-auto.json')
auto['confirmed_review_results'] = {mapping[c]: {k: v for k, v in row.items() if k in ('M1', 'M3', 'M5', 'M8', 'M11', 'M13')} for c, row in cases.items()}
dump(FINAL / 'scores-auto.json', auto)

saved = []
for name, rel in sorted(load(FINAL / 'selected-sessions.json').items()):
    if name.split('-')[0] not in ('B', 'C'):
        continue
    session = BASE / rel
    previous = None
    changes, snapshots = [], []
    for turn in range(1, 12):
        paths = list((session / f'files-after-{turn:02}').rglob('learning-record.md'))
        assert len(paths) <= 1
        data = paths[0].read_bytes() if paths else None
        digest = hashlib.sha256(data).hexdigest() if data is not None else None
        if digest != previous:
            changes.append(turn)
        snapshots.append({'turn': turn, 'sha256': digest})
        previous = digest
        if turn == 10:
            text10 = data.decode('utf-8') if data else ''
    readiness = [line for line in text10.splitlines() if 'readiness' in line.lower() or 'ready for' in line.lower()]
    # Semantic check: these lines must describe the current whole-exam review,
    # not generic "insufficient" transfer evidence or a source-gap mention.
    present = bool(readiness)
    assert present == name.startswith('C-')
    reply = (session / 'response-11.md').read_text(encoding='utf-8')
    stale = 'Picking up the unanswered question:' in reply
    assert stale == (name == 'B-P-rep1')
    saved.append({'session': name, 'record_bytes_changed_at_turns': changes,
                  'snapshots': snapshots, 'readiness_review_after_turn10': present,
                  'readiness_evidence': readiness,
                  'resume_stale_answered_transfer': stale,
                  'resume_evidence': next(line for line in reply.splitlines() if ('Picking up the unanswered' in line if stale else any(term in line.lower() for term in ('next step', 'next was', 'next topic'))))})
dump(FINAL / 'saved-state-audit.json', {'method': 'Compare learning-record.md bytes across adjacent files-after-NN snapshots; absence before initial creation counts as a change. Readiness and stale resume are manually confirmed against record and turn-11 reply; no reply/record edits.', 'sessions': saved})
table = '| Session | Record bytes changed at turns | Turn-10 readiness review saved | Turn-11 stale answered-transfer resume |\n|---|---|---|---|\n'
table += '\n'.join(f"| {s['session']} | {', '.join(map(str, s['record_bytes_changed_at_turns']))} | {'Yes' if s['readiness_review_after_turn10'] else 'No'} | {'Yes' if s['resume_stale_answered_transfer'] else 'No'} |" for s in saved)
report = original('REPORT.md')
report = report.replace('A2 did so twice out of four.', 'A2 did so 2/4 under the retained adjudication, or 3/4 if A2-P-rep2 is accepted (primary pass, independent second fail), versus B 4/4. This genuine-transfer gap depends on that contested adjudication.')
report = report.replace('C therefore did not fully repair reply completeness. This metric concerns what the resume reply reflects, not proof of data loss in its saved file.', 'M9/M12 measure what the resume reply recites, rather than whether the saved state is current. M12 is a weakness of the cc-written rubric: a useful resume need not recite every prior event. The 1/4 result is not evidence of an unrepaired stale-state defect; see the saved-state audit below.')
report = report.replace("C's M6 passed three times out of four versus B's four times out of four: one C item was a new story with the same explicit-group calculation. A recheck marker does not make such an item a genuine transfer.", "C's M6 has three passes and one unclear versus B's four passes. The C-S-rep2 item is a contested adjudication, not an established C regression. A1-S-rep1 now has the same unclear outcome: both reverse conditioning, explicitly supply the reference-group total, and include a distractor group. The frozen rubric accepts reversals but excludes mere explicit-group calculations, leaving this overlap unresolved.")
report = report.replace('## Behavioral counts', table + '\n\nReadiness review is saved in C 4/4 versus B 0/4, and an already-answered transfer is re-posed at resume in B 1/4 versus C 0/4. B-P-rep1 repeats the early-stop question answered at turn 7. Other B resumes use the saved transfer result but still lack the turn-10 readiness review; this is narrower than claiming their files were fully current. The reviewer\'s approximate B 1/4 readiness figure is not confirmed: all four B records were unchanged after turn 5 or 7, before the readiness request. B\'s five-turn meaningful-change checkpoint happened to land on script turn 7 in 3/4 sessions, understating the batching risk seen in the pilot. [Saved-state audit](final/saved-state-audit.json) includes per-turn hashes and evidence.\n\n## Behavioral counts')
report = report.replace('| C | 4 | 3 /1 | 4 /0 | 3 /1 /0 |', '| C | 4 | 3 /1 | 4 /0 | 3 /0 /1 |')
report = report.replace('The other fifteen case judgments and prior adjudications are unchanged.', 'NEW disclosed post-review adjudication: C-S-rep2 M6 changes fail to unclear; A1-S-rep1 stays unclear with matched reasoning. Original judgments and prior adjudications remain visible in their original files and in [the new adjudication record](final/post-review-adjudication.json). CASE-03 uses numeric counts M8=3, M12=0, M14=0; its M14 denotes direct teaching of Bayes\' rule as course content without a labelled offer, and M4/M14 now quote the actual teaching line. All other judgments are unchanged.')
report = report.replace('## Resource differences', 'M1 sensitivity: B-P-rep1 and C-P-rep1 fail because worked examples on a same-size four-element pass reproduce Q1\'s keyed value, 3 comparisons, although they use different data from Q1. The frozen key-value rule still scores both as fails; this small integer is reproduced by any same-size full pass. No skill-arm S session failed M1. These qualifications apply to every M1 count above; the counts themselves are unchanged.\n\n## Resource differences')
(BASE / 'REPORT.md').write_text(report, encoding='utf-8', newline='')
print('Post-review corrections generated; six authorized entries changed, other judgments and all selected-session files preserved.')
