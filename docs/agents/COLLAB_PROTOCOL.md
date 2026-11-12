# Multi-Agent Collaboration Protocol (Claude Code × Codex)

> 版本：1.0 · 适用对象：Claude Code（`cc`）、Codex（`codex`）、人类负责人（`human`）
> 本文件是两个 agent 共同遵守的**唯一规范**。`CLAUDE.md` / `AGENTS.md` 只声明身份并指向这里。

---

## 0. 优先级与基本原则

**优先级（从高到低）**：人类在对话中的直接指令 > 本协议 > 项目其他文档 > agent 自身默认习惯。

五条铁律（任何情况下都不得违反）：

1. **隔离**：每个 agent 只在**自己的 git worktree + 自己的分支**里改代码，绝不进入对方的 worktree。
2. **先认领，后修改**：动任何文件前，必须在 `.collab/LOCKS.md` 中持有覆盖该路径的锁。
3. **不覆盖他人工作**：发现非自己产生的改动，**停下并报告**，不得 revert、reset、checkout 覆盖或"顺手修复"。
4. **只通过文件沟通**：两个 agent 不直接对话，所有协调信息写入 `.collab/`；分歧由 `human` 裁决。
5. **不碰主干**：任何 agent 都不得直接提交、推送或强推 `main`；合并由集成者（默认 `human`）执行。

---

## 1. 身份

每个 agent 启动时从入口文件读取自己的 `AGENT_ID`：

| 入口文件 | AGENT_ID | 分支前缀 | worktree 目录 |
|---|---|---|---|
| `CLAUDE.md` | `cc` | `cc/` | `.worktrees/cc-<TASK_ID>` |
| `AGENTS.md` | `codex` | `codex/` | `.worktrees/codex-<TASK_ID>` |

所有写入 `.collab/` 的记录、所有 commit 都必须带上 `AGENT_ID`。

---

## 2. 角色分工

默认分工如下（`human` 可在 `.collab/TASKS.md` 顶部覆盖）：

| 职责 | 默认负责方 | 说明 |
|---|---|---|
| 需求拆解、任务建卡、验收标准 | `human`（可委托 `cc`） | 每张卡必须有可验证的 Done 条件 |
| 架构 / 接口设计、跨模块重构 | `cc` | 先写设计说明到任务卡，再动代码 |
| 功能实现、测试编写 | `cc` 与 `codex` 均可 | 按认领分配 |
| 代码评审 | **非作者的那一方** | 交叉评审，作者不得自审通过 |
| 合并到 `main`、解决合并冲突 | `human`（集成者） | 可授权某个 agent 担任，须在 TASKS.md 写明 |
| 依赖、构建、CI、全局配置 | 集成者 | 见 §5.3 热点文件 |

> 原则：**同一时间，同一文件只有一个 owner。** 分工按"模块/目录"切，而不是按"同一文件的不同函数"切。

---

## 3. 工作区隔离

### 3.1 目录布局

```
<repo>/
├── AGENTS.md                 # Codex 入口
├── CLAUDE.md                 # Claude Code 入口
├── docs/agents/COLLAB_PROTOCOL.md
├── .collab/                  # 协调状态（gitignored，两个 agent 共享读写）
│   ├── TASKS.md              # 任务看板
│   ├── LOCKS.md              # 文件锁表
│   ├── LOG.md                # 追加式事件日志
│   ├── handoff/<TASK_ID>.md  # 交接单
│   └── reviews/<TASK_ID>.md  # 评审意见
└── .worktrees/               # 各 agent 的独立工作树（gitignored）
    ├── cc-T003/
    └── codex-T004/
```

- `<repo>` 根目录（主 worktree）保持在 `main`，**只供人类与集成使用**，agent 不在这里改代码，只读写 `.collab/`。
- `.collab/` 不进 git，避免两个分支同时改看板产生冲突。需要留档时由 `human` 定期归档。

### 3.2 创建工作区（认领任务后执行）

```bash
# 在 <repo> 根目录
git fetch origin
git worktree add .worktrees/<AGENT_ID>-<TASK_ID> -b <AGENT_ID>/<TASK_ID>-<short-slug> origin/main
```

### 3.3 禁止事项

- 不得在主 worktree 执行 `git checkout` / `git switch` / `git stash` / `git reset`。
- 不得读写对方 worktree（`.worktrees/<对方ID>-*`）内的任何文件（只读查看也应通过对方已推送的分支）。
- 不得删除任何不属于自己的 worktree 或分支。

---

## 4. 任务生命周期

### 4.1 状态机

```
TODO ──claim──▶ CLAIMED ──start──▶ IN_PROGRESS ──submit──▶ REVIEW ──approve──▶ READY_TO_MERGE ──merge──▶ DONE
                                     │    ▲                   │
                                     ▼    │                   └─request changes──▶ IN_PROGRESS
                                   BLOCKED
```

### 4.2 规则

