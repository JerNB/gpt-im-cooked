---
name: gpt-im-cooked-start
description: Show the getting-started guide for the GPT, I'm Cooked plugin after installation or when a student asks how to begin, what materials to bring, or how to use its review workflow.
---

# Start GPT, I'm Cooked

Read [the main skill](../gpt-im-cooked/SKILL.md) and its [first-use guide](../gpt-im-cooked/assets/first-use.md). Follow the main skill's greeting, course boundary, record rules, and start/resume behavior; this entry point does not define a second tutoring workflow.

For a setup-only request, show the concise welcome and optional starter prompt, then ask for the course and one available material. With a supplied task or attempt, shorten the introduction and immediately do that work. Respect existing progress and record `Quick start shown` only when the welcome was actually shown.

The host can invoke this packaged entry point through its setup UI. Do not promise an automatic installation pop-up. The main skill supplies the same welcome if this entry point is not surfaced. No separate account, API key, or connected service is required by this skills-only plugin.
