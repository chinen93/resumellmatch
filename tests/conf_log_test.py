"""
Unittest configuration helper for the scraper project.

Configure logging for unittest tests to suppress output during test runs.

Usage in your test files:
    from tests.conftest import BaseTestCase

    class MyTest(BaseTestCase):
        def test_something(self):
            # Logging is automatically configured for tests
            pass

Or manually in a test module:
    import unittest
    from src.logging_config import setup_logging

    # Configure at module level
    setup_logging(testing=True)

    class MyTest(unittest.TestCase):
        def test_something(self):
            pass
"""

import unittest

from src.logging_config import enable_logging, setup_logging


class BaseTestCase(unittest.TestCase):
    """
    Base test case class that automatically configures logging for tests.

    Inherit from this class instead of unittest.TestCase to automatically
    suppress logging output during tests.

    Example:
        from tests.conftest import BaseTestCase

        class TestMyModule(BaseTestCase):
            def test_something(self):
                # Logging suppressed automatically
                pass
    """

    @classmethod
    def setUpClass(cls):
        """Configure logging for test class"""
        setup_logging(testing=True)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Re-enable logging after tests"""
        enable_logging()
        super().tearDownClass()
