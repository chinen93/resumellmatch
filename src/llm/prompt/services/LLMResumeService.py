from typing import Optional

from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.responses.resume_response import ExtractKeywordResponse
from src.llm.prompt.services.prompt_service import LLMPromptService

PROMPT_EXTRACT_RESUME_KEYWORDS = "extract_resume_keywords.md"
PROMPT_FOLDER = "resume"


class LLMResumeService(LLMPromptService):

    def __init__(self, llm_client: OllamaLocalClient):
        super().__init__(llm_client)

    def extract_resume_keywords(self, resume_text: str) -> Optional[str]:
        """Extract keywords and key information from a resume.

        Args:
            resume_text: The resume text content.

        Returns:
            JSON with extracted keywords or None if extraction fails.
        """
        return self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_RESUME_KEYWORDS,
            ExtractKeywordResponse,
            resume_text=resume_text,
        )
