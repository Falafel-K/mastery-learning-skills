from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def run_tool(self, relative: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, relative],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_skill_package_validator_passes(self) -> None:
        result = self.run_tool("tools/validate_skill_package.py")
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        self.assertIn("passed", result.stdout.lower())

    def test_eval_validator_passes(self) -> None:
        result = self.run_tool("tools/validate_evals.py")
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        self.assertIn("passed", result.stdout.lower())

    def test_skill_uses_portable_frontmatter(self) -> None:
        text = (ROOT / "skills/deep-skills/SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: deep-skills", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertNotIn("disable-model-invocation", frontmatter)
        self.assertNotIn("allowed-tools", frontmatter)


if __name__ == "__main__":
    unittest.main()
