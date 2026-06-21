# Mastery Learning Skills (掌握度学习技能包)

> [English](./README.md) | 简体中文

基于 Obsidian 笔记库与 Agent 交互的掌握度学习 (Mastery Learning) 技能插件。

本技能包专为**刻意练习**、**证据驱动的进度门禁**以及**结构化笔记归档**而设计，原生兼容 Claude Code 等支持 Markdown 技能协议的 AI 代理宿主。其核心目标是通过交互式评估与诊断，将学习内容沉淀为持久的 Obsidian Markdown 笔记，而非生成无序的聊天对话记录。

---

## 快速开始（30秒上手）

1. **一键在线安装（推荐，无需手动克隆或安装 Git）**：
   在终端中复制并运行以下对应系统的命令：
   - **macOS / Linux**:
     ```bash
     curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash
     ```
   - **Windows (PowerShell)**:
     ```powershell
     irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1 | iex
     ```
2. **开发者本地安装（已克隆本仓库，方便改动后实时生效）**：
   在仓库根目录下直接运行本地脚本以自动创建软链接：
   - **macOS/Linux**: `chmod +x install.sh && ./install.sh`
   - **Windows (PowerShell)**: `.\install.ps1`
3. 粘贴你的学习资料，直接开启刻意学习会话：

```text
Use mastery-learning-obsidian to learn from the material below:

[在此粘贴你的学习资料]
```

4. 如果你想将笔记自动同步到本地，请提供你的 Obsidian Vault 绝对路径。否则，插件将自动退级运行在 **Preview 预览模式**，并为你输出完整、可复制的 Markdown 内容。

---

## 命令参考矩阵 (Reference)

| 命令行指令 | 执行动作 | 对应的行为规则契约 |
|---|---|---|
| `/study [目标]` / `/learn [目标]` | 教学循环：若提供 `[目标]`（如 `K03`、`S1/第2节` 或关键字），强制覆盖自动顺序对该目标进行教学（若缺少前置知识会报警提示，但可强制执行）；若省去则自动学习下一知识点。 | `learning-protocol.md` |
| `/review [目标]` | 复习循环：若提供 `[目标]`（如 `K01`），立即对该知识点启动检索式复习；若省去则复习队列中所有到期的知识点。 | `assessment-and-mastery.md` |
| `/audit` | 触发资料覆盖度审计：核验原始资料中的每一处核心论断/公式/代码是否已被全部映射并核验。 | `learning-protocol.md` |
| `/handoff` | 瞬间打包当前会话的进度、得分、活跃错误和笔记路径，生成一份紧凑的交接上下文（Handoff Block），便于新会话或新 Agent 快速接管。 | `learning-protocol.md` |
| `/sync` | 强制调用本地安全的 Python 脚本 `sync_course.py`，将当前的掌握度、Session 日志和错题本安全地同步到本地 Vault 中。 | `storage-contract.md` |
| `/create-skill` | 元工程技能：对用户启动极简“三问协议”，在后台静默自动构建标准化技能包（创建 `SKILL.md` 骨架），并调用包校验工具自检通过后呈现预览。 | `skill-scaffolder/SKILL.md` |

---

## 设计解决的教学痛点

本技能包致力于解决与大模型交互学习时最常见的 5 种“学习失效”场景：

1. **防止假性流畅感**：被动阅读 AI 的解释往往产生“已掌握”的错觉。本技能包引入**严苛的证据门禁**。在学习者提供可观察的证据（复述、辨析、应用、迁移、纠错或综合任务）之前，禁止推进。
2. **缺乏个性化进度门禁**：AI 导师常盲目倾倒大段内容。我们实施 **0-5 掌握度评分标准**。低于 3 分禁止解锁新概念；核心概念要求 4 分；综合 capstone 要求 5 分。若连续三次核验失败，自动执行认知降级，退回检查前置依赖。
3. **过度热心夺走检索难度**：AI 常常直接给出答案。本技能包强制使用**提示梯子 (Hint Ladder)**（思路暗示 → 框架骨架 → 相似 Worked Example → Graded Task）。在向学生提供例题示范后，必须换一道全新变式题进行测试，且示范代码不计入掌握证据。
4. **笔记数据噪音过载**：直接记录聊天历史噪音巨大。我们通过**存储契约**，仅在 `03-掌握度账本.md` 等文件的 `AI-MANAGED` 托管区间内自动更新结构化卡片，绝不修改您的个人笔记。
5. **跨会话学习状态丢失**：AI 的上下文窗口限制了长期维系。本技能包以本地 Markdown **掌握度账本**为唯一真相源，跨会话只需重新读取账本即可恢复前次进度。

