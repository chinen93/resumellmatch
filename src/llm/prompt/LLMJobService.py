from typing import Optional

from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.prompt_service import LLMPromptService
from src.llm.prompt.response import JobDescriptioKeywordsResponse

PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS = "extract_job_description_keywords.md"
PROMPT_FOLDER = "job"


class LLMJobService(LLMPromptService):

    def __init__(self, llm_client: OllamaLocalClient):
        super().__init__(llm_client)

    def extract_job_description_keywords(self, job_description: str) -> Optional[str]:
        """Extract keywords and requirements from a job description.

        Args:
            job_description: The job description text content.

        Returns:
            JSON with extracted keywords and skills or None if extraction fails.
        """
        return self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS,
            JobDescriptioKeywordsResponse,
            job_description=job_description,
        )
