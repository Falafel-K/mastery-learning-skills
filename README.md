# Mastery Learning Skills

> English | [简体中文](./README_zh.md)

An interactive Mastery Learning skill package for agent hosts, integrated with Obsidian vault storage.

This package enforces **deliberate practice**, **evidence-based progression gates**, and **structured note archiving**. It is fully compatible with Claude Code and other agent hosts supporting Markdown-based skill protocols. It focuses on diagnosing and reinforcing learner capability, compiling learning history into structured Obsidian notes rather than bloated chat transcripts.

---

## Quickstart (30-second setup)

The installer automatically detects active agent environments on your system and links/copies the skills to all of them:
- **Google Gemini / Antigravity**: `~/.gemini/config/skills`
- **Claude Code**: `~/.claude/skills`
- **General Fallback / Codex**: `~/.agents/skills`

This registers the main program alongside dedicated sub-command router skills (`/study`, `/review`, `/dashboard`, `/sync`, `/audit`, `/handoff`, and `/help`). They will appear directly in your agent's autocomplete dropdown menu!

### 1. One-Line Online Installation (Recommended, no Git required)
Copy and run the appropriate command for your system in your terminal:
- **macOS / Linux**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash
  ```
- **Windows (PowerShell)**:
  ```powershell
  irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1 | iex
  ```

### 2. One-Click Uninstall (Clean removal of skills)
To completely remove the skills and clean up the directories:
- **macOS / Linux**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash -s -- --uninstall
  ```
- **Windows (PowerShell)**:
  ```powershell
  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1))) -Uninstall
  ```

### 3. Local Developer Installation (Clone & Symlink)
Clone the repository and run the local installer to create live developer symlinks:
```bash
git clone https://github.com/Falafel-K/mastery-learning-skills.git
cd mastery-learning-skills
```
Then run the installer:
- **macOS/Linux**: `chmod +x install.sh && ./install.sh` (Uninstall: `./install.sh --uninstall`)
- **Windows (PowerShell)**: `.\install.ps1` (Uninstall: `.\install.ps1 -Uninstall`)

### 4. Start Learning
Start a deliberate learning session by pasting your study material in your agent chat:

```text
Use mastery-learning-obsidian to learn from the material below:

[Paste material here]
```

If you want filesystem-backed Obsidian notes, provide a Vault path. Otherwise, the skill runs in **Preview mode** and outputs copy-pasteable Markdown.

---

## Reference

| Command | Action | Reusable Discipline |
|---|---|---|
| `/study [target]` / `/learn [target]` | Learning loop: teach target `[target]` (e.g. `K03`, `S1/Sec2`, or keyword) overriding default order. Defaults to the automatic next objective if omitted. | `learning-protocol.md` |
| `/review [target]` | Start a retrieval-based review session for a specific `[target]` (e.g. `K01`) or all overdue points if omitted. | `assessment-and-mastery.md` |
| `/audit` | Perform a coverage audit: verify that every important source claim maps to an assessed Kxx point. | `learning-protocol.md` |
| `/handoff` | Pack active session state, scores, and paths into a compact handoff block for another agent or session. | `learning-protocol.md` |
| `/sync` | Force a synchronization of files to the Vault using the secure local python tool `sync_course.py`. | `storage-contract.md` |
| `/create-skill` | Meta-Engineering: Grill the user with 3 questions and scaffold a new standardized agent skill folder. Runs silent validation before presenting a preview. | `skill-scaffolder/SKILL.md` |

---

## Design Goals & Key Features

This package addresses 5 common failure modes when learning with LLMs:

