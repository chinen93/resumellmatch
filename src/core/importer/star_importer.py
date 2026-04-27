from typing import List

from src.core.processor.star_processor import StarEntryProcessor, StarMetadataProcessor
from src.data_ingestion.csv_loader import CSVLoader
from src.logging_config import get_logger

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

    loader: CSVLoader
    processor: StarMetadataProcessor

    def __init__(self, loader: CSVLoader, processor: StarMetadataProcessor):
        self.loader = loader
        self.processor = processor
        self._log = get_logger("StarMetadataImporter")

    def importer_function(self, values: dict[str, str]) -> None:
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
        self._log.info("Reading Star Metadata")

        ret: List[str] = []
        try:
            self.loader.load_csv(
                filename, EXPECTED_STAR_METADATA_HEADER, self.importer_function
            )
        except FileNotFoundError as e:
            self._log.error(e)
        except ValueError as e:
            self._log.error(e)

        return ret


class StarEntryImporter:
    loader: CSVLoader
    processor: StarEntryProcessor

    def __init__(self, loader: CSVLoader, processor: StarEntryProcessor):
        self.loader = loader
        self.processor = processor
        self._log = get_logger("StarEntryImporter")

    def importer_function(self, values: dict[str, str]) -> None:
        self.processor.new_item(
            metadata_id=values[EXPECTED_STAR_ENTRY_HEADER[0]],
            title=values[EXPECTED_STAR_ENTRY_HEADER[1]],
            situation=values[EXPECTED_STAR_ENTRY_HEADER[2]],
            task=values[EXPECTED_STAR_ENTRY_HEADER[3]],
            action=values[EXPECTED_STAR_ENTRY_HEADER[4]],
            result=values[EXPECTED_STAR_ENTRY_HEADER[5]],
        )

    def run(self, filename: str) -> List[str]:
        self._log.info("Reading Star Entries")
        ret: List[str] = []

        try:
            self.loader.load_csv(
                filename, EXPECTED_STAR_ENTRY_HEADER, self.importer_function
            )
        except FileNotFoundError as e:
            self._log.error(e)
        except ValueError as e:
            self._log.error(e)

        return ret
