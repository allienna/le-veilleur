# pyright: basic
# ^ wraps google-auth's impersonation helper; like secrets.py this SDK-boundary helper is
# dropped to basic checking.
"""Shared credential minting for the podcast adapters.

`minion-sa` (the Job's own ambient Application Default Credentials in Cloud Run) impersonates
the dedicated `podcast-sa` (infra/podcast.tf) via `roles/iam.serviceAccountTokenCreator` — no key
material is stored for `podcast-sa` at all. Both `tts.py` and `gcs.py` need the same
short-lived, impersonated bearer token, so it lives here once rather than twice.
"""

from __future__ import annotations

import google.auth
import google.auth.impersonated_credentials
import google.auth.transport.requests

from minion import config

_SCOPES: tuple[str, ...] = ("https://www.googleapis.com/auth/cloud-platform",)


def impersonated_access_token() -> str:
    """Return a fresh bearer token for `config.PODCAST_SA_EMAIL`, minted by impersonating it
    from the calling identity's own ambient credentials (ADC)."""
    source_credentials, _project = google.auth.default()
    target_credentials = google.auth.impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=config.PODCAST_SA_EMAIL,
        target_scopes=list(_SCOPES),
    )
    target_credentials.refresh(google.auth.transport.requests.Request())
    token = target_credentials.token
    if not token:
        raise RuntimeError("impersonated_credentials produced no access token")
    return token
