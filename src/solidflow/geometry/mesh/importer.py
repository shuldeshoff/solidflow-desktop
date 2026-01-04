"""
Импорт STL файлов
"""

import pyvista as pv
import trimesh
from pathlib import Path
from typing import Union


class STLImporter:
    """Класс для импорта STL файлов"""

    @staticmethod
    def load(file_path: Union[str, Path]) -> pv.PolyData:
        """
        Загрузить STL файл

        Args:
            file_path: Путь к STL файлу

        Returns:
            pv.PolyData: Загруженный mesh

        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если файл не является корректным STL
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        if file_path.suffix.lower() != ".stl":
            raise ValueError(f"Ожидается .stl файл, получен: {file_path.suffix}")

        try:
            # Используем PyVista для загрузки
            mesh = pv.read(str(file_path))

            if mesh.n_points == 0:
                raise ValueError("Файл не содержит данных")

            return mesh

        except Exception as e:
            raise ValueError(f"Ошибка при загрузке STL файла: {str(e)}")

    @staticmethod
    def validate(file_path: Union[str, Path]) -> bool:
        """
        Проверить, является ли файл корректным STL

        Args:
            file_path: Путь к файлу

        Returns:
            bool: True если файл корректный
        """
        try:
            STLImporter.load(file_path)
            return True
        except:
            return False

