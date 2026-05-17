"""Resume processing workflow orchestration.

This module handles the workflow for processing and enhancing resume documents,
including PDF reading, content extraction, and LLM-based enhancement.
"""

from config.logging import get_logger
from src.core.importer import ResumeImporter
from src.core.orchestrator.workflows.handler import Handler
from src.core.orchestrator.workflows.workflow_orchestrator import WorkflowOrchestrator
from src.core.processor import ResumeProcessor
from src.llm.prompt.services.LLMResumeService import LLMResumeService


def run_resume_workflow():
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

    resume_handler = Handler(prompt_service=LLMResumeService, isTest=False)
    log.debug("Handler initialized for resume workflow")

    orchestrator = WorkflowOrchestrator(resume_handler)
    log.debug("Workflow orchestrator created")

    # Process resume
    log.info("Processing resume from PDF file")
    orchestrator.run_simple_workflow(
        ResumeImporter, ResumeProcessor, "resume.pdf", isTest=False
    )
    log.debug("Resume processing completed")

    log.info("Resume workflow completed")
