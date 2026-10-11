# v0.4.0 skill and plugin cleanup

The main skill now presents the review flow in six stages with shared course-grounding, evidence, and continuity rules. Detailed record, practice, and artifact guidance stays in conditional references. The setup skill delegates to that main workflow instead of repeating it.

## Distribution changes

- Plugin identity and source directory: `gpt-im-cooked`; main skill: `gpt-im-cooked`; setup skill: `gpt-im-cooked-start`.
- Repository marketplace resolves `./plugins/gpt-im-cooked`. Downloaded plugin marketplace resolves `./` from its extracted plugin folder. Both point to actual packaged files.
- Portable and compatibility manifests share identity, version, listing, prompts, and setup path. Existing listing prompt values/order are preserved.
- `scripts/build_packages.py` builds both ZIPs from the maintained source. Hidden catalog/compatibility files and every skill resource are included; student records and public examples are excluded from installed packages.
- Existing plugin ID `exam-loop` requires an intentional replacement install; this change does not rewrite or migrate any student's study folder. The standalone main skill retains its invocation.
- The original study artifacts and archived evaluation wording remain unchanged. One archived transcript hyperlink is pinned to the preceding v0.3.0 source commit because its old relative path was removed.

## Verification

Both skills pass skill-creator's quick validator using Python UTF-8 mode. The package validator checks manifests, catalogs, UI metadata, icons, and links. `tests/check_distribution.py` extracts each ZIP into a temporary directory and compares all files with the maintained source, then resolves setup, icons, references, and the standalone resource paths.

The builder is run twice and archive hashes compared to check reproducibility. Package files are checked for stale active names; old names occur only in migration guidance. Existing historical downloads remain available at their previous URLs.

These are source and distribution checks. The machine's npm Codex CLI is 0.94.0 and lacks plugin marketplace subcommands; a `--help` probe confirmed this limitation. This revision does not claim desktop installation, automatic discovery, setup UI, or fresh model behavior was tested. The earlier v0.3.0 model runs remain historical evidence.

Package behavior follows the [official OpenAI packaging and onboarding guide](https://developers.openai.com/plugins/build/plugins) and [manifest field reference](https://developers.openai.com/plugins/deploy/submission).
