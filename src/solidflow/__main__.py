"""
Главная точка входа в приложение SolidFlow Desktop
"""

import logging
import platform
import sys

from solidflow.core.logging_setup import install_excepthook, install_qt_message_handler, setup_logging


def main():
    """Запуск приложения"""
    log_file = setup_logging(app_name="SolidFlow")
    install_excepthook("SolidFlow")
    install_qt_message_handler("SolidFlow.Qt")

    logging.getLogger("SolidFlow").info(
        "Starting SolidFlow. python=%s platform=%s argv=%s log=%s",
        sys.executable,
        platform.platform(),
        sys.argv,
        log_file,
    )

    # Важно: импортируем Qt/приложение ПОСЛЕ настройки логирования
    from solidflow.core.application import Application

    app = Application(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())

