"""Data ingestion utility functions.

Provides helper functions for file path construction and data directory access.
"""

from pathlib import Path

from config.settings import get_settings


def get_filepath(filename: str) -> str:
    """Get the full file path for a filename in the input directory.

    Constructs the full path to a file in the configured data input directory.

    Args:
        filename: The filename or relative path within the input directory.

    Returns:
        The full absolute path to the file.

    Raises:
        AssertionError: If DATA_DIR is not configured in environment settings.
    """

    settings = get_settings()
    assert (
        settings.DATA_DIR is not None
    ), "DATA_DIR must be set in environment variables"

    filepath = (
        Path(__file__).parent.parent.parent / settings.DATA_DIR / "input" / filename
    )

    return str(filepath)
