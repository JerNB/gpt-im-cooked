// Replay the maintained worksheet's actual script. No browser/layout claim.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '..');

function worksheet() {
  const html = fs.readFileSync(path.join(ROOT, 'docs/demo.html'), 'utf8');
  const nodes = new Map();
  const element = () => ({value:'', checked:false, handlers:{},
    addEventListener(t,f){this.handlers[t]=f;}, setAttribute(){}, click(){}, remove(){}});
  const get = id => {if(!nodes.has(id)) nodes.set(id,element()); return nodes.get(id);};
  const sections = [...html.matchAll(/<section class="question" id="([^"]+)" data-kind="([^"]+)" data-topic="([^"]+)" data-source="([^"]+)"/g)].map(m => {
    const fields = new Map();
    return {id:m[1], dataset:{kind:m[2], topic:m[3], source:m[4]}, fields, answers:[],
      querySelector(key){if(!fields.has(key))fields.set(key,element());return fields.get(key);},
      querySelectorAll(){return this.answers;}};
  });
  assert.equal(sections.length, 8);
  class FixedDate extends Date {constructor(...args){super(...(args.length?args:['2026-10-17T02:00:00Z']));}}
  const context = vm.createContext({document:{querySelectorAll:()=>sections,
    querySelector:()=>element(),getElementById:get,createElement:()=>element(),body:{append(){}}},
    crypto:{randomUUID:()=> 'evidence-session'}, Blob,
    URL:{createObjectURL:()=> 'blob:test', revokeObjectURL(){}}, setTimeout(){}, Date:FixedDate, Math});
  get('exam').reset=()=>sections.forEach(s=>{s.answers=[];s.fields.forEach(e=>{e.value='';e.checked=false;});});
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], context);
  return {sections, click:id=>get(id).handlers.click(),
    export(){get('export').handlers.click();return JSON.parse(get('export-output').value);}};
}

function replay() {
  const page = worksheet();
  const q4 = page.sections.find(s=>s.id==='q4');
  q4.answers=[{value:'B'}];
  q4.querySelector('[name="reasoning"]').value='The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70.';
  const before = page.export();
  page.click('key-link');
  const after = page.export();
  page.click('retry');
  q4.answers=[{value:'B'}];
  q4.querySelector('[name="reasoning"]').value='The reference population is Plus-plan tickets: 40. Of those, 28 had a short wait, so 28/40 = 0.70.';
  const retry = page.export();
  return {before, after, retry};
}

function prepare(destination) {
  const dir=path.resolve(destination);
  fs.mkdirSync(dir,{recursive:true});
  const states=replay();
  for(const [name,data] of Object.entries(states))fs.writeFileSync(path.join(dir,`${name}.json`),JSON.stringify(data,null,2)+'\n');
  for(const [source,target] of [['docs/demo.html','worksheet.html'],['docs/course-packet.md','course-packet.md'],['docs/answer-key.html','answer-key.html']])
    fs.copyFileSync(path.join(ROOT,source),path.join(dir,target));
  fs.writeFileSync(path.join(dir,'course-profile.md'),`# Course profile

Course: Fictional intro statistics. Exam: Mock Exam A.
Sources: course-packet.md S1-S5; worksheet.html q1-q8; answer-key.html.
Included: course-packet.md S1-S5. Exclusions: its Scope and practice style section.
Learning record: learning-record.md. No official points rubric.
`);
  fs.writeFileSync(path.join(dir,'learning-record.md'),`# Learning record

## Study setup
- Quick start shown: Yes
- Language: English

## Active course and exam
Fictional intro statistics / Mock Exam A; course-profile.md.

## Concepts
| Concept ID | Concept | Status | Evidence | Next task |
|---|---|---|---|---|
| within-group-denominator | Reference population | Improving | P01: after an earlier whole-table denominator error, student correctly explained 6/15 fiction loans versus 6/40 all loans. Explicitly reported no hints, solutions or outside help before that response. One distinct context; not Demonstrated. Basis: course-packet.md S3. | New context with population explanation |

## Attempt history
P01 original response: "Six overdue fiction loans out of 15 fiction loans: 6/15; out of all 40 loans: 6/40. The requested population sets the denominator." Reviewed correct; independence is student-reported. Prior wrong original response: "6/40 in both because always use all rows." Corrected in prior feedback. Date unknown.

## Import ledger
No worksheet export reviewed yet.

## Student-reported difficulties
Previously choosing denominators in word problems.

## Open questions
No item time for P01; do not infer its chronology relative to exports.

## Next session
Review supplied export and select the next useful practice.
`);
}

if(require.main===module){if(!process.argv[2])throw Error('Usage: node tests/prepare_evidence_case.cjs <isolated-directory>');prepare(process.argv[2]);}
module.exports={worksheet,replay,prepare};
