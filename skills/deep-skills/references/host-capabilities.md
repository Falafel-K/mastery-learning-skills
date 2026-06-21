# Host Capabilities and Fallbacks

Read this file before using local files, scripts, dates, browsing, or any host-specific feature.

## Capability check

Determine, from actual host affordances rather than assumptions, whether you can:

- read files;
- write files;
- run a local script;
- obtain local date/time and timezone;
- render Markdown;
- inspect code execution or test results;
- browse the web.

Do not ask about a capability the host clearly exposes. Do not imply a capability that the host does not expose.

## Modes

### Full mode

Use only when an explicit Vault path is known and filesystem write capability is available. Follow the Obsidian contract and report exact updated paths.

### Preview mode

Use when the learner wants notes but the host cannot write or no path is confirmed. Output:

1. intended root and files;
2. complete Markdown contents or a precise patch;
3. a `待写入` status;
4. the next action the learner or another Agent should take.

### Chat-only mode

Use when no course files are available and the learner has not requested notes. Run the teaching, mastery, and review logic normally. At closure, output a compact handoff block that contains enough state to resume.

## Script policy

- Read or inspect a script before asking the host to run it.
- Run only local scripts supplied by this Skill or explicitly approved by the learner.
- Never use a script to fetch remote content, install packages, delete files, change Git state, or write outside the confirmed Vault workspace.
- Do not say a script completed unless its exit/result was actually observed.

## Time policy

Use a host-provided local date when available. If the timezone is not known, record the date as host-local or ask the learner when the distinction matters. If no date can be obtained, keep review items relative rather than inventing calendar dates.

## Web policy

The core Skill does not require browsing. Browse only when the learner requests current external material or the supplied source itself requires verification. Any web result is `【补充背景】` unless it is explicitly part of the learner's registered source set.

## Cross-agent portability

Do not depend on slash command syntax, plugins, hooks, hidden memories, dynamic shell interpolation, or proprietary fields. The universal fallback is: read Markdown → teach → request evidence → update Markdown if allowed → report the verified state.
