# =========================================================
# Helper Decorator (This handles the boilerplate)
# =========================================================
def db_transaction(func):
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
