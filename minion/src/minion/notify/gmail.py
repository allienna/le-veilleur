# pyright: basic
# ^ google-api-python-client builds its Resource chain dynamically and ships incomplete stubs
# (see pyproject reportMissingTypeStubs); this SDK-boundary client is dropped to basic checking,
# matching ingest/gmail.py. Behaviour is covered by this module's tests via a fake Resource.
"""Production `Notifier` — sends the post-run email over the Gmail API.

Reuses the shared refresh-token OAuth chain (`google_oauth.gmail_credentials`), now including
the `gmail.send` scope alongside the ingestion `gmail.readonly` one — see `config.GMAIL_SCOPES`.
"""

from __future__ import annotations

import base64
from email.mime.text import MIMEText
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from minion import config
from minion.google_oauth import gmail_credentials
from minion.notify.ports import NotifyError


class GmailNotifier:
    """`Notifier` implementation over the Gmail API's `messages.send`.

    `service` may be injected (tests pass a fake Resource); otherwise it is built lazily from
    the refresh-token secret so importing this module needs no credentials.
    """

    def __init__(self, service: Any | None = None) -> None:
        self._service = service

    def _resource(self) -> Any:
        if self._service is None:
            self._service = build(
                "gmail", "v1", credentials=gmail_credentials(), cache_discovery=False
            )
        return self._service

    def send(self, *, subject: str, body: str) -> None:
        message = MIMEText(body, "html")
        message["to"] = config.NOTIFY_TO_ADDRESS
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
        try:
            self._resource().users().messages().send(userId="me", body={"raw": raw}).execute()
        except HttpError as exc:
            raise NotifyError(f"Gmail send failed: {exc}") from exc
