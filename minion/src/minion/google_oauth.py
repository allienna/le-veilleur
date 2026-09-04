# pyright: basic
# ^ google-auth ships incomplete stubs (see pyproject reportMissingTypeStubs); this SDK-boundary
# helper is dropped to basic checking, matching secrets.py and ingest/gmail.py.
"""Shared Gmail OAuth credential construction.

One refresh-token secret (`gmail-oauth-refresh-token`), authorized for every scope in
`config.GMAIL_SCOPES` (read, for ingestion, and send, for the post-run notify email) — a single
operator consent covers both `ingest/gmail.py` and `notify/gmail.py`.
"""

from __future__ import annotations

import json
from typing import Any

from google.oauth2.credentials import Credentials

from minion import config, secrets

_DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"


def gmail_credentials() -> Credentials:
    """Build short-lived Gmail credentials from the operator's refresh-token JSON secret."""
    info: dict[str, Any] = json.loads(secrets.require(config.GMAIL_REFRESH_TOKEN_SECRET))
    return Credentials(
        token=None,
        refresh_token=info["refresh_token"],
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        token_uri=info.get("token_uri", _DEFAULT_TOKEN_URI),
        scopes=list(config.GMAIL_SCOPES),
    )
