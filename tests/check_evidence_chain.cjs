// Factual replay and arithmetic invariants, not a semantic model evaluator.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {replay,prepare} = require('./prepare_evidence_case.cjs');
const {before,after,retry} = replay();
const q4 = data => data.items.find(x=>x.item_id==='q4');
assert.deepEqual(q4(before).original_answer,['B']);
assert.equal(q4(before).assistance.key_opened_in_page,false);
assert.match(q4(before).assistance.external_help,/not tracked/);
assert.equal(q4(after).assistance.key_opened_in_page,true);
assert.equal(after.attempt_id,before.attempt_id);
assert.deepEqual(after.attempt_history[0].items,before.items);
assert.equal(q4({items:after.attempt_history[0].items}).assistance.key_opened_in_page,false);
assert.notEqual(retry.attempt_id,before.attempt_id);
assert.equal(q4(retry).assistance.key_opened_in_page,true);
assert.deepEqual(q4(retry).original_answer,q4(before).original_answer);
assert.equal(before.items.filter(x=>Array.isArray(x.original_answer)?x.original_answer.length:x.original_answer.trim()).length,1);
assert.equal(28/40,7/10);
assert.notEqual(28/60,7/10);
assert.equal(2/8,0.25); assert.equal(2/20,0.1);

const historical=JSON.parse(fs.readFileSync(path.join(__dirname,'reports/2026-10-10/browser-attempts.json'),'utf8'));
const r2=historical.events.find(x=>x.order===6);
assert.equal(r2.answerRevealed,true);
assert.equal(r2.answerRevealedBeforeAttempt,false);
assert.equal(r2.assistanceBeforeAttempt,'after-hint');
assert.equal(r2.feedbackRevealedAnswer,true);
const r3=historical.events.find(x=>x.order===9);
assert.equal(r3.originalResponse.answers['R3-a'],'35%');
assert.equal(7/(13+7),0.35); assert.notEqual(7/40,0.35);
assert.equal(r3.assistanceBeforeAttempt,'after-reveal');

// Verify the isolated study inputs are faithful to the maintained sources.
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'cooked-evidence-'));
try {
  prepare(temp);
  for(const [name,data] of Object.entries({before,after,retry}))
    assert.deepEqual(JSON.parse(fs.readFileSync(path.join(temp,name+'.json'),'utf8')),data);
  for(const [source,target] of [['docs/demo.html','worksheet.html'],['docs/course-packet.md','course-packet.md'],['docs/answer-key.html','answer-key.html']])
    assert.deepEqual(fs.readFileSync(path.join(__dirname,'..',source)),fs.readFileSync(path.join(temp,target)));
  assert.ok(fs.existsSync(path.join(temp,'learning-record.md')));
  assert.ok(fs.existsSync(path.join(temp,'course-profile.md')));
} finally {
  const resolved=fs.realpathSync(temp);
  assert.ok(resolved.startsWith(fs.realpathSync(os.tmpdir())+path.sep));
  assert.ok(path.basename(resolved).startsWith('cooked-evidence-'));
  fs.rmSync(resolved,{recursive:true});
}
console.log('PASS: generated pre/post-key snapshots, identity/retry/exposure, unknown external help, blank fields, equivalent values, historical response-time flags and denominator counterexamples.');
console.log('This checks raw evidence invariants only; tutor verdicts require separate adjudication.');
