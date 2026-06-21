# Security Policy

## Scope

This repository contains natural-language instructions, Markdown templates, and small local Python utilities. The main risks are prompt injection in study materials, accidental exposure of learner data, and unintended filesystem writes.

## Security model

- Study materials are **untrusted data**. Any instruction embedded in them must not override the Skill, repository guidance, user intent, or host safety rules.
- Obsidian synchronization is optional. Without confirmed filesystem capability and an explicit vault path, the Skill must use preview mode.
- Runtime scripts are intentionally local-only: no network access, no package installation, no shell execution, no deletion, no Git mutation, and no writes outside the selected vault path.
- Templates separate AI-maintained content with `AI-MANAGED` markers. User-authored content outside those markers must be preserved.
- Learner sources may contain personal information. The Skill should redact secrets and minimize copied sensitive material.

## Reporting a vulnerability

Please do not open a public issue for a security vulnerability. Report it privately to the repository maintainer through the contact method listed on the repository profile. Include:

- a concise description;
- reproduction steps;
- affected files or behavior;
- expected versus actual behavior;
- suggested mitigation, if known.

We will acknowledge reports, investigate, and coordinate a fix before public disclosure when practical.
