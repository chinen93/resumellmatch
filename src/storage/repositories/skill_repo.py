from typing import List, Optional

from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import Skill


class SkillRepo:

    def __init__(self, isTest):
        self._log = get_logger("SkillRepo")
        self.db = DatabaseConnection(isTest)

    def create(self, name: str) -> int:
        result = None

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                skill = Skill(name=name)
                session.add(skill)
                session.commit()

                result = int(skill.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Skill: {skill}")
                raise e

        return result

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

    def update(self, skill_id: int, name: Optional[str] = None) -> Skill:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                skill = session.query(Skill).filter(Skill.id == skill_id).first()
                if not skill:
                    raise ValueError(f"Skill with id {skill_id} not found")
                if name is not None:
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
