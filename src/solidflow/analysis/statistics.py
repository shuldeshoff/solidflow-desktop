"""
Статистика и метрики для mesh моделей
"""

import numpy as np
from typing import Dict


class MeshStatistics:
    """Класс для вычисления статистики mesh моделей"""

    def __init__(self, mesh):
        """
        Инициализация

        Args:
            mesh: PyVista mesh объект
        """
        self.mesh = mesh

    def compute_all(self) -> Dict[str, any]:
        """
        Вычислить всю статистику

        Returns:
            dict: Словарь со всей статистикой
        """
        bounds = self.mesh.bounds

        return {
            "geometry": self.get_geometry_info(),
            "size": self.get_size_info(),
            "volume": self.get_volume(),
            "surface_area": self.get_surface_area(),
            "bounding_box": {
                "min": [bounds[0], bounds[2], bounds[4]],
                "max": [bounds[1], bounds[3], bounds[5]],
                "center": self.mesh.center,
            },
        }

    def get_geometry_info(self) -> Dict[str, int]:
        """
        Получить информацию о геометрии

        Returns:
            dict: Количество треугольников и вершин
        """
        return {
            "triangles": self.mesh.n_cells,
            "vertices": self.mesh.n_points,
            "edges": self.mesh.n_cells * 3,  # Приблизительно
        }

    def get_size_info(self) -> Dict[str, float]:
        """
        Получить размеры модели

        Returns:
            dict: Размеры по осям X, Y, Z
        """
        bounds = self.mesh.bounds

        return {
            "x": float(bounds[1] - bounds[0]),
            "y": float(bounds[3] - bounds[2]),
            "z": float(bounds[5] - bounds[4]),
            "diagonal": float(
                np.sqrt(
                    (bounds[1] - bounds[0]) ** 2
                    + (bounds[3] - bounds[2]) ** 2
                    + (bounds[5] - bounds[4]) ** 2
                )
            ),
        }

    def get_volume(self) -> float:
        """
        Вычислить объем модели

        Returns:
            float: Объем в кубических единицах
        """
        # PyVista не имеет прямого метода для объема
        # Используем trimesh для вычисления
        try:
            import trimesh

            vertices = self.mesh.points
            faces = self.mesh.faces.reshape((-1, 4))[:, 1:]
            tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)

            if tmesh.is_watertight:
                return float(tmesh.volume)
            else:
                return 0.0  # Не можем вычислить объем для негерметичных моделей
        except:
            return 0.0

    def get_surface_area(self) -> float:
        """
        Вычислить площадь поверхности

        Returns:
            float: Площадь поверхности
        """
        try:
            import trimesh

            vertices = self.mesh.points
            faces = self.mesh.faces.reshape((-1, 4))[:, 1:]
            tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)

            return float(tmesh.area)
        except:
            return 0.0

    def get_center_of_mass(self) -> np.ndarray:
        """
        Получить центр масс

        Returns:
            np.ndarray: Координаты центра масс
        """
        return self.mesh.center

