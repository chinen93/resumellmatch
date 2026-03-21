from typing import List, Optional

from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import JobDescription, JobDescriptionParsed

_log = get_logger("JobRepo")


class JobDescriptionRepo:
    def __init__(self, isTest):
        self.db = DatabaseConnection(isTest)

    def create(self, url: str, title: str, raw_text: str) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                job_description = JobDescription(
                    url=url, title=title, raw_text=raw_text
                )
                session.add(job_description)
                session.commit()

                result = int(job_description.id)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error(f"Error when creating JobDescription: {e}")
                raise e

        return result

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
                _log.error(f"Error when updating JobDescription: {e}")
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
                _log.error(f"Error when deleting JobDescription: {e}")
                raise e

            return True


class JobDescriptionParsedRepo:
    def __init__(self, isTest):
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        job_description_id: int,
        summary: str,
        required_skills: str,
        prefered_skills: str,
        keywords: str,
    ) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                job_parsed = JobDescriptionParsed(
                    job_description_id=job_description_id,
                    summary=summary,
                    required_skills=required_skills,
                    prefered_skills=prefered_skills,
                    keywords=keywords,
                )
                session.add(job_parsed)
                session.commit()

                result = int(job_parsed.id)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error(f"Error when creating JobDescriptionParsed: {e}")
                raise e

        return result

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
                _log.error(f"Error when updating JobDescriptionParsed: {e}")
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
                _log.error(f"Error when deleting JobDescriptionParsed: {e}")
                raise e

            return True
