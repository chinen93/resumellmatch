from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# TODO
# Add another database connection to be used on the tests, and pass it via dependency injection


class DatabaseConnection:
    """
    Singleton class to manage SQLAlchemy database connections and sessions.
    Provides an execute method to handle session lifecycle, transactions, and error handling,
    allowing repositories to focus on CRUD operations by supplying callables.
    """

    _instance = None

    engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialize engine with SQLite for MVP; configurable later
            cls._instance.engine = create_engine(
                "sqlite:///./output/storage.db", echo=False
            )
        return cls._instance

    def get_session(self) -> Session:
        return Session(self.engine)
