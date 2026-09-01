"""CLI tests — date validation exit codes and an end-to-end wired stub run."""

from __future__ import annotations

from click.testing import CliRunner

from minion import cli as cli_mod
from minion.cli import cli
from minion.clock import Clock, SystemClock
from minion.fiches.fakes import FakeFicheGenerateRunner
from minion.fiches.ports import FicheGenerateRunner
from minion.generate.fakes import FakeGenerateRunner
from minion.generate.ports import GenerateRunner
from minion.ingest.fakes import FakeGmailClient, FakeScraperClient
from minion.ingest.ports import GmailClient, ScraperClient
from minion.publish.fakes import (
    FakeContentRepository,
    FakeImageGenerator,
    FakePromptRewriter,
)
from minion.publish.ports import ContentRepository, ImageGenerator, PromptRewriter
from minion.store.memory import InMemoryLockStore, InMemoryRunStore


def test_calendar_invalid_date_exits_nonzero() -> None:
    result = CliRunner().invoke(cli, ["run", "--date", "2026-13-40"])
    assert result.exit_code != 0
    assert "not a real date" in result.output


def test_malformed_date_exits_nonzero() -> None:
    result = CliRunner().invoke(cli, ["run", "--date", "nope"])
    assert result.exit_code != 0
    assert "YYYY-MM-DD" in result.output


def test_non_padded_date_rejected() -> None:
    result = CliRunner().invoke(cli, ["run", "--date", "2026-6-1"])
    assert result.exit_code != 0


def test_build_stores_needs_no_credentials() -> None:
    """The composition root must be importable and buildable with no secrets at all — the
    clients are the only credential-bearing part, and they are constructed lazily."""
    run_store, lock_store = cli_mod.build_stores(SystemClock())
    assert isinstance(run_store, InMemoryRunStore)
    assert isinstance(lock_store, InMemoryLockStore)


def test_wired_run_exits_zero(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    def fake_build(clock: Clock) -> tuple[InMemoryRunStore, InMemoryLockStore]:
        return InMemoryRunStore(), InMemoryLockStore(clock)

    def fake_clients() -> tuple[
        GmailClient,
        ScraperClient,
        GenerateRunner,
        ImageGenerator,
        PromptRewriter,
        ContentRepository,
        FicheGenerateRunner,
    ]:
        # Empty mailbox → the run skips at validate_input, before generate/imagen/github/fiches.
        return (
            FakeGmailClient(),
            FakeScraperClient(),
            FakeGenerateRunner(),
            FakeImageGenerator(),
            FakePromptRewriter(),
            FakeContentRepository(),
            FakeFicheGenerateRunner(),
        )

    monkeypatch.setattr(cli_mod, "build_stores", fake_build)
    monkeypatch.setattr(cli_mod, "build_clients", fake_clients)
    result = CliRunner().invoke(cli, ["run", "--date", "2026-06-01"])
    assert result.exit_code == 0, result.output  # skipped (no sources) is not a failure
