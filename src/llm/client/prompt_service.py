"""Prompt-based LLM workflow service.

Provides high-level methods for running structured LLM workflows using
predefined prompts for specific tasks like resume keyword extraction,
job description parsing, and job-STAR matching.
"""

from typing import Optional

from config.logging import get_logger
from src.llm.client.ollama import OllamaLocalClient
from src.llm.client.prompt_loader import PromptLoader
from src.llm.client.response import (
    ExtractKeywordResponse,
    JobDescriptioKeywordsResponse,
    MatchJobWithStarResponse,
    RewriteStarResponse,
)

PROMPT_EXTRACT_RESUME_KEYWORDS = "extract_resume_keywords.md"
PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS = "extract_job_description_keywords.md"
PROMPT_MATCH_JOB_WITH_STAR = "match_job_with_star.md"
PROMPT_REWRITE_STAR_BULLET_POINT = "rewrite_star_bullet_point.md"


class LLMPromptService:
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
        self, prompt_filename: str, response_type: type, **template_kwargs
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
        prompt_template = self.prompt_loader.load(prompt_filename)
        if prompt_template is None:
            return None

        try:
            return self.llm_client.generate_with_cache(
                prompt_template.format(**template_kwargs), response_type
            )
        except Exception as e:
            self._log.error(f"Prompt execution failed for {prompt_filename}: {e}")
            return None

    def extract_resume_keywords(self, resume_text: str) -> Optional[str]:
        """Extract keywords and key information from a resume.

        Args:
            resume_text: The resume text content.

        Returns:
            JSON with extracted keywords or None if extraction fails.
        """
        return self._run_prompt(
            PROMPT_EXTRACT_RESUME_KEYWORDS,
            ExtractKeywordResponse,
            resume_text=resume_text,
        )

    def extract_job_description_keywords(self, job_description: str) -> Optional[str]:
        """Extract keywords and requirements from a job description.

        Args:
            job_description: The job description text content.

        Returns:
            JSON with extracted keywords and skills or None if extraction fails.
        """
        return self._run_prompt(
            PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS,
            JobDescriptioKeywordsResponse,
            job_description=job_description,
        )

    def match_job_with_star(self, job_parsed: str, star_text: str) -> Optional[str]:
        """Match a job description with a STAR entry.

        Args:
            job_parsed: Parsed job description with extracted info.
            star_text: STAR entry text.

        Returns:
            Match score/analysis or None if matching fails.
        """
        return self._run_prompt(
            PROMPT_MATCH_JOB_WITH_STAR,
            MatchJobWithStarResponse,
            job_parsed=job_parsed,
            star_text=star_text,
        )

    def rewrite_star_to_bullet_point(
        self, star_text: str, job_parsed: str, match_score: str
    ) -> Optional[str]:
        """Rewrite STAR entry as a bullet point aligned with job requirements.

        Args:
            star_text: Original STAR entry text.
            job_parsed: Parsed job description with requirements.
            match_score: Match score or analysis from previous matching.

        Returns:
            Rewritten bullet point or None if rewriting fails.
        """
        return self._run_prompt(
            PROMPT_REWRITE_STAR_BULLET_POINT,
            RewriteStarResponse,
            star_text=star_text,
            job_parsed=job_parsed,
            match_score=match_score,
        )
