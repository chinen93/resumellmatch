from pathlib import Path

from config.settings import get_settings


def get_filepath(filename: str) -> str:
    """Get the full file path for a given filename."""

    settings = get_settings()
    assert (
        settings.DATA_DIR is not None
    ), "DATA_DIR must be set in environment variables"

    filepath = (
        Path(__file__).parent.parent.parent / settings.DATA_DIR / "input" / filename
    )

    return str(filepath)
