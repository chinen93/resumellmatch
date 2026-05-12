"""
Logging configuration manager.

This module provides functions to configure logging based on the environment:
- Production/Normal mode: logs to both console and file
- Testing mode: uses NullHandler to suppress output

Usage:
    # In your main application startup
    from src.logging_config import setup_logging
    setup_logging(testing=False)

    # In your test setup
    from src.logging_config import setup_logging
    setup_logging(testing=True)
"""

import logging
from pathlib import Path

from config.settings import dependent_load_dotenv, get_settings


def ensure_logs_directory() -> None:
    """Create logs directory if it doesn't exist."""
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)


def setup_logging(testing: bool = False) -> None:
    """
    Configure logging for the application.

    Args:
        testing: If True, use test configuration (suppresses logs).
                If False, use production configuration (logs to file and console).
    """
    # Ensure logs directory exists for production mode
    if not testing:
        ensure_logs_directory()

    dependent_load_dotenv(isTest=False)


def configure_root_logger() -> None:

    root = logging.getLogger()
    if root.handlers:
        return

    settings = get_settings()

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root.setLevel(level)

    formatter = logging.Formatter(settings.LOG_FORMAT)

    if settings.LOG_TO_CONSOLE:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        root.addHandler(ch)

    if settings.LOG_FILE:
        fh = logging.FileHandler(settings.LOG_FILE)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        root.addHandler(fh)

    root.info("=" * 30)
    root.debug(f"ENV FILE: '{settings.ENV_FILEPATH}'")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    """
    configure_root_logger()
    return logging.getLogger(name)
