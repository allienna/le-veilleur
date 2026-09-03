"""Hermetic test doubles for the publishing ports.

Mirrors `ingest/fakes.py` and `generate/fakes.py`: in-memory fakes satisfying the
`ImageGenerator` / `PromptRewriter` / `ContentRepository` Protocols so the steps and the full
pipeline run without Imagen, Claude, GitHub, or network.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from minion.publish.ports import ContentRepoError, ImagenBlockedError


def _no_outcomes() -> list[bytes | Exception]:
    return []


def _no_prompts() -> list[str]:
    return []


@dataclass
class FakeImageGenerator:
    """Scripted `ImageGenerator`. Returns `outcomes[call]` (bytes) or raises it (Exception).

    Repeats the last outcome once the script is exhausted. Records every prompt it was given so
    tests can assert the brand template and the softened-prompt retry.
    """

    outcomes: list[bytes | Exception] = field(default_factory=_no_outcomes)
    prompts: list[str] = field(default_factory=_no_prompts)

    def generate(self, prompt: str) -> bytes:
        self.prompts.append(prompt)
        if not self.outcomes:
            raise ImagenBlockedError("FakeImageGenerator needs `outcomes` configured")
        outcome = self.outcomes[min(len(self.prompts) - 1, len(self.outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def _no_calls() -> list[tuple[str, str]]:
    return []


@dataclass
class FakePromptRewriter:
    """Records `(prompt, reason)` calls and returns a deterministic softened rewrite."""

    calls: list[tuple[str, str]] = field(default_factory=_no_calls)

    def soften(self, prompt: str, reason: str) -> str:
        self.calls.append((prompt, reason))
        return f"softened: {prompt}"


@dataclass
class PutCall:
    """One recorded `put_files` invocation — one commit, carrying one or more files."""

    files: list[tuple[str, bytes]]
    message: str

    def path_content(self) -> dict[str, bytes]:
        """The commit's files as a `{path: content}` map, for assertions that don't care about
        the order files were added to the batch."""
        return dict(self.files)


def _no_put_calls() -> list[PutCall]:
    return []


@dataclass
class FakeContentRepository:
    """Records `put_files` calls, one per commit. Optionally raises `ContentRepoError` for the
    first `fail_times` calls (to exercise the caller's retry/backoff), then succeeds with a
    deterministic SHA derived from the call index."""

    fail_times: int = 0
    calls: list[PutCall] = field(default_factory=_no_put_calls)

    def put_files(self, files: list[tuple[str, bytes]], message: str) -> str:
        self.calls.append(PutCall(files=list(files), message=message))
        if len(self.calls) <= self.fail_times:
            raise ContentRepoError(f"fake transient failure ({len(self.calls)}/{self.fail_times})")
        return f"sha-{len(self.calls)}"
