"""Shared fixtures: a frozen clock and in-memory stores wired for the orchestrator."""

from __future__ import annotations

from datetime import datetime

import pytest

from minion import config
from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.store.memory import InMemoryLockStore, InMemoryRunStore

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)


@pytest.fixture(autouse=True)
def _podcast_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every e2e/pipeline test built before the `podcast` step existed asserts exact commit
    counts and clean `success` statuses; opting every test out by default keeps those
    assertions accurate without threading a podcast fake through each one. Tests that actually
    exercise the podcast step (test_podcast_step.py) override this explicitly."""
    monkeypatch.setenv(config.PODCAST_ENABLED_ENV_VAR, "false")


@pytest.fixture
def clock() -> FrozenClock:
    return FrozenClock(T0)


@pytest.fixture
def run_store() -> InMemoryRunStore:
    return InMemoryRunStore()


@pytest.fixture
def lock_store(clock: FrozenClock) -> InMemoryLockStore:
    return InMemoryLockStore(clock)
