// Run the rendered mock-exam worksheet script against a minimal DOM; not a browser/layout test.
const fs = require('node:fs');
const os = require('node:os');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');

const skill = path.join(__dirname, '../plugins/gpt-im-cooked/skills/gpt-im-cooked');
const out = fs.mkdtempSync(path.join(os.tmpdir(), 'cooked-mock-'));
const python = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
execFileSync(python, ['-B', path.join(skill, 'scripts/render_mock_exam.py'),
  path.join(skill, 'assets/mock-exam-example.json'), '--out', out]);
const exam = JSON.parse(fs.readFileSync(path.join(skill, 'assets/mock-exam-example.json'), 'utf8'));
const html = fs.readFileSync(path.join(out, exam.artifact_id + '.html'), 'utf8');
const dataJson = html.match(/<script type="application\/json" id="artifact-data">([\s\S]*?)<\/script>/)[1];
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const sectionRe = /<section class="question" id="([^"]+)" data-kind="([^"]+)" data-topic="([^"]+)" data-source="([^"]+)"/g;
const parsed = [...html.matchAll(sectionRe)];
assert.equal(parsed.length, exam.questions.length);

const element = () => ({value: '', checked: false, open: false, textContent: '', handlers: {},
  addEventListener(t, f) { this.handlers[t] = f; }, setAttribute() {}, click() {}, remove() {}});
const nodes = new Map();
const get = id => { if (!nodes.has(id)) nodes.set(id, element()); return nodes.get(id); };
get('artifact-data').textContent = dataJson;
const navStatus = new Map();
const sections = parsed.map(([, id, kind, topic, source]) => {
  const fields = new Map();
  const s = {id, dataset: {kind, topic, source}, answers: [], fields,
    querySelector(key) { if (!fields.has(key)) fields.set(key, element()); return fields.get(key); },
    querySelectorAll() { return this.answers; }};
  return s;
});
const doc = {
  querySelectorAll: sel => (sel === '.question' ? sections : []),
  querySelector: sel => { const m = sel.match(/data-nav="([^"]+)"/); if (!m) return null;
    if (!navStatus.has(m[1])) navStatus.set(m[1], element()); return navStatus.get(m[1]); },
  getElementById: get, createElement: () => element(), body: {append() {}}
};
let unload = null;
const context = vm.createContext({document: doc, crypto: {randomUUID: () => 'test-session'}, Blob,
  URL: {createObjectURL: () => 'blob:test', revokeObjectURL() {}}, setTimeout() {}, Date, Math, JSON, console,
  addEventListener: (t, f) => { if (t === 'beforeunload') unload = f; }});
get('exam').reset = () => sections.forEach(s => { s.answers = []; s.fields.forEach(e => { e.value = ''; e.checked = false; }); });
vm.runInContext(script, context);

const byId = id => sections.find(s => s.id === id);
const click = id => get(id).handlers.click();
const input = s => get('exam').handlers.input({target: {closest: () => s}});
const exported = () => JSON.parse(get('export-output').value);

assert.equal(get('progress-text').textContent, `0 of ${sections.length} answered`);
byId('q2').answers = [{value: 'A'}];
byId('q3').querySelector('[name="answer"]').value = '12/30';
byId('q3').querySelector('[name="reasoning"]').value = 'Before the key';
byId('q1').querySelector('[data-flag]').checked = true;
input(byId('q2'));
assert.equal(get('progress-text').textContent, `2 of ${sections.length} answered`);
assert.equal(navStatus.get('q2').textContent, '●');
assert.equal(navStatus.get('q1').textContent, '⚑');
assert.equal(navStatus.get('q4').textContent, '○');
const prevented = {preventDefault() { this.done = true; }};
unload(prevented);
assert.equal(prevented.done, true, 'unexported answers should warn before unload');

click('key-link');
byId('q2').answers = [{value: 'B'}];
click('export');
const first = exported();
assert.equal(first.schema_version, '1.0');
assert.equal(first.artifact_id, exam.artifact_id);
assert.equal(first.session_id, 'test-session');
assert.equal(first.items.length, exam.questions.length);
const pre = first.attempt_history[0];
assert.equal(pre.reason, 'before key access');
assert.deepEqual(pre.items.find(i => i.item_id === 'q2').original_answer, ['A']);
assert.equal(pre.items.find(i => i.item_id === 'q3').original_answer, '12/30');
assert.equal(pre.items.find(i => i.item_id === 'q2').assistance.key_opened_in_page, false);
assert.equal(first.items.find(i => i.item_id === 'q2').assistance.key_opened_in_page, true);
assert.deepEqual(first.items.find(i => i.item_id === 'q2').original_answer, ['B']);
assert.ok(first.items.every(i => i.source_basis && i.topic_id && i.item_type));
const after = {preventDefault() { this.done = true; }};
unload(after);
assert.notEqual(after.done, true, 'no warning right after export');

click('export');
assert.equal(exported().attempt_id, first.attempt_id, 'repeat export keeps the attempt identity');
click('retry');
click('export');
const retry = exported();
assert.notEqual(retry.attempt_id, first.attempt_id);
assert.equal(retry.session_id, first.session_id);
assert.equal(retry.items.find(i => i.item_id === 'q2').assistance.key_opened_in_page, true, 'exposure survives retry');
assert.deepEqual(retry.items.find(i => i.item_id === 'q2').original_answer, []);
assert.equal(retry.attempt_history[0].items.find(i => i.item_id === 'q2').assistance.key_opened_in_page, false,
  'earlier snapshot is not rewritten');
fs.rmSync(out, {recursive: true, force: true});
console.log('PASS: rendered worksheet status/flags, unload warning, pre-key snapshot, stable export identity, retry exposure.');
