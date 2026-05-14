"""Main application entry point for core workflows.

This module serves as the entry point for the application's core workflows.
It delegates to the workflow factory for executing different workflow types.
"""

from config.logging import get_logger
from src.core.orchestrator.factory import WorkflowFactory, WorkflowType


def handle_job():
    """Handle all job-related resume matching workflow."""
    log = get_logger("MainHandler")
    log.info("Job workflow requested")
    WorkflowFactory.run_workflow(WorkflowType.JOB)


def handle_star():
    """Process STAR interview response data from CSV files."""
    log = get_logger("MainHandler")
    log.info("STAR workflow requested")
    WorkflowFactory.run_workflow(WorkflowType.STAR)


def handle_resume():
    """Process and enhance a resume document."""
    log = get_logger("MainHandler")
    log.info("Resume workflow requested")
    WorkflowFactory.run_workflow(WorkflowType.RESUME)
