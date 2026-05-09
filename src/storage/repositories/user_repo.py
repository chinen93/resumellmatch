from typing import List, Optional

from src.core.models import User as UserModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.mappers.user_mapper import UserMapper
from src.storage.models import User


class UserRepo:
    def __init__(self, isTest):
        self._log = get_logger("UserRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: UserModel) -> int:
        """Create or update a User from a model (checks by email)."""

        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = UserMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(self, id: int, name: str, email: str) -> int:
        """Create using individual fields (builds model internally)."""
        model = UserMapper.from_raw_fields(id, name, email)
        return self.create_or_update(model)

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(user_id)

        if not storage_model:
            return None

        return UserMapper.to_core_model(storage_model)

    def get_all(self) -> List[UserModel]:
        """Fetches all records and converts them to the Core Model list."""
        with self.db.get_session() as session:
            storage_models = session.query(User).all()

            return [UserMapper.to_core_model(model) for model in storage_models]

    def delete(self, user_id: int) -> bool:
        storage_model = self._retrieve(user_id)

        if not storage_model:
            self._log.debug(f"User with id {user_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(self, core_model: UserModel) -> User:

        storage_model = UserMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve(core_model.id)
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: User) -> int:
        """Create a User from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating User: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve(self, user_id: int) -> Optional[User]:
        with self.db.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()

    def _retrieve_by_email(self, email: str) -> Optional[User]:
        with self.db.get_session() as session:
            return session.query(User).filter(User.email == email).first()

    def _update(self, storage_model: User, core_model: UserModel) -> int:
        storage_model.name = core_model.name
        storage_model.email = core_model.email

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating User: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: User) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting User: {e}")
                raise e

        return True
