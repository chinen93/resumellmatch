from src.core.models import LLMCache as LLMCacheModel
from src.storage.models import LLMCache


class LLMCacheMapper:
    @staticmethod
    def to_core_model(storage_model: LLMCache) -> LLMCacheModel:
        return LLMCacheModel(
            id=storage_model.id,
            prompt_hash=storage_model.prompt_hash,
            prompt_text=storage_model.prompt_text,
            response_hash=storage_model.response_hash,
            response_json=storage_model.response_json,
            llm_name=storage_model.llm_name,
            created_at=storage_model.created_at,
        )

    @staticmethod
    def to_storage_model(core_model: LLMCacheModel) -> LLMCache:
        return LLMCache(
            id=core_model.id,
            prompt_hash=core_model.prompt_hash,
            prompt_text=core_model.prompt_text,
            response_hash=core_model.response_hash,
            response_json=core_model.response_json,
            llm_name=core_model.llm_name,
            created_at=core_model.created_at,
        )

    @staticmethod
    def from_raw_fields(
        prompt_hash: str,
        prompt_text: str,
        response_hash: str,
        response_json: str,
        llm_name: str,
    ) -> LLMCacheModel:
        """Builds the core model directly from raw input fields."""
        return LLMCacheModel(
            prompt_hash=prompt_hash,
            prompt_text=prompt_text,
            response_hash=response_hash,
            response_json=response_json,
            llm_name=llm_name,
        )
