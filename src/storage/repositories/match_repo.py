from typing import List, Optional

from src.core.models import Match as MatchModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import Matches


class MatchRepo:
    def __init__(self, isTest):
        self._log = get_logger("MatchRepo")
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        model: Optional[MatchModel] = None,
        resume_id: Optional[int] = None,
        job_description_parsed_id: Optional[int] = None,
        score: Optional[int] = None,
        llm_analysis: Optional[str] = None,
    ) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                if model is None:
                    model = MatchModel(
                        resume_id=resume_id,
                        job_description_parsed_id=job_description_parsed_id,
                        score=score or 0,
                        llm_analysis=llm_analysis or "",
                    )

                match = Matches(
                    resume_id=model.resume_id,
                    job_description_parsed_id=model.job_description_parsed_id,
                    score=model.score,
                    llm_analysis=model.llm_analysis,
                )
                session.add(match)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Match: {e}")
                raise e

        return True

    def create_from_model(self, model: MatchModel) -> bool:
        """Create a Match using a `core.models.Match` instance."""
        return self.create(model=model)

    def create_from_fields(
        self,
        resume_id: int,
        job_description_parsed_id: int,
        score: int,
        llm_analysis: str,
    ) -> bool:
        """Create a Match using individual fields (legacy style)."""
        return self.create(
            resume_id=resume_id,
            job_description_parsed_id=job_description_parsed_id,
            score=score,
            llm_analysis=llm_analysis,
        )

    def get_by_ids(
        self, resume_id: int, job_description_parsed_id: int
    ) -> Optional[Matches]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(Matches)
                .filter(
                    Matches.resume_id == resume_id,
                    Matches.job_description_parsed_id == job_description_parsed_id,
                )
                .first()
            )

    def get_all(self) -> List[Matches]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Matches).all()

    def get_all_by_resume_id(self, resume_id: int) -> List[Matches]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(Matches).filter(Matches.resume_id == resume_id).all()

    def get_all_by_job_parsed_id(self, job_description_parsed_id: int) -> List[Matches]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(Matches)
                .filter(Matches.job_description_parsed_id == job_description_parsed_id)
                .all()
            )

    def update(
        self,
        resume_id: int,
        job_description_parsed_id: int,
        model: Optional[MatchModel] = None,
        score: Optional[int] = None,
        llm_analysis: Optional[str] = None,
    ) -> Matches:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                match = (
                    session.query(Matches)
                    .filter(
                        Matches.resume_id == resume_id,
                        Matches.job_description_parsed_id == job_description_parsed_id,
                    )
                    .first()
                )
                if not match:
                    raise ValueError(
                        f"Match with resume_id {resume_id} and job_description_parsed_id {job_description_parsed_id} not found"
                    )
                if model is not None:
                    match.score = model.score  # type: ignore
                    match.llm_analysis = model.llm_analysis  # type: ignore
                else:
                    if score is not None:
                        match.score = score  # type: ignore
                    if llm_analysis is not None:
                        match.llm_analysis = llm_analysis  # type: ignore

                session.add(match)
                session.commit()

                return match

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating Match: {e}")
                raise e

    def delete(self, resume_id: int, job_description_parsed_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                match = (
                    session.query(Matches)
                    .filter(
                        Matches.resume_id == resume_id,
                        Matches.job_description_parsed_id == job_description_parsed_id,
                    )
                    .first()
                )
                if not match:
                    raise ValueError(
                        f"Match with resume_id {resume_id} and job_description_parsed_id {job_description_parsed_id} not found"
                    )
                session.delete(match)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting Match: {e}")
                raise e

            return True
