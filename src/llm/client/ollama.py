from typing import Optional

from ollama import generate

from config.settings import get_settings
from src.llm.client.cache_manager import LLMCacheManager
from src.llm.client.response import BaseResponse, SimpleResponse
from src.logging_config import get_logger
from src.utils.hash import compute_hash


class OllamaLocalClient:

    def __init__(self, cache_manager: LLMCacheManager):

        self._log = get_logger("llm")
        self.cache_manager = cache_manager

        settings = get_settings()
        assert (
            settings.AGENT_MODEL is not None
        ), "AGENT_MODEL must be set in environment variables"

        self.agent_model = settings.AGENT_MODEL

        # Check if ready (optional, for backward compatibility)
        self.ready = self._check_readiness()

    def _generate(self, message: str, format: type[BaseResponse]) -> str:

        self._log.debug(message)

        try:
            output = generate(
                model=self.agent_model,
                prompt=message,
                format=format.model_json_schema(),
                stream=False,
                options={"temperature": 0},
            )
        except Exception as e:
            self._log.error(f"Failed to generate response: {e}")
            raise RuntimeError(f"LLM generation failed: {e}") from e

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
            self._log.error(f"Failed to format generated response: {e}")
            raise ValueError(f"Invalid response format: {e}") from e

        response_json = validate_response.model_dump_json()

        return response_json

    def generate_with_cache(
        self, message: str, format: type[BaseResponse]
    ) -> Optional[str]:

        if not self.ready:
            self._log.warning("LLM client not ready")
            return None

        prompt_hash = compute_hash(message)

        # Check cache
        cached = self.cache_manager.get_cached(prompt_hash)
        if cached:
            return cached

        # Generate new response
        try:
            response_json = self._generate(message=message, format=format)
        except (RuntimeError, ValueError) as e:
            self._log.error(f"Generation failed: {e}")
            return None

        # Save to cache
        self.cache_manager.save_cache(prompt_hash, message, response_json)

        return response_json

    def _check_readiness(self) -> bool:
        """Check if the LLM is ready by attempting a simple generation."""
        try:
            # Simple test prompt
            test_message = "Hello"
            self._generate(test_message, SimpleResponse)
            return True
        except Exception:
            return False

    # ===============================================================
    # Core LLM wrapper methods
    # ===============================================================
