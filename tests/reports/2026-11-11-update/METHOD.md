# Post-PR3 validation and benchmark method

Study date label: November 11, 2026, America/New_York. Raw timestamps use UTC.
This is a synthetic engineering evaluation, not a real-student learning study.

## Questions and comparisons

1. Does the current source pass the existing regression suite and package checks?
2. For an identical change to one Concepts row, how do full-file and section-level record workflows differ in transmitted content and local execution time?
3. Which reported renderer failures are rejected at each historical implementation checkpoint, and what is the local cost of the added checks?
4. In a small real-model test, does the updated skill preserve teaching/record quality, use section updates, and produce a usable original mock exam? What are its actual reported resource differences?

Baseline source: `0dc295bf7fc9f6bc614f659d819676bf0a53b6de` (main immediately before PR3).
Candidate source: `97be1720f890745b3b59be52ad9ec3dea740393e` (PR3 merge; same tracked tree as `a1265ff`).
Both manifest versions remain 2.0.0; these are source checkpoints, not two separately published releases.

## Local record experiment

Use frozen helpers from the two commits, a three-section synthetic Markdown record, and histories of 10, 100, 1,000, and 5,000 rows. Change exactly one Concepts row while preserving all historical attempts and the Next session section.

- Baseline workflow: `read_record` followed by `commit_record` with the complete expected Markdown.
- Candidate workflow: `read_section("Concepts")` followed by `update_section(..., "upsert-rows", "Concept ID")` with one row.
- Construct the expected candidate bytes once before measurement, then give both workflows precisely that final-state requirement. This supplies a correct merge; it does not measure a model's ability to construct one.
- Run 30 repetitions per arm/size after one excluded warmup. Alternate baseline/candidate order by repetition; execute serially.
- Reset files and prepare submitted content before starting the timer. Time helper reads and helper writes separately with `perf_counter_ns`; the write includes hash/lock, backup, fsync, atomic replace, and verification.
- After every sample assert exact expected record bytes, exact prior-byte backup, and lock removal.
- Store all 240 samples. Report median, nearest-rank p95, minimum and maximum, with the environment and fixture size.

The payload proxy is supplied content UTF-8 bytes plus JSON read/write response bytes, excluding random backup paths. It excludes shell-command text, tool envelopes, system/skill instructions, reasoning, retries and model output. It is **not model tokens or billing**. Both helpers still rewrite a complete record and backup; this experiment does not establish lower disk writes. Timings use imported helpers in warm Python, not CLI startup or model latency. Local temporary-disk results need not match OneDrive or network storage.

The proxy assumes complete supplied/returned content at the helper boundary. A real tutor can instead merge the old full-file candidate with local Python and filter its printed output, avoiding transcription of all those bytes into a model tool call. Therefore even very large proxy reductions need not predict measured model-token reductions.

## Renderer experiment

Run five review reproductions at `dac1bad`, `a32e170`, `f019ba2`, `cccacaf`, and `a1265ff`: embedded iframe, tab-obfuscated javascript URL, SVG reserved ID, quoted-angle SVG reserved ID, and reserved question ID. Record accepted/rejected and error text. These 25 probes are known regressions, not a complete security assessment or an attack-success rate.

Time safe synthetic papers with 5, 25, and 100 questions, 30 repetitions each after one warmup, comparing first-renderer `dac1bad` with hardened `a1265ff`. This gives 180 trials. The pre-PR3 baseline has no renderer and is not assigned a fictitious rendering time. The renderer timing runs all first-renderer cells before all hardened cells; order is **not balanced**, and host drift limits fine speed comparisons. These measurements quantify checked-template overhead, not the cost of model-authored HTML.

## Real-model plan

Use the repository's existing `benchmark_record_cost.py` runner and `analyze_record_cost.py` analyzer, configured by `tests/benchmark_update.py --phase model --pairs 2`:

- Codex CLI 0.162.1; configured `gpt-6.1-sol`, medium reasoning; identical configuration in both arms.
- Two paired replicates, four turns per arm, 16 total model turns. Pair 1 starts baseline, pair 2 starts candidate; interleave by turn and run calls serially.
- Each arm has a separate continued session, isolated temporary configuration, frozen full skill directory, identical supplied packet/profile and a record with 100 explicitly synthetic historical attempts. Temporary login material is excluded from evidence.
- Turns 1-3 review Q1 (wrong full-sample denominator), Q3 (correct same-structure answer), and Q5 (correct same-structure answer), each with an explicit save request. Turn 4 requests a five-question original mixed-format HTML mock exam, separate checked key, final save and handoff. This is a save/artifact-heavy workload, not ordinary batching.
- Ordinary replies have an identical 120-180 word target; actual outputs and teaching are not forced identical. Tutor prompts do not include the evaluation rubric or intended result.
- Retain every completed call, failures, actual responses, per-turn record/profile snapshots, raw sanitized events, own-session accounting, frozen source and final generated files. Never select favorable runs or overwrite old reports.
- Verify session identity and establish whether `turn.completed` usage is cumulative against the session's `token_count` totals before aggregating. Derive per-turn differences only if that semantics holds; cached input is a subset, not an added token category.
- Review final records, assistance/progress calibration and generated questions/keys independently of the resource summary. A resource reduction without adequate output quality is not an equal-quality efficiency improvement.

The legacy runner names its candidate arm `v2`; here that means source `97be172`, not a new release. Its generic protocol string says "small initial record"; the actual archived initial record, 100-row construction above and measured byte count define this workload. The complete skill differs between arms, so no measured percentage can be attributed solely to section updates or solely to the template.

## Evidence, changes and limits

Keep source/input hashes, raw JSON samples, regression stdout/stderr, derived summaries, review notes, and a final SHA-256 manifest. Refresh the final manifest after all derived reports are written. Browser checks, if executed, are reported separately from DOM-stub tests. Absence of a model/build/browser capability is recorded as not performed, never as a pass.

Task changes consist of an opt-in benchmark runner, reports/evidence, and the user-required collaboration bootstrap. Product skill/helpers and published release ZIPs are frozen inputs and are not edited in this task. The canonical Chinese collaboration protocol receives a narrow exception in the repository's English-content validator; other package-language rules remain enforced.

No real learner gains, plugin auto-discovery, physical-device compatibility, accessibility certification, crash recovery, fee savings, or general course/model reliability can be inferred from this small synthetic test.

## Execution deviation retained

The original 16-call batch completed 15 calls and hit a service usage limit on the last. End-only artifact capture in the inherited runner lost temporary generated files; raw events and record snapshots survive. After an explicit continuation, one separate eight-call BA recovery pair ran November 12 using the same frozen inputs and per-call capture. Neither the failure nor any retry was discarded. See [FAILURE-AND-RECOVERY.md](FAILURE-AND-RECOVERY.md); report the original complete pair and recovery pair separately rather than silently pooling cross-window latency. The maintained runner now also has failure-retention and snapshot-synchronization regressions. No product code was changed.
