#!/usr/bin/env bash
set -euo pipefail

# SolidFlow Desktop: macOS .app bundle build script with progress logging.
#
# Output:
# - dist/SolidFlow.app
# - build_logs/build-macos-app-YYYYmmdd-HHMMSS.log

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LOG_DIR="$ROOT_DIR/build_logs"
mkdir -p "$LOG_DIR"

TS="$(date +"%Y%m%d-%H%M%S")"
LOG_FILE="$LOG_DIR/build-macos-app-$TS.log"

exec > >(tee -a "$LOG_FILE") 2>&1

step() {
  echo
  echo "==> $1"
}

die() {
  echo
  echo "ERROR: $1"
  echo "Log: $LOG_FILE"
  exit 1
}

step "Environment"
echo "Project: $ROOT_DIR"
echo "Date: $(date)"
echo "uname: $(uname -a)"

if [[ "$(uname -s)" != "Darwin" ]]; then
  die "This script is intended to run on macOS (Darwin)."
fi

if ! command -v python >/dev/null 2>&1; then
  die "python not found in PATH."
fi

PY_VER="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
PY_MAJ_MIN="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "python: $(command -v python)"
echo "python version: $PY_VER"

if [[ "$PY_MAJ_MIN" != "3.10" && "$PY_MAJ_MIN" != "3.11" && "$PY_MAJ_MIN" != "3.12" ]]; then
  die "Python 3.10+ is required. Current: $PY_VER"
fi

step "Create/activate venv"
if [[ ! -d "$ROOT_DIR/venv" ]]; then
  python -m venv venv
fi

# shellcheck disable=SC1091
source "$ROOT_DIR/venv/bin/activate"
echo "venv python: $(command -v python)"
python --version

step "Install build dependencies"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

step "Clean previous build artifacts"
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR/__pycache__" || true

step "Build macOS .app bundle (PyInstaller spec)"
python -m PyInstaller --noconfirm --clean solidflow.spec

step "Verify output"
if [[ ! -d "$ROOT_DIR/dist/SolidFlow.app" ]]; then
  echo "dist directory:"
  ls -la "$ROOT_DIR/dist" || true
  die "Expected output not found: dist/SolidFlow.app"
fi

echo "OK: dist/SolidFlow.app"
echo "Size:"
du -sh "$ROOT_DIR/dist/SolidFlow.app" || true

step "Done"
echo "App bundle: $ROOT_DIR/dist/SolidFlow.app"
echo "Log: $LOG_FILE"


