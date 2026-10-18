// Execute the delivered page script; a minimal DOM, not a rendering test.
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const path=require('node:path');

async function replay(file,firstAnswer='2'){
  const html=fs.readFileSync(file,'utf8');
  const nodes=new Map();
  const element=()=>({value:'',checked:false,disabled:false,innerHTML:'',textContent:'',
    className:'',readOnly:false,classList:{remove(){},add(){}},
    addEventListener(type,fn){this['on'+type]=fn;},click(){},focus(){}});
  const get=id=>{if(!nodes.has(id))nodes.set(id,element());return nodes.get(id);};
  get('group').value='team';get('stat').value='mean';
  const ops=[{...element(),value:'mutate',checked:true},{...element(),value:'summarize'}];
  const answers=[{...element(),value:'2'},{...element(),value:'4'}];
  let payload,clock=0,random=0;
  class ReplayDate extends Date {
    constructor(...args){super(...(args.length?args:[ReplayDate.now()]));}
    static now(){return Date.parse('2026-10-17T03:00:00Z')+clock++;}
  }
  const replayMath=Object.create(Math);replayMath.random=()=> (++random)/100;
  const context=vm.createContext({document:{getElementById:get,
    querySelectorAll(selector){return selector==='[name=op]'?ops:selector==='[name=answer]'?answers:[get('group'),get('stat')];},
    querySelector(){return answers.find(x=>x.checked)||null;},createElement:element},
    Date:ReplayDate,Math:replayMath,Blob,
    URL:{createObjectURL(blob){payload=blob;return 'blob:test';},revokeObjectURL(){}}});
  const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
  for(const script of scripts)vm.runInContext(script[1],context);
  const submit=(answer,explanation)=>{answers.forEach(x=>x.checked=x.value===answer);get('reason').value=explanation;get('check').onclick();};
  get('check').onclick(); // Blank input must not submit an attempt.
  submit(firstAnswer,firstAnswer==='2'?'There are two regions, so one row per region.':'Mutate preserves all four state rows.');
  const feedbackBeforeRetry=get('feedback').innerHTML;
  assert.match(feedbackBeforeRetry,/4 rows/,'First submission must actually disclose the solution in this fixture');
  get('check').onclick(); // Locked submissions must not duplicate the answer.
  get('retry').onclick();
  submit('4','Mutate keeps all four state observations.');
  get('export').onclick();
  const first=JSON.parse(await payload.text());
  get('export').onclick();
  const repeated=JSON.parse(await payload.text());
  assert.equal(first.attempt_id,repeated.attempt_id,'Re-export must preserve attempt identity');
  assert.equal(first.transfer_history.length,2,'Blank/double-click must not add attempts');
  assert.notEqual(first.transfer_history[0].attempt_id,first.transfer_history[1].attempt_id);
  assert.equal(first.transfer_history[0].original_answer.predicted_rows,firstAnswer);
  assert.equal(first.transfer_history[1].original_answer.predicted_rows,'4');
  return {feedback_before_retry:feedbackBeforeRetry,export:first};
}

async function check(file,output){
  const result=await replay(file);
  if(output)fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
  const rows=result.export.transfer_history;
  assert.equal(rows[0].reveal_before_submission,false,'Feedback must not retroactively taint the original response');
  assert.equal(rows[1].reveal_before_submission,true,'Retry after disclosed solution must retain exposure');
  assert.notEqual(rows[1].stage,'independent_transfer','Revealed retry must not claim independent transfer');
  const correctFirst=await replay(file,'4');
  assert.equal(correctFirst.export.transfer_history[0].reveal_before_submission,false);
  assert.equal(correctFirst.export.transfer_history[1].reveal_before_submission,true);
  console.log('PASS: actual page script preserves pre-feedback response, exposed retry, stable exports, original answers and blank/locked-submit handling.');
}
if(require.main===module)check(path.resolve(process.argv[2]||'examples/grouped-transformations.html'),process.argv[3]).catch(error=>{console.error(error);process.exitCode=1;});
module.exports={replay,check};
