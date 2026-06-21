---
name: audit
description: 启动原始资料的覆盖度审计，核验每一处核心论断与知识点是否已被映射与评估。(Audit course source coverage against knowledge points.)
license: MIT
compatibility: Markdown-capable agent.
---

# Audit Command Router

Perform a coverage audit by invoking the core `mastery-learning-obsidian` skill.

## Trigger Instructions

When this command is triggered:
1. You must immediately load the instructions and references of the `mastery-learning-obsidian` skill.
2. Trigger the `/audit` command of the `mastery-learning-obsidian` skill to verify that every important source claim maps to a knowledge point, an assessment, and a current mastery state, reporting any gaps.
