---
name: update
description: 一键自动升级 Mastery Learning Skills 到最新版本，拉取最新的指令与教学功能。(One-click automatic update of Mastery Learning Skills to the latest version.)
license: MIT
compatibility: Markdown-capable agent; requires local execution permissions.
---

# Update Command Router

Automatically update all installed Mastery Learning Skills to the latest version from the remote repository.

## Trigger Instructions

When this command is triggered:
1. Detect the operating system (Windows or Unix/Linux).
2. Execute the online update command in the background (propose the command to the user for approval):
   - **Windows (PowerShell)**:
     ```powershell
     & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.ps1)))
     ```
   - **Unix/Linux (Bash)**:
     ```bash
     curl -fsSL https://raw.githubusercontent.com/Falafel-K/mastery-learning-skills/main/install.sh | bash
     ```
3. Inform the user that the update has started, and once completed, summarize the new features or instructions.
4. **Strict File-Write Boundary**: You MUST operate in Preview Mode and output Markdown in the chat window only, WITHOUT creating or writing any files on the filesystem, UNLESS the user has explicitly provided a target Obsidian Vault path in their prompt. Do not write to the project workspace root by default.
