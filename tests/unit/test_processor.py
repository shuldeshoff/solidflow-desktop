"""
Тесты для процессора mesh
"""

import pytest

pytest.importorskip("trimesh")
pytest.importorskip("pyvista")

from solidflow.geometry.mesh.processor import MeshProcessor


def test_processor_creation():
    """Тест создания процессора"""
    pytest.importorskip("trimesh")
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    processor = MeshProcessor(mesh)

    assert processor.mesh is not None


def test_processor_remove_duplicates():
    """Тест удаления дубликатов"""
    pytest.importorskip("trimesh")
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    processor = MeshProcessor(mesh)

    cleaned = processor.remove_duplicates()

    assert cleaned is not None
    assert cleaned.n_points > 0


def test_processor_smooth():
    """Тест сглаживания"""
    pytest.importorskip("trimesh")
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    processor = MeshProcessor(mesh)

    smoothed = processor.smooth(iterations=5)

    assert smoothed is not None
    assert smoothed.n_points > 0

