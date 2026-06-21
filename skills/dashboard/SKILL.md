---
name: dashboard
description: 展示当前学习进度的可视化看板，包括知识地图状态、掌握度分布与 ASCII 进度条。(Display the visual mastery learning progress report dashboard.)
license: MIT
compatibility: Markdown-capable agent.
---

# Dashboard Command Router

Display the progress dashboard by invoking the core `mastery-learning-obsidian` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions and references of the `mastery-learning-obsidian` skill.
2. Trigger the `/dashboard` command of the `mastery-learning-obsidian` skill to read the local ledger and render the progress report (including ASCII progress bars and status counts) in the chat window.
