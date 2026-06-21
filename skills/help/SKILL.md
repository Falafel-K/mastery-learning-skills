---
name: help
description: 显示 Obsidian 互动式掌握学习系统（Mastery Learning）中所有可用指令的使用指南。(Display help information for all Mastery Learning skills and commands.)
license: MIT
compatibility: Markdown-capable agent.
---

# Mastery Learning System - Help Command

This command lists and explains all available slash commands for the interactive Mastery Learning Obsidian system.

## Command Reference Matrix

| Command | Action / Purpose | Description |
| :--- | :--- | :--- |
| **`/study [target]`** (or `/learn`) | Learning Loop | Starts or resumes an interactive study session for a specified target (e.g. `K03`, `S1/第2节` or a keyword). If omitted, teaches the automatic next objective. |
| **`/review [target]`** | Retrieval Practice | Starts a spaced repetition review session for a specified target (e.g. `K01`) or all overdue items in the queue if omitted. |
| **`/dashboard`** | Progress Report | Reads local ledgers and renders a visual progress report with ASCII progress bars, status counts, and the knowledge map. |
| **`/sync`** | Note Synchronization | Synchronizes the active session state and scores from the log to your local Obsidian Vault note files inside the designated `AI-MANAGED` boundaries. |
| **`/audit`** | Coverage Audit | Verifies that all important claims and concepts in the source materials have been successfully mapped to knowledge points and assessed. |
| **`/handoff`** | Session Hand-off | Compacts the active session state, scores, open errors, next task, and note paths into a short code block to easily resume in a new chat. |
| **`/help`** | Help Guide | Displays this guide explaining all commands and the overall Mastery Learning loop. |

## Quickstart Guide

1. Paste your study materials and type `/study` to begin learning.
2. Provide your local Obsidian Vault absolute path if you want note synchronization. Otherwise, the system runs in **Preview mode** where you can copy-paste the notes manually.
3. Finish the evaluation tasks presented by the agent to score points and advance.

## Strict File-Write Boundary & Preview Mode

To protect your local storage and keep your workspace clean, the Mastery Learning system enforces a strict boundary for filesystem writes:
- **Preview Mode (Default)**: By default, the system operates in Preview Mode. It will output all learning materials, ledger updates, error logs, and session notes directly in the chat window for you to review and copy.
- **Full Mode (Obsidian Synchronization)**: The agent will only create or modify note files on your filesystem if you explicitly provide an absolute Obsidian Vault path in your prompt (e.g. `D:\Obsidian\MyVault`). The agent is strictly forbidden from writing files to default, relative, or guess-based paths.
