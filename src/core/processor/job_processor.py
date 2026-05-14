"""Job description processing module.

Handles LLM-based extraction of keywords and requirements from job descriptions,
and persists both the original description and parsed results to the database.
"""

import json
from typing import Optional

from config.logging import get_logger
from src.llm.client.prompt_service import LLMPromptService
from src.storage.repositories import JobDescriptionParsedRepo, JobDescriptionRepo


class JobDescriptionProcessor:
    """Process job descriptions through LLM and persist results.

    Orchestrates the extraction of skills, keywords, and requirements from
    job descriptions using LLM prompts, then stores both raw and parsed data.

    Attributes:
        prompt_service: LLMPromptService for running LLM prompts.
        job_repo: Repository for JobDescription entities.
        parsed_repo: Repository for JobDescriptionParsed entities.
    """

    def __init__(self, prompt_service: LLMPromptService, isTest: bool = True):
        self.prompt_service = prompt_service
        self.job_repo = JobDescriptionRepo(isTest)
        self.parsed_repo = JobDescriptionParsedRepo(isTest)
        self._log = get_logger("JobDescriptionProcessor")

    def new_item(self, job_description: str, input_hash: str) -> Optional[str]:
        """Process a new job description and persist it.

        Runs the job description through LLM keyword extraction, then stores
        both the original description and the parsed results in the database.

        Args:
            job_description: The raw job description text.
            input_hash: SHA256 hash of the job description for caching.

        Returns:
            The LLM response with extracted keywords or None if processing failed.
        """
        self._log.info("Processing new job description")
        self._log.debug(f"Input hash: {input_hash[:8]}...")

        job_parsed = self.prompt_service.extract_job_description_keywords(
            job_description
        )

        if job_parsed is not None:
            self._log.debug("LLM keyword extraction successful")
            self._persist_job(job_description, input_hash, job_parsed)
            self._log.info("Job description processing completed")
            return job_parsed
        else:
            self._log.warning("LLM keyword extraction failed")
            return None

        return job_parsed

    def exist_job_description(self, input_hash: str) -> Optional[str]:
        """Check if job description has been previously processed.

        Looks up whether this job description (by hash) has been previously
        processed and returns the cached LLM response if available.

        Args:
            input_hash: SHA256 hash of the job description.

        Returns:
            The previously processed result or None if not found.
        """
        self._log.debug(
            f"Checking for existing job description with hash: {input_hash[:8]}..."
        )
        existing = self.parsed_repo.get_by_input_hash(input_hash)
        if existing:
            self._log.debug("Found cached job description processing result")
            return str(existing.full_response)
        else:
            self._log.debug("No cached result found for job description")

        return None

    def _persist_job(self, job_description: str, input_hash: str, job_parsed: str):
        """Persist job description and parsed data to the database.

        Stores both the original job description and the LLM-extracted data
        (skills, keywords, etc.) to the database.

        Args:
            job_description: The raw job description text.
            input_hash: SHA256 hash for caching.
            job_parsed: The LLM response as a JSON string.
        """
        self._log.debug("Persisting job description to database")
        try:
            job_id = self.job_repo.create_from_fields(
                id=None, url="", title="", raw_text=job_description
            )
            self._log.debug(f"Created job description record with ID: {job_id}")

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
            self._log.debug("Created parsed job description record")
        except Exception as e:
            self._log.error(f"Failed to persist job description: {e}")
            raise
        except Exception:
            pass
