import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class Singleton(type):
    _instances: dict[type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def dependent_load_dotenv(isTest=False) -> None:

    print("a" * 20)

    if isTest:
        BASE_DIR = Path(__file__).parent.parent
        env_file = BASE_DIR / ".env.test"
        print(env_file, env_file.exists())
        load_dotenv(env_file)
    else:
        load_dotenv()

    return get_settings()


def get_settings():  # type: ignore

    @dataclass(frozen=True)
    class Settings(metaclass=Singleton):
        ENVIRONMENT: str = os.getenv("ENVIRONMENT")

        LOG_LEVEL: str = os.getenv("LOG_LEVEL")
        LOG_FORMAT: str = os.getenv("LOG_FORMAT")
        LOG_FILE: str = os.getenv("LOG_FILE")
        LOG_TO_CONSOLE: bool = os.getenv("LOG_TO_CONSOLE")
        DATABASE_URL: str = os.getenv("DATABASE_URL")

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