1. **Eliminate Illusion of Fluency**: Passive reading builds no durable memory. We implement **strict evidence gates** requiring active evidence (Recall, Discrimination, Application, Transfer, Error Repair, or Synthesis) before moving forward.
2. **Paced Progression Rubric**: AI tutors often dump vast text without verification. We apply a **0-5 mastery grading system**. Scores below 3 block progression; key points require 4; integrative capstone work requires 5. Consecutive failures trigger cognitive backoff and prerequisite review.
3. **Preserve Retrieval Difficulty**: AI shouldn't bypass your thinking by showing answers instantly. We mandate a **Hint Ladder** (Metacognitive cue → Directional hint → Code/Formula skeleton → Worked example). An example demonstration never counts as learner mastery; a fresh verification task is always presented afterward.
4. **Clean Archive over Chat logs**: Direct chat backups create noise. We enforce a **Storage Contract**, writing only in designated `AI-MANAGED` blocks within Obsidian notes, preserving your custom hand-written files.
5. **Session Recovery via Markdown**: Chat limits erase context. We treat local **Mastery Ledger** markdown files as the single source of truth, enabling instant state restoration across sessions.

---

## Four Pillars Architecture

This project adopts a highly robust, portable, and flexible agent skill design paradigm consisting of four core pillars:

1. **Trigger & Invocation Paradigm** (触发与调用隔离): Separates user-entered slash commands (User-invoked, like `/study` and `/review`) from autonomous routines (Model-invoked, like `mastery-assessment` and `learning-repair`) to keep the user in control and prevent accidental prompts. See [docs/invocation.md](./docs/invocation.md).
2. **Soft Degradation Decoupling** (存储软降级): decoupled pedagogical scoring from direct file writes. Enables smooth fallbacks across `Full mode` (local writes), `Cloud mode` (Notion/Feishu patches), and `Chat-only mode` (memory + handoff blocks). See [docs/adr/0001-mastery-storage-soft-degradation.md](./docs/adr/0001-mastery-storage-soft-degradation.md).
3. **Vocabulary Alignment** (术语统一对齐): Enforces a strict vocabulary filter using [CONTEXT.md](./CONTEXT.md) to ensure consistent AI phrasing and eliminate terminology confusion.
4. **Linking Ecosystem & Scaffolding** (自动链接与脚手架): Provides fast symlinking via `install.ps1`/`install.sh` for development reloading, and extends `skill-scaffolder` to automatically generate new skills complying with these pillars.

---

## Under the Hood

The portable core is structured into:
- `CONTEXT.md`: Terminology vocabulary filter.
- `docs/invocation.md` & `docs/adr/`: Invocation specs and architectural decision records.
- `SKILL.md`: Light entrypoint defining triggers and commands.
- `references/`: Modular documents consulted dynamically by the agent.
  - `learning-protocol.md`: State machine and cognitive load rules.
  - `assessment-and-mastery.md`: Rubrics, hint ladders, error taxonomy, spaced repetition schedule.
  - `subject-adapters.md`: Technical adapters for Mathematics, CS/Programming, Physics, Chemistry, Biology, Statistics/ML, and Economics.
  - `storage-contract.md`: Formatting standards and template sync rules.
  - `host-capabilities.md`: Fail-safes and capability degradation matrix.
  - `safety-and-privacy.md`: Shielding against prompt injections inside study materials.
- `assets/templates/`: Default templates for Obsidian notes (Chinese-first, bilingual friendly).
- `scripts/`: Local tools to manage Vault creation and updates:
  - `create_course.py`: Safe, template-backed course setup.
  - `sync_course.py`: Safely modifies Markdown tables and files inside the managed zones.
  - `validate_learning_vault.py`: Validates Vault structure compliance.

---

## Validate & Test

No third-party Python packages are required.

```bash
# Validate skill package integrity
python tools/validate_skill_package.py

# Validate eval behaviors
python tools/validate_evals.py

# Run standard-library unit tests
python -m unittest discover -s tests -v
```

To dry-run course generation locally:
```bash
python skills/mastery-learning-obsidian/scripts/create_course.py \
  --vault "/path/to/Obsidian Vault" \
  --topic "数学-极限" \
  --subject "数学" \
  --dry-run
```
