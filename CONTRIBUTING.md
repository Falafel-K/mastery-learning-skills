# Contributing

Thank you for improving the learning Skill.

## What belongs here

Good contributions make the learning workflow more reliable, more portable, more source-grounded, or easier to verify. Examples:

- a missing edge case in the mastery gate;
- a clearer subject adapter for a technical discipline;
- a safe, local-only improvement to course scaffolding;
- a regression case for a false-completion failure;
- documentation that makes host capability limits clearer.

## Before opening a pull request

1. Read `AGENTS.md` and the relevant reference protocol.
2. Avoid platform-specific fields in `skills/deep-skills/SKILL.md`.
3. Update evaluation cases if behavior changes.
4. Add or update tests for scripts and validators.
5. Run:

```bash
python tools/validate_skill_package.py
python tools/validate_evals.py
python -m unittest discover -s tests -v
```

## Pull request expectations

Explain:

- the learner or maintainer failure mode being addressed;
- the exact behavior change;
- which evaluations cover it;
- whether the change alters the portable core, only documentation, or only host-specific installation guidance.

## Content rules

- Do not submit real learner notes, copyrighted study material that you cannot redistribute, credentials, API keys, personal paths, or host workspace files.
- Do not add auto-executing network access, deletion, Git operations, or unprompted writes to runtime scripts.
- Do not replace evidence-based progression with “the learner said they understand.”
- Do not add a new Skill unless it has a distinct trigger, protocol, and evaluation set.

## Versioning

Update `CHANGELOG.md` for user-visible behavior changes. Keep experimental ideas out of the stable Skill until they have clear evaluation cases.
