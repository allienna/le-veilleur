"""`build_message` — pure formatting of a finished `Run` into the notify email."""

from __future__ import annotations

from datetime import datetime

from minion.config import PARIS_TZ
from minion.generate.models import ArticleFrontmatter, GeneratedArticle
from minion.ingest.models import ScrapedSource, SourceOutcome, SourceSet
from minion.models import Run, RunStatus, RunStep, StepName
from minion.notify.message import build_message
from minion.publish.models import ImageArtifact

DATE = "2026-06-01"
T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)
T1 = datetime(2026, 6, 1, 6, 4, 12, tzinfo=PARIS_TZ)

_ARTICLE = GeneratedArticle(
    theme="ai",
    frontmatter=ArticleFrontmatter(title="T", date=DATE, themes=["IA"]),
    body="body",
    linkedin="Share-worthy LinkedIn post text.",
    image_prompt="prompt",
)


def _run(
    status: RunStatus,
    *,
    steps: list[RunStep] | None = None,
    error: str | None = None,
    cost_usd: float | None = None,
    tokens: int | None = None,
    started_at: datetime | None = T0,
    ended_at: datetime | None = T1,
) -> Run:
    return Run(
        run_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        date=DATE,
        status=status,
        started_at=started_at,
        ended_at=ended_at,
        error=error,
        cost_usd=cost_usd,
        tokens=tokens,
        steps=steps or [],
    )


def _github_success() -> RunStep:
    return RunStep(name=StepName.github, status=RunStatus.success, started_at=T0, ended_at=T1)


def test_success_includes_article_link_and_linkedin_text() -> None:
    run = _run(RunStatus.success, steps=[_github_success()], cost_usd=0.42, tokens=1200)
    subject, body = build_message(run, {"article": _ARTICLE})
    assert DATE in subject and "OK" in subject
    assert "Statut : OK (success)" in body
    assert f"articles/{DATE}/" in body
    assert "Share-worthy LinkedIn post text." in body
    assert "0.42 $" in body and "1200 tokens" in body
    assert "4m12s" in body
    assert "runId%3D%2201ARZ3NDEKTSV4RRFFQ69G5FAV%22" in body  # logs link, URL-encoded


def test_failure_before_generate_has_no_article_or_link() -> None:
    steps = [
        RunStep(name=StepName.gmail, status=RunStatus.success, started_at=T0, ended_at=T0),
        RunStep(
            name=StepName.assemble,
            status=RunStatus.failure,
            started_at=T0,
            ended_at=T1,
            error="boom",
        ),
    ]
    run = _run(RunStatus.failure, steps=steps, error="assemble: boom")
    subject, body = build_message(run, {})
    assert "KO" in subject
    assert "Statut : KO (failure)" in body
    assert "Raison : assemble: boom" in body
    assert "assemble: boom" in body  # per-step error line too
    assert "pas publié" in body
    assert "aucun article généré" in body


def test_article_generated_but_publish_failed_still_shows_linkedin_text_not_link() -> None:
    steps = [
        RunStep(name=StepName.generate, status=RunStatus.success, started_at=T0, ended_at=T0),
        RunStep(
            name=StepName.github,
            status=RunStatus.failure,
            started_at=T0,
            ended_at=T1,
            error="commit failed",
        ),
    ]
    run = _run(RunStatus.failure, steps=steps, error="github: commit failed")
    _subject, body = build_message(run, {"article": _ARTICLE})
    assert "pas publié" in body
    assert "Share-worthy LinkedIn post text." in body
    assert f"articles/{DATE}/" not in body


def test_success_with_warnings_labels_ok_with_warning() -> None:
    run = _run(RunStatus.success_with_warnings, error="imagen_unavailable")
    subject, body = build_message(run, {})
    assert "OK (avertissement)" in subject
    assert "Raison : imagen_unavailable" in body


def test_skipped_run_omits_cost_and_duration_when_absent() -> None:
    run = _run(RunStatus.skipped, error="no_sources", cost_usd=None, tokens=None)
    subject, body = build_message(run, {})
    assert "SKIPPED" in subject
    assert "Coût" not in body
    assert "Durée" in body  # started/ended are still set on a graceful terminal exit


def test_body_is_a_complete_html_document() -> None:
    run = _run(RunStatus.success, steps=[_github_success()])
    _subject, body = build_message(run, {"article": _ARTICLE})
    assert body.startswith("<!doctype html>")
    assert "<html" in body and "</html>" in body


def test_hero_image_embedded_as_data_uri_when_available() -> None:
    run = _run(RunStatus.success, steps=[_github_success()])
    image = ImageArtifact(filename="2026-06-01.png", png=b"\x89PNGfakebytes")
    _subject, body = build_message(run, {"article": _ARTICLE, "image": image})
    import base64

    encoded = base64.b64encode(b"\x89PNGfakebytes").decode("ascii")
    assert f"data:image/png;base64,{encoded}" in body


def test_no_hero_image_section_when_unavailable() -> None:
    run = _run(RunStatus.success, steps=[_github_success()])
    image = ImageArtifact(filename="2026-06-01.png", png=b"")  # imagen gave up
    _subject, body = build_message(run, {"article": _ARTICLE, "image": image})
    assert "data:image/png;base64," not in body


def test_linkedin_text_is_html_escaped() -> None:
    dangerous = ArticleFrontmatter(title="T", date=DATE, themes=["IA"])
    article = GeneratedArticle(
        theme="ai",
        frontmatter=dangerous,
        body="body",
        linkedin="<script>alert(1)</script> & <b>bold</b>",
        image_prompt="prompt",
    )
    run = _run(RunStatus.success, steps=[_github_success()])
    _subject, body = build_message(run, {"article": article})
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body


def test_shows_source_count_when_sources_present() -> None:
    sources = SourceSet(
        sources=[
            *(ScrapedSource(url=f"https://a.io/{i}", outcome=SourceOutcome.ok) for i in range(40)),
            *(
                ScrapedSource(url=f"https://b.io/{i}", outcome=SourceOutcome.paywalled)
                for i in range(17)
            ),
            *(
                ScrapedSource(url=f"https://c.io/{i}", outcome=SourceOutcome.failed)
                for i in range(43)
            ),
        ]
    )
    run = _run(RunStatus.success, steps=[_github_success()])
    _subject, body = build_message(run, {"article": _ARTICLE, "sources": sources})
    assert "Sources : 40 OK / 100 (17 payantes, 43 échouées)" in body


def test_no_source_count_when_sources_absent() -> None:
    run = _run(RunStatus.failure, error="gmail: boom")
    _subject, body = build_message(run, {})
    assert "Sources :" not in body


def test_share_linkedin_button_only_when_published() -> None:
    published = _run(RunStatus.success, steps=[_github_success()])
    _subject, body = build_message(published, {"article": _ARTICLE})
    assert "linkedin.com/sharing/share-offsite" in body

    steps = [
        RunStep(
            name=StepName.github,
            status=RunStatus.failure,
            started_at=T0,
            ended_at=T1,
            error="commit failed",
        )
    ]
    not_published = _run(RunStatus.failure, steps=steps, error="github: commit failed")
    _subject, body = build_message(not_published, {"article": _ARTICLE})
    assert "linkedin.com/sharing/share-offsite" not in body
