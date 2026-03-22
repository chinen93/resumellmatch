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
import logging.config
from pathlib import Path

from config.settings import get_settings


def get_config_path(testing: bool = False) -> str:
    """
    Get the path to the appropriate logging configuration file.

    Args:
        testing: If True, return path to test config; otherwise production config

    Returns:
        Absolute path to the logging configuration file
    """
    config_dir = Path(__file__).parent.parent / "config"

    if testing:
        config_file = config_dir / "logging_test.conf"
    else:
        config_file = config_dir / "logging.conf"

    if not config_file.exists():
        raise FileNotFoundError(f"Logging configuration file not found: {config_file}")

    return str(config_file)


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

    # Get the appropriate config file
    # config_file = get_config_path(testing=testing)

    # Load logging configuration
    # logging.config.fileConfig(config_file, disable_existing_loggers=False)

    # mode = "TESTING" if testing else "PRODUCTION"

    # logger = logging.getLogger(__name__)
    # logger.info("=" * 30)
    # logger.debug(f"Logging configured for {mode} mode using {config_file}")


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
        ch.setLevel(level)
        ch.setFormatter(formatter)
        root.addHandler(ch)

    if settings.LOG_FILE:
        fh = logging.FileHandler(settings.LOG_FILE)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        root.addHandler(fh)

    root.info("=" * 30)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    """
    print(name)
    configure_root_logger()
    return logging.getLogger(name)
