#!/bin/bash
# Cross-platform installer shell script to link or download Mastery Learning Skills packages.

set -e

# Default destination directory for agent skills
DEFAULT_DEST="$HOME/.agents/skills"
DEST="$DEFAULT_DEST"

show_help() {
  echo "Usage: ./install.sh [options]"
  echo ""
  echo "Options:"
  echo "  -d, --dest <dir>   Set the target destination directory (default: $DEFAULT_DEST)"
  echo "  -h, --help         Show this help message"
  echo ""
}

# Parse CLI arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -d|--dest) DEST="$2"; shift ;;
    -h|--help) show_help; exit 0 ;;
    *) echo "Unknown option: $1"; show_help; exit 1 ;;
  esac
  shift
done

# Ensure the destination directory exists
if [ ! -d "$DEST" ]; then
  echo "Creating directory: $DEST"
  mkdir -p "$DEST"
fi

# Determine if running in online piped mode or local mode
LOCAL_MODE=true
if [ ! -f "${BASH_SOURCE[0]}" ] || [ ! -d "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills" ]; then
  LOCAL_MODE=false
fi

echo "----------------------------------------"
echo "Mastery Learning Skills Installer"
echo "----------------------------------------"
echo "Target directory: $DEST"

if [ "$LOCAL_MODE" = true ]; then
  SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  echo "Mode: Local (Developer Symlink)"
  echo "Source directory: $SRC_DIR"
  echo ""
  
  # Create symlinks
  for skill in "mastery-learning-obsidian" "skill-scaffolder"; do
    SKILL_SRC="$SRC_DIR/skills/$skill"
    SKILL_DEST="$DEST/$skill"

    if [ -d "$SKILL_SRC" ]; then
      echo "Linking: $skill -> $SKILL_DEST"
      # Remove existing link/file if it exists
      rm -rf "$SKILL_DEST"
      ln -sf "$SKILL_SRC" "$SKILL_DEST"
    else
      echo "Warning: Source skill package not found at $SKILL_SRC"
    fi
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
    exit 1
  fi
  
  echo "Extracting packages..."
  if command -v unzip >/dev/null 2>&1; then
    unzip -q "$ZIP_PATH" -d "$TEMP_DIR"
  else
    echo "Error: unzip command was not found. Please install unzip first." >&2
    exit 1
  fi
  
  EXTRACTED_DIR="$TEMP_DIR/mastery-learning-skills-main"
  for skill in "mastery-learning-obsidian" "skill-scaffolder"; do
    SKILL_SRC="$EXTRACTED_DIR/skills/$skill"
    SKILL_DEST="$DEST/$skill"
    if [ -d "$SKILL_SRC" ]; then
      echo "Copying: $skill -> $SKILL_DEST"
      rm -rf "$SKILL_DEST"
      cp -r "$SKILL_SRC" "$SKILL_DEST"
    else
      echo "Warning: Package $skill not found in archive."
    fi
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
