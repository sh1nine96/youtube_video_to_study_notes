"""
chunking.py

Utilities for splitting long transcripts into chunks.
"""

from typing import List


def chunk_transcript(
    transcript: str,
    chunk_size: int = 2000,
    overlap: int = 200
    ) -> List[str]:

    words = transcript.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks