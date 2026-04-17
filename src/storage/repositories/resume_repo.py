from typing import List, Optional

from src.core.models import Resume as ResumeModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import Resume


class ResumeRepo:
    def __init__(self, isTest):
        self._log = get_logger("ResumeRepo")
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        model: Optional[ResumeModel] = None,
        user_id: Optional[int] = None,
        raw_text: Optional[str] = None,
    ) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                if model is None:
                    model = ResumeModel(user_id=user_id, raw_text=raw_text or "")

                resume = Resume(user_id=model.user_id, raw_text=model.raw_text)
                session.add(resume)
                session.commit()

                result = int(resume.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Resume: {e}")
                raise e

        return result

    def create_from_model(self, model: ResumeModel) -> int:
        """Create using a `core.models.Resume` instance."""
        return self.create(model=model)

    def create_from_fields(self, user_id: int, raw_text: str) -> int:
        """Create using individual fields (legacy style)."""
        return self.create(user_id=user_id, raw_text=raw_text)

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
        model: Optional[ResumeModel] = None,
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
                if model is not None:
                    if model.user_id is not None:
                        resume.user_id = model.user_id  # type: ignore
                    if model.raw_text is not None:
                        resume.raw_text = model.raw_text  # type: ignore
                else:
                    if user_id is not None:
                        resume.user_id = user_id  # type: ignore
                    if raw_text is not None:
                        resume.raw_text = raw_text  # type: ignore

                session.add(resume)
                session.commit()

                return resume

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating Resume: {e}")
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
                self._log.error(f"Error when deleting Resume: {e}")
                raise e

            return True
