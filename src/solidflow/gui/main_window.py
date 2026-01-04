"""
Главное окно приложения
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QToolBar,
    QFileDialog,
    QMessageBox,
    QSplitter,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from pathlib import Path
from solidflow.core.config import Config
from solidflow.gui.viewport.viewport3d import Viewport3D
from solidflow.geometry.mesh.importer import STLImporter
from solidflow.geometry.mesh.exporter import STLExporter
from solidflow.geometry.mesh.processor import MeshProcessor
from solidflow.analysis.validator import MeshValidator
from solidflow.analysis.statistics import MeshStatistics


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()

        self.setWindowTitle(Config.WINDOW_TITLE)
        self.resize(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        # 3D viewport
        self.viewport = None

        # Текущий файл
        self.current_file = None

        # Текущая статистика и валидация
        self.current_stats = None
        self.current_validation = None

        self._setup_ui()
        self._create_menu()
        self._create_toolbar()

    def _setup_ui(self):
        """Настройка UI"""
        # Центральный виджет
        central_widget = QWidget()
        layout = QHBoxLayout()

        # Splitter для разделения viewport и боковой панели
        splitter = QSplitter(Qt.Horizontal)

        # 3D Viewport
        self.viewport = Viewport3D()
        splitter.addWidget(self.viewport)

        # Боковая панель с информацией (пока заглушка)
        info_panel = self._create_info_panel()
        splitter.addWidget(info_panel)

        # Размеры: 80% viewport, 20% info panel
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _create_info_panel(self):
        """Создать панель информации"""
        panel = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Информация о модели")
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(label)

        self.info_text = QLabel("Модель не загружена")
        self.info_text.setAlignment(Qt.AlignTop)
        self.info_text.setWordWrap(True)
        layout.addWidget(self.info_text)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def _create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Меню File
        file_menu = menubar.addMenu("Файл")

        # Action: Open
        self.open_action = QAction("Открыть...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Открыть STL файл")
        self.open_action.triggered.connect(self._on_open)
        file_menu.addAction(self.open_action)

        # Action: Save
        self.save_action = QAction("Сохранить", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Сохранить модель")
        self.save_action.setEnabled(False)
        self.save_action.triggered.connect(self._on_save)
        file_menu.addAction(self.save_action)

        # Action: Save As
        self.save_as_action = QAction("Сохранить как...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.setStatusTip("Сохранить модель в новый файл")
        self.save_as_action.setEnabled(False)
        self.save_as_action.triggered.connect(self._on_save_as)
        file_menu.addAction(self.save_as_action)

        file_menu.addSeparator()

        # Action: Exit
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Выйти из приложения")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню View
        view_menu = menubar.addMenu("Вид")

        # Action: Wireframe
        self.wireframe_action = QAction("Каркас", self)
        self.wireframe_action.setCheckable(True)
        self.wireframe_action.setStatusTip("Отображение в режиме каркаса")
        self.wireframe_action.triggered.connect(self._on_wireframe)
        view_menu.addAction(self.wireframe_action)

        # Action: Solid
        self.solid_action = QAction("Заливка", self)
        self.solid_action.setCheckable(True)
        self.solid_action.setChecked(True)
        self.solid_action.setStatusTip("Отображение в режиме заливки")
        self.solid_action.triggered.connect(self._on_solid)
        view_menu.addAction(self.solid_action)

        view_menu.addSeparator()

        # Action: Reset Camera
        reset_camera_action = QAction("Сбросить камеру", self)
        reset_camera_action.setShortcut("Home")
        reset_camera_action.setStatusTip("Сбросить положение камеры")
        reset_camera_action.triggered.connect(self._on_reset_camera)
        view_menu.addAction(reset_camera_action)

        # Меню Tools
        tools_menu = menubar.addMenu("Инструменты")

        # Action: Analyze
        analyze_action = QAction("Анализировать модель", self)
        analyze_action.setStatusTip("Выполнить анализ текущей модели")
        analyze_action.setEnabled(False)
        analyze_action.triggered.connect(self._on_analyze)
        tools_menu.addAction(analyze_action)
        self.analyze_action = analyze_action

        tools_menu.addSeparator()

        # Action: Repair
        repair_action = QAction("Ремонт модели", self)
        repair_action.setStatusTip("Выполнить базовый ремонт модели")
        repair_action.setEnabled(False)
        repair_action.triggered.connect(self._on_repair)
        tools_menu.addAction(repair_action)
        self.repair_action = repair_action

        # Action: Fix Normals
        fix_normals_action = QAction("Исправить нормали", self)
        fix_normals_action.setStatusTip("Исправить ориентацию нормалей")
        fix_normals_action.setEnabled(False)
        fix_normals_action.triggered.connect(self._on_fix_normals)
        tools_menu.addAction(fix_normals_action)
        self.fix_normals_action = fix_normals_action

        # Меню Help
        help_menu = menubar.addMenu("Справка")

        # Action: About
        about_action = QAction("О программе", self)
        about_action.setStatusTip("О программе SolidFlow Desktop")
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

        # Статус бар
        self.statusBar().showMessage("Готово")

    def _create_toolbar(self):
        """Создать панель инструментов"""
        toolbar = QToolBar("Основная")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Добавляем основные действия
        toolbar.addAction(self.open_action)
        toolbar.addSeparator()
        toolbar.addAction(self.wireframe_action)
        toolbar.addAction(self.solid_action)

    def _on_open(self):
        """Обработчик открытия файла"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть STL файл", "", Config.get_file_filter()
        )

        if file_name:
            try:
                # Используем STLImporter для загрузки
                mesh = STLImporter.load(file_name)
                self.viewport.load_mesh(mesh)
                self.current_file = file_name

                # Включаем действия
                self.save_action.setEnabled(True)
                self.save_as_action.setEnabled(True)
                self.analyze_action.setEnabled(True)
                self.repair_action.setEnabled(True)
                self.fix_normals_action.setEnabled(True)

                # Автоматический анализ
                self._perform_analysis()

                # Обновить информацию
                self._update_info()

                self.statusBar().showMessage(f"Загружено: {file_name}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}")

    def _on_save(self):
        """Обработчик сохранения файла"""
        if self.current_file and self.viewport.current_mesh:
            try:
                STLExporter.save(self.viewport.current_mesh, self.current_file)
                self.statusBar().showMessage(f"Сохранено: {self.current_file}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def _on_save_as(self):
        """Обработчик сохранения файла как"""
        if self.viewport.current_mesh:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Сохранить STL файл", "", Config.get_file_filter()
            )

            if file_name:
                try:
                    STLExporter.save(self.viewport.current_mesh, file_name)
                    self.current_file = file_name
                    self.statusBar().showMessage(f"Сохранено: {file_name}", 3000)
                except Exception as e:
                    QMessageBox.critical(
                        self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}"
                    )

    def _on_wireframe(self):
        """Переключение в режим каркаса"""
        self.viewport.set_display_mode("wireframe")
        self.wireframe_action.setChecked(True)
        self.solid_action.setChecked(False)
        self.statusBar().showMessage("Режим отображения: Каркас", 2000)

    def _on_solid(self):
        """Переключение в режим заливки"""
        self.viewport.set_display_mode("solid")
        self.solid_action.setChecked(True)
        self.wireframe_action.setChecked(False)
        self.statusBar().showMessage("Режим отображения: Заливка", 2000)

    def _on_reset_camera(self):
        """Сброс камеры"""
        self.viewport.reset_camera()
        self.statusBar().showMessage("Камера сброшена", 2000)

    def _perform_analysis(self):
        """Выполнить анализ модели"""
        if self.viewport.current_mesh:
            try:
                # Статистика
                stats = MeshStatistics(self.viewport.current_mesh)
                self.current_stats = stats.compute_all()

                # Валидация
                validator = MeshValidator(self.viewport.current_mesh)
                self.current_validation = validator.validate()

            except Exception as e:
                print(f"Ошибка анализа: {e}")
                self.current_stats = None
                self.current_validation = None

    def _update_info(self):
        """Обновить информацию о модели"""
        if self.viewport.current_mesh is not None:
            mesh = self.viewport.current_mesh

            info = f'<b>Файл:</b> {Path(self.current_file).name if self.current_file else "Не указан"}<br><br>'

            # Геометрия
            info += f"<b>Геометрия:</b><br>"
            info += f"Треугольников: {mesh.n_cells}<br>"
            info += f"Вершин: {mesh.n_points}<br><br>"

            # Размеры
            if self.current_stats:
                size = self.current_stats["size"]
                info += f"<b>Размеры:</b><br>"
                info += f"X: {size['x']:.2f} мм<br>"
                info += f"Y: {size['y']:.2f} мм<br>"
                info += f"Z: {size['z']:.2f} мм<br><br>"

                # Объем и площадь
                volume = self.current_stats["volume"]
                area = self.current_stats["surface_area"]
                if volume > 0:
                    info += f"<b>Объем:</b> {volume:.2f} мм³<br>"
                info += f"<b>Площадь:</b> {area:.2f} мм²<br><br>"

            # Валидация
            if self.current_validation:
                info += "<b>Валидация:</b><br>"
                if self.current_validation["valid"]:
                    info += '<span style="color: green;">✓ Модель корректна</span><br>'
                else:
                    info += '<span style="color: red;">✗ Найдены проблемы</span><br>'

                if not self.current_validation["watertight"]:
                    info += '<span style="color: orange;">⚠ Не герметична</span><br>'
                if not self.current_validation["manifold"]["is_manifold"]:
                    info += '<span style="color: orange;">⚠ Non-manifold</span><br>'

            self.info_text.setText(info)
        else:
            self.info_text.setText("Модель не загружена")

    def _on_analyze(self):
        """Обработчик анализа модели"""
        if self.viewport.current_mesh:
            self._perform_analysis()
            self._update_info()

            # Показать детальную информацию
            if self.current_validation:
                issues = self.current_validation["issues"]
                if issues:
                    msg = "Найдены проблемы:\n\n" + "\n".join(f"• {issue}" for issue in issues)
                    QMessageBox.warning(self, "Результаты анализа", msg)
                else:
                    QMessageBox.information(
                        self, "Результаты анализа", "Модель не содержит проблем!"
                    )

    def _on_repair(self):
        """Обработчик ремонта модели"""
        if self.viewport.current_mesh:
            try:
                processor = MeshProcessor(self.viewport.current_mesh)
                repaired_mesh = processor.repair()

                self.viewport.load_mesh(repaired_mesh)
                self._perform_analysis()
                self._update_info()

                self.statusBar().showMessage("Ремонт выполнен", 3000)
                QMessageBox.information(
                    self, "Ремонт модели", "Модель успешно отремонтирована!"
                )
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить ремонт:\n{str(e)}")

    def _on_fix_normals(self):
        """Обработчик исправления нормалей"""
        if self.viewport.current_mesh:
            try:
                processor = MeshProcessor(self.viewport.current_mesh)
                fixed_mesh = processor.fix_normals()

                self.viewport.load_mesh(fixed_mesh)
                self._perform_analysis()
                self._update_info()

                self.statusBar().showMessage("Нормали исправлены", 3000)
                QMessageBox.information(
                    self, "Исправление нормалей", "Нормали успешно исправлены!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Не удалось исправить нормали:\n{str(e)}"
                )

    def _on_about(self):
        """Обработчик О программе"""
        QMessageBox.about(
            self,
            "О программе",
            f"<h3>SolidFlow Desktop</h3>"
            f"<p>Версия {Config.VERSION}</p>"
            f"<p>Desktop-платформа подготовки и оптимизации<br>"
            f"моделей для 3D-печати и мехобработки</p>"
            f"<p><b>Текущий этап:</b> MVP Этап 2 - 3D Визуализация</p>",
        )
