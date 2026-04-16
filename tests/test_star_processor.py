import unittest

from src.core.processor.star_processor import StarMetadataProcessor
from tests.conf_log_test import BaseTestCase

# from unittest.mock import patch


class TestStarMetadataProcessor(BaseTestCase):
    """Unit tests for StarMetadataProcessor class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = StarMetadataProcessor(isTest=True)

    def tearDown(self):
        """Clean up after each test method."""
        pass

    # @patch("src.core.processor.star_processor.StarMetadata")
    # def test_new_item(self, mock_star_metadata):
    #     """Test creating a new StarMetadata item."""
    #     self.processor.new_item(
    #         user_id=1,
    #         type="work",
    #         title="Software Engineer",
    #         subtitle="Tech Company",
    #         location="New York",
    #         start_date="2020-01-01",
    #         end_date="2023-01-01",
    #     )

    #     mock_star_metadata.assert_called_once_with(
    #         user_id=1,
    #         type="work",
    #         title="Software Engineer",
    #         subtitle="Tech Company",
    #         location="New York",
    #         start_date="2020-01-01",
    #         end_date="2023-01-01",
    #     )


if __name__ == "__main__":
    unittest.main()
