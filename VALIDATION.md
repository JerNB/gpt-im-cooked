# Validation status

Version 0.4.1 — source and distribution checked October 11, 2026. The model-run evidence below belongs to v0.3.0 instruction snapshots; it was not rerun for the state update.

The v0.4.1 state update adds an optional Python 3.10+ write helper, import identity/revision guidance, a record import ledger, versioned session/attempt exports, pre-key snapshots, and strict package file boundaries. New helper and Node demo-script regressions are recorded in [STATE.md](tests/reports/2026-10-11/STATE.md). These are mechanical checks; the new [state pilot](tests/STATE-PILOT.md) has not been run against a fresh tutoring model. No database, automatic import service, multi-file transaction, or draft persistence is added.

The v0.4.0 update unifies plugin/skill naming, streamlines the review workflow, removes duplicated onboarding instructions, and fixes the downloaded plugin's marketplace layout. Both new ZIPs are extracted and compared with the maintained source; setup, icon, and resource paths resolve. A reproducible package builder is now included. See the [cleanup report](tests/reports/2026-10-11/CLEANUP.md). The local npm CLI is 0.94.0 and does not expose plugin marketplace subcommands; desktop installation remains unverified.

The v0.3.1 update adds an original exam-style demo, separate solutions and source packet, a project landing page, refreshed branding, and downloadable packages. See the [showcase checks](tests/reports/2026-10-10/SHOWCASE.md) for this revision's browser and package checks. The main skill now distinguishes independent mock exams from coached practice.

## Completed

- Both skills passed skill-creator's `quick_validate.py`.
- `python tests/validate_package.py` checks manifests, stable plugin identity, renamed skill, onboarding paths, prompts, YAML, SVG, relative links, English package content, and absence of personal absolute paths. It does not certify installation.
- Real model interactions ran in five isolated tutoring contexts: baseline v0.2 (3 turns), revised skill (5), onboarding/marker recovery (2), fresh resume and browser import (3), and a joint programming/astronomy request (1). These are synthetic requests, not classmates or actual course examinations.
- An independent reviewer assessed the first three turns without the author's conclusions. Both runs respected exclusions, source gaps, hints, ambiguous grading, and mastery restraint. Baseline unnecessarily retained temporary tiredness; revised omitted it. Live-record verification was partial in that review; the author separately inspected saved records and snapshots.
- Fresh-chat resume used saved files without earlier conversation history to produce a personalized guide. A thanks-only turn left the learning-record hash unchanged.
- The personalized HTML page was exercised in Chrome: blank/wrong answers, equivalent percentages/fractions, hints, reveals, retries, reset, provisional scoring, text export, and download. Downloaded JSON matched the visible export. Download-event capture timed out; filesystem verification confirmed the file afterward.
- Actual export import retained assistance across reset and caught a numerically correct response with wrong reasoning. Prior success remained preserved; page counters did not imply mastery.
- Keyboard Tab advanced between labelled fields. A narrow-viewport DOM measurement showed no horizontal overflow. Desktop layout was visually inspected. This is not a full accessibility or physical-mobile audit.
- `python tests/check_run_evidence.py` checks archived export equality, events, assistance, no-change evidence, markers, and selective retention. It does not rerun models.

See the [run report](tests/reports/2026-10-10/REPORT.md), [independent review](tests/reports/2026-10-10/review-first-three.md), and [evaluation method](tests/EVALUATION.md). The [original walkthrough](examples/DEMO.md) remains an authored illustration.

## Still to test

- Actual plugin installation, automatic discovery, and onboarding UI in target desktop clients. These runs explicitly loaded skill instructions.
- Repeated runs across model versions, more packets, unreadable/large PDFs, source conflicts, and all 22 fresh-chat pilot cases.
- Real student usability, independent learning gains, and delayed retention. Simulations cannot establish these.
- Physical mobile devices, cross-browser behavior, complete accessibility, and PDF/print layout.

No cloud sync, plugin-directory certification, or automatic browser-to-workspace writeback is provided. Students export page attempts and bring them to a tutor for reviewed record updates. The greeting is a workflow marker, not a context-capacity detector.
