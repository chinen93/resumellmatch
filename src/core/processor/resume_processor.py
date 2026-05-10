from typing import Optional

from src.llm.client import OllamaLocalClient
from src.storage.repositories import ResumeRepo


class ResumeProcessor:
    """Handle creating Resume objects and persisting them via repo."""

    def __init__(self, llm_client: OllamaLocalClient, isTest: bool = True):
        self.llm_client = llm_client
        self.resume_repo = ResumeRepo(isTest)

    def new_item(self, resume: str, input_hash: str) -> Optional[str]:
        resume_parsed = self.llm_client.extract_resume_keywords(resume)

        if resume_parsed is not None:
            self._persist_resume(resume, input_hash, resume_parsed)

        return resume_parsed

    def exist_resume(self, input_hash: str) -> Optional[str]:
        existing = self.resume_repo.get_by_input_hash(input_hash)
        if existing:
            return str(existing.raw_text)

        return None

    def _persist_resume(self, resume: str, input_hash: str, resume_parsed: str) -> None:
        try:
            self.resume_repo.create_from_fields(
                id=None,
                user_id=1,
                raw_text=resume,
                input_hash=input_hash,
                full_text=resume_parsed,
            )
        except Exception:
            pass
