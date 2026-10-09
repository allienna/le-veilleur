"""Real ingestion steps: `gmail`, `scrape`, `validate_input`.

The first three pipeline slots. Each step depends only on an injected client Protocol
(`GmailClient` / `ScraperClient`) so the pipeline runs hermetically under fakes.

Data bag contract between the steps:
- `gmail`          → writes `newsletters: list[Newsletter]`, `candidate_urls: list[str]`,
                     `source_weights: dict[str, float]`
- `scrape`         → reads `candidate_urls`, writes `sources: SourceSet`
- `validate_input` → reads `newsletters` + `sources`, gates the run
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from email.utils import parseaddr
from typing import cast
from urllib.parse import urlparse

from minion import config
from minion.ingest.models import Newsletter, SourceOutcome, SourceSet
from minion.ingest.ports import GmailClient, ScraperClient
from minion.models import RunStatus, StepName
from minion.steps.base import StepContext, StepResult


class InsufficientSourcesError(RuntimeError):
    """Raised by `validate_input` when too few sources scraped OK to publish."""


def _sender_address(sender: str) -> str:
    """Lowercased email address parsed from a raw `From` header value."""
    _, address = parseaddr(sender)
    return address.lower()


def _is_denied(sender: str, denylist: frozenset[str]) -> bool:
    """True if `sender` matches the denylist by full address or `@domain` suffix."""
    address = _sender_address(sender)
    if not address:
        return False
    for raw in denylist:
        entry = raw.lower()
        if entry.startswith("@"):
            if address.endswith(entry):
                return True
        elif address == entry:
            return True
    return False


def _weight_for(
    newsletter: Newsletter,
    weights: dict[str, float],
    subject_weights: dict[str, float],
) -> float:
    """Configured weight for one newsletter, default 1.0.

    The longest matching subject prefix wins first (case-insensitive) — that is the only way to
    tell apart editions sharing one sender, e.g. TLDR AI vs TLDR Data. Then the sender: exact
    address, then `@domain` suffix.
    """
    subject = newsletter.subject.strip().lower()
    prefixes = [p for p in subject_weights if subject.startswith(p.lower())]
    if prefixes:
        return subject_weights[max(prefixes, key=len)]
    address = _sender_address(newsletter.sender)
    if not address:
        return 1.0
    if address in weights:
        return weights[address]
    for key, weight in weights.items():
        if key.startswith("@") and address.endswith(key.lower()):
            return weight
    return 1.0


def _interleave(
    queues: list[tuple[float, list[str]]], cap: int
) -> tuple[list[str], dict[str, float], list[int]]:
    """Weighted round-robin over per-newsletter URL queues, deduped, stopped at `cap`.

    Smooth weighted round-robin (the nginx scheme): every turn each non-empty queue gains its
    weight in credit, the richest queue (first on ties, i.e. fetch order) yields its next unseen
    URL and pays back the turn's total. Over any window each newsletter's share of picks tracks
    its share of the weight, so the cap trims every sender proportionally instead of keeping
    whoever arrived first. Returns the URLs, each URL's weight, and how many each queue gave.
    """
    pending = [list(urls) for _, urls in queues]
    credit = [0.0] * len(queues)
    taken = [0] * len(queues)
    seen: set[str] = set()
    urls: list[str] = []
    weights: dict[str, float] = {}

    while len(urls) < cap:
        # Drop already-seen heads so an exhausted queue stops competing for turns.
        for queue in pending:
            while queue and queue[0] in seen:
                queue.pop(0)
        active = [i for i, queue in enumerate(pending) if queue]
        if not active:
            break
        for i in active:
            credit[i] += queues[i][0]
        pick = max(active, key=lambda i: credit[i])  # max() keeps the first on ties
        credit[pick] -= sum(queues[i][0] for i in active)
        url = pending[pick].pop(0)
        seen.add(url)
        urls.append(url)
        weights[url] = queues[pick][0]
        taken[pick] += 1

    return urls, weights, taken


@dataclass
class GmailStep:
    """Step 1: fetch unread newsletters, apply the denylist, extract+dedupe+cap article URLs."""

    client: GmailClient
    name: StepName = StepName.gmail

    def run(self, ctx: StepContext) -> StepResult:
        newsletters = self.client.fetch_unread(ctx.date)
        kept = [n for n in newsletters if not _is_denied(n.sender, config.EXCLUDED_SENDERS)]

        queues = [
            (
                _weight_for(n, config.NEWSLETTER_WEIGHTS, config.NEWSLETTER_SUBJECT_WEIGHTS),
                n.candidate_urls,
            )
            for n in kept
        ]
        total = len({url for _, urls in queues for url in urls})
        urls, source_weights, taken = _interleave(queues, config.MAX_URLS)
        if total > config.MAX_URLS:
            ctx.log.info("url cap reached", extra={"total": total, "capped_to": config.MAX_URLS})

        ctx.log.info(
            "gmail fetched",
            extra={
                "fetched": len(newsletters),
                "kept": len(kept),
                "urls": len(urls),
                # What each newsletter contributed after the cap — the input to tune weights.
                "per_sender": [
                    {
                        "sender": _sender_address(n.sender),
                        "subject": n.subject[:80],
                        "weight": weight,
                        "candidates": len(n.candidate_urls),
                        "kept": count,
                    }
                    for n, (weight, _), count in zip(kept, queues, taken, strict=True)
                ],
            },
        )
        payload: dict[str, object] = {
            "newsletters": kept,
            "candidate_urls": urls,
            "source_weights": source_weights,
        }
        return StepResult(payload=payload)


@dataclass
class ScrapeStep:
    """Step 2: scrape the candidate URLs to clean Markdown, preserving per-source outcomes."""

    client: ScraperClient
    name: StepName = StepName.scrape

    def run(self, ctx: StepContext) -> StepResult:
        urls = cast("list[str]", ctx.data.get("candidate_urls", []))
        sources = SourceSet(sources=self.client.scrape(urls))
        ctx.log.info(
            "scrape complete",
            extra={
                "ok": sources.ok_count,
                "paywalled": sources.paywalled_count,
                "failed": sources.failed_count,
                "total": sources.total,
            },
        )
        failed = [s for s in sources.sources if s.outcome is SourceOutcome.failed]
        if failed:
            # Diagnoses *why* the run's failed bucket is large — one bad host vs. a broad
            # failure mode (e.g. every source getting non_html_content_type) look identical in
            # the aggregate counts above but need very different fixes.
            by_reason = Counter(s.failure_reason for s in failed)
            by_host = Counter(urlparse(s.url).netloc for s in failed)
            ctx.log.info(
                "scrape failures breakdown",
                extra={
                    "by_reason": dict(by_reason.most_common()),
                    "by_host": dict(by_host.most_common(10)),
                },
            )
        return StepResult(payload={"sources": sources})


@dataclass
class ValidateInputStep:
    """Step 3: the quality gate. Skip an empty mailbox; gate on the ≥50%-AND-≥5 threshold, or on
    ≥MIN_SOURCES_OK_UNCONDITIONAL OK sources regardless of fraction."""

    name: StepName = StepName.validate_input

    def run(self, ctx: StepContext) -> StepResult:
        sources = cast("SourceSet", ctx.data.get("sources") or SourceSet(sources=[]))

        if sources.total == 0:
            # Empty mailbox / no usable URLs → graceful skip, not a failure.
            ctx.log.info("no sources; skipping run", extra={"reason": "no_sources"})
            return StepResult(terminal_status=RunStatus.skipped, reason="no_sources")

        ok, total = sources.ok_count, sources.total
        fraction = ok / total
        meets_fraction_gate = (
            ok >= config.MIN_SOURCES_OK and fraction >= config.MIN_SOURCES_FRACTION
        )
        meets_volume_override = ok >= config.MIN_SOURCES_OK_UNCONDITIONAL
        if not (meets_fraction_gate or meets_volume_override):
            # Include the paywalled/failed split so a thin-news day (mostly paywalled) is
            # distinguishable from scrape trouble (mostly failed — fetch errors / dead links).
            raise InsufficientSourcesError(
                f"insufficient_sources: {ok}/{total} ok "
                f"({sources.paywalled_count} paywalled, {sources.failed_count} failed; "
                f"need ≥{config.MIN_SOURCES_OK} and ≥{config.MIN_SOURCES_FRACTION:.0%}, "
                f"or ≥{config.MIN_SOURCES_OK_UNCONDITIONAL} regardless of fraction)"
            )

        ctx.log.info(
            "input validated",
            extra={
                "ok": ok,
                "paywalled": sources.paywalled_count,
                "failed": sources.failed_count,
                "total": total,
                "via_volume_override": not meets_fraction_gate,
            },
        )
        return StepResult()
