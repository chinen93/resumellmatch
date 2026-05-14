"""Base orchestration classes for workflow management.

This module provides base classes and utilities for orchestrating application
workflows, reducing duplication in importer-processor-repository patterns.
"""

from typing import Type

from src.core.orchestrator.workflows.handler import Handler


class WorkflowOrchestrator:
    """Base class for orchestrating common workflow patterns.

    Provides a unified interface for running workflows that follow the
    importer → processor → repository pattern.

    Args:
        handler: Handler instance providing LLM and other services.
    """

    def __init__(self, handler: Handler):
        self.handler = handler

    def run_simple_workflow(
        self,
        importer_class: Type,
        processor_class: Type,
        filename: str,
        *args,
        **kwargs
    ):
        """Run a simple workflow with importer and processor.

        Creates a processor instance with the handler's prompt service,
        creates an importer with the processor, and runs the import.

        Args:
            importer_class: The importer class to instantiate.
            processor_class: The processor class to instantiate.
            filename: Filename to pass to the importer's run method.
            *args: Additional positional args for processor constructor.
            **kwargs: Additional keyword args for processor constructor.

        Returns:
            Result of the importer's run method.
        """
        processor = processor_class(self.handler.prompt_service, *args, **kwargs)
        importer = importer_class(processor)
        return importer.run(filename)
