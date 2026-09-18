"""Podcast ports — the only script-writer / TTS / GCS surfaces the `podcast` step knows.

Mirrors `publish/ports.py`: the podcast step depends on these Protocols, `script.py` / `tts.py`
/ `gcs.py` implement them over the real APIs, and `fakes.py` provides hermetic doubles. Each of
the three calls (script, synthesis, upload) is a single best-effort attempt per run — a failure
here must never cost the day's article.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from minion.ingest.models import ScrapedSource


class PodcastGenerationError(RuntimeError):
    """The two-speaker script could not be written — subprocess/transport failure, a malformed
    or empty response, or the retry budget exhausted. Caught by the `podcast` step; never a hard
    run failure on its own — a missing episode must not cost the day's article."""


class AudioSynthesisError(RuntimeError):
    """Cloud Text-to-Speech could not synthesize the script — auth/quota/5xx/network, or an
    unexpected response shape. Caught by the `podcast` step alongside `PodcastGenerationError`."""


class AudioUploadError(RuntimeError):
    """Uploading the generated audio to the podcast bucket failed (transport or non-2xx).
    Caught by the `podcast` step alongside the other two."""


@dataclass(frozen=True)
class ScriptTurn:
    """One line of the two-speaker dialogue script."""

    speaker: Literal["A", "B"]
    text: str


@dataclass(frozen=True)
class AudioOverviewResult:
    """The synthesized, concatenated episode audio, before it is uploaded anywhere."""

    audio_bytes: bytes
    content_type: str
    duration_seconds: int | None


class ScriptWriter(Protocol):
    """Turns the day's validated sources into a two-speaker dialogue script."""

    def write_script(self, sources: list[ScrapedSource], target_words: int) -> list[ScriptTurn]:
        """Ask the model for a two-speaker (`A`/`B`) French dialogue script covering `sources`,
        aiming for roughly `target_words` words total. Raises `PodcastGenerationError` on any
        transport failure or a response that doesn't parse into turns."""
        ...


class AudioSynthesizer(Protocol):
    """Renders a dialogue script to a single audio file."""

    def synthesize(self, turns: list[ScriptTurn], language_code: str) -> AudioOverviewResult:
        """Synthesize each turn with its speaker's voice and concatenate them in order into one
        audio file. Raises `AudioSynthesisError` on any failure mode."""
        ...


class AudioStorage(Protocol):
    """Publishes the generated audio bytes to a public URL."""

    def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        """Upload `data` to the podcast bucket at `object_name` and return the resulting public
        HTTPS URL. Raises `AudioUploadError` on any non-2xx response or transport failure."""
        ...
