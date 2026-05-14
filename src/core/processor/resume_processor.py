"""Resume processing module.

Handles LLM-based extraction of keywords and information from resumes,
and persists both the original resume and extracted content to the database.
"""

from typing import Optional

from config.logging import get_logger
from src.llm.client.prompt_service import LLMPromptService
from src.storage.repositories import ResumeRepo


class ResumeProcessor:
    """Process resumes through LLM and persist results.

    Orchestrates the extraction of keywords and key information from resumes
    using LLM prompts, then stores both raw and processed data.

    Attributes:
        prompt_service: LLMPromptService for running LLM prompts.
        resume_repo: Repository for Resume entities.
    """

    def __init__(self, prompt_service: LLMPromptService, isTest: bool = True):
        self.prompt_service = prompt_service
        self.resume_repo = ResumeRepo(isTest)
        self._log = get_logger("ResumeProcessor")

    def new_item(self, resume: str, input_hash: str) -> Optional[str]:
        """Process a new resume and persist it.

        Runs the resume through LLM keyword extraction, then stores both
        the original resume and the enhanced version in the database.

        Args:
            resume: The raw resume text.
            input_hash: SHA256 hash of the resume for caching.

        Returns:
            The LLM response with extracted keywords or None if processing failed.
        """
        self._log.info("Processing new resume")
        self._log.debug(f"Input hash: {input_hash[:8]}...")

        resume_parsed = self.prompt_service.extract_resume_keywords(resume)

        if resume_parsed is not None:
            self._log.debug("LLM keyword extraction successful")
            self._persist_resume(resume, input_hash, resume_parsed)
            self._log.info("Resume processing completed")
            return resume_parsed
        else:
            self._log.warning("LLM keyword extraction failed")
            return None

    def exist_resume(self, input_hash: str) -> Optional[str]:
        """Check if resume has been previously processed.

        Looks up whether this resume (by hash) has been previously processed
        and returns the cached resume if available.

        Args:
            input_hash: SHA256 hash of the resume.

        Returns:
            The previously processed resume or None if not found.
        """
        self._log.debug(f"Checking for existing resume with hash: {input_hash[:8]}...")
        existing = self.resume_repo.get_by_input_hash(input_hash)
        if existing:
            self._log.debug("Found cached resume processing result")
            return str(existing.raw_text)
        else:
            self._log.debug("No cached result found for resume")

        return None

    def _persist_resume(self, resume: str, input_hash: str, resume_parsed: str) -> None:
        """Persist resume and processed data to the database.

        Stores both the original resume and the LLM-processed version to the database.

        Args:
            resume: The raw resume text.
            input_hash: SHA256 hash for caching.
            resume_parsed: The LLM response with extracted content.
        """
        self._log.debug("Persisting resume to database")
        try:
            self.resume_repo.create_from_fields(
                id=None,
                user_id=1,
                raw_text=resume,
                input_hash=input_hash,
                full_text=resume_parsed,
            )
            self._log.debug("Resume persisted successfully")
        except Exception as e:
            self._log.error(f"Failed to persist resume: {e}")
            raise
