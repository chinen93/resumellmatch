from typing import List

from src.data_ingestion import FileReader
from src.llm.client import LLMPromptService
from config.logging import get_logger
from src.storage.repositories import StarEntryRepo, StarMetadataRepo


class JobStarMatch:
    """Handles matching job descriptions with STAR entries and rewriting bullets."""

    def __init__(self, prompt_service: LLMPromptService, isTest: bool):
        self.prompt_service = prompt_service
        self._log = get_logger("JobStarMatch")

        self.star_metadata_repo = StarMetadataRepo(isTest)
        self.star_entry_repo = StarEntryRepo(isTest)

    def _process_star_match(self, job_parsed: str, star_file_path: str) -> None:
        """Load STAR data, match with job, and rewrite bullets if match found."""
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
        """Return list of matching star based on job_parsed"""

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
