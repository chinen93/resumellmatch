from typing import Optional

from src.logging_config import get_logger
from src.storage.repositories import LLMCacheRepo
from src.utils.hash import compute_hash


class LLMCacheManager:
    """Manages LLM response caching."""

    def __init__(self, cache_repo: LLMCacheRepo):
        self.cache_repo = cache_repo
        self._log = get_logger("LLMCacheManager")

    def get_cached(self, prompt_hash: str) -> Optional[str]:
        """Retrieve cached response if available."""
        try:
            cached = self.cache_repo.get_by_prompt_hash(prompt_hash)
            if cached:
                self._log.info("LLM cache hit for prompt")
                return str(cached.response_json)
        except Exception as e:
            self._log.warning(f"Cache retrieval failed: {e}")
        return None

    def save_cache(
        self, prompt_hash: str, prompt_text: str, response_json: str
    ) -> None:
        """Save response to cache."""
        response_hash = compute_hash(response_json)
        try:
            self.cache_repo.create_from_fields(
                prompt_hash=prompt_hash,
                prompt_text=prompt_text,
                response_hash=response_hash,
                response_json=response_json,
                llm_name="ollama",
            )
        except Exception as e:
            self._log.warning(f"Cache save failed: {e}")
