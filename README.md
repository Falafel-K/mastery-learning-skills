# Deep Skills

> English | [简体中文](./README_zh.md)

> My agent skills that I use every day to master technical subjects — not vibe learning.

Learning complex technical topics (math, programming, data science, engineering) is hard. Standard AI explanations make you feel smart in the moment, but they build no storage strength. You forget it all tomorrow. 

These skills are designed to enforce deliberate practice, evidence-based gatekeeping, and structured Obsidian notes. They work with any agent host.

---

## Quickstart (30-second setup)

1. Clone or download this repository.
2. Copy or symlink `skills/deep-skills/` into your agent host's skills directory.
3. Start a deliberate learning session by pasting your study material:

```text
Use deep-skills to learn from the material below:

[Paste material here]
```

4. If you want filesystem-backed Obsidian notes, provide a Vault path. Otherwise, the skill runs in **Preview mode** and outputs copy-pasteable Markdown.

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

## Why These Skills Exist

We built this skill to fix common failure modes when learning with Claude Code, Codex, and other coding agents.

### #1: "The agent explained it, but I cannot use it."
**The Problem**: Reading an explanation gives an illusion of fluency, but no storage strength.
**The Fix**: Strict evidence gates. You cannot advance to the next topic by saying "I understand". You must provide active evidence: **Recall, Discrimination, Application, Transfer, Error Repair, or Synthesis**.

### #2: "The agent moved on while I was still confused."
**The Problem**: AI tutors often dump chapters at once and keep going without checking.
**The Fix**: A strict 0-5 mastery rubric. Scores below 3 block progression. Key points require a score of 4. Integrative capstone work requires 5. If you fail 3 times, the skill triggers a cognitive backup: downgrading difficulty or checking missing prerequisites.

### #3: "The agent gave me the answer before I could think."
**The Problem**: AI often outputs the solution to its own questions, depriving you of retrieval difficulty.
**The Fix**: A structured hint ladder (Metacognitive prompt → Directional cue → Partial structure → Worked example) and fresh verification tasks. A solved example never counts as learner evidence.

### #4: "My notes became an unreadable transcript."
**The Problem**: Storing complete dialogue transcripts makes notes useless for quick reviews.
**The Fix**: The Obsidian Contract. We only record durable learning state in structure notes (`00-课程主页.md`, `02-知识点地图.md`, `03-掌握度账本.md`, `04-错题与误区.md`, `06-复习队列.md`). AI only modifies data between `<!-- AI-MANAGED:START -->` and `<!-- AI-MANAGED:END -->` blocks, leaving your private notes untouched.

### #5: "A new chat or different agent lost all my learning state."
**The Problem**: Chat history limit wipes out your progress.
**The Fix**: Plain Markdown files are the single source of truth. A new agent or session reads `03-掌握度账本.md` and immediately resumes right where you left off.

---

## Under the Hood

The portable core is structured into:
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
python skills/deep-skills/scripts/create_course.py \
  --vault "/path/to/Obsidian Vault" \
  --topic "数学-极限" \
  --subject "数学" \
  --dry-run
```
