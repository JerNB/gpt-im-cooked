# Installation

Version 0.5.1 keeps `gpt-im-cooked` for both the plugin ID and main skill. The getting-started entry is `gpt-im-cooked-start`. Choose one normal installation route to avoid duplicate workflows.

## Standalone skill: the simplest route

1. [Download the skill ZIP](downloads/gpt-im-cooked-skill-v0.5.1.zip).
2. Extract the entire `gpt-im-cooked` folder into `~/.codex/skills/`, or your configured `$CODEX_HOME/skills/`. Preserve an existing copy unless intentionally replacing it.
3. Refresh skills or restart the client if needed. In a new chat, bring a course file and send:

```text
Use $gpt-im-cooked to help me prepare for my exam.
Here are my course notes and practice paper.
```

The skill already includes the first-use guide and complete study workflow. Repository source is at `plugins/gpt-im-cooked/skills/gpt-im-cooked/`; copy the whole folder, including references, assets, and UI metadata. If installed skill discovery is unavailable, ask the agent to read the source SKILL.md and relevant supporting files for a manual preview.

## Plugin: bundled setup and listing

[Download the plugin ZIP](downloads/gpt-im-cooked-plugin-v0.5.1.zip) and extract its entire `gpt-im-cooked` folder, including hidden directories. This folder has its own `.agents/plugins/marketplace.json`, so it is also a local marketplace root.

Open the extracted folder as a project in a supported desktop client. Refresh the Plugins Directory or restart the client if needed, choose **GPT, I'm Cooked**, and install **gpt-im-cooked**. Run its setup entry or invoke `$gpt-im-cooked` in a new chat with your materials. Setup goes straight into the supplied task; the main skill supplies the same welcome when setup is not surfaced.

For clients with a plugin-capable CLI, first check `codex plugin marketplace --help`. If supported, register the extracted folder from its terminal:

```text
codex plugin marketplace add .
```

Then install through the desktop Plugins Directory. Registration is not installation. Older CLIs without a `plugin` command cannot use this command; use a supported desktop client or the standalone skill route. During this revision, the machine's npm CLI was 0.94.0 and did not expose plugin marketplace commands; actual desktop installation remains a separate check.

## Install from the repository

```text
git clone https://github.com/JerNB/gpt-im-cooked.git
cd gpt-im-cooked
```

The repository root has a catalog pointing to `./plugins/gpt-im-cooked`. Open that root as a desktop project, or register it with `codex plugin marketplace add .` when your CLI supports the command. A supporting CLI can also register `JerNB/gpt-im-cooked` directly. Keep the source folder accessible for local marketplace entries.

## Update from older versions

- Version 0.5.0 centers review on conversation and selected learning evidence. Mock exams default to HTML with a separate key, study guides default to PDF, and concept pages are optional. Explicit format requests still take precedence. Update the complete package so the new supporting references accompany the main skill.
- The standalone skill keeps the same `$gpt-im-cooked` invocation. Intentionally replace its full installed folder with the new version.
- The old plugin ID was `exam-loop`; 0.4.1 uses `gpt-im-cooked`. This is a replacement identity, not an automatic update of an installed old plugin. Preserve study files, install the new package, and disable the old copy to avoid duplicate workflows. The old `examloop-start` entry becomes `gpt-im-cooked-start`.
- The older `exam-review-coach` skill is another separate copy. Replace or disable it only when ready. No package update moves, clears, or uploads your course records.

## What the plugin contains

The plugin bundles the main skill, a small setup entry, manifests, listing prompts, an icon, and a local marketplace. It provides no AI server or connected service and requires no separate API key. Teaching, file writes, code execution, and PDF rendering use the host's available tools. Browser attempts are exported and reviewed by the tutor before a study record changes.

The manifests and catalogs follow the [official OpenAI plugin packaging documentation](https://developers.openai.com/plugins/build/plugins). A GitHub download is a local preview, not a universal-directory listing. An automatic installation pop-up is not guaranteed; the host supplies setup UI and the skill has a first-use fallback.
