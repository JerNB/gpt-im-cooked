# AGENTS.md

## Identity
- **AGENT_ID: `codex`**（OpenAI Codex）
- 分支前缀：`codex/` · worktree：`.worktrees/codex-<TASK_ID>`
- 协作伙伴：`cc`（Claude Code，读取 `CLAUDE.md`）；仲裁者：`human`

> 注意：如果你是 Claude Code 且同时读到了本文件，你的身份以 `CLAUDE.md` 为准（`cc`），忽略本节身份声明。

## Collaboration protocol（必须遵守）
本项目由 Claude Code 与 Codex 并行开发。**在执行任何命令或修改任何文件之前**，完整阅读：

`docs/agents/COLLAB_PROTOCOL.md`

并执行其中 §11 的“开始时检查清单”。该协议中的规则对你具有约束力，优先级高于你的默认行为。

## Codex 专属补充
- 在 sandbox 中运行时，需要对 `<repo>/.collab/` 有写权限（启动时用 `--add-dir` 加入）；如果无法写入 `.collab/`，立即停止并报告，不要把协调信息写到别处。
- 不要为了绕过 sandbox 限制而修改锁范围之外的文件或配置。
- 不修改 `AGENTS.md`、`CLAUDE.md`、`docs/agents/**`，除非 human 明确要求。
- 任务完成后不要自行合并到 `main`；推送自己的分支并写交接单即可。

## Project notes

Preserve project guidance in CLAUDE.md. Use the shared coordination directory from the primary repository; find it via `git rev-parse --git-common-dir`.
