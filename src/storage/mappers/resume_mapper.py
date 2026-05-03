from src.core.models import Resume as ResumeModel
from src.storage.models import Resume


class ResumeMapper:
    @staticmethod
    def to_core_model(storage_model: Resume) -> ResumeModel:
        return ResumeModel(
            id=storage_model.id,
            user_id=storage_model.user_id,
            raw_text=storage_model.raw_text,
            created_at=storage_model.created_at,
        )

    @staticmethod
    def to_storage_model(core_model: ResumeModel) -> Resume:
        return Resume(
            id=core_model.id,
            user_id=core_model.user_id,
            raw_text=core_model.raw_text,
            created_at=core_model.created_at,
        )

    @staticmethod
    def from_raw_fields(user_id: int, raw_text: str) -> ResumeModel:
        """Builds the core model directly from raw input fields."""
        return ResumeModel(user_id=user_id, raw_text=raw_text)
