"""Database connection utilities for storage layer.

This module defines the application database connection manager and provides
singleton access to SQLAlchemy sessions for production and test environments.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

TEST_ENGINE = "sqlite:///./example/output/test_storage.db"
PROD_ENGINE = "sqlite:///./example/output/storage.db"


class DatabaseConnection:
    """Singleton managing SQLAlchemy engine and sessions.

    Attributes:
        engine: SQLAlchemy engine instance for the configured database.
    """

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
            return cls._instance

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialize engine with SQLite for MVP; configurable later
            cls._instance.engine = create_engine(PROD_ENGINE, echo=False)

        return cls._instance

    def get_session(self) -> Session:
        return Session(self.engine)
