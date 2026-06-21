---
name: sync
description: 强制执行当前学习状态的同步，将本会话的学习记录安全写入到本地笔记库中。(Force synchronization of the learning state to the local notebook/Vault.)
license: MIT
compatibility: Markdown-capable agent.
---

# Sync Command Router

Synchronize the learning state by invoking the core `mastery-learning-obsidian` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions and references of the `mastery-learning-obsidian` skill.
2. Trigger the `/sync` command of the `mastery-learning-obsidian` skill to synchronize the active session state from the session log to the mastery ledger by modifying the local note files inside the designated `AI-MANAGED` zones.
3. **Strict File-Write Boundary**: You MUST operate in Preview Mode and output Markdown in the chat window only, WITHOUT creating or writing any files on the filesystem, UNLESS the user has explicitly provided a target Obsidian Vault path in their prompt. Do not write to the project workspace root by default.
