import json
from typing import Optional

from src.llm.client.ollama import OllamaLocalClient
from src.storage.repositories import JobDescriptionParsedRepo, JobDescriptionRepo


class JobDescriptionProcessor:
    """Handle creating StarMetadata objects and persisting them via repo."""

    def __init__(self, llm_client: OllamaLocalClient, isTest: bool = True):
        self.llm_client = llm_client
        self.job_repo = JobDescriptionRepo(isTest)
        self.parsed_repo = JobDescriptionParsedRepo(isTest)

    def new_item(self, job_description: str, input_hash: str) -> Optional[str]:
        job_parsed = self.llm_client.extract_job_description_keywords(job_description)

        if job_parsed is not None:
            self._persist_job(job_description, input_hash, job_parsed)

        return job_parsed

    def exist_job_description(self, input_hash: str) -> Optional[str]:
        existing = self.parsed_repo.get_by_input_hash(input_hash)
        if existing:
            # handler._log.info("Using cached parsed job description from DB")
            return str(existing.full_response)

        return None

    def _persist_job(self, job_description: str, input_hash: str, job_parsed: str):
        # persist job description and parsed response
        try:
            job_id = self.job_repo.create_from_fields(
                id=None, url="", title="", raw_text=job_description
            )

            # attempt to extract fields from the LLM response JSON
            parsed_obj = json.loads(job_parsed)
            summary = parsed_obj.get("summary", "")
            required_skills = json.dumps(parsed_obj.get("technical_skills", []))
            prefered_skills = json.dumps(parsed_obj.get("soft_skills", []))
            keywords = json.dumps(parsed_obj.get("keywords", []))

            self.parsed_repo.create_from_fields(
                id=None,
                job_description_id=job_id,
                summary=summary,
                required_skills=required_skills,
                prefered_skills=prefered_skills,
                keywords=keywords,
                input_hash=input_hash,
                full_response=job_parsed,
            )
        except Exception:
            pass
            # handler._log.exception("Failed to persist parsed job description")
