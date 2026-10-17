# Verification of the October 17 patch

## Six-phase report

| Phase | Result | Evidence and boundary |
|---|---|---|
| Build/distribution | PASS | Candidate ZIPs built by the existing builder; 13 skill / 20 plugin files match source byte-for-byte; extraction/link/metadata checks pass. |
| Types/syntax | Syntax PASS; static typing N/A | Modified Python files parse; JS scripts execute. No static type-check configuration exists for this skills/HTML repository. No type-safety claim. |
| Lint | Diff check PASS; dedicated linter N/A | git diff --check passes. No new linter dependency/configuration added. |
| Tests | PASS, with intentional preserved RED | Three JS test scripts pass; state/helper, historical evidence, new archive and package checks pass. The preserved legacy page intentionally fails its exposure assertion. |
| Security scan | No matches in scoped scan | Credential-pattern search used filenames-only output over examples/plugins/scripts/tests; rg exit 1 means no matching files, not a failing test. Not a security audit. |
| Diff review | Reviewed | Product behavior changes are the repaired page and two narrow references. Metadata/docs/packages identify v0.5.1. Most added files are frozen evidence, excluded from distributable ZIPs. |

See check-outputs.json for actual tool outputs and REPORT.md for semantic
adjudication. Neither a source grep nor a passing archive check proves a tutor
judgment correct. Main and onboarding skill-creator quick_validate.py checks also
pass with Python UTF-8 mode. Its initial host-default GBK read failed on existing
UTF-8 text; rerunning with `python -X utf8` passed without changing the validator
or skill content for that encoding issue.

The initial staged diff check treated original CRLF bytes as trailing whitespace.
Scoped .gitattributes rules preserve the evidence byte-for-byte and suppress
whitespace rewriting/diagnostics only for raw run/skill/legacy-fixture artifacts;
authored report paths recognize CRLF explicitly. The final default staged diff
check passes. A separate Git blob-hash comparison confirms all 213 indexed
evidence files match their original working-file bytes, preserving SHA evidence
across checkouts with different line-ending defaults.

JS test adapter/preparer coverage: 100% lines, 94.85% branches, 95.95% functions.
The dynamic HTML VM script is not instrumented by that coverage report. Runtime
tests exercise both wrong-first and correct-first feedback/retry paths, not
browser rendering, native downloads, real R execution, or all generated pages.

## TDD evidence

- RED: actual legacy script returns false for the second response's earlier
  reveal, despite the first response showing the solution. Captured before any
  repair in red.txt and legacy-replay-red.json; checkpoint `5d4b078`.
- GREEN: repaired example retains exposure and original response identity;
  check_concept_retry.cjs passes the same failing assertion and the additional
  correct-first path. See legacy-replay-green.json.
- No claim of a model RED/GREEN improvement: before and after import judgments
  were both 0/3 observed assistance failures. The extra instruction is a narrow
  evidence-cross-check clarification, not a measured accuracy gain.

## Candidate package fingerprints

| Package | SHA-256 |
|---|---|
| gpt-im-cooked-skill-v0.5.1.zip | 08f19d9b43f4d8251915b90a413b91cbbae61b55aa8373b21216aa426abc51bd |
| gpt-im-cooked-plugin-v0.5.1.zip | f00876bc4b3439c1e326255ddf9654bdf3cb15adac7da03f3543cc5bb195f85e |

Older versioned archives are preserved. Candidate files are local, not a
publication, installation, plugin discovery test, or migration of old pages.

## Unperformed external checks

Direct local-file browser inspection was blocked by browser URL policy and was
not bypassed. No new browser screenshots or rendering verification are claimed.
Teacher/TA blind adjudication, equivalent learner-form validation, real students,
delayed outcomes and a precisely exposed backend model build remain unavailable
to this run. Their absence is not converted into PASS.
