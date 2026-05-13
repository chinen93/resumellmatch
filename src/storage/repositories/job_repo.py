"""Repositories for job description persistence.

This module contains repositories for storing and retrieving job descriptions
and parsed job metadata from the database.
"""

from typing import List, Optional

from config.logging import get_logger
from src.core.models import JobDescription as JobDescriptionModel
from src.core.models import JobDescriptionParsed as JobDescriptionParsedModel
from src.storage.connection import DatabaseConnection
from src.storage.mappers.job_mapper import (
    JobDescriptionMapper,
    JobDescriptionParsedMapper,
)
from src.storage.models import JobDescription, JobDescriptionParsed


class JobDescriptionRepo:
    """Repository for CRUD operations on JobDescription entities."""

    def __init__(self, isTest):
        self._log = get_logger("JobDescRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: JobDescriptionModel) -> int:
        """Create or update a JobDescription from a model"""

        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = JobDescriptionMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self, id: Optional[int], url: str, title: str, raw_text: str
    ) -> int:
        """Create using individual fields (builds model internally)."""
        model = JobDescriptionMapper.from_raw_fields(id, url, title, raw_text)
        return self.create_or_update(model)

    def get_by_id(self, job_id: int) -> Optional[JobDescriptionModel]:
        """Fetches a record and converts it immediately to the Core Model."""

        storage_model = self._retrieve(job_id)

        if not storage_model:
            return None

        return JobDescriptionMapper.to_core_model(storage_model)

    def get_all(self) -> List[JobDescriptionModel]:
        """Fetches all records and converts them to the Core Model list."""

        with self.db.get_session() as session:
            storage_models = session.query(JobDescription).all()

            return [
                JobDescriptionMapper.to_core_model(model) for model in storage_models
            ]

    def delete(self, job_id: int) -> bool:
        storage_model = self._retrieve(job_id)

        if not storage_model:
            self._log.debug(f"JobDescription with id {job_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(self, core_model: JobDescriptionModel) -> JobDescription:

        storage_model = JobDescriptionMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve(core_model.id)
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: JobDescription) -> int:
        """Create a JobDescription from a model"""

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating JobDescription: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve(self, job_id: int) -> Optional[JobDescription]:
        with self.db.get_session() as session:
            return (
                session.query(JobDescription)
                .filter(JobDescription.id == job_id)
                .first()
            )

    def _update(
        self, storage_model: JobDescription, core_model: JobDescriptionModel
    ) -> int:
        storage_model.url = core_model.url
        storage_model.title = core_model.title
        storage_model.raw_text = core_model.raw_text

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating JobDescription: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: JobDescription) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting JobDescription: {e}")
                raise e

        return True


class JobDescriptionParsedRepo:
    """Repository for CRUD operations on JobDescriptionParsed entities."""

    def __init__(self, isTest):
        self._log = get_logger("JobDescParsedRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: JobDescriptionParsedModel) -> int:
        """Create or update a JobDescriptionParsed from a model.

        Checks by job_description_id first, then by input_hash if available.
        """

        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = JobDescriptionParsedMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self,
        id: Optional[int],
        job_description_id: int,
        summary: str,
        required_skills: str,
        prefered_skills: str,
        keywords: str,
        input_hash: str | None = None,
        full_response: str | None = None,
    ) -> int:
        """Create using individual fields (builds model internally)."""
        model = JobDescriptionParsedMapper.from_raw_fields(
            id=id,
            job_description_id=job_description_id,
            summary=summary,
            required_skills=required_skills,
            prefered_skills=prefered_skills,
            keywords=keywords,
            input_hash=input_hash,
            full_response=full_response,
        )
        return self.create_or_update(model)

    def get_by_id(self, parsed_id: int) -> Optional[JobDescriptionParsedModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve_by_id(parsed_id)

        if not storage_model:
            return None

        return JobDescriptionParsedMapper.to_core_model(storage_model)

    def get_by_job_id(self, job_id: int) -> Optional[JobDescriptionParsedModel]:
        """Fetches by job_description_id and converts to Core Model."""
        storage_model = self._retrieve_by_job_id(job_id)

        if not storage_model:
            return None

        return JobDescriptionParsedMapper.to_core_model(storage_model)

    def get_by_input_hash(self, input_hash: str) -> Optional[JobDescriptionParsedModel]:
        """Fetches by input_hash and converts to Core Model."""
        storage_model = self._retrieve_by_input_hash(input_hash)

        if not storage_model:
            return None

        return JobDescriptionParsedMapper.to_core_model(storage_model)

    def get_all(self) -> List[JobDescriptionParsedModel]:
        """Fetches all records and converts them to the Core Model list."""
        with self.db.get_session() as session:
            storage_models = session.query(JobDescriptionParsed).all()

            return [
                JobDescriptionParsedMapper.to_core_model(model)
                for model in storage_models
            ]

    def delete(self, parsed_id: int) -> bool:
        storage_model = self._retrieve_by_id(parsed_id)

        if not storage_model:
            self._log.debug(f"JobDescriptionParsed with id {parsed_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(
        self, core_model: JobDescriptionParsedModel
    ) -> JobDescriptionParsed:

        storage_model = JobDescriptionParsedMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve_by_id(core_model.id)
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: JobDescriptionParsed) -> int:
        """Create a JobDescriptionParsed from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating JobDescriptionParsed: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve_by_id(self, parsed_id: int) -> Optional[JobDescriptionParsed]:
        with self.db.get_session() as session:
            return (
                session.query(JobDescriptionParsed)
                .filter(JobDescriptionParsed.id == parsed_id)
                .first()
            )

    def _retrieve_by_job_id(self, job_id: int) -> Optional[JobDescriptionParsed]:
        with self.db.get_session() as session:
            return (
                session.query(JobDescriptionParsed)
                .filter(JobDescriptionParsed.job_description_id == job_id)
                .first()
            )

    def _retrieve_by_input_hash(
        self, input_hash: str
    ) -> Optional[JobDescriptionParsed]:
        with self.db.get_session() as session:
            return (
                session.query(JobDescriptionParsed)
                .filter(JobDescriptionParsed.input_hash == input_hash)
                .first()
            )

    def _update(
        self, storage_model: JobDescriptionParsed, core_model: JobDescriptionParsedModel
    ) -> int:
        storage_model.summary = core_model.summary
        storage_model.required_skills = core_model.required_skills
        storage_model.prefered_skills = core_model.prefered_skills
        storage_model.keywords = core_model.keywords
        storage_model.full_response = (
            core_model.full_response if core_model.full_response is not None else ""
        )
        storage_model.input_hash = (
            core_model.input_hash if core_model.input_hash is not None else ""
        )

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating JobDescriptionParsed: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: JobDescriptionParsed) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting JobDescriptionParsed: {e}")
                raise e

        return True
