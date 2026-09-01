"""GithubStep: the three-file commit, idempotent replay, and retry-then-fail."""

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


def test_commits_image_then_markdown_then_linkedin() -> None:
    repo = FakeContentRepository()
    result = _step(repo).run(_ctx(**_bag()))

    # Image first, so a published post never references a missing hero image.
    assert [c.path for c in repo.calls] == [IMAGE_PATH, MD_PATH, LINKEDIN_PATH]
    commits = result.payload["commits"]
    assert isinstance(commits, list) and all(isinstance(c, CommitResult) for c in commits)
    by_path = {c.path: c.sha for c in commits}
    assert result.payload["commit_sha"] == by_path[MD_PATH]  # the article commit is the run's SHA

    committed = {c.path: c.content for c in repo.calls}
    assert b'title: "Hello World"' in committed[MD_PATH]
    assert b"themes: [IA]" in committed[MD_PATH]
    assert b"le post LinkedIn" in committed[LINKEDIN_PATH]


def test_article_path_is_keyed_by_date_alone() -> None:
    """The site resolves an article's URL from its filename, and the fiches' `used_in` keys on
    the date — so the path must not carry a slug."""
    repo = FakeContentRepository()
    _step(repo).run(_ctx(**_bag()))
    assert MD_PATH in {c.path for c in repo.calls}
    assert not any("hello-world" in c.path for c in repo.calls)


def test_missing_image_skips_the_image_commit_but_still_publishes() -> None:
    """Imagen gave up: the article and the LinkedIn post must still ship."""
    bag = _bag(png=b"")
    bag["article"] = _article().model_copy(
        update={"frontmatter": _article().frontmatter.model_copy(update={"image": ""})}
    )
    repo = FakeContentRepository()
    _step(repo).run(_ctx(**bag))
    assert [c.path for c in repo.calls] == [MD_PATH, LINKEDIN_PATH]
    committed = {c.path: c.content for c in repo.calls}
    assert b"image:" not in committed[MD_PATH]


def test_replay_overwrites_same_paths() -> None:
    repo = FakeContentRepository()
    step = _step(repo)
    step.run(_ctx(**_bag()))
    step.run(_ctx(**_bag()))  # replay
    # Same three paths committed again — idempotent by date, no new path variants.
    assert sorted({c.path for c in repo.calls}) == sorted([IMAGE_PATH, MD_PATH, LINKEDIN_PATH])


def test_retries_then_succeeds() -> None:
    repo = FakeContentRepository(fail_times=2)  # first two puts fail, third succeeds
    result = _step(repo).run(_ctx(**_bag()))
    # image: calls 1,2 fail then 3 succeeds; md: call 4; linkedin: call 5.
    assert len(repo.calls) == 5
    assert result.payload["commit_sha"] == "sha-4"


def test_retries_exhausted_hard_fails() -> None:
    repo = FakeContentRepository(fail_times=99)  # always fail
    with pytest.raises(ContentRepoError):
        _step(repo).run(_ctx(**_bag()))
    # The image is attempted GITHUB_RETRIES + 1 times, then raises — no silent partial publish.
    assert len(repo.calls) == config.GITHUB_RETRIES + 1
