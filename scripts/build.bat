@echo off
setlocal enabledelayedexpansion

cd /d %~dp0\..

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

python -m PyInstaller --noconfirm --clean solidflow.spec

echo.
echo Build completed. Output is in dist\
dir dist

endlocal


