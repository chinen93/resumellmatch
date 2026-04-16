from datetime import date, datetime
from typing import List, Optional

from src.storage.models import StarEntry, StarMetadata
from src.storage.repositories.star_repo import StarEntryRepo, StarMetadataRepo


class StarMetadataProcessor:
    """Handle creating StarMetadata objects and persisting them via repo."""

    def __init__(self, isTest: bool = True):
        self.repo = StarMetadataRepo(isTest)

    def _parse_date(self, value: Optional[str]) -> date:
        if value is None or str(value).strip() == "":
            return datetime.now().date()

        s = str(value).strip()
        # Accept year-only like '2015' or full ISO date 'YYYY-MM-DD'
        try:
            if len(s) == 4 and s.isdigit():
                return date(int(s), 1, 1)
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return datetime.now().date()

    def new_item(
        self, user_id, type, title, subtitle, location, start_date, end_date
    ) -> None:
        # create a StarMetadata instance (useful for tests that patch the model)
        _ = StarMetadata(
            user_id=user_id,
            type=type,
            title=title,
            subtitle=subtitle,
            location=location,
            start_date=start_date,
            end_date=end_date,
        )

        # persist using repository (convert types appropriately)
        try:
            u_id = (
                int(user_id)
                if user_id is not None and str(user_id).strip() != ""
                else None
            )
        except Exception:
            u_id = None

        sd = self._parse_date(start_date)
        ed = self._parse_date(end_date)

        if u_id is None:
            # repository expects an integer user id; raise to indicate bad data
            raise ValueError("user_id is required and must be an integer")

        self.repo.create(
            user_id=u_id,
            type=type,
            title=title,
            subtitle=subtitle,
            location=location,
            start_date=sd,
            end_date=ed,
        )


class StarEntryProcessor:
    """Handle creating StarEntry objects and persisting them via repo."""

    def __init__(self, isTest: bool = True):
        self.repo = StarEntryRepo(isTest)

    def new_item(
        self,
        metadata_id,
        title,
        situation,
        task,
        action,
        result,
        skills: List[int] = [],
    ) -> None:
        # create model instance (keeps parity with tests that might patch StarEntry)
        _ = StarEntry(
            metadata_id=metadata_id,
            title=title,
            situation=situation,
            task=task,
            action=action,
            result=result,
        )

        # persist using repository
        try:
            m_id = (
                int(metadata_id)
                if metadata_id is not None and str(metadata_id).strip() != ""
                else None
            )
        except Exception:
            m_id = None

        if m_id is None:
            raise ValueError("metadata_id is required and must be an integer")

        self.repo.create(
            metadata_id=m_id,
            title=title,
            situation=situation,
            task=task,
            action=action,
            result=result,
            skills=skills,
        )
