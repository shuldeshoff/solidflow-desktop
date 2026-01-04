"""
Базовый тест для конфигурации
"""

from solidflow.core.config import Config


def test_config_version():
    """Проверка версии"""
    assert Config.VERSION == "0.1.0"


def test_config_window_size():
    """Проверка размеров окна"""
    assert Config.WINDOW_WIDTH > 0
    assert Config.WINDOW_HEIGHT > 0


def test_config_supported_formats():
    """Проверка поддерживаемых форматов"""
    assert "stl" in Config.SUPPORTED_FORMATS
    assert isinstance(Config.SUPPORTED_FORMATS, dict)


def test_config_file_filter():
    """Проверка фильтра файлов"""
    filter_str = Config.get_file_filter()
    assert "STL" in filter_str
    assert "All Files" in filter_str

