from typing import List, Optional

from src.core.models import User as UserModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import User


class UserRepo:

    def __init__(self, isTest):
        self._log = get_logger("UserRepo")
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        model: Optional[UserModel] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> int:
        result = None

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            try:
                if model is None:
                    model = UserModel(name=name or "", email=email or "")

                user = User(name=model.name, email=model.email)
                session.add(user)
                session.commit()

                result = int(user.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating User: {user}")
                raise e

        return result

    def create_from_model(self, model: UserModel) -> int:
        """Create using a `core.models.User` instance."""
        return self.create(model=model)

    def create_from_fields(self, name: str, email: str) -> int:
        """Create using individual fields (legacy style)."""
        return self.create(name=name, email=email)

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
        self,
        user_id: int,
        model: Optional[UserModel] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> User:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            try:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    raise ValueError(f"User with id {user_id} not found")
                if model is not None:
                    if model.name is not None:
                        user.name = model.name  # type: ignore
                    if model.email is not None:
                        user.email = model.email  # type: ignore
                else:
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
