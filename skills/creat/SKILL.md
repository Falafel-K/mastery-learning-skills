---
name: creat
description: 自动生成符合四大支柱（触发范式、降级容错、统一词汇、调试生态与写保护约束）的标准化 Agent 技能包结构。(Scaffold a new standardized agent skill folder.)
license: MIT
compatibility: Markdown-capable agent; local filesystem access for skill folder generation.
---

# Create Command Router

Automate the scaffolding of new agent skills by invoking the core `skill-scaffolder` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions of the `skill-scaffolder` skill.
2. Trigger the scaffolding workflow as defined by the core `skill-scaffolder` protocol, starting with the 3-question grilling or auto-inferring the design parameters.
3. Ensure the generated skill contains the four pillars, including the **Strict File-Write Boundary** (Rule 11) in its instructions.
4. **Strict File-Write Boundary**: You MUST operate in Preview Mode and output Markdown in the chat window only, WITHOUT creating or writing any files on the filesystem, UNLESS the user has explicitly provided a target Obsidian Vault path in their prompt. Do not write to the project workspace root by default.
