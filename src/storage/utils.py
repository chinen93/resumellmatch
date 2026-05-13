"""Storage transaction utilities.

This module provides helper decorators for managing database transaction
lifecycles, including commit and rollback behavior.
"""


# =========================================================
# Helper Decorator (This handles the boilerplate)
# =========================================================
def db_transaction(func):
    """Decorator that manages SQLAlchemy session transaction lifecycle.

    This decorator wraps repository methods to open a session, begin a
    transaction, commit on success, and rollback on exception.
    """
    """Handles session setup, commit, rollback, and logging for write operations."""

    def wrapper(self, *args, **kwargs):
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            try:
                result = func(self, session, *args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                self._log.error(f"Transaction failed in {func.__name__}: {e}")
                raise e

    return wrapper
