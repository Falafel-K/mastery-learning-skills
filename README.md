# Mastery Learning Skills

> English | [简体中文](./README_zh.md)

**Turn AI conversations into durable knowledge through evidence-based learning.**

Mastery Learning Skills is an interactive learning system for AI agents that enforces **deliberate practice**, **progression gates**, and **structured note archiving**. Unlike passive Q&A, it requires you to demonstrate understanding through recall, application, and error correction before moving forward—then preserves your learning progress in organized Obsidian notes.

### Why This Exists

When learning with AI, three problems emerge:
1. **Illusion of understanding**: You read an explanation and feel like you "got it," but can't apply it later
2. **No retention**: Chat logs vanish, and you restart from scratch each session
3. **No accountability**: The AI keeps explaining without verifying you actually learned

This system solves these by treating learning as **a process with gates, evidence, and memory**—not just information transfer.

### What You Get

- **Evidence-based progression**: No advancement without demonstration (0-5 mastery scoring)
- **Spaced retrieval practice**: Automatic review scheduling for long-term retention
- **Structured knowledge archives**: Clean Obsidian notes, not messy chat logs
- **Cross-session continuity**: Pick up exactly where you left off, even in new conversations
- **Subject-aware tutoring**: Specialized adapters for mathematics, programming, science, and more

---

## Who Is This For?

### ✅ Good Fit
- Learning structured knowledge (mathematics, programming, science, technical skills)
- Have specific study materials (textbooks, documentation, course notes)
- Want long-term retention, not quick answers
- Comfortable with AI-assisted interactive learning

### ❌ Not Ideal For
- Quick fact lookups (use regular chat instead)
- Unstructured exploration or brainstorming
- Learning purely procedural skills without concepts
- Users uncomfortable with being "tested" by AI

---

## Three Ways to Use This

### 🚀 Path 1: Quick Trial (No Installation)

**Best for**: First-time users who want to see how it works

Just paste this into any compatible AI agent:

```text
Use mastery-learning-obsidian to teach me Python list comprehensions.
Treat this as a preview—don't write any files.

Material:
List comprehensions provide a concise way to create lists.
Basic syntax: [expression for item in iterable if condition]
Example: squares = [x**2 for x in range(10)]
```

The agent will:
1. Break down the concept into knowledge points
2. Teach each point interactively
3. Test your understanding before moving forward
4. Output structured Markdown you can copy-paste

**No installation. No file writes. Pure learning loop.**

### 📚 Path 2: Full System (With Obsidian)

**Best for**: Serious learners who want durable notes and spaced repetition

Install the skills, provide an Obsidian vault path, and get:
- Automatic note organization (knowledge maps, mastery ledger, error logs)
- Cross-session state preservation
- Spaced review scheduling
- Complete audit trails

→ See [Installation Guide](./docs/installation.md) for setup

### 🔧 Path 3: Development & Contribution

**Best for**: Contributors, researchers, or those customizing workflows

Clone the repo, symlink for live reloading, run validations:

```bash
git clone https://github.com/Falafel-K/mastery-learning-skills.git
cd mastery-learning-skills
./install.sh  # or .\install.ps1 on Windows
```

→ See [CONTRIBUTING.md](./CONTRIBUTING.md) and [AGENTS.md](./AGENTS.md)

---

## Quickstart (30-second installation)

The installer automatically detects active agent environments on your system and links/copies the skills to all of them:
- **Google Gemini / Antigravity**: `~/.gemini/config/skills`
- **Claude Code**: `~/.claude/skills`
- **General Fallback / Codex**: `~/.agents/skills`

This registers the main program alongside dedicated sub-command router skills (`/study`, `/review`, `/dashboard`, `/sync`, `/audit`, `/handoff`, `/help`, `/creat`, `/update`). They will appear directly in your agent's autocomplete dropdown menu!

### 1. Agent-Assisted Installation (Easiest, zero terminal setup)
If your current active agent has terminal/command execution capabilities (like Claude Code, Gemini, or Antigravity), simply paste this prompt directly into your agent chat window:

```text
Please install Mastery Learning Skills for me: if on Windows, run 'irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1 | iex'; if on macOS/Linux, run 'curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash'.
```

The agent will automatically download and execute the installer script, setting up all skills in the background.

