"""Job-to-STAR matching and bullet point rewriting module.

Provides functionality to match job descriptions with STAR (Situation, Task,
Action, Result) entries and automatically rewrite STAR bullet points to better
align with job requirements.
"""

from typing import List

from config.logging import get_logger
from src.data_ingestion import FileReader
from src.llm.client import LLMPromptService
from src.storage.repositories import StarEntryRepo, StarMetadataRepo


class JobStarMatch:
    """Orchestrates matching between job descriptions and STAR entries.

    Uses LLM to find STAR entries that match job requirements and can rewrite
    STAR bullet points to better align with job descriptions.

    Attributes:
        prompt_service: LLMPromptService for LLM matching operations.
        star_metadata_repo: Repository for STAR metadata.
        star_entry_repo: Repository for individual STAR entries.
        _log: Logger instance.
    """

    def __init__(self, prompt_service: LLMPromptService, isTest: bool):
        self.prompt_service = prompt_service
        self._log = get_logger("JobStarMatch")

        self.star_metadata_repo = StarMetadataRepo(isTest)
        self.star_entry_repo = StarEntryRepo(isTest)

    def _process_star_match(self, job_parsed: str, star_file_path: str) -> None:
        """Load STAR data, match with job, and rewrite matching bullets.

        Loads STAR entry from a JSON file, matches it against the job description,
        and if a match is found, rewrites the STAR bullet point to align with
        the job requirements.

        Args:
            job_parsed: The parsed job description with keywords and requirements.
            star_file_path: Path to JSON file containing STAR entry data.
        """
        # Load STAR info
        star = FileReader.read_json_file(star_file_path)

        if not star:
            self._log.warning(f"Failed to load STAR data from {star_file_path}")
            return

        match_job_star = self.prompt_service.match_job_with_star(job_parsed, star)

        if match_job_star:
            self.prompt_service.rewrite_star_to_bullet_point(
                star, job_parsed, match_job_star
            )
            self._log.info("STAR bullets rewritten based on job match")
        else:
            self._log.info("No STAR match found for job description")

    def get_matching_star(self, job_parsed: str) -> List[str]:
        """Find STAR entries that match the job description.

        Retrieves all STAR entries for the user, matches each against the job
        description using LLM analysis, and returns entries that meet the match criteria.

        Note: This method currently has incomplete threshold logic (TODO).

        Args:
            job_parsed: The parsed job description with requirements and keywords.

        Returns:
            List of matching STAR entries or descriptions.
        """

        matching: List[str] = []

        star_metadatas = self.star_metadata_repo.get_all_by_user(user_id=1)
        for metadata in star_metadatas:

            metadata_id = metadata.id
            if metadata_id is not None:
                star_entries = self.star_entry_repo.get_all_by_metadata(metadata_id)

                for entry in star_entries:
                    self._log.debug(str(entry))
                    match_job_star = self.prompt_service.match_job_with_star(
                        job_parsed, str(entry)
                    )

                    if match_job_star:
                        self._log.debug(match_job_star)

        # TODO:
        # Match entry with job parsed
        # if matching score > threshold add it to matching return list

        return matching
