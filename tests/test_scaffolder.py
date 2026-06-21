from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDER = ROOT / "skills/skill-scaffolder/scripts/scaffold_skill.py"
VALIDATOR = ROOT / "tools/validate_skill_package.py"


class ScaffolderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_skill_name = "test-temp-scaffolded-skill"
        self.temp_skill_dir = ROOT / "skills" / self.temp_skill_name
        self.cleanup_temp_skill()

    def tearDown(self) -> None:
        self.cleanup_temp_skill()

    def cleanup_temp_skill(self) -> None:
        if self.temp_skill_dir.exists():
            shutil.rmtree(self.temp_skill_dir)

    def run_command(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True)

    def test_dry_run_does_not_create_anything(self) -> None:
        result = self.run_command(
            [
                sys.executable,
                str(SCAFFOLDER),
                "--name",
                self.temp_skill_name,
                "--description",
                "A very detailed description of at least forty characters long for the mock skill.",
                "--commands",
                json.dumps(["/mock-command"]),
                "--dry-run",
            ]
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertFalse(self.temp_skill_dir.exists())
        self.assertIn("Dry-run:", result.stdout)

    def test_scaffold_and_validate_workflow(self) -> None:
        # 1. Run scaffold command
        description = "A very detailed description of at least forty characters long for the mock skill."
        scaffold_res = self.run_command(
            [
                sys.executable,
                str(SCAFFOLDER),
                "--name",
                self.temp_skill_name,
                "--description",
                description,
                "--commands",
                json.dumps(["/mock-command-1", "/mock-command-2"]),
            ]
        )
        self.assertEqual(scaffold_res.returncode, 0, msg=scaffold_res.stderr)
        self.assertTrue(self.temp_skill_dir.is_dir())
        
        skill_file = self.temp_skill_dir / "SKILL.md"
        self.assertTrue(skill_file.is_file())
        
        # Check contents
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn(f"name: {self.temp_skill_name}", content)
        self.assertIn(description, content)
        self.assertIn("/mock-command-1", content)
        self.assertIn("/mock-command-2", content)
        
        # 2. Validate the scaffolded skill using tools/validate_skill_package.py
        validate_res = self.run_command(
            [
                sys.executable,
                str(VALIDATOR),
                "--skill-dir",
                str(self.temp_skill_dir),
            ]
        )
        self.assertEqual(validate_res.returncode, 0, msg=validate_res.stderr + validate_res.stdout)
        self.assertIn("passed", validate_res.stdout.lower())

    def test_scaffold_already_exists_fails(self) -> None:
        # Create folder
        self.temp_skill_dir.mkdir(parents=True, exist_ok=True)
        (self.temp_skill_dir / "SKILL.md").write_text("dummy", encoding="utf-8")
        
        result = self.run_command(
            [
                sys.executable,
                str(SCAFFOLDER),
                "--name",
                self.temp_skill_name,
                "--description",
                "A very detailed description of at least forty characters long for the mock skill.",
            ]
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
