"""FichesStep: non-blocking per-source analysis, generated only for cited sources."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.fiches.fakes import FakeFicheGenerateRunner
from minion.generate.models import (
    ArticleFrontmatter,
    AssembledContext,
    ContextSource,
    GeneratedArticle,
)
from minion.logging import bind
from minion.publish.fakes import FakeContentRepository
from minion.steps.base import StepContext
from minion.steps.fiches import FICHE_PARTIAL_FAILURE_WARNING, FichesStep

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)
DATE = "2026-06-01"

SOURCE_A = ContextSource(url="https://a.example/1", title="Source A", markdown="content a")
SOURCE_B = ContextSource(url="https://b.example/2", title="Source B", markdown="content b")


def _fiche_json(theme: str = "IA", body: str | None = None) -> str:
    return json.dumps(
        {
            "theme": theme,
            "keywords": ["ia", "agents"],
            "tone": "opinion",
            "body": body
            or (
                "## Résumé\nUn résumé.\n\n"
                "## Points clés\n- un\n- deux\n\n"
                "## Analyse approfondie\nUne analyse.\n\n"
                "## Pourquoi ça compte\nParce que."
            ),
        }
    )


def _article(cites: list[ContextSource]) -> GeneratedArticle:
    citations = "\n".join(f"- [{s.title}]({s.url})" for s in cites)
    return GeneratedArticle(
        theme="ai",
        frontmatter=ArticleFrontmatter(title="T", date=DATE, themes=["IA"]),
        body=f"Corps de l'article.\n\n## Sources\n\n{citations}\n",
        linkedin="post",
        image_prompt="prompt",
    )


def _ctx(**data: Any) -> StepContext:
    return StepContext(run_id="R", date=DATE, clock=FrozenClock(T0), log=bind("R"), data=data)


def _committed(repo: FakeContentRepository, slug: str, date: str = DATE) -> bytes | None:
    """The content committed for `slug` on `date`, or None if no fiche was published."""
    path = f"site/src/content/fiches/{date}-{slug}.md"
    return next((c.content for c in repo.calls if c.path == path), None)


def test_persists_one_fiche_per_cited_source() -> None:
    runner = FakeFicheGenerateRunner(
        outputs={SOURCE_A.url: _fiche_json(), SOURCE_B.url: _fiche_json()}
    )
    repo = FakeContentRepository()
    result = FichesStep(runner=runner, content_repo=repo).run(
        _ctx(
            article=_article([SOURCE_A, SOURCE_B]),
            context=AssembledContext(sources=[SOURCE_A, SOURCE_B]),
        )
    )
    assert result.warning is None
    a = _committed(repo, "source-a")
    b = _committed(repo, "source-b")
    assert a is not None and SOURCE_A.url.encode() in a
    assert b'used_in: ["2026-06-01"]' in a
    assert b is not None and b'theme: "IA"' in b


def test_ignores_sources_not_cited_in_the_article() -> None:
    runner = FakeFicheGenerateRunner(outputs={SOURCE_A.url: _fiche_json()})
    repo = FakeContentRepository()
    FichesStep(runner=runner, content_repo=repo).run(
        _ctx(
            article=_article([SOURCE_A]),  # only A cited
            context=AssembledContext(sources=[SOURCE_A, SOURCE_B]),
        )
    )
    assert runner.calls == [SOURCE_A.url]  # B never invoked
    assert _committed(repo, "source-b") is None


def test_no_cited_sources_is_a_clean_noop() -> None:
    runner = FakeFicheGenerateRunner()
    repo = FakeContentRepository()
    result = FichesStep(runner=runner, content_repo=repo).run(
        _ctx(article=_article([]), context=AssembledContext(sources=[SOURCE_A]))
    )
    assert result.warning is None
    assert runner.calls == []


def test_one_failed_source_warns_but_does_not_block_the_others() -> None:
    runner = FakeFicheGenerateRunner(
        outputs={SOURCE_A.url: _fiche_json()}, fail_urls=frozenset({SOURCE_B.url})
    )
    repo = FakeContentRepository()
    result = FichesStep(runner=runner, content_repo=repo).run(
        _ctx(
            article=_article([SOURCE_A, SOURCE_B]),
            context=AssembledContext(sources=[SOURCE_A, SOURCE_B]),
        )
    )
    assert result.warning == FICHE_PARTIAL_FAILURE_WARNING
    assert _committed(repo, "source-a") is not None
    assert _committed(repo, "source-b") is None


def test_invalid_fiche_body_is_skipped_with_a_warning() -> None:
    # Missing the required "## Pourquoi ça compte" section.
    bad_body = "## Résumé\nx\n\n## Points clés\n- a\n\n## Analyse approfondie\ny"
    runner = FakeFicheGenerateRunner(outputs={SOURCE_A.url: _fiche_json(body=bad_body)})
    repo = FakeContentRepository()
    result = FichesStep(runner=runner, content_repo=repo).run(
        _ctx(article=_article([SOURCE_A]), context=AssembledContext(sources=[SOURCE_A]))
    )
    assert result.warning == FICHE_PARTIAL_FAILURE_WARNING
    assert _committed(repo, "source-a") is None


def test_a_source_cited_on_two_dates_yields_one_fiche_per_date() -> None:
    """The site keys fiches by `{date}-{slug}`, so re-citing a source publishes a second,
    separately-dated fiche rather than mutating the first."""
    runner = FakeFicheGenerateRunner(outputs={SOURCE_A.url: _fiche_json()})
    repo = FakeContentRepository()
    step = FichesStep(runner=runner, content_repo=repo)
    step.run(_ctx(article=_article([SOURCE_A]), context=AssembledContext(sources=[SOURCE_A])))
    later_ctx = StepContext(
        run_id="R2",
        date="2026-06-15",
        clock=FrozenClock(T0),
        log=bind("R2"),
        data={"article": _article([SOURCE_A]), "context": AssembledContext(sources=[SOURCE_A])},
    )
    step.run(later_ctx)
    first = _committed(repo, "source-a")
    second = _committed(repo, "source-a", date="2026-06-15")
    assert first is not None and b'used_in: ["2026-06-01"]' in first
    assert second is not None and b'used_in: ["2026-06-15"]' in second


def test_a_fiche_that_cannot_be_committed_is_skipped_not_fatal() -> None:
    """The article is already published by the time this step runs; no fiche is worth a failure."""
    runner = FakeFicheGenerateRunner(outputs={SOURCE_A.url: _fiche_json()})
    repo = FakeContentRepository(fail_times=99)
    result = FichesStep(runner=runner, content_repo=repo).run(
        _ctx(article=_article([SOURCE_A]), context=AssembledContext(sources=[SOURCE_A]))
    )
    assert result.warning == FICHE_PARTIAL_FAILURE_WARNING
