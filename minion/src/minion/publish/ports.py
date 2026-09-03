"""Publishing ports — the only Imagen / Claude-rewrite / GitHub surfaces the steps know.

Mirrors `generate/ports.py` and `ingest/ports.py`: the publish steps depend on these Protocols,
`imagen.py` / `github.py` implement them over the real SDKs, and `fakes.py` provides hermetic
doubles. Retry/backoff and the moderation fallback live in the *steps*, not here.
"""

from __future__ import annotations

from typing import Protocol


class ImagenBlockedError(RuntimeError):
    """Imagen returned no usable image — safety/moderation rejection, empty response, or quota.

    The `imagen` step catches this to drive the rewrite-then-omit-image fallback; it is never a
    hard run failure on its own — a missing hero image must not cost the day's article.
    """


class ContentRepoError(RuntimeError):
    """A GitHub Contents API call failed (non-2xx or transport). The `github` step retries with
    backoff and, only after exhausting them, hard-fails the run."""


class ImageGenerator(Protocol):
    """Generates one 16:9 hero image and returns it as PNG bytes."""

    def generate(self, prompt: str) -> bytes:
        """Generate a 16:9 PNG image for `prompt`. Raises `ImagenBlockedError` when no usable
        image comes back (moderation / empty / quota)."""
        ...


class PromptRewriter(Protocol):
    """Softens a rejected image prompt via an agentic `claude -p` call."""

    def soften(self, prompt: str, reason: str) -> str:
        """Return a softer, moderation-safer rewrite of `prompt` given the rejection `reason`."""
        ...


class ContentRepository(Protocol):
    """Commits files to the public Astro repo."""

    def put_files(self, files: list[tuple[str, bytes]], message: str) -> str:
        """Create or overwrite every `(path, content)` pair as ONE atomic commit and return the
        resulting commit SHA. A multi-file publish (the article's markdown, image and LinkedIn
        draft, or a batch of fiches) must land as a single history entry and trip a single
        Pages deploy, not one commit per file. Raises `ContentRepoError` on any non-2xx
        response or transport failure."""
        ...
