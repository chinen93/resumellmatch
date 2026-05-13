"""Main application handlers for core workflows.

This module contains the main orchestration logic for job processing, resume handling,
and STAR entry import workflows. Each handler coordinates multiple components including
importers, processors, and LLM services.
"""

from config.logging import get_logger
from src.core.importer import (
    JobDescriptionImporter,
    ResumeImporter,
    StarEntryImporter,
    StarMetadataImporter,
)
from src.core.matcher import JobStarMatch
from src.core.processor import (
    JobDescriptionProcessor,
    ResumeProcessor,
    StarEntryProcessor,
    StarMetadataProcessor,
)
from src.data_ingestion import CSVLoader
from src.llm.client import LLMCacheManager, LLMPromptService, OllamaLocalClient
from src.storage.repositories import LLMCacheRepo


class Handler:
    """Orchestrates LLM client and processing services.

    Acts as a facade providing unified access to LLM capabilities and prompt
    services for various processing workflows.

    Attributes:
        _log: Logger instance for this handler.
        llm_client: Ollama LLM client for text generation.
        prompt_service: Service for prompt-based LLM workflows with caching.

    Args:
        isTest: If True, uses test database; if False, uses production database.
    """

    def __init__(self, isTest: bool = False):
        self._log = get_logger("Handler")

        cache_repo = LLMCacheRepo(isTest)
        cache_manager = LLMCacheManager(cache_repo)
        self.llm_client = OllamaLocalClient(cache_manager)
        self.prompt_service = LLMPromptService(self.llm_client)


def handle_job():
    """
    Handle all Job related resume match

    Steps:
        1) Read and Parse Job Description
        2) For all resume match with job description and separe the best match score
        3) IF score is less than X improve resume with rewriten star responses
        4) Rewrite resume to have keywords from job description
    """

    handler = Handler(isTest=False)
    handler._log.info("Handle Job Description")

    job_processor = JobDescriptionProcessor(handler.prompt_service, isTest=False)
    job_importer = JobDescriptionImporter(job_processor)

    job_parsed = job_importer.run("job_description.txt")

    if job_parsed:
        job_star_match = JobStarMatch(handler.prompt_service, isTest=False)

        # TODO:
        _ = job_star_match.get_matching_star(job_parsed)

    handler._log.info("Finished handling Job Description")


def handle_star():
    """Process STAR interview response data from CSV files.

    Imports STAR (Situation, Task, Action, Result) interview responses from CSV files
    into the system. Processes both metadata (experience context) and individual
    entries (STAR stories).

    Workflow:
        1. Load STAR metadata from CSV (star_metadata.csv)
        2. Process and validate metadata entries
        3. Load STAR entries from CSV (star_entries.csv)
        4. Process and validate individual stories
    """
    handler = Handler(isTest=False)
    handler._log.info("Handle STAR responses")

    csvLoader = CSVLoader()

    star_metadata_processor = StarMetadataProcessor(isTest=False)
    star_metadata_importer = StarMetadataImporter(
        loader=csvLoader, processor=star_metadata_processor
    )
    star_metadata_importer.run(filename="star/star_metadata.csv")

    star_entry_processor = StarEntryProcessor(isTest=False)
    star_entry_importer = StarEntryImporter(
        loader=csvLoader, processor=star_entry_processor
    )
    star_entry_importer.run(filename="star/star_entries.csv")

    handler._log.info("Finished handling STAR responses")


def handle_resume():
    """Process and enhance a resume document.

    Imports a resume from a PDF file and processes it with LLM enhancement.
    Extracts key information and generates enriched text for job matching.

    Workflow:
        1. Read resume from PDF file (resume.pdf)
        2. Extract and parse resume content
        3. Process with LLM for keyword extraction and enhancement
        4. Store processed resume in database
    """
    handler = Handler(isTest=False)
    handler._log.info("Handle Resume")

    resume_processor = ResumeProcessor(handler.prompt_service, isTest=False)
    resume_importer = ResumeImporter(resume_processor)

    resume_importer.run("resume.pdf")

    handler._log.info("Finished handling Resume")
