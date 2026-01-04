"""
Базовый тест для проверки импорта модулей
"""

import pytest


def test_imports():
    """Проверка что основные модули импортируются"""
    import solidflow
    from solidflow.core import config

    assert solidflow.__version__ == "0.3.1"
    assert hasattr(config, "Config")

    # GUI части требуют PySide6 и 3D стека; если их нет в окружении — пропускаем.
    pytest.importorskip("PySide6")
    pytest.importorskip("pyvista")
    pytest.importorskip("pyvistaqt")

    from solidflow.core import application
    from solidflow.gui import main_window

    assert hasattr(application, "Application")
    assert hasattr(main_window, "MainWindow")

