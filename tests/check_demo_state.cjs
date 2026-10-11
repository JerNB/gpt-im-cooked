// Execute the actual demo script against a minimal DOM; not a browser/layout test.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../docs/demo.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const element = () => ({value:'',checked:false,handlers:{},addEventListener(t,f){this.handlers[t]=f;},setAttribute(){},click(){},remove(){}});
const nodes = new Map();
const get = id => {if(!nodes.has(id)) nodes.set(id,element());return nodes.get(id);};
const sections = Array.from({length:8},(_,i)=>{
  const fields = new Map();
  return {id:'q'+(i+1),dataset:{kind:'single',topic:'T'+i,source:'S1'},
    fields, querySelector(key){if(!fields.has(key))fields.set(key,element());return fields.get(key);},
    querySelectorAll(){return this.answers || [];}, answers:[]};
});
const context = vm.createContext({
  document:{querySelectorAll:()=>sections,querySelector:()=>element(),getElementById:get,
    createElement:()=>element(),body:{append() {}}},
  crypto:{randomUUID:()=> 'test-session'}, Blob, URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},
  setTimeout(){}, Date, Math, console
});
get('exam').reset=()=>{sections.forEach(s=>{s.answers=[];s.fields.forEach(e=>{e.value='';e.checked=false;});});};
vm.runInContext(script,context);
const click = id => get(id).handlers.click();
const exported = () => JSON.parse(get('export-output').value);
sections[0].answers=[{value:'B'}];
sections[0].querySelector('[name="reasoning"]').value='Before seeing the key';
click('key-link');
sections[0].answers=[{value:'A'}];
click('export');
const first=exported();
assert.equal(first.schema_version,'1.0');
assert.equal(first.session_id,'test-session');
assert.deepEqual(first.attempt_history[0].items[0].original_answer,['B']);
assert.equal(first.attempt_history[0].items[0].assistance.key_opened_in_page,false);
assert.equal(first.items[0].assistance.key_opened_in_page,true);
click('export');
assert.equal(exported().attempt_id,first.attempt_id);
click('retry');
click('export');
const retry=exported();
assert.notEqual(retry.attempt_id,first.attempt_id);
assert.equal(retry.session_id,first.session_id);
assert.equal(retry.items[0].assistance.key_opened_in_page,true);
assert.deepEqual(retry.items[0].original_answer,[]);
assert.equal(retry.attempt_history[0].items[0].assistance.key_opened_in_page,false);
console.log('PASS: pre-key answers, immutable snapshots, stable export identity, retry identity and exposure');
