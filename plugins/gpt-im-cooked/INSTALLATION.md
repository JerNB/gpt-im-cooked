# GPT, I'm Cooked plugin

Extract this entire `gpt-im-cooked` folder, including hidden directories.
It contains the plugin, both skills, and its own local marketplace catalog.

Open this extracted folder as a project in a supported desktop client. Refresh
the Plugins Directory or restart the client if needed, choose **GPT, I'm Cooked**,
and install **gpt-im-cooked**. Run its setup entry or start a new chat with:

```text
Use $gpt-im-cooked to help me prepare for my exam.
Here are my course notes and practice paper.
```

If your CLI exposes `codex plugin marketplace --help`, register the extracted
folder from its terminal with `codex plugin marketplace add .` and install
through the desktop Plugins Directory. Older CLIs without this command cannot
register a marketplace this way; use a supported desktop client or the standalone
skill download. Registration alone is not installation.

This plugin needs no connected service or API key. Its getting-started skill is
`gpt-im-cooked-start`; ordinary studying uses `gpt-im-cooked`.

Version 0.5.0 starts concept review in English conversation. Mock exams default
to HTML exam worksheets with separate keys; study guides default to PDF when
the host supports generation. Interactive pages for selected concepts are
optional, and explicit language or format requests override the defaults.

If you installed the former `exam-loop` plugin, the new ID is a replacement,
not an automatic update. Preserve your study folder, install this package,
and disable the old copy to avoid duplicate workflows. Standalone skill users
keep the same `$gpt-im-cooked` name. Neither installation route migrates or
deletes student records.

[Full instructions](https://github.com/JerNB/gpt-im-cooked/blob/main/docs/INSTALLATION.md)
 · [Real study examples](https://jernb.github.io/gpt-im-cooked/examples/)
