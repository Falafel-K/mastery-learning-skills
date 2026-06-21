# Claude Code Repository Guidance

Read and follow `AGENTS.md` before modifying this repository.

Before changing any Skill protocol, templates, or scripts:

1. Inspect relevant evaluation cases.
2. Update tests when behavior changes.
3. Run the validation workflow.

---

## Four Pillars Architecture Rules (四大支柱架构规则)

所有在本仓库中发布或扩展的技能（位于 `skills/` 目录下），必须严格遵守以下四大支柱规则：

1. **触发与隔离范式 (Trigger & Invocation)**：
   - 区分用户触发（User-invoked）与模型自主触发（Model-invoked）。
   - 手动触发的指令类技能必须在 YAML 头部标注 `disable-model-invocation: true`，且描述面向人类浏览。
   - 自主流程型技能不得设置该标志，且描述中应包含清晰的模型触发短语 (Trigger Phrases)。有关详细规范请参考 [docs/invocation.md](./docs/invocation.md)。

2. **存储依赖软降级 (Soft Degradation)**：
   - 所有涉及写操作的技能必须根据环境进行多级容错。
   - 遵循 [ADR 0001](./docs/adr/0001-mastery-storage-soft-degradation.md) 决策，适配 `Full mode`（本地账本写盘）、`Cloud mode`（Notion/飞书 Markdown 提示补丁）与 `Chat-only mode`（输出 Session Handoff 备忘块）。

3. **术语统一对齐 (Vocabulary Alignment)**：
   - 技能和引导话术中严禁使用二义性同义词。必须强引用根目录的 [CONTEXT.md](./CONTEXT.md) 并遵循其名词规范（如：掌握度账本、前置依赖、提示梯子、认知修复）。

4. **自动化打包与调试验证 (Scaffolding & Link)**：
   - 使用 `/create-skill` (由 `skill-scaffolder` 实现) 来自动搭建符合上述支柱的技能骨架。
   - 更新技能后必须运行部署脚本（`install.ps1` 或 `install.sh`）以重新装载与校验本地软链。
