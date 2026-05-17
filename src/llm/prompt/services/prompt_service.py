"""Prompt-based LLM workflow service.

Provides high-level methods for running structured LLM workflows using
predefined prompts for specific tasks like resume keyword extraction,
job description parsing, and job-STAR matching.
"""

from abc import ABC
from typing import Optional

from config.logging import get_logger
from src.llm.client.ollama import OllamaLocalClient
from src.llm.utils.prompt_loader import PromptLoader


# TODO: Transform this class into a simpler factory
class LLMPromptService(ABC):
    """Service for executing prompt-based LLM workflows.

    Manages loading and executing predefined prompts for structured tasks,
    with built-in caching and response validation.

    Attributes:
        llm_client: OllamaLocalClient for LLM generation.
        prompt_loader: PromptLoader for loading prompt templates.
        _log: Logger instance.
    """

    def __init__(self, llm_client: OllamaLocalClient):
        self.llm_client = llm_client
        self.prompt_loader = PromptLoader()
        self._log = get_logger("LLMPromptService")

    def _run_prompt(
        self,
        prompt_folder: str,
        prompt_filename: str,
        response_type: type,
        **template_kwargs,
    ) -> Optional[str]:
        """Run a prompt template with variable substitution.

        Loads a prompt template, substitutes variables, and executes it
        through the LLM client with response validation.

        Args:
            prompt_filename: Name of the prompt template file to load.
            response_type: Pydantic response model for validation.
            **template_kwargs: Variables for template substitution.

        Returns:
            The LLM response as validated JSON or None if execution fails.
        """
        prompt_template = self.prompt_loader.load(prompt_folder, prompt_filename)
        if prompt_template is None:
            return None

        try:
            return self.llm_client.generate_with_cache(
                prompt_template.format(**template_kwargs), response_type
            )
        except Exception as e:
            self._log.error(f"Prompt execution failed for {prompt_filename}: {e}")
            return None
