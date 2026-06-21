from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREATE = ROOT / "skills/deep-skills/scripts/create_course.py"
SYNC = ROOT / "skills/deep-skills/scripts/sync_course.py"


class SyncToolTests(unittest.TestCase):
    def run_command(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True)

    def test_sync_actions_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            topic = "Python 文件处理"
            
            # 1. Create a new course
            create_res = self.run_command(
                [
                    sys.executable,
                    str(CREATE),
                    "--vault",
                    str(vault),
                    "--topic",
                    topic,
                    "--subject",
                    "编程",
                ]
            )
            self.assertEqual(create_res.returncode, 0, msg=create_res.stderr)
            
            course_dir = vault / "学习" / "Python-文件处理"
            self.assertTrue(course_dir.is_dir())
            
            # 2. Test update-ledger
            ledger_data = [
                {
                    "k_id": "K01",
                    "name": "文件读写",
                    "anchor": "S1 / 1.1",
                    "score": 3,
                    "status": "学习中",
                    "evidence": "能够独立编写读写代码",
                    "next_review": "2026-06-22",
                    "next_step": "学习 K02"
                }
            ]
            sync_ledger_res = self.run_command(
                [
                    sys.executable,
                    str(SYNC),
                    "--vault",
                    str(vault),
                    "--topic",
                    topic,
                    "--action",
                    "update-ledger",
                    "--data",
                    json.dumps(ledger_data)
                ]
            )
            self.assertEqual(sync_ledger_res.returncode, 0, msg=sync_ledger_res.stderr)
            
            ledger_content = (course_dir / "03-掌握度账本.md").read_text(encoding="utf-8")
            self.assertIn("K01", ledger_content)
            self.assertIn("文件读写", ledger_content)
            self.assertIn("S1 / 1.1", ledger_content)
            self.assertIn("3", ledger_content)
            self.assertIn("学习中", ledger_content)
            
            # 3. Test add-review
            review_data = {
                "review_date": "2026-06-22",
                "k_id": "K01",
                "weakness": "概念边界不清晰",
                "review_type": "回忆 + 应用",
                "pass_condition": "独立达到既定分数",
                "status": "待复习"
            }
            sync_review_res = self.run_command(
                [
                    sys.executable,
                    str(SYNC),
                    "--vault",
                    str(vault),
                    "--topic",
                    topic,
                    "--action",
                    "add-review",
                    "--data",
                    json.dumps(review_data)
                ]
            )
            self.assertEqual(sync_review_res.returncode, 0, msg=sync_review_res.stderr)
            
            review_content = (course_dir / "06-复戏队列.md" if (course_dir / "06-复戏队列.md").exists() else course_dir / "06-复习队列.md").read_text(encoding="utf-8")
            self.assertIn("K01", review_content)
            self.assertIn("2026-06-22", review_content)
            self.assertIn("概念边界不清晰", review_content)
            self.assertIn("回忆 + 应用", review_content)
            
            # 4. Test add-error
            error_data = {
                "err_id": "E01",
                "date": "2026-06-21",
                "k_id": "K01",
                "error_type": "概念混淆",
                "learner_answer": "wrong syntax",
                "core_mistake": "syntax error",
                "reason": "forgot colon",
                "correct_understanding": "use python syntax",
                "repair_task": "rewrite it",
                "rechecked": "否",
                "recheck_result": ""
            }
            sync_error_res = self.run_command(
                [
                    sys.executable,
                    str(SYNC),
                    "--vault",
                    str(vault),
                    "--topic",
                    topic,
                    "--action",
                    "add-error",
                    "--data",
                    json.dumps(error_data)
                ]
            )
            self.assertEqual(sync_error_res.returncode, 0, msg=sync_error_res.stderr)
            
            error_content = (course_dir / "04-错题与误区.md").read_text(encoding="utf-8")
            self.assertIn("E01", error_content)
            self.assertIn("wrong syntax", error_content)
            self.assertIn("forgot colon", error_content)
            
            # 5. Test append-session (create new YYYY-MM-DD.md session file)
            session_data_1 = {
                "date": "2026-06-21",
                "goals": ["掌握文件读取"],
                "k_points": ["K01"],
                "anchors": ["S1 / 1.1"],
                "evidence": [
                    {
                        "k_id": "K01",
                        "evidence_type": "Recall",
                        "summary": "Learner explained X",
                        "score": 3,
                        "result": "Passed"
                    }
                ],
                "errors": [
                    {
                        "error_link": "[[04-错题与误区#E01]]",
                        "repair_status": "Fixed"
                    }
                ],
                "artifacts": [
                    {
                        "name": "Task 1",
                        "path": "artifacts/code/solution.py",
                        "result": "Tests passed"
                    }
                ],
                "summary": {
                    "mastered": ["K01"],
                    "unstable": [],
                    "next_priority": "Study K02",
                    "review_schedule": "2026-06-22: K01"
                },
                "flashcards": [
                    {
                        "question": "What is X?",
                        "answer": "X is Y."
                    }
                ]
            }
            sync_session_1_res = self.run_command(
                [
                    sys.executable,
                    str(SYNC),
                    "--vault",
                    str(vault),
                    "--topic",
                    topic,
                    "--action",
                    "append-session",
                    "--data",
                    json.dumps(session_data_1)
                ]
            )
            self.assertEqual(sync_session_1_res.returncode, 0, msg=sync_session_1_res.stderr)
            
            session_file = course_dir / "sessions" / "2026-06-21.md"
            self.assertTrue(session_file.is_file())
            session_content = session_file.read_text(encoding="utf-8")
            self.assertIn("session_count: 1", session_content)
            self.assertIn("## 第 1 次学习", session_content)
            self.assertIn("掌握文件读取", session_content)
            self.assertIn("What is X? :: X is Y. #flashcard/Python_文件处理", session_content)
            
            # 6. Test append-session (append second session to same date file)
            session_data_2 = {
                "date": "2026-06-21",
                "goals": ["掌握文件写入"],
                "k_points": ["K02"],
                "anchors": ["S1 / 1.2"],
                "evidence": [
                    {
                        "k_id": "K02",
                        "evidence_type": "Recall",
                        "summary": "Learner explained Y",
                        "score": 4,
                        "result": "Passed"
                    }
                ],
                "errors": [],
                "artifacts": [],
                "summary": {
                    "mastered": ["K02"],
                    "unstable": [],
                    "next_priority": "Study K03",
                    "review_schedule": "2026-06-24: K02"
                },
                "flashcards": [
                    {
                        "question": "What is Y?",
                        "answer": "Y is Z."
                    }
                ]
            }
            sync_session_2_res = self.run_command(
                [
                    sys.executable,
                    str(SYNC),
                    "--vault",
                    str(vault),
                    "--topic",
                    topic,
                    "--action",
                    "append-session",
                    "--data",
                    json.dumps(session_data_2)
                ]
            )
            self.assertEqual(sync_session_2_res.returncode, 0, msg=sync_session_2_res.stderr)
            
            session_content = session_file.read_text(encoding="utf-8")
            self.assertIn("session_count: 2", session_content)
            self.assertIn("## 第 1 次学习", session_content)
            self.assertIn("## 第 2 次学习", session_content)
            self.assertIn("掌握文件读取", session_content)
            self.assertIn("掌握文件写入", session_content)
            self.assertIn("What is Y? :: Y is Z. #flashcard/Python_文件处理", session_content)


if __name__ == "__main__":
    unittest.main()
