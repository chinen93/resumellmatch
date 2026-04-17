from typing import List, Optional

from src.core.models import JobDescription as JobDescriptionModel
from src.core.models import JobDescriptionParsed as JobDescriptionParsedModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import JobDescription, JobDescriptionParsed


class JobDescriptionRepo:
    def __init__(self, isTest):
        self._log = get_logger("JobDescRepo")
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        model: Optional[JobDescriptionModel] = None,
        url: Optional[str] = None,
        title: Optional[str] = None,
        raw_text: Optional[str] = None,
    ) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                if model is None:
                    model = JobDescriptionModel(
                        url=url or "", title=title or "", raw_text=raw_text or ""
                    )

                job_description = JobDescription(
                    url=model.url, title=model.title, raw_text=model.raw_text
                )
                session.add(job_description)
                session.commit()

                result = int(job_description.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating JobDescription: {e}")
                raise e

        return result

    def create_from_model(self, model: JobDescriptionModel) -> int:
        """Create using a `core.models.JobDescription` instance."""
        return self.create(model=model)

    def create_from_fields(self, url: str, title: str, raw_text: str) -> int:
        """Create using individual fields (legacy style)."""
        return self.create(url=url, title=title, raw_text=raw_text)

    def get_by_id(self, job_id: int) -> Optional[JobDescription]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(JobDescription)
                .filter(JobDescription.id == job_id)
                .first()
            )

    def get_all(self) -> List[JobDescription]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(JobDescription).all()

    def update(
        self,
        job_id: int,
        url: Optional[str] = None,
        title: Optional[str] = None,
        raw_text: Optional[str] = None,
    ) -> JobDescription:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                job_description = (
                    session.query(JobDescription)
                    .filter(JobDescription.id == job_id)
                    .first()
                )
                if not job_description:
                    raise ValueError(f"JobDescription with id {job_id} not found")
                if url is not None:
                    job_description.url = url  # type: ignore
                if title is not None:
                    job_description.title = title  # type: ignore
                if raw_text is not None:
                    job_description.raw_text = raw_text  # type: ignore

                session.add(job_description)
                session.commit()

                return job_description

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating JobDescription: {e}")
                raise e

    def delete(self, job_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                job_description = (
                    session.query(JobDescription)
                    .filter(JobDescription.id == job_id)
                    .first()
                )
                if not job_description:
                    raise ValueError(f"JobDescription with id {job_id} not found")
                session.delete(job_description)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting JobDescription: {e}")
                raise e

            return True


class JobDescriptionParsedRepo:
    def __init__(self, isTest):
        self._log = get_logger("JobDescParsedRepo")
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        model: Optional[JobDescriptionParsedModel] = None,
        job_description_id: Optional[int] = None,
        summary: Optional[str] = None,
        required_skills: Optional[str] = None,
        prefered_skills: Optional[str] = None,
        keywords: Optional[str] = None,
        input_hash: str | None = None,
        full_response: str | None = None,
    ) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                if model is None:
                    model = JobDescriptionParsedModel(
                        job_description_id=job_description_id,
                        input_hash=input_hash,
                        full_response=full_response,
                        summary=summary or "",
                        required_skills=required_skills or "",
                        prefered_skills=prefered_skills or "",
                        keywords=keywords or "",
                    )

                job_parsed = JobDescriptionParsed(
                    job_description_id=model.job_description_id,
                    input_hash=model.input_hash,
                    full_response=model.full_response,
                    summary=model.summary,
                    required_skills=model.required_skills,
                    prefered_skills=model.prefered_skills,
                    keywords=model.keywords,
                )
                session.add(job_parsed)
                session.commit()

                result = int(job_parsed.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating JobDescriptionParsed: {e}")
                raise e

        return result

    def create_parsed_from_model(self, model: JobDescriptionParsedModel) -> int:
        """Create parsed JD using a `core.models.JobDescriptionParsed` instance."""
        return self.create(model=model)

    def create_parsed_from_fields(
        self,
        job_description_id: int,
        summary: str,
        required_skills: str,
        prefered_skills: str,
        keywords: str,
        input_hash: str | None = None,
        full_response: str | None = None,
    ) -> int:
        """Create parsed JD using individual fields (legacy style)."""
        return self.create(
            job_description_id=job_description_id,
            summary=summary,
            required_skills=required_skills,
            prefered_skills=prefered_skills,
            keywords=keywords,
            input_hash=input_hash,
            full_response=full_response,
        )

    def get_by_id(self, parsed_id: int) -> Optional[JobDescriptionParsed]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(JobDescriptionParsed)
                .filter(JobDescriptionParsed.id == parsed_id)
                .first()
            )

    def get_by_job_id(self, job_id: int) -> Optional[JobDescriptionParsed]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(JobDescriptionParsed)
                .filter(JobDescriptionParsed.job_description_id == job_id)
                .first()
            )

    def get_by_input_hash(self, input_hash: str) -> Optional[JobDescriptionParsed]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(JobDescriptionParsed)
                .filter(JobDescriptionParsed.input_hash == input_hash)
                .first()
            )

    def get_all(self) -> List[JobDescriptionParsed]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return session.query(JobDescriptionParsed).all()

    def update(
        self,
        parsed_id: int,
        summary: Optional[str] = None,
        required_skills: Optional[str] = None,
        prefered_skills: Optional[str] = None,
        keywords: Optional[str] = None,
    ) -> JobDescriptionParsed:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                job_parsed = (
                    session.query(JobDescriptionParsed)
                    .filter(JobDescriptionParsed.id == parsed_id)
                    .first()
                )
                if not job_parsed:
                    raise ValueError(
                        f"JobDescriptionParsed with id {parsed_id} not found"
                    )
                if summary is not None:
                    job_parsed.summary = summary  # type: ignore
                if required_skills is not None:
                    job_parsed.required_skills = required_skills  # type: ignore
                if prefered_skills is not None:
                    job_parsed.prefered_skills = prefered_skills  # type: ignore
                if keywords is not None:
                    job_parsed.keywords = keywords  # type: ignore

                session.add(job_parsed)
                session.commit()

                return job_parsed

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating JobDescriptionParsed: {e}")
                raise e

    def delete(self, parsed_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                job_parsed = (
                    session.query(JobDescriptionParsed)
                    .filter(JobDescriptionParsed.id == parsed_id)
                    .first()
                )
                if not job_parsed:
                    raise ValueError(
                        f"JobDescriptionParsed with id {parsed_id} not found"
                    )
                session.delete(job_parsed)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting JobDescriptionParsed: {e}")
                raise e

            return True
