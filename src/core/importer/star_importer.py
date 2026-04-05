from typing import List

from src.core.processor.star_processor import StarMetadataProcessor
from src.data_ingestion.csv_loader import CSVLoader

EXPECTED_STAR_METADATA_HEADER: List[str] = [
    "User_id",
    "Type",
    "Title",
    "Subtitle",
    "Location",
    "Start_date",
    "End_date",
]

EXPECTED_STAR_ENTRY_HEADER: List[str] = [
    "Star_metadata_id",
    "Title",
    "Situation",
    "Task",
    "Action",
    "Result",
]


class StarMetadataImporter:

    loader: CSVLoader
    processor: StarMetadataProcessor

    def __init__(self, loader: CSVLoader, processor: StarMetadataProcessor):
        self.loader = loader
        self.processor = processor

    def importer_function(self, values: dict[str, str]) -> None:
        # Validate that the fields are not empty
        self.processor.new_item(
            user_id=values["User_id"],
            type=values["Type"],
            title=values["Title"],
            subtitle=values["Subtitle"],
            location=values["location"],
            start_date=values["start_date"],
            end_date=values["end_date"],
        )

    def run(self, filepath: str) -> List[str]:
        ret: List[str] = []

        try:
            self.loader.load_csv(
                filepath, EXPECTED_STAR_METADATA_HEADER, self.importer_function
            )
        except FileNotFoundError:
            pass
        except ValueError:
            pass

        return ret


class StarEntryImporter:
    pass
