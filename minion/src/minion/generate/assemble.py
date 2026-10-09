"""Deterministic context assembly for `/generate`.

Turns the validated `SourceSet` into the `AssembledContext` the agent consumes: only
`ok` sources, ordered by sender weight, with GenAI-centred sources capped to a share of the
mix, trimmed so the estimated token count fits the 500k input budget. Every cut is logged —
never silent.
"""

from __future__ import annotations

import math

from minion import config
from minion.generate.classify import classify
from minion.generate.models import AssembledContext, ContextSource
from minion.generate.validate import estimate_tokens
from minion.ingest.models import SourceSet
from minion.logging import BoundLogger


def _ai_cap(non_ai: int) -> int:
    """How many IA-hinted sources keep the context at or under MAX_AI_SOURCE_FRACTION.

    Floored at MIN_AI_SOURCES_KEPT, so a day whose inbox is nearly all GenAI still yields
    enough material to write from — /generate is then asked for the non-GenAI angle in it.
    """
    fraction = config.MAX_AI_SOURCE_FRACTION
    proportional = math.floor(non_ai * fraction / (1 - fraction)) if fraction < 1 else non_ai
    return max(config.MIN_AI_SOURCES_KEPT, proportional)


def assemble_context(
    source_set: SourceSet, *, weights: dict[str, float] | None = None, log: BoundLogger
) -> AssembledContext:
    """Select OK sources by weight, cap the IA share, then fit the input-token budget.

    Sources are first stable-sorted by `weights` (descending, unlisted URLs default to 1.0), so a
    low-weight sender's links sort toward the end and are the first cut; ties keep their original
    (fetch) order. They are also deduped by title (first-seen kept): the same article is sometimes
    syndicated across multiple newsletter editions with distinct tracking-wrapper URLs (e.g. TLDR
    Dev and TLDR AI both linking the same post). Left undeduped, the model cites one URL while the
    article prose still names the shared title, which makes the copyright validator's
    title-attribution check flag the other, uncited duplicate as "referenced but not linked"
    (2026-07-31 burn-in).

    Each survivor gets a keyword `theme_hint`; IA-hinted sources beyond `_ai_cap` are dropped,
    lowest weight first, so GenAI cannot crowd out the Data/Software/Leadership material the
    editorial line asks for.
    """
    ordered = sorted(source_set.ok_sources, key=lambda s: -(weights or {}).get(s.url, 1.0))

    candidates: list[ContextSource] = []
    seen_titles: set[str] = set()
    for source in ordered:
        title_key = (source.title or "").strip().lower()
        if title_key and title_key in seen_titles:
            continue
        if title_key:
            seen_titles.add(title_key)
        title = source.title or ""
        markdown = source.markdown or ""
        candidates.append(
            ContextSource(
                url=source.url,
                title=title,
                markdown=markdown,
                theme_hint=classify(title, markdown),
            )
        )

    ai_total = sum(c.theme_hint == "IA" for c in candidates)
    ai_allowed = _ai_cap(len(candidates) - ai_total)
    if ai_total > ai_allowed:
        kept_ai = 0
        mixed: list[ContextSource] = []
        for candidate in candidates:
            if candidate.theme_hint == "IA":
                kept_ai += 1
                if kept_ai > ai_allowed:
                    continue
            mixed.append(candidate)
        log.info(
            "ia sources capped",
            extra={"ia_total": ai_total, "ia_kept": ai_allowed, "dropped": ai_total - ai_allowed},
        )
        candidates = mixed

    selected: list[ContextSource] = []
    used_tokens = 0
    for candidate in candidates:
        cost = (
            estimate_tokens(candidate.markdown)
            + estimate_tokens(candidate.url)
            + estimate_tokens(candidate.title)
        )
        if used_tokens + cost > config.MAX_GENERATE_INPUT_TOKENS:
            log.info(
                "context truncated to fit input budget",
                extra={
                    "kept": len(selected),
                    "dropped": len(candidates) - len(selected),
                    "est_tokens": used_tokens,
                },
            )
            break
        selected.append(candidate)
        used_tokens += cost

    log.info(
        "context assembled",
        extra={
            "sources": len(selected),
            "theme_mix": {
                theme: sum(s.theme_hint == theme for s in selected)
                for theme in config.THEME_PRIORITY
            },
        },
    )
    return AssembledContext(sources=selected)
