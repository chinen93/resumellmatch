from typing import Optional

from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.responses.match_response import MatchJobWithStarResponse
from src.llm.prompt.services.prompt_service import LLMPromptService

PROMPT_MATCH_JOB_WITH_STAR = "match_job_with_star.md"
PROMPT_FOLDER = "match"


class LLMMatchService(LLMPromptService):

    def __init__(self, llm_client: OllamaLocalClient):
        super().__init__(llm_client)

    def match_job_with_star(self, job_parsed: str, star_text: str) -> Optional[str]:
        """Match a job description with a STAR entry.

        Args:
            job_parsed: Parsed job description with extracted info.
            star_text: STAR entry text.

        Returns:
            Match score/analysis or None if matching fails.
        """
        return self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_MATCH_JOB_WITH_STAR,
            MatchJobWithStarResponse,
            job_parsed=job_parsed,
            star_text=star_text,
        )
