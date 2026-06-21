# Authoring Guide

## A Skill is a behavioral contract

Write instructions that a reviewer can observe. Prefer:

- “Do not advance while the score is below 3.”
- “Label material outside the source as `【补充背景】`.”
- “In preview mode, output the intended path and complete Markdown.”

Avoid vague requests such as “be rigorous,” “teach well,” or “make great notes” unless the behavior is specified elsewhere.

## Keep the entrypoint small

`SKILL.md` should contain:

- triggering boundaries;
- capability and safety checks;
- the core learning state machine;
- non-negotiable progression gates;
- reference-loading instructions;
- completion and note-update requirements.

Put detailed taxonomies, templates, and domain-specific methods in `references/` and `assets/`. A long Skill body stays in agent context after activation and increases drift risk.

## Add a rule safely

For every new rule, answer:

1. What failure mode does it prevent?
2. When exactly does it apply?
3. What observable action demonstrates compliance?
4. Which evaluation case proves it?
5. Does it require a template, script, or documentation change?

## Add a future Skill only when justified

Create a new directory under `skills/` only when it has:

- a distinct trigger;
- a reusable workflow that should not always load with this Skill;
- its own output contract;
- at least three evaluation cases;
- a clear relationship to the shared Obsidian data model.

For example, `math-proof-tutor` could become separate if it needs a proof-specific workflow beyond the generic subject adapter. It should still read the same course ledger and source map rather than inventing parallel state.

## Template compatibility

Templates are user data once copied into a Vault. Do not casually rename files, remove frontmatter fields, or move `AI-MANAGED` markers. Treat such changes as migrations: document them, preserve user content, and add validation.

## Script rules

Runtime scripts must:

- rely on the standard library unless a dependency is justified;
- receive explicit paths through arguments;
- print planned actions before writing when possible;
- refuse unsafe overwrite behavior;
- never network, delete, commit, or install packages;
- have tests.
