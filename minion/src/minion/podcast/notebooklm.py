# pyright: basic
# ^ wraps an untyped, Pre-GA JSON REST API over httpx; like publish/github.py this
# external-boundary adapter is dropped to basic checking. Behaviour is covered by
# FakeNotebookLMClient + the gated integration test (no NotebookLM/network in CI).
"""Production `NotebookLMClient` over the Gemini Notebook Enterprise (NotebookLM Enterprise)
REST API.

TODO(verify before relying on this in prod): this is a Pre-GA surface
(`discoveryengine.googleapis.com/v1alpha`, package `google.cloud.notebooklm.v1alpha`) — the
request/response shapes below are best-effort from public documentation at the time this was
written, not confirmed against a live call. Before the first real run, verify: the exact path
segments and payload fields for `notebooks.create` / `notebooks.sources.batchCreate` /
`notebooks.audioOverviews.create`, the shape of a long-running-operation response for the audio
overview, and the shape of the finished result (in particular where the actual audio bytes or a
download URL live). Adjust `_create_notebook` / `_add_sources` / `_create_audio_overview` /
`_poll_audio_overview` together with the real docs; keep the one-exception-type contract
(`PodcastGenerationError`) the same regardless.

Auth is by impersonating the dedicated `podcast-sa` (`_auth.impersonated_access_token`), not a
stored key. `podcast-sa` holds `roles/discoveryengine.notebookLmUser` (`infra/podcast.tf`) — at
project scope that role only covers `notebooks.create`/`.list`; `sources.*` and `audioOverviews.*`
are not in it. This relies on an unconfirmed assumption (common elsewhere in this product family)
that creating a notebook makes the creator its resource-level Owner automatically. If
`_add_sources`/`_create_audio_overview` 403 in a real run, grant `roles/discoveryengine
.notebookLmOwner` instead.

Also unconfirmed: `discoveryengine.notebooks.delete` does not appear anywhere in the IAM
permissions reference for this service — `purge_notebooks_older_than`'s `_delete` call below may
have no backing endpoint. It is wrapped in the same swallow-and-log try/except as every other
failure mode here, so a 403/404 there degrades to "purged 0" rather than breaking anything, but
the 30-day notebook cleanup this was meant to provide should not be assumed to actually work
until verified against a real call.
"""

from __future__ import annotations

import time
from datetime import UTC
from typing import Any

import httpx

from minion import config, secrets
from minion.podcast._auth import impersonated_access_token
from minion.podcast.ports import AudioOverviewResult, PodcastGenerationError

_API_BASE = "https://discoveryengine.googleapis.com/v1alpha"
_LOCATION = "global"


