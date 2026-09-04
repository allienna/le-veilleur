"""The notify port — the only surface `cli.py`'s post-run hook knows."""

from __future__ import annotations

from typing import Protocol


class NotifyError(RuntimeError):
    """Sending the notification email failed. Never fatal to the run: the caller logs and
    swallows it, since a notify failure must not mask or change the pipeline's own outcome."""


class Notifier(Protocol):
    """Sends the post-run notification email."""

    def send(self, *, subject: str, body: str) -> None:
        """Send one plain-text email. Raises `NotifyError` on failure."""
        ...
