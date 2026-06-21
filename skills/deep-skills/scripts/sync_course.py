#!/usr/bin/env python3
"""Sync and update learning course records safely.

This script parses and edits Markdown files in the Obsidian Vault
only within the <!-- AI-MANAGED:START --> and <!-- AI-MANAGED:END --> markers.
It supports updating the ledger, adding errors, managing the review queue,
and appending daily session logs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# AI-managed markers
MARKER_START = "<!-- AI-MANAGED:START -->"
MARKER_END = "<!-- AI-MANAGED:END -->"


def ensure_within(child: Path, parent: Path) -> None:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError as exc:
        raise ValueError(f"Refusing to access outside selected vault: {child}") from exc


def get_ai_managed_section(text: str) -> tuple[str, str, str]:
    """Split text into before, inside, and after AI-MANAGED markers."""
    start_idx = text.find(MARKER_START)
    end_idx = text.find(MARKER_END)
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        raise ValueError("Target file lacks valid AI-MANAGED markers.")
    before = text[:start_idx + len(MARKER_START)]
    inside = text[start_idx + len(MARKER_START):end_idx]
    after = text[end_idx:]
    return before, inside, after


def parse_markdown_table(table_text: str) -> tuple[list[str], list[list[str]]]:
    """Parse Markdown table headers and rows."""
    lines = [line.strip() for line in table_text.strip().splitlines() if line.strip()]
    if len(lines) < 2:
        return [], []
    # Split by '|' and strip cells, discarding the empty outer cells
    headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
    rows = []
    for line in lines[2:]:
        row = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(row)
    return headers, rows


def format_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    """Format headers and rows as a Markdown table."""
    header_line = "| " + " | ".join(headers) + " |"
    # Align score column to right, others default
    separator_line = "| " + " | ".join(["---" if h != "分数 0-5" else "---:" for h in headers]) + " |"
    row_lines = []
    for row in rows:
        row_lines.append("| " + " | ".join(row) + " |")
    return "\n".join([header_line, separator_line] + row_lines)


def update_ledger_table(inside_text: str, updates: list[dict]) -> str:
    """Update or append rows in the mastery ledger table."""
    table_pattern = re.compile(r"(\| K编号 \|[^\n]*\n\|[^\n]*\n(?:\|[^\n]*\n*)*)")
    match = table_pattern.search(inside_text)
    
    headers = ["K编号", "知识点", "资料锚点", "分数 0-5", "状态", "已有证据", "错误链接", "下次复习", "下一步"]
    rows = []
    
    if match:
        table_text = match.group(1)
        headers, rows = parse_markdown_table(table_text)
    
    # Track row index by K编号
    row_map = {row[0]: idx for idx, row in enumerate(rows) if row}
    
    HEADER_TO_KEY = {
        "知识点": "name",
        "资料锚点": "anchor",
        "分数 0-5": "score",
        "状态": "status",
        "已有证据": "evidence",
        "错误链接": "error_link",
        "下次复习": "next_review",
        "下一步": "next_step"
    }
    
    for up in updates:
        k_id = up.get("k_id")
        if not k_id:
            continue
        
        # Build row cells mapping
        row_cells = {
            "K编号": k_id,
            "知识点": up.get("name", ""),
            "资料锚点": up.get("anchor", ""),
            "分数 0-5": str(up.get("score", "0")),
            "状态": up.get("status", "未学"),
            "已有证据": up.get("evidence", "无"),
            "错误链接": up.get("error_link", ""),
            "下次复习": up.get("next_review", ""),
            "下一步": up.get("next_step", "")
        }
        
        row_list = [row_cells[h] for h in headers]
        
        if k_id in row_map:
            idx = row_map[k_id]
            # Merge with existing row values for omitted fields
            for i, h in enumerate(headers):
                if h == "K编号":
                    continue
                key = HEADER_TO_KEY.get(h)
                if key and key not in up:
                    row_list[i] = rows[idx][i]
            rows[idx] = row_list
        else:
            rows.append(row_list)
            row_map[k_id] = len(rows) - 1
            
    # Remove dummy row if populated
    rows = [r for r in rows if r and (r[0] != "K01" or r[1] != "待解析")]
    if not rows:
        rows.append(["K01", "待解析", "S1 / 待定位", "0", "未学", "无", "", "", "建立知识点定义"])
        
    new_table = format_markdown_table(headers, rows)
    if match:
        return inside_text.replace(match.group(1), new_table + "\n")
    else:
        return inside_text.strip() + "\n\n" + new_table + "\n"


def update_review_table(inside_text: str, updates: list[dict]) -> str:
    """Update or append rows in the review queue table."""
    table_pattern = re.compile(r"(\| 复习日期 \|[^\n]*\n\|[^\n]*\n(?:\|[^\n]*\n*)*)")
    match = table_pattern.search(inside_text)
    
    headers = ["复习日期", "K编号", "当前薄弱点", "复习方式", "通过条件", "状态"]
    rows = []
    
    if match:
        table_text = match.group(1)
        headers, rows = parse_markdown_table(table_text)
        
    REVIEW_HEADER_TO_KEY = {
        "复习日期": "review_date",
        "K编号": "k_id",
        "当前薄弱点": "weakness",
        "复习方式": "review_type",
        "通过条件": "pass_condition",
        "状态": "status"
    }
        
    for up in updates:
        rev_date = up.get("review_date")
        k_id = up.get("k_id")
        if not rev_date or not k_id:
            continue
            
        row_cells = {
            "复习日期": rev_date,
            "K编号": k_id,
            "当前薄弱点": up.get("weakness", ""),
            "复习方式": up.get("review_type", ""),
            "通过条件": up.get("pass_condition", ""),
            "状态": up.get("status", "待复习")
        }
        row_list = [row_cells[h] for h in headers]
        
        # Check matching row by (Date, K编号)
        found = False
        for idx, r in enumerate(rows):
            if r and r[0] == rev_date and r[1] == k_id:
                # Merge
                for i, h in enumerate(headers):
                    if h in ("复习日期", "K编号"):
                        continue
                    key = REVIEW_HEADER_TO_KEY.get(h)
                    if key and key not in up:
                        row_list[i] = r[i]
                rows[idx] = row_list
                found = True
                break
        if not found:
            rows.append(row_list)
            
    # Filter placeholder
    rows = [r for r in rows if r and (r[0] != "待安排" or r[1] != "K01")]
    if not rows:
        rows.append(["待安排", "K01", "待确认", "回忆 + 应用", "独立达到既定分数", "待复习"])
        
    new_table = format_markdown_table(headers, rows)
    if match:
        return inside_text.replace(match.group(1), new_table + "\n")
    else:
        return inside_text.strip() + "\n\n" + new_table + "\n"


def update_errors_file(inside_text: str, err_data: dict) -> str:
    """Update or append an error block in the error log file."""
    err_id = err_data.get("err_id")
    if not err_id:
        return inside_text
        
    content_block = f"""## {err_id}
