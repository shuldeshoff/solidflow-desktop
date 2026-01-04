#!/bin/bash
# Проверка качества кода

echo "Проверка стиля кода с помощью flake8..."
flake8 src/ tests/

if [ $? -eq 0 ]; then
    echo ""
    echo "Проверка стиля кода пройдена успешно!"
else
    echo ""
    echo "Обнаружены проблемы со стилем кода."
    exit 1
fi

