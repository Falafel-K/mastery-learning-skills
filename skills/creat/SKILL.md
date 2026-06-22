---
name: creat
description: 自动生成符合四大支柱（触发范式、降级容错、统一词汇、调试生态与写保护约束）的标准化 Agent 技能包结构。(Scaffold a new standardized agent skill folder.)
license: MIT
compatibility: Markdown-capable agent; local filesystem access for skill folder generation.
---

# /creat — Skill Scaffolder (技能脚手架生成器)

Automate the scaffolding of new agent skills. Enforce predictability, clear triggers, and checkable completion criteria while keeping user cognitive load to a minimum.

## Step 1 — 三问提议 vs. 免问直接生成 (3-Question Grilling vs. Frictionless Direct Generation)

When the user triggers `/creat` or requests a new skill:

### 1a. 主动评估，决定是否跳过提问
Before asking anything, analyze the user's description and apparent technical level:

- If the description is **very simple**, the intent is obvious, or the user appears to be a **non-technical end-user** who would find questions about trigger commands, observable output, or write directories frustrating to answer — **skip the 3 questions entirely**.
- State the inferred design parameters (slugified name, trigger command(s), target folder) in one short summary line, then proceed directly to Step 2 (Scaffolding).

### 1b. 如果需要提问，只问三个问题
If the user's request is technical and design choices need clarification, ask exactly these 3 questions in a single message:

- **Q1 (触发场景与激活方式 / Trigger Scenario)**: 这个技能在什么情况下应该被激活？是用具体的 Slash Command（如 `/my-cmd`）手动触发，还是在特定任务时由 AI 自动调用？
- **Q2 (核心产出与完成标准 / Observable Output)**: 这个技能的终极可观察产出是什么？AI 如何判断该技能的任务已彻底完成（Checkable Completion Criteria）？
- **Q3 (写操作与外部依赖 / Writes & Dependencies)**: 它是否需要读写本地文件？是否需要运行本地脚本？如果有，写操作是否需要限制在特定目录？

**Crucial Rule**: Always append this escape hatch to the 3-question message:
> 💡 如果您不确定或不便回答，可直接回复 **"默认"** 或 **"直接生成"**，我将根据您的描述自动推导并生成骨架。

### 1c. 处理"不知道"或"默认"回复
If the user responds with any of: `"默认"`, `"直接生成"`, `"skip"`, `"I don't know"`, expresses confusion, or fails to answer clearly — **immediately stop the interview**. Infer all 3 answers autonomously from the initial description and proceed directly to Step 2.

---

## Step 2 — 脚手架生成 (Scaffolding Steps)

Once the details are gathered or inferred, execute these steps:

1. **Sanitize Skill Name**: Convert the target skill name to lowercase, dash-separated folder format (e.g. `git-guardrails`).

2. **Strict File-Write Boundary (Rule 11)**:
   - **Default is Preview Mode**: Output the complete directory structure and all file contents as formatted Markdown in the chat window ONLY. Do NOT create or write any files on the filesystem unless the user explicitly provides a target folder path (e.g. `d:\MySkills` or `/home/user/skills`).
   - If a target path was explicitly provided: use your native filesystem tools (`write_to_file`, `run_command mkdir`, etc.) to create the folder and file physically. **Do not run external Python helper scripts**.

3. **Draft the Skill Instructions** in `skills/<slugified-name>/SKILL.md`, strictly enforcing the **Four Pillars**:
   - **Pillar 1 (Invocation)**: Define in YAML frontmatter whether it is User-invoked (slash command, manual trigger) or Model-invoked (autonomous, AI-triggered). User-invoked commands must be clearly labeled.
   - **Pillar 2 (Degradation)**: Specify operating modes (Full Mode → local writes; Chat-only Mode → preview + handoff). **Mandate Rule 11 (Strict File-Write Boundary) in the new skill** — no writes unless user explicitly provides a path. Reference `../../docs/adr/0001-mastery-storage-soft-degradation.md` for fallback behavior specs.
   - **Pillar 3 (Vocabulary)**: Include a required step to load the shared vocabulary in `../../CONTEXT.md` to avoid term mismatch.
   - **Pillar 4 (Checkability)**: Define checkable, exhaustive **Completion Criteria** at the end. Separate ordered actions (steps) from static rules (reference).

4. **Auto-Run Validation** (only applies in Full Mode when files were actually written):
   ```bash
   python tools/validate_skill_package.py --skill-dir "skills/<slugified-name>"
   ```
   If the validator reports errors, fix the generated `SKILL.md` and re-run until it passes.

5. **Present Summary**: Show the user the skill name, trigger command(s), description, output type, and confirmation of validation result (or a note that validation is skipped in Preview Mode).

---

## Completion Criteria

- [ ] Skill name is sanitized (lowercase, dash-separated).
- [ ] In **Full Mode**: `skills/<slugified-name>/SKILL.md` physically exists and passes `validate_skill_package.py`.
- [ ] In **Preview Mode**: Complete SKILL.md content is output to chat as formatted Markdown.
- [ ] All Four Pillars are present in the generated instructions.
- [ ] Rule 11 (Strict File-Write Boundary) is embedded in the new skill's instructions.
- [ ] User sees the summary and can copy/approve the result.
