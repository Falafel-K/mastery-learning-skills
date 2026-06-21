---
name: handoff
description: 瞬间打包并压缩当前会话的进度、得分与笔记路径，生成交接文本供下个 Agent 恢复。(Handoff active session state into a compact block for state restoration.)
license: MIT
compatibility: Markdown-capable agent.
---

# Handoff Command Router

Pack active session state by invoking the core `mastery-learning-obsidian` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions and references of the `mastery-learning-obsidian` skill.
2. Trigger the `/handoff` command of the `mastery-learning-obsidian` skill to produce a compact resume state: topic, current objective, scores, evidence, open errors, next task, sources, and exact note paths.
