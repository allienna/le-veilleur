"""Minion-internal ingestion boundary models.

These are
intermediate pipeline values carried in the orchestrator data bag between the `gmail`,
`scrape`, and `validate_input` steps. Every value crossing a step boundary is one of these
Pydantic models, never a raw dict.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class SourceOutcome(StrEnum):
    """The terminal outcome of scraping a single candidate URL."""

    ok = "ok"
    paywalled = "paywalled"
    failed = "failed"


class Newsletter(BaseModel):
    """One unread newsletter fetched from Gmail, with the article URLs extracted from it."""

    model_config = ConfigDict(extra="forbid")

    sender: str
    subject: str
    received_at: datetime
    candidate_urls: list[str]


class ScrapedSource(BaseModel):
    """The result of scraping one candidate URL.

    `markdown` and `title` are populated only when `outcome is SourceOutcome.ok`; a
    `paywalled` or `failed` source carries the outcome and no usable content.
    `failure_reason` is set only when `outcome is SourceOutcome.failed`, for diagnosing which
    failure mode (bad status, non-HTML, empty extraction, deadline) dominates a given run.
    """

    model_config = ConfigDict(extra="forbid")

    url: str
    outcome: SourceOutcome
    title: str | None = None
    markdown: str | None = None
    failure_reason: str | None = None


class SourceSet(BaseModel):
    """The full set of scraped sources for a run — the input to the validation gate.

    `ok_count / total` and `ok_count` drive the ≥50%-AND-≥5 threshold; paywalled and failed
    sources count toward `total` but not toward `ok_count`.
    """

    model_config = ConfigDict(extra="forbid")

    sources: list[ScrapedSource]

    @property
    def total(self) -> int:
        return len(self.sources)

    @property
    def ok_sources(self) -> list[ScrapedSource]:
        return [s for s in self.sources if s.outcome is SourceOutcome.ok]

    @property
    def ok_count(self) -> int:
        return len(self.ok_sources)

    @property
    def paywalled_count(self) -> int:
        return sum(1 for s in self.sources if s.outcome is SourceOutcome.paywalled)

    @property
    def failed_count(self) -> int:
        """Sources that errored out (non-retryable 4xx, or 429/5xx/transport after retries).
        Distinct from paywalled — used to tell a thin-news day apart from scrape trouble."""
        return sum(1 for s in self.sources if s.outcome is SourceOutcome.failed)
