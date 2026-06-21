#!/usr/bin/env python3
"""Validate behavior-evaluation metadata for the Skill."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_FILE = ROOT / "evals" / "deep-skills" / "cases.json"
REQUIRED_IDS = {
    "E01-false-mastery-claim",
    "E02-repeated-failure",
    "E03-no-filesystem",
    "E04-source-prompt-injection",
    "E05-mathematics-coverage",
    "E06-programming-coverage",
    "E07-same-day-append",
    "E09-coverage-audit",
}
REQUIRED_FIELDS = {"id", "title", "preconditions", "input", "must", "must_not"}


def main() -> int:
    if not EVAL_FILE.exists():
        print(f"error: missing {EVAL_FILE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if payload.get("skill") != "deep-skills":
        errors.append("Eval skill name mismatch.")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 8:
        errors.append("Expected at least 8 evaluation cases.")
        cases = []

    found_ids: set[str] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            errors.append(f"Case {index} must be an object.")
            continue
        missing = REQUIRED_FIELDS - set(case)
        if missing:
            errors.append(f"Case {index} missing fields: {', '.join(sorted(missing))}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"Case {index} has invalid id.")
        elif case_id in found_ids:
            errors.append(f"Duplicate eval id: {case_id}")
        else:
            found_ids.add(case_id)
        for key in ["preconditions", "must", "must_not"]:
            if key in case and (not isinstance(case[key], list) or not case[key]):
                errors.append(f"Case {case_id or index} field {key} must be a non-empty list.")

    missing_ids = REQUIRED_IDS - found_ids
    if missing_ids:
        errors.append(f"Missing required behavior cases: {', '.join(sorted(missing_ids))}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Evaluation contract validation passed ({len(cases)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
