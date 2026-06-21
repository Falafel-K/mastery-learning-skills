#!/usr/bin/env python3
"""Scaffold a new Agent Skill package safely.

Creates a standard folder and templated SKILL.md under skills/
based on CLI arguments.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def safe_skill_name(name: str) -> str:
    """Sanitize and return a lowercase dash-separated skill folder name."""
    normalized = name.lower().strip()
    normalized = normalized.replace("/", "-").replace("\\", "-")
    # Replace spaces and underscores with dashes
    normalized = re.sub(r"[\s_]+", "-", normalized)
    # Remove any characters that aren't lowercase alphanumeric or dashes
    normalized = re.sub(r"[^a-z0-9\-]", "", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    if not normalized:
        raise ValueError("Skill name must contain at least one valid alphanumeric character.")
    return normalized[:100]


def format_command_section(commands_str: str | None) -> str:
    """Format commands JSON list into markdown list."""
    if not commands_str:
        return ""
    try:
        commands = json.loads(commands_str)
        if not isinstance(commands, list) or not commands:
            return ""
        lines = ["## Slash Commands\n", "You must recognize and respond to these commands:"]
        for cmd in commands:
            lines.append(f"- `{cmd}` — [Define action and triggers here]")
        return "\n".join(lines) + "\n\n"
    except (json.JSONDecodeError, TypeError):
        return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Name of the skill.")
    parser.add_argument("--description", required=True, help="Description for skill discovery.")
    parser.add_argument("--commands", help="JSON list of commands, e.g., '[\"/study\", \"/review\"]'")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without writing.")
    
    args = parser.parse_args(argv)
    
    try:
        sanitized_name = safe_skill_name(args.name)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
        
    skill_dir = ROOT / "skills" / sanitized_name
    skill_file = skill_dir / "SKILL.md"
    
    # Check if directory already exists
    if skill_dir.exists():
        print(f"error: skill folder already exists at {skill_dir}", file=sys.stderr)
        return 2
        
    display_name = sanitized_name.replace("-", " ").title()
    commands_md = format_command_section(args.commands)
    
    template = f"""---
name: {sanitized_name}
description: {args.description}
license: MIT
compatibility: Markdown-capable agent.
---

# {display_name}

[Describe the general purpose and philosophy of the skill here]

## Scope and trigger

- [Define what triggers this skill, including any keywords or scenario matches]

{commands_md}## Steps

1. **Step Name**
   - [Step description]
   - **Completion Criterion**: [Explicit, checkable condition that indicates the step is done]

## Rules

1. **Rule Name**: [Detailed instruction/rule behavior]
2. **Rule Name**: [Detailed instruction/rule behavior]

## Completion Criteria

- [Generic condition that defines if the overall skill execution is completed]
"""
    
    if args.dry_run:
        print(f"Dry-run: Would create directory: {skill_dir}")
        print(f"Dry-run: Would create file: {skill_file}")
        print("Planned contents of SKILL.md:")
        print(template)
        return 0
        
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        skill_file.write_text(template, encoding="utf-8")
        print(f"Successfully scaffolded skill '{sanitized_name}' at {skill_file}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
        
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
