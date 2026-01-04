"""
Базовый тест для проверки импорта модулей
"""

def test_imports():
    """Проверка что основные модули импортируются"""
    import solidflow
    from solidflow.core import application, config
    from solidflow.gui import main_window

    assert solidflow.__version__ == "0.1.0"
    assert hasattr(application, "Application")
    assert hasattr(config, "Config")
    assert hasattr(main_window, "MainWindow")

