from src.core.models import JobDescription as JobDescriptionModel
from src.core.models import JobDescriptionParsed as JobDescriptionParsedModel
from src.storage.models import JobDescription, JobDescriptionParsed


class JobDescriptionMapper:
    """
    Handles all conversion logic between different representations
    of a JobDescription:
    1. Storage Model (DB ORM object)
    2. Core Model (Application's Domain Object)
    3. Raw Fields (Primitives)
    """

    @staticmethod
    def to_core_model(storage_model: JobDescription) -> JobDescriptionModel:
        """Converts a storage JobDescription (DB object) to the core application model."""
        return JobDescriptionModel(
            id=storage_model.id,
            url=storage_model.url,
            title=storage_model.title,
            raw_text=storage_model.raw_text,
            created_at=storage_model.created_at,
        )

    @staticmethod
    def to_storage_model(core_model: JobDescriptionModel) -> JobDescription:
        """Converts a core JobDescription model to a storage JobDescription (DB object)."""
        return JobDescription(
            id=core_model.id,  # ID logic remains the same
            url=core_model.url,
            title=core_model.title,
            raw_text=core_model.raw_text,
            created_at=core_model.created_at,
        )

    @staticmethod
    def from_raw_fields(url: str, title: str, raw_text: str) -> JobDescriptionModel:
        """Builds the core model directly from raw input fields."""
        return JobDescriptionModel(url=url, title=title, raw_text=raw_text)


class JobDescriptionParsedMapper:
    @staticmethod
    def to_core_model(storage_model: JobDescriptionParsed) -> JobDescriptionParsedModel:
        return JobDescriptionParsedModel(
            id=storage_model.id,
            job_description_id=storage_model.job_description_id,
            input_hash=storage_model.input_hash,
            full_response=storage_model.full_response,
            summary=storage_model.summary,
            required_skills=storage_model.required_skills,
            prefered_skills=storage_model.prefered_skills,
            keywords=storage_model.keywords,
        )

    @staticmethod
    def to_storage_model(core_model: JobDescriptionParsedModel) -> JobDescriptionParsed:
        return JobDescriptionParsed(
            id=core_model.id,
            job_description_id=core_model.job_description_id,
            input_hash=core_model.input_hash,
            full_response=core_model.full_response,
            summary=core_model.summary,
            required_skills=core_model.required_skills,
            prefered_skills=core_model.prefered_skills,
            keywords=core_model.keywords,
        )

    @staticmethod
    def from_raw_fields(
        job_description_id: int,
        summary: str,
        required_skills: str,
        prefered_skills: str,
        keywords: str,
        input_hash: str | None = None,
        full_response: str | None = None,
    ) -> JobDescriptionParsedModel:
        """Builds the core model directly from raw input fields."""
        return JobDescriptionParsedModel(
            job_description_id=job_description_id,
            input_hash=input_hash,
            full_response=full_response,
            summary=summary,
            required_skills=required_skills,
            prefered_skills=prefered_skills,
            keywords=keywords,
        )
