"""
Главное окно приложения
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from solidflow.core.config import Config


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()

        self.setWindowTitle(Config.WINDOW_TITLE)
        self.resize(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        self._setup_ui()
        self._create_menu()

    def _setup_ui(self):
        """Настройка UI"""
        # Центральный виджет (временно с заглушкой)
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Заглушка - будет заменена на 3D viewport
        placeholder = QLabel("3D Viewport (будет добавлен на следующем этапе)")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(
            "QLabel { background-color: #2b2b2b; color: #888; font-size: 16px; }"
        )

        layout.addWidget(placeholder)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Меню File
        file_menu = menubar.addMenu("Файл")

        # Action: Open
        open_action = QAction("Открыть...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Открыть STL файл")
        open_action.triggered.connect(self._on_open)
        file_menu.addAction(open_action)

        # Action: Save
        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Сохранить модель")
        save_action.setEnabled(False)  # Пока не реализовано
        file_menu.addAction(save_action)

        # Action: Save As
        save_as_action = QAction("Сохранить как...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.setStatusTip("Сохранить модель в новый файл")
        save_as_action.setEnabled(False)  # Пока не реализовано
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Action: Exit
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Выйти из приложения")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Help
        help_menu = menubar.addMenu("Справка")

        # Action: About
        about_action = QAction("О программе", self)
        about_action.setStatusTip("О программе SolidFlow Desktop")
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

        # Статус бар
        self.statusBar().showMessage("Готово")

    def _on_open(self):
        """Обработчик открытия файла (заглушка)"""
        self.statusBar().showMessage("Открытие файла (будет реализовано на Этапе 3)", 3000)

    def _on_about(self):
        """Обработчик О программе"""
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.about(
            self,
            "О программе",
            f"<h3>SolidFlow Desktop</h3>"
            f"<p>Версия {Config.VERSION}</p>"
            f"<p>Desktop-платформа подготовки и оптимизации<br>"
            f"моделей для 3D-печати и мехобработки</p>",
        )

