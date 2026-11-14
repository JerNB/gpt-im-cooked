# Attempt history and evidence boundaries

Agent: codex. Real model calls were explicitly authorized by human, including continuing after the quota window reset. All benchmark tutoring calls use `gpt-6.1-sol`, medium effort, Codex CLI 0.162.1. Review-agent calls are separate from the tutoring benchmark.

## Initial attempt

The root-level `runs/` directory contains 13 completed calls: A1-S-rep1 turns 1–6, A2-S-rep1 turns 1–6, and B-S-rep1 turn 1. Shell execution failed with `registered Core process has no package identity`; neither materials nor the requested skill were read. The original gate incorrectly accepted attempted commands/agent text as evidence of reading. This attempt is invalid and must not be scored as a product comparison. No later session is spliced onto it.

## Core routing and global skill discovery

The `restart/` attempt removed three inherited desktop-routing environment variables from the child CLI, retaining workspace-write and Windows unelevated sandbox settings. A fixed-content local-file probe succeeded. A stronger gate now requires a successful content-reading command and nonempty output; merely listing files, attempting a command, or claiming to read is insufficient.

At 133 completed call-metadata files, the A2-P-rep2 raw events revealed a read of the user-global installed tutoring skill and references. `CODEX_HOME` isolation and `--ignore-user-config` did not disable user-global skills. All active runners and descendants were stopped; the remaining eight copied auth files were removed. This whole attempt is invalid as a controlled comparison. This observation does not establish that every earlier baseline read a global skill.

The next probe disabled 61 discovered external SKILL.md paths using per-call `skills.config` selectors and disabled bundled skills. Its session record contained no tutoring-skill reference and the local read succeeded. Subsequent benchmark calls use these selectors in all arms, plus an external-skill command audit. Global installed skill files were not edited. A later full-child-environment-cleanup probe also read its file after a pending command; it was diagnostic only, and does not establish that broader environment cleanup caused the recovery.

## Isolated attempt and quota

`isolated/` retains the next full experiment. Three sessions failed because the service explicitly reported a usage limit: C-S-rep1 turn 11, B-S-rep2 turn 7, and B-P-rep2 turn 7. Failure logs, executed commands, partial snapshots, and null completed-call usage are retained; unknown failed-call usage is not estimated.

After the stated reset time and human's instruction to continue, four sessions whose phase 1 had completed without a failure resumed their original contexts for phase 2. Each of the three failed sessions was rerun from turn 1 in its own labelled `recovery-*` report/work directory. Recovery answers address each new session's own turn-6 question. Successful recovery calls never replace the old raw failed-call files.

Resource data spans different quota windows and host-tool delays. Report per-session/per-window values; do not silently pool latency as a skill-only effect.

## Frozen S packet correction

The post-run byte audit found that the original PowerShell extraction converted all seven frozen S files from LF to CRLF. Their normalized text matched Git exactly, but their bytes did not match the supplied pilot fingerprints. Codex disclosed this preparation error. These S calls and their provisional blinded scores are retained as diagnostic evidence, not the final frozen-S sample.

`frozen-packet-s-git/` was extracted using `git archive` and byte writes. All seven original files match both the Git blobs and the pilot's SHA-256 values exactly. The additional rubric-v2 file is the pre-run M1/M11–M15 extension already frozen earlier. Commit `b549566` records the corrected inputs before new S calls. The eight S sessions are rerun in `exact-S/`, using the same model, CLI, prompts and frozen skills, with the two opposite arm orders.

P was authored and frozen before its first model call. Its actual fixture fingerprints are preserved in each protocol/results file. P's eight complete valid isolated/recovery sessions are retained; they are not rerun or replaced because of the S-only extraction issue.

## Final selection rule

Select all eight byte-exact S sessions from `exact-S/runs/`. Select the eight P sessions from `isolated/runs/`, except B-P-rep2, which comes wholly from `recovery-B-P-rep2/runs/`. Every selected session must have eleven complete call records, successful turn-1 material/skill gates as applicable, and no external-skill command. Keep every excluded attempt, its reason, and its measured resource use separately. No percentages, significance claims, billing claims or learning-gain claims are inferred.
