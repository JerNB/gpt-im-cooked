# Post-PR3 test and benchmark report

Started November 11 and continued November 12, 2026 (America/New_York). Raw timestamps are UTC.

**Synthetic engineering evaluation. No measured learning, billing, or general reliability claim.**

## Changes under test

Baseline: `0dc295bf7fc9f6bc614f659d819676bf0a53b6de`. Candidate: `97be1720f890745b3b59be52ad9ec3dea740393e` (PR3 merge, same tracked tree as `a1265ff`). Both source checkpoints declare package version 2.0.0; existing published archives remain unchanged.

- Mock exams: JSON-to-template rendering, separate answer key, mixed question types, versioned filenames, stable export identities and exposure-aware history.
- Records: section read/replace/append/upsert, composite ledger keys, whole-file conflict hash, lock, prior-byte backup and verified atomic write.
- Review fixes: dangerous SVG/URL handling, complete-page ID checks via HTMLParser, code-fence/section integrity, unsaved exposure/history warnings.

See [the full method](METHOD.md), [local protocol/environment](protocol-local.json), [raw samples](local-results.json), and [derived distributions](local-summary.json).

## Regression checks

| Command | Exit code | Wall seconds | Raw log |
|---|---:|---:|---|
| `python -B tests/check_state_io.py` | 0 | 0.305 | [log](regressions/01-check_state_io.txt) |
| `python -B tests/check_mock_render.py` | 0 | 0.301 | [log](regressions/02-check_mock_render.txt) |
| `python -B tests/check_run_evidence.py` | 0 | 0.044 | [log](regressions/03-check_run_evidence.txt) |
| `python -B tests/check_evidence_archive.py` | 0 | 0.160 | [log](regressions/04-check_evidence_archive.txt) |
| `python -B tests/validate_package.py` | 0 | 0.510 | [log](regressions/05-validate_package.txt) |
| `node tests/check_mock_template.cjs` | 0 | 0.119 | [log](regressions/06-check_mock_template.txt) |
| `node tests/check_demo_state.cjs` | 0 | 0.050 | [log](regressions/07-check_demo_state.txt) |
| `node tests/check_concept_retry.cjs` | 0 | 0.050 | [log](regressions/08-check_concept_retry.txt) |
| `node tests/check_evidence_chain.cjs` | 0 | 0.066 | [log](regressions/09-check_evidence_chain.txt) |

9 scripts executed; 0 nonzero exits. Script counts are not individual assertion counts.

## Record workflow benchmark

240 measured workflows; 30 samples per arm/size, plus excluded warmups. Both arms produce byte-identical final records and prior-byte backups.

| History rows | Initial bytes | Full payload bytes | Section payload bytes | Payload reduction | Full median / p95 ms | Section median / p95 ms |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 2,184 | 4,612 | 642 | 86.080% | 3.721 / 4.683 | 4.046 / 4.930 |
| 100 | 18,384 | 37,102 | 642 | 98.270% | 3.708 / 4.562 | 4.204 / 5.095 |
| 1,000 | 180,384 | 362,002 | 642 | 99.823% | 4.459 / 7.095 | 6.033 / 10.438 |
| 5,000 | 900,384 | 1,806,002 | 642 | 99.964% | 11.495 / 16.523 | 19.807 / 32.431 |

**Interpretation:** section updates reduce the content transmitted for this one-row change. They do not reduce whole-record/backup disk writes. Extra section parsing and integrity checks can make local helper execution slower; read/write phase timings are retained in the raw samples. Payload bytes are not measured tokens, model latency, or fees.

## Renderer timings and known-defect probes

| Questions | First-renderer median ms | Hardened median ms |
|---:|---:|---:|
| 5 | 2.149 | 3.702 |
| 25 | 5.279 | 15.828 |
| 100 | 15.488 | 69.710 |

180 trials. The comparator is first-renderer `dac1bad`, because pre-PR3 source has no renderer. Hardened checks add local work. Timing order was first-renderer then hardened, not interleaved; host drift is a limitation. No model-generation speed claim follows.

| Probe | dac1bad | a32e170 | f019ba2 | cccacaf | a1265ff |
|---|---|---|---|---|---|
| svg_embedded_document | accepted | rejected | rejected | rejected | rejected |
| svg_tab_url | accepted | accepted | rejected | rejected | rejected |
| svg_reserved_id | accepted | accepted | accepted | rejected | rejected |
| svg_quoted_angle_id | accepted | accepted | accepted | accepted | rejected |
| question_reserved_id | accepted | accepted | rejected | rejected | rejected |

