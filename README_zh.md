# Mastery Learning Skills (掌握度学习导师插件)

> [English](./README.md) | 简体中文

> 我每天用于攻克技术难题和核心知识的 AI 代理插件 —— 拒绝“氛围感学习”（Vibe Learning）。

学习复杂的硬核技术主题（如数学、编程、数据科学、系统工程）非常困难。常规的 AI 解释常常会让你在阅读当下产生“我懂了”的流畅感假象（Fluency Strength），但却没有建立真正的长期存储强度（Storage Strength）。明天你就会忘得一干二净。

这套 Mastery Learning 插件专为**刻意练习、证据驱动门禁、以及结构化 Obsidian 笔记归档**而设计。它与任何 Agent 宿主（如 Claude Code, Codex, Antigravity）原生兼容。

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

## 为什么需要这个插件？

我写这套插件是为了解决在使用 Claude Code、Codex 等 AI 编程助手时，最常遇到的 5 种“学习失效”场景：

### #1. “AI 讲得很透彻，但我自己还是不会用。”
- **痛点**：被动阅读 AI 的解释只能建立“流畅感”，无法内化为能力。
- **解决机制**：**严苛的证据门禁**。在你说“懂了”的时候，插件拒绝前进。你必须通过 **复述、辨析、应用、迁移、纠错、或综合任务** 提交可观察的证据，否则进度将被死死卡住。

### #2. “我还没搞懂这步，AI 就急着讲下一章了。”
- **痛点**：传统的 AI 导师喜欢一股脑倾倒整章内容，不顾读者的理解进度。
- **解决机制**：**0-5 分级掌握度标准**。低于 3 分禁止学习新概念，核心知识点必须达到 4 分，综合项目/定理证明必须达到 5 分。若连续三次核验失败，将触发“认知降级机制”：主动降低难度，或回退检查前置知识是否缺失。

### #3. “还没等我想，AI 就把答案和代码吐出来了。”
- **痛点**：AI 的过度热心剥夺了你的“必要难度检索过程”。
- **解决机制**：**渐进式提示天梯（Hint Ladder）**（元认知提问 → 方向性线索 → 局部骨架代码 → 完整例题示范）。AI 提供的例题示范不能作为你的掌握证据，示范后必须用一道**全新的等价变式题**对你进行重新核验。

### #4. “我的 Obsidian 笔记变成了又臭又长的聊天逐字稿。”
- **痛点**：直接备份聊天记录会导致信息噪音极大，未来根本无法复习。
- **解决机制**：**Obsidian 档案契约**。我们只沉淀经过提炼的结构化笔记（课程主页、知识点地图、掌握度账本、错题与误区、复习队列）。AI 的写入完全被限制在 `<!-- AI-MANAGED:START -->` 与 `<!-- AI-MANAGED:END -->` 标记内，绝对不修改你的个人手写笔记。

### #5. “开启新对话或换个 Agent，我的学习进度全丢了。”
- **痛点**：大模型的上下文窗口限制了长期课程的维系。
- **解决机制**：**本地 Markdown 才是唯一真相源**。无论开启多少次新对话，AI 只要首先读取你的 `03-掌握度账本.md`，就能瞬间恢复上一次的教学状态，接续前进。

---

## 核心架构设计 (Under the Hood)

本 Skill 遵循高移植性的开放目录标准设计：
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
