"""STAR entry import module.

Handles importing STAR (Situation, Task, Action, Result) interview response data
from CSV files. Supports both STAR metadata (experience context) and individual
STAR entries (stories).
"""

from typing import List

from config.logging import get_logger
from src.core.processor.star_processor import StarEntryProcessor, StarMetadataProcessor
from src.data_ingestion.csv_loader import CSVLoader

EXPECTED_STAR_METADATA_HEADER: List[str] = [
    "id",
    "user_id",
    "type",
    "title",
    "subtitle",
    "location",
    "start_date",
    "end_date",
]

EXPECTED_STAR_ENTRY_HEADER: List[str] = [
    "id",
    "star_metadata_id",
    "title",
    "situation",
    "task",
    "action",
    "result",
]


class StarMetadataImporter:
    """Imports STAR metadata from CSV files.

    Loads STAR metadata (work/education/project experience context) from CSV files
    and processes each row through the StarMetadataProcessor.

    Attributes:
        loader: CSVLoader instance for CSV file operations.
        processor: StarMetadataProcessor instance for processing metadata.
        _log: Logger instance.
    """

    loader: CSVLoader
    processor: StarMetadataProcessor

    def __init__(self, loader: CSVLoader, processor: StarMetadataProcessor):
        self.loader = loader
        self.processor = processor
        self._log = get_logger("StarMetadataImporter")

    def importer_function(self, values: dict[str, str]) -> None:
        """Process a single STAR metadata row from CSV.

        Called as a callback for each row in the CSV file.
        Passes the parsed values to the processor for validation and storage.

        Args:
            values: Dictionary mapping column headers to values from a CSV row.
        """
        # Validate that the fields are not empty
        self.processor.new_item(
            id=values[EXPECTED_STAR_METADATA_HEADER[0]],
            user_id=values[EXPECTED_STAR_METADATA_HEADER[1]],
            type=values[EXPECTED_STAR_METADATA_HEADER[2]],
            title=values[EXPECTED_STAR_METADATA_HEADER[3]],
            subtitle=values[EXPECTED_STAR_METADATA_HEADER[4]],
            location=values[EXPECTED_STAR_METADATA_HEADER[5]],
            start_date=values[EXPECTED_STAR_METADATA_HEADER[6]],
            end_date=values[EXPECTED_STAR_METADATA_HEADER[7]],
        )

    def run(self, filename: str) -> List[str]:
        """Import STAR metadata from a CSV file.

        Loads and processes all STAR metadata records from the specified CSV file.
        Handles file not found and validation errors gracefully with logging.

        Args:
            filename: Name of the CSV file containing STAR metadata.

        Returns:
            List of error messages (empty list if successful).
        """
        self._log.info(f"Starting STAR metadata import from file: {filename}")

        ret: List[str] = []
        try:
            self.loader.load_csv(
                filename, EXPECTED_STAR_METADATA_HEADER, self.importer_function
            )
            self._log.info("STAR metadata import completed successfully")
        except FileNotFoundError as e:
            self._log.error(f"STAR metadata file not found: {e}")
        except ValueError as e:
            self._log.error(f"STAR metadata validation error: {e}")
        except Exception as e:
            self._log.error(f"Unexpected error during STAR metadata import: {e}")

        if ret:
            self._log.warning(f"STAR metadata import completed with {len(ret)} errors")
        else:
            self._log.info("STAR metadata import c  gompleted without errors")

        return ret


class StarEntryImporter:
    """Imports STAR entries from CSV files.

    Loads individual STAR (Situation, Task, Action, Result) stories from
    CSV files and processes each row through the StarEntryProcessor.

    Attributes:
        loader: CSVLoader instance for CSV file operations.
        processor: StarEntryProcessor instance for processing entries.
        _log: Logger instance.
    """

    loader: CSVLoader
    processor: StarEntryProcessor

    def __init__(self, loader: CSVLoader, processor: StarEntryProcessor):
        self.loader = loader
        self.processor = processor
        self._log = get_logger("StarEntryImporter")

    def importer_function(self, values: dict[str, str]) -> None:
        """Process a single STAR entry row from CSV.

        Called as a callback for each row in the CSV file.
        Passes the parsed values to the processor for validation and storage.

        Args:
            values: Dictionary mapping column headers to values from a CSV row.
        """
        self.processor.new_item(
            id=values[EXPECTED_STAR_ENTRY_HEADER[0]],
            metadata_id=values[EXPECTED_STAR_ENTRY_HEADER[1]],
            title=values[EXPECTED_STAR_ENTRY_HEADER[2]],
            situation=values[EXPECTED_STAR_ENTRY_HEADER[3]],
            task=values[EXPECTED_STAR_ENTRY_HEADER[4]],
            action=values[EXPECTED_STAR_ENTRY_HEADER[5]],
            result=values[EXPECTED_STAR_ENTRY_HEADER[6]],
        )

    def run(self, filename: str) -> List[str]:
        """Import STAR entries from a CSV file.

        Loads and processes all STAR entry records from the specified CSV file.
        Handles file not found and validation errors gracefully with logging.

        Args:
            filename: Name of the CSV file containing STAR entries.

        Returns:
            List of error messages (empty list if successful).
        """
        self._log.info(f"Starting STAR entries import from file: {filename}")

        ret: List[str] = []
        try:
            self.loader.load_csv(
                filename, EXPECTED_STAR_ENTRY_HEADER, self.importer_function
            )
            self._log.info("STAR entries import completed successfully")
        except FileNotFoundError as e:
            self._log.error(f"STAR entries file not found: {e}")
        except ValueError as e:
            self._log.error(f"STAR entries validation error: {e}")
        except Exception as e:
            self._log.error(f"Unexpected error during STAR entries import: {e}")

        if ret:
            self._log.warning(f"STAR entries import completed with {len(ret)} errors")
        else:
            self._log.info("STAR entries import completed without errors")

        return ret
