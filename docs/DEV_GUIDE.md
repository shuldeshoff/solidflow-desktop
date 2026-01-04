# Руководство по разработке

## Качество кода

### Форматирование кода

Проект использует **black** для автоматического форматирования кода.

```bash
# Автоматическое форматирование всего кода
black src/ tests/ scripts/

# Или используйте скрипт
./scripts/format.sh  # Linux/macOS
scripts\format.bat   # Windows

# Проверка без изменений
black --check src/ tests/ scripts/
```

### Проверка стиля кода

Проект использует **flake8** для проверки стиля кода.

```bash
# Проверка стиля
flake8 src/ tests/

# Или используйте скрипт
./scripts/lint.sh    # Linux/macOS
scripts\lint.bat     # Windows
```

### Настройки инструментов

* **black**: настройки в `pyproject.toml` (максимальная длина строки 100)
* **flake8**: настройки в `.flake8`

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=src/solidflow --cov-report=html --cov-report=term

# Только unit-тесты
pytest tests/unit/

# Только интеграционные тесты
pytest tests/integration/

# Конкретный файл
pytest tests/unit/test_viewport.py

# Конкретный тест
pytest tests/unit/test_viewport.py::test_viewport_creation
```

### Написание тестов

* Unit-тесты в `tests/unit/`
* Интеграционные тесты в `tests/integration/`
* Тестовые данные в `tests/fixtures/`
* Используйте `pytest` fixtures для повторяющихся настроек

## CI/CD

### GitHub Actions

Проект использует GitHub Actions для автоматизации:

**Workflows:**
* **Test** - запуск тестов на Python 3.10, 3.11, 3.12 и Windows, macOS, Linux
* **Lint** - проверка форматирования (black) и стиля (flake8)
* **Build** - сборка приложения с PyInstaller

Workflows запускаются при:
* Push в ветки `main` и `develop`
* Pull requests в ветки `main` и `develop`

### Локальная проверка перед коммитом

Перед коммитом рекомендуется запустить:

```bash
# Форматирование
black src/ tests/ scripts/

# Линтинг
flake8 src/ tests/

# Тесты
pytest
```

## Структура проекта

```
solidflow-desktop/
├── src/solidflow/          # Исходный код
│   ├── core/              # Ядро приложения
│   ├── gui/               # GUI компоненты
│   │   ├── viewport/     # 3D viewport
│   │   └── widgets/      # Кастомные виджеты
│   ├── geometry/          # Работа с геометрией
│   │   └── mesh/         # Mesh операции
│   └── analysis/          # Анализ моделей
├── tests/                 # Тесты
│   ├── unit/             # Unit-тесты
│   ├── integration/      # Интеграционные тесты
│   └── fixtures/         # Тестовые данные
├── resources/            # Ресурсы
│   ├── icons/           # Иконки
│   ├── models/          # Тестовые модели
│   └── shaders/         # Шейдеры
├── scripts/             # Вспомогательные скрипты
│   ├── setup.sh/.bat   # Установка
│   ├── format.sh/.bat  # Форматирование
│   └── lint.sh/.bat    # Линтинг
├── docs/                # Документация
└── .github/workflows/   # CI/CD конфигурация
```

## Рабочий процесс

### Создание новой функции

1. Создайте ветку от `develop`:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/название-функции
   ```

2. Разработайте функцию

3. Добавьте тесты

4. Запустите форматирование и линтинг:
   ```bash
   black src/ tests/ scripts/
   flake8 src/ tests/
   ```

5. Запустите тесты:
   ```bash
   pytest
   ```

6. Закоммитьте изменения:
   ```bash
   git add .
   git commit -m "feat: описание функции"
   ```

7. Создайте Pull Request в `develop`

### Исправление бага

1. Создайте ветку от `main` или `develop`:
   ```bash
   git checkout main  # или develop
   git pull
   git checkout -b fix/описание-бага
   ```

2. Исправьте баг

3. Добавьте тест, воспроизводящий баг (если возможно)

4. Следуйте шагам 4-7 из предыдущего раздела

## Стиль коммитов

Используйте conventional commits:

* `feat:` - новая функция
* `fix:` - исправление бага
* `docs:` - изменения в документации
* `style:` - форматирование (не влияет на код)
* `refactor:` - рефакторинг
* `test:` - добавление/изменение тестов
* `chore:` - изменения в процессе сборки

Примеры:
```
feat: добавить импорт OBJ файлов
fix: исправить ошибку в вычислении объема
docs: обновить README с новыми инструкциями
```

## Полезные команды

```bash
# Создание тестовых моделей
python scripts/create_test_models.py

# Запуск приложения
python -m solidflow

# Проверка версии зависимостей
pip list | grep -E "PySide6|pyvista|trimesh"

# Обновление зависимостей
pip install --upgrade -r requirements.txt
```

## Дополнительная информация

* [План MVP](docs/mvp-plan.md)
* [Архитектура](docs/architecture.md)
* [Технический стек](docs/tech-stack.md)
* [Инструкция по установке](docs/INSTALL.md)

