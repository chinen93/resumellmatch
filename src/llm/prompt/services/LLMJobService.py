from typing import List

from config.logging import get_logger
from src.llm.client.ollama import OllamaLocalClient
from src.llm.prompt.responses.base import BaseResponse
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

        prompt_responses: List[tuple] = [
            ("summary", PROMPT_EXTRACT_SUMMARY, JobSummaryResponse),
            ("role", PROMPT_EXTRACT_ROLE, JobRoleResponse),
            ("tech_skill", PROMPT_EXTRACT_TECH_SKILLS, JobTechSkillResponse),
            ("soft_skill", PROMPT_EXTRACT_SOFT_SKILLS, JobSoftSkillResponse),
            (
                "responsabilities",
                PROMPT_EXTRACT_RESPONSABILITIES,
                JobResponsabilitiesResponse,
            ),
            ("ownership", None, None),
            ("tools", PROMPT_EXTRACT_TOOLS, JobToolsResponse),
            ("methodologies", None, None),
            ("domain_knowledge", None, None),
            ("work_model", PROMPT_EXTRACT_WORK_MODEL, JobWorkModelResponse),
            ("compensation", PROMPT_EXTRACT_COMPENSATION, JobCompensationResponse),
        ]

        job_parsed = JobDescriptioKeywordsResponse(
            summary=self._extract(job_description, prompt_responses[0]),
            role=self._extract(job_description, prompt_responses[1]),
            technical_skills=self._extract(job_description, prompt_responses[2]),
            soft_skills=self._extract(job_description, prompt_responses[3]),
            responsabilities=self._extract(job_description, prompt_responses[4]),
            ownership="",
            tools=self._extract(job_description, prompt_responses[6]),
            methodologies="",
            domain_knowledge="",
            work_model=self._extract(job_description, prompt_responses[9]),
            compensation=self._extract(job_description, prompt_responses[10]),
        )

        self._log.debug(job_parsed.model_dump_json())

        return job_parsed.model_dump_json()

    def _extract(self, job_description: str, prompt_responses: tuple) -> str:

        key: str = prompt_responses[0]
        prompt: str = prompt_responses[1]
        response_type: type[BaseResponse] = prompt_responses[2]

        self._log.debug(f"Extracting job {key}")
        json_response = self._run_prompt(
            prompt_folder=PROMPT_FOLDER,
            prompt_filename=prompt,
            response_type=response_type,
            job_description=job_description,
        )

        if json_response is None:
            return ""

        return json_response
