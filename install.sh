#!/bin/bash
# Cross-platform installer shell script to link Deep Skills packages.

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

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "----------------------------------------"
echo "Deep Skills Installer"
echo "----------------------------------------"
echo "Source directory: $SRC_DIR"
echo "Target directory: $DEST"
echo ""

# Ensure the destination directory exists
if [ ! -d "$DEST" ]; then
  echo "Creating directory: $DEST"
  mkdir -p "$DEST"
fi

# Create symlinks
for skill in "deep-skills" "skill-scaffolder"; do
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

echo ""
echo "Successfully linked Deep Skills!"
echo "You can now use these skills in your Agent workspace."
echo "----------------------------------------"
