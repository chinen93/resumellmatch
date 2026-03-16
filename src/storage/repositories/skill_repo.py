from typing import List, Optional

from src.storage.connection import DatabaseConnection
from src.storage.models import Skill

db = DatabaseConnection()


class SkillRepo:
    @classmethod
    def create(cls, name: str) -> int:
        result = None

        with db.get_session() as session:
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
                print("Error when creating Skill:", skill)
                raise e

        return result

    @classmethod
    def get_by_id(cls, skill_id: int) -> Optional[Skill]:
        with db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Skill).filter(Skill.id == skill_id).first()

    @classmethod
    def get_all(cls) -> List[Skill]:
        with db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Skill).all()

    @classmethod
    def update(cls, skill_id: int, name: Optional[str] = None) -> Skill:
        with db.get_session() as session:
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
                print("Error when updating Skill:", skill)
                raise e

    @classmethod
    def delete(cls, skill_id: int) -> bool:
        with db.get_session() as session:
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
                print("Error when deleting Skill:", skill)
                raise e

            return True
