from typing import Optional

from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.responses.star_response import RewriteStarResponse
from src.llm.prompt.services.prompt_service import LLMPromptService

PROMPT_REWRITE_STAR_BULLET_POINT = "rewrite_star_bullet_point.md"
PROMPT_FOLDER = "star"


class LLMStarService(LLMPromptService):

    def __init__(self, llm_client: OllamaLocalClient):
        super().__init__(llm_client)

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
            PROMPT_FOLDER,
            PROMPT_REWRITE_STAR_BULLET_POINT,
            RewriteStarResponse,
            star_text=star_text,
            job_parsed=job_parsed,
            match_score=match_score,
        )
