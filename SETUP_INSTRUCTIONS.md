# Примечание к установке зависимостей

## Для запуска приложения необходимо установить зависимости:

```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте его
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate.bat  # Windows

# Установите зависимости
pip install -r requirements.txt
```

## Создание тестовых моделей

После установки зависимостей выполните:

```bash
python scripts/create_test_models.py
```

Это создаст тестовые STL файлы в `resources/models/`:
- test_cube.stl
- test_sphere.stl  
- test_cylinder.stl

## Запуск приложения

```bash
python -m solidflow
```

Теперь вы сможете:
1. Открыть STL файл через меню File -> Open
2. Просмотреть модель в 3D viewport
3. Переключать режимы отображения (Wireframe/Solid)
4. Вращать, масштабировать и перемещать модель
5. Сбросить камеру клавишей Home

