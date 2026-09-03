"""End-to-end: the full fake pipeline, plus a gated real Imagen/GitHub smoke.

The fake e2e drives the whole nine-step pipeline through `run_pipeline` with every external
boundary faked, proving the "publishable article" path: the article, its hero image and the
LinkedIn post are all committed, at the paths the Astro site actually reads.

The `integration` test is deselected by default (`addopts = -m 'not integration'`); run it with
`uv run pytest -m integration` on a host holding the Gemini and GitHub secrets.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import pytest

from minion.config import PARIS_TZ
from minion.fiches.fakes import FakeFicheGenerateRunner
from minion.generate.fakes import FakeGenerateRunner
from minion.ingest.fakes import FakeGmailClient, FakeScraperClient
from minion.ingest.models import Newsletter
from minion.models import RunStatus
from minion.orchestrator import run_pipeline
from minion.publish.fakes import FakeContentRepository, FakeImageGenerator, FakePromptRewriter
from minion.publish.ports import ImagenBlockedError
from minion.publish.serialize import slugify
from minion.steps import build_pipeline

DATE = "2026-06-01"
T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)
URLS = [f"https://x.com/{i}" for i in range(6)]  # ≥5 → passes validate_input

MD_PATH = f"site/src/content/articles/{DATE}.md"
IMAGE_PATH = f"site/public/images/{DATE}.png"
LINKEDIN_PATH = f"linkedin/{DATE}.md"


def _artifact(**overrides: Any) -> str:
    payload: dict[str, Any] = {
        "theme": "IA",
        "frontmatter": {
            "title": "Daily AI Watch",
            "date": "2026-06-01",
            "themes": ["IA"],
        },
        "body": "a clean synthesis body",
        "linkedin": "a post",
        "image_prompt": "a watchful owl",
    }
    payload.update(overrides)
    return json.dumps(payload)


def _pipeline(
    content_repo: FakeContentRepository,
    image_gen: FakeImageGenerator,
    *,
    gmail: FakeGmailClient | None = None,
    generate_output: str | None = None,
    fiche_runner: FakeFicheGenerateRunner | None = None,
) -> tuple[Any, ...]:
    return build_pipeline(
        gmail
        or FakeGmailClient(
            [Newsletter(sender="a@x.com", subject="s", received_at=T0, candidate_urls=URLS)]
        ),
        FakeScraperClient(),
        FakeGenerateRunner(outputs=[generate_output or _artifact()]),
        image_gen,
        FakePromptRewriter(),
        content_repo,
        fiche_runner or FakeFicheGenerateRunner(),
    )


def test_full_fake_pipeline_publishes_article(run_store, lock_store, clock) -> None:
    content_repo = FakeContentRepository()
    steps = _pipeline(content_repo, FakeImageGenerator(outcomes=[b"HEROIMG"]))

    final = run_pipeline(DATE, run_store=run_store, lock_store=lock_store, clock=clock, steps=steps)

    assert final.status is RunStatus.success
    assert len(final.steps) == 9 and all(s.status is RunStatus.success for s in final.steps)

    # One commit for the whole day's article — no cited sources here, so no second (fiches)
    # commit follows it.
    assert len(content_repo.calls) == 1
    committed = content_repo.calls[0].path_content()
    # The three published artefacts, at the paths the site and the operator read.
    assert committed[IMAGE_PATH] == b"HEROIMG"
    assert b'title: "Daily AI Watch"' in committed[MD_PATH]
    assert f"image: {DATE}.png".encode() in committed[MD_PATH]
    assert b"a post" in committed[LINKEDIN_PATH]


def test_full_fake_pipeline_fiches_cited_sources_and_survives_a_failure(
    run_store, lock_store, clock
) -> None:
    # Distinct domains, not the shared module-level `URLS` (which are all `x.com/N`): the
    # copyright validator's `missing_attribution` check flags an ingested-but-uncited source as
    # unattributed once its *domain* appears anywhere in the prose — same-domain sources would
    # spuriously fail generate validation the moment any one of them gets cited.
    urls = [f"https://source{i}.example/a" for i in range(6)]
    # `urls[0]`/`urls[1]` are cited; `urls[2:]` are ingested but never referenced, so only the
    # cited two should be ficheable — the whole point of the "only cited sources" scope decision.
    article_body = (
        "a clean synthesis body\n\n## Sources\n\n"
        f"1. [Title for {urls[0]}]({urls[0]})\n2. [Title for {urls[1]}]({urls[1]})\n"
    )
    fiche_body = (
        "## Résumé\nx\n\n## Points clés\n- a\n\n## Analyse approfondie\ny\n\n"
        "## Pourquoi ça compte\nz"
    )
    fiche_runner = FakeFicheGenerateRunner(
        outputs={urls[0]: json.dumps({"theme": "IA", "keywords": [], "body": fiche_body})},
        fail_urls=frozenset({urls[1]}),
    )
    content_repo = FakeContentRepository()
    steps = _pipeline(
        content_repo,
        FakeImageGenerator(outcomes=[b"HEROIMG"]),
        gmail=FakeGmailClient(
            [Newsletter(sender="a@x.com", subject="s", received_at=T0, candidate_urls=urls)]
        ),
        generate_output=_artifact(body=article_body),
        fiche_runner=fiche_runner,
    )

    final = run_pipeline(DATE, run_store=run_store, lock_store=lock_store, clock=clock, steps=steps)

    # The article publishes normally despite the fiche failure — fiches are never on its
    # critical path.
    assert final.status is RunStatus.success_with_warnings
    # Two commits: the article's own batch, then one more for every fiche that survived.
    assert len(content_repo.calls) == 2
    paths: set[str] = set()
    for call in content_repo.calls:
        paths |= set(call.path_content())
    assert MD_PATH in paths and IMAGE_PATH in paths and LINKEDIN_PATH in paths

    # Only the two cited sources were ever invoked — the never-referenced urls[2:] were skipped.
    assert set(fiche_runner.calls) == {urls[0], urls[1]}
    ok_slug = slugify(f"Title for {urls[0]}")
    failed_slug = slugify(f"Title for {urls[1]}")
    assert f"site/src/content/fiches/{DATE}-{ok_slug}.md" in paths
    assert f"site/src/content/fiches/{DATE}-{failed_slug}.md" not in paths  # scripted failure


def test_full_fake_pipeline_ships_the_article_when_imagen_gives_up(
    run_store, lock_store, clock
) -> None:
    content_repo = FakeContentRepository()
    # Imagen always rejects → the rewrite retry also rejects → ship without a hero image.
    image_gen = FakeImageGenerator(outcomes=[ImagenBlockedError("x"), ImagenBlockedError("y")])
    steps = _pipeline(content_repo, image_gen)

    final = run_pipeline(DATE, run_store=run_store, lock_store=lock_store, clock=clock, steps=steps)

    assert final.status is RunStatus.success_with_warnings
    assert len(content_repo.calls) == 1  # still one commit, just without the image file
    committed = content_repo.calls[0].path_content()
    assert IMAGE_PATH not in committed  # nothing to commit
    assert MD_PATH in committed and LINKEDIN_PATH in committed
    assert b"image:" not in committed[MD_PATH]  # the site falls back to its placeholder SVG


@pytest.mark.integration
def test_real_imagen_and_github_smoke() -> None:
    """Real Imagen generation + a GitHub commit round-trip (secrets required)."""
    from minion import config
    from minion.publish.github import GitHubContentRepository
    from minion.publish.imagen import GeminiImageGenerator
    from minion.secrets import MissingSecretError, require

    for secret in (config.GITHUB_PAT_SECRET, config.GEMINI_API_KEY_SECRET):
        try:
            require(secret)
        except MissingSecretError:
            pytest.skip(f"{secret} not provisioned")

    png = GeminiImageGenerator().generate(f"A simple test image. {config.IMAGEN_BRAND_TEMPLATE}")
    assert png[:8] == b"\x89PNG\r\n\x1a\n"  # PNG signature
    sha = GitHubContentRepository().put_files(
        [("site/public/images/_smoke.png", png)], "chore: imagen+github smoke"
    )
    assert isinstance(sha, str) and sha
