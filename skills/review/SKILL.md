---
name: review
description: 启动 Obsidian 互动式掌握学习系统中的复习闭环，开始对过期知识点进行检索式复习评估。(Start a retrieval review session for target knowledge points.)
license: MIT
compatibility: Markdown-capable agent.
---

# Review Command Router

Start a retrieval-practice review session by invoking the core `mastery-learning-obsidian` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions and references of the `mastery-learning-obsidian` skill.
2. Trigger the `/review` command of the `mastery-learning-obsidian` skill, passing along any arguments provided by the user (such as a specific knowledge point Kxx).
3. If no target was specified, start a review for all overdue points in the queue as defined by the core assessment protocol.
4. **Strict File-Write Boundary**: You MUST operate in Preview Mode and output Markdown in the chat window only, WITHOUT creating or writing any files on the filesystem, UNLESS the user has explicitly provided a target Obsidian Vault path in their prompt. Do not write to the project workspace root by default.
