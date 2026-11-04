# V2 token and latency benchmark

Date: October 31, 2026. **Exploratory whole-version comparison, not a learning-outcome study.**

In two paired synthetic study sessions, V2 used **39.20% fewer reported input-plus-output tokens** and **25.40% less end-to-end wall time** than v0.5.1. Both comparisons included all five learning turns and the final save/handoff turn. Neither saved evidence nor mathematical feedback was omitted in the reviewed sample. However, one V2 session prematurely promoted a progress label, so these results **do not establish quality-neutral savings**.

## Measured results

The table pools two six-turn sessions per version (12 turns per version; 24 real tutor turns overall). Reduction is `(baseline - V2) / baseline`.

| Metric | Baseline | V2 | Reduction |
|---|---:|---:|---:|
| Reported input + output tokens | 1,166,425 | 709,148 | 39.20% |
| Input tokens, including cached input | 1,155,178 | 701,700 | 39.26% |
| Cached input tokens (input subset) | 1,060,736 | 665,472 | 37.26% |
| Uncached input tokens | 94,442 | 36,228 | 61.64% |
| Output tokens, including reasoning | 11,247 | 7,448 | 33.78% |
| End-to-end wall time (seconds) | 287.827 | 214.724 | 25.40% |
| Completed shell-command batches | 27 | 15 | 44.44% |

Records changed after all six turns in each baseline session and after turns 5 and 6 in each V2 session: **12 versus 4 change-bearing save turns, a 66.67% reduction**. This counts turns whose persisted record content changed, not every low-level filesystem write. Considering only the five learning turns gives 10 versus 2; the headline comparison includes the closing saves instead of advertising the more favorable partial result.

| Pair / execution order | Baseline total tokens | V2 total tokens | Token reduction | Baseline time | V2 time | Time reduction |
|---|---:|---:|---:|---:|---:|---:|
| 1 / baseline then V2 within each turn | 566,085 | 339,374 | 40.05% | 146.410 s | 107.191 s | 26.79% |
| 2 / V2 then baseline within each turn | 600,340 | 369,774 | 38.41% | 141.417 s | 107.533 s | 23.96% |

These are two replicates of one workload, not two independent courses. No confidence interval or reliability percentage is claimed. Regex word counts of normalized saved agent messages were 2,226 versus 2,117 (4.90% fewer for V2), including Markdown, commentary, and closing replies. Reply length was targeted equally but was not identical. Output-token usage also includes generated tool arguments/record drafts and reasoning, so it is not a visible-reply word count.

## The latency tradeoff

For turns 1-4, mean end-to-end time was 25.53 s for baseline and 11.54 s for V2 (54.79% lower). At the turn-5 checkpoint, mean time was 21.18 s versus 38.58 s: **V2 was 82.12% slower for that save turn**. Closing-turn mean time was 20.60 s versus 22.61 s. V2 reduced whole-session time while concentrating more work at checkpoints; it did not make every answer faster.

Timing covers CLI launch through process completion, including model calls, local commands, and saves. It is not time to first token or first visible explanation. Network/server load, cache behavior, and Windows command startup were not isolated. No command-execution items returned nonzero exit codes in the four sessions. Both arms logged temporary-home helper-alias and shell-snapshot warnings; these are retained in stderr evidence and limit extrapolation to normal desktop sessions.

## Quality and persistence findings

An independent agent reviewer inspected the synthetic questions, all 20 question-feedback events, and the four final records without reading the token/time summary. This is an agent review under the skill's criteria, not external educator adjudication.

- All 20 mathematical/conceptual feedback events were judged correct.
- All four final records retained the three original error mechanisms and reasoning, both later correct applications, and actionable next steps.
- Pair 1 baseline gave a Q3-specific cue before Q3 and then correctly recorded that attempt as guided; V2 used another hypothetical. The generated teaching content was therefore not identical despite identical scripted student prompts.
- In pair 2, V2 upgraded conditional probability to `Demonstrated` after Q3/Q5, although these are same-structure applications. The reviewer judged this too strong under the rule that changing names alone does not establish transfer. Baseline remained `Improving`. **The V2 progress-calibration gate failed in one of its two sessions.** This is a conservative semantic review finding, not a mathematical grading error.
- Final captured workspace records exactly matched the saved turn-6 snapshots. Recent evidence remained unsaved until the intended V2 checkpoint; abrupt-close recovery was not tested.

See the [quality review and evidence locators](QUALITY-REVIEW.md). Do not advertise this result as "no quality tradeoff," "all quality gates passed," or a measured learning improvement.

