# Инструкция по установке и запуску

## Установка

### Предварительные требования

* Python 3.10 или выше
* pip (обычно устанавливается вместе с Python)
* Git

### Клонирование репозитория

```bash
git clone https://github.com/shuldeshoff/solidflow-desktop.git
cd solidflow-desktop
```

### Установка зависимостей

#### Linux/macOS

Используйте скрипт автоматической установки:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Или установите вручную:

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Для разработки (опционально)
pip install -r requirements-dev.txt
```

#### Windows

Используйте скрипт автоматической установки:

```cmd
scripts\setup.bat
```

Или установите вручную:

```cmd
REM Создание виртуального окружения
python -m venv venv

REM Активация виртуального окружения
venv\Scripts\activate.bat

REM Установка зависимостей
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Для разработки (опционально)
pip install -r requirements-dev.txt
```

## Запуск приложения

После активации виртуального окружения:

```bash
python -m solidflow
```

## Разработка

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=src/solidflow --cov-report=html

# Только unit-тесты
pytest tests/unit/

# Только интеграционные тесты
pytest tests/integration/
```

### Форматирование кода

```bash
black src/ tests/
```

### Проверка стиля

```bash
flake8 src/ tests/
```

## Текущий статус (Этап 1 MVP)

На данный момент реализовано:

* Структура проекта
* Базовое Qt приложение с главным окном
* Меню File (Open, Save, Exit)
* Меню Help (About)
* Базовая конфигурация

Следующий этап: интеграция 3D viewport (PyVista)

## Устранение проблем

### Ошибка импорта PySide6

Если возникает ошибка импорта PySide6, убедитесь что:

1. Виртуальное окружение активировано
2. Все зависимости установлены: `pip install -r requirements.txt`

### Проблемы с VTK

На некоторых системах может потребоваться установка дополнительных системных библиотек:

**Ubuntu/Debian:**
```bash
sudo apt-get install libgl1-mesa-glx
```

**macOS:**
VTK должен работать без дополнительных библиотек.

**Windows:**
VTK должен работать без дополнительных библиотек.

