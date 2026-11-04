"""Aggregate the benchmark's cumulative CLI usage without double counting."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'tests/reports/2026-10-31-token-benchmark'


def increments(rows):
    previous = {}
    answer = []
    for row in rows:
        key = (row['pair'], row['arm'])
        old = previous.get(key, {})
        usage = row['usage']
        delta = {k: v - old.get(k, 0) for k, v in usage.items()}
        assert all(v >= 0 for v in delta.values()), (key, row['turn'], delta)
        previous[key] = usage
        answer.append({**row, 'incremental_usage': delta})
    return answer


def main():
    # A continued session reports 10 then 16, so the two turns total 16, not 26.
    example = [{'pair': 1, 'arm': 'a', 'turn': 1, 'usage': {'input_tokens': 10}},
               {'pair': 1, 'arm': 'a', 'turn': 2, 'usage': {'input_tokens': 16}}]
    assert sum(r['incremental_usage']['input_tokens'] for r in increments(example)) == 16
    rows = increments(json.loads((REPORT / 'results.json').read_text(encoding='utf-8')))
    summaries = []
    for pair in sorted({r['pair'] for r in rows}):
        for arm in ['baseline', 'v2']:
            items = [r for r in rows if (r['pair'], r['arm']) == (pair, arm)]
            run = REPORT / 'runs' / f'pair-{pair}-{arm}'
            totals = {k: sum(r['incremental_usage'][k] for r in items) for k in items[0]['usage']}
            assert totals == items[-1]['usage']
            accounting = json.loads((run / f"accounting-after-{items[-1]['turn']:02}.json").read_text(encoding="utf-8"))
            assert accounting and accounting[-1]["total_token_usage"]["input_tokens"] == totals["input_tokens"]
            assert accounting[-1]["total_token_usage"]["output_tokens"] == totals["output_tokens"]
            commands = 0
            failed_commands = 0
            associated = 0
            changes = []
            words = []
            before = (REPORT / 'initial-learning-record.md').read_text(encoding='utf-8')
            for row in items:
                turn = row['turn']
                events = [json.loads(s) for s in (run / f'turn-{turn:02}.jsonl').read_text(encoding='utf-8').splitlines()]
                for event in events:
                    item = event.get('item', {})
                    if event.get('type') == 'item.completed' and item.get('type') == 'command_execution':
                        commands += 1
                        failed_commands += int(item.get("exit_code", 0) not in (None, 0))
                        associated += int('learning-record' in item.get('command', ''))
                after = (run / f'learning-record-after-{turn:02}.md').read_text(encoding='utf-8')
                if after != before:
                    changes.append(turn)
                before = after
                words.append(len(re.findall(r'\b[\w\x27-]+\b', (run / f'response-{turn:02}.md').read_text(encoding='utf-8'))))
            summaries.append({
                'pair': pair, 'arm': arm, **totals,
                'uncached_input_tokens': totals['input_tokens'] - totals['cached_input_tokens'],
                'total_tokens': totals['input_tokens'] + totals['output_tokens'],
                'wall_seconds': round(sum(r['wall_seconds'] for r in items), 3),
                'command_execution_items': commands,
                'nonzero_exit_commands': failed_commands,
                'max_observed_model_call_input': max(a['last_token_usage']['input_tokens'] for a in accounting if a),
                'commands_mentioning_learning_record': associated,
                'record_changed_after_turns': changes,
                'agent_message_words_by_turn': words,
            })
    comparisons = []
    keys = ['total_tokens', 'input_tokens', 'cached_input_tokens', 'uncached_input_tokens', 'output_tokens', 'wall_seconds', 'command_execution_items']
    for pair in sorted({s['pair'] for s in summaries}):
        a = next(s for s in summaries if s['pair'] == pair and s['arm'] == 'baseline')
        b = next(s for s in summaries if s['pair'] == pair and s['arm'] == 'v2')
        comparisons.append({'pair': pair, 'reduction_percent': {k: round(100 * (a[k] - b[k]) / a[k], 2) for k in keys}})
    pooled = {}
    for k in keys:
        a = sum(s[k] for s in summaries if s['arm'] == 'baseline')
        b = sum(s[k] for s in summaries if s['arm'] == 'v2')
        pooled[k] = {'baseline': a, 'v2': b, 'reduction_percent': round(100 * (a - b) / a, 2)}
    result = {'accounting': 'turn.completed usage is session cumulative; per-turn values are first differences', 'sessions': summaries, 'pairs': comparisons, 'pooled': pooled, 'turns': rows}
    (REPORT / 'summary.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'sessions': summaries, 'pairs': comparisons, 'pooled': pooled}, indent=2))


if __name__ == '__main__':
    main()
