"""Job-to-STAR matching and bullet point rewriting module.

Provides functionality to match job descriptions with STAR (Situation, Task,
Action, Result) entries and automatically rewrite STAR bullet points to better
align with job requirements.
"""

from typing import List

from config.logging import get_logger
from src.core.matcher.strategies import MatchScoreCombiner
from src.llm.prompt.LLMMatchService import LLMMatchService
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

    def __init__(self, prompt_service: LLMMatchService, isTest: bool):
        self._log = get_logger("JobStarMatch")
        self._log.debug("Initializing JobStarMatch")

        self.star_metadata_repo = StarMetadataRepo(isTest)
        self.star_entry_repo = StarEntryRepo(isTest)

        self.score_strategy = MatchScoreCombiner(prompt_service)

        self._log.debug("JobStarMatch initialized with repositories and matchers")

    def _star_entry_matches(self, job_parsed: str, entry_text: str) -> bool:
        """Evaluate whether a STAR entry matches the job description.

        Uses both the LLM matcher and string similarity matcher, then combines
        the results into a unified score.

        Args:
            job_parsed: Parsed job description text.
            entry_text: STAR entry text to compare.

        Returns:
            True if the combined match score exceeds the configured threshold.
        """
        if self.score_strategy.above_threshold(job_parsed, entry_text):
            return True

        return False

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
                    if self._star_entry_matches(job_parsed, str(entry)):
                        matching.append(str(entry))

        self._log.info(
            f"STAR matching completed. Found {len(matching)} matching entries"
        )

        return matching
