# Trigger & Invocation (触发与调用规范)

Mastery Learning 技能和命令在调用上严格区分为 **用户触发型 (User-invoked)** 与 **模型触发型 (Model-invoked)** 双轴。

## 1. 用户触发型 (User-invoked)
- **触发标志**：由人类显式键入指令（如 `/study`, `/review`, `/dashboard`, `/audit`, `/handoff`, `/sync`）。
- **说明规范**：技能 descriptions 面向人类，语言精炼，严禁在 `SKILL.md` 中写诱导 AI 自动加载的触发短语 (Trigger Phrases)。
- **写操作安全**：凡是涉及本地文件修改、状态重置的大型操作，必须由用户手动输入，严禁模型自主调用。

## 2. 模型触发型 (Model-invoked)
- **触发标志**：省略 `disable-model-invocation: true`，由模型根据上下文或任务自动调用。
- **说明规范**：description 包含 AI 的触发逻辑 (如 `Use when assessing learner answer...`)。
- **代表功能**：掌握度打分评估、认知修复重测、底层笔记物理写入。

## 3. 依赖传递规则 (Chaining Rules)
1. 用户触发型技能（如 `/study`）可以隐式调用模型触发型子功能（如掌握度评估与打分）。
2. 用户触发型技能之间**严禁隐式串联调用**（例如，AI 绝不能在学习测试后自动执行物理落盘的 `/sync` 命令）。
3. 跨主指令操作必须提示用户手动键入（如：*"本次掌握测试已通过，请手动运行 `/sync` 存盘。"*）。
