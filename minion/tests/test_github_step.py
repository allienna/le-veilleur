"""GithubStep: the single atomic commit, idempotent replay, and retry-then-fail."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest

from minion import config
from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.generate.models import ArticleFrontmatter, GeneratedArticle
from minion.logging import bind
from minion.publish.fakes import FakeContentRepository
from minion.publish.models import CommitResult, ImageArtifact
from minion.publish.ports import ContentRepoError
from minion.steps.base import StepContext
from minion.steps.publish import GithubStep

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)
DATE = "2026-06-01"

MD_PATH = f"site/src/content/articles/{DATE}.md"
IMAGE_PATH = f"site/public/images/{DATE}.png"
LINKEDIN_PATH = f"linkedin/{DATE}.md"


def _article() -> GeneratedArticle:
    return GeneratedArticle(
        theme="IA",
        frontmatter=ArticleFrontmatter(
            title="Hello World", date=DATE, themes=["IA"], image=f"{DATE}.png"
        ),
        body="body",
        linkedin="le post LinkedIn",
        image_prompt="prompt",
    )


def _ctx(**data: Any) -> StepContext:
    return StepContext(run_id="R", date=DATE, clock=FrozenClock(T0), log=bind("R"), data=data)


def _bag(png: bytes = b"IMG") -> dict[str, Any]:
    return {"article": _article(), "image": ImageArtifact(filename=f"{DATE}.png", png=png)}


def _step(repo: FakeContentRepository) -> GithubStep:
    return GithubStep(content_repo=repo, sleep=lambda _s: None)


def test_commits_image_markdown_and_linkedin_as_one_commit() -> None:
    repo = FakeContentRepository()
    result = _step(repo).run(_ctx(**_bag()))

    # Exactly one commit, carrying all three files — the whole point of the redesign.
    assert len(repo.calls) == 1
    files = repo.calls[0].path_content()
    assert set(files) == {IMAGE_PATH, MD_PATH, LINKEDIN_PATH}

    commits = result.payload["commits"]
    assert isinstance(commits, list) and all(isinstance(c, CommitResult) for c in commits)
    assert {c.sha for c in commits} == {"sha-1"}  # every file shares the one commit's SHA
    assert result.payload["commit_sha"] == "sha-1"

    assert b'title: "Hello World"' in files[MD_PATH]
    assert b"themes: [IA]" in files[MD_PATH]
    assert b"le post LinkedIn" in files[LINKEDIN_PATH]


def test_article_path_is_keyed_by_date_alone() -> None:
    """The site resolves an article's URL from its filename, and the fiches' `used_in` keys on
    the date — so the path must not carry a slug."""
    repo = FakeContentRepository()
    _step(repo).run(_ctx(**_bag()))
    files = repo.calls[0].path_content()
    assert MD_PATH in files
    assert not any("hello-world" in path for path in files)


def test_missing_image_skips_the_image_file_but_still_publishes() -> None:
    """Imagen gave up: the article and the LinkedIn post must still ship."""
    bag = _bag(png=b"")
    bag["article"] = _article().model_copy(
        update={"frontmatter": _article().frontmatter.model_copy(update={"image": ""})}
    )
    repo = FakeContentRepository()
    _step(repo).run(_ctx(**bag))
    files = repo.calls[0].path_content()
    assert set(files) == {MD_PATH, LINKEDIN_PATH}
    assert b"image:" not in files[MD_PATH]


def test_replay_is_a_second_commit_with_the_same_paths() -> None:
    repo = FakeContentRepository()
    step = _step(repo)
    step.run(_ctx(**_bag()))
    step.run(_ctx(**_bag()))  # replay
    assert len(repo.calls) == 2
    assert set(repo.calls[0].path_content()) == set(repo.calls[1].path_content())


def test_retries_then_succeeds() -> None:
    repo = FakeContentRepository(fail_times=2)  # first two attempts fail, third succeeds
    result = _step(repo).run(_ctx(**_bag()))
    assert len(repo.calls) == 3  # one batch, retried twice
    assert result.payload["commit_sha"] == "sha-3"


def test_retries_exhausted_hard_fails() -> None:
    repo = FakeContentRepository(fail_times=99)  # always fail
    with pytest.raises(ContentRepoError):
        _step(repo).run(_ctx(**_bag()))
    assert len(repo.calls) == config.GITHUB_RETRIES + 1
