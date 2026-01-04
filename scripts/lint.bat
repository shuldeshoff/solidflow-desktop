@echo off
REM Проверка качества кода

echo Проверка стиля кода с помощью flake8...
flake8 src/ tests/

if %errorlevel% equ 0 (
    echo.
    echo Проверка стиля кода пройдена успешно!
) else (
    echo.
    echo Обнаружены проблемы со стилем кода.
    exit /b 1
)
pause

