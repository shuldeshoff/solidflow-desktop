#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

python -m PyInstaller --noconfirm --clean solidflow.spec

echo
echo "Build completed. Output:"
ls -la dist || true


