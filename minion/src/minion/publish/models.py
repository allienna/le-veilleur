"""Minion-internal publishing artefacts.

These cross the `imagen` → `github` step boundaries in the orchestrator data bag; every value
is an `extra="forbid"` Pydantic model so a malformed publish fails loudly.

There is no persisted article document any more: the committed markdown in the repo *is* the
artefact, and git is the recovery mechanism.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ["CommitResult", "ImageArtifact"]


class ImageArtifact(BaseModel):
    """The generated hero image carried from `imagen` to `github`.

    `png` is empty when Imagen could not be satisfied: the article still ships, with `image`
    omitted from its frontmatter, and the site falls back to its own placeholder SVG.
    """

    model_config = ConfigDict(extra="forbid")

    filename: str  # the date-stamped hero filename, e.g. "2026-09-01.png"
    png: bytes  # the PNG-encoded image bytes; empty when unavailable

    @property
    def available(self) -> bool:
        return bool(self.png)


class CommitResult(BaseModel):
    """One committed file's path and resulting commit SHA (returned by `ContentRepository`)."""

    model_config = ConfigDict(extra="forbid")

    path: str
    sha: str
