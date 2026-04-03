from pathlib import Path
from typing import List, Optional

from ollama import generate
from pydantic import BaseModel


class OutputResponse(BaseModel):
    name: str
    content_text: List[str]


class OllamaClient:

    def _generate(self, message: str) -> str:
        output = generate(
            model="gemma3:1b",
            prompt=message,
            # format=OutputResponse.model_json_schema(),
            options={"temperature": 0},
        )

        content = output["response"]
        return content

    def _get_filepath(self, filename: str) -> Path:
        filepath = Path(__file__).parent.parent / "prompt" / filename
        return filepath

    def _get_prompt(self, filename: str) -> Optional[str]:
        filepath = self._get_filepath(filename)

        try:
            with open(filepath, "r") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def hello_world(self) -> None:
        message = self._get_prompt("hello_world.txt")

        if message is not None:
            content = self._generate(message)
            print(content)
