#!/usr/bin/env python3
"""Validate the portable Skill packages without third-party dependencies.

Supports validating a single specified skill folder or dynamically scanning
and validating all skill folders under the skills/ directory.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED_FRONTMATTER = {
    "disable-model-invocation",
    "allowed-tools",
    "disallowed-tools",
    "hooks",
    "agent",
    "mcpServers",
}

# Specific rules for mastery-learning-obsidian
MASTERY_REFERENCES = [
    "learning-protocol.md",
    "assessment-and-mastery.md",
    "subject-adapters.md",
    "storage-contract.md",
    "host-capabilities.md",
    "safety-and-privacy.md",
]
MASTERY_TEMPLATES = [
    "course-home.md",
    "source-log.md",
    "knowledge-map.md",
    "mastery-ledger.md",
    "error-log.md",
    "assignments.md",
    "review-queue.md",
    "daily-session.md",
]
MASTERY_SCRIPTS = ["create_course.py", "validate_learning_vault.py", "sync_course.py", "generate_dashboard.py"]


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must begin with YAML frontmatter bounded by --- lines.")
    values: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            raise ValueError(f"Malformed frontmatter line: {raw_line}")
        key, value = raw_line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def validate_generic_skill(skill_dir: Path, errors: list[str], warnings: list[str]) -> None:
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    
    if not skill_file.is_file():
        errors.append(f"[{skill_name}] Missing SKILL.md in {skill_dir.relative_to(ROOT)}")
        return
        
    text = skill_file.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        errors.append(f"[{skill_name}] YAML frontmatter error: {exc}")
        frontmatter = {}
        
    if frontmatter.get("name") != skill_name:
        errors.append(f"[{skill_name}] Frontmatter name '{frontmatter.get('name')}' must match folder name '{skill_name}'")
        
    description = frontmatter.get("description", "")
    if len(description) < 40:
        errors.append(f"[{skill_name}] Frontmatter description is too short ({len(description)} chars) for reliable discovery. Must be >= 40 chars.")
        
    if len(text.splitlines()) > 500:
        warnings.append(f"[{skill_name}] SKILL.md exceeds 500 lines; move conditional detail to references.")
        
    for key in BANNED_FRONTMATTER.intersection(frontmatter):
        errors.append(f"[{skill_name}] Portable SKILL.md must not contain vendor-specific field: '{key}'")
        
    # Check templates if they exist
    templates_dir = skill_dir / "assets" / "templates"
    if templates_dir.is_dir():
        for template in templates_dir.glob("*.md"):
            contents = template.read_text(encoding="utf-8")
            if "<!-- AI-MANAGED:START -->" not in contents or "<!-- AI-MANAGED:END -->" not in contents:
                errors.append(f"[{skill_name}] Template missing AI-managed markers: {template.name}")


def validate_mastery_learning_obsidian(skill_dir: Path, errors: list[str], warnings: list[str]) -> None:
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return
        
    text = skill_file.read_text(encoding="utf-8")
    
    # Check that all required references are mentioned in SKILL.md
    for expected in MASTERY_REFERENCES:
        if f"references/{expected}" not in text:
            errors.append(f"[{skill_name}] SKILL.md does not reference required protocol: {expected}")
            
    # Check that files exist
    for folder, names in [
        (skill_dir / "references", MASTERY_REFERENCES),
        (skill_dir / "assets" / "templates", MASTERY_TEMPLATES),
        (skill_dir / "scripts", MASTERY_SCRIPTS),
    ]:
        for name in names:
            if not (folder / name).is_file():
                errors.append(f"[{skill_name}] Missing required asset: {(folder / name).relative_to(ROOT)}")


def validate_skill_scaffolder(skill_dir: Path, errors: list[str], warnings: list[str]) -> None:
    skill_name = skill_dir.name
    script_file = skill_dir / "scripts" / "scaffold_skill.py"
    if not script_file.is_file():
        errors.append(f"[{skill_name}] Missing required script: {script_file.relative_to(ROOT)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", help="Path to a specific skill package folder to validate.")
    args = parser.parse_args(argv)
    
    errors: list[str] = []
    warnings: list[str] = []
    
    skills_to_validate: list[Path] = []
    
    if args.skill_dir:
        target_dir = Path(args.skill_dir).expanduser().resolve()
        if not target_dir.is_dir():
            print(f"error: specified skill directory does not exist: {target_dir}", file=sys.stderr)
            return 2
        skills_to_validate.append(target_dir)
    else:
        # Dynamically discover all folders under skills/ containing SKILL.md
        skills_root = ROOT / "skills"
        if not skills_root.is_dir():
            print(f"error: skills directory not found at {skills_root}", file=sys.stderr)
            return 2
        for child in sorted(skills_root.iterdir()):
            if child.is_dir() and (child / "SKILL.md").is_file():
                skills_to_validate.append(child)
                
    if not skills_to_validate:
        print("warning: no skills found to validate.")
        return 0
        
    print(f"Validating {len(skills_to_validate)} skill package(s)...")
    for skill_dir in skills_to_validate:
        print(f"  Validating: {skill_dir.name}")
        validate_generic_skill(skill_dir, errors, warnings)
        
        # Specific validation based on name
        if skill_dir.name == "mastery-learning-obsidian":
            validate_mastery_learning_obsidian(skill_dir, errors, warnings)
        elif skill_dir.name == "skill-scaffolder":
            validate_skill_scaffolder(skill_dir, errors, warnings)
            
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
        
    print("All skill packages validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
