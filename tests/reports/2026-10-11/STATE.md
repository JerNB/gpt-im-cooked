# v0.4.1 state reliability update

Student records remain Markdown in the selected workspace. A packaged optional Python 3.10+ standard-library helper reads content plus SHA-256 and commits a separate candidate under an exclusive sidecar lock. It rejects stale hashes, writes via temporary-file replacement, preserves one prior backup, and verifies final bytes. Locks coordinate only cooperating writers; partial multi-file activities need tutor reconciliation. Interrupted writers can leave locks requiring inspection. It is not a grading or import service.

The state reference and template now track imported identities and review revisions. Repeated exports do not count as independent attempts; legacy formats require qualified identity checks. Original evidence and revised judgments remain separate. The demo declares schema 1.0, package 0.4.1 and artifact content 0.3.1, creates session/attempt identities, and captures answers immediately before opening the key. Retry retains exposure and old snapshots. Reload loses unexported work and starts a new session; the page explains this.

The builder validates an explicit file allowlist before writing either archive. Unexpected files and symlinks are rejected. Adding a legitimate resource requires updating that list. Installed packages contain the helper and templates, not student workspace records.

## Checks run

- `tests/check_state_io.py`: creation, no-change, backup, stale-writer rejection, lock preservation, invalid candidate rejection, simulated replacement failure, cleanup, and unexpected/missing package files.
- `tests/check_demo_state.cjs`: executes the actual demo script with a minimal DOM; checks pre-key original answers, immutable snapshots, stable repeated-export identity, new retry identity, retained exposure and blank retry answers. This is not a real-browser layout/download test.
- Both skills pass the skill quick validator.
- Package, extracted-distribution and historical-evidence checks; two temporary builds compared for reproducibility and agreement with maintained downloads.

The fresh-model scenarios in STATE-PILOT.md are pending. Existing v0.3.0 model and browser runs are historical evidence only. Desktop installation, automatic discovery, new browser downloads and student learning gains have not been retested.
