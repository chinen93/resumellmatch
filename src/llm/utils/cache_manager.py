"""LLM response caching manager.

Manages retrieval and storage of cached LLM responses to improve performance
and reduce redundant LLM calls.
"""

from typing import Optional

from config.logging import get_logger
from src.storage.repositories import LLMCacheRepo
from src.utils.hash import compute_hash


class LLMCacheManager:
    """Manages LLM response caching via repository.

    Handles checking the cache for existing responses and storing new responses.
    Uses prompt hash as the cache key.

    Attributes:
        cache_repo: Repository for LLMCache entities.
        _log: Logger instance.
    """

    def __init__(self, cache_repo: LLMCacheRepo):
        self.cache_repo = cache_repo
        self._log = get_logger("LLMCacheManager")

    def get_cached(self, prompt_hash: str) -> Optional[str]:
        """Retrieve cached response for a given prompt hash.

        Args:
            prompt_hash: SHA256 hash of the prompt text.

        Returns:
            The cached response as JSON or None if not found.
        """
        try:
            cached = self.cache_repo.get_by_prompt_hash(prompt_hash)
            if cached:
                self._log.debug("LLM cache hit for prompt")
                return str(cached.response_json)
        except Exception as e:
            self._log.warning(f"Cache retrieval failed: {e}")
        return None

    def save_cache(
        self, prompt_hash: str, prompt_text: str, response_json: str
    ) -> None:
        """Save a LLM response to the cache.

        Args:
            prompt_hash: SHA256 hash of the prompt text.
            prompt_text: The original prompt text.
            response_json: The LLM response as JSON.
        """
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
