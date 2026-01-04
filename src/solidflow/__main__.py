"""
Главная точка входа в приложение SolidFlow Desktop
"""

import sys
from solidflow.core.application import Application


def main():
    """Запуск приложения"""
    app = Application(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())

