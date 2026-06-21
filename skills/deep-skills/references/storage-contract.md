# Universal Note & Storage Contract (通用笔记与存储契约)

Read this file before creating, reading, or modifying a learning workspace.

This contract defines how learning records are stored, structured, and updated across different notebooks (Obsidian, Notion, Feishu, or local Markdown folders).

---

## 1. Storage Options (存储适配模式)

The Skill supports three types of storage setups to ensure zero friction:

### A. Local Markdown Folder (本地文件夹模式 - 默认)
- **Concept**: Pure Markdown files stored in a local directory. Fully compatible with any text editor (VS Code, PyCharm, Typora, Logseq).
- **Structure**: Uses standard Markdown tables and headings. Extremely portable and offline-first.

### B. Obsidian Vault (Obsidian 增强模式)
- **Concept**: Identical to the Local Folder mode, but leverages Obsidian plugins:
  - **Dataview**: Renders dynamic tables of recent sessions and pending tasks.
  - **Spaced Repetition**: Parses `#flashcard` tags for interactive reviews.

### C. Cloud Note Adapter (云端笔记模式 - Notion, 飞书, 语雀)
- **Concept**: For notebooks hosted in the cloud where direct filesystem access is unavailable or requires API keys.
- **Protocol (Clipboard Patches / 剪贴板增量更新)**:
  - The Agent runs in **Preview Mode (预览模式)**.
  - It generates beautifully formatted Markdown chunks clearly labeled with their destination pages (e.g., `[Notion Patch: 03-掌握度账本.md]` or `[飞书: 追加学习日志]`).
  - The user can comfortably copy-paste these updates into their cloud notebook.

---

## 2. Preconditions for File Writes

Write to the local filesystem only when all are true:
1. The learner has requested records or synchronization.
2. A local directory path (Vault path or workspace root) is configured and confirmed.
3. The host environment permits filesystem writes.
4. The action is limited to the configured learning workspace.
5. The action does not overwrite user-authored content outside an `AI-MANAGED` block.

*If any condition is false, fall back to Preview Mode.* Generate the structured content, label it clearly with `待写入` (Pending Write), and print it to the console so the user can easily save or copy it.

---

## 3. Course Layout

For each independent topic, create one folder containing these core files:

```text
<Workspace Root>/学习/<topic>/
├── 00-课程主页.md         # Course index, mission, status, unresolved questions
├── 01-原始资料.md         # Source materials register and excerpts
├── 02-知识点地图.md       # Kxx knowledge map, prerequisites, evidence plan
├── 03-掌握度账本.md       # Canonical learning state, scores, and mastery ledger
├── 04-错题与误区.md       # Durable error logs, causes, and verification results
├── 05-作业与项目.md       # Assignments and capstone project specifications
├── 06-复习队列.md         # Retrieval-based review schedule and spaced repetition dates
├── sessions/             # Dated session records
│   └── YYYY-MM-DD.md     # Learning-day evidence, state changes, and flashcards
└── artifacts/            # Learner work: code, derivations, experiments
```

---

## 4. Content Ownership & Markers

All AI-managed sections inside the core files must be enclosed by these markers:

```html
<!-- AI-MANAGED:START -->
<!-- AI-MANAGED:END -->
```

The Agent may update content **only** between these markers, leaving user-authored notes and YAML frontmatter completely untouched. If markers are missing, do not attempt to write or overwrite the file; instead, output a preview and request permission.

---

## 5. Spaced Repetition Flashcards

Flashcards must be written under `### 闪卡制作 (Spaced Repetition)` in session files using the format:
```text
Question :: Answer #flashcard/Topic_Name
```
Ensure topic names are slugified (alphanumeric and underscores only, e.g., `#flashcard/Python_文件处理`).

---

## 6. Update Sequence

When a learning state change occurs:
1. Append or update the dated session file in `sessions/YYYY-MM-DD.md`.
2. Update the canonical ledger `03-掌握度账本.md` (e.g. status and scores).
3. Update error logs, assignments, or review files if applicable.
4. Update `00-课程主页.md` to show the current learning objective.
5. Report all path updates and reasons clearly to the user.
