# Independent benchmark-method review

Date: October 31, 2026. Scope: protocol review only; no models or external services were run for this review and no measured result is reported here.

## Source basis

The baseline state rules at commit `4212af7` require meaningful updates once per tutoring turn. Current [state rules](../../../plugins/gpt-im-cooked/skills/gpt-im-cooked/references/state.md) batch five meaningful-change turns but force earlier saves at imports, artifacts, scope changes, explicit saves, and session close. Current [artifact rules](../../../plugins/gpt-im-cooked/skills/gpt-im-cooked/references/review-artifacts.md) reuse loaded state for ordinary answers. The existing [evaluation protocol](../../EVALUATION.md) calls for synthetic fixtures, one student message at a time, raw replies and state snapshots, and separate judgments for correctness and learning evidence.

## Minimum credible comparison

- Freeze both full skill directories by commit and hash; use identical synthetic source packets, initial course profiles and records, permitted tools, model/reasoning configuration, and scripted student messages. Keep run-specific workspace paths comparable in length. Exclude global installed copies from the tutor's allowed sources.
- Use one genuinely continued CLI conversation per arm. Fresh conversations on every turn would force both arms to reload state and would not test the intended ordinary-chat workflow. Verify the resumed session identity rather than assume it.
- Run at least five meaningful-change tutoring turns, then a matched explicit save/session-close request. Count the closing turn's tokens, time, and writes in both arms; otherwise V2 could appear cheaper merely by leaving work unsaved.
- Alternate arm order across at least two paired replicates (AB then BA). A single pair is an exploratory pilot, not a stable average. Preserve failures and retries rather than silently dropping expensive runs.
- Keep substantive tutoring requests comparable and impose the same reasonable reply-length target on both arms. Report actual reply length. Equal limits do not imply equal output or equivalent teaching quality.
- Prefer a primary ordinary-chat scenario without artifact/import triggers. Report an artifact-heavy scenario separately because the intended early-save rules may remove much of the batching benefit. Do not generalize a deliberately favorable five-change-turn sequence to every study session.

## Planned execution conditions supplied by the parent

- CLI version: `0.162.1`; explicitly hold model `gpt-6.1-sol` and reasoning effort `medium` constant.
- Two paired replicates, six turns per arm, 24 turns total. Pair 1 starts baseline/V2; pair 2 starts V2/baseline. Interleave arms by turn but execute sequentially to avoid concurrent local latency contention.
- Synthetic statistics packet with three concepts and a small initial record. Five reviewed-evidence turns precede a sixth explicit save/close request.
- Isolated `CODEX_HOME` directories may reuse local authentication for execution, but credentials and home configuration are excluded from report artifacts. Inspect logs for private paths or sensitive metadata before publication; preserve usage/event fidelity when producing a sanitized public copy.
- Discover the usage event schema from the first planned turn, not from an extra excluded smoke run. Retain raw JSONL usage, end-to-end wall time, and per-turn record snapshots for human evidence checks.

These are planned conditions, not results. Two pairs support an exploratory paired comparison without confidence-interval or fee-savings claims. A small initial record does not measure scaling to long course histories, and 24 total turns do not establish long-session compaction behavior.

## Required measurements

Retain raw machine-readable event logs and wall-clock timestamps for every turn. Establish whether each usage event is per-turn or cumulative before aggregating; cumulative counters require differences rather than repeated sums.

Report input tokens, cached input tokens, derived uncached input tokens (`input - cached`, only if the usage schema defines cached as a subset), and output tokens separately. Show raw totals and the percentage change for each. A useful headline total is reported input plus output, with its cache breakdown beside it. Token count alone is not a dollar-cost estimate: cached and uncached input and output may have different prices. Avoid inventing a subscription-credit conversion.

Report end-to-end wall time per turn and per complete session. Distinguish this from time-to-first-visible-answer, which needs separate stream timestamps. Record helper read and commit invocations, observed file revisions, and failures. Tool-call count is supporting process evidence, not a substitute for tokens.

For each pair calculate reduction as `(baseline - V2) / baseline`. Show all paired values and the median/range when repeated. Do not attribute an observed percentage to batching alone when comparing the complete V2 skill: changed instructions, guide guidance, pending summaries, and output choices also affect usage. A batching-only ablation would be needed for that causal claim.

## Quality and persistence gates

Compare final persisted records after the explicit save. They need not be byte-identical, but both should retain the same meaningful errors, reasoning, corrections, assistance, improvement, and next task without invented weakness or mastery. Check final saves actually succeeded. A version that drops evidence or misgrades the work does not establish an equivalent-quality efficiency gain.

Record whether interim state remained unsaved, whether a checkpoint occurred at the intended point, and whether tool failures were retried. An optional fresh-chat recovery check can assess the handoff, but its tokens and time should be a separate measured phase. A short-session test does not demonstrate compaction savings or long-term retention.

## Safe announcement boundary

An honest result says: "In N paired synthetic sessions on [reported model/configuration], V2 used X% fewer reported input-plus-output tokens [with cache breakdown] and Y% less total wall time; final evidence checks [result]." State turn count, scenario, sample size, and variability. If only one pair completes, label X and Y observed pilot differences and omit reliability language.

Commit reductions cannot be promoted to total-token reductions. A negative or mixed result must be reported. Do not claim real learner gains, general humanities grading reliability, dollar savings, or universal response acceleration from this experiment.
