"""Hash utility functions.

Provides hash generation utilities used across the application for caching
and deduplication.
"""

import hashlib


def compute_hash(text: str) -> str:
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
