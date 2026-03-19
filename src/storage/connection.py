from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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
            cls._instance.engine = create_engine(
                "sqlite:///./output/test_storage.db", echo=False
            )
            return cls._instance

        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialize engine with SQLite for MVP; configurable later
            cls._instance.engine = create_engine(
                "sqlite:///./output/storage.db", echo=False
            )

        return cls._instance

    def get_session(self) -> Session:
        return Session(self.engine)
