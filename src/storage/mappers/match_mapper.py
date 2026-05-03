from src.core.models import Match as MatchModel
from src.storage.models import Matches as MatchStorage


class MatchMapper:
    @staticmethod
    def to_core_model(storage_model: MatchStorage) -> MatchModel:
        return MatchModel(
            resume_id=storage_model.resume_id,
            job_description_parsed_id=storage_model.job_description_parsed_id,
            score=storage_model.score,
            llm_analysis=storage_model.llm_analysis,
        )

    @staticmethod
    def to_storage_model(core_model: MatchModel) -> MatchStorage:
        return MatchStorage(
            resume_id=core_model.resume_id,
            job_description_parsed_id=core_model.job_description_parsed_id,
            score=core_model.score,
            llm_analysis=core_model.llm_analysis,
        )

    @staticmethod
    def from_raw_fields(
        resume_id: int, job_description_parsed_id: int, score: int, llm_analysis: str
    ) -> MatchModel:
        """Builds the core model directly from raw input fields."""
        return MatchModel(
            resume_id=resume_id,
            job_description_parsed_id=job_description_parsed_id,
            score=score,
            llm_analysis=llm_analysis,
        )
