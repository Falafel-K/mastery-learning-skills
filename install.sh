#!/bin/bash
# Cross-platform installer shell script to link or download Mastery Learning Skills packages.

set -e

# Target paths for installation
TARGET_PATHS=()

show_help() {
  echo "Usage: ./install.sh [options]"
  echo ""
  echo "Options:"
  echo "  -d, --dest <dir>   Set the target destination directory (default: auto-detected)"
  echo "  -u, --uninstall    Uninstall/remove Mastery Learning Skills from target/detected directories"
  echo "  -h, --help         Show this help message"
  echo ""
}

# Parse CLI arguments
DEST=""
UNINSTALL=false
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -d|--dest) DEST="$2"; shift ;;
    -u|--uninstall) UNINSTALL=true ;;
    -h|--help) show_help; exit 0 ;;
    *) echo "Unknown option: $1"; show_help; exit 1 ;;
  esac
  shift
done

# Skills to handle
SKILLS=("mastery-learning-obsidian" "skill-scaffolder" "study" "review" "dashboard" "sync" "audit" "handoff" "help")

# Auto-detect target paths if DEST is not specified
if [ -n "$DEST" ]; then
  TARGET_PATHS+=("$DEST")
else
  FOUND_ANY=false
  
  # 1. Gemini / Antigravity
  GEMINI_DIR="$HOME/.gemini/config"
  if [ -d "$GEMINI_DIR" ]; then
    TARGET_PATHS+=("$GEMINI_DIR/skills")
    FOUND_ANY=true
  fi
  
  # 2. Claude Code
  CLAUDE_DIR="$HOME/.claude"
  if [ -d "$CLAUDE_DIR" ]; then
    TARGET_PATHS+=("$CLAUDE_DIR/skills")
    FOUND_ANY=true
  fi
  
  # 3. Legacy / Codex / General agents (include old path for cleanup/compatibility)
  AGENTS_DIR="$HOME/.agents"
  if [ -d "$AGENTS_DIR" ]; then
    TARGET_PATHS+=("$AGENTS_DIR/skills")
    FOUND_ANY=true
  fi
  
  # Fallback if none exist
  if [ "$FOUND_ANY" = false ]; then
    TARGET_PATHS+=("$HOME/.gemini/config/skills")
    TARGET_PATHS+=("$HOME/.agents/skills")
  fi
fi

# Determine if running in online piped mode or local mode
LOCAL_MODE=true
if [ ! -f "${BASH_SOURCE[0]}" ] || [ ! -d "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills" ]; then
  LOCAL_MODE=false
fi

if [ "$UNINSTALL" = true ]; then
  echo "----------------------------------------"
  echo "Mastery Learning Skills - Uninstall Mode"
  echo "----------------------------------------"
  
  for target in "${TARGET_PATHS[@]}"; do
    echo "Checking target directory: $target"
    if [ -d "$target" ]; then
      for skill in "${SKILLS[@]}"; do
        SKILL_DEST="$target/$skill"
        if [ -e "$SKILL_DEST" ] || [ -L "$SKILL_DEST" ]; then
          echo "Removing: $SKILL_DEST"
          rm -rf "$SKILL_DEST"
        fi
      done
      # Clean up empty parent directory if it contains no other files/folders
      if [ -z "$(ls -A "$target" 2>/dev/null)" ]; then
        echo "Removing empty parent directory: $target"
        rmdir "$target" 2>/dev/null || true
      fi
    fi
  done
  
  echo ""
  echo "Successfully uninstalled Mastery Learning Skills!"
  echo "All configured links and folders have been cleared."
  echo "----------------------------------------"
  exit 0
fi

echo "----------------------------------------"
echo "Mastery Learning Skills Installer"
echo "----------------------------------------"
echo "Target directories:"
for target in "${TARGET_PATHS[@]}"; do
  echo "  - $target"
done
echo ""

if [ "$LOCAL_MODE" = true ]; then
  SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  echo "Mode: Local (Developer Symlink)"
  echo "Source directory: $SRC_DIR"
  echo ""
  
  # Create symlinks
  for target in "${TARGET_PATHS[@]}"; do
    if [ ! -d "$target" ]; then
      echo "Creating directory: $target"
      mkdir -p "$target"
    fi
    for skill in "${SKILLS[@]}"; do
      SKILL_SRC="$SRC_DIR/skills/$skill"
      SKILL_DEST="$target/$skill"

      if [ -d "$SKILL_SRC" ]; then
        echo "Linking: $skill -> $SKILL_DEST"
        # Remove existing link/file if it exists
        rm -rf "$SKILL_DEST"
        ln -sf "$SKILL_SRC" "$SKILL_DEST"
      else
        echo "Warning: Source skill package not found at $SKILL_SRC"
      fi
    done
  done
else
  echo "Mode: Online (Auto-download & Copy)"
  echo ""
  
  # Create a secure temp directory
  TEMP_DIR=$(mktemp -d -t mastery-install-XXXXXXXXXX)
  ZIP_PATH="$TEMP_DIR/archive.zip"
  
  echo "Downloading latest packages from GitHub..."
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "https://github.com/Falafel-K/mastery-learning-skills/archive/refs/heads/main.zip" -o "$ZIP_PATH"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$ZIP_PATH" "https://github.com/Falafel-K/mastery-learning-skills/archive/refs/heads/main.zip"
  else
    echo "Error: Neither curl nor wget was found. Cannot download packages." >&2
    rm -rf "$TEMP_DIR"
    exit 1
  fi
  
  echo "Extracting packages..."
  if command -v unzip >/dev/null 2>&1; then
    unzip -q "$ZIP_PATH" -d "$TEMP_DIR"
  else
    echo "Error: unzip command was not found. Please install unzip first." >&2
    rm -rf "$TEMP_DIR"
    exit 1
  fi
  
  EXTRACTED_DIR="$TEMP_DIR/mastery-learning-skills-main"
  
  for target in "${TARGET_PATHS[@]}"; do
    if [ ! -d "$target" ]; then
      echo "Creating directory: $target"
      mkdir -p "$target"
    fi
    for skill in "${SKILLS[@]}"; do
      SKILL_SRC="$EXTRACTED_DIR/skills/$skill"
      SKILL_DEST="$target/$skill"
      if [ -d "$SKILL_SRC" ]; then
        echo "Copying: $skill -> $SKILL_DEST"
        rm -rf "$SKILL_DEST"
        cp -r "$SKILL_SRC" "$SKILL_DEST"
      else
        echo "Warning: Package $skill not found in archive."
      fi
    done
  done
  
  # Cleanup temp directory
  rm -rf "$TEMP_DIR"
fi

echo ""
echo "Successfully installed Mastery Learning Skills!"
echo "Four Pillars Architecture active:"
echo "  - Vocabulary aligned via CONTEXT.md in project root."
echo "  - User/Model invocation triggers mapped (see docs/invocation.md)."
echo "  - Soft degradation storage rules defined (see docs/adr/0001-mastery-storage-soft-degradation.md)."
echo "You can now use these skills in your Agent workspace."
echo "----------------------------------------"
