import os

import pytest


@pytest.mark.integration
def test_full_cycle_import_analyze_repair_export(tmp_path):
    """
    Интеграционный тест полного цикла:
    import STL -> analyze -> repair -> export -> reimport.

    По умолчанию отключен, чтобы не ломать CI на окружениях без тяжелых зависимостей.
    Запуск:
        SOLIDFLOW_RUN_INTEGRATION=1 pytest -m integration
    """
    if os.getenv("SOLIDFLOW_RUN_INTEGRATION") != "1":
        pytest.skip("Integration tests are disabled. Set SOLIDFLOW_RUN_INTEGRATION=1 to run.")

    trimesh = pytest.importorskip("trimesh")
    pytest.importorskip("pyvista")

    from solidflow.analysis.statistics import MeshStatistics
    from solidflow.analysis.validator import MeshValidator
    from solidflow.geometry.mesh.exporter import STLExporter
    from solidflow.geometry.mesh.importer import STLImporter
    from solidflow.geometry.mesh.processor import MeshProcessor

    input_file = tmp_path / "cube.stl"
    output_file = tmp_path / "cube_processed.stl"

    # Create a test STL
    cube = trimesh.creation.box(extents=[10, 10, 10])
    cube.export(input_file)

    # Import
    mesh = STLImporter.load(input_file)
    assert mesh.n_points > 0
    assert mesh.n_cells > 0

    # Analyze
    stats = MeshStatistics(mesh).compute_all()
    assert stats["size"]["x"] > 0
    assert stats["surface_area"] > 0

    validation = MeshValidator(mesh).validate()
    assert "valid" in validation

    # Repair (should not crash)
    repaired = MeshProcessor(mesh).repair()
    assert repaired.n_points > 0
    assert repaired.n_cells > 0

    # Export
    STLExporter.save(repaired, output_file)
    assert output_file.exists()
    assert output_file.stat().st_size > 0

    # Re-import
    mesh2 = STLImporter.load(output_file)
    assert mesh2.n_points > 0
    assert mesh2.n_cells > 0


