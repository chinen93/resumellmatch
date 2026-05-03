from src.core.models import Skill as SkillModel
from src.storage.models import Skill


class SkillMapper:
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
    def from_raw_fields(name: str) -> SkillModel:
        return SkillModel(name=name)
