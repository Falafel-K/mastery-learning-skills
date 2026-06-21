#!/usr/bin/env python3
"""Setup Git pre-commit hooks to automate validation on commit."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GIT_DIR = ROOT / ".git"
HOOK_FILE = GIT_DIR / "hooks" / "pre-commit"


def main() -> int:
    print("----------------------------------------")
    print("Setting up Git Pre-commit Hook...")
    print("----------------------------------------")

    if not GIT_DIR.is_dir():
        print("error: .git directory not found in workspace root.", file=sys.stderr)
        print("Please initialize git first using 'git init'.", file=sys.stderr)
        return 1

    hooks_dir = HOOK_FILE.parent
    if not hooks_dir.is_dir():
        hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_content = """#!/bin/sh
# Git pre-commit hook to validate Mastery Learning Skills package integrity.

echo "=== Running Mastery Learning Skills pre-commit validation ==="

# 1. Run package structures validator
python tools/validate_skill_package.py
if [ $? -ne 0 ]; then
  echo "error: Skill package validation failed."
  exit 1
fi

# 2. Run behavior-evaluations schema validator
python tools/validate_evals.py
if [ $? -ne 0 ]; then
  echo "error: Behavior evaluation cases validation failed."
  exit 1
fi

# 3. Run regression unit tests
python -m unittest discover -s tests -v
if [ $? -ne 0 ]; then
  echo "error: Regression tests failed."
  exit 1
fi

echo "=== All pre-commit validations passed successfully! ==="
exit 0
"""

    try:
        HOOK_FILE.write_text(hook_content, encoding="utf-8")
        # Make executable
        os.chmod(HOOK_FILE, 0o755)
        print(f"Successfully created pre-commit hook at {HOOK_FILE.relative_to(ROOT)}")
        print("Hook will run automatically before every 'git commit' to prevent invalid code.")
    except Exception as exc:
        print(f"error: Failed to write git hook: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
