"""Main application entry point for core workflows.

This module serves as the entry point for the application's core workflows.
It delegates to the workflow factory for executing different workflow types.
"""

from config.logging import get_logger
from src.core.orchestrator.factory import WorkflowFactory, WorkflowType


def handle_job(use_llm_cache: bool = True):
    """Handle all job-related resume matching workflow."""
    log = get_logger("MainHandler")
    log.info("Job workflow requested")
    WorkflowFactory.run_workflow(WorkflowType.JOB, use_llm_cache=use_llm_cache)


def handle_star(use_llm_cache: bool = True):
    """Process STAR interview response data from CSV files."""
    log = get_logger("MainHandler")
    log.info("STAR workflow requested")
    WorkflowFactory.run_workflow(WorkflowType.STAR, use_llm_cache=use_llm_cache)


def handle_resume(use_llm_cache: bool = True):
    """Process and enhance a resume document."""
    log = get_logger("MainHandler")
    log.info("Resume workflow requested")
    WorkflowFactory.run_workflow(WorkflowType.RESUME, use_llm_cache=use_llm_cache)
