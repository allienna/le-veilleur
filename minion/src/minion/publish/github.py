# pyright: basic
# ^ wraps the GitHub Git Data API (untyped JSON over httpx); like generate/runner.py this
# external-boundary adapter is dropped to basic checking. Behaviour is covered by
# FakeContentRepository + the gated integration test (no GitHub/network in CI).
"""Production `ContentRepository` over the GitHub Git Data API.

One commit per call, however many files it carries: read the branch tip, create a blob per
file, build one tree on top of the tip's tree, create one commit on that tree, fast-forward the
branch ref onto it. The higher-level Contents API (one PUT per file) was tried first and
reverted — it makes one commit per file, so a run that published an article (image + markdown +
LinkedIn draft) plus ten fiches left thirteen commits and tripped the Pages deploy workflow
thirteen times in a row, superseded down to one real deploy but still flooding the history.

Retry/backoff lives in the caller; this adapter raises `ContentRepoError` on any non-2xx
response or transport failure — including a rejected fast-forward, since this repo has exactly
one writer per run (the global lock) and no other process pushes to this branch, so a ref
update failing means something is genuinely wrong rather than a race to retry past.

The target repo is this one, configured in `config` — the Minion runs in Cloud Run with no
checkout, so it publishes through the API rather than with git.
"""

from __future__ import annotations

import base64
from typing import Any

import httpx

from minion import config, secrets
from minion.publish.ports import ContentRepoError

_API_BASE = "https://api.github.com"


class GitHubContentRepository:
    """Commits to `{owner}/{repo}@{branch}` via the Git Data API."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        # Reuse one client per run for connection pooling; injectable for tests.
        self._client = client or httpx.Client(timeout=config.GITHUB_TIMEOUT.total_seconds())

    def _headers(self) -> dict[str, str]:
        pat = secrets.require(config.GITHUB_PAT_SECRET)
        return {
            "Authorization": f"Bearer {pat}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _url(self, path: str) -> str:
        return f"{_API_BASE}/repos/{config.GITHUB_REPO_OWNER}/{config.GITHUB_REPO_NAME}/{path}"

    def _get(self, path: str, headers: dict[str, str]) -> dict[str, Any]:
        try:
            response = self._client.get(self._url(path), headers=headers)
        except httpx.HTTPError as exc:
            raise ContentRepoError(f"GitHub GET {path} failed: {exc}") from exc
        if response.is_error:
            raise ContentRepoError(
                f"GitHub GET {path} returned {response.status_code}: {response.text[:300]}"
            )
        return response.json()

    def _post(self, path: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self._client.post(self._url(path), headers=headers, json=payload)
        except httpx.HTTPError as exc:
            raise ContentRepoError(f"GitHub POST {path} failed: {exc}") from exc
        if response.is_error:
            raise ContentRepoError(
                f"GitHub POST {path} returned {response.status_code}: {response.text[:300]}"
            )
        return response.json()

    def put_files(self, files: list[tuple[str, bytes]], message: str) -> str:
        headers = self._headers()
        branch = config.GITHUB_BRANCH

        ref = self._get(f"git/ref/heads/{branch}", headers)
        parent_sha = ref["object"]["sha"]
        parent_commit = self._get(f"git/commits/{parent_sha}", headers)
        base_tree_sha = parent_commit["tree"]["sha"]

        tree_entries = []
        for path, content in files:
            blob = self._post(
                "git/blobs",
                headers,
                {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
            )
            tree_entries.append(
                {"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]}
            )

        tree = self._post("git/trees", headers, {"base_tree": base_tree_sha, "tree": tree_entries})
        commit = self._post(
            "git/commits",
            headers,
            {"message": message, "tree": tree["sha"], "parents": [parent_sha]},
        )
        commit_sha = commit["sha"]

        try:
            response = self._client.patch(
                self._url(f"git/refs/heads/{branch}"),
                headers=headers,
                json={"sha": commit_sha, "force": False},
            )
        except httpx.HTTPError as exc:
            raise ContentRepoError(f"GitHub PATCH ref failed: {exc}") from exc
        if response.is_error:
            raise ContentRepoError(
                f"GitHub PATCH ref returned {response.status_code}: {response.text[:300]}"
            )

        return commit_sha
