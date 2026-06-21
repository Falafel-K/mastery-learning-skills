# Trigger & Invocation Paradigm: User-invoked vs Model-invoked

在 Mastery Learning 项目中，所有的技能与操作命令在调用模式上被严格区分为 **用户触发型 (User-invoked)** 与 **模型触发型 (Model-invoked)** 双轴。这种隔离旨在维护“学生主动掌控，AI 隐性施教”的教学平衡，并防止 AI 在没有得到用户明确许可的情况下私自修改本地文件或账本。

---

## 1. 用户触发型 (User-invoked)

### 1.1 特征与标志
- **YAML Frontmatter**：包含 `disable-model-invocation: true` 属性。
- **描述设计**：面向人类浏览，语言精炼直白。不允许包含诱导 AI 自动触发的短语（Trigger Phrases）。
- **示例命令**：
  - `/study` 或 `/learn`：开始学习环路。
  - `/review`：启动知识检索与复习。
  - `/dashboard`：生成图形化掌握度进度。
  - `/audit`：发起课程覆盖度审计。
  - `/handoff`：生成会话移交。
  - `/sync`：触发本地文件同步。

### 1.2 目的与约束
- **防意外触发**：避免 AI 在与用户日常交谈中自动加载庞大的教学流程。
- **写操作安全隔离**：用户触发型命令通常涉及较重的文件读写或重要的教学环路开启。在设计上，**非人类显式键入这些命令，AI 绝不主动加载它们**。

---

## 2. 模型触发型 (Model-invoked)

### 1.1 特征与标志
- **YAML Frontmatter**：省略 `disable-model-invocation`（即默认为 `false`）。
- **描述设计**：面向 AI 模型，包含清晰、丰富的触发场景（例如 `"Use when the user has provided an answer to a math problem..."`）。
- **示例功能**：
  - `mastery-assessment`：掌握度出题与评估子程序（判断用户回答的证据等级，给出 0-5 评分）。
  - `learning-repair`：认知修复机制（在评估得分 < 3 时介入，搭建提示梯子引导用户发现错误）。
  - `storage-writer`：底层笔记持久化写程序（在 Full Mode 下辅助格式化写入 `AI-MANAGED` 区域）。

### 1.2 目的与约束
- **自动化流转**：AI 根据学习进展自主运行（例如在讲授完一个微知识点后，自动调用评估模块出题，并在用户答错时自动启动认知修复）。

---

## 3. 依赖传递约束 (The Chaining Rule)

为了保证这一套教学体系的健壮性，技能间的依赖调用必须严格遵守以下原则：

1. **上级触发下级**：用户触发型命令（如 `/study`）在执行中可以随时调用模型触发型功能（如 `mastery-assessment` 进行出题测试）。
2. **同级禁止横向串联**：用户触发型命令之间**绝对禁止横向互相隐式串联调用**（例如，AI 导师绝不能在执行完 `/study` 的打分后，静默替用户调用 `/sync` 完成物理写盘）。
3. **交互式指引**：如果需要完成链式工作，AI 必须通过明确的引导话术向用户建议（例如：*"您的本次知识点学习已完成，推荐运行 `/sync` 将最新状态落盘。"*），让学生拥有终极的控制权。
