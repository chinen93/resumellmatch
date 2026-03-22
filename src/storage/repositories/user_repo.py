from typing import List, Optional

from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import User


class UserRepo:

    def __init__(self, isTest):
        self._log = get_logger("UserRepo")
        self.db = DatabaseConnection(isTest)

    def create(self, name: str, email: str) -> int:
        result = None

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            try:
                user = User(name=name, email=email)
                session.add(user)
                session.commit()

                result = int(user.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating User: {user}")
                raise e

        return result

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            return session.query(User).filter(User.id == user_id).first()

    def get_all(self) -> List[User]:
        with self.db.get_session() as session:
            session.begin()
            return session.query(User).all()

    def update(
        self, user_id: int, name: Optional[str] = None, email: Optional[str] = None
    ) -> User:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            try:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    raise ValueError(f"User with id {user_id} not found")
                if name is not None:
                    user.name = name  # type: ignore
                if email is not None:
                    user.email = email  # type: ignore

                session.add(user)
                session.commit()

                return user

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating User: {user}")
                raise e

    def delete(self, user_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    raise ValueError(f"User with id {user_id} not found")
                session.delete(user)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.debug(f"Error when deleting User: {user_id}")
                raise e

            return True
