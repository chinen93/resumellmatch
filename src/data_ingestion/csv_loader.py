"""CSV file loading and parsing utilities.

Provides functionality to load and validate CSV files with optional callbacks
for processing each row.
"""

import csv
from typing import Callable, List, Optional, Sequence

from config.logging import get_logger
from src.data_ingestion.utils import get_filepath


class CSVLoader:
    """Loads and parses CSV files with header validation and row callbacks.

    Handles file reading, header validation, and optional per-row processing
    through callback functions.

    Attributes:
        linesRead: Count of data rows processed in the most recent load_csv call.
    """

    linesRead: int = 0

    def __init__(self):
        self._log = get_logger("CSVLoader")

    def load_csv(
        self,
        filename: str,
        expected_header: List[str],
        callback: Optional[Callable[[dict[str, str]], None]] = None,
    ) -> None:
        """Load and parse CSV file with optional row-by-row callback processing.

        Loads the CSV file, validates headers against expected format, and
        optionally calls a callback function for each data row.

        Args:
            filename: Name of the CSV file to load.
            expected_header: List of expected column names to validate against.
            callback: Optional function to call for each row with row data as dict.

        Raises:
            FileNotFoundError: If the CSV file doesn't exist.
            ValueError: If the CSV file is empty or has no data rows.
        """
        self.linesRead = 0
        filepath = get_filepath(filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    raise ValueError(f"CSV file is empty: {filepath}")

                self.validateHeader(filepath, reader.fieldnames, expected_header)

                for row in reader:
                    self.linesRead += 1

                    if callback is not None:
                        self._log.debug(f"{self.linesRead}: {callback}")
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
        self, filepath: str, headers: Sequence[str], expected_headers: List[str]
    ) -> None:
        """Validate CSV headers match expected headers.

        Checks that the CSV file contains the expected column headers.

        Args:
            filepath: Path to the CSV file being validated.
            headers: The actual headers found in the CSV file.
            expected_headers: List of expected column names.

        Raises:
            ValueError: If headers don't match expected headers.
        """
        missed = []
        for header in expected_headers:
            if header not in headers:
                missed.append(header)

        if len(missed) > 0:
            raise ValueError(
                f"CSV file header incorrect: {filepath}, missing: '{";".join(missed)}'"
            )
