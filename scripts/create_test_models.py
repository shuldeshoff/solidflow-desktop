"""
Простой скрипт для генерации тестовых моделей
"""

import trimesh
from pathlib import Path


def create_test_models():
    """Создать тестовые модели для разработки"""
    models_dir = Path(__file__).parent.parent / "resources" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    # Куб
    cube = trimesh.creation.box(extents=[10, 10, 10])
    cube.export(models_dir / "test_cube.stl")
    print(f"Создан: {models_dir / 'test_cube.stl'}")

    # Сфера
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=5.0)
    sphere.export(models_dir / "test_sphere.stl")
    print(f"Создан: {models_dir / 'test_sphere.stl'}")

    # Цилиндр
    cylinder = trimesh.creation.cylinder(radius=5.0, height=20.0)
    cylinder.export(models_dir / "test_cylinder.stl")
    print(f"Создан: {models_dir / 'test_cylinder.stl'}")

    print("\nТестовые модели созданы успешно!")


if __name__ == "__main__":
    create_test_models()

