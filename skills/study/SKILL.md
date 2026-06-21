---
name: study
description: 启动 Obsidian 互动式掌握学习系统中的学习闭环，开展指定知识点的学习与评估。(Start an interactive study session for a specific target in the mastery learning system.)
license: MIT
compatibility: Markdown-capable agent.
---

# Study Command Router

Start a deliberate learning session by invoking the core `mastery-learning-obsidian` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions and references of the `mastery-learning-obsidian` skill.
2. Trigger the `/study` command of the `mastery-learning-obsidian` skill, passing along any arguments provided by the user (such as specific knowledge point Kxx or keywords).
3. If no target was specified, proceed with the automatic next objective as defined by the core study protocol.
4. **Strict File-Write Boundary**: You MUST operate in Preview Mode and output Markdown in the chat window only, WITHOUT creating or writing any files on the filesystem, UNLESS the user has explicitly provided a target Obsidian Vault path in their prompt. Do not write to the project workspace root by default.
