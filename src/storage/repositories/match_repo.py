"""Repository for match persistence.

This module provides operations to store and retrieve resume-job match records
from the database.
"""

from typing import List, Optional

from config.logging import get_logger
from src.core.models import Match as MatchModel
from src.storage.connection import DatabaseConnection
from src.storage.mappers.match_mapper import MatchMapper
from src.storage.models import Matches


class MatchRepo:
    """Repository for CRUD operations on Match entities."""

    def __init__(self, isTest):
        self._log = get_logger("MatchRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: MatchModel) -> bool:
        """Create or update a Match from a model (composite key: resume_id + job_description_parsed_id)."""

        if core_model.resume_id is None or core_model.job_description_parsed_id is None:
            return False

        storage_model = self._retrieve(
            core_model.resume_id, core_model.job_description_parsed_id
        )

        if storage_model is not None:
            self._update(storage_model, core_model)
            return True
        else:
            storage_model = MatchMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self,
        resume_id: int,
        job_description_parsed_id: int,
        score: int,
        llm_analysis: str,
    ) -> bool:
        """Create using individual fields (builds model internally)."""
        model = MatchMapper.from_raw_fields(
            resume_id, job_description_parsed_id, score, llm_analysis
        )
        return self.create_or_update(model)

    def get_by_ids(
        self, resume_id: int, job_description_parsed_id: int
    ) -> Optional[MatchModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(resume_id, job_description_parsed_id)

        if not storage_model:
            return None

        return MatchMapper.to_core_model(storage_model)

    def get_all(self) -> List[MatchModel]:
        """Fetches all records and converts them to the Core Model list."""
        with self.db.get_session() as session:
            storage_models = session.query(Matches).all()

            return [MatchMapper.to_core_model(model) for model in storage_models]

    def get_all_by_resume_id(self, resume_id: int) -> List[MatchModel]:
        """Fetches all by resume_id and converts to Core Model list."""
        with self.db.get_session() as session:
            storage_models = (
                session.query(Matches).filter(Matches.resume_id == resume_id).all()
            )

            return [MatchMapper.to_core_model(model) for model in storage_models]

    def get_all_by_job_parsed_id(
        self, job_description_parsed_id: int
    ) -> List[MatchModel]:
        """Fetches all by job_description_parsed_id and converts to Core Model list."""
        with self.db.get_session() as session:
            storage_models = (
                session.query(Matches)
                .filter(Matches.job_description_parsed_id == job_description_parsed_id)
                .all()
            )

            return [MatchMapper.to_core_model(model) for model in storage_models]

    def delete(self, resume_id: int, job_description_parsed_id: int) -> bool:
        storage_model = self._retrieve(resume_id, job_description_parsed_id)

        if not storage_model:
            self._log.debug(
                f"Match with resume_id {resume_id} and job_parsed_id {job_description_parsed_id} not found"
            )
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _create(self, storage_model: Matches) -> bool:
        """Create a Match from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()
                return True

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating Match: {e}")
                raise e

    def _retrieve(
        self, resume_id: int, job_description_parsed_id: int
    ) -> Optional[Matches]:
        with self.db.get_session() as session:
            return (
                session.query(Matches)
                .filter(
                    Matches.resume_id == resume_id,
                    Matches.job_description_parsed_id == job_description_parsed_id,
                )
                .first()
            )

    def _update(self, storage_model: Matches, core_model: MatchModel) -> None:
        storage_model.score = core_model.score
        storage_model.llm_analysis = core_model.llm_analysis

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating Match: {e}")
                raise e

    def _delete(self, storage_model: Matches) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting Match: {e}")
                raise e

        return True
