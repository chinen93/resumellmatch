"""Mapper for skill storage and core models.

This module handles conversion between skill ORM storage models and the
application's core Skill domain model.
"""

from src.core.models import Skill as SkillModel
from src.storage.models import Skill


class SkillMapper:
    """Mapper between storage Skill and core Skill models."""

    @staticmethod
    def to_core_model(storage_model: Skill) -> SkillModel:
        return SkillModel(
            id=storage_model.id,
            name=storage_model.name,
            created_at=storage_model.created_at,
        )

    @staticmethod
    def to_storage_model(core_model: SkillModel) -> Skill:
        return Skill(
            id=core_model.id,
            name=core_model.name,
            created_at=core_model.created_at,
        )

    @staticmethod
    def from_raw_fields(id: int, name: str) -> SkillModel:
        return SkillModel(id=id, name=name)
