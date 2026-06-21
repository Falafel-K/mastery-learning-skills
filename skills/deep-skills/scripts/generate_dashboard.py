#!/usr/bin/env python3
"""Parse the mastery ledger and print a beautiful ASCII progress report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ANSI colors for beautiful terminal output
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"


def find_ledger_file(start_path: Path) -> Path | None:
    """Scan current or parent directories to locate 03-掌握度账本.md."""
    # Check current directory
    for p in start_path.glob("**/*03-掌握度账本.md"):
        return p
    # Check parents
    for parent in start_path.parents:
        for p in parent.glob("**/*03-掌握度账本.md"):
            return p
    return None


def parse_mastery_ledger(file_path: Path) -> list[dict[str, str]] | None:
    """Parse Markdown table into a list of dictionaries."""
    if not file_path.exists():
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    rows: list[dict[str, str]] = []
    # Match markdown table row structure: | K01 | ... |
    # Group pattern to capture columns
    pattern = re.compile(r"^\s*\|\s*(K\d+)\s*\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|")
    
    for line in content.splitlines():
        match = pattern.match(line)
        if match:
            k_id = match.group(1).strip()
            name = match.group(2).strip()
            score_str = match.group(4).strip()
            status = match.group(5).strip()
            next_step = match.group(9).strip()
            
            try:
                score = int(score_str)
            except ValueError:
                score = 0
                
            rows.append({
                "id": k_id,
                "name": name,
                "score": score,
                "status": status,
                "next_step": next_step
            })
            
    return rows


def generate_progressbar(percentage: float, width: int = 30) -> str:
    """Render a progress bar using block characters."""
    filled_len = int(round(width * percentage / 100))
    bar = "█" * filled_len + "░" * (width - filled_len)
    return bar


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate learning mastery terminal dashboard.")
    parser.add_argument("--ledger", help="Path to 03-掌握度账本.md. If omitted, scans workspace.")
    args = parser.parse_args(argv)

    start_path = Path.cwd()
    ledger_path: Path | None = None

    if args.ledger:
        ledger_path = Path(args.ledger)
    else:
        ledger_path = find_ledger_file(start_path)

    if not ledger_path or not ledger_path.is_file():
        print(f"{C_RED}error: 03-掌握度账本.md not found in {start_path} or its subdirectories.{C_RESET}", file=sys.stderr)
        print("Please run this command inside a course folder or specify --ledger.", file=sys.stderr)
        return 1

    rows = parse_mastery_ledger(ledger_path)
    if rows is None:
        print(f"{C_RED}error: Failed to read or parse ledger file: {ledger_path}{C_RESET}", file=sys.stderr)
        return 1

    if not rows:
        print(f"{C_YELLOW}warning: No knowledge points (Kxx) found in the ledger.{C_RESET}")
        return 0

    total_k = len(rows)
    mastered_k = sum(1 for r in rows if r["score"] >= 3)
    blocked_k = [r for r in rows if r["status"] in ("受阻", "blocked", "BLOCKED")]
    overdue_k = [r for r in rows if r["status"] in ("待复习", "overdue", "OVERDUE")]

    percentage = (mastered_k / total_k) * 100 if total_k > 0 else 0.0

    # Group counts
    status_counts: dict[str, int] = {}
    for r in rows:
        st = r["status"]
        status_counts[st] = status_counts.get(st, 0) + 1

    # Reconfigure stdout to utf-8 if supported to prevent crashes on Windows/GBK consoles
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    # Printing Dashboard
    print(f"\n{C_BOLD}{C_CYAN}=================================================={C_RESET}")
    print(f"{C_BOLD}{C_BLUE}>>> DEEP SKILLS LEARNING DASHBOARD (学习掌握度看板) <<<{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}=================================================={C_RESET}")
    print(f"Ledger file: {C_BOLD}{ledger_path.name}{C_RESET} ({ledger_path.parent.name})")
    print(f"Total Knowledge Points: {C_BOLD}{total_k}{C_RESET}")
    print(f"Mastered (Score >= 3) : {C_BOLD}{C_GREEN}{mastered_k}{C_RESET} / {total_k}")
    
    # Progress bar
    bar_str = generate_progressbar(percentage)
    color = C_GREEN if percentage >= 80 else (C_YELLOW if percentage >= 40 else C_RED)
    print(f"Mastery Progress      : {color}[{bar_str}] {percentage:.1f}%{C_RESET}")
    print("")

    # Status Breakdown
    print(f"{C_BOLD}Status Breakdown (状态分布):{C_RESET}")
    for status, count in sorted(status_counts.items()):
        status_color = C_RESET
        if status in ("稳定掌握", "高掌握", "mastered"):
            status_color = C_GREEN
        elif status in ("学习中", "learning"):
            status_color = C_BLUE
        elif status in ("受阻", "blocked"):
            status_color = C_RED + C_BOLD
        elif status in ("待复习", "overdue"):
            status_color = C_YELLOW + C_BOLD
            
        print(f"  - {status_color}{status:<10}{C_RESET}: {count} point(s)")

    # Alerts for Blocked / Overdue
    if blocked_k:
        print(f"\n{C_BOLD}{C_RED}[!] BLOCKED POINTS (受阻知识点):{C_RESET}")
        for r in blocked_k:
            print(f"  [{C_RED}{r['id']}{C_RESET}] {C_BOLD}{r['name']}{C_RESET}")
            print(f"       Next Step: {r['next_step']}")
            
    if overdue_k:
        print(f"\n{C_BOLD}{C_YELLOW}[R] OVERDUE REVIEWS (待复习知识点):{C_RESET}")
        for r in overdue_k:
            print(f"  [{C_YELLOW}{r['id']}{C_RESET}] {r['name']} (Score: {r['score']})")

    print(f"\n{C_BOLD}{C_CYAN}=================================================={C_RESET}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
