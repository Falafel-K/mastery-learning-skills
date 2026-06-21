# Repository guidance for coding agents

This repository publishes a cross-agent learning Skill. Treat `skills/deep-skills/` as a public, portable product rather than a private prompt dump.

## Non-negotiable contracts

1. Do not weaken source grounding, mastery gates, user-control of filesystem writes, or privacy protections without changing the relevant evaluation cases and documentation.
2. Do not add vendor-specific frontmatter to the portable `SKILL.md`. Keep the core compatible with generic Agent Skills hosts.
3. Do not commit a real Obsidian Vault, private study material, secrets, API keys, absolute personal paths, `.obsidian/workspace*.json`, or generated `__pycache__` files.
4. Do not claim a script is safe without reading it. Scripts in the installable Skill must remain local-only, non-networked, non-destructive, and explicit about write targets.
5. Preserve the division of responsibility:
   - `skills/`: installable product;
   - `references/`: on-demand protocols;
   - `assets/`: copied runtime templates;
   - `scripts/`: optional runtime helpers;
   - `evals/`, `tools/`, `tests/`: repository quality assurance.
6. `03-掌握度账本.md` is the learning-state source of truth. Do not create a competing ledger.
7. Every behavior change to a core teaching rule needs at least one regression evaluation. Every change to a template or script must be covered by validation or a test.

## Before editing

1. Read the affected `SKILL.md` section and linked reference documents.
2. Inspect relevant `evals/deep-skills/cases.json` cases.
3. Make the smallest coherent change.
4. Update docs, templates, and tests when the contract changes.
5. Run:

```bash
python tools/validate_skill_package.py
python tools/validate_evals.py
python -m unittest discover -s tests -v
```

## Style

- Use plain, precise English in portable Skill instructions.
- User-facing Obsidian templates are Chinese-first but should remain understandable to bilingual users.
- Prefer rules that can be observed and evaluated over aspirational language.
- Keep `SKILL.md` concise; move conditional or detailed rules into `references/`.
- Never add a dependency just to parse YAML or JSON when the standard library is sufficient.