### 2. One-Line Online Installation (Manual terminal copy)
If you prefer to run it manually in your system terminal, run the appropriate command:
- **macOS / Linux**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash
  ```
- **Windows (PowerShell)**:
  ```powershell
  irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1 | iex
  ```

### 3. One-Click Uninstall (Clean removal of skills)
You can uninstall the skills by running the uninstall command directly in your agent chat:
```text
Please uninstall Mastery Learning Skills: if on Windows, run '& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1))) -Uninstall'; if on macOS/Linux, run 'curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash -s -- --uninstall'.
```
Or run the uninstall command manually in your system terminal:
- **macOS / Linux**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash -s -- --uninstall
  ```
- **Windows (PowerShell)**:
  ```powershell
  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1))) -Uninstall
  ```

### 4. Local Developer Installation (Clone & Symlink)
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

## Design Goals & Key Features

This package addresses 5 common failure modes when learning with LLMs:

1. **Eliminate Illusion of Fluency**: Passive reading builds no durable memory. We implement **strict evidence gates** requiring active evidence (Recall, Discrimination, Application, Transfer, Error Repair, or Synthesis) before moving forward.
2. **Paced Progression Rubric**: AI tutors often dump vast text without verification. We apply a **0-5 mastery grading system**. Scores below 3 block progression; key points require 4; integrative capstone work requires 5. Consecutive failures trigger cognitive backoff and prerequisite review.
3. **Preserve Retrieval Difficulty**: AI shouldn't bypass your thinking by showing answers instantly. We mandate a **Hint Ladder** (Metacognitive cue → Directional hint → Code/Formula skeleton → Worked example). An example demonstration never counts as learner mastery; a fresh verification task is always presented afterward.
4. **Clean Archive over Chat logs**: Direct chat backups create noise. We enforce a **Storage Contract**, writing only in designated `AI-MANAGED` blocks within Obsidian notes, preserving your custom hand-written files.
5. **Session Recovery via Markdown**: Chat limits erase context. We treat local **Mastery Ledger** markdown files as the single source of truth, enabling instant state restoration across sessions.

→ See [docs/architecture.md](./docs/architecture.md) for technical details

---

## Command Reference

| Command | Action | Documentation |
|---|---|---|
| `/study [target]` | Learning loop: teach target `[target]` or automatic next objective | [learning-protocol.md](./skills/mastery-learning-obsidian/references/learning-protocol.md) |
| `/review [target]` | Retrieval-based review for specific or overdue knowledge points | [assessment-and-mastery.md](./skills/mastery-learning-obsidian/references/assessment-and-mastery.md) |
| `/dashboard` | Visual progress report with ASCII progress bars | [storage-contract.md](./skills/mastery-learning-obsidian/references/storage-contract.md) |
| `/sync` | Force synchronization to Vault using local Python tool | [storage-contract.md](./skills/mastery-learning-obsidian/references/storage-contract.md) |
| `/audit` | Coverage audit: verify all source material is assessed | [learning-protocol.md](./skills/mastery-learning-obsidian/references/learning-protocol.md) |
| `/handoff` | Pack session state for handoff to another agent/session | [learning-protocol.md](./skills/mastery-learning-obsidian/references/learning-protocol.md) |
| `/creat` | Meta-engineering: scaffold a new standardized agent skill | [skill-scaffolder/SKILL.md](./skills/skill-scaffolder/SKILL.md) |
| `/update` | Auto-update: pull latest versions and update all linked skills | [host-capabilities.md](./skills/mastery-learning-obsidian/references/host-capabilities.md) |
| `/help` | Display help guide for all commands | [host-capabilities.md](./skills/mastery-learning-obsidian/references/host-capabilities.md) |

---

## Documentation

**Getting Started**
- [Quick Start Guide](./docs/quickstart.md) - 5-minute walkthrough
- [Installation Guide](./docs/installation.md) - Detailed setup for all platforms
- [FAQ](./docs/faq.md) - Common questions and answers
- [Troubleshooting](./docs/troubleshooting.md) - Solutions to common issues

**Core Concepts**
- [Architecture](./docs/architecture.md) - System design and philosophy
- [Agent Compatibility](./docs/agent-compatibility.md) - Supported AI agents
- [Authoring Guide](./docs/authoring-guide.md) - For contributors

**Examples**
- [Python File I/O](./examples/python-demo-vault/) - Complete learning workflow example
- [More Examples](./examples/README.md) - Additional subject demonstrations

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
