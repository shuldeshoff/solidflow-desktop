"""
Главный класс приложения SolidFlow Desktop
"""

import logging

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
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
        log = logging.getLogger("SolidFlow.Application")
        log.info("Creating MainWindow...")
        self.main_window = MainWindow()
        log.info("Showing MainWindow...")
        self.main_window.show()

        # На macOS иногда полезно явно активировать окно.
        def _activate():  # type: ignore[no-untyped-def]
            try:
                self.main_window.raise_()
                self.main_window.activateWindow()
            except Exception:
                log.exception("Failed to activate main window")

        QTimer.singleShot(0, _activate)
        log.info("Entering Qt event loop...")
        return self.qt_app.exec()

