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
import re
from typing import Any

import httpx

from minion import config, secrets
from minion.models import RecentArticle
from minion.publish.ports import ContentRepoError

_API_BASE = "https://api.github.com"

_ARTICLES_DIR = "site/src/content/articles"
# Matches only the exact shapes `publish/serialize.py` emits (`title: "…"`, `themes: [A, B]`) —
# this is the only writer of these files, so a dependency-free regex beats a `pyyaml` add just to
# read a format this codebase fully controls.
_FRONTMATTER_TITLE = re.compile(r'^title:\s*"((?:[^"\\]|\\.)*)"\s*$', re.MULTILINE)
_FRONTMATTER_THEMES = re.compile(r"^themes:\s*\[(.*)\]\s*$", re.MULTILINE)


def _parse_frontmatter(text: str) -> tuple[str, list[str]] | None:
    """Extract `(title, themes)` from a `render_post`-shaped article, or `None` if it doesn't
    match — e.g. a malformed or hand-edited file, skipped rather than failing the whole read."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    title_match = _FRONTMATTER_TITLE.search(block)
    themes_match = _FRONTMATTER_THEMES.search(block)
    if not title_match or not themes_match:
        return None
    title = title_match.group(1).replace('\\"', '"').replace("\\\\", "\\")
    themes = [t.strip() for t in themes_match.group(1).split(",") if t.strip()]
    return title, themes


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

    def _get(self, path: str, headers: dict[str, str]) -> Any:
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

    def get_recent_articles(self, n: int) -> list[RecentArticle]:
        headers = self._headers()
        entries = self._get(f"contents/{_ARTICLES_DIR}", headers)
        if not isinstance(entries, list):
            return []
        names = sorted(
            (
                e["name"]
                for e in entries
                if isinstance(e, dict) and str(e.get("name", "")).endswith(".md")
            ),
            reverse=True,
        )[:n]

        recent: list[RecentArticle] = []
        for name in names:
            file_obj = self._get(f"contents/{_ARTICLES_DIR}/{name}", headers)
            if not isinstance(file_obj, dict) or file_obj.get("encoding") != "base64":
                continue
            try:
                text = base64.b64decode(file_obj["content"]).decode("utf-8")
            except (KeyError, ValueError):
                continue
            parsed = _parse_frontmatter(text)
            if parsed is None:
                continue
            title, themes = parsed
            recent.append(RecentArticle(date=name.removesuffix(".md"), title=title, themes=themes))
        return recent