- 日期：{err_data.get('date', '')}
- 关联知识点：{err_data.get('k_id', '')}
- 错误类型：{err_data.get('error_type', '')}
- 我的原回答：{err_data.get('learner_answer', '')}
- 错误的最小核心：{err_data.get('core_mistake', '')}
- 为什么会错：{err_data.get('reason', '')}
- 正确理解：{err_data.get('correct_understanding', '')}
- 修复练习：{err_data.get('repair_task', '')}
- 是否已复验：{err_data.get('rechecked', '否')}
- 复验结果：{err_data.get('recheck_result', '')}
"""
    content_block = content_block.strip() + "\n\n"
    
    # Regex to extract error blocks starting with ## err_id
    pattern = rf"(## {re.escape(err_id)}\n.*?(?=\n## |\n<!-- AI-MANAGED:END -->|$))"
    match = re.search(pattern, inside_text, re.DOTALL)
    if match:
        inside_text = inside_text.replace(match.group(1), content_block)
    else:
        inside_text = inside_text.strip() + "\n\n" + content_block
        
    return inside_text.strip() + "\n"


def format_session_block(n: int, session_data: dict, topic: str) -> str:
    """Format structured session details as a markdown block."""
    goals = "\n".join(f"- {g}" for g in session_data.get("goals", [])) or "- "
    k_points = "\n".join(f"- {k}" for k in session_data.get("k_points", [])) or "- "
    anchors = "\n".join(f"- {a}" for a in session_data.get("anchors", [])) or "- "
    
    # Evidence Table
    evidence_headers = ["K编号", "证据类型", "我的回答/产出摘要", "分数 0-5", "结论"]
    evidence_rows = []
    for ev in session_data.get("evidence", []):
        evidence_rows.append([
            ev.get("k_id", ""),
            ev.get("evidence_type", ""),
            ev.get("summary", ""),
            str(ev.get("score", "0")),
            ev.get("result", "")
        ])
    evidence_table = format_markdown_table(evidence_headers, evidence_rows) if evidence_rows else "| K编号 | 证据类型 | 我的回答/产出摘要 | 分数 0-5 | 结论 |\n|---|---|---|---:|---|\n|  |  |  |  |  |"
    
    # Errors
    errors_list = []
    for err in session_data.get("errors", []):
        errors_list.append(f"- 关联错题：{err.get('error_link', '')}\n- 修复结果：{err.get('repair_status', '')}")
    errors_str = "\n".join(errors_list) if errors_list else "- 关联错题：\n- 修复结果："
    
    # Artifacts
    art_list = []
    for art in session_data.get("artifacts", []):
        art_list.append(f"- 任务：{art.get('name', '')}\n- 产物路径：{art.get('path', '')}\n- 验收/测试结果：{art.get('result', '')}")
    art_str = "\n".join(art_list) if art_list else "- 任务：\n- 产物路径：\n- 验收/测试结果："
    
    # Flashcards
    flashcards_list = []
    for fc in session_data.get("flashcards", []):
        flashcards_list.append(f"{fc.get('question', '')} :: {fc.get('answer', '')} #flashcard/{topic.replace(' ', '_')}")
    flashcards_str = "\n".join(flashcards_list) if flashcards_list else ""
    flashcards_heading = f"### 闪卡制作 (Spaced Repetition)\n<!-- #flashcard/{topic} 可在此区域下方追加闪卡，格式为：问题 :: 答案 -->"
    if flashcards_str:
        flashcards_section = f"{flashcards_heading}\n{flashcards_str}"
    else:
        flashcards_section = flashcards_heading
        
    summary = session_data.get("summary", {})
    mastered = ", ".join(summary.get("mastered", [])) or "无"
    unstable = ", ".join(summary.get("unstable", [])) or "无"
    next_priority = summary.get("next_priority", "")
    review_schedule = summary.get("review_schedule", "")
    
    block = f"""## 第 {n} 次学习

