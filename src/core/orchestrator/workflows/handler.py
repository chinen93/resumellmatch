"""Handler for LLM services orchestration.

This module provides the Handler class that acts as a facade for initializing
and coordinating LLM-related services including caching, client connections,
and prompt management.
"""

from src.llm.client import LLMCacheManager, LLMPromptService, OllamaLocalClient
from src.storage.repositories import LLMCacheRepo


class Handler:
    """Orchestrates LLM client and processing services.

    Acts as a facade providing unified access to LLM capabilities and prompt
    services for various processing workflows.

    Attributes:
        _log: Logger instance for this handler.
        llm_client: Ollama LLM client for text generation.
        prompt_service: Service for prompt-based LLM workflows with caching.

    Args:
        isTest: If True, uses test database; if False, uses production database.
    """

    def __init__(self, isTest: bool = False):
        cache_repo = LLMCacheRepo(isTest)
        cache_manager = LLMCacheManager(cache_repo)

        self.llm_client = OllamaLocalClient(cache_manager)
        self.prompt_service = LLMPromptService(self.llm_client)
