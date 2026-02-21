"""Logging helpers using loguru."""

import sys

from loguru import logger


def configure_logger(level: str = "INFO") -> None:
    """Configure a structured console logger."""
    logger.remove()
    logger.add(sys.stderr, level=level, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")


__all__ = ["logger", "configure_logger"]
