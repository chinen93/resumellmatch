import unittest
from unittest.mock import MagicMock, patch

from src.llm.client.ollama import OllamaLocalClient
from src.llm.client.response import SimpleResponse
from tests.conf_log_test import BaseTestCase


class TestOllamaLocalClient(BaseTestCase):
    """Unit tests for OllamaLocalClient class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def tearDown(self):
        """Clean up after each test method."""
        pass

    @patch("src.llm.client.ollama.generate")
    @patch("src.llm.client.ollama.OllamaLocalClient._get_prompt")
    def test_init_success(self, mock_get_prompt, mock_generate):
        """Test successful initialization."""
        mock_get_prompt.return_value = "Hello world prompt"
        mock_generate.return_value = {
            "response": '{"message": "Hello"}',
            "total_duration": 1000000000,
            "load_duration": 500000000,
            "prompt_eval_duration": 200000000,
            "eval_duration": 300000000,
            "prompt_eval_count": 10,
            "eval_count": 5,
        }

        client = OllamaLocalClient()

        self.assertTrue(client.ready)
        mock_get_prompt.assert_called_with("hello_world.txt")

    @patch("src.llm.client.ollama.generate")
    @patch("src.llm.client.ollama.OllamaLocalClient._get_prompt")
    def test_init_connection_error(self, mock_get_prompt, mock_generate):
        """Test initialization with connection error."""
        mock_get_prompt.return_value = "Hello world prompt"
        mock_generate.side_effect = ConnectionError()

        client = OllamaLocalClient()

        self.assertFalse(client.ready)

    @patch("src.llm.client.ollama.generate")
    def test_generate(self, mock_generate):
        """Test the _generate method."""
        mock_generate.return_value = {
            "response": '{"message": "test response"}',
            "total_duration": 1000000000,
            "load_duration": 500000000,
            "prompt_eval_duration": 200000000,
            "eval_duration": 300000000,
            "prompt_eval_count": 10,
            "eval_count": 5,
        }

        client = OllamaLocalClient()
        result = client._generate("test message", SimpleResponse)

        self.assertIsInstance(result, str)
        self.assertEqual(len(mock_generate.mock_calls), 2)

    @patch("src.llm.client.ollama.generate")
    def test_get_filepath(self, _):
        """Test getting filepath for prompts."""
        client = OllamaLocalClient()
        path = client._get_filepath("test.txt")

        self.assertTrue(str(path).endswith("prompt/test.txt"))

    @patch("src.llm.client.ollama.generate")
    @patch("builtins.open")
    def test_get_prompt_success(self, mock_open, _):
        """Test successful prompt retrieval."""
        mock_file = MagicMock()
        mock_file.read.return_value = "prompt content"
        mock_open.return_value.__enter__.return_value = mock_file

        client = OllamaLocalClient()
        result = client._get_prompt("test.txt")

        self.assertEqual(result, "prompt content")

    @patch("src.llm.client.ollama.generate")
    @patch("builtins.open")
    def test_get_prompt_file_not_found(self, mock_open, _):
        """Test prompt retrieval when file not found."""
        mock_open.side_effect = FileNotFoundError()

        client = OllamaLocalClient()
        result = client._get_prompt("nonexistent.txt")

        self.assertIsNone(result)

    @patch("src.llm.client.ollama.generate")
    @patch("src.llm.client.ollama.OllamaLocalClient._generate_when_ready")
    @patch("src.llm.client.ollama.OllamaLocalClient._get_prompt")
    def test_extract_resume_keywords(self, mock_get_prompt, mock_generate_ready, _):
        """Test extracting resume keywords."""
        mock_get_prompt.return_value = "Extract keywords from: {resume_text}"
        mock_generate_ready.return_value = '{"keywords": ["python", "testing"]}'

        client = OllamaLocalClient()
        client.ready = True
        result = client.extract_resume_keywords("some resume text")

        self.assertEqual(result, '{"keywords": ["python", "testing"]}')
        mock_get_prompt.assert_called_with("extract_resume_keywords.txt")

    @patch("src.llm.client.ollama.generate")
    @patch("src.llm.client.ollama.OllamaLocalClient._generate_when_ready")
    @patch("src.llm.client.ollama.OllamaLocalClient._get_prompt")
    def test_extract_job_description_keywords(
        self, mock_get_prompt, mock_generate_ready, _
    ):
        """Test extracting job description keywords."""
        mock_get_prompt.return_value = "Extract keywords from: {job_description}"
        mock_generate_ready.return_value = '{"keywords": ["software", "engineer"]}'

        client = OllamaLocalClient()
        client.ready = True
        result = client.extract_job_description_keywords("some job text")

        self.assertEqual(result, '{"keywords": ["software", "engineer"]}')
        mock_get_prompt.assert_called_with("extract_job_description_keywords.txt")

    @patch("src.llm.client.ollama.generate")
    @patch("src.llm.client.ollama.OllamaLocalClient._get_prompt")
    def test_extract_keywords_not_ready(self, mock_get_prompt, _):
        """Test keyword extraction when client is not ready."""
        mock_get_prompt.return_value = "prompt"

        client = OllamaLocalClient()
        client.ready = False
        result = client.extract_resume_keywords("text")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
