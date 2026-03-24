import os
import tempfile
import unittest
from typing import List

from src.data_ingestion.csv_loader import CSVLoader


class TestCSVLoader(unittest.TestCase):
    """Unit tests for CSVLoader class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.loader = CSVLoader()

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_load_csv_valid_file(self):
        """Test loading a valid CSV file."""
        csv_content = "name,age,city\nJohn,25,NYC\nJane,30,LA\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            self.loader.load_csv(temp_file, ["name", "age", "city"])
            expected_lines = [
                {"name": "John", "age": "25", "city": "NYC"},
                {"age": "30", "city": "LA", "name": "Jane"},
            ]
            self.assertEqual(self.loader.linesRead, len(expected_lines))
        finally:
            os.unlink(temp_file)

    def test_load_csv_valid_file_with_function(self):
        """Test loading a valid CSV file."""
        csv_content = "name,age,city\nJohn,25,NYC\nJane,30,LA\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_file = f.name

        # Function callback to be used
        ret = []

        def csv_function(line: dict[str]) -> None:
            value: List[str] = [line["name"], line["age"], line["city"]]
            ret.append(value)

        try:
            self.loader.load_csv(temp_file, ["name", "age", "city"], csv_function)
            expected_lines = [["John", "25", "NYC"], ["Jane", "30", "LA"]]
            self.assertEqual(ret, expected_lines)
        finally:
            os.unlink(temp_file)

    def test_load_csv_empty_file(self):
        """Test loading an empty CSV file raises ValueError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("")
            temp_file = f.name

        try:
            with self.assertRaises(ValueError) as context:
                self.loader.load_csv(temp_file, ["name", "age", "city"])
            self.assertIn("CSV file is empty", str(context.exception))
        finally:
            os.unlink(temp_file)

    def test_load_csv_no_data_rows(self):
        """Test loading CSV with only headers raises ValueError."""
        csv_content = "name,age,city\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            with self.assertRaises(ValueError) as context:
                self.loader.load_csv(temp_file, ["name", "age", "city"])
            self.assertIn("CSV file has no data rows", str(context.exception))
        finally:
            os.unlink(temp_file)

    def test_load_csv_file_not_found(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError) as context:
            self.loader.load_csv("non_existent_file.csv", ["name", "age", "city"])
        self.assertIn("CSV file not found", str(context.exception))

    def test_validate_csv_correct_headers(self):
        """Test validating CSV with correct headers."""
        csv_content = "name,age,city\nJohn,25,NYC\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            self.loader.load_csv(temp_file, ["name", "age", "city"])
        finally:
            os.unlink(temp_file)

    def test_validate_csv_incorrect_headers(self):
        """Test validating CSV with incorrect headers."""
        csv_content = "name,age,city\nJohn,25,NYC\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            with self.assertRaises(ValueError):
                self.loader.load_csv(temp_file, ["aaaaaa"])
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()
