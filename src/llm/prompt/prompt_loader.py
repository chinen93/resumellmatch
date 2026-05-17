"""Prompt template loader for the LLM workflow.

This module defines a loader that reads prompt template files from the
`src/llm/prompt` directory and returns their contents for use in prompt
execution services.
"""

from pathlib import Path
from typing import Optional

from config.logging import get_logger


class PromptLoader:
    """A utility class responsible for loading prompt templates.

    It manages the loading of prompt files from the filesystem and provides
    them as strings for the LLM prompt service.
    """

    def __init__(self):
        """Initialize the prompt loader.

        Sets the prompt directory path and prepares a logger for error handling.
        """
        self.prompt_dir = Path(__file__).parent.parent / "prompt" / "text"
        self._log = get_logger("PromptLoader")

    def load(self, folder: str, filename: str) -> Optional[str]:
        """Load the content of a prompt file.

        Args:
            filename: Name of the prompt file to load.

        Returns:
            The prompt file contents as a string, or None if the file could not
            be found or an error occurred while reading it.
        """
        if folder != "":
            filepath = self.prompt_dir / folder / filename
        else:
            filepath = self.prompt_dir / filename

        try:
            with open(filepath, "r") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            self._log.error(f"Error: File not found at {filepath}")
            return None
        except Exception as e:
            self._log.error(f"An error occurred while loading {filename}: {e}")
            return None
