"""Fiche-internal generation artefact models.

Mirrors `minion.generate.models`: intermediate pipeline values carried between
`extract_cited_sources` and the `fiches` step.

`FicheDoc` is the shape serialized to `site/src/content/fiches/{date}-{slug}.md`; its field
set is the site's `fiches` collection (site/src/content/config.ts). `url`/`title` come from
the already-trusted `ContextSource`, never from the LLM's echo of them, so a hallucinated URL
can never reach the site.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ["FicheDoc", "FicheInvocation", "GeneratedFiche"]


class GeneratedFiche(BaseModel):
    """The artefact produced by one per-source fiche invocation."""

    model_config = ConfigDict(extra="forbid")

    theme: str
    keywords: list[str]
    authors: list[str] = []
    tone: str | None = None
    body: str  # markdown: ## Résumé, ## Points clés, ## Analyse approfondie, ## Pourquoi ça compte


class FicheDoc(BaseModel):
    """A fiche as published on the site — the site's `fiches` content-collection schema."""

    model_config = ConfigDict(extra="forbid")

    slug: str
    title: str
    date: str
    url: str
    authors: list[str] = []
    keywords: list[str] = []
    theme: str = "Autre"
    tone: str | None = None
    used_in: list[str] = []
    body: str


class FicheInvocation(BaseModel):
    """One fiche-generation call's result: the artefact text plus usage telemetry.

    Same shape as `minion.generate.models.GenerateInvocation` — `cost_usd`/`tokens` come from
    `claude --output-format json`; both None when the CLI didn't report them.
    """

    model_config = ConfigDict(extra="forbid")

    text: str
    cost_usd: float | None = None
    tokens: int | None = None
