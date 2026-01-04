"""
Валидатор для проверки корректности mesh
"""

import trimesh
import numpy as np
from typing import Dict, List, Tuple


class MeshValidator:
    """Класс для валидации mesh моделей"""

    def __init__(self, mesh):
        """
        Инициализация валидатора

        Args:
            mesh: PyVista или trimesh mesh объект
        """
        # Конвертируем PyVista mesh в trimesh для анализа
        if hasattr(mesh, "points") and hasattr(mesh, "faces"):
            # PyVista mesh
            vertices = mesh.points
            faces = mesh.faces.reshape((-1, 4))[:, 1:]  # Убираем первый элемент (количество)
            self.mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        else:
            self.mesh = mesh

        self.issues = {}

    def validate(self) -> Dict[str, any]:
        """
        Выполнить полную валидацию mesh

        Returns:
            dict: Словарь с результатами валидации
        """
        results = {
            "valid": True,
            "watertight": self.check_watertight(),
            "manifold": self.check_manifold(),
            "normals": self.check_normals(),
            "degenerate_faces": self.check_degenerate_faces(),
            "duplicate_vertices": self.check_duplicate_vertices(),
            "issues": [],
        }

        # Собираем все проблемы
        if not results["watertight"]:
            results["issues"].append("Модель не герметична (не watertight)")
            results["valid"] = False

        if not results["manifold"]["is_manifold"]:
            results["issues"].append(
                f"Найдено {results['manifold']['non_manifold_edges']} "
                f"некорректных ребер (non-manifold)"
            )
            results["valid"] = False

        if results["normals"]["flipped_count"] > 0:
            results["issues"].append(
                f"Найдено {results['normals']['flipped_count']} "
                f"перевернутых нормалей"
            )

        if results["degenerate_faces"] > 0:
            results["issues"].append(f"Найдено {results['degenerate_faces']} вырожденных граней")
            results["valid"] = False

        if results["duplicate_vertices"] > 0:
            results["issues"].append(
                f"Найдено {results['duplicate_vertices']} дублирующихся вершин"
            )

        return results

    def check_watertight(self) -> bool:
        """
        Проверка герметичности модели

        Returns:
            bool: True если модель герметична
        """
        return self.mesh.is_watertight

    def check_manifold(self) -> Dict[str, any]:
        """
        Проверка на manifold геометрию

        Returns:
            dict: Информация о manifold статусе
        """
        return {
            "is_manifold": self.mesh.is_winding_consistent,
            "non_manifold_edges": len(self.mesh.edges[self.mesh.edges_unique_inverse > 2])
            if hasattr(self.mesh, "edges_unique_inverse")
            else 0,
        }

    def check_normals(self) -> Dict[str, any]:
        """
        Проверка нормалей

        Returns:
            dict: Информация о нормалях
        """
        # Проверяем согласованность нормалей
        face_normals = self.mesh.face_normals

        # Считаем потенциально перевернутые нормали
        # (смотрящие внутрь, если центр масс считается внутри)
        center = self.mesh.centroid
        vectors_to_center = center - self.mesh.triangles_center

        # Скалярное произведение с нормалями
        dots = np.sum(vectors_to_center * face_normals, axis=1)
        flipped_count = np.sum(dots > 0)

        return {
            "flipped_count": int(flipped_count),
            "total_faces": len(face_normals),
            "flipped_percentage": (flipped_count / len(face_normals) * 100)
            if len(face_normals) > 0
            else 0,
        }

    def check_degenerate_faces(self) -> int:
        """
        Проверка на вырожденные грани (с нулевой площадью)

        Returns:
            int: Количество вырожденных граней
        """
        areas = self.mesh.area_faces
        degenerate = np.sum(areas < 1e-10)
        return int(degenerate)

    def check_duplicate_vertices(self) -> int:
        """
        Проверка на дублирующиеся вершины

        Returns:
            int: Количество дублирующихся вершин
        """
        unique_vertices = self.mesh.vertices
        # trimesh автоматически объединяет дублирующиеся вершины
        # поэтому проверяем через merge_vertices
        merged = self.mesh.copy()
        merged.merge_vertices()

        duplicates = len(self.mesh.vertices) - len(merged.vertices)
        return int(duplicates)

