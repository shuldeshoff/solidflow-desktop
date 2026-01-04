"""
Тесты для валидатора mesh
"""

import pytest

pytest.importorskip("trimesh")

from solidflow.analysis.validator import MeshValidator


def test_validator_watertight():
    """Тест проверки герметичности"""
    trimesh = pytest.importorskip("trimesh")
    # Создаем герметичный куб
    mesh = trimesh.creation.box()
    validator = MeshValidator(mesh)

    assert validator.check_watertight() is True


def test_validator_validation():
    """Тест полной валидации"""
    trimesh = pytest.importorskip("trimesh")
    mesh = trimesh.creation.box()
    validator = MeshValidator(mesh)

    results = validator.validate()

    assert "valid" in results
    assert "watertight" in results
    assert "manifold" in results
    assert "issues" in results


def test_validator_degenerate_faces():
    """Тест проверки вырожденных граней"""
    trimesh = pytest.importorskip("trimesh")
    mesh = trimesh.creation.box()
    validator = MeshValidator(mesh)

    count = validator.check_degenerate_faces()
    assert count >= 0

