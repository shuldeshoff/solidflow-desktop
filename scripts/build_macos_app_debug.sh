#!/usr/bin/env bash
set -euo pipefail

# SolidFlow Desktop: macOS DEBUG .app build with progress logging.
#
# Отличие от релизной сборки:
# - другой bundle id и имя (SolidFlowDebug.app)
# - включен debug/console режим в EXE (для более подробной диагностики)
# - все логи приложения пишутся в ~/Library/Logs/SolidFlow/solidflow.log (кодом)
#
# Output:
# - dist/SolidFlowDebug.app
# - build_logs/build-macos-app-debug-YYYYmmdd-HHMMSS.log

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LOG_DIR="$ROOT_DIR/build_logs"
mkdir -p "$LOG_DIR"

TS="$(date +"%Y%m%d-%H%M%S")"
LOG_FILE="$LOG_DIR/build-macos-app-debug-$TS.log"

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

PY_MAJ_MIN="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "python: $(command -v python)"
python --version

if [[ "$PY_MAJ_MIN" != "3.10" && "$PY_MAJ_MIN" != "3.11" && "$PY_MAJ_MIN" != "3.12" ]]; then
  die "Python 3.10+ is required."
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

step "Prepare temporary debug spec"
TMP_DIR="$(mktemp -d "$ROOT_DIR/.tmp-solidflow-build-XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

DEBUG_SPEC="$TMP_DIR/solidflow_debug.spec"
cp solidflow.spec "$DEBUG_SPEC"

python - "$DEBUG_SPEC" "$ROOT_DIR" <<'PY'
import sys
from pathlib import Path

spec_path = Path(sys.argv[1])
root_dir = Path(sys.argv[2]).resolve()

text = spec_path.read_text(encoding="utf-8")

# Когда spec лежит вне корня проекта, PyInstaller интерпретирует относительные пути
# относительно директории spec. Поэтому заменяем на абсолютные.
text = text.replace('["src/solidflow/__main__.py"]', f'["{(root_dir / "src" / "solidflow" / "__main__.py").as_posix()}"]')
text = text.replace('pathex=["src"]', f'pathex=["{(root_dir / "src").as_posix()}"]')

spec_path.write_text(text, encoding="utf-8")
PY

# Простая замена параметров в spec (без дополнительных зависимостей)
sed -i '' 's/name="SolidFlow"/name="SolidFlowDebug"/g' "$DEBUG_SPEC"
sed -i '' 's/name="SolidFlow.app"/name="SolidFlowDebug.app"/g' "$DEBUG_SPEC"
sed -i '' 's/bundle_identifier="com.shuldeshoff.solidflow"/bundle_identifier="com.shuldeshoff.solidflow.debug"/g' "$DEBUG_SPEC"
sed -i '' 's/debug=False/debug=True/g' "$DEBUG_SPEC"
sed -i '' 's/console=False/console=True/g' "$DEBUG_SPEC"

step "Clean previous build artifacts"
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR/__pycache__" || true

step "Build macOS DEBUG .app bundle (PyInstaller temp spec)"
python -m PyInstaller --noconfirm --clean "$DEBUG_SPEC"

step "Verify output"
if [[ ! -d "$ROOT_DIR/dist/SolidFlowDebug.app" ]]; then
  echo "dist directory:"
  ls -la "$ROOT_DIR/dist" || true
  die "Expected output not found: dist/SolidFlowDebug.app"
fi

echo "OK: dist/SolidFlowDebug.app"
du -sh "$ROOT_DIR/dist/SolidFlowDebug.app" || true

step "Done"
echo "App bundle: $ROOT_DIR/dist/SolidFlowDebug.app"
echo "Log: $LOG_FILE"


