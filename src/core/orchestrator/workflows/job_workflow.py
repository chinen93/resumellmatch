"""Job description workflow orchestration.

This module handles the complete workflow for processing job descriptions,
including parsing, keyword extraction, and matching against STAR entries.
"""

from logging import Logger
from typing import Optional, cast

from config.logging import get_logger
from src.core.importer import JobDescriptionImporter
from src.core.matcher import JobStarMatch
from src.core.orchestrator.workflows.handler import Handler
from src.core.processor import JobDescriptionProcessor
from src.llm.prompt.services.LLMJobService import LLMJobService
from src.llm.prompt.services.LLMMatchService import LLMMatchService

JOB_DESCRIPTION_FILE = "job_description.txt"


def _job_parser(use_llm_cache: bool, log: Logger) -> Optional[str]:
    job_handler = Handler(
        prompt_service=LLMJobService,
        isTest=False,
        use_llm_cache=use_llm_cache,
    )
    log.debug("Handler initialized for job workflow")

    job_processor = JobDescriptionProcessor(
        cast(LLMJobService, job_handler.prompt_service),
        isTest=False,
        use_llm_cache=use_llm_cache,
    )
    job_importer = JobDescriptionImporter(job_processor)

    return job_importer.run(JOB_DESCRIPTION_FILE)


def run_job_workflow(use_llm_cache: bool):
    """Execute the complete job description processing workflow.

    Steps:
        1) Read and Parse Job Description
        2) For all resume match with job description and separate the best match score
        3) IF score is less than X improve resume with rewritten star responses
        4) Rewrite resume to have keywords from job description
    """
    log = get_logger("JobWorkflow")
    log.info("Starting job description workflow")

    job_parsed = _job_parser(use_llm_cache=use_llm_cache, log=log)

    if job_parsed:
        log.info(
            "Job description processed successfully, proceeding with STAR matching"
        )
        # Match against STAR entries
        match_handler = Handler(
            prompt_service=LLMMatchService,
            isTest=False,
            use_llm_cache=use_llm_cache,
        )
        job_star_match = JobStarMatch(match_handler.prompt_service, isTest=False)
        log.debug("Created job-STAR matcher")

        # TODO: Implement matching logic
        log.info("Starting job-STAR matching process")
        _ = job_star_match.get_matching_star(job_parsed)
        log.info("Job-STAR matching completed")

        # TODO after matching some STAR, implement logic to recreate the resume with the new information
    else:
        log.warning("Job description processing failed or returned no results")

    log.info("Job description workflow completed")
