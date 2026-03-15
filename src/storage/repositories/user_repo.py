from typing import List, Optional

from src.storage.connection import DatabaseConnection
from src.storage.models import User

db = DatabaseConnection()


class UserRepo:
    @classmethod
    def create(cls, name: str, email: str) -> int:
        result = None

        with db.get_session() as session:
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
                print("Error when creating User:", user)
                raise e

        return result

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[User]:
        with db.get_session() as session:
            session.begin()
            session.expire_on_commit = False
            return session.query(User).filter(User.id == user_id).first()

    @classmethod
    def get_all(cls) -> List[User]:
        with db.get_session() as session:
            session.begin()
            return session.query(User).all()

    @classmethod
    def update(
        cls, user_id: int, name: Optional[str] = None, email: Optional[str] = None
    ) -> User:
        with db.get_session() as session:
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
                print("Error when deleting User:", user)
                raise e

    @classmethod
    def delete(cls, user_id: int) -> bool:
        with db.get_session() as session:
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
                print("Error when deleting User:", user)
                raise e

            return True
