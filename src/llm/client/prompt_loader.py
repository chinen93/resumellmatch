from pathlib import Path
from typing import Optional

from src.logging_config import get_logger


class PromptLoader:
    """Handles loading of prompt files from the prompt directory."""

    def __init__(self):
        self.prompt_dir = Path(__file__).parent.parent / "prompt"
        self._log = get_logger("PromptLoader")

    def load(self, filename: str) -> Optional[str]:
        """Load the content of a prompt file."""
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
