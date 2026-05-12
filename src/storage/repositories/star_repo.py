from datetime import date
from typing import List, Optional

from src.core.models import StarEntry as StarEntryModel
from src.core.models import StarMetadata as StarMetadataModel
from config.logging import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.mappers.skill_mapper import SkillMapper
from src.storage.mappers.star_mapper import StarEntryMapper, StarMetadataMapper
from src.storage.models import StarEntry, StarMetadata


class StarMetadataRepo:
    def __init__(self, isTest):
        self._log = get_logger("StarMetadataRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: StarMetadataModel) -> int:
        """Create or update a StarMetadata from a model.

        Checks by unique composite key: (user_id + type + title + subtitle).
        """
        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = StarMetadataMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self,
        id: int,
        user_id: int,
        type: str,
        title: str,
        subtitle: str,
        location: str,
        start_date: date,
        end_date: Optional[date] = None,
    ) -> int:
        """Create using individual fields (builds model internally)."""
        model = StarMetadataMapper.from_raw_fields(
            id=id,
            user_id=user_id,
            type=type,
            title=title,
            subtitle=subtitle,
            location=location,
            start_date=start_date,
            end_date=end_date,
        )
        return self.create_or_update(model)

    def get_by_id(self, star_metadata_id: int) -> Optional[StarMetadataModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(star_metadata_id)

        if not storage_model:
            return None

        return StarMetadataMapper.to_core_model(storage_model)

    def get_all_by_user(self, user_id: int) -> List[StarMetadataModel]:
        """Fetches all by user_id and converts to Core Model list."""
        with self.db.get_session() as session:
            storage_models = (
                session.query(StarMetadata)
                .filter(StarMetadata.user_id == user_id)
                .all()
            )

            return [StarMetadataMapper.to_core_model(model) for model in storage_models]

    def delete(self, star_metadata_id: int) -> bool:
        storage_model = self._retrieve(star_metadata_id)

        if not storage_model:
            self._log.debug(f"StarMetadata with id {star_metadata_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(self, core_model: StarMetadataModel) -> StarMetadata:

        storage_model = StarMetadataMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve(core_model.id)
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: StarMetadata) -> int:
        """Create a StarMetadata from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating StarMetadata: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve(self, star_metadata_id: int) -> Optional[StarMetadata]:
        with self.db.get_session() as session:
            return (
                session.query(StarMetadata)
                .filter(StarMetadata.id == star_metadata_id)
                .first()
            )

    def _retrieve_by_composite_key(
        self, user_id: int, type: str, title: str, subtitle: str
    ) -> Optional[StarMetadata]:
        with self.db.get_session() as session:
            return (
                session.query(StarMetadata)
                .filter(
                    StarMetadata.user_id == user_id,
                    StarMetadata.type == type,
                    StarMetadata.title == title,
                    StarMetadata.subtitle == subtitle,
                )
                .first()
            )

    def _update(
        self, storage_model: StarMetadata, core_model: StarMetadataModel
    ) -> int:
        storage_model.type = core_model.type
        storage_model.title = core_model.title
        storage_model.subtitle = core_model.subtitle
        storage_model.location = core_model.location
        storage_model.start_date = core_model.start_date
        storage_model.end_date = (
            core_model.end_date if core_model.end_date is not None else date.today()
        )

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating StarMetadata: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: StarMetadata) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting StarMetadata: {e}")
                raise e

        return True


class StarEntryRepo:
    def __init__(self, isTest):
        self._log = get_logger("StarEntryRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: StarEntryModel) -> int:
        """Create or update a StarEntry from a model.

        Checks by unique composite key: (metadata_id + title + situation + task + action + result).
        """
        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = StarEntryMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self,
        id: int,
        metadata_id: int,
        title: str,
        situation: str,
        task: str,
        action: str,
        result: str,
    ) -> int:
        """Create using individual fields (builds model internally)."""
        model = StarEntryMapper.from_raw_fields(
            id=id,
            metadata_id=metadata_id,
            title=title,
            situation=situation,
            task=task,
            action=action,
            result=result,
        )
        return self.create_or_update(model)

    def get_by_id(self, star_entry_id: int) -> Optional[StarEntryModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(star_entry_id)

        if not storage_model:
            return None

        return StarEntryMapper.to_core_model(storage_model)

    def get_all_by_metadata(self, metadata_id: int) -> List[StarEntryModel]:
        """Fetches all by metadata_id and converts to Core Model list."""
        with self.db.get_session() as session:
            storage_models = (
                session.query(StarEntry)
                .filter(StarEntry.metadata_id == metadata_id)
                .all()
            )

            return [StarEntryMapper.to_core_model(model) for model in storage_models]

    def delete(self, star_entry_id: int) -> bool:
        storage_model = self._retrieve(star_entry_id)

        if not storage_model:
            self._log.debug(f"StarEntry with id {star_entry_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(self, core_model: StarEntryModel) -> StarEntry:

        storage_model = StarEntryMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve(core_model.id)
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: StarEntry) -> int:
        """Create a StarEntry from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating StarEntry: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve(self, star_entry_id: int) -> Optional[StarEntry]:
        with self.db.get_session() as session:
            return (
                session.query(StarEntry).filter(StarEntry.id == star_entry_id).first()
            )

    def _retrieve_by_composite_key(
        self,
        metadata_id: int,
        title: str,
        situation: str,
        task: str,
        action: str,
        result: str,
    ) -> Optional[StarEntry]:
        with self.db.get_session() as session:
            return (
                session.query(StarEntry)
                .filter(
                    StarEntry.metadata_id == metadata_id,
                    StarEntry.title == title,
                    StarEntry.situation == situation,
                    StarEntry.task == task,
                    StarEntry.action == action,
                    StarEntry.result == result,
                )
                .first()
            )

    def _update(self, storage_model: StarEntry, core_model: StarEntryModel) -> int:
        storage_model.title = core_model.title
        storage_model.situation = core_model.situation
        storage_model.task = core_model.task
        storage_model.action = core_model.action
        storage_model.result = core_model.result
        storage_model.skills = [
            SkillMapper.to_storage_model(skill) for skill in core_model.skills
        ]

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating StarEntry: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: StarEntry) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting StarEntry: {e}")
                raise e

        return True
