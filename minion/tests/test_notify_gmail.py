"""Tests for the real notify Gmail client (`GmailNotifier`) over a fake googleapiclient Resource."""

from __future__ import annotations

import base64
from email import message_from_bytes
from email.header import decode_header
from typing import Any

import pytest

from minion.notify.gmail import GmailNotifier
from minion.notify.ports import NotifyError


class _RaisingHttpError(Exception):
    """Stand-in raised by the fake Resource to exercise the NotifyError translation."""


class _Exec:
    def __init__(self, raises: Exception | None = None) -> None:
        self._raises = raises

    def execute(self) -> Any:
        if self._raises is not None:
            raise self._raises
        return {"id": "sent-1"}


class _Messages:
    def __init__(self, rec: dict[str, Any], raises: Exception | None = None) -> None:
        self._rec = rec
        self._raises = raises

    def send(self, *, userId: str, body: dict[str, str]) -> _Exec:  # noqa: N803
        self._rec["userId"] = userId
        self._rec["raw"] = body["raw"]
        return _Exec(self._raises)


class _Users:
    def __init__(self, messages: _Messages) -> None:
        self._messages = messages

    def messages(self) -> _Messages:
        return self._messages


class _Service:
    def __init__(self, users: _Users) -> None:
        self._users = users

    def users(self) -> _Users:
        return self._users


def _build_service(*, raises: Exception | None = None) -> tuple[_Service, dict[str, Any]]:
    rec: dict[str, Any] = {}
    return _Service(_Users(_Messages(rec, raises))), rec


def test_send_encodes_mime_and_calls_users_messages_send() -> None:
    service, rec = _build_service()
    notifier = GmailNotifier(service=service)  # type: ignore[arg-type]

    notifier.send(subject="Le Veilleur — 2026-06-01 — OK", body="hello\nworld")

    assert rec["userId"] == "me"
    decoded = base64.urlsafe_b64decode(rec["raw"])
    parsed = message_from_bytes(decoded)
    subject_bytes, encoding = decode_header(parsed["subject"])[0]
    subject = subject_bytes.decode(encoding or "ascii")
    assert subject == "Le Veilleur — 2026-06-01 — OK"
    assert parsed.get_payload(decode=True).decode("utf-8").strip() == "hello\nworld"


def test_send_wraps_http_errors_as_notify_error() -> None:
    from googleapiclient.errors import HttpError
    from httplib2 import Response

    error = HttpError(Response({"status": "500"}), b"boom")
    service, _ = _build_service(raises=error)
    notifier = GmailNotifier(service=service)  # type: ignore[arg-type]

    with pytest.raises(NotifyError):
        notifier.send(subject="s", body="b")
