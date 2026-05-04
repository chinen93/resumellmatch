from datetime import date, datetime
from typing import Optional

from src.storage.repositories import StarEntryRepo, StarMetadataRepo

# from src.storage.models import StarEntry, StarMetadata


class StarMetadataProcessor:
    """Handle creating StarMetadata objects and persisting them via repo."""

    def __init__(self, isTest: bool = True):
        self.repo = StarMetadataRepo(isTest)

    def _parse_date(self, value: Optional[str]) -> date:
        if value is None or str(value).strip() == "":
            return date.today()

        s = str(value).strip()
        # Accept year-only like '2015' or full ISO date 'YYYY-MM-DD'
        try:
            if len(s) == 4 and s.isdigit():
                return date(int(s), 1, 1)
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return date.today()

    def new_item(
        self, id, user_id, type, title, subtitle, location, start_date, end_date
    ) -> None:
        self.repo.create_from_fields(
            id=id,
            user_id=user_id,
            type=type,
            title=title,
            subtitle=subtitle,
            location=location,
            start_date=self._parse_date(start_date),
            end_date=self._parse_date(end_date),
        )


class StarEntryProcessor:
    """Handle creating StarEntry objects and persisting them via repo."""

    def __init__(self, isTest: bool = True):
        self.repo = StarEntryRepo(isTest)

    def new_item(
        self,
        id,
        metadata_id,
        title,
        situation,
        task,
        action,
        result,
    ) -> None:

        self.repo.create_from_fields(
            id=id,
            metadata_id=metadata_id,
            title=title,
            situation=situation,
            task=task,
            action=action,
            result=result,
        )
