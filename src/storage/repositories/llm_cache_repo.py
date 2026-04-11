from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.models import LLMCache


class LLMCacheRepo:
    def __init__(self, isTest=False):
        self._log = get_logger("LLMCacheRepo")
        self.db = DatabaseConnection(isTest)

    def get_by_prompt_hash(self, prompt_hash: str):
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            return (
                session.query(LLMCache)
                .filter(LLMCache.prompt_hash == prompt_hash)
                .first()
            )

    def create(
        self,
        prompt_hash: str,
        prompt_text: str,
        response_hash: str,
        response_json: str,
        llm_name: str | None = None,
    ) -> int:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                entry = LLMCache(
                    prompt_hash=prompt_hash,
                    prompt_text=prompt_text,
                    response_hash=response_hash,
                    response_json=response_json,
                    llm_name=llm_name,
                )
                session.add(entry)
                session.commit()

                result = int(entry.id)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating LLMCache entry: {e}")
                raise e

        return result
