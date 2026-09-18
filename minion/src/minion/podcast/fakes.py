"""Hermetic test doubles for the podcast ports.

Mirrors `publish/fakes.py`: in-memory fakes satisfying the `NotebookLMClient` / `AudioStorage`
Protocols so the `podcast` step and the full pipeline run without NotebookLM Enterprise, GCS, or
network.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from minion.podcast.ports import AudioOverviewResult, AudioUploadError, PodcastGenerationError


def _no_generation_outcomes() -> list[AudioOverviewResult | Exception]:
    return []


def _no_generation_calls() -> list[tuple[str, list[tuple[str, str]], str]]:
    return []


@dataclass
class FakeNotebookLMClient:
    """Scripted `NotebookLMClient`. Returns `outcomes[call]` or raises it, then repeats the last
    outcome. Records every `generate_episode` call so tests can assert on the sources it was
    given. `purge_count` scripts `purge_notebooks_older_than`'s return value; `purge_raises`
    lets a test exercise the "purge itself fails" path without affecting the returned result."""

    outcomes: list[AudioOverviewResult | Exception] = field(default_factory=_no_generation_outcomes)
    calls: list[tuple[str, list[tuple[str, str]], str]] = field(
        default_factory=_no_generation_calls
    )
    purge_count: int = 0
    purge_raises: bool = False

    def generate_episode(
        self, date: str, sources: list[tuple[str, str]], language_code: str
    ) -> AudioOverviewResult:
        self.calls.append((date, sources, language_code))
        if not self.outcomes:
            raise PodcastGenerationError("FakeNotebookLMClient needs `outcomes` configured")
        outcome = self.outcomes[min(len(self.calls) - 1, len(self.outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def purge_notebooks_older_than(self, days: int) -> int:
        if self.purge_raises:
            # A real adapter never raises here (it swallows internally) — a fake that raises
            # anyway exercises the step's own defensive try/except around the call.
            raise RuntimeError("fake purge failure")
        return self.purge_count


def _no_storage_outcomes() -> list[str | Exception]:
    return []


def _no_storage_calls() -> list[tuple[str, bytes, str]]:
    return []


@dataclass
class FakeAudioStorage:
    """Scripted `AudioStorage`. Returns `outcomes[call]` (a URL) or raises it, then repeats the
    last outcome. Records every `upload` call."""

    outcomes: list[str | Exception] = field(default_factory=_no_storage_outcomes)
    calls: list[tuple[str, bytes, str]] = field(default_factory=_no_storage_calls)

    def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        self.calls.append((object_name, data, content_type))
        if not self.outcomes:
            raise AudioUploadError("FakeAudioStorage needs `outcomes` configured")
        outcome = self.outcomes[min(len(self.calls) - 1, len(self.outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
