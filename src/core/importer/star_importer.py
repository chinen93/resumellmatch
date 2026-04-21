import os
from typing import List

from src.core.processor.star_processor import StarEntryProcessor, StarMetadataProcessor
from src.data_ingestion.csv_loader import CSVLoader
from src.logging_config import get_logger

EXPECTED_STAR_METADATA_HEADER: List[str] = [
    "id"
    "user_id",
    "type",
    "title",
    "subtitle",
    "location",
    "start_date",
    "end_date",
]

EXPECTED_STAR_ENTRY_HEADER: List[str] = [
    "id"
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
            id=values["id"],
            user_id=values["user_id"],
            type=values["type"],
            title=values["title"],
            subtitle=values["subtitle"],
            location=values["location"],
            start_date=values["start_date"],
            end_date=values["end_date"],
        )

    def run(self, filename: str) -> List[str]:
        ret: List[str] = []
        filepath = os.path.join("input", filename)

        try:
            self.loader.load_csv(
                filepath, EXPECTED_STAR_METADATA_HEADER, self.importer_function
            )
        except FileNotFoundError:
            self._log.info(f"File not found '{filepath}'")
        except ValueError:
            self._log.info(f"File '{filepath}' has unexpected headers")

        return ret


class StarEntryImporter:
    loader: CSVLoader
    processor: StarEntryProcessor

    def __init__(self, loader: CSVLoader, processor: StarEntryProcessor):
        self.loader = loader
        self.processor = processor
        self._log = get_logger("StarEntryImporter")

    def importer_function(self, values: dict[str, str]) -> None:
        # Accept both capitalized and lowercase CSV headers
        metadata_id = (
            values.get("Star_metadata_id")
            or values.get("star_metadata_id")
            or values.get("StarMetadata_id")
            or values.get("starMetadata_id")
            or values.get("star_metadata")
            or values.get("metadata_id")
        )
        title = values.get("Title") or values.get("title")
        situation = values.get("Situation") or values.get("situation")
        task = values.get("Task") or values.get("task")
        action = values.get("Action") or values.get("action")
        result = values.get("Result") or values.get("result")

        self.processor.new_item(
            metadata_id=metadata_id,
            title=title,
            situation=situation,
            task=task,
            action=action,
            result=result,
        )

    def run(self, filename: str) -> List[str]:
        ret: List[str] = []
        filepath = os.path.join("input", filename)

        try:
            self.loader.load_csv(
                filepath, EXPECTED_STAR_ENTRY_HEADER, self.importer_function
            )
        except FileNotFoundError:
            self._log.info(f"File not found '{filepath}'")
        except ValueError:
            self._log.info(f"File '{filepath}' has unexpected headers")

        return ret
