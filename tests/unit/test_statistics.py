"""
Тесты для статистики mesh
"""

import pytest
from solidflow.analysis.statistics import MeshStatistics


def test_statistics_creation():
    """Тест создания статистики"""
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    stats = MeshStatistics(mesh)

    assert stats.mesh is not None


def test_statistics_geometry_info():
    """Тест получения информации о геометрии"""
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    stats = MeshStatistics(mesh)

    info = stats.get_geometry_info()

    assert "triangles" in info
    assert "vertices" in info
    assert info["triangles"] > 0
    assert info["vertices"] > 0


def test_statistics_size_info():
    """Тест получения размеров"""
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    stats = MeshStatistics(mesh)

    size = stats.get_size_info()

    assert "x" in size
    assert "y" in size
    assert "z" in size
    assert size["x"] > 0
    assert size["y"] > 0
    assert size["z"] > 0


def test_statistics_compute_all():
    """Тест вычисления всей статистики"""
    pv = pytest.importorskip("pyvista")
    mesh = pv.Cube()
    stats = MeshStatistics(mesh)

    all_stats = stats.compute_all()

    assert "geometry" in all_stats
    assert "size" in all_stats
    assert "bounding_box" in all_stats

