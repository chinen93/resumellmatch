import json
from typing import Optional

from config.logging import get_logger
from config.settings import get_settings
from src.core.matcher.strategies import LLMJobStarMatcher, StringJobStarMatcher
from src.llm.prompt.services.LLMMatchService import LLMMatchService


class MatchScoreCombiner:
    """Combine multiple match scores into a unified score."""

    def __init__(self, prompt_service: LLMMatchService):
        self._log = get_logger("MatchScoreCombiner")

        self._settings = get_settings()
        self.threshold = self._settings.MATCH_THRESHOLD
        self.llm_weight = self._settings.LLM_WEIGHT
        self.text_weight = self._settings.TEXT_WEIGHT

        self._llm_matcher = LLMJobStarMatcher(prompt_service)
        self._text_matcher = StringJobStarMatcher()

    def combine(self, llm_score: Optional[int], string_score: int) -> float:
        """Combine LLM and string similarity scores into a single float."""
        if llm_score is None:
            llm_score = 0

        assert llm_score >= 0 and llm_score <= 10, "LLM score should be between 0 - 10"
        assert (
            string_score >= 0 and string_score <= 10
        ), "String score should be between 0 - 10"

        return llm_score * self.llm_weight + string_score * self.text_weight

    def above_threshold(self, job_parsed: str, entry_text: str) -> bool:
        llm_score = self._llm_matcher.score(job_parsed, entry_text)
        string_score = self._text_matcher.score(job_parsed, entry_text)
        combined_score = self.combine(llm_score, string_score)

        is_above = False

        if combined_score > self._settings.MATCH_THRESHOLD:
            self._log.info("STAR entry matched with job description")
            self._log.debug(
                f"LLM score={llm_score:.2f}, "
                f"string score={string_score:.2f}, "
                f"combined score={combined_score:.2f} "
                f"threshold score={self._settings.MATCH_THRESHOLD:.2f}"
            )
            is_above = True
        else:
            self._log.debug(
                f"STAR entry did not meet threshold: combined score={combined_score:.2f}, "
                f"threshold score={self._settings.MATCH_THRESHOLD:.2f}, "
                f"LLM score={llm_score:.2f}, "
                f"string score={string_score:.2f}"
            )

        self._log.debug(json.dumps({"job": job_parsed, "star": entry_text}))
        return is_above
