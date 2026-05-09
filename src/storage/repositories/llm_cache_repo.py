from typing import List, Optional

from src.core.models import LLMCache as LLMCacheModel
from src.logging_config import get_logger
from src.storage.connection import DatabaseConnection
from src.storage.mappers.llm_cache_mapper import LLMCacheMapper
from src.storage.models import LLMCache


class LLMCacheRepo:
    def __init__(self, isTest=False):
        self._log = get_logger("LLMCacheRepo")
        self.db = DatabaseConnection(isTest)

    def create_or_update(self, core_model: LLMCacheModel) -> int:
        """Create or update an LLMCache from a model (checks by prompt_hash)."""

        storage_model = self._get_storage_model(core_model)

        if storage_model.id is not None:
            return self._update(storage_model, core_model)
        else:
            storage_model = LLMCacheMapper.to_storage_model(core_model)
            return self._create(storage_model)

    def create_from_fields(
        self,
        prompt_hash: str,
        prompt_text: str,
        response_hash: str,
        response_json: str,
        llm_name: str | None = None,
    ) -> int:
        """Create using individual fields (builds model internally)."""
        model = LLMCacheMapper.from_raw_fields(
            prompt_hash=prompt_hash,
            prompt_text=prompt_text,
            response_hash=response_hash,
            response_json=response_json,
            llm_name=llm_name if llm_name is not None else "",
        )
        return self.create_or_update(model)

    def get_by_id(self, cache_id: int) -> Optional[LLMCacheModel]:
        """Fetches a record and converts it immediately to the Core Model."""
        storage_model = self._retrieve(cache_id)

        if not storage_model:
            return None

        return LLMCacheMapper.to_core_model(storage_model)

    def get_by_prompt_hash(self, prompt_hash: str) -> Optional[LLMCacheModel]:
        """Fetches by prompt_hash and converts to Core Model."""
        storage_model = self._retrieve_by_prompt_hash(prompt_hash)

        if not storage_model:
            return None

        return LLMCacheMapper.to_core_model(storage_model)

    def get_all(self) -> List[LLMCacheModel]:
        """Fetches all records and converts them to the Core Model list."""
        with self.db.get_session() as session:
            storage_models = session.query(LLMCache).all()

            return [LLMCacheMapper.to_core_model(model) for model in storage_models]

    def delete(self, cache_id: int) -> bool:
        storage_model = self._retrieve(cache_id)

        if not storage_model:
            self._log.debug(f"LLMCache with id {cache_id} not found")
            return False

        try:
            self._delete(storage_model)
            return True
        except Exception:
            return False

    def _get_storage_model(self, core_model: LLMCacheModel) -> LLMCache:

        storage_model = LLMCacheMapper.to_storage_model(core_model)
        storage_model.id = None

        if core_model.id is not None:
            retrieved_storage_model = self._retrieve_by_prompt_hash(
                core_model.prompt_hash
            )
            if retrieved_storage_model is not None:
                storage_model = retrieved_storage_model

        return storage_model

    def _create(self, storage_model: LLMCache) -> int:
        """Create an LLMCache from a storage model."""
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when creating LLMCache: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _retrieve(self, cache_id: int) -> Optional[LLMCache]:
        with self.db.get_session() as session:
            return session.query(LLMCache).filter(LLMCache.id == cache_id).first()

    def _retrieve_by_prompt_hash(self, prompt_hash: str) -> Optional[LLMCache]:
        with self.db.get_session() as session:
            return (
                session.query(LLMCache)
                .filter(LLMCache.prompt_hash == prompt_hash)
                .first()
            )

    def _update(self, storage_model: LLMCache, core_model: LLMCacheModel) -> int:
        storage_model.prompt_hash = core_model.prompt_hash
        storage_model.prompt_text = core_model.prompt_text
        storage_model.response_hash = core_model.response_hash
        storage_model.response_json = core_model.response_json
        storage_model.llm_name = (
            core_model.llm_name if core_model.llm_name is not None else ""
        )

        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.add(storage_model)
                session.commit()

            except Exception as e:
                session.rollback()
                self._log.error(f"Error when updating LLMCache: {e}")
                raise e

        assert storage_model.id is not None
        return int(storage_model.id)

    def _delete(self, storage_model: LLMCache) -> bool:
        with self.db.get_session() as session:
            session.begin()
            session.expire_on_commit = False

            try:
                session.delete(storage_model)
                session.commit()
            except Exception as e:
                session.rollback()
                self._log.error(f"Error when deleting LLMCache: {e}")
                raise e

        return True
