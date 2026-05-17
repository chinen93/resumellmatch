from typing import List

from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.responses.job_response import (
    JobDescriptioKeywordsResponse,
    JobResponsabilitiesResponse,
    JobSoftSkillResponse,
    JobSummaryResponse,
)
from src.llm.prompt.services.prompt_service import LLMPromptService

PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS = "extract_job_description_keywords.md"
PROMPT_EXTRACT_JOB_DESCRIPTION_SUMMARY = "extract_job_summary.md"
PROMPT_EXTRACT_JOB_DESCRIPTION_RESPONSABILITIES = "extract_job_responsabilities.md"
PROMPT_EXTRACT_JOB_DESCRIPTION_SOFT_SKILLS = "extract_job_soft_skills.md"


PROMPT_FOLDER = "job"


class LLMJobService(LLMPromptService):

    def __init__(self, llm_client: OllamaLocalClient):
        super().__init__(llm_client)

    def extract_job_description_keywords(self, job_description: str) -> str:
        """Extract keywords and requirements from a job description.

        Args:
            job_description: The job description text content.

        Returns:
            JSON with extracted keywords and skills or None if extraction fails.
        """

        job_parsed = JobDescriptioKeywordsResponse(
            summary=self.extract_job_summary(job_description),
            role=[],
            technical_skills=[],
            soft_skills=self.extract_job_soft_skills(job_description),
            responsabilities=self.extract_job_responsabilities(job_description),
            ownership=[],
            tools=[],
            methodologies=[],
            domain_knowledge=[],
            work_model=[],
            compensation=[],
        )

        return job_parsed.model_dump_json()

    def extract_job_summary(self, job_description: str) -> str:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_JOB_DESCRIPTION_SUMMARY,
            JobSummaryResponse,
            job_description=job_description,
        )

        if json_response is None:
            return ""

        response = JobSummaryResponse.model_validate_json(json_response)
        return response.summary

    def extract_job_soft_skills(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_JOB_DESCRIPTION_SOFT_SKILLS,
            JobSoftSkillResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobSoftSkillResponse.model_validate_json(json_response)
        return response.skills

    def extract_job_responsabilities(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_JOB_DESCRIPTION_RESPONSABILITIES,
            JobResponsabilitiesResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobResponsabilitiesResponse.model_validate_json(json_response)
        return response.responsabilities
