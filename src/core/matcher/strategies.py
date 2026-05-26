import json
import re
from typing import Optional

from config.logging import get_logger
from src.llm.prompt.services.LLMMatchService import LLMMatchService


class LLMJobStarMatcher:
    """LLM-based matcher for job descriptions and STAR entries."""

    def __init__(self, prompt_service: LLMMatchService):
        self._log = get_logger("LLMJobStarMatcher")
        self.prompt_service = prompt_service

    def _parse_match_response(self, match_job_star: str) -> dict:
        try:
            return json.loads(match_job_star)
        except json.JSONDecodeError:
            self._log.warning("Unable to parse STAR match response as JSON")
            return {}

    def score(self, job_parsed: str, entry_text: str) -> Optional[int]:
        """Use the LLM to score a job/STAR match.

        Returns:
            The integer score from the LLM response, or None if unavailable.
        """
        match_job_star = self.prompt_service.match_job_with_star(job_parsed, entry_text)
        if match_job_star is None:
            self._log.debug("STAR entry match call failed or returned no response")
            return None

        match_response = self._parse_match_response(match_job_star)
        score = match_response.get("score")
        if isinstance(score, int):
            return score

        self._log.warning("LLM match response did not contain a valid integer score")
        return None


# TODO: Improve string matcher, as  just looking for the word is not enough
class StringJobStarMatcher:
    """Compute string similarity between job descriptions and STAR texts."""

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"\w+", text.lower()))

    def score(self, job_parsed: str, entry_text: str) -> int:
        """Return a heuristic similarity score from 0 to 10."""
        job_tokens = self._tokenize(job_parsed)
        entry_tokens = self._tokenize(entry_text)
        if not job_tokens or not entry_tokens:
            return 0

        intersect = job_tokens.intersection(entry_tokens)
        ratio = len(intersect) / max(len(job_tokens), len(entry_tokens))
        return min(10, int(round(ratio * 10)))
