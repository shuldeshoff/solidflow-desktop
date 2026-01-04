"""
Обработчик mesh - ремонт и модификации
"""

import trimesh
import pyvista as pv
import numpy as np


class MeshProcessor:
    """Класс для обработки и ремонта mesh моделей"""

    def __init__(self, mesh):
        """
        Инициализация

        Args:
            mesh: PyVista mesh объект
        """
        self.mesh = mesh
        self._tmesh = None

    def _to_trimesh(self):
        """Конвертировать в trimesh для обработки"""
        if self._tmesh is None:
            vertices = self.mesh.points
            faces = self.mesh.faces.reshape((-1, 4))[:, 1:]
            self._tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        return self._tmesh

    def _from_trimesh(self, tmesh):
        """Конвертировать trimesh обратно в PyVista"""
        faces = np.hstack(
            [np.full((len(tmesh.faces), 1), 3, dtype=np.int64), tmesh.faces]
        ).flatten()
        return pv.PolyData(tmesh.vertices, faces)

    def repair(self) -> pv.PolyData:
        """
        Выполнить базовый ремонт mesh

        Returns:
            pv.PolyData: Отремонтированный mesh
        """
        tmesh = self._to_trimesh()

        # Заполнение дырок
        tmesh.fill_holes()

        # Удаление дублирующихся вершин
        tmesh.merge_vertices()

        # Удаление дублирующихся граней
        tmesh.remove_duplicate_faces()

        # Удаление вырожденных граней
        tmesh.remove_degenerate_faces()

        # Удаление бесконечно малых компонентов
        tmesh.remove_infinite_values()

        return self._from_trimesh(tmesh)

    def fix_normals(self) -> pv.PolyData:
        """
        Исправить ориентацию нормалей

        Returns:
            pv.PolyData: Mesh с исправленными нормалями
        """
        tmesh = self._to_trimesh()

        # Исправление ориентации граней
        tmesh.fix_normals()

        return self._from_trimesh(tmesh)

    def remove_duplicates(self) -> pv.PolyData:
        """
        Удалить дублирующиеся вершины и грани

        Returns:
            pv.PolyData: Очищенный mesh
        """
        tmesh = self._to_trimesh()

        tmesh.merge_vertices()
        tmesh.remove_duplicate_faces()

        return self._from_trimesh(tmesh)

    def simplify(self, target_reduction: float = 0.5) -> pv.PolyData:
        """
        Упростить mesh (уменьшить количество треугольников)

        Args:
            target_reduction: Процент уменьшения (0.5 = 50% уменьшение)

        Returns:
            pv.PolyData: Упрощенный mesh
        """
        # Используем PyVista для simplification
        target_triangles = int(self.mesh.n_cells * (1 - target_reduction))
        simplified = self.mesh.decimate(target_triangles / self.mesh.n_cells)

        return simplified

    def smooth(self, iterations: int = 20) -> pv.PolyData:
        """
        Сгладить mesh

        Args:
            iterations: Количество итераций сглаживания

        Returns:
            pv.PolyData: Сглаженный mesh
        """
        return self.mesh.smooth(n_iter=iterations)

    def fill_holes(self) -> pv.PolyData:
        """
        Заполнить дырки в mesh

        Returns:
            pv.PolyData: Mesh с заполненными дырками
        """
        tmesh = self._to_trimesh()
        tmesh.fill_holes()
        return self._from_trimesh(tmesh)

