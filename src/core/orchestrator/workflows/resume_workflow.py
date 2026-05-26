"""Resume processing workflow orchestration.

This module handles the workflow for processing and enhancing resume documents,
including PDF reading, content extraction, and LLM-based enhancement.
"""

from typing import cast

from config.logging import get_logger
from src.core.importer import ResumeImporter
from src.core.orchestrator.workflows.handler import Handler
from src.core.processor import ResumeProcessor
from src.llm.prompt.services.LLMResumeService import LLMResumeService

RESUME_FILE = "resume.pdf"


def run_resume_workflow(use_llm_cache: bool):
    """Execute the resume processing workflow.

    Imports a resume from a PDF file and processes it with LLM enhancement.
    Extracts key information and generates enriched text for job matching.

    Workflow:
        1. Read resume from PDF file (resume.pdf)
        2. Extract and parse resume content
        3. Process with LLM for keyword extraction and enhancement
        4. Store processed resume in database
    """
    log = get_logger("ResumeWorkflow")
    log.info("Starting resume workflow")

    resume_handler = Handler(
        prompt_service=LLMResumeService,
        isTest=False,
        use_llm_cache=use_llm_cache,
    )
    log.debug("Handler initialized for resume workflow")

    resume_processor = ResumeProcessor(
        cast(LLMResumeService, resume_handler.prompt_service), isTest=False
    )
    resume_importer = ResumeImporter(resume_processor)

    log.info("Processing resume from PDF file")
    resume_importer.run(RESUME_FILE)
    log.debug("Resume processing completed")

    log.info("Resume workflow completed")
