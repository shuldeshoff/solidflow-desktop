"""
3D Viewport виджет на основе PyVista
"""

import logging
import time

from PySide6.QtWidgets import QFrame, QVBoxLayout


class Viewport3D(QFrame):
    """3D viewport виджет для отображения моделей"""

    def __init__(self, parent=None):
        """
        Инициализация viewport

        Args:
            parent: Родительский виджет
        """
        super().__init__(parent)

        self._log = logging.getLogger("SolidFlow.Viewport3D")

        # Создание PyVista plotter
        self.plotter = None
        self._pv = None

        # Layout, чтобы QtInteractor гарантированно отображался внутри QFrame
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._init_plotter()

        # Текущая загруженная модель
        self.current_mesh = None
        self.current_actor = None

        # Режим отображения
        self._display_mode = "solid"  # solid или wireframe

        self._setup_plotter()

    def _init_plotter(self):
        """Ленивая инициализация тяжелых зависимостей (PyVista/VTK/QtInteractor)."""
        t0 = time.perf_counter()
        self._log.info("Initializing QtInteractor/PyVista...")
        try:
            import pyvista as pv  # тяжелый импорт
            from pyvistaqt.plotting import QtInteractor
        except Exception:
            self._log.exception("Failed to import pyvista/pyvistaqt")
            raise

        self._pv = pv
        self.plotter = QtInteractor(self)
        self.plotter.set_background("grey")
        self.layout().addWidget(self.plotter)
        self._log.info("QtInteractor initialized (%.2fs).", time.perf_counter() - t0)

    def _setup_plotter(self):
        """Настройка plotter"""
        if self.plotter is None:
            return

        # Добавление осей координат (небольшие, в углу)
        self.plotter.add_axes(
            interactive=False,
            line_width=2,
            cone_radius=0.6,
            shaft_length=0.7,
            tip_length=0.3,
            ambient=0.5,
            label_size=(0.4, 0.16),
        )

        # Настройка камеры
        self.plotter.camera_position = "iso"
        self.plotter.reset_camera()

    def load_mesh(self, mesh):
        """
        Загрузить mesh для отображения

        Args:
            mesh: PyVista mesh или путь к файлу
        """
        if self.plotter is None or self._pv is None:
            self._log.error("Viewport is not initialized (plotter is None).")
            return

        # Удаление предыдущей модели
        if self.current_actor is not None:
            self.plotter.remove_actor(self.current_actor)

        # Загрузка mesh
        if isinstance(mesh, str):
            self.current_mesh = self._pv.read(mesh)
        else:
            self.current_mesh = mesh

        # Отображение mesh
        self._display_mesh()

        # Сброс камеры для центрирования модели
        self.plotter.reset_camera()

    def _display_mesh(self):
        """Отобразить текущий mesh"""
        if self.current_mesh is None:
            return

        # Параметры отображения в зависимости от режима
        if self._display_mode == "wireframe":
            self.current_actor = self.plotter.add_mesh(
                self.current_mesh,
                color="white",
                style="wireframe",
                line_width=1,
                lighting=False,
            )
        else:  # solid
            self.current_actor = self.plotter.add_mesh(
                self.current_mesh,
                color="lightblue",
                show_edges=False,
                smooth_shading=True,
            )

    def set_display_mode(self, mode):
        """
        Установить режим отображения

        Args:
            mode: "solid" или "wireframe"
        """
        if mode not in ["solid", "wireframe"]:
            return

        self._display_mode = mode

        # Обновить отображение если есть модель
        if self.current_mesh is not None:
            self.plotter.remove_actor(self.current_actor)
            self._display_mesh()

    def get_display_mode(self):
        """
        Получить текущий режим отображения

        Returns:
            str: Режим отображения
        """
        return self._display_mode

    def clear(self):
        """Очистить viewport"""
        if self.current_actor is not None:
            self.plotter.remove_actor(self.current_actor)
            self.current_actor = None
            self.current_mesh = None

    def reset_camera(self):
        """Сбросить камеру к начальному положению"""
        self.plotter.reset_camera()

    def show_edges(self, show=True):
        """
        Показать/скрыть ребра модели

        Args:
            show: True для показа ребер
        """
        if self.current_mesh is not None and self._display_mode == "solid":
            self.plotter.remove_actor(self.current_actor)
            self.current_actor = self.plotter.add_mesh(
                self.current_mesh,
                color="lightblue",
                show_edges=show,
                smooth_shading=True,
                edge_color="black",
            )

