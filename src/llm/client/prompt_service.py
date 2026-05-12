from typing import Optional

from src.llm.client.ollama import OllamaLocalClient
from src.llm.client.prompt_loader import PromptLoader
from src.llm.client.response import (
    ExtractKeywordResponse,
    JobDescriptioKeywordsResponse,
    MatchJobWithStarResponse,
    RewriteStarResponse,
)
from config.logging import get_logger

PROMPT_EXTRACT_RESUME_KEYWORDS = "extract_resume_keywords.md"
PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS = "extract_job_description_keywords.md"
PROMPT_MATCH_JOB_WITH_STAR = "match_job_with_star.md"
PROMPT_REWRITE_STAR_BULLET_POINT = "rewrite_star_bullet_point.md"


class LLMPromptService:
    """Runs prompt-based workflows on a generic LLM client."""

    def __init__(self, llm_client: OllamaLocalClient):
        self.llm_client = llm_client
        self.prompt_loader = PromptLoader()
        self._log = get_logger("LLMPromptService")

    def _run_prompt(
        self, prompt_filename: str, response_type: type, **template_kwargs
    ) -> Optional[str]:
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
        return self._run_prompt(
            PROMPT_EXTRACT_RESUME_KEYWORDS,
            ExtractKeywordResponse,
            resume_text=resume_text,
        )

    def extract_job_description_keywords(self, job_description: str) -> Optional[str]:
        return self._run_prompt(
            PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS,
            JobDescriptioKeywordsResponse,
            job_description=job_description,
        )

    def match_job_with_star(self, job_parsed: str, star_text: str) -> Optional[str]:
        return self._run_prompt(
            PROMPT_MATCH_JOB_WITH_STAR,
            MatchJobWithStarResponse,
            job_parsed=job_parsed,
            star_text=star_text,
        )

    def rewrite_star_to_bullet_point(
        self, star_text: str, job_parsed: str, match_score: str
    ) -> Optional[str]:
        return self._run_prompt(
            PROMPT_REWRITE_STAR_BULLET_POINT,
            RewriteStarResponse,
            star_text=star_text,
            job_parsed=job_parsed,
            match_score=match_score,
        )
