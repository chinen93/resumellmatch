"""Job-to-STAR matching and bullet point rewriting module.

Provides functionality to match job descriptions with STAR (Situation, Task,
Action, Result) entries and automatically rewrite STAR bullet points to better
align with job requirements.
"""

import json
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
        self._log.debug("Initializing JobStarMatch")

        self.star_metadata_repo = StarMetadataRepo(isTest)
        self.star_entry_repo = StarEntryRepo(isTest)
        self._log.debug("JobStarMatch initialized with repositories")

    def _process_star_match(self, job_parsed: str, star_file_path: str) -> None:
        """Load STAR data, match with job, and rewrite matching bullets.

        Loads STAR entry from a JSON file, matches it against the job description,
        and if a match is found, rewrites the STAR bullet point to align with
        the job requirements.

        Args:
            job_parsed: The parsed job description with keywords and requirements.
            star_file_path: Path to JSON file containing STAR entry data.
        """
        self._log.debug(f"Processing STAR match for file: {star_file_path}")

        # Load STAR info
        star = FileReader.read_json_file(star_file_path)

        if not star:
            self._log.warning(f"Failed to load STAR data from {star_file_path}")
            return

        self._log.debug("STAR data loaded, performing LLM matching")
        match_job_star = self.prompt_service.match_job_with_star(job_parsed, star)

        if match_job_star:
            self._log.info("STAR-job match found, rewriting bullet points")
            self.prompt_service.rewrite_star_to_bullet_point(
                star, job_parsed, match_job_star
            )
            self._log.info("STAR bullets rewritten based on job match")
        else:
            self._log.info("No STAR match found for job description")

    # TODO: Function is too large, break it into smaller parts
    def get_matching_star(self, job_parsed: str) -> List[str]:
        """Find STAR entries that match the job description.

        Retrieves all STAR entries for the user, matches each against the job
        description using LLM analysis, and returns entries that meet the match criteria.

        Args:
            job_parsed: The parsed job description with requirements and keywords.

        Returns:
            List of matching STAR entries or descriptions.
        """
        self._log.info("Starting STAR matching process for job description")
        matching: List[str] = []

        star_metadatas = self.star_metadata_repo.get_all_by_user(user_id=1)
        self._log.debug(f"Retrieved {len(star_metadatas)} STAR metadata records")

        for metadata in star_metadatas:
            self._log.info(
                f"Processing STAR metadata: {metadata.title} - {metadata.subtitle}"
            )

            metadata_id = metadata.id
            if metadata_id is not None:
                star_entries = self.star_entry_repo.get_all_by_metadata(metadata_id)
                self._log.debug(
                    f"Found {len(star_entries)} STAR entries for metadata {metadata_id}"
                )

                for entry in star_entries:
                    self._log.debug(f"Matching STAR entry: {entry.title}")
                    match_job_star = self.prompt_service.match_job_with_star(
                        job_parsed, str(entry)
                    )

                    if match_job_star is None:
                        self._log.debug(
                            "STAR entry match call failed or returned no response"
                        )
                        continue

                    try:
                        match_response = json.loads(match_job_star)
                    except json.JSONDecodeError:
                        self._log.warning("Unable to parse STAR match response as JSON")
                        continue

                    score = match_response.get("score")
                    explanation = match_response.get("explanation")
                    threshold = 5

                    if isinstance(score, int) and score >= threshold:
                        self._log.info(
                            f"STAR entry matched with job description: {entry.title}"
                        )
                        self._log.debug(
                            f"Match score={score}, explanation={explanation}"
                        )
                        matching.append(str(entry))
                    else:
                        self._log.debug(
                            f"STAR entry did not meet threshold: score={score}, {explanation}"
                        )

        self._log.info(
            f"STAR matching completed. Found {len(matching)} matching entries"
        )

        return matching