- 任务 ID 形如 `T001`，由建卡者分配，全局唯一递增。
- **认领**：只能认领状态为 `TODO` 且 `Owner` 为空（或指定给自己）的任务；同一 agent 同时 `IN_PROGRESS` 的任务 **≤ 2**。
- **认领三步（原子顺序）**：
  1. 重新读取 `TASKS.md` 与 `LOCKS.md`（不得使用会话早先读到的旧内容）；
  2. 确认无冲突后，在 `LOCKS.md` 写入锁，在 `TASKS.md` 把 Owner/状态改为自己；
  3. 再次读取两个文件，确认自己的写入仍在、且没有他人同时认领。若被抢占，撤回自己的写入并选择其他任务。
- 状态变化必须同步追加一行到 `LOG.md`。
- 遇到阻塞（需求不清、需要对方锁定的文件、环境问题）→ 状态改 `BLOCKED`，写明原因与需要谁做什么，然后停止该任务。

---

## 5. 文件锁

### 5.1 锁表格式（`.collab/LOCKS.md`）

```
| Path (glob)          | Owner | Task | Mode  | Since (ISO8601)      | Heartbeat            |
|----------------------|-------|------|-------|----------------------|----------------------|
| src/auth/**          | cc    | T003 | write | 2026-11-04T10:00+08  | 2026-11-04T11:20+08  |
| src/api/user.ts      | codex | T004 | write | 2026-11-04T10:05+08  | 2026-11-04T10:50+08  |
```

### 5.2 规则

- **粒度**：优先锁目录（`src/auth/**`），不要锁整个仓库（`**`）。新建文件也要被锁覆盖。
- **重叠即冲突**：任意两条 `write` 锁的 glob 有交集，后来者不得写入，必须 `BLOCKED` 并在 LOG 中请求协调。
- **Heartbeat**：持锁期间每完成一个阶段（或至少每 60 分钟）更新一次 `Heartbeat`。
- **过期**：Heartbeat 超过 **4 小时** 未更新视为陈旧锁。agent **不得自行抢占**陈旧锁，只能在 LOG 中标记 `STALE_LOCK?` 并请 `human` 处理。
- **释放**：任务进入 `READY_TO_MERGE` 或被放弃时，立即删除自己的锁行。
- 只能修改/删除 `Owner` 为自己的锁行。

### 5.3 热点文件（只有集成者可改，或需单独建卡并独占锁）

以下文件冲突代价高，**普通任务禁止修改**；如确需修改，在任务卡中写明，交由集成者处理或由 `human` 明确授权：

- 依赖清单与锁文件：`package.json`、`package-lock.json`、`pnpm-lock.yaml`、`requirements*.txt`、`pyproject.toml`、`poetry.lock`、`go.mod/go.sum`、`Cargo.toml/Cargo.lock` 等
- 数据库迁移目录（迁移编号必须串行）
- CI/CD、Docker、构建配置：`.github/**`、`Dockerfile`、`docker-compose*`、`tsconfig*.json`、`vite/webpack` 配置等
- 全局格式化/静态检查配置：`.eslintrc*`、`.prettierrc*`、`ruff.toml`、`.editorconfig`
- 协作文件本身：`AGENTS.md`、`CLAUDE.md`、`docs/agents/**`
- `.env*` 与任何密钥文件（agent 永远不得写入真实密钥）

---

## 6. 编辑规范

1. **改前重读**：编辑某文件前必须重新读取其最新内容，不得基于会话早期的缓存内容做替换。
2. **最小 diff**：只改任务需要的部分。禁止顺手重排 import、全文件格式化、批量改名、改换行符/缩进风格。
3. **不跨界**：发现锁范围外的 bug，不要修，写进任务卡的 `Follow-ups` 或新建 `TODO` 卡。
4. **移动/重命名/删除文件**：必须同时持有源路径和目标路径的锁，并在交接单中列出。
5. **公共接口变更**（导出的函数签名、API 契约、数据结构、DB schema）：先在任务卡写 `Interface Change` 说明，标记受影响模块；若受影响模块被对方锁定 → `BLOCKED` 等待协调。
6. **生成文件**（codegen、编译产物、快照）：不要手改；记录生成命令，由脚本重新生成。
7. **不留半成品**：会话结束前，代码必须处于能编译/能通过已有测试的状态，或明确在交接单中标注 `WIP` 与失败原因。

---

## 7. Git 规范

- **分支**：`<AGENT_ID>/<TASK_ID>-<short-slug>`，例：`codex/T004-user-profile-api`。
- **Commit 信息**：Conventional Commits + 任务号 + agent 尾注：

  ```
  feat(auth): add refresh token rotation [T003]

  <为什么这么改，一两句>

  Agent: cc
  ```

- 小步提交，一个 commit 只做一件事；禁止把格式化与逻辑修改混在同一 commit。
- **提交评审前**：`git fetch && git rebase origin/main`，本地跑通测试/lint，再推送自己的分支。
- 禁止：`git push --force` 到非自己的分支、推送 `main`、`git commit --no-verify`、修改他人 commit、`git clean -fdx`。
- 自己分支 rebase 后可用 `git push --force-with-lease`（仅限自己的分支）。

