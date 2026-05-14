"""Orchestration layer for application workflows.

This package contains the core orchestration logic for handling job descriptions,
STAR entries, and resumes. It provides a unified interface for workflow execution
and coordinates between importers, processors, and repositories.
"""

from .factory import WorkflowFactory, WorkflowType

__all__ = ["WorkflowFactory", "WorkflowType"]
