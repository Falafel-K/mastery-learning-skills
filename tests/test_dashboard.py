from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

# Import the parsing function from scripts
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "deep-skills" / "scripts"))
from generate_dashboard import parse_mastery_ledger, find_ledger_file, generate_progressbar


class DashboardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_parse_valid_ledger(self) -> None:
        ledger_file = self.temp_dir / "03-掌握度账本.md"
        ledger_content = """---
type: mastery-ledger
topic: "Test Topic"
---

# 掌握度账本

<!-- AI-MANAGED:START -->
| K编号 | 知识点 | 资料锚点 | 分数 0-5 | 状态 | 已有证据 | 错误链接 | 下次复习 | 下一步 |
|---|---|---|---:|---|---|---|---|---|
| K01 | Test Point One | S1 / A | 3 | 稳定掌握 | Validated | | | Continue |
| K02 | Test Point Two | S1 / B | 1 | 学习中 | None | | | Learn |
<!-- AI-MANAGED:END -->
"""
        ledger_file.write_text(ledger_content, encoding="utf-8")
        
        rows = parse_mastery_ledger(ledger_file)
        self.assertIsNotNone(rows)
        self.assertEqual(len(rows), 2)
        
        self.assertEqual(rows[0]["id"], "K01")
        self.assertEqual(rows[0]["name"], "Test Point One")
        self.assertEqual(rows[0]["score"], 3)
        self.assertEqual(rows[0]["status"], "稳定掌握")
        self.assertEqual(rows[0]["next_step"], "Continue")
        
        self.assertEqual(rows[1]["id"], "K02")
        self.assertEqual(rows[1]["name"], "Test Point Two")
        self.assertEqual(rows[1]["score"], 1)
        self.assertEqual(rows[1]["status"], "学习中")
        self.assertEqual(rows[1]["next_step"], "Learn")

    def test_parse_empty_or_missing_ledger(self) -> None:
        missing_file = self.temp_dir / "missing.md"
        self.assertIsNone(parse_mastery_ledger(missing_file))

    def test_generate_progressbar(self) -> None:
        self.assertEqual(generate_progressbar(0, 10), "░" * 10)
        self.assertEqual(generate_progressbar(50, 10), "█████░░░░░")
        self.assertEqual(generate_progressbar(100, 10), "█" * 10)


if __name__ == "__main__":
    unittest.main()
