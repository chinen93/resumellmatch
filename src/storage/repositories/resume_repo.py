from typing import List, Optional

from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import Resume

_log = get_logger("ResumeRepo")


class ResumeRepo:
    def __init__(self, isTest):
        self.db = DatabaseConnection(isTest)

    def create(self, user_id: int, raw_text: str) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                resume = Resume(user_id=user_id, raw_text=raw_text)
                session.add(resume)
                session.commit()

                result = int(resume.id)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error(f"Error when creating Resume: {e}")
                raise e

        return result

    def get_by_id(self, resume_id: int) -> Optional[Resume]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Resume).filter(Resume.id == resume_id).first()

    def get_all(self) -> List[Resume]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Resume).all()

    def get_all_by_user_id(self, user_id: int) -> List[Resume]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Resume).filter(Resume.user_id == user_id).all()

    def update(
        self,
        resume_id: int,
        user_id: Optional[int] = None,
        raw_text: Optional[str] = None,
    ) -> Resume:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                resume = session.query(Resume).filter(Resume.id == resume_id).first()
                if not resume:
                    raise ValueError(f"Resume with id {resume_id} not found")
                if user_id is not None:
                    resume.user_id = user_id  # type: ignore
                if raw_text is not None:
                    resume.raw_text = raw_text  # type: ignore

                session.add(resume)
                session.commit()

                return resume

            except Exception as e:
                session.rollback()
                _log.error(f"Error when updating Resume: {e}")
                raise e

    def delete(self, resume_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                resume = session.query(Resume).filter(Resume.id == resume_id).first()
                if not resume:
                    raise ValueError(f"Resume with id {resume_id} not found")
                session.delete(resume)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error(f"Error when deleting Resume: {e}")
                raise e

            return True
