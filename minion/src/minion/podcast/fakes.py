"""Hermetic test doubles for the podcast ports.

Mirrors `publish/fakes.py`: in-memory fakes satisfying the `ScriptWriter` / `AudioSynthesizer` /
`AudioStorage` Protocols so the `podcast` step and the full pipeline run without Claude, Cloud
TTS, GCS, or network.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from minion.ingest.models import ScrapedSource
from minion.podcast.ports import (
    AudioOverviewResult,
    AudioSynthesisError,
    AudioUploadError,
    PodcastGenerationError,
    ScriptTurn,
)


def _no_script_outcomes() -> list[list[ScriptTurn] | Exception]:
    return []


def _no_script_calls() -> list[tuple[list[ScrapedSource], int]]:
    return []


@dataclass
class FakeScriptWriter:
    """Scripted `ScriptWriter`. Returns `outcomes[call]` (turns) or raises it, then repeats the
    last outcome. Records every `write_script` call so tests can assert on the sources given."""

    outcomes: list[list[ScriptTurn] | Exception] = field(default_factory=_no_script_outcomes)
    calls: list[tuple[list[ScrapedSource], int]] = field(default_factory=_no_script_calls)

    def write_script(self, sources: list[ScrapedSource], target_words: int) -> list[ScriptTurn]:
        self.calls.append((sources, target_words))
        if not self.outcomes:
            raise PodcastGenerationError("FakeScriptWriter needs `outcomes` configured")
        outcome = self.outcomes[min(len(self.calls) - 1, len(self.outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def _no_synth_outcomes() -> list[AudioOverviewResult | Exception]:
    return []


def _no_synth_calls() -> list[tuple[list[ScriptTurn], str]]:
    return []


@dataclass
class FakeAudioSynthesizer:
    """Scripted `AudioSynthesizer`. Returns `outcomes[call]` or raises it, then repeats the last
    outcome. Records every `synthesize` call."""

    outcomes: list[AudioOverviewResult | Exception] = field(default_factory=_no_synth_outcomes)
    calls: list[tuple[list[ScriptTurn], str]] = field(default_factory=_no_synth_calls)

    def synthesize(self, turns: list[ScriptTurn], language_code: str) -> AudioOverviewResult:
        self.calls.append((turns, language_code))
        if not self.outcomes:
            raise AudioSynthesisError("FakeAudioSynthesizer needs `outcomes` configured")
        outcome = self.outcomes[min(len(self.calls) - 1, len(self.outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


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
