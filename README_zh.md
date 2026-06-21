# Mastery Learning Skills (掌握度学习技能包)

> [English](./README.md) | 简体中文

基于 Obsidian 笔记库与 Agent 交互的掌握度学习 (Mastery Learning) 技能插件。

本技能包专为**刻意练习**、**证据驱动的进度门禁**以及**结构化笔记归档**而设计，原生兼容 Claude Code 等支持 Markdown 技能协议的 AI 代理宿主。其核心目标是通过交互式评估与诊断，将学习内容沉淀为持久的 Obsidian Markdown 笔记，而非生成无序的聊天对话记录。

---

## 快速开始（30秒上手）

安装脚本会自动识别你系统上已激活的 Agent 环境，并将技能一键安装/链接到它们之中：
- **Google Gemini / Antigravity**：`~/.gemini/config/skills`
- **Claude Code**：`~/.claude/skills`
- **通用 / Codex / 备用路径**：`~/.agents/skills`

### 1. 在线一键安装 (无需克隆)
在终端中复制并运行以下对应系统的命令：
- **macOS / Linux**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash
  ```
- **Windows (PowerShell)**:
  ```powershell
  irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1 | iex
  ```

### 2. 一键卸载清理 (干净清除全部技能指令)
如需彻底卸载本技能包并清理配置目录，请执行以下命令：
- **macOS / Linux**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash -s -- --uninstall
  ```
- **Windows (PowerShell)**:
  ```powershell
  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1))) -Uninstall
  ```

### 3. 本地克隆安装 (方便开发调试)
克隆本仓库并在本地运行安装脚本以创建实时生效的软链接：
```bash
git clone https://github.com/Falafel-K/mastery-learning-skills.git
cd mastery-learning-skills
```
然后运行安装脚本：
- **macOS/Linux**: `chmod +x install.sh && ./install.sh` (卸载: `./install.sh --uninstall`)
- **Windows (PowerShell)**: `.\install.ps1` (卸载: `.\install.ps1 -Uninstall`)

### 4. 开启学习会话
在 Agent 会话中粘贴你的学习资料，直接开启刻意学习：

```text
Use mastery-learning-obsidian to learn from the material below:

[在此粘贴你的学习资料]
```

如果你想将笔记自动同步到本地，请提供你的 Obsidian Vault 绝对路径。否则，插件将自动退级运行在 **Preview 预览模式**，并为你输出完整、可复制的 Markdown 内容。

---

## 指令参考 (Reference)

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

本技能包旨在解决用 AI 学习时最常见的 5 种“假学会”问题：

- **防止“假装懂了”**：只看 AI 的讲解容易产生“我学会了”的错觉。这里设置了严格的“证据卡点”——必须通过复述、对比、实际应用、迁移或找错等测试，才能解锁新内容。
- **不让进度“坐火箭”**：传统 AI 喜欢一次倒给你一整章内容。我们采用 0-5 分评分制，得分低于 3 分时会被强制留在当前知识点，AI 会降低难度重新教你，直到及格。
- **AI 不当“剧透狂”**：很多 AI 总是直接把代码和答案甩出来。这里强制使用“提示梯子”一步步引导你（先给思路，再给代码骨架，接着讲相似例题，最后让你做新变式题）。AI 的例题演示不能作为你学会的证据。
- **笔记不记流水账**：直接导出聊天记录噪音太多。本技能包有专属的“存储规矩”，只在笔记特定的“AI托管区”里更新账本，绝对不乱动你的手写笔记。
- **新开对话不怕忘**：大模型对话长了就会失忆。我们以本地的 Markdown 掌握度账本为准，每次新开对话，AI 读一下账本就能瞬间接上之前的进度。

---

## 四大支柱架构设计 (Four Pillars Architecture)

本插件遵循高度健壮、可移植且灵活的 AI 智能体技能设计范式，由以下四大核心支柱构成：

- **触发控制**：明确划分“人类主动下指令”（如学习 `/study`、复习 `/review`）和“AI 自动跑子任务”（如打分评估、纠错引导）的界限，防止 AI 在日常聊天时自作主张打扰你。详见 [docs/invocation.md](./docs/invocation.md)。
- **存储降级**：学习逻辑和笔记写入是松耦合的。支持三种模式：本地 Obsidian 直接写入、云笔记本（Notion/飞书）复制粘贴补丁包、纯聊天对话框导出移交备忘录。详见 [docs/adr/0001-mastery-storage-soft-degradation.md](./docs/adr/0001-mastery-storage-soft-degradation.md)。
- **统一术语**：在根目录 [CONTEXT.md](./CONTEXT.md) 中锁死了“掌握度账本”、“前置依赖”、“提示梯子”、“认知修复”等教学术语，防止 AI 说话多变、制造混乱。
- **链接与脚手架**：一键脚本（`install.ps1`/`install.sh`）可在本地快速创建软链接方便调试；同时配备自动脚手架 `/create-skill` 确保新开发的技能自动符合上述三大标准。

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
