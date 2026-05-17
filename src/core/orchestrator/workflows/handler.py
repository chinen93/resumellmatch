"""Handler for LLM services orchestration.

This module provides the Handler class that acts as a facade for initializing
and coordinating LLM-related services including caching, client connections,
and prompt management.
"""

from typing import Type

from config.logging import get_logger
from src.llm.client import OllamaLocalClient
from src.llm.prompt.prompt_service import LLMPromptService
from src.llm.utils.cache_manager import LLMCacheManager
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

    def __init__(self, prompt_service: Type[LLMPromptService], isTest: bool = False):
        self._log = get_logger("Handler")
        self._log.debug(f"Initializing Handler (test_mode={isTest})")

        cache_repo = LLMCacheRepo(isTest)
        cache_manager = LLMCacheManager(cache_repo)
        self._log.debug("Initialized LLM cache manager")

        self.llm_client = OllamaLocalClient(cache_manager)
        self._log.debug("Initialized Ollama LLM client")

        self.prompt_service = prompt_service(self.llm_client)
        self._log.debug("Initialized LLM prompt service")

        self._log.info("Handler initialization complete")
