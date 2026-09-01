"""ImagenStep: happy generation, rewrite retry, and giving up on the image with a warning."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from minion import config
from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.generate.models import ArticleFrontmatter, GeneratedArticle
from minion.logging import bind
from minion.publish.fakes import FakeImageGenerator, FakePromptRewriter
from minion.publish.models import ImageArtifact
from minion.publish.ports import ImagenBlockedError
from minion.steps.base import StepContext
from minion.steps.publish import ImagenStep

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)
DATE = "2026-06-01"


def _article() -> GeneratedArticle:
    return GeneratedArticle(
        theme="ai",
        frontmatter=ArticleFrontmatter(title="T", date=DATE, themes=["IA"]),
        body="body",
        linkedin="post",
        image_prompt="a watchful owl over a city",
    )


def _ctx(**data: Any) -> StepContext:
    return StepContext(run_id="R", date=DATE, clock=FrozenClock(T0), log=bind("R"), data=data)


def _step(gen: FakeImageGenerator, rewriter: FakePromptRewriter) -> ImagenStep:
    return ImagenStep(image_generator=gen, prompt_rewriter=rewriter)


def test_happy_generation_writes_artifact_and_backfills_image() -> None:
    gen = FakeImageGenerator(outcomes=[b"PNGDATA"])
    rewriter = FakePromptRewriter()
    result = _step(gen, rewriter).run(_ctx(article=_article()))

    image = result.payload["image"]
    assert isinstance(image, ImageArtifact)
    assert image.filename == f"{DATE}.png" and image.png == b"PNGDATA"
    assert image.available is True
    assert result.warning is None
    # The brand template is appended to the article's image_prompt.
    assert config.IMAGEN_BRAND_TEMPLATE in gen.prompts[0]
    assert "watchful owl" in gen.prompts[0]
    # frontmatter.image is back-filled on the article passed downstream.
    assert result.payload["article"].frontmatter.image == f"{DATE}.png"  # type: ignore[union-attr]
    assert rewriter.calls == []  # no rewrite on the happy path


def test_rejection_then_rewrite_succeeds() -> None:
    gen = FakeImageGenerator(outcomes=[ImagenBlockedError("blocked"), b"PNG2"])
    rewriter = FakePromptRewriter()
    result = _step(gen, rewriter).run(_ctx(article=_article()))

    image = result.payload["image"]
    assert isinstance(image, ImageArtifact) and image.png == b"PNG2"
    assert image.available is True
    assert result.warning is None
    assert len(rewriter.calls) == 1  # one softening retry
    assert gen.prompts[1].startswith("softened: ")  # the rewritten prompt was used


def test_rewrite_failure_ships_without_an_image() -> None:
    # The rewrite itself blows up (e.g. missing OAuth token / `claude` not installed); the step
    # must treat it as best-effort and let the article ship, never propagate.
    class BoomRewriter:
        def soften(self, prompt: str, reason: str) -> str:
            raise RuntimeError("no OAuth token")

    gen = FakeImageGenerator(outcomes=[ImagenBlockedError("blocked")])
    result = ImagenStep(image_generator=gen, prompt_rewriter=BoomRewriter()).run(
        _ctx(article=_article())
    )
    image = result.payload["image"]
    assert isinstance(image, ImageArtifact) and image.available is False
    assert result.warning == config.IMAGEN_FALLBACK_WARNING


def test_rejection_exhausted_ships_without_an_image_and_warns() -> None:
    gen = FakeImageGenerator(
        outcomes=[ImagenBlockedError("blocked"), ImagenBlockedError("still blocked")]
    )
    rewriter = FakePromptRewriter()
    result = _step(gen, rewriter).run(_ctx(article=_article()))

    image = result.payload["image"]
    assert isinstance(image, ImageArtifact)
    assert image.available is False
    assert result.warning == config.IMAGEN_FALLBACK_WARNING
    assert len(rewriter.calls) == config.IMAGEN_RETRIES
    # No `image` key reaches the frontmatter, so the site uses its own placeholder SVG.
    assert result.payload["article"].frontmatter.image == ""  # type: ignore[union-attr]
