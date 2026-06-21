# ADR 0001: Mastery Storage Soft Degradation (存储软降级决策)

## 状态
已通过 (Accepted)

## 上下文 (Context)
Mastery Learning 技能需要运行在多种环境下：
1. **Full mode**：具备物理文件系统读写权限（本地 Obsidian 笔记库）。
2. **Cloud mode**：网页端/云笔记本（Notion、飞书）。
3. **Chat-only mode**：无物理读写权限的会话框。
为避免“因无文件读写权限而报错阻断学习”，必须将学习核心逻辑与存储写入解耦。

## 决策 (Decision)
核心教学评估系统对物理存储为“软依赖 (Soft Dependency)”，提供三级退化方案：
1. **本地模式 (Full Mode)**：自动往 `03-掌握度账本.md` 中物理写入学习状态。写入范围仅限 `AI-MANAGED` 块，绝不破坏用户自有文字。
2. **云笔记本模式 (Cloud Mode)**：不执行物理写入。以 Markdown 代码块形式输出更新补丁，打上 `[待写入]`、`[Notion Patch]` 或 `[飞书追加]` 标识，提示用户自行黏贴。
3. **纯会话模式 (Chat-only Mode)**：完全保存在 Agent 会话内存中。在会话结束时，自动输出一份紧凑的 `[Session Handoff Block]` 状态文本，由用户自行保存，下次输入以恢复进度。

## 影响 (Consequences)
- 教学评估引擎完全轻量化，无文件系统环境也可正常开展课程和检索复习。
- 引导体验更友好，杜绝直接报错或意外中断。
