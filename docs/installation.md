# Installation

## Install the portable core

The unit to install is this directory:

```text
skills/mastery-learning-obsidian/
```

Copy or symlink the whole directory. Do not copy only `SKILL.md`; the Skill references supporting protocols, templates, and safe scripts.

## Codex

For a repository-specific install, place the directory at:

```text
<your-project>/.agents/skills/mastery-learning-obsidian/
```

For a personal install, use the user-level skills location supported by your Codex installation. Codex can discover repository skills while walking from the working directory toward the repository root.

## Claude Code

For a project-specific install:

```text
<your-project>/.claude/skills/mastery-learning-obsidian/
```

For a personal install:

```text
~/.claude/skills/mastery-learning-obsidian/
```

Claude Code can invoke a Skill directly by name or load it when the request matches its description. This Skill is intentionally framed as an explicit learning workflow because it may write durable study records.

## Google Antigravity

Use the workspace or global Skills location exposed by the installed Antigravity version, or its Skills import/manager UI, and copy the same `mastery-learning-obsidian` directory unchanged. Antigravity supports a directory-based `SKILL.md` format, but locations and UI steps can change between releases.

## Other Agent Skills hosts

Use the host's documented Skill discovery path and install the complete directory. The portable core expects only the generic `SKILL.md` package layout.

## Symlink example

On macOS or Linux, from a checked-out copy of this repository:

```bash
mkdir -p /path/to/project/.agents/skills
ln -s "$(pwd)/skills/mastery-learning-obsidian" \
  /path/to/project/.agents/skills/mastery-learning-obsidian
```

Use a copy instead of a symlink when your host or operating system does not follow symlinks.

## First learning session

Start with an explicit request:

```text
Use mastery-learning-obsidian to learn from the material below.
I want evidence of explanation, application, error repair, and transfer—not a fast summary.

[Paste material]
```

If you want Obsidian records, provide a vault path and confirm that the agent may write under its `学习/` workspace. Otherwise, the Skill must generate a preview only.

## Update

Replace the installed directory with a newer version, then restart or reload your host if it does not watch skill files live. Keep real learner Vaults separate from this repository.
