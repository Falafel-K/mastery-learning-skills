# Agent Compatibility

## Portable contract

The package is intentionally based on the shared Agent Skills pattern:

```text
<skill-name>/
├── SKILL.md
├── references/   # optional
├── assets/       # optional
└── scripts/      # optional
```

`SKILL.md` uses only portable frontmatter fields: `name`, `description`, `license`, and `compatibility`. It does not rely on vendor-only frontmatter such as tool preapproval, hooks, plugin manifests, model-only invocation switches, or MCP declarations.

## Capability matrix

| Capability | Required? | Behavior when unavailable |
|---|---:|---|
| Read user-supplied material | Yes | The Skill cannot teach without a source or an explicitly requested general topic. |
| Markdown output | Yes | Core learning protocol still works. |
| Filesystem read | No | Ask the learner to provide needed course state or run in chat-only mode. |
| Filesystem write | No | Use preview mode; output paths and Markdown without claiming a save. |
| Python or terminal | No | Do not run helpers; produce the course schema manually. |
| Local date/time | No | Use a user-provided date or leave the review date as a relative instruction. |
| Browser/network | No | Not needed for the core protocol. |

## Known host patterns

| Host | Core package | Typical project placement | Notes |
|---|---|---|---|
| Codex | Supported | `.agents/skills/<name>/` | Uses the open Agent Skills format and also reads repository `AGENTS.md`. |
| Claude Code | Supported | `.claude/skills/<name>/` | Supports the open format plus optional Claude-only extensions, intentionally unused here. |
| Google Antigravity | Supported in principle | Host-managed workspace/global skill location | Use the host's current Skills UI or documented location; do not alter the package. |
| Other compatible agents | Expected | Host-specific | The core requires only a directory containing `SKILL.md`. |

## Why there is no `agents/openai.yaml`, `.claude-plugin`, or `package.json`

They are not required for the learning protocol.

- `agents/openai.yaml` is a Codex-specific optional enhancement for presentation/dependency metadata.
- `.claude-plugin` metadata is needed only when distributing a Claude plugin with hooks, agents, or MCP resources.
- `package.json` is useful only when a Node-based installer, website, release tooling, or runtime package is actually introduced.

Adding any of them now would create maintenance surface without improving the portable learning behavior.

## No duplicate Skills per host

Do not maintain separate `claude-version`, `codex-version`, and `antigravity-version` copies of the teaching protocol. They will drift. Keep one canonical portable package, then add a narrow adapter only when a platform-specific capability becomes necessary and has its own test coverage.
