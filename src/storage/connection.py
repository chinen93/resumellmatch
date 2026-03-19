from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.logging_config import get_logger

_log = get_logger("Connection")

TEST_ENGINE = "sqlite:///./output/test_storage.db"
PROD_ENGINE = "sqlite:///./output/storage.db"


class DatabaseConnection:
    """
    Singleton class to manage SQLAlchemy database connections and sessions.
    Provides an execute method to handle session lifecycle, transactions, and error handling,
    allowing repositories to focus on CRUD operations by supplying callables.
    """

    _instance = None

    engine = None

    def __new__(cls, isTest=False):

        if isTest:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(TEST_ENGINE, echo=False)
            _log.debug("New Connection to '%s'", TEST_ENGINE)
            return cls._instance

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialize engine with SQLite for MVP; configurable later
            cls._instance.engine = create_engine(PROD_ENGINE, echo=False)

            _log.debug("New Connection to '%s'", PROD_ENGINE)

        return cls._instance

    def get_session(self) -> Session:
        return Session(self.engine)
