"""
Инициализация логирования для SolidFlow Desktop.

Цель: иметь логи даже в случае падения приложения до показа окна (особенно в .app).
"""

from __future__ import annotations

import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def _default_log_dir() -> Path:
    home = Path.home()
    if platform.system() == "Darwin":
        return home / "Library" / "Logs" / "SolidFlow"
    return home / ".solidflow" / "logs"


def setup_logging(
    *,
    app_name: str = "SolidFlow",
    level: Optional[str] = None,
    log_dir: Optional[Path] = None,
) -> Path:
    """
    Настроить логирование в файл (и в stderr в режиме разработки).

    Управление:
    - SOLIDFLOW_LOG_LEVEL: DEBUG/INFO/WARNING/ERROR (по умолчанию INFO)
    - SOLIDFLOW_LOG_STDERR=1: дублировать в stderr (удобно при запуске из терминала)
    """

    log_dir = log_dir or _default_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "solidflow.log"

    env_level = (level or os.environ.get("SOLIDFLOW_LOG_LEVEL") or "INFO").upper()
    numeric_level = getattr(logging, env_level, logging.INFO)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s %(process)d %(threadName)s "
        "%(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Не добавляем обработчики повторно (например, при перезапуске внутри одного процесса)
    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    if os.environ.get("SOLIDFLOW_LOG_STDERR") == "1" and not any(
        isinstance(h, logging.StreamHandler) for h in root.handlers
    ):
        stream = logging.StreamHandler(stream=sys.stderr)
        stream.setLevel(numeric_level)
        stream.setFormatter(formatter)
        root.addHandler(stream)

    logging.getLogger(app_name).info("Logging initialized. File: %s", log_file)
    return log_file


def install_excepthook(logger_name: str = "SolidFlow") -> None:
    """
    Логировать необработанные исключения (включая те, что до UI).
    """

    logger = logging.getLogger(logger_name)
    original_hook = sys.excepthook

    def _hook(exc_type, exc, tb):  # type: ignore[no-untyped-def]
        try:
            logger.exception("Unhandled exception", exc_info=(exc_type, exc, tb))
        finally:
            original_hook(exc_type, exc, tb)

    sys.excepthook = _hook  # type: ignore[assignment]


def install_qt_message_handler(logger_name: str = "SolidFlow.Qt") -> None:
    """
    Перехватить сообщения Qt (warnings/errors), чтобы они попадали в лог.
    """

    try:
        from PySide6.QtCore import QtMsgType, qInstallMessageHandler  # type: ignore
    except Exception:
        # Если Qt не импортируется, логгер все равно будет полезен.
        logging.getLogger(logger_name).warning("Qt is not available; Qt message handler not installed.")
        return

    logger = logging.getLogger(logger_name)

    def _handler(msg_type, context, message):  # type: ignore[no-untyped-def]
        # context может быть пустым в зависимости от сборки Qt
        prefix = getattr(QtMsgType, "name", None)
        if msg_type == QtMsgType.QtDebugMsg:
            logger.debug("%s", message)
        elif msg_type == QtMsgType.QtInfoMsg:
            logger.info("%s", message)
        elif msg_type == QtMsgType.QtWarningMsg:
            logger.warning("%s", message)
        elif msg_type == QtMsgType.QtCriticalMsg:
            logger.error("%s", message)
        elif msg_type == QtMsgType.QtFatalMsg:
            logger.critical("%s", message)
        else:
            logger.info("%s", message)

    qInstallMessageHandler(_handler)


