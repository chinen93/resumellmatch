from datetime import date
from typing import List, Optional

from src.storage.connection import DatabaseConnection
from src.storage.models import StarMetadata

db = DatabaseConnection()


class StarMetadataRepo:
    @classmethod
    def create(
        cls,
        user_id: int,
        type: str,
        title: str,
        subtitle: str,
        location: str,
        start_date: date,
        end_date: date,
    ) -> int:
        result = None

        with db.get_session() as session:
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
                print("Error when creating StarMetadata:", star_metadata)
                raise e

        return result

    @classmethod
    def get_by_id(cls, star_metadata_id: int) -> Optional[StarMetadata]:
        with db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(StarMetadata)
                .filter(StarMetadata.id == star_metadata_id)
                .first()
            )

    @classmethod
    def get_all(cls, user_id: int) -> List[StarMetadata]:
        with db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(StarMetadata)
                .filter(StarMetadata.user_id == user_id)
                .all()
            )

    @classmethod
    def update(
        cls,
        star_metadata_id: int,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        location: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> StarMetadata:
        with db.get_session() as session:
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
                print("Error when updating StarMetadata:", star_metadata)
                raise e

    @classmethod
    def delete(cls, star_metadata_id: int) -> bool:
        with db.get_session() as session:
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
                print("Error when deleting StartMetadata:", star_metadata)
                raise e

            return True
