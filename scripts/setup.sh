# Инструкция по установке зависимостей
echo "Установка зависимостей SolidFlow Desktop..."

if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Установка зависимостей для разработки..."
pip install -r requirements-dev.txt

echo ""
echo "Установка завершена!"
echo "Для запуска приложения используйте: python -m solidflow"

