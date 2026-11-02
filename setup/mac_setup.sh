#!/usr/bin/env bash
# One-time setup for the studio on an Apple Silicon Mac. Safe to re-run.
#   cd ~/Projects/faceless-3d-studio && bash setup/mac_setup.sh
# Installs: ffmpeg + uv (via Homebrew), Python 3.13 (managed by uv, inside .venv),
# Blender 5.2.3 as a Python module (bpy) and PyYAML. Nothing is installed system-wide
# except the two Homebrew packages; deleting the project folder removes everything else.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
echo "Project folder: $ROOT"

case "$ROOT" in
  "$HOME/Desktop"*|"$HOME/Documents"*|"$HOME/Library/Mobile Documents"*)
    echo "WARNING: this folder may be synced to iCloud. Renders write gigabytes of frames."
    echo "         Move it first:  mkdir -p ~/Projects && mv \"$ROOT\" ~/Projects/"
    ;;
esac
[ "$(uname -m)" = "arm64" ] || echo "NOTE: not an Apple Silicon Mac; renders may be slow."

if ! command -v brew >/dev/null 2>&1; then
  echo
  echo "Homebrew (the standard Mac package manager) is not installed."
  echo "Install it by pasting the one-line command from https://brew.sh into Terminal, then re-run:"
  echo "  bash setup/mac_setup.sh"
  exit 1
fi

echo "==> Installing ffmpeg and uv with Homebrew"
brew install ffmpeg uv

echo "==> Creating Python 3.13 environment in .venv"
uv venv --python 3.13 .venv

echo "==> Installing Blender 5.2.3 (bpy, ~250 MB download) and PyYAML"
uv pip install --python .venv/bin/python -r requirements.txt

echo "==> Running the doctor check and a speed test"
.venv/bin/python -m studio.doctor