### 本次目标
{goals}

### 本次涉及知识点
{k_points}

### 资料锚点
{anchors}

### 学习证据与评分
{evidence_table}

### 错误与修复
{errors_str}

### 作业与产物
{art_str}

{flashcards_section}

### 本次结束状态
- 已真正掌握：{mastered}
- 仍然不稳：{unstable}
- 下次优先任务：{next_priority}
- 复习安排：{review_schedule}
"""
    return block.strip() + "\n"


def handle_append_session(vault: Path, course_dir: Path, topic: str, date_str: str, timezone: str, session_data: dict, dry_run: bool) -> None:
    session_file = course_dir / "sessions" / f"{date_str}.md"
    ensure_within(session_file, vault)
    
    # Initialize session file if missing
    if not session_file.exists():
        template_file = Path(__file__).resolve().parents[1] / "assets" / "templates" / "daily-session.md"
        if not template_file.is_file():
            raise FileNotFoundError(f"Missing templates/daily-session.md: {template_file}")
        template_text = template_file.read_text(encoding="utf-8")
        initialized_text = template_text.replace("{{TOPIC}}", topic).replace("{{DATE}}", date_str).replace("{{TIMEZONE}}", timezone)
        
        # Write format session block 1
        before, _, after = get_ai_managed_section(initialized_text)
        session_content = format_session_block(1, session_data, topic)
        final_text = before + "\n" + session_content + after
        
        if not dry_run:
            session_file.parent.mkdir(parents=True, exist_ok=True)
            session_file.write_text(final_text, encoding="utf-8")
        print(f"Action: Created new session file {session_file.name} with 第 1 次学习")
        return
        
    # Read existing
    text = session_file.read_text(encoding="utf-8")
    before, inside, after = get_ai_managed_section(text)
    
    # Check current session count in frontmatter
    count_match = re.search(r"session_count:\s*(\d+)", before)
    current_count = int(count_match.group(1)) if count_match else 1
    next_count = current_count + 1
    
    # Check if current session is placeholder / empty (goals is just "- " or empty)
    is_placeholder = False
    if current_count == 1:
        goals_match = re.search(r"### 本次目标\s*\n-\s*\n", inside)
        if goals_match:
            is_placeholder = True
            
    if is_placeholder:
        # Overwrite 第 1 次学习 in-place
        inside_updated = format_session_block(1, session_data, topic)
        print(f"Action: Overwriting placeholder session count 1 in {session_file.name}")
    else:
        # Append 第 N 次学习
        inside_updated = inside.strip() + "\n\n" + format_session_block(next_count, session_data, topic)
        # Update session_count in frontmatter
        if count_match:
            before = before.replace(count_match.group(0), f"session_count: {next_count}")
        print(f"Action: Appended session count {next_count} to {session_file.name}")
        
    final_text = before + "\n" + inside_updated + after
    if not dry_run:
        session_file.write_text(final_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, help="Path to Obsidian Vault root.")
    parser.add_argument("--topic", required=True, help="Course topic name.")
    parser.add_argument("--workspace-dir", default="学习", help="Directory in the vault for learning records.")
    parser.add_argument("--timezone", default="Europe/Helsinki", help="IANA Timezone.")
    parser.add_argument("--action", required=True, choices=["update-ledger", "add-review", "add-error", "append-session"], help="Sync action.")
    parser.add_argument("--data", required=True, help="JSON string or file path containing data payload.")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without writing files.")
    
    args = parser.parse_args()
    
    try:
        # Parse payload
        try:
            payload = json.loads(args.data)
        except json.JSONDecodeError:
            # Try loading as file path
            data_path = Path(args.data)
            if data_path.is_file():
                payload = json.loads(data_path.read_text(encoding="utf-8"))
            else:
                raise ValueError("Data argument must be a valid JSON string or existing file path.")
                
        vault = Path(args.vault).expanduser().resolve()
        
        # Sanitize topic directory name (identical to create_course.py)
        normalized = re.sub(r"[<>:\\|?*\x00-\x1f/\\]", "-", args.topic).strip(".- ")
        normalized = re.sub(r"\s+", "-", normalized)
        topic_folder = re.sub(r"-+", "-", normalized)[:120]
        
        course_dir = vault / args.workspace_dir / topic_folder
        
        if not course_dir.exists() and not args.dry_run:
            print(f"error: course directory does not exist: {course_dir}", file=sys.stderr)
            return 2
            
        if args.action == "update-ledger":
            ledger_file = course_dir / "03-掌握度账本.md"
            ensure_within(ledger_file, vault)
            text = ledger_file.read_text(encoding="utf-8")
            before, inside, after = get_ai_managed_section(text)
            
            updates = payload if isinstance(payload, list) else [payload]
            inside_new = update_ledger_table(inside, updates)
            final_text = before + inside_new + after
            
            if not args.dry_run:
                ledger_file.write_text(final_text, encoding="utf-8")
            print(f"Action: Updated ledger file {ledger_file.name}")
            
        elif args.action == "add-review":
            review_file = course_dir / "06-复习队列.md"
            ensure_within(review_file, vault)
            text = review_file.read_text(encoding="utf-8")
            before, inside, after = get_ai_managed_section(text)
            
            updates = payload if isinstance(payload, list) else [payload]
            inside_new = update_review_table(inside, updates)
            final_text = before + inside_new + after
            
            if not args.dry_run:
                review_file.write_text(final_text, encoding="utf-8")
            print(f"Action: Updated review queue file {review_file.name}")
            
        elif args.action == "add-error":
            error_file = course_dir / "04-错题与误区.md"
            ensure_within(error_file, vault)
            text = error_file.read_text(encoding="utf-8")
            before, inside, after = get_ai_managed_section(text)
            
            inside_new = update_errors_file(inside, payload)
            final_text = before + inside_new + after
            
            if not args.dry_run:
                error_file.write_text(final_text, encoding="utf-8")
            print(f"Action: Updated error log file {error_file.name}")
            
        elif args.action == "append-session":
            date_str = payload.get("date", datetime.now().strftime("%Y-%m-%d"))
            handle_append_session(vault, course_dir, args.topic, date_str, args.timezone, payload, args.dry_run)
            
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
        
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
