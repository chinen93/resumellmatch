from typing import List, Optional

from src.core.models import Resume as ResumeModel
from config.logging import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.mappers.resume_mapper import ResumeMapper
from src.storage.models import Resume


class ResumeRepo:
    def __init__(self, isTest):
        self._log = get_logger("ResumeRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: ResumeModel) -> int:
        """Create or update a Resume from a model (checks by user_id)."""

        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = ResumeMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self,
        id: Optional[int],
        user_id: int,
        raw_text: str,
        input_hash: Optional[str],
        full_text: Optional[str],
    ) -> int:
        """Create using individual fields (builds model internally)."""
        model = ResumeMapper.from_raw_fields(
            id, user_id, raw_text, input_hash, full_text
        )
        return self.create_or_update(model)

    def get_by_id(self, resume_id: int) -> Optional[ResumeModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(resume_id)

        if not storage_model:
            return None

        return ResumeMapper.to_core_model(storage_model)

    def get_by_user_id(self, user_id: int) -> Optional[ResumeModel]:
        """Fetches by user_id and converts to Core Model."""
        storage_model = self._retrieve_by_user_id(user_id)

        if not storage_model:
            return None

        return ResumeMapper.to_core_model(storage_model)

    def get_by_input_hash(self, input_hash: str) -> Optional[ResumeModel]:
        """Fetches by input_hash and converts to Core Model."""
        storage_model = self._retrieve_by_input_hash(input_hash)

        if not storage_model:
            return None

        return ResumeMapper.to_core_model(storage_model)

    def get_all(self) -> List[ResumeModel]:
        """Fetches all records and converts them to the Core Model list."""
        with self.db.get_session() as session:
            storage_models = session.query(Resume).all()

            return [ResumeMapper.to_core_model(model) for model in storage_models]

    def delete(self, resume_id: int) -> bool:
        storage_model = self._retrieve(resume_id)

        if not storage_model:
            self._log.debug(f"Resume with id {resume_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(self, core_model: ResumeModel) -> Resume:

        storage_model = ResumeMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve(core_model.id)
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: Resume) -> int:
        """Create a Resume from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Resume: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve(self, resume_id: int) -> Optional[Resume]:
        with self.db.get_session() as session:
            return session.query(Resume).filter(Resume.id == resume_id).first()

    def _retrieve_by_user_id(self, user_id: int) -> Optional[Resume]:
        with self.db.get_session() as session:
            return session.query(Resume).filter(Resume.user_id == user_id).first()

    def _retrieve_by_input_hash(self, input_hash: str) -> Optional[Resume]:
        with self.db.get_session() as session:
            return session.query(Resume).filter(Resume.input_hash == input_hash).first()

    def _update(self, storage_model: Resume, core_model: ResumeModel) -> int:
        storage_model.user_id = (
            core_model.user_id if core_model.user_id is not None else -1
        )
        storage_model.raw_text = core_model.raw_text

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating Resume: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: Resume) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting Resume: {e}")
                raise e

        return True
