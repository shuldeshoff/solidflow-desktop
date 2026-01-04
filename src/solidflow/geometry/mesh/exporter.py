"""
Экспорт STL файлов
"""

import pyvista as pv
from pathlib import Path
from typing import Union


class STLExporter:
    """Класс для экспорта STL файлов"""

    @staticmethod
    def save(mesh: pv.PolyData, file_path: Union[str, Path], binary: bool = True):
        """
        Сохранить mesh в STL файл

        Args:
            mesh: PyVista mesh для сохранения
            file_path: Путь для сохранения
            binary: True для бинарного формата, False для текстового

        Raises:
            ValueError: Если mesh пустой
            IOError: Если не удалось сохранить файл
        """
        if mesh.n_points == 0:
            raise ValueError("Mesh не содержит данных")

        file_path = Path(file_path)

        # Убедимся что расширение .stl
        if file_path.suffix.lower() != ".stl":
            file_path = file_path.with_suffix(".stl")

        try:
            # PyVista автоматически сохраняет в бинарном формате для STL
            mesh.save(str(file_path))

        except Exception as e:
            raise IOError(f"Ошибка при сохранении STL файла: {str(e)}")

