from pathlib import Path
from typing import List, Optional

from ollama import generate
from pydantic import BaseModel


class OutputResponse(BaseModel):
    name: str
    content_text: List[str]


PROMPT_HELLO_WORLD = "hello_world.txt"
PROMPT_EXTRACT_KEYWORDS = "extract_keywords.txt"


class OllamaLocalClient:

    def _generate(self, message: str) -> str:
        # print(message)

        output = generate(
            model="gemma3:1b",  # Faster
            # model="gemma3:4b", # Slower
            prompt=message,
            # format=OutputResponse.model_json_schema(),
            options={"temperature": 0},
        )

        total_duration = int(output["total_duration"]) / 1_000_000_000
        load_duration = int(output["load_duration"]) / 1_000_000_000
        prompt_eval_duration = int(output["prompt_eval_duration"]) / 1_000_000_000
        eval_duration = int(output["eval_duration"]) / 1_000_000_000

        prompt_eval_count = int(output["prompt_eval_count"])
        eval_count = int(output["eval_count"])

        if load_duration > total_duration:
            print("Loading Model could be bottleneck")

        if prompt_eval_duration > total_duration:
            print("Prompt overly complex and require further refinement")

        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Load Duration: {load_duration:.2f}s")
        print(f"Prompt Eval Duration: {prompt_eval_duration:.2f}s")
        print(f"Eval Duration: {eval_duration:.2f}s")
        print(f"Prompt Eval Count: {prompt_eval_count}")
        print(f"Eval Count: {eval_count}")

        response = output["response"]
        return response

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
        message = self._get_prompt(PROMPT_HELLO_WORLD)

        if message is not None:
            content = self._generate(message)
            print(content)

    def extract_keywords(self, text: str) -> List[str]:
        ret: List[str] = []
        message = self._get_prompt(PROMPT_EXTRACT_KEYWORDS)

        if message is not None:
            content = self._generate(message.format(text=text))
            print(content)

        return ret
