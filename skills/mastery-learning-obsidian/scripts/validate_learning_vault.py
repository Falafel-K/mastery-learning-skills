#!/usr/bin/env python3
"""Validate the structural contract of one generated learning course.

The validator is intentionally conservative: it reports missing contract files,
AI-managed markers, and malformed session date names. It does not edit files.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REQUIRED_FILES = [
    "00-课程主页.md",
    "01-原始资料.md",
    "02-知识点地图.md",
    "03-掌握度账本.md",
    "04-错题与误区.md",
    "05-作业与项目.md",
    "06-复习队列.md",
]
MARKER_START = "<!-- AI-MANAGED:START -->"
MARKER_END = "<!-- AI-MANAGED:END -->"
DATE_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


def validate_file(path: Path, errors: list[str], warnings: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing required file: {path.name}")
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        warnings.append(f"No YAML frontmatter detected: {path.name}")
    start_count = text.count(MARKER_START)
    end_count = text.count(MARKER_END)
    if start_count != 1 or end_count != 1:
        errors.append(
            f"Expected exactly one AI-MANAGED marker pair in {path.name}; "
            f"found start={start_count}, end={end_count}."
        )
    elif text.index(MARKER_START) > text.index(MARKER_END):
        errors.append(f"AI-MANAGED markers are out of order: {path.name}")


def validate_session_name(path: Path, errors: list[str]) -> None:
    if not DATE_NAME.match(path.name):
        errors.append(f"Session filename must be YYYY-MM-DD.md: {path.name}")
        return
    try:
        date.fromisoformat(path.stem)
    except ValueError:
        errors.append(f"Session filename has invalid date: {path.name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--course", required=True, help="Path to one topic course directory.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    course = Path(args.course).expanduser().resolve()
    if not course.is_dir():
        print(f"error: course directory does not exist: {course}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    for filename in REQUIRED_FILES:
        validate_file(course / filename, errors, warnings)

    sessions = course / "sessions"
    if not sessions.is_dir():
        errors.append("Missing sessions directory.")
    else:
        for session in sorted(sessions.glob("*.md")):
            validate_session_name(session, errors)
            validate_file(session, errors, warnings)

    artifacts = course / "artifacts"
    for name in ["code", "derivations", "experiments", "projects"]:
        if not (artifacts / name).is_dir():
            errors.append(f"Missing artifacts/{name} directory.")

    ledger = course / "03-掌握度账本.md"
    if ledger.exists() and "唯一真相源" not in ledger.read_text(encoding="utf-8"):
        warnings.append("Mastery ledger does not declare its source-of-truth role.")

    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Valid learning course: {course}")
    if warnings:
        print(f"Completed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
