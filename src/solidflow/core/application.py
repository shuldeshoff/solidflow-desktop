"""
Главный класс приложения SolidFlow Desktop
"""

from PySide6.QtWidgets import QApplication
from solidflow.core.config import Config
from solidflow.gui.main_window import MainWindow


class Application:
    """Главный класс приложения"""

    def __init__(self, argv):
        """
        Инициализация приложения

        Args:
            argv: Аргументы командной строки
        """
        self.qt_app = QApplication(argv)
        self.qt_app.setApplicationName("SolidFlow Desktop")
        self.qt_app.setOrganizationName("SolidFlow")
        self.qt_app.setApplicationVersion(Config.VERSION)

        self.main_window = None

    def run(self):
        """
        Запуск приложения

        Returns:
            int: Код возврата приложения
        """
        self.main_window = MainWindow()
        self.main_window.show()

        return self.qt_app.exec()

