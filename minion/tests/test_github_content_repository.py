"""Tests for `GitHubContentRepository.get_recent_articles` over `httpx.MockTransport`.

Mirrors `test_scraper_client.py`: no real GitHub/network, just a scripted transport plus a
stubbed secret accessor. `put_files` already has end-to-end coverage via `test_publish_integration`
(fake pipeline) and the gated real smoke test; this file only covers the new read path.
"""

from __future__ import annotations

import base64

import httpx
import pytest

from minion import secrets
from minion.publish.github import GitHubContentRepository
from minion.publish.ports import ContentRepoError

_DIR_PATH = "/repos/allienna/le-veilleur/contents/site/src/content/articles"


def _file_response(text: str) -> dict[str, object]:
    return {"content": base64.b64encode(text.encode()).decode("ascii"), "encoding": "base64"}


def _article(title: str, themes: list[str], *, extra: str = "") -> str:
    theme_list = ", ".join(themes)
    return (
        f'---\ntitle: "{title}"\ndate: 2026-09-01\nthemes: [{theme_list}]\nsources: 3{extra}\n'
        "---\n\nbody\n"
    )


@pytest.fixture(autouse=True)
def _fake_pat(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(secrets, "require", lambda name: "ghp-fake")


def _make_repo(handler) -> GitHubContentRepository:  # type: ignore[no-untyped-def]
    return GitHubContentRepository(client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_returns_most_recent_n_parsed_articles() -> None:
    files = {
        "2026-09-01.md": _article("Un", ["IA"]),
        "2026-09-02.md": _article("Deux", ["Data", "Leadership"]),
        "2026-09-03.md": _article("Trois", ["Sécurité"]),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == _DIR_PATH:
            return httpx.Response(200, json=[{"name": name, "type": "file"} for name in files])
        name = request.url.path.rsplit("/", 1)[-1]
        return httpx.Response(200, json=_file_response(files[name]))

    recent = _make_repo(handler).get_recent_articles(2)

    assert [a.date for a in recent] == ["2026-09-03", "2026-09-02"]  # most recent first
    assert recent[0].title == "Trois"
    assert recent[0].themes == ["Sécurité"]
    assert recent[1].themes == ["Data", "Leadership"]


def test_malformed_file_is_skipped_not_fatal() -> None:
    files = {
        "2026-09-01.md": "not frontmatter at all",
        "2026-09-02.md": _article("Deux", ["Data"]),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == _DIR_PATH:
            return httpx.Response(200, json=[{"name": name, "type": "file"} for name in files])
        name = request.url.path.rsplit("/", 1)[-1]
        return httpx.Response(200, json=_file_response(files[name]))

    recent = _make_repo(handler).get_recent_articles(5)

    assert [a.date for a in recent] == ["2026-09-02"]


def test_listing_failure_raises_content_repo_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    with pytest.raises(ContentRepoError):
        _make_repo(handler).get_recent_articles(5)


def test_empty_directory_returns_empty_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    assert _make_repo(handler).get_recent_articles(5) == []
