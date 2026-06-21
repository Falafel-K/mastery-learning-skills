#!/usr/bin/env python3
"""Create a safe, template-backed Obsidian learning course.

This helper is local-only. It never accesses the network, deletes files, runs
shell commands, or writes outside the explicitly supplied vault/workspace.
Use --dry-run first.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "assets" / "templates"

TEMPLATE_MAP = {
    "course-home.md": "00-课程主页.md",
    "source-log.md": "01-原始资料.md",
    "knowledge-map.md": "02-知识点地图.md",
    "mastery-ledger.md": "03-掌握度账本.md",
    "error-log.md": "04-错题与误区.md",
    "assignments.md": "05-作业与项目.md",
    "review-queue.md": "06-复习队列.md",
}


def safe_topic_name(topic: str) -> str:
    """Return a filesystem-safe, human-readable folder name without traversal."""
    normalized = unicodedata.normalize("NFKC", topic).strip()
    normalized = normalized.replace("/", "-").replace("\\", "-")
    normalized = re.sub(r"[<>:\\|?*\x00-\x1f]", "-", normalized)
    normalized = re.sub(r"\s+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip(".- ")
    if not normalized or normalized in {".", ".."}:
        raise ValueError("Topic must contain at least one safe visible character.")
    return normalized[:120]


def today_for_timezone(timezone_name: str) -> str:
    try:
        return datetime.now(ZoneInfo(timezone_name)).date().isoformat()
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown timezone: {timezone_name}") from exc


def render(template: str, values: dict[str, str]) -> str:
    output = template
    for key, value in values.items():
        output = output.replace(f"{{{{{key}}}}}", value)
    return output


def ensure_within(child: Path, parent: Path) -> None:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError as exc:
        raise ValueError(f"Refusing to write outside selected vault: {child}") from exc


def planned_paths(course_dir: Path, session_date: str) -> list[Path]:
    paths = [course_dir / destination for destination in TEMPLATE_MAP.values()]
    paths.extend(
        [
            course_dir / "sessions" / f"{session_date}.md",
            course_dir / "artifacts" / "code",
            course_dir / "artifacts" / "derivations",
            course_dir / "artifacts" / "experiments",
            course_dir / "artifacts" / "projects",
        ]
    )
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, help="Confirmed path to an Obsidian Vault.")
    parser.add_argument("--topic", required=True, help="Course topic; becomes a safe folder name.")
    parser.add_argument("--subject", default="未指定", help="Subject label for frontmatter.")
    parser.add_argument("--workspace-dir", default="学习", help="Directory inside the vault for courses.")
    parser.add_argument("--timezone", default="Europe/Helsinki", help="IANA timezone used for the session date.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without creating anything.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Permit an existing course directory; only missing files are created.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        vault = Path(args.vault).expanduser().resolve()
        topic_folder = safe_topic_name(args.topic)
        workspace_name = safe_topic_name(args.workspace_dir)
        date = today_for_timezone(args.timezone)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not TEMPLATE_DIR.is_dir():
        print(f"error: templates missing: {TEMPLATE_DIR}", file=sys.stderr)
        return 2

    workspace_dir = vault / workspace_name
    course_dir = workspace_dir / topic_folder
    ensure_within(course_dir, vault)

    course_id = hashlib.sha256(f"{topic_folder}|{date}".encode("utf-8")).hexdigest()[:12]
    values = {
        "TOPIC": args.topic,
        "SUBJECT": args.subject,
        "DATE": date,
        "TIMEZONE": args.timezone,
        "COURSE_ID": course_id,
    }

    if course_dir.exists() and not args.append:
        print(
            f"error: course already exists: {course_dir}\n"
            "Use --append to create only missing template files.",
            file=sys.stderr,
        )
        return 2

    print("Planned course structure:")
    for path in planned_paths(course_dir, date):
        print(f"  {path}")

    if args.dry_run:
        print("Dry run only; no files were created.")
        return 0

    vault.mkdir(parents=True, exist_ok=True)
    workspace_dir.mkdir(exist_ok=True)
    course_dir.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []
    for template_name, destination_name in TEMPLATE_MAP.items():
        destination = course_dir / destination_name
        ensure_within(destination, vault)
        if destination.exists():
            skipped.append(destination)
            continue
        template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
        destination.write_text(render(template, values), encoding="utf-8")
        created.append(destination)

    for directory in [
        course_dir / "sessions",
        course_dir / "artifacts" / "code",
        course_dir / "artifacts" / "derivations",
        course_dir / "artifacts" / "experiments",
        course_dir / "artifacts" / "projects",
    ]:
        ensure_within(directory, vault)
        directory.mkdir(parents=True, exist_ok=True)

    session_path = course_dir / "sessions" / f"{date}.md"
    if session_path.exists():
        skipped.append(session_path)
    else:
        template = (TEMPLATE_DIR / "daily-session.md").read_text(encoding="utf-8")
        session_path.write_text(render(template, values), encoding="utf-8")
        created.append(session_path)

    print(f"Created {len(created)} file(s).")
    for path in created:
        print(f"  + {path}")
    if skipped:
        print(f"Skipped {len(skipped)} existing file(s).")
        for path in skipped:
            print(f"  = {path}")
    print("No files were deleted or overwritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
