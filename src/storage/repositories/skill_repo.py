from typing import List, Optional

from src.core.models import Skill as SkillModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.mappers.skill_mapper import SkillMapper
from src.storage.models import Skill


class SkillRepo:
    def __init__(self, isTest):
        self._log = get_logger("SkillRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: SkillModel) -> int:
        """Create or update a Skill from a model (checks by name)."""
        if core_model.id is None:
            return -1

        storage_model = self._retrieve(core_model.id)
        if storage_model is None:
            storage_model = self._retrieve_by_name(core_model.name)

        if storage_model is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = SkillMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(self, id: int, name: str) -> int:
        """Create using individual fields (builds model internally)."""
        model = SkillMapper.from_raw_fields(id, name)
        return self.create_or_update(model)

    def get_by_id(self, skill_id: int) -> Optional[SkillModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(skill_id)

        if not storage_model:
            return None

        return SkillMapper.to_core_model(storage_model)

    def get_all(self) -> List[SkillModel]:
        """Fetches all records and converts them to the Core Model list."""
        with self.db.get_session() as session:
            storage_models = session.query(Skill).all()

            return [SkillMapper.to_core_model(model) for model in storage_models]

    def delete(self, skill_id: int) -> bool:
        storage_model = self._retrieve(skill_id)

        if not storage_model:
            self._log.debug(f"Skill with id {skill_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _create(self, storage_model: Skill) -> int:
        """Create a Skill from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()
                return int(storage_model.id)

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Skill: {e}")
                raise e

    def _retrieve(self, skill_id: int) -> Optional[Skill]:
        with self.db.get_session() as session:
            return session.query(Skill).filter(Skill.id == skill_id).first()

    def _retrieve_by_name(self, name: str) -> Optional[Skill]:
        with self.db.get_session() as session:
            return session.query(Skill).filter(Skill.name == name).first()

    def _update(self, storage_model: Skill, core_model: SkillModel) -> int:
        storage_model.name = core_model.name

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

                return int(storage_model.id)

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating Skill: {e}")
                raise e

    def _delete(self, storage_model: Skill) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting Skill: {e}")
                raise e

        return True
