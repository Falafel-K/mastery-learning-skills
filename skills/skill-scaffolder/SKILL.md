---
name: skill-scaffolder
description: Scaffold a new agent skill based on user requirements. Use when the user requests to create, scaffold, or generate a new Agent Skill, or enters the /create-skill command.
license: MIT
compatibility: Markdown-capable agent; local filesystem access for skill folder generation.
---

# Skill Scaffolder (技能脚手架生成器)

Automate the scaffolding of new agent skills. Enforce predictability, clear triggers, and checkable completion criteria while keeping user cognitive load to a minimum.

## 3-Question Grilling & Frictionless Direct Generation (三问提议与免问跳过)

When the user enters `/create-skill` or requests a new skill:
1. **Proactively Evaluate and Skip (主动评估与跳过)**:
   - Before asking any questions, analyze the user's initial description and technical level.
   - If the user's description is very simple, or they appear to be a non-technical end-user who would find technical/hardcore questions (e.g., trigger commands, observable output, write directories) difficult or frustrating to answer, **the Agent MUST skip the 3-question grilling completely**.
   - Directly state the inferred design parameters (slugified name, trigger commands, and target folder) and proceed straight to scaffolding to minimize user cognitive load.
2. **Offer Grilling with Clear Fallback (提问时明示退路)**:
   - If the user's request is technical and design choices need clarification, the Agent may ask exactly 3 key questions:
     - **Q1 (触发场景与激活方式 / Trigger Scenario)**: 这个技能在什么情况下应该被激活？是用具体的 Slash Command（如 `/my-cmd`）手动触发，还是在特定任务时由 AI 自动调用？
     - **Q2 (核心产出与完成标准 / Observable Output)**: 这个技能的终极可观察产出是什么？AI 如何判断该技能的任务已彻底完成（Checkable Completion Criteria）？
     - **Q3 (写操作与外部依赖 / Writes & Dependencies)**: 它是否需要读写本地文件？是否需要运行本地脚本？如果有，写操作是否需要限制在特定目录？
   - **Crucial Rule**: When asking these questions, the Agent MUST append a prominent instruction: *"如果您不确定或不便回答，可直接回复“默认”或“直接生成”，我将根据您的描述自动为您推导并生成骨架。"*
3. **Handle Confusion or Inability to Answer**:
   - If the user responds with "默认", "直接生成", "skip", "I don't know", expresses confusion, or fails to answer the technical questions clearly, **immediately stop the interview**.
   - Use smart defaults and context analysis of the user's initial description to **infer all 3 answers autonomously**, and proceed directly to scaffolding.
4. Once the details are gathered or inferred, proceed directly to scaffolding.

## Scaffolding Steps

1. **Sanitize Skill Name**: Convert the target skill name to lowercase, dash-separated folder format (e.g. `git-guardrails`).
2. **Create Folders and Base Templates Natively**: Use your native filesystem tools (like write, make directory, etc.) to create the folder `skills/<slugified-name>/` and create the base file `skills/<slugified-name>/SKILL.md` using the template layout defined in step 3. Do not run any external Python helper scripts to do this.
3. **Draft the Skill Instructions**: Write the detailed instructions inside the newly created `skills/<slugified-name>/SKILL.md` file:
   - Include clear frontmatter (name, description, license, compatibility).
   - Define checkable, exhaustive **Completion Criteria** at the end of each step.
   - Separate ordered actions (steps) from static rules (reference).
4. **Auto-Run Validation (AI Self-Testing)**:
   - Run the local package validator on the new skill:
     ```bash
     python tools/validate_skill_package.py --skill-dir "skills/<slugified-name>"
     ```
   - If the validator reports any errors, fix the generated `SKILL.md` file and re-run the validation until it passes.
5. **Present Preview Artifact**: Show the created skill's name, description, commands, and a confirmation of validation success to the user for final approval.

## Completion Criteria

- The new skill directory `skills/<slugified-name>/` exists.
- The `skills/<slugified-name>/SKILL.md` contains valid frontmatter matching the folder name.
- The package validator (`validate_skill_package.py`) executes successfully on the new directory.
