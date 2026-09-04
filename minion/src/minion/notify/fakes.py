"""Hermetic test double for the notify port.

Mirrors `publish/fakes.py`: an in-memory fake satisfying `Notifier` so the CLI and step tests
run without Gmail or network.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from minion.notify.ports import NotifyError


@dataclass
class SentEmail:
    """One recorded `send` call."""

    subject: str
    body: str


def _no_sent() -> list[SentEmail]:
    return []


@dataclass
class FakeNotifier:
    """Records every `send` call. Optionally raises `NotifyError` for the first `fail_times`
    calls (to exercise the caller's swallow-and-log path), then succeeds."""

    fail_times: int = 0
    sent: list[SentEmail] = field(default_factory=_no_sent)

    def send(self, *, subject: str, body: str) -> None:
        self.sent.append(SentEmail(subject=subject, body=body))
        if len(self.sent) <= self.fail_times:
            raise NotifyError(f"fake notify failure ({len(self.sent)}/{self.fail_times})")
