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
from src.logging_config import get_logger
from src.storage.repositories import LLMCacheRepo


class Handler:
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
    handler = Handler(isTest=False)
    handler._log.info("Handle Resume")

    resume_processor = ResumeProcessor(handler.prompt_service, isTest=False)
    resume_importer = ResumeImporter(resume_processor)

    resume_importer.run("resume.pdf")

    handler._log.info("Finished handling Resume")
