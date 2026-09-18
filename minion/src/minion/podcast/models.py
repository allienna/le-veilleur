"""Minion-internal podcast artefact.

Crosses the `podcast` step's internal generation → its own commit, and forward into the notify
data bag under `"podcast"` — mirrors `publish/models.py`'s `ImageArtifact` exactly, including the
empty-means-unavailable convention.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ["PodcastArtifact"]


class PodcastArtifact(BaseModel):
    """The generated episode carried from the `podcast` step into the notify data bag.

    `audio_url` is empty when no episode could be produced/published this run: the site simply
    has no entry for the day, and the notify email omits its podcast section.
    """

    model_config = ConfigDict(extra="forbid")

    date: str
    title: str
    audio_url: str
    duration_seconds: int | None = None

    @property
    def available(self) -> bool:
        return bool(self.audio_url)
