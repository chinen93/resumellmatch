"""Job description workflow orchestration.

This module handles the complete workflow for processing job descriptions,
including parsing, keyword extraction, and matching against STAR entries.
"""

from config.logging import get_logger
from src.core.importer import JobDescriptionImporter
from src.core.matcher import JobStarMatch
from src.core.orchestrator.workflows.handler import Handler
from src.core.orchestrator.workflows.workflow_orchestrator import WorkflowOrchestrator
from src.core.processor import JobDescriptionProcessor


def run_job_workflow():
    """Execute the complete job description processing workflow.

    Steps:
        1) Read and Parse Job Description
        2) For all resume match with job description and separate the best match score
        3) IF score is less than X improve resume with rewritten star responses
        4) Rewrite resume to have keywords from job description
    """
    handler = Handler(isTest=False)

    log = get_logger("JobWorkflow")
    log.info("Starting job description workflow")

    orchestrator = WorkflowOrchestrator(handler)

    # Process job description
    job_parsed = orchestrator.run_simple_workflow(
        JobDescriptionImporter,
        JobDescriptionProcessor,
        "job_description.txt",
        isTest=False,
    )

    if job_parsed:
        # Match against STAR entries
        job_star_match = JobStarMatch(handler.prompt_service, isTest=False)
        # TODO: Implement matching logic
        _ = job_star_match.get_matching_star(job_parsed)

    log.info("Finished job description workflow")
