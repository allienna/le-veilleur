"""Tests for ValidateInputStep — the skip path, the ≥50%-AND-≥5 gate, and the
≥MIN_SOURCES_OK_UNCONDITIONAL volume override."""

from __future__ import annotations

from datetime import datetime

import pytest

from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.ingest.models import ScrapedSource, SourceOutcome, SourceSet
from minion.logging import bind
from minion.models import RunStatus
from minion.steps.base import StepContext
from minion.steps.ingestion import InsufficientSourcesError, ValidateInputStep

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)


def _source_set(ok: int, not_ok: int, *, paywalled: int = 0) -> SourceSet:
    sources = [ScrapedSource(url=f"https://ok.io/{i}", outcome=SourceOutcome.ok) for i in range(ok)]
    sources += [
        ScrapedSource(url=f"https://bad.io/{i}", outcome=SourceOutcome.failed)
        for i in range(not_ok)
    ]
    sources += [
        ScrapedSource(url=f"https://wall.io/{i}", outcome=SourceOutcome.paywalled)
        for i in range(paywalled)
    ]
    return SourceSet(sources=sources)


def _ctx(sources: SourceSet | None) -> StepContext:
    data: dict[str, object] = {} if sources is None else {"sources": sources}
    return StepContext(
        run_id="RUN", date="2026-06-01", clock=FrozenClock(T0), log=bind("RUN"), data=data
    )


def test_no_sources_triggers_skip() -> None:
    result = ValidateInputStep().run(_ctx(_source_set(ok=0, not_ok=0)))
    assert result.terminal_status is RunStatus.skipped
    assert result.reason == "no_sources"


def test_missing_sources_key_triggers_skip() -> None:
    result = ValidateInputStep().run(_ctx(None))
    assert result.terminal_status is RunStatus.skipped
    assert result.reason == "no_sources"


def test_passes_at_threshold_boundary() -> None:
    # 5 ok of 10 → ok_count == 5 (≥5) and fraction == 0.5 (≥0.5): passes.
    result = ValidateInputStep().run(_ctx(_source_set(ok=5, not_ok=5)))
    assert result.terminal_status is None


def test_fails_on_count_below_minimum() -> None:
    # 4 ok of 4 → fraction 1.0 but only 4 OK (<5): fails.
    with pytest.raises(InsufficientSourcesError, match="4/4"):
        ValidateInputStep().run(_ctx(_source_set(ok=4, not_ok=0)))


def test_fails_on_fraction_below_half() -> None:
    # 6 ok of 13 → ≥5 OK but fraction ≈0.46 (<0.5): fails.
    with pytest.raises(InsufficientSourcesError, match="6/13"):
        ValidateInputStep().run(_ctx(_source_set(ok=6, not_ok=7)))


def test_source_set_counts_outcomes() -> None:
    s = _source_set(ok=3, not_ok=4, paywalled=2)
    assert (s.ok_count, s.failed_count, s.paywalled_count, s.total) == (3, 4, 2, 9)


def test_failure_message_breaks_down_paywalled_vs_failed() -> None:
    # The breakdown tells a thin-news day (paywalled) apart from scrape trouble (failed).
    with pytest.raises(InsufficientSourcesError, match=r"4/12.*1 paywalled, 7 failed"):
        ValidateInputStep().run(_ctx(_source_set(ok=4, not_ok=7, paywalled=1)))


def test_volume_override_passes_despite_low_fraction() -> None:
    # 35 ok of 105 → fraction ≈0.33 (<0.5), but ok ≥ MIN_SOURCES_OK_UNCONDITIONAL (30): passes
    # anyway (2026-09-05 burn-in: tracking-redirect 403s tanked the fraction on a day with
    # plenty of real, usable sources).
    result = ValidateInputStep().run(_ctx(_source_set(ok=35, not_ok=70)))
    assert result.terminal_status is None


def test_just_under_volume_override_still_fails_on_low_fraction() -> None:
    # 29 ok of 105 → fraction ≈0.28 (<0.5) and ok just below the override threshold (30): fails.
    with pytest.raises(InsufficientSourcesError, match="29/105"):
        ValidateInputStep().run(_ctx(_source_set(ok=29, not_ok=76)))
