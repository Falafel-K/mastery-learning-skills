from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREATE = ROOT / "skills/deep-skills/scripts/create_course.py"
VALIDATE = ROOT / "skills/deep-skills/scripts/validate_learning_vault.py"


class VaultValidatorTests(unittest.TestCase):
    def run_command(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True)

    def test_dry_run_does_not_create_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            result = self.run_command(
                [
                    sys.executable,
                    str(CREATE),
                    "--vault",
                    str(vault),
                    "--topic",
                    "数学-极限",
                    "--dry-run",
                ]
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertFalse((vault / "学习").exists())
            self.assertIn("Dry run", result.stdout)

    def test_create_then_validate_course(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            create = self.run_command(
                [
                    sys.executable,
                    str(CREATE),
                    "--vault",
                    str(vault),
                    "--topic",
                    "Python 文件处理",
                    "--subject",
                    "编程",
                    "--timezone",
                    "Europe/Helsinki",
                ]
            )
            self.assertEqual(create.returncode, 0, msg=create.stderr)
            course = vault / "学习" / "Python-文件处理"
            self.assertTrue(course.is_dir())
            validate = self.run_command([sys.executable, str(VALIDATE), "--course", str(course)])
            self.assertEqual(validate.returncode, 0, msg=validate.stderr + validate.stdout)
            self.assertIn("Valid learning course", validate.stdout)

    def test_existing_course_requires_append(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            args = [sys.executable, str(CREATE), "--vault", str(vault), "--topic", "测试主题"]
            first = self.run_command(args)
            self.assertEqual(first.returncode, 0, msg=first.stderr)
            second = self.run_command(args)
            self.assertEqual(second.returncode, 2)
            append = self.run_command(args + ["--append"])
            self.assertEqual(append.returncode, 0, msg=append.stderr)
            self.assertIn("Skipped", append.stdout)


if __name__ == "__main__":
    unittest.main()
