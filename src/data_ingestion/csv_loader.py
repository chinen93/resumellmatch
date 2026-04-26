import csv
from typing import Callable, List, Optional, Sequence

from src.data_ingestion.utils import get_filepath


class CSVLoader:
    """
    Loads and parses CSV files into structured data.
    Handles file reading, parsing, and header validation.
    """

    linesRead: int = 0

    def load_csv(
        self,
        filename: str,
        expected_header: List[str],
        callback: Optional[Callable[[dict[str, str]], None]] = None,
    ) -> None:
        """
        Load and parse CSV file into a list of dictionaries.
        validate that the csv has the expected format using the header as reference

        for each line call callback function if it exists

        Args:
            filepath: Path to the CSV file

        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If the CSV file is empty
        """
        self.linesRead = 0
        filepath = get_filepath(filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    raise ValueError(f"CSV file is empty: {filepath}")

                if not self.validateHeader(reader.fieldnames, expected_header):
                    raise ValueError(f"CSV file header incorrect: {filepath}")

                for row in reader:
                    self.linesRead += 1

                    if callback is not None:
                        callback(row)

                if self.linesRead == 0:
                    raise ValueError(f"CSV file has no data rows: {filepath}")

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    def validateHeader(
        self, headers: Sequence[str], expected_headers: List[str]
    ) -> bool:
        """
        Validate the CSV headers with the expected header.
        Uses self.lines after load_csv to validate its accuracy.

        Args:
            expected_header: List of expected column names

        Returns:
            True if headers match, False otherwise
        """
        # TODO: raise exception with the list of missing headers so it is easier to fix after seeing the logs
        for header in expected_headers:
            if header not in headers:
                return False

        return True
