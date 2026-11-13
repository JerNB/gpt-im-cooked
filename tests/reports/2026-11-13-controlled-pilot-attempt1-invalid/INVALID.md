# Attempt 1 — invalid, kept as a harness-defect record

All three arms ran turns 1-6 with `sandbox_mode="workspace-write"` and no Windows
sandbox configured. Codex CLI 0.162.1 on Windows rejected every shell command
("blocked by policy"), so no arm could read `materials/`, and arm B never loaded
`skill/SKILL.md`. Every arm answered from general knowledge and asked the student
to paste the files. The responses therefore compare nothing and are not scored.

Fix verified with a one-call probe: adding `-c windows.sandbox="unelevated"`
lets the model read files in the workspace. Phase 2 was never run; copied
credentials were deleted from the work directory.