## Reproducible setup

- Configured model: `gpt-6.1-sol`; reasoning effort: `medium`; CLI: `0.162.1`; Windows host. An immutable backend model build was not exposed.
- Baseline: v0.5.1 source at `4212af7`; candidate: v2.0.0 at `a2d5d9b`. Full skill directories are frozen in [skills/baseline](skills/baseline/SKILL.md) and [skills/v2](skills/v2/SKILL.md), with full commit IDs in [protocol.json](protocol.json).
- Each arm used a separate, continued CLI session, isolated configuration, the same [1,127-byte initial record](initial-learning-record.md), [course profile](course-profile.md), and [1,813-byte synthetic packet](packet.md). No installed skill or private student record was supplied.
- Each pair alternated arms by turn, with all calls executed serially. Pair 2 reversed the starting arm. No completed call was discarded and no trial was rerun to replace an unfavorable outcome.
- The [six scripted prompts](prompts.json) cover three explained errors, two correct same-structure applications, and an explicit save/close. No PDF, HTML artifact, or import is requested. This ordinary-chat scenario favors batching; artifact/import-heavy sessions and large histories remain untested.
- This compares the complete skill versions, including instruction and response differences. It is not a batching-only ablation and cannot assign a causal percentage to one rule change.

The runner uses an existing local Codex login. Its temporary authentication directories are excluded from evidence and removed on completion. Logs contain only synthetic study material; private home paths are normalized and extracted response links are made relative. The run used a sidecar to preserve generated synthetic files; the current runner integrates final capture for future reproductions without changing model prompts or configuration.

## Accounting and interpretation

[Official Codex documentation](https://learn.chatgpt.com/docs/non-interactive-mode) describes non-interactive JSON event output and session continuation. In this execution, each `turn.completed.usage` object was **session cumulative**. The analyzer differences counters separately for each session before summing and verifies final totals against that session's `token_count` accounting. Summing the six cumulative counters directly would overcount the session.

[OpenAI's token-counting documentation](https://developers.openai.com/api/docs/guides/token-counting) explains that processed input includes more than user-visible text, and reported output includes more than the visible answer. Here, totals count input processed across repeated model calls plus output, rather than unique conversation text. Cached input is included in input and is not added again. Recorded cache-write counts were zero; reasoning-output tokens are a subset of output and are not added again.

**Token reduction is not a dollar or subscription-credit saving percentage.** [Prompt-cache pricing and behavior](https://developers.openai.com/api/docs/guides/prompt-caching) differ from uncached processing, and no bill was measured. Cache-hit proportions also differed across arms. Maximum observed single-call input was below 41,000 tokens, against a reported 475,000-token context window. Session-cumulative input totals above that window do not imply compaction. No compaction saving, fresh-chat recovery performance, or long-term learning gain was measured.

## Evidence and rerun

- [Raw cumulative counters and per-call wall times](results.json)
- [Computed summary and per-turn counter differences](summary.json)
- [Frozen inputs and execution metadata](protocol.json)
- [Independent method review](METHOD-REVIEW.md) and [quality review](QUALITY-REVIEW.md)
- [Runner](../../benchmark_record_cost.py) and [analyzer](../../analyze_record_cost.py)
- [Evidence fingerprints](manifest.json)

The `runs/` directories preserve sanitized CLI JSONL events, stderr, responses, accounting snapshots, record snapshots after every turn, and final synthetic workspaces. Command paths/output paths may use placeholders; numerical usage fields are preserved. The fingerprint manifest checks stored bytes, not semantic correctness.

Run the analyzer without inference cost:

```text
python tests/analyze_record_cost.py
```

Running `python tests/benchmark_record_cost.py --pairs 2` makes new model calls using the current login/quota and refuses to overwrite an existing `results.json`. Preserve or relocate the existing report before reproducing. The tested commit snapshots remain fixed in the runner.

## Suggested public wording

> In an exploratory 24-turn comparison on one synthetic statistics-review workload, GPT, I'm Cooked V2 used 39.2% fewer reported input-plus-output tokens and completed the sessions in 25.4% less total time than v0.5.1, including final saves. All reviewed attempts were preserved. We also found one overly optimistic progress label, which remains a follow-up issue; this small test does not establish equal quality, fee savings, or learning gains.

Before making broader efficiency claims, repeat on more courses and models, add artifact-heavy and long-record workloads, and tighten/retest progress calibration with a genuine transfer check.
