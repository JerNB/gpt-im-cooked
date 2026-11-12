# Original-batch failure and recovery plan

The study started November 11, 2026 (America/New_York), and continued November 12 after the human asked to continue. Raw logs use UTC.

## Original batch: retained as incomplete

The planned 16-call, two-pair experiment completed 15 calls. Pair 2, baseline turn 4 exited after the service reported a usage limit. Four shell-command batches in that final turn completed, including synthetic question/key construction, but there was no completed tutor turn or final usage event. Its usage and exact end-to-end duration were not retained by the original runner and are not estimated.

The entire original raw event/error log and all 15 completed-call usage rows and record/profile snapshots remain under `model/`. No call is replaced or silently dropped. The [original-batch summary](original-batch-summary.json) reports only the balanced, complete pair 1 as a four-turn session comparison. Pair 2 has unequal completed lengths and is not pooled as a complete session comparison.

The inherited runner copied generated workspace files only after **all** calls completed. Temporary-directory cleanup therefore removed the original transient HTML/JSON files before this copy. This is a test-harness capture defect, separate from the service quota failure. Recorded authoring commands, successful computation/browser-check output, final replies and saved record snapshots survive, but exact delivered artifact bytes cannot be independently rerun from that original batch. Missing files are not reconstructed and passed off as originals.

For usable archive links, `learning-record.md` aliases copy each arm's last captured record snapshot without altering its bytes. Six missing HTML link targets instead contain prominently labelled **Artifact NOT RETAINED** notices, not recreated exams or keys. [capture-loss-index.json](capture-loss-index.json) records this provenance. These notices are excluded from artifact/browser acceptance and are not evidence that original files were retained.

## Framework correction

- Archive each completed or failed call's synthetic study workspace before temporary cleanup.
- Retain stdout/stderr before JSON parsing, including malformed and partial output.
- Write per-call start time, measured wall duration, return code and timeout status.
- Exclude the separate temporary login home from evidence.
- Add a deterministic fake-CLI regression: quota, timeout and malformed-output failures retain artifacts/logs but do not produce false complete results. The test failed on the original runner and passed after the fix; it uses a synthetic login fixture and no model calls.
- A follow-up review found additive mirrors could retain deleted drafts. The final runner synchronizes its non-skill `final-study` snapshot against an authoritative file inventory; the root evidence mirror remains cumulative. The regression verifies draft deletion.

The recovery process had already loaded the earlier per-call-capture implementation before the draft-deletion correction. Its archive is consequently treated as a **cumulative capture**, and independent browser checks select the delivered worksheet identified by the final reply. No claim of a byte-exact complete final filesystem is made for this batch. `recovery-runner-executed.py` preserves the implementation actually loaded; the final tested runner is maintained in `tests/benchmark_record_cost.py`.

## Separate recovery batch

After the quota reset and the human's continuation request, run one new eight-call pair under `model-recovery/`, starting candidate then baseline (BA). Use the same frozen source commits, packet, profile, 100-history-row initial record, four prompts, configured model and reasoning effort. This is an explicitly separate replication, not a replacement for the failed call or a resumption of deleted conversation state.

Report the original complete pair and recovery pair separately. Their time windows differ by roughly twelve hours, so do not silently pool cross-window latency. Review the captured recovery records/questions/keys independently, then rerun browser checks and save screenshots. Keep any new failure as a failure; do not loop until a favorable outcome appears.
