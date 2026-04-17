from typing import List, Optional

from src.core.models import Skill as SkillModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import Skill


class SkillRepo:

    def __init__(self, isTest):
        self._log = get_logger("SkillRepo")
        self.db = DatabaseConnection(isTest)

    def create(
        self, model: Optional[SkillModel] = None, name: Optional[str] = None
    ) -> int:
        """Accepts a `core.models.Skill` instance or legacy `name` parameter."""
        result = None

        if model is None and name is not None:
            model = SkillModel(name=name)

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                skill = Skill(name=model.name)  # type: ignore
                session.add(skill)
                session.commit()

                result = skill.id
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Skill: {model}")
                raise e

        return result  # type: ignore

    def create_from_model(self, model: SkillModel) -> int:
        """Create using a `core.models.Skill` instance."""
        return self.create(model=model)

    def create_from_fields(self, name: str) -> int:
        """Create using individual fields (legacy style)."""
        return self.create(name=name)

    def get_by_id(self, skill_id: int) -> Optional[Skill]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Skill).filter(Skill.id == skill_id).first()

    def get_all(self) -> List[Skill]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Skill).all()

    def update(
        self,
        skill_id: int,
        model: Optional[SkillModel] = None,
        name: Optional[str] = None,
    ) -> Skill:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                skill = session.query(Skill).filter(Skill.id == skill_id).first()
                if not skill:
                    raise ValueError(f"Skill with id {skill_id} not found")
                if model is not None:
                    skill.name = model.name  # type: ignore
                elif name is not None:
                    skill.name = name  # type: ignore

                session.add(skill)
                session.commit()

                return skill

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating Skill: {skill}")
                raise e

    def delete(self, skill_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                skill = session.query(Skill).filter(Skill.id == skill_id).first()
                if not skill:
                    raise ValueError(f"Skill with id {skill_id} not found")
                session.delete(skill)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting Skill: {skill}")
                raise e

            return True
