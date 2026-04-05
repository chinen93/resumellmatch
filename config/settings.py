import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Singleton(type):
    _instances: dict[type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def dependent_load_dotenv(isTest=False):

    print("a" * 20)

    BASE_DIR = Path(__file__).parent.parent
    env_file = str(BASE_DIR) + "/"

    if isTest:
        env_file += ".env.test"
    else:
        env_file += ".env"

    print(f"loading {env_file}")
    load_dotenv(env_file)

    return get_settings()


def get_settings():  # type: ignore

    @dataclass(frozen=True)
    class Settings(metaclass=Singleton):
        ENVIRONMENT: Optional[str] = os.getenv("ENVIRONMENT")  # type: ignore

        LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # type: ignore

        LOG_FORMAT: Optional[str] = os.getenv("LOG_FORMAT")  # type: ignore
        LOG_FILE: Optional[str] = os.getenv("LOG_FILE")  # type: ignore
        LOG_TO_CONSOLE: Optional[str] = os.getenv("LOG_TO_CONSOLE")  # type: ignore
        DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")  # type: ignore

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
                }.items()
                if value is None or (isinstance(value, str) and not value.strip())
            ]
            if missing:
                raise ValueError(f"Missing required settings: {', '.join(missing)}")

    settings = Settings()
    print(settings)
    return settings
