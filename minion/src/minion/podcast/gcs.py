# pyright: basic
# ^ wraps a raw JSON API over httpx; like publish/github.py this external-boundary adapter is
# dropped to basic checking. Behaviour is covered by FakeAudioStorage + the gated integration
# test (no GCS/network in CI).
"""Production `AudioStorage` over the GCS JSON API's simple media upload.

Raw REST over `httpx` rather than adding `google-cloud-storage` as a dependency — consistent
with `publish/github.py`'s own raw-REST style for an external-boundary adapter this codebase
fully controls the one call it needs from.

Auth is by impersonating the dedicated `podcast-sa` (`_auth.impersonated_access_token`), not a
stored key. The bucket itself is public-read (infra/podcast.tf) so the resulting
`storage.googleapis.com` URL is directly fetchable by a podcast app's RSS enclosure — no signed
URL needed.
"""

from __future__ import annotations

import httpx

from minion import config
from minion.podcast._auth import impersonated_access_token
from minion.podcast.ports import AudioUploadError

_UPLOAD_URL = "https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o"
_PUBLIC_URL = "https://storage.googleapis.com/{bucket}/{object_name}"


class GcsAudioStorage:
    """`AudioStorage` over the GCS JSON API."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(timeout=config.GITHUB_TIMEOUT.total_seconds())

    def upload(self, object_name: str, data: bytes, content_type: str) -> str:
        url = _UPLOAD_URL.format(bucket=config.PODCAST_BUCKET_NAME)
        try:
            response = self._client.post(
                url,
                params={"uploadType": "media", "name": object_name},
                headers={
                    "Authorization": f"Bearer {impersonated_access_token()}",
                    "Content-Type": content_type,
                },
                content=data,
            )
        except httpx.HTTPError as exc:
            raise AudioUploadError(f"GCS upload failed: {exc}") from exc
        if response.is_error:
            raise AudioUploadError(
                f"GCS upload returned {response.status_code}: {response.text[:300]}"
            )
        return _PUBLIC_URL.format(bucket=config.PODCAST_BUCKET_NAME, object_name=object_name)
