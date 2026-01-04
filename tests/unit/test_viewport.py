"""
Тест для 3D viewport
"""

import pytest
from PySide6.QtWidgets import QApplication
from solidflow.gui.viewport.viewport3d import Viewport3D


@pytest.fixture
def qapp():
    """Fixture для Qt приложения"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_viewport_creation(qapp):
    """Тест создания viewport"""
    viewport = Viewport3D()
    assert viewport is not None
    assert viewport.current_mesh is None
    assert viewport.get_display_mode() == "solid"


def test_viewport_display_mode(qapp):
    """Тест смены режима отображения"""
    viewport = Viewport3D()

    # Проверка solid
    viewport.set_display_mode("solid")
    assert viewport.get_display_mode() == "solid"

    # Проверка wireframe
    viewport.set_display_mode("wireframe")
    assert viewport.get_display_mode() == "wireframe"

    # Проверка недопустимого режима
    viewport.set_display_mode("invalid")
    assert viewport.get_display_mode() == "wireframe"  # Должен остаться прежним


def test_viewport_clear(qapp):
    """Тест очистки viewport"""
    viewport = Viewport3D()
    viewport.clear()
    assert viewport.current_mesh is None
    assert viewport.current_actor is None

