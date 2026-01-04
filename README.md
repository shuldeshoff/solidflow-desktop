# SolidFlow Desktop

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![CI](https://github.com/shuldeshoff/solidflow-desktop/workflows/CI/badge.svg)](https://github.com/shuldeshoff/solidflow-desktop/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Desktop-платформа подготовки и оптимизации моделей для 3D-печати и мехобработки.

## Описание

SolidFlow Desktop — это кроссплатформенное desktop-приложение для инженерной предобработки 3D-моделей, объединяющее CAD-геометрию, mesh и point cloud в одном рабочем пространстве. Продукт закрывает разрыв между CAD-системами и реальным производством (3D-печать, CNC).

## Основные возможности

### Импорт и конвертация
* Поддержка форматов: STEP, STL, OBJ, PLY, point cloud
* Конвертация между B-Rep и mesh с контролем допусков

### Анализ геометрии
* Анализ толщины стенок
* Обнаружение самопересечений
* Выявление острых углов и дефектов сетки

### Подготовка к 3D-печати
* Оптимальная ориентация модели
* Генерация поддержек
* Проверка технологичности

### CAM-подготовка
* Разбиение на операции
* Расчет припусков

### Визуализация
* Интерактивный 3D-viewport
* Сечения, измерения, аннотации

### ML-компонент
* Автоматическое определение проблемных зон модели
* Рекомендации по ориентации и параметрам печати
* Классификация дефектов геометрии

## Технический стек

* **Язык**: Python 3.10+
* **GUI**: PySide6
* **3D-визуализация**: PyVista + VTK
* **Геометрия**: cadquery, pythonocc (B-Rep), trimesh, Open3D (mesh, point cloud)
* **Численные расчеты**: NumPy, SciPy
* **ML**: PyTorch (локальный inference)

## Требования

* Python 3.10 или выше
* Операционная система: Windows 10+, macOS 10.15+, или Linux

## Установка

### Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/shuldeshoff/solidflow-desktop.git
cd solidflow-desktop

# Установка зависимостей (Linux/macOS)
./scripts/setup.sh

# Или для Windows
scripts\setup.bat

# Запуск приложения
python -m solidflow
```

Подробная инструкция по установке: [docs/INSTALL.md](docs/INSTALL.md)

## Статус проекта

**Версия:** 0.3.1  
**Статус:** MVP завершен (100%)

**Текущий этап:** MVP готов к релизу

### Что реализовано (все этапы MVP):
* Структура проекта [OK]
* Базовое Qt приложение [OK]
* 3D viewport с PyVista [OK]
* Импорт и отображение STL файлов [OK]
* Режимы отображения (Wireframe/Solid) [OK]
* Интерактивная навигация [OK]
* Панель информации о модели [OK]
* **Валидация mesh** [OK]
* **Статистика моделей** [OK]
* **Ремонт и обработка mesh** [OK]
* **Экспорт STL** [OK]
* **Защита от потери данных** [OK]
* **Интеграционное тестирование** [OK]
* CI/CD (GitHub Actions) [OK]
* Инструменты качества кода (black, flake8) [OK]
* Сборка дистрибутивов (PyInstaller) [OK]
* Документация для пользователей и разработчиков [OK]

**Следующий этап:** Релиз MVP v1.0.0 или добавление новых форматов (OBJ, STEP)

## Документация

* **Пользователям:** [Руководство пользователя](docs/USER_GUIDE.md) | [FAQ](docs/FAQ.md)
* **Разработчикам:** [Руководство по разработке](docs/DEV_GUIDE.md) | [Архитектура](docs/architecture.md)
* **Полная документация:** [docs/](docs/)

## Вклад в проект

Вклад в проект приветствуется! Пожалуйста, ознакомьтесь с [CONTRIBUTING.md](CONTRIBUTING.md) для получения информации о процессе разработки.

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## Автор

[shuldeshoff](https://github.com/shuldeshoff)

## Ссылки

* [Issues](https://github.com/shuldeshoff/solidflow-desktop/issues) - сообщить о баге или предложить новую функцию
* [Discussions](https://github.com/shuldeshoff/solidflow-desktop/discussions) - обсуждения и вопросы

