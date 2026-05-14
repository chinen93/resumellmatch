"""STAR entry processing module.

Handles validation and persistence of STAR (Situation, Task, Action, Result)
metadata and individual entry records from CSV imports.
"""

from datetime import date, datetime
from typing import Optional

from config.logging import get_logger
from src.storage.repositories import StarEntryRepo, StarMetadataRepo


class StarMetadataProcessor:
    """Process and persist STAR metadata.

    Validates and persists STAR metadata (experience context) records
    from CSV imports into the database.

    Attributes:
        repo: Repository for StarMetadata entities.
    """

    def __init__(self, isTest: bool = True):
        self.repo = StarMetadataRepo(isTest)
        self._log = get_logger("StarMetadataProcessor")

    def _parse_date(self, value: Optional[str]) -> date:
        """Parse date from various formats.

        Accepts year-only format (YYYY) or full ISO date format (YYYY-MM-DD).
        Returns today's date if parsing fails or value is empty.

        Args:
            value: Date string in YYYY or YYYY-MM-DD format.

        Returns:
            Parsed date or today's date if parsing fails.
        """
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
        """Create and persist a new STAR metadata record.

        Args:
            id: Unique identifier.
            user_id: Associated user ID.
            type: Experience type (e.g., 'work', 'education', 'project').
            title: Title of the position/program/project.
            subtitle: Additional context (e.g., company name).
            location: Geographic location.
            start_date: Start date (year or full date).
            end_date: End date (year or full date).
        """
        self._log.debug(
            f"Processing STAR metadata: id={id}, title='{title}', type='{type}'"
        )
        try:
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
            self._log.debug(f"Successfully created STAR metadata record: {id}")
        except Exception as e:
            self._log.error(f"Failed to create STAR metadata record {id}: {e}")
            raise


class StarEntryProcessor:
    """Process and persist individual STAR entries.

    Validates and persists individual STAR story entries
    from CSV imports into the database.

    Attributes:
        repo: Repository for StarEntry entities.
    """

    def __init__(self, isTest: bool = True):
        self.repo = StarEntryRepo(isTest)
        self._log = get_logger("StarEntryProcessor")

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
        """Create and persist a new STAR entry record.

        Args:
            id: Unique identifier.
            metadata_id: Foreign key to parent STAR metadata.
            title: Title of the STAR story.
            situation: The situation or context.
            task: The task or responsibility.
            action: The action taken.
            result: The result or outcome.
        """
        self._log.debug(
            f"Processing STAR entry: id={id}, metadata_id={metadata_id}, title='{title}'"
        )
        try:
            self.repo.create_from_fields(
                id=id,
                metadata_id=metadata_id,
                title=title,
                situation=situation,
                task=task,
                action=action,
                result=result,
            )
            self._log.debug(f"Successfully created STAR entry record: {id}")
        except Exception as e:
            self._log.error(f"Failed to create STAR entry record {id}: {e}")
            raise
