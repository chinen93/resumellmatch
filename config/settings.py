"""Configuration settings management for the application.

This module handles loading environment variables from .env files and providing
a singleton Settings object containing all application configuration parameters.
Settings are validated on initialization to ensure all required values are present.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

ENV_FILEPATH = ""


class Singleton(type):
    """Metaclass implementing the singleton pattern.

    Ensures that only one instance of a class is created and reused
    across the application.

    Attributes:
        _instances: Dictionary storing singleton instances by class.
    """

    _instances: dict[type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def dependent_load_dotenv(isTest=False):
    """Load environment variables from .env file and return settings.

    Loads environment variables from either .env (production) or .env.test
    (test) file and returns the singleton Settings instance.

    Args:
        isTest: If True, loads from .env.test; if False, loads from .env.

    Returns:
        Settings: The singleton Settings instance.

    Raises:
        ValueError: If required settings are missing from the .env file.
    """
    BASE_DIR = Path(__file__).parent.parent
    env_file = str(BASE_DIR) + "/"

    if isTest:
        env_file += ".env.test"
    else:
        env_file += ".env"

    global ENV_FILEPATH
    ENV_FILEPATH = env_file
    load_dotenv(env_file)

    return get_settings()


def get_settings():  # type: ignore
    """Get the singleton Settings instance.

    Returns the singleton Settings object containing all application configuration.
    On first call, initializes Settings from environment variables and validates
    that all required settings are present.

    Returns:
        Settings: The singleton Settings instance.

    Raises:
        ValueError: If any required settings are missing or invalid.
    """

    @dataclass(frozen=True)
    class Settings(metaclass=Singleton):
        """Frozen dataclass containing all application settings.

        All settings are loaded from environment variables at startup.
        The class is frozen to prevent accidental modification of settings.

        Attributes:
            ENV_FILEPATH: Path to the .env file being used.
            ENVIRONMENT: Current environment (e.g., 'development', 'production').
            LOG_LEVEL: Logging verbosity level (e.g., 'INFO', 'DEBUG', 'ERROR').
            LOG_FORMAT: Log message format string.
            LOG_FILE: Path to log file.
            LOG_TO_CONSOLE: Whether to output logs to console.
            DATABASE_URL: SQLAlchemy database connection URL.
            DATA_DIR: Directory for data files.
            AGENT_MODEL: LLM model identifier for Ollama.
        """

        ENV_FILEPATH: str = ENV_FILEPATH  # type: ignore

        ENVIRONMENT: Optional[str] = os.getenv("ENVIRONMENT")  # type: ignore

        LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # type: ignore

        LOG_FORMAT: Optional[str] = os.getenv("LOG_FORMAT")  # type: ignore
        LOG_FILE: Optional[str] = os.getenv("LOG_FILE")  # type: ignore
        LOG_TO_CONSOLE: Optional[str] = os.getenv("LOG_TO_CONSOLE")  # type: ignore
        DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")  # type: ignore
        DATA_DIR: Optional[str] = os.getenv("DATA_DIR")  # type: ignore
        AGENT_MODEL: Optional[str] = os.getenv("AGENT_MODEL")  # type: ignore

        def __post_init__(self):
            missing = [
                key
                for key, value in {
                    "ENVIRONMENT": self.ENVIRONMENT,
                    "LOG_LEVEL": self.LOG_LEVEL,
                    "LOG_FORMAT": self.LOG_FORMAT,
                    "LOG_FILE": self.LOG_FILE,
                    "LOG_TO_CONSOLE": self.LOG_TO_CONSOLE,
                    "DATABASE_URL": self.DATABASE_URL,
                    "DATA_DIR": self.DATA_DIR,
                    "AGENT_MODEL": self.AGENT_MODEL,
                }.items()
                if value is None or (isinstance(value, str) and not value.strip())
            ]
            if missing:
                raise ValueError(
                    f"File '{ENV_FILEPATH}' missing required settings: {', '.join(missing)}"
                )

    settings = Settings()
    return settings