---

## 8. 交接单（`.collab/handoff/<TASK_ID>.md`）

任务进入 `REVIEW`、`BLOCKED`，或会话结束而任务未完成时，必须写/更新交接单：

```markdown
# Handoff T004 — <标题>
- Agent: codex          - Branch: codex/T004-user-profile-api
- Status: REVIEW | BLOCKED | WIP
- Updated: 2026-11-04T15:30+08:00

## 做了什么
- …

## 改动文件
- src/api/user.ts（新增 GET /users/:id/profile）
- tests/api/user.test.ts

## 如何验证
- `npm test -- user`  → 期望全部通过
- 手动：…

## 未完成 / 已知问题
- …

## 需要对方或人类做的事
- [ ] cc：评审 `src/api/user.ts` 的错误处理
- [ ] human：确认 profile 字段是否包含 email
```

---

## 9. 交叉评审

- 进入 `REVIEW` 的任务由**非作者 agent** 评审，结果写入 `.collab/reviews/<TASK_ID>.md`。
- 评审者**只读**被评审分支（`git fetch` 后 `git diff origin/main...origin/<branch>`），**不得直接在对方分支上提交修改**；需要修改时写成意见，由作者修改。
- 意见分级：
  - `BLOCKER`：正确性 / 安全 / 数据丢失 / 违反协议，必须修
  - `MAJOR`：应修，作者可说明理由拒绝，由 human 裁决
  - `NIT`：可选
- 评审清单：
  - [ ] 满足任务卡 Done 条件
  - [ ] 改动全部在作者锁范围内，无越界修改、无热点文件
  - [ ] 有对应测试，且测试真实覆盖新逻辑
  - [ ] 无秘密泄露、无调试残留、无注释掉的大段代码
  - [ ] 公共接口变更已记录并通知受影响方
- 无 `BLOCKER` → 状态改为 `READY_TO_MERGE`；否则退回 `IN_PROGRESS`。

---

## 10. 异常处理

| 情况 | 必须做 | 禁止做 |
|---|---|---|
| 工作区出现不是自己产生的改动 | 停止，记录 `git status`/`git diff --stat` 到 LOG，标 `BLOCKED` 通知 human | revert、reset、stash、覆盖 |
| 想改的文件被对方锁定 | `BLOCKED`，在 LOG 写明需要的路径与原因 | 偷偷改、复制一份绕过 |
| rebase 产生冲突 | 只解决**自己改动**引起的冲突；涉及对方逻辑的冲突 → 中止 rebase（`git rebase --abort`），交给集成者 | 用 `--ours/--theirs` 一刀切 |
| 测试失败且非自己引起 | 在 LOG 与交接单中报告失败用例与证据 | 删除/跳过/弱化测试让其通过 |
| 需求不清或两个 agent 意见冲突 | 写下两种方案及取舍，交 human 决定 | 擅自按自己理解推进大改 |
| 协调文件格式损坏 | 停止写入，报告 human | 整个重写 `.collab/` 文件 |

---

## 11. 会话检查清单

### 开始时（每次新会话都执行）

1. 读取本协议 → 确认自己的 `AGENT_ID`。
2. 读取 `.collab/TASKS.md`、`.collab/LOCKS.md`、`LOG.md` 最近 30 行、与自己相关的 `handoff/` 与 `reviews/`。
3. 确认当前目录是**自己的** worktree、分支名前缀正确：`git rev-parse --show-toplevel && git branch --show-current`。
4. `git status` 应干净或只有自己上次留下的已记录改动；否则按 §10 处理。
5. 优先处理：发给自己的评审意见 > 自己 `IN_PROGRESS` 的任务 > 待评审的对方任务 > 新任务。

### 结束时

1. 代码可编译或已标注 WIP；已提交并推送自己的分支。
2. 更新任务状态、锁 Heartbeat（或释放锁）、交接单。
3. 在 `LOG.md` 追加一行总结。

---

## 12. LOG 格式（`.collab/LOG.md`，只追加，不改历史）

```
2026-11-04T10:00+08 | cc    | T003 | CLAIM    | locked src/auth/**
2026-11-04T11:40+08 | cc    | T003 | SUBMIT   | → REVIEW, handoff/T003.md
2026-11-04T12:10+08 | codex | T003 | REVIEW   | 1 BLOCKER, 2 NIT → reviews/T003.md
2026-11-04T12:15+08 | codex | T005 | BLOCKED  | need src/auth/session.ts (locked by cc/T003)
```

动作枚举：`CLAIM` `START` `HEARTBEAT` `SUBMIT` `REVIEW` `APPROVE` `CHANGES` `BLOCKED` `UNBLOCK` `RELEASE` `MERGE` `NOTE` `STALE_LOCK?`
