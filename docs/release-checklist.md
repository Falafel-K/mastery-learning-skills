# Release Checklist

## Content and behavior

- [ ] `SKILL.md` has a concise, accurate trigger description.
- [ ] Every reference named by `SKILL.md` exists and is still needed.
- [ ] No vendor-specific frontmatter has entered the portable core.
- [ ] Mastery gates still block false progression.
- [ ] Preview mode still prevents false “saved” claims.
- [ ] Templates preserve `AI-MANAGED` boundaries.
- [ ] Subject adapters still require application and transfer, not only recall.
- [ ] Error repair still uses fresh verification after a worked example.

## Privacy and safety

- [ ] No real learner Vault, source material, secrets, or absolute personal paths are tracked.
- [ ] Scripts are local-only and non-destructive.
- [ ] Prompt-injection treatment remains explicit.
- [ ] No new auto-approved shell or network behavior was introduced.

## Validation

```bash
python tools/validate_skill_package.py
python tools/validate_evals.py
python -m unittest discover -s tests -v
python skills/deep-skills/scripts/create_course.py \
  --vault /tmp/example-vault \
  --topic "验证主题" \
  --dry-run
```

## Documentation and release

- [ ] `CHANGELOG.md` updated for user-visible changes.
- [ ] README and installation instructions reflect the package.
- [ ] Agent compatibility claims are conservative and current.
- [ ] GitHub Actions passed on the release commit.
