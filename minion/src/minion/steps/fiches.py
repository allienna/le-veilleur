"""Step 10 (final): per-source analysis, one fiche per cited source (F-016).

Data bag contract:
- reads `article: GeneratedArticle` + `context: AssembledContext`
- writes nothing new steps downstream depend on (this is the last step).

Each fiche is committed to `site/src/content/fiches/{date}-{slug}.md` through the same
`ContentRepository` the article uses.

Never raises: a failed fiche (transport error, unparseable output, failed structural validation)
is skipped and logged, not fatal. If at least one fiche fails, the step returns a `warning` —
the run still finishes as `success_with_warnings`, same mechanism as the Imagen placeholder
fallback. Placed last in `STEP_ORDER` so it can never block the article itself from shipping.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial

from pydantic import ValidationError as PydanticValidationError

from minion import config
from minion.fiches.extract import extract_cited_sources
from minion.fiches.models import FicheDoc, GeneratedFiche
from minion.fiches.parse import extract_json_object
from minion.fiches.ports import FicheGenerateRunner, FicheGenerateTransportError
from minion.fiches.validate import validate_fiche
from minion.generate.models import AssembledContext, ContextSource, GeneratedArticle
from minion.models import StepName
from minion.publish.ports import ContentRepoError, ContentRepository
from minion.publish.serialize import render_fiche, slugify
from minion.steps.base import StepContext, StepResult

# Run-level warning latched when at least one cited source fails to fiche (plan AD-4).
FICHE_PARTIAL_FAILURE_WARNING = "fiche_partial_failure"


def _require_article(ctx: StepContext) -> GeneratedArticle:
    article = ctx.data.get("article")
    if not isinstance(article, GeneratedArticle):
        raise RuntimeError("fiches step missing a GeneratedArticle in the data bag")
    return article


def _require_context(ctx: StepContext) -> AssembledContext:
    context = ctx.data.get("context")
    if not isinstance(context, AssembledContext):
        raise RuntimeError("fiches step missing an AssembledContext in the data bag")
    return context


@dataclass
class FichesStep:
    """Generates and persists one fiche per source cited in the published article."""

    runner: FicheGenerateRunner
    content_repo: ContentRepository
    sleep: Callable[[float], None] = time.sleep
    name: StepName = StepName.fiches

    def _invoke(self, source: ContextSource) -> str:
        """One logical invocation with transport-retry + exponential backoff, mirroring
        `GenerateStep._invoke` — but the caller catches everything, never re-raises past here."""
        for attempt in range(config.FICHE_TRANSPORT_RETRIES + 1):
            try:
                return self.runner.invoke(source).text
            except FicheGenerateTransportError:
                if attempt >= config.FICHE_TRANSPORT_RETRIES:
                    raise
                self.sleep(config.FICHE_BACKOFF_BASE.total_seconds() * (2**attempt))
        raise AssertionError("unreachable")  # pragma: no cover

    def _make_fiche(self, ctx: StepContext, source: ContextSource) -> FicheDoc | None:
        """Invoke, parse, validate, and build the persisted doc for one source. Returns None
        (after logging) on any failure — never raises."""
        try:
            raw = self._invoke(source)
            generated = GeneratedFiche.model_validate(extract_json_object(raw))
        except (
            FicheGenerateTransportError,
            json.JSONDecodeError,
            PydanticValidationError,
        ) as exc:
            ctx.log.warning(
                "fiche generation failed", extra={"url": source.url, "error": str(exc)[:300]}
            )
            return None

        report = validate_fiche(generated)
        if not report.ok:
            ctx.log.warning(
                "fiche failed validation",
                extra={"url": source.url, "errors": [e.code for e in report.errors]},
            )
            return None

        return FicheDoc(
            slug=slugify(source.title),
            title=source.title,
            date=ctx.date,
            url=source.url,
            authors=generated.authors,
            keywords=generated.keywords,
            theme=generated.theme,
            tone=generated.tone,
            used_in=[ctx.date],
            body=generated.body,
        )

    def run(self, ctx: StepContext) -> StepResult:
        article = _require_article(ctx)
        context = _require_context(ctx)
        cited = extract_cited_sources(article.body, context.sources)
        if not cited:
            ctx.log.info("no cited sources to fiche")
            return StepResult()

        with ThreadPoolExecutor(max_workers=config.FICHE_MAX_CONCURRENCY) as pool:
            docs = list(pool.map(partial(self._make_fiche, ctx), cited))

        generated_docs = [doc for doc in docs if doc is not None]
        succeeded: list[FicheDoc] = []
        for doc in generated_docs:
            path = config.FICHE_MD_PATH_TEMPLATE.format(date=ctx.date, slug=doc.slug)
            try:
                self.content_repo.put_file(
                    path, render_fiche(doc).encode("utf-8"), f"feat: add {ctx.date} fiches"
                )
            except ContentRepoError as exc:
                # A fiche that cannot be committed is skipped like one that failed to generate:
                # the article is already published by now, and no fiche is worth failing a run.
                ctx.log.warning(
                    "fiche commit failed", extra={"path": path, "error": str(exc)[:300]}
                )
                continue
            succeeded.append(doc)

        failed_count = len(cited) - len(succeeded)
        ctx.log.info(
            "fiches step done",
            extra={"cited": len(cited), "succeeded": len(succeeded), "failed": failed_count},
        )
        return StepResult(
            warning=FICHE_PARTIAL_FAILURE_WARNING if failed_count else None,
        )