class NotebookLMEnterpriseClient:
    """`NotebookLMClient` over the Gemini Notebook Enterprise REST API."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        timeout = config.PODCAST_GENERATION_TIMEOUT.total_seconds()
        self._client = client or httpx.Client(timeout=timeout)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {impersonated_access_token()}",
            "Content-Type": "application/json",
        }

    def _parent(self) -> str:
        # Addressed by project id (veilleur-app) rather than project number — verify this is
        # accepted by the real API; some GCP APIs require the numeric project.
        return f"projects/{secrets.PROJECT_ID}/locations/{_LOCATION}"

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self._client.post(
                f"{_API_BASE}/{path}", headers=self._headers(), json=payload
            )
        except httpx.HTTPError as exc:
            raise PodcastGenerationError(f"POST {path} failed: {exc}") from exc
        if response.is_error:
            raise PodcastGenerationError(
                f"POST {path} returned {response.status_code}: {response.text[:300]}"
            )
        return response.json()

    def _get(self, path: str) -> dict[str, Any]:
        try:
            response = self._client.get(f"{_API_BASE}/{path}", headers=self._headers())
        except httpx.HTTPError as exc:
            raise PodcastGenerationError(f"GET {path} failed: {exc}") from exc
        if response.is_error:
            raise PodcastGenerationError(
                f"GET {path} returned {response.status_code}: {response.text[:300]}"
            )
        return response.json()

    def _delete(self, path: str) -> None:
        try:
            response = self._client.delete(f"{_API_BASE}/{path}", headers=self._headers())
        except httpx.HTTPError as exc:
            raise PodcastGenerationError(f"DELETE {path} failed: {exc}") from exc
        if response.is_error:
            raise PodcastGenerationError(
                f"DELETE {path} returned {response.status_code}: {response.text[:300]}"
            )

    def _create_notebook(self, date: str) -> str:
        notebook_name = config.PODCAST_NOTEBOOK_NAME_TEMPLATE.format(date=date)
        result = self._post(f"{self._parent()}/notebooks", {"title": notebook_name})
        notebook_id = result.get("notebookId") or result.get("name")
        if not notebook_id:
            raise PodcastGenerationError("notebooks.create returned no notebook id")
        return str(notebook_id)

    def _add_sources(self, notebook_id: str, sources: list[tuple[str, str]]) -> None:
        payload = {
            "sources": [{"webContent": {"url": url, "sourceName": title}} for url, title in sources]
        }
        self._post(f"{self._parent()}/notebooks/{notebook_id}/sources:batchCreate", payload)

    def _create_audio_overview(self, notebook_id: str, language_code: str) -> str:
        payload = {
            "languageCode": language_code,
            "targetDurationSeconds": int(config.PODCAST_TARGET_DURATION.total_seconds()),
        }
        result = self._post(f"{self._parent()}/notebooks/{notebook_id}/audioOverviews", payload)
        operation_name = result.get("name")
        if not operation_name:
            raise PodcastGenerationError("audioOverviews.create returned no operation name")
        return str(operation_name)

    def _poll_audio_overview(self, operation_name: str) -> dict[str, Any]:
        deadline = time.monotonic() + config.PODCAST_GENERATION_TIMEOUT.total_seconds()
        while True:
            operation = self._get(operation_name)
            if operation.get("done"):
                if "error" in operation:
                    error = operation["error"]
                    raise PodcastGenerationError(f"audio overview generation failed: {error}")
                response = operation.get("response")
                if not isinstance(response, dict):
                    raise PodcastGenerationError(
                        "finished audio overview operation carried no response"
                    )
                return response
            if time.monotonic() >= deadline:
                raise PodcastGenerationError(
                    f"audio overview generation timed out after "
                    f"{config.PODCAST_GENERATION_TIMEOUT.total_seconds():.0f}s"
                )
            time.sleep(config.PODCAST_POLL_INTERVAL.total_seconds())

    def _download_audio(self, response: dict[str, Any]) -> tuple[bytes, str]:
        audio_url = response.get("audioUrl") or response.get("downloadUrl")
        if not audio_url:
            raise PodcastGenerationError("finished audio overview carried no downloadable URL")
        try:
            audio_response = self._client.get(audio_url, headers=self._headers())
        except httpx.HTTPError as exc:
            raise PodcastGenerationError(f"downloading the audio overview failed: {exc}") from exc
        if audio_response.is_error:
            raise PodcastGenerationError(
                f"downloading the audio overview returned {audio_response.status_code}"
            )
        content_type = audio_response.headers.get("content-type", "audio/mpeg")
        return audio_response.content, content_type

    def generate_episode(
        self, date: str, sources: list[tuple[str, str]], language_code: str
    ) -> AudioOverviewResult:
        try:
            notebook_id = self._create_notebook(date)
            self._add_sources(notebook_id, sources)
            operation_name = self._create_audio_overview(notebook_id, language_code)
            response = self._poll_audio_overview(operation_name)
            audio_bytes, content_type = self._download_audio(response)
        except PodcastGenerationError:
            raise
        except Exception as exc:
            raise PodcastGenerationError(f"podcast generation failed: {exc}") from exc
        return AudioOverviewResult(
            audio_bytes=audio_bytes,
            content_type=content_type,
            duration_seconds=response.get("durationSeconds"),
            notebook_id=notebook_id,
        )

    def purge_notebooks_older_than(self, days: int) -> int:
        import logging
        from datetime import datetime, timedelta

        logger = logging.getLogger(__name__)
        try:
            listing = self._get(f"{self._parent()}/notebooks")
            notebooks = listing.get("notebooks", [])
            cutoff = datetime.now(tz=UTC) - timedelta(days=days)
            purged = 0
            for notebook in notebooks:
                title = notebook.get("title", "")
                try:
                    notebook_date = datetime.strptime(title, "%Y-%m-%d").replace(tzinfo=UTC)
                except ValueError:
                    continue  # not one of ours (name doesn't match PODCAST_NOTEBOOK_NAME_TEMPLATE)
                if notebook_date < cutoff:
                    notebook_id = notebook.get("notebookId") or notebook.get("name")
                    if notebook_id:
                        self._delete(f"{self._parent()}/notebooks/{notebook_id}")
                        purged += 1
            return purged
        except Exception:
            logger.warning("podcast notebook purge failed", exc_info=True)
            return 0
