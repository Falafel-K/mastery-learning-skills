# Architecture

## Purpose

This repository deliberately separates the **installable learning product** from the **quality system used to maintain it**.

```text
skills/mastery-learning-obsidian/  -> installed by an agent host
  SKILL.md                         -> activation and orchestration
  references/                      -> detailed protocols read on demand
  assets/templates/                -> copied into a learner's Obsidian Vault
  scripts/                         -> optional local helpers

evals/, tools/, tests/             -> repository-only maintenance assets
```

## Why one Skill in v0.1

The learning workflow has one user-facing activation: begin, continue, review, or audit a source-grounded study topic. Splitting it too early would create routing overhead and make a first installation harder.

Internally, the Skill is modular through references:

- `learning-protocol.md`: state machine and lesson loop;
- `assessment-and-mastery.md`: scoring, gates, error repair, review;
- `subject-adapters.md`: mathematics, science, programming, statistics, and engineering patterns;
- `storage-contract.md`: durable Markdown state and write policy;
- `host-capabilities.md`: capability detection and degradation;
- `safety-and-privacy.md`: prompt injection, data, and write safety.

When one of these modules acquires a distinct trigger and its own evaluations, it can graduate into a separate Skill under `skills/` without changing the learning data contract.

## Runtime state

A topic is a durable course folder inside the learner's Obsidian Vault:

```text
学习/<topic>/
├── 00-课程主页.md
├── 01-原始资料.md
├── 02-知识点地图.md
├── 03-掌握度账本.md      # canonical mastery state
├── 04-错题与误区.md
├── 05-作业与项目.md
├── 06-复习队列.md
├── sessions/YYYY-MM-DD.md
└── artifacts/
```

`03-掌握度账本.md` is the source of truth for mastery. Session notes capture evidence and discussion, but the ledger is the only file that decides whether a knowledge point is blocked, review-due, stable, or ready for synthesis.

## Progressive disclosure

The host should see a short `name` and `description` first, then load `SKILL.md` when relevant. `SKILL.md` tells the agent which detailed reference it must consult for the current action. This keeps every-session context compact while keeping behavior explicit.

## Portability boundary

The portable core assumes only Markdown reading and writing. It does not assume a particular slash-command format, plugin manifest, MCP server, browser, terminal, or model.

Host-specific features may improve convenience but must not redefine core behavior. For example, an agent with a terminal may call `create_course.py`; an agent without one must produce the same structure as a preview. An agent with no filesystem access can still run the instructional and assessment loops.

## Evaluation boundary

Natural-language Skills can drift when edited. Evaluation cases therefore test observable contracts: no false advancement, source anchoring, safe preview mode, fresh verification, subject-appropriate practice, and append-only same-day notes.