---

## 四大支柱架构设计 (Four Pillars Architecture)

本插件遵循高度健壮、可移植且灵活的 AI 智能体技能设计范式，由以下四大核心支柱构成：

1. **触发与调用隔离**：划分用户显式键入指令（User-invoked，如 `/study` 和 `/review`）与 AI 自主运行子程序（Model-invoked，如打分出题和错误修复）的边界，避免在日常会话中意外打扰用户。详见 [docs/invocation.md](./docs/invocation.md)。
2. **存储依赖软降级**：学习核心逻辑与持久层物理写入解耦，提供 `Full mode`（本地 Obsidian 写入）、`Cloud mode`（输出 Notion/飞书 Markdown 补丁块）与 `Chat-only mode`（输出 Handoff 会话移交块）三级退化方案。详见 [docs/adr/0001-mastery-storage-soft-degradation.md](./docs/adr/0001-mastery-storage-soft-degradation.md)。
3. **术语统一过滤器**：通过根目录 [CONTEXT.md](./CONTEXT.md) 锁定标准教学用词（掌握度账本、前置依赖、提示梯子、认知修复），消除 Agent 代名词歧义与黑话。
4. **敏捷调试与脚手架**：支持通过 `install.ps1`/`install.sh` 快速在本地 `.agents/skills` 建立软链接开发调试，并使用 `skill-scaffolder` 自动生成符合此四大支柱规范的新技能。

---

## 核心架构设计 (Under the Hood)

本 Skill 遵循高移植性的开放目录标准设计：
- `CONTEXT.md`：术语统一词汇字典。
- `docs/invocation.md` & `docs/adr/`：双轴触发隔离规范与架构决策记录。
- `SKILL.md`：轻量级入口，定义触发词与 Slash Commands。
- `references/`：模块化行为契约库，供 Agent 在运行时按需按指示读取：
  - `learning-protocol.md`：核心教学状态机与认知负荷控制规则。
  - `assessment-and-mastery.md`：评分细则、提示天梯、错误分类法、间隔重复算法。
  - `subject-adapters.md`：针对数学、编程/计算机、物理、化学、生物、统计/机器学习和经济学的专业教学适配器。
  - `storage-contract.md`：Obsidian 档案格式标准与防写越界策略。
  - `host-capabilities.md`：环境兼容与无缝功能降级策略。
  - `safety-and-privacy.md`：防止学习材料中夹带恶意 prompt 注入的安全防御契约。
- `assets/templates/`：Obsidian 档案的基础 Markdown 模板。
- `scripts/`：供 Agent 调用的本地安全 Python 脚本（不联网、不覆盖写、仅使用标准库）：
  - `create_course.py`：安全创建课程结构与模板。
  - `sync_course.py`：安全读写托管区段内的表格和数据。
  - `validate_learning_vault.py`：校验 Vault 档案合规性。

---

## 本地校验与测试

本项目不依赖任何第三方 Python 库，使用标准库即可完成所有测试：

```bash
# 校验 Skill 目录合规性与 Frontmatter 移植性
python tools/validate_skill_package.py

# 校验 behavior-level regression 用例
python tools/validate_evals.py

# 运行单元测试
python -m unittest discover -s tests -v
```

如果需要在本地安全地预览课程生成目录结构：
```bash
python skills/mastery-learning-obsidian/scripts/create_course.py \
  --vault "/path/to/Obsidian Vault" \
  --topic "数学-极限" \
  --subject "数学" \
  --dry-run
```
