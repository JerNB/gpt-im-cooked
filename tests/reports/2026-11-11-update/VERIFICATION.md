# Executed verification and acceptance

## Product regressions and packages

The initial local experiment executed nine existing scripts with zero nonzero exits; raw stdout/stderr and durations are in [local-results.json](local-results.json). Final verification additionally exercises the benchmark-capture regression and records individual outcomes in [verification-results.json](verification-results.json). Python syntax, whitespace, package and temporary distribution checks are recorded in the final verification evidence.

Published v2.0.0 archives are not rebuilt in place. Package validation includes the real repository reports; a narrow language exception covers the exact canonical collaboration protocol required by the human. No English-content or link checks are disabled for benchmark evidence.

## Independent browser checks

Used the preinstalled Python Playwright and Chromium **148.0.7778.96**, headless, on the two actual recovery-batch worksheets. No browser/package downloads or external services were required. See [browser results](browser/results.json), [key viewport results](browser/key-results.json), and [the reproducible worksheet harness](browser_check.py).

- **26 worksheet checks passed**: desktop 1280x900 and phone-like 375x900 document overflow; CSS zoom 150%; keyboard reaching a control; blank initial answers; actual downloaded schema 1.0 exports with five items; stable repeated-export attempt/session identity; no page JavaScript errors or HTTP requests. Candidate additionally exercises actual key-link opening, retry identity, preserved session/exposure and pre-key history.
- **Four independent key-page viewport checks passed**, 1280px and 375px for each key, with no page JavaScript errors.
- The browser harness initially failed to identify baseline's differently worded export action. DOM inspection showed both actual pages use `button#export`; the selector was corrected. This was a test-harness assumption, not a product failure.
- Screenshots were visually inspected for hierarchy and clipping. Candidate mobile entry has a long introduction before question 1; its numbered navigation provides a direct jump. The key blueprint uses a horizontally scrollable table at 375px; the document itself does not overflow. These are usability observations, not an accessibility certification.

| Artifact | Desktop | Phone-like viewport |
|---|---|---|
| Candidate worksheet | [1280px](browser/pair-1-v2-1280.png) | [375px](browser/pair-1-v2-375.png) |
| Baseline worksheet | [1280px](browser/pair-1-baseline-1280.png) | [375px](browser/pair-1-baseline-375.png) |
| Candidate key | [1280px](browser/pair-1-v2-key-1280.png) | [375px](browser/pair-1-v2-key-375.png) |
| Baseline key | [1280px](browser/pair-1-baseline-key-1280.png) | [375px](browser/pair-1-baseline-key-375.png) |

Synthetic browser responses are labelled as tests and saved only under `browser/`. They were not imported into any student's learning record. Emulated CSS viewport/zoom is not physical-device or native browser-zoom testing. Print rendering and full accessibility were not performed.

## Benchmark-framework regression

`python tests/check_benchmark_capture.py` uses a fake CLI and synthetic login fixture, not model quota. [Original RED evidence](framework-red.txt) shows lost output after failure. The corrected runner retains raw output, execution metadata and artifacts for quota, timeout and malformed-output paths; it refuses false completed results, excludes authentication, and synchronizes deleted drafts in its maintained `final-study` snapshot. Current GREEN output is under [final checks](final-checks/check_benchmark_capture.txt).

The actual recovery model process loaded the earlier additive-capture implementation, archived as [recovery-runner-executed.py](recovery-runner-executed.py). Its selected delivered papers and record snapshots were independently checked; no exact-complete-filesystem claim is made. The final synchronization correction is verified by the deterministic regression rather than an extra model rerun.

## Explicit non-claims

No configured type checker, lint suite or coverage threshold exists for this skills-only repository; Python syntax and whitespace checks are separate from type/branch coverage. No coverage percentage is invented. The observed quota failure remains part of the experiment. No security certification, economic saving, learner gain or broad model/course reliability is inferred.
