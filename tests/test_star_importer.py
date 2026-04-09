import unittest
from unittest.mock import MagicMock

from src.core.importer.star_importer import StarMetadataImporter
from src.data_ingestion.csv_loader import CSVLoader
from tests.conf_log_test import BaseTestCase


class TestStarMetadataImporter(BaseTestCase):
    """Unit tests for StarMetadataImporter class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_loader = MagicMock(spec=CSVLoader)
        self.mock_processor = MagicMock()
        self.importer = StarMetadataImporter(self.mock_loader, self.mock_processor)

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_init(self):
        """Test initialization of StarMetadataImporter."""
        self.assertIs(self.importer.loader, self.mock_loader)
        self.assertIs(self.importer.processor, self.mock_processor)

    def test_importer_function(self):
        """Test the importer function processes values correctly."""
        values = {
            "User_id": "1",
            "Type": "work",
            "Title": "Engineer",
            "Subtitle": "Company",
            "location": "NYC",
            "start_date": "2020-01-01",
            "end_date": "2023-01-01",
        }

        self.importer.importer_function(values)

        self.mock_processor.new_item.assert_called_once_with(
            user_id="1",
            type="work",
            title="Engineer",
            subtitle="Company",
            location="NYC",
            start_date="2020-01-01",
            end_date="2023-01-01",
        )

    def test_run_success(self):
        """Test successful run of importer."""
        filepath = "test.csv"
        expected_headers = [
            "User_id",
            "Type",
            "Title",
            "Subtitle",
            "Location",
            "Start_date",
            "End_date",
        ]

        result = self.importer.run(filepath)

        self.mock_loader.load_csv.assert_called_once_with(
            filepath, expected_headers, self.importer.importer_function
        )
        self.assertEqual(result, [])

    def test_run_file_not_found(self):
        """Test run when file is not found."""
        self.mock_loader.load_csv.side_effect = FileNotFoundError()

        result = self.importer.run("nonexistent.csv")

        self.assertEqual(result, [])

    def test_run_value_error(self):
        """Test run when ValueError occurs."""
        self.mock_loader.load_csv.side_effect = ValueError()

        result = self.importer.run("invalid.csv")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
