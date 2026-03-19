from datetime import date
from typing import List, Optional

from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import StarEntry, StarMetadata
from src.storage.repositories.skill_repo import SkillRepo

_log = get_logger("StarRepo")


class StarMetadataRepo:

    def __init__(self, isTest):
        self.db = DatabaseConnection(isTest)

    def create(
        self,
        user_id: int,
        type: str,
        title: str,
        subtitle: str,
        location: str,
        start_date: date,
        end_date: date,
    ) -> int:
        result = None

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                star_metadata = StarMetadata(
                    user_id=user_id,
                    type=type,
                    title=title,
                    subtitle=subtitle,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                )
                session.add(star_metadata)
                session.commit()

                result = int(star_metadata.id)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error("Error when creating StarMetadata:", star_metadata)
                raise e

        return result

    def get_by_id(self, star_metadata_id: int) -> Optional[StarMetadata]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(StarMetadata)
                .filter(StarMetadata.id == star_metadata_id)
                .first()
            )

    def get_all(self, user_id: int) -> List[StarMetadata]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(StarMetadata)
                .filter(StarMetadata.user_id == user_id)
                .all()
            )

    def update(
        self,
        star_metadata_id: int,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        location: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> StarMetadata:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                star_metadata = (
                    session.query(StarMetadata)
                    .filter(StarMetadata.id == star_metadata_id)
                    .first()
                )
                if not star_metadata:
                    raise ValueError(
                        f"StarMetadata with id {star_metadata_id} not found"
                    )
                if title is not None:
                    star_metadata.title = title  # type: ignore
                if subtitle is not None:
                    star_metadata.subtitle = subtitle  # type: ignore
                if location is not None:
                    star_metadata.location = location  # type: ignore
                if start_date is not None:
                    star_metadata.start_date = start_date  # type: ignore
                if end_date is not None:
                    star_metadata.end_date = end_date  # type: ignore

                session.add(star_metadata)
                session.commit()

                return star_metadata

            except Exception as e:
                session.rollback()
                _log.error("Error when updating StarMetadata:", star_metadata)
                raise e

    def delete(self, star_metadata_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                star_metadata = (
                    session.query(StarMetadata)
                    .filter(StarMetadata.id == star_metadata_id)
                    .first()
                )
                if not star_metadata:
                    raise ValueError(
                        f"StarMetadata with id {star_metadata_id} not found"
                    )
                session.delete(star_metadata)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error("Error when deleting StartMetadata:", star_metadata)
                raise e

            return True


class StarEntryRepo:

    def __init__(self, isTest):
        self.db = DatabaseConnection(isTest)
        self.skill_repo = SkillRepo(isTest)

    def create(
        self,
        metadata_id: int,
        title: str,
        situation: str,
        task: str,
        action: str,
        result: str,
        skills: List[int] = [],
    ) -> int:
        ret = None

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                star_entry = StarEntry(
                    metadata_id=metadata_id,
                    title=title,
                    situation=situation,
                    task=task,
                    action=action,
                    result=result,
                )
                session.add(star_entry)
                session.commit()

                if skills != []:
                    for skill_id in skills:
                        skill = self.skill_repo.get_by_id(skill_id)
                        star_entry.skills.append(skill)
                    session.commit()

                ret = int(star_entry.id)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error("Error when creating StarEntry:", star_entry)
                raise e

        return ret

    def get_by_id(self, star_entry_id: int) -> Optional[StarEntry]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(StarEntry).filter(StarEntry.id == star_entry_id).first()
            )

    def get_all(self, metadata_id: int) -> List[StarEntry]:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(StarEntry)
                .filter(StarEntry.metadata_id == metadata_id)
                .all()
            )

    def update(
        self,
        star_entry_id: int,
        title: Optional[str] = None,
        situation: Optional[str] = None,
        task: Optional[str] = None,
        action: Optional[str] = None,
        result: Optional[str] = None,
    ) -> StarEntry:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                star_entry = (
                    session.query(StarEntry)
                    .filter(StarEntry.id == star_entry_id)
                    .first()
                )
                if not star_entry:
                    raise ValueError(f"StarEntry with id {star_entry_id} not found")
                if title is not None:
                    star_entry.title = title  # type: ignore
                if situation is not None:
                    star_entry.situation = situation  # type: ignore
                if task is not None:
                    star_entry.task = task  # type: ignore
                if action is not None:
                    star_entry.action = action  # type: ignore
                if result is not None:
                    star_entry.result = result  # type: ignore

                session.add(star_entry)
                session.commit()

                return star_entry

            except Exception as e:
                session.rollback()
                _log.error("Error when updating StarEntry:", star_entry)
                raise e

    def delete(self, star_entry_id: int) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                star_entry = (
                    session.query(StarEntry)
                    .filter(StarEntry.id == star_entry_id)
                    .first()
                )
                if not star_entry:
                    raise ValueError(f"StarEntry with id {star_entry_id} not found")
                session.delete(star_entry)
                session.commit()
            except Exception as e:
                session.rollback()
                _log.error("Error when deleting StarEntry:", star_entry)
                raise e

            return True
