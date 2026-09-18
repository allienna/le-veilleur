"""Podcast ports — the only NotebookLM Enterprise / GCS surfaces the `podcast` step knows.

Mirrors `publish/ports.py`: the podcast step depends on these Protocols, `notebooklm.py` /
`gcs.py` implement them over the real APIs, and `fakes.py` provides hermetic doubles. Retry lives
in the step for the GitHub commit only — NotebookLM generation and the GCS upload are each a
single best-effort attempt per run, since a failure here must never cost the day's article.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class PodcastGenerationError(RuntimeError):
    """NotebookLM could not produce a usable audio overview — notebook creation, source
    ingestion, audio-overview generation, or the bounded poll all fold into this one exception,
    exactly as `GeminiImageGenerator` collapses every Imagen failure mode into
    `ImagenBlockedError`. The `podcast` step catches this; it is never a hard run failure on its
    own — a missing episode must not cost the day's article.
    """


class AudioUploadError(RuntimeError):
    """Uploading the generated audio to the podcast bucket failed (transport or non-2xx).
    Caught by the `podcast` step alongside `PodcastGenerationError`."""


@dataclass(frozen=True)
class AudioOverviewResult:
    """One generated audio overview, before it is uploaded anywhere."""

    audio_bytes: bytes
    content_type: str
    duration_seconds: int | None
    notebook_id: str | None


class NotebookLMClient(Protocol):
    """Drives one day's NotebookLM Enterprise notebook end to end."""

    def generate_episode(
        self, date: str, sources: list[tuple[str, str]], language_code: str
    ) -> AudioOverviewResult:
        """Create a notebook named `date`, batch-add `sources` (each an `(url, title)` pair) as
        web-content sources, request a default-focus audio overview in `language_code`, and poll
        until it completes or `config.PODCAST_GENERATION_TIMEOUT` elapses.

        Raises `PodcastGenerationError` on any failure mode — notebook creation, source
        ingestion, generation, or timeout — so the step never needs to know which of the
        underlying API calls failed.
        """
        ...

    def purge_notebooks_older_than(self, days: int) -> int:
        """Best-effort hygiene: delete every date-named notebook older than `days`, return the
        count deleted. Never raises — the adapter itself logs and swallows internal failures,
        since this is pure cleanup and must never affect today's outcome."""
        ...


class AudioStorage(Protocol):
    """Publishes the generated audio bytes to a public URL."""

    def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        """Upload `data` to the podcast bucket at `object_name` and return the resulting public
        HTTPS URL. Raises `AudioUploadError` on any non-2xx response or transport failure."""
        ...
