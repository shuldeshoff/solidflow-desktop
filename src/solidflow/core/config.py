"""
Конфигурация приложения
"""

import os
from pathlib import Path


class Config:
    """Базовая конфигурация приложения"""

    # Версия приложения
    VERSION = "0.1.0"

    # Пути
    ROOT_DIR = Path(__file__).parent.parent.parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"
    MODELS_DIR = RESOURCES_DIR / "models"
    ICONS_DIR = RESOURCES_DIR / "icons"

    # Настройки UI
    WINDOW_TITLE = "SolidFlow Desktop"
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

    # Поддерживаемые форматы (для MVP только STL)
    SUPPORTED_FORMATS = {
        "stl": "STL Files (*.stl)",
    }

    @classmethod
    def get_file_filter(cls):
        """
        Получить строку фильтра файлов для диалога

        Returns:
            str: Строка фильтра
        """
        filters = list(cls.SUPPORTED_FORMATS.values())
        filters.append("All Files (*.*)")
        return ";;".join(filters)

