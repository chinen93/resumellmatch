"""Workflow factory for creating and running workflows.

This module provides a factory pattern for workflow execution, allowing
dynamic selection and execution of different workflow types via an enum.
"""

from enum import Enum

from src.core.orchestrator.workflows import job_workflow, resume_workflow, star_workflow


class WorkflowType(Enum):
    """Enumeration of available workflow types.

    Provides type-safe workflow selection with string values matching
    command-line flags.
    """

    JOB = "job"
    STAR = "star"
    RESUME = "resume"


class WorkflowFactory:
    """Factory for creating and executing workflows.

    Provides a centralized way to run different types of workflows
    based on a WorkflowType enum value.
    """

    _WORKFLOW_MAP = {
        WorkflowType.JOB: job_workflow.run_job_workflow,
        WorkflowType.STAR: star_workflow.run_star_workflow,
        WorkflowType.RESUME: resume_workflow.run_resume_workflow,
    }

    @classmethod
    def run_workflow(cls, workflow_type) -> None:
        """Run the specified workflow type.

        Args:
            workflow_type: The type of workflow to run. Can be a WorkflowType enum
                or a string matching the enum value ('job', 'star', or 'resume').

        Raises:
            ValueError: If the workflow type is not recognized.
        """
        # Support both enum and string input for backward compatibility
        if isinstance(workflow_type, str):
            try:
                workflow_type = WorkflowType(workflow_type)
            except ValueError:
                raise ValueError(f"Unknown workflow type: {workflow_type}")

        workflow_func = cls._WORKFLOW_MAP.get(workflow_type)
        if workflow_func is None:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        workflow_func()
