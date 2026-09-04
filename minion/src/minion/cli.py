"""Command-line entrypoint: `python -m minion run --date YYYY-MM-DD`.

The composition root — it configures logging, picks the real clock, builds the in-memory run
stores and the production clients, and drives `run_pipeline`. Clients are constructed lazily
(inside `build_clients`) so importing this module, and unit-testing the CLI, needs no
credentials at all.
"""

from __future__ import annotations

import re
from datetime import datetime

import click

from minion.clock import Clock, SystemClock
from minion.fiches.ports import FicheGenerateRunner
from minion.generate.ports import GenerateRunner
from minion.ingest.ports import GmailClient, ScraperClient
from minion.logging import bind, configure_logging
from minion.models import RunStatus
from minion.notify.message import build_message
from minion.notify.ports import Notifier, NotifyError
from minion.orchestrator import run_pipeline
from minion.publish.ports import ContentRepository, ImageGenerator, PromptRewriter
from minion.steps import build_pipeline
from minion.store.memory import InMemoryLockStore, InMemoryRunStore
from minion.store.ports import LockStore, RunStore

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_date(ctx: click.Context, param: click.Parameter, value: str | None) -> str | None:
    """Click callback: require a zero-padded, real YYYY-MM-DD."""
    if value is None:
        return None
    if not _DATE_RE.match(value):
        raise click.BadParameter("date must be YYYY-MM-DD (zero-padded)")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise click.BadParameter(f"not a real date: {value}") from exc
    return value


def build_stores(clock: Clock) -> tuple[RunStore, LockStore]:
    """Construct the run stores. In-process only: the durable trace is Cloud Logging, and the
    published artefacts are committed to the repo."""
    return InMemoryRunStore(), InMemoryLockStore(clock)


def build_clients() -> tuple[
    GmailClient,
    ScraperClient,
    GenerateRunner,
    ImageGenerator,
    PromptRewriter,
    ContentRepository,
    FicheGenerateRunner,
    Notifier,
]:
    """Construct the production ingestion / generation / publishing / notify clients (lazy —
    needs creds)."""
    from minion.fiches.runner import ClaudeFicheGenerateRunner
    from minion.generate.runner import ClaudeGenerateRunner
    from minion.ingest.gmail import GmailReaderClient
    from minion.ingest.scraper import LocalExtractorClient
    from minion.notify.gmail import GmailNotifier
    from minion.publish.github import GitHubContentRepository
    from minion.publish.imagen import ClaudePromptRewriter, GeminiImageGenerator

    return (
        GmailReaderClient(),
        LocalExtractorClient(),
        ClaudeGenerateRunner(),
        GeminiImageGenerator(),
        ClaudePromptRewriter(),
        GitHubContentRepository(),
        ClaudeFicheGenerateRunner(),
        GmailNotifier(),
    )


@click.group()
def cli() -> None:
    """Veilleur Minion — the daily tech-watch pipeline."""


@cli.command()
@click.option(
    "--date",
    default=None,
    callback=_validate_date,
    help="Run date YYYY-MM-DD (Europe/Paris). Defaults to today.",
)
def run(date: str | None) -> None:
    """Execute the pipeline for DATE (idempotent; replays overwrite)."""
    configure_logging()
    clock = SystemClock()
    target = date or clock.now().strftime("%Y-%m-%d")
    run_store, lock_store = build_stores(clock)
    (
        gmail_client,
        scraper_client,
        generate_runner,
        image_generator,
        prompt_rewriter,
        content_repo,
        fiche_runner,
        notifier,
    ) = build_clients()
    steps = build_pipeline(
        gmail_client,
        scraper_client,
        generate_runner,
        image_generator,
        prompt_rewriter,
        content_repo,
        fiche_runner,
    )
    data: dict[str, object] = {}
    result = run_pipeline(
        target,
        run_store=run_store,
        lock_store=lock_store,
        clock=clock,
        steps=steps,
        data_out=data,
    )
    if result.status is not RunStatus.aborted:
        # aborted means the concurrency guard refused to start a run at all — nothing happened,
        # nothing to report. Every other terminal status is notified, success or not: a notify
        # failure is logged and swallowed, never allowed to change the pipeline's own outcome.
        try:
            subject, body = build_message(result, data)
            notifier.send(subject=subject, body=body)
        except NotifyError:
            bind(result.run_id).exception("notify failed")
    if result.status is RunStatus.failure:
        raise SystemExit(1)
