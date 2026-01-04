@echo off
REM Инструкция по установке зависимостей для Windows

echo Установка зависимостей SolidFlow Desktop...

if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Установка зависимостей для разработки...
pip install -r requirements-dev.txt

echo.
echo Установка завершена!
echo Для запуска приложения используйте: python -m solidflow
pause