Accepted/rejected describes validator behavior, not executed browser exploitation. These are five known reproductions, not an exhaustive security test.

## Real-model comparison

**Original batch incomplete:** 15/16 calls completed; the final baseline call hit a service usage limit. Failed-call usage and duration are not estimated. All original logs remain; unequal-length pair 2 is not pooled. See [failure and recovery](FAILURE-AND-RECOVERY.md) and [original measured data](original-batch-summary.json).

| Original complete pair 1 only | Baseline | Candidate | Reduction |
|---|---:|---:|---:|
| total_tokens | 808,129.000 | 912,026.000 | -12.86% |
| wall_seconds | 283.493 | 231.684 | 18.28% |

Original transient exam files were not retained by the legacy end-only capture. Six HTML capture-loss notices are explicitly not original artifacts; record aliases are exact copies of the last available snapshots. The separate recovery below retains generated files and is not a replacement for this failure. Cross-window latency is not pooled.

**Separate batch: model-recovery.** Configured model: gpt-6.1-sol, reasoning medium, CLI codex-cli 0.162.1. 1 paired replicates, 4 continued turns per arm, 8 completed calls; first arm v2, serial turn-interleaving. Three forced saves followed by a mock-exam/save/handoff request. The legacy arm name `v2` means the candidate source, not a newly published version.

| Metric | Baseline | Candidate | Reduction (negative = increase) |
|---|---:|---:|---:|
| total_tokens | 980,574 | 852,170 | 13.09% |
| input_tokens | 969,194 | 842,364 | 13.09% |
| cached_input_tokens | 923,136 | 782,592 | 15.22% |
| uncached_input_tokens | 46,058 | 59,772 | -29.78% |
| output_tokens | 11,380 | 9,806 | 13.83% |
| wall_seconds | 332.589 | 268.392 | 19.30% |
| command_execution_items | 18 | 13 | 27.78% |

| Pair / arm | Total tokens | Wall seconds | Changed-record turns |
|---|---:|---:|---|
| 1 / baseline | 980,574 | 332.589 | [1, 2, 3, 4] |
| 1 / v2 | 852,170 | 268.392 | [1, 2, 3, 4] |

| Pair | Total-token reduction | Wall-time reduction |
|---:|---:|---:|
| 1 | 13.09% | 19.30% |

Raw [usage and wall times](model-recovery/results.json), [derived per-turn differences](model-recovery/summary.json), [configuration](model-recovery/protocol.json), [identical prompts](model-recovery/prompts.json), and [initial record](model-recovery/initial-learning-record.md) are archived. The generic inherited protocol description calls the record small; this experiment explicitly adds 100 historical rows. Use its actual bytes and METHOD.md to interpret the workload.

**Quality must be checked before claiming an improvement:** [independent quality review](QUALITY-REVIEW.md). Lower resource use is not automatically equal-quality savings. Whole-skill changes, generated artifact size, command choices, caching, output length, server load and latency all contribute. Two pairs of one packet cannot establish general reliability or causality.

## Validation and evidence limits

- Independent method review: [METHOD-REVIEW.md](METHOD-REVIEW.md).
- Browser evidence and package checks, if executed: [VERIFICATION.md](VERIFICATION.md). DOM-stub regressions are not browser layout verification.
- This task adds a reproducible opt-in runner, raw evidence and reports. It also installs the missing canonical collaboration entries/protocol and ignore rules as required by the human; the English-content validator exempts only that canonical protocol alongside the existing original student artifact.
- The benchmark runner was corrected to capture failures and per-call workspaces, with deterministic fake-CLI regression tests. No product skill/helper, manifest version or published ZIP is modified.
- No learner gains, dollar/subscription savings, compaction savings, automatic plugin discovery, physical-device support, accessibility certification, or broad course/model reliability was measured.

## Reproduction

```text
python tests/benchmark_update.py --phase local --output <new-report-directory> --repeats 30
python tests/benchmark_update.py --phase model --output <same-report-directory> --pairs 2
python tests/benchmark_update.py --phase model --output <same-report-directory> --pairs 1 --model-directory model-recovery --start-arm v2
python tests/benchmark_update.py --phase report --output <same-report-directory>
```

The model phase uses current login/quota. Existing result files are refused. The report phase reads archived measurements and makes no model calls. Preserve existing evidence; independent review files are not generated by the report command.
