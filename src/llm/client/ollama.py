from pathlib import Path
from typing import Optional

from ollama import generate

from config.settings import get_settings
from src.llm.client.response import (
    BaseResponse,
    ExtractKeywordResponse,
    JobDescriptioKeywordsResponse,
    MatchJobWithStarResponse,
    RewriteStarResponse,
    SimpleResponse,
)
from src.logging_config import get_logger
from src.storage.repositories.llm_cache_repo import LLMCacheRepo
from src.utils.hash import compute_hash

PROMPT_HELLO_WORLD = "hello_world.md"
PROMPT_EXTRACT_RESUME_KEYWORDS = "extract_resume_keywords.md"
PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS = "extract_job_description_keywords.md"
PROMPT_MATCH_JOB_WITH_STAR = "match_job_with_star.md"
PROMPT_REWRITE_STAR_BULLET_POINT = "rewrite_star_bullet_point.md"


class OllamaLocalClient:

    ready: bool

    def __init__(self):

        self._log = get_logger("llm")

        settings = get_settings()
        assert (
            settings.AGENT_MODEL is not None
        ), "AGENT_MODEL must be set in environment variables"

        self.agent_model = settings.AGENT_MODEL

        try:
            self._hello_world()
            self.ready = True
        except ConnectionError:
            self.ready = False

    def _generate(self, message: str, format: type[BaseResponse]) -> str:

        self._log.debug(message)

        output = generate(
            model=self.agent_model,
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
            self._log.error(f"Failed to format generated response: {e}")

        response_json = validate_response.model_dump_json()

        return response_json

    def _generate_when_ready_with_cache(
        self, message: str, format: type[BaseResponse]
    ) -> Optional[str]:

        if not self.ready:
            return None

        # Check cache for prompt
        try:
            cache_repo = LLMCacheRepo()
            prompt_hash = compute_hash(message)
            cached = cache_repo.get_by_prompt_hash(prompt_hash)
            if cached:
                self._log.info("LLM cache hit for prompt")
                return str(cached.response_json)
        except Exception:
            # Cache failures should not block LLM calls
            pass

        response_json = self._generate(message=message, format=format)

        # Persist cache entry (best-effort)
        try:
            response_hash = compute_hash(response_json)
            cache_repo.create(
                prompt_hash=compute_hash(message),
                prompt_text=message,
                response_hash=response_hash,
                response_json=response_json,
                llm_name="ollama",
            )
        except Exception:
            # Do not fail on cache write errors
            pass

        return response_json

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

    def extract_resume_keywords(self, resume_text: str) -> Optional[str]:
        message = self._get_prompt(PROMPT_EXTRACT_RESUME_KEYWORDS)

        if message is not None:
            content = self._generate_when_ready_with_cache(
                message.format(resume_text=resume_text), ExtractKeywordResponse
            )

            if content is not None:
                self._log.info(content)
                return content

        return None

    def extract_job_description_keywords(self, job_description: str) -> Optional[str]:
        message = self._get_prompt(PROMPT_EXTRACT_JOB_DESCRIPTION_KEYWORDS)

        if message is not None:
            content = self._generate_when_ready_with_cache(
                message.format(job_description=job_description),
                JobDescriptioKeywordsResponse,
            )

            if content is not None:
                self._log.info(content)
                return content

        return None

    def match_job_with_star(self, job_parsed: str, star_text: str) -> Optional[str]:
        message = self._get_prompt(PROMPT_MATCH_JOB_WITH_STAR)

        if message is not None:
            content = self._generate_when_ready_with_cache(
                message.format(job_parsed=job_parsed, star_text=star_text),
                MatchJobWithStarResponse,
            )

            if content is not None:
                self._log.info(content)
                return content

        return None

    def rewrite_star_to_bullet_point(
        self, star_text: str, job_parsed: str, match_score: str
    ) -> Optional[str]:
        message = self._get_prompt(PROMPT_REWRITE_STAR_BULLET_POINT)

        if message is not None:
            content = self._generate_when_ready_with_cache(
                message.format(
                    star_text=star_text, job_parsed=job_parsed, match_score=match_score
                ),
                RewriteStarResponse,
            )

            if content is not None:
                self._log.info(content)
                return content

        return None
