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

    Example:
        # In your main.py or application startup
        from src.logging_config import setup_logging

        if __name__ == "__main__":
            setup_logging(testing=False)
            # Your application code here

        # In your test conftest.py
        import pytest
        from src.logging_config import setup_logging

        @pytest.fixture(scope="session", autouse=True)
        def configure_test_logging():
            setup_logging(testing=True)
    """
    # Ensure logs directory exists for production mode
    if not testing:
        ensure_logs_directory()

    # Get the appropriate config file
    config_file = get_config_path(testing=testing)

    # Load logging configuration
    logging.config.fileConfig(config_file, disable_existing_loggers=False)

    mode = "TESTING" if testing else "PRODUCTION"

    logger = logging.getLogger(__name__)
    logger.info("=" * 30)
    logger.debug(f"Logging configured for {mode} mode using {config_file}")


def disable_logging() -> None:
    """
    Completely disable logging (useful for tests that don't want any output).

    Example:
        from src.logging_config import disable_logging

        class MyTestCase(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                disable_logging()
    """
    logging.disable(logging.CRITICAL)


def enable_logging() -> None:
    """
    Re-enable logging after it was disabled.

    Example:
        from src.logging_config import enable_logging

        class MyTestCase(unittest.TestCase):
            @classmethod
            def tearDownClass(cls):
                enable_logging()
    """
    logging.disable(logging.NOTSET)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance

    Example:
        from src.logging_config import get_logger

        logger = get_logger(__name__)
        logger.info("Application started")
    """
    return logging.getLogger(name)
