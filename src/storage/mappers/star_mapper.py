"""Mapper for STAR storage and core models.

This module converts STAR metadata and STAR entry records between storage ORM
models and domain-level models used by the application.
"""

from datetime import date
from typing import Optional

from src.core.models import StarEntry as StarEntryModel
from src.core.models import StarMetadata as StarMetadataModel
from src.storage.mappers.skill_mapper import SkillMapper
from src.storage.models import StarEntry, StarMetadata


class StarMetadataMapper:
    """Mapper between storage StarMetadata and core StarMetadata models."""

    @staticmethod
    def to_core_model(storage_model: StarMetadata) -> StarMetadataModel:
        return StarMetadataModel(
            id=storage_model.id,
            user_id=storage_model.user_id,
            type=storage_model.type,
            title=storage_model.title,
            subtitle=storage_model.subtitle,
            location=storage_model.location,
            start_date=storage_model.start_date,
            end_date=storage_model.end_date,
            created_at=storage_model.created_at,
            entries=[
                StarEntryMapper.to_core_model(entry) for entry in storage_model.entries
            ],
        )

    @staticmethod
    def to_storage_model(core_model: StarMetadataModel) -> StarMetadata:
        return StarMetadata(
            id=core_model.id,
            user_id=core_model.user_id,
            type=core_model.type,
            title=core_model.title,
            subtitle=core_model.subtitle,
            location=core_model.location,
            start_date=core_model.start_date,
            end_date=core_model.end_date,
            created_at=core_model.created_at,
            entries=[
                StarEntryMapper.to_storage_model(entry) for entry in core_model.entries
            ],
        )

    @staticmethod
    def from_raw_fields(
        id: int,
        user_id: int,
        type: str,
        title: str,
        subtitle: str,
        location: str,
        start_date: date,
        end_date: Optional[date] = None,
    ) -> StarMetadataModel:
        """Builds the core model directly from raw input fields."""
        return StarMetadataModel(
            id=id,
            user_id=user_id,
            type=type,
            title=title,
            subtitle=subtitle,
            location=location,
            start_date=start_date,
            end_date=end_date,
        )


class StarEntryMapper:
    """Mapper between storage StarEntry and core StarEntry models."""

    @staticmethod
    def to_core_model(storage_model: StarEntry) -> StarEntryModel:
        return StarEntryModel(
            id=storage_model.id,
            metadata_id=storage_model.metadata_id,
            title=storage_model.title,
            situation=storage_model.situation,
            task=storage_model.task,
            action=storage_model.action,
            result=storage_model.result,
            skills=[SkillMapper.to_core_model(skill) for skill in storage_model.skills],
            updated_at=storage_model.updated_at,
            created_at=storage_model.created_at,
        )

    @staticmethod
    def to_storage_model(core_model: StarEntryModel) -> StarEntry:
        return StarEntry(
            id=core_model.id,
            metadata_id=core_model.metadata_id,
            title=core_model.title,
            situation=core_model.situation,
            task=core_model.task,
            action=core_model.action,
            result=core_model.result,
            skills=[SkillMapper.to_storage_model(skill) for skill in core_model.skills],
            updated_at=core_model.updated_at,
            created_at=core_model.created_at,
        )

    @staticmethod
    def from_raw_fields(
        id: int,
        metadata_id: int,
        title: str,
        situation: str,
        task: str,
        action: str,
        result: str,
    ) -> StarEntryModel:
        """Builds the core model directly from raw input fields."""
        return StarEntryModel(
            id=id,
            metadata_id=metadata_id,
            title=title,
            situation=situation,
            task=task,
            action=action,
            result=result,
        )
