from typing import List

from config.logging import get_logger
from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.responses.job_response import (
    JobCompensationResponse,
    JobDescriptioKeywordsResponse,
    JobResponsabilitiesResponse,
    JobRoleResponse,
    JobSoftSkillResponse,
    JobSummaryResponse,
    JobTechSkillResponse,
    JobToolsResponse,
    JobWorkModelResponse,
)
from src.llm.prompt.services.prompt_service import LLMPromptService

PROMPT_EXTRACT_KEYWORDS = "extract_job_description_keywords.md"
PROMPT_EXTRACT_SUMMARY = "extract_job_summary.md"
PROMPT_EXTRACT_RESPONSABILITIES = "extract_job_responsabilities.md"
PROMPT_EXTRACT_SOFT_SKILLS = "extract_job_soft_skills.md"
PROMPT_EXTRACT_WORK_MODEL = "extract_job_work_model.md"
PROMPT_EXTRACT_TECH_SKILLS = "extract_job_tech_skills.md"
PROMPT_EXTRACT_TOOLS = "extract_job_tools.md"
PROMPT_EXTRACT_ROLE = "extract_job_role.md"
PROMPT_EXTRACT_COMPENSATION = "extract_job_compensation.md"


PROMPT_FOLDER = "job"


# TODO: Make it easier to change the values
class LLMJobService(LLMPromptService):

    def __init__(self, llm_client: OllamaLocalClient):
        super().__init__(llm_client)
        self._log = get_logger("LLMJobService")

    def extract_job_description_keywords(self, job_description: str) -> str:
        """Extract keywords and requirements from a job description.

        Args:
            job_description: The job description text content.

        Returns:
            JSON with extracted keywords and skills or None if extraction fails.
        """
        self._log.debug("Extract job description keywords")

        job_parsed = JobDescriptioKeywordsResponse(
            summary=self._extract_summary(job_description),
            role=self._extract_role(job_description),
            technical_skills=self._extract_tech_skill(job_description),
            soft_skills=self._extract_soft_skills(job_description),
            responsabilities=self._extract_responsabilities(job_description),
            ownership=[],
            tools=self._extract_tools(job_description),
            methodologies=[],
            domain_knowledge=[],
            work_model=self._extract_work_model(job_description),
            compensation=self._extract_compensation(job_description),
        )

        self._log.debug(job_parsed.model_dump_json())

        return job_parsed.model_dump_json()

    def _extract_summary(self, job_description: str) -> str:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_SUMMARY,
            JobSummaryResponse,
            job_description=job_description,
        )

        if json_response is None:
            return ""

        response = JobSummaryResponse.model_validate_json(json_response)
        return response.summary

    def _extract_work_model(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_WORK_MODEL,
            JobWorkModelResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobWorkModelResponse.model_validate_json(json_response)
        return response.work_model

    def _extract_role(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_ROLE,
            JobRoleResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobRoleResponse.model_validate_json(json_response)
        return response.role

    def _extract_tech_skill(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_TECH_SKILLS,
            JobTechSkillResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobTechSkillResponse.model_validate_json(json_response)
        return response.skills

    def _extract_soft_skills(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_SOFT_SKILLS,
            JobSoftSkillResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobSoftSkillResponse.model_validate_json(json_response)
        return response.skills

    def _extract_responsabilities(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_RESPONSABILITIES,
            JobResponsabilitiesResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobResponsabilitiesResponse.model_validate_json(json_response)
        return response.responsabilities

    def _extract_compensation(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_COMPENSATION,
            JobCompensationResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobCompensationResponse.model_validate_json(json_response)
        return response.compensation

    def _extract_tools(self, job_description: str) -> List[str]:
        json_response = self._run_prompt(
            PROMPT_FOLDER,
            PROMPT_EXTRACT_TOOLS,
            JobToolsResponse,
            job_description=job_description,
        )

        if json_response is None:
            return []

        response = JobToolsResponse.model_validate_json(json_response)
        return response.tools
