from pathlib import Path
from typing import Optional

from ollama import generate

from src.llm.client.response import (
    BaseResponse,
    ExtractKeywordResponse,
    JobDescriptioKeywordsResponse,
    SimpleResponse,
)
from src.logging_config import get_logger

PROMPT_HELLO_WORLD = "hello_world.txt"
PROMPT_EXTRACT_RESUME_KEYWORDS = "extract_resume_keywords.txt"
PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS = "extract_job_description_keywords.txt"


class OllamaLocalClient:

    ready: bool

    def __init__(self):

        self._log = get_logger("llm")

        try:
            self._hello_world()
            self.ready = True
        except ConnectionError:
            self.ready = False

    def _generate(self, message: str, format: type[BaseResponse]) -> str:
        # print(message)

        output = generate(
            # model="gemma3:1b",  # Faster
            model="gemma3:4b",  # Slower
            prompt=message,
            format=format.model_json_schema(),
            stream=False,
            options={"temperature": 0},
        )

        total_duration = int(output["total_duration"]) / 1_000_000_000
        load_duration = int(output["load_duration"]) / 1_000_000_000
        prompt_eval_duration = int(output["prompt_eval_duration"]) / 1_000_000_000
        eval_duration = int(output["eval_duration"]) / 1_000_000_000

        prompt_eval_count = int(output["prompt_eval_count"])
        eval_count = int(output["eval_count"])

        if load_duration > total_duration:
            self._log.debug("Loading Model could be bottleneck")

        if prompt_eval_duration > total_duration:
            self._log.debug("Prompt overly complex and require further refinement")

        self._log.debug(f"Total Duration: {total_duration:.2f}s")
        self._log.debug(
            f"Load Duration: {load_duration:.2f}s (Disk > RAM; Default 5min inactive unloads model)"
        )
        self._log.debug(f"Prompt Eval Duration: {prompt_eval_duration:.2f}s")
        self._log.debug(f"Eval Duration: {eval_duration:.2f}s")
        self._log.debug(f"Prompt Eval Count: {prompt_eval_count}")
        self._log.debug(f"Eval Count: {eval_count}")

        response = output["response"]

        try:
            validate_response = format.model_validate_json(response)
        except Exception as e:
            validate_response = BaseResponse()
            self._log.error(f"Failed to parse resume keyword response: {e}")

        return validate_response.model_dump_json()

    def _generate_when_ready(
        self, message: str, format: type[BaseResponse]
    ) -> Optional[str]:

        if self.ready:
            return self._generate(message=message, format=format)

        return None

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
            self._log.error(f"Error: File not found at {filepath}")
            return None
        except Exception as e:
            self._log.error(f"An error occurred: {e}")
            return None

    def _hello_world(self) -> None:
        message = self._get_prompt(PROMPT_HELLO_WORLD)

        if message is not None:
            content = self._generate(message, SimpleResponse)
            self._log.info(content)

    # ===============================================================
    # LLM Commands
    # ===============================================================

    def extract_resume_keywords(self, text: str) -> Optional[str]:
        message = self._get_prompt(PROMPT_EXTRACT_RESUME_KEYWORDS)

        if message is not None:
            content = self._generate_when_ready(
                message.format(text=text), ExtractKeywordResponse
            )

            if content is not None:
                self._log.info(content)
                return content

        return None

    def extract_job_description_keywords(self, text: str) -> Optional[str]:
        message = self._get_prompt(PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS)

        if message is not None:
            content = self._generate_when_ready(
                message.format(text=text), JobDescriptioKeywordsResponse
            )

            if content is not None:
                self._log.info(content)
                return content

        return None
