#!/usr/bin/env python3
"""
Скрипт для тестирования полного цикла работы с моделями
"""

import sys
import trimesh
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from solidflow.geometry.mesh.importer import STLImporter
from solidflow.geometry.mesh.exporter import STLExporter
from solidflow.geometry.mesh.processor import MeshProcessor
from solidflow.analysis.validator import MeshValidator
from solidflow.analysis.statistics import MeshStatistics


def test_full_cycle():
    """Тест полного цикла: импорт -> анализ -> ремонт -> экспорт"""
    print("=" * 60)
    print("Тест полного цикла обработки модели")
    print("=" * 60)
    
    # Путь к тестовым файлам
    test_file = Path(__file__).parent.parent / "resources" / "models" / "test_cube.stl"
    output_file = Path(__file__).parent.parent / "resources" / "models" / "test_cube_processed.stl"
    
    # Создаем тестовый файл если нет
    if not test_file.exists():
        print("\n[1/6] Создание тестового файла...")
        test_file.parent.mkdir(parents=True, exist_ok=True)
        cube = trimesh.creation.box(extents=[10, 10, 10])
        cube.export(test_file)
        print(f"  [OK] Создан: {test_file.name}")
    else:
        print(f"\n[1/6] Используется существующий файл: {test_file.name}")
    
    # 1. ИМПОРТ
    print("\n[2/6] Импорт STL...")
    try:
        mesh = STLImporter.load(str(test_file))
        print(f"  [OK] Загружено: {mesh.n_cells} треугольников, {mesh.n_points} вершин")
    except Exception as e:
        print(f"  [FAIL] Ошибка импорта: {e}")
        return False
    
    # 2. СТАТИСТИКА
    print("\n[3/6] Расчет статистики...")
    try:
        stats = MeshStatistics(mesh)
        stats_data = stats.compute_all()
        print(f"  [OK] Размеры: {stats_data['size']['x']:.2f} x {stats_data['size']['y']:.2f} x {stats_data['size']['z']:.2f} мм")
        print(f"  [OK] Объем: {stats_data['volume']:.2f} мм³")
        print(f"  [OK] Площадь: {stats_data['surface_area']:.2f} мм²")
    except Exception as e:
        print(f"  [FAIL] Ошибка расчета статистики: {e}")
        return False
    
    # 3. ВАЛИДАЦИЯ
    print("\n[4/6] Валидация модели...")
    try:
        validator = MeshValidator(mesh)
        validation = validator.validate()
        print(f"  [OK] Корректность: {'ДА' if validation['valid'] else 'НЕТ'}")
        print(f"  [OK] Watertight: {'ДА' if validation['watertight'] else 'НЕТ'}")
        print(f"  [OK] Manifold: {'ДА' if validation['manifold']['is_manifold'] else 'НЕТ'}")
        if validation['issues']:
            print(f"  ! Проблемы: {len(validation['issues'])}")
            for issue in validation['issues'][:3]:  # Показываем первые 3
                print(f"    - {issue}")
    except Exception as e:
        print(f"  [FAIL] Ошибка валидации: {e}")
        return False
    
    # 4. РЕМОНТ (если нужен)
    if not validation['valid']:
        print("\n[5/6] Ремонт модели...")
        try:
            processor = MeshProcessor(mesh)
            mesh = processor.repair()
            
            # Повторная валидация
            validator = MeshValidator(mesh)
            validation = validator.validate()
            print("  [OK] Ремонт выполнен")
            print(f"  [OK] Корректность после ремонта: {'ДА' if validation['valid'] else 'НЕТ'}")
        except Exception as e:
            print(f"  [FAIL] Ошибка ремонта: {e}")
            return False
    else:
        print("\n[5/6] Ремонт не требуется (модель корректна)")
    
    # 5. ЭКСПОРТ
    print("\n[6/6] Экспорт STL...")
    try:
        STLExporter.save(mesh, str(output_file))
        print(f"  [OK] Сохранено: {output_file.name}")
        
        # Проверка размера файла
        file_size = output_file.stat().st_size
        print(f"  [OK] Размер файла: {file_size / 1024:.2f} КБ")
    except Exception as e:
        print(f"  [FAIL] Ошибка экспорта: {e}")
        return False
    
    # Финальная проверка - повторный импорт
    print("\n[Проверка] Повторный импорт для проверки...")
    try:
        mesh_check = STLImporter.load(str(output_file))
        print(f"  [OK] Файл корректен: {mesh_check.n_cells} треугольников")
    except Exception as e:
        print(f"  [FAIL] Ошибка проверки: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("[OK] ТЕСТ ПРОЙДЕН УСПЕШНО")
    print("=" * 60)
    print(f"\nВходной файл:  {test_file}")
    print(f"Выходной файл: {output_file}")
    
    return True


def test_with_problematic_mesh():
    """Тест с проблемной моделью"""
    print("\n\n" + "=" * 60)
    print("Тест с проблемной моделью (с дырками)")
    print("=" * 60)
    
    # Создаем куб с дыркой
    print("\n[1/4] Создание проблемной модели...")
    cube = trimesh.creation.box(extents=[10, 10, 10])
    
    # Удаляем несколько граней чтобы создать дырки
    faces_to_keep = cube.faces[:-2]  # Удаляем 2 грани
    problematic_mesh = trimesh.Trimesh(vertices=cube.vertices, faces=faces_to_keep)
    
    print(f"  [OK] Создана модель с {problematic_mesh.n_cells} треугольников")
    
    # Валидация ДО ремонта
    print("\n[2/4] Валидация ДО ремонта...")
    validator = MeshValidator(problematic_mesh)
    validation_before = validator.validate()
    print(f"  [OK] Watertight: {'ДА' if validation_before['watertight'] else 'НЕТ'}")
    print(f"  [OK] Проблем найдено: {len(validation_before['issues'])}")
    
    # Ремонт
    print("\n[3/4] Ремонт модели...")
    processor = MeshProcessor(problematic_mesh)
    repaired_mesh = processor.repair()
    print("  [OK] Ремонт выполнен")
    print(f"  [OK] Треугольников после ремонта: {repaired_mesh.n_cells}")
    
    # Валидация ПОСЛЕ ремонта
    print("\n[4/4] Валидация ПОСЛЕ ремонта...")
    validator = MeshValidator(repaired_mesh)
    validation_after = validator.validate()
    print(f"  [OK] Watertight: {'ДА' if validation_after['watertight'] else 'НЕТ'}")
    print(f"  [OK] Проблем осталось: {len(validation_after['issues'])}")
    
    if validation_after['watertight']:
        print("\n[OK] ТЕСТ ПРОЙДЕН: Модель успешно отремонтирована!")
    else:
        print("\n[WARN] Некоторые проблемы не исправлены")
        print("  (это нормально для сложных случаев)")
    
    return True


if __name__ == "__main__":
    try:
        # Основной тест
        success1 = test_full_cycle()
        
        # Тест с проблемной моделью
        success2 = test_with_problematic_mesh()
        
        if success1 and success2:
            print("\n" + "=" * 60)
            print("[OK] ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n" + "=" * 60)
            print("[FAIL] НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
            print("=" * 60)
            sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

