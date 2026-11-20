# Smoke 1, invalid (harness defect)

The runner omitted `-c windows.sandbox="unelevated"`, so Codex CLI 0.162.1 on Windows blocked every shell command and the tutor could read neither the materials nor SKILL.md (calendar/New turn 1 stopped at the read gate after one model turn). Kept unscored as a harness-defect record; fixed in the next commit, with a fake-CLI assertion.
