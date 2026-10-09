"""Tests for deterministic context assembly."""

from __future__ import annotations

import pytest

from minion import config
from minion.generate.assemble import assemble_context
from minion.ingest.models import ScrapedSource, SourceOutcome, SourceSet
from minion.logging import bind

LOG = bind("RUN")


def _ok(i: int, markdown: str = "body") -> ScrapedSource:
    return ScrapedSource(
        url=f"https://s.io/{i}", outcome=SourceOutcome.ok, title=f"T{i}", markdown=markdown
    )


def test_selects_only_ok_sources_in_order() -> None:
    source_set = SourceSet(
        sources=[
            _ok(0),
            ScrapedSource(url="https://pay.io", outcome=SourceOutcome.paywalled),
            _ok(1),
            ScrapedSource(url="https://down.io", outcome=SourceOutcome.failed),
            _ok(2),
        ]
    )
    context = assemble_context(source_set, log=LOG)
    assert [s.url for s in context.sources] == [
        "https://s.io/0",
        "https://s.io/1",
        "https://s.io/2",
    ]


def test_carries_title_and_markdown() -> None:
    context = assemble_context(SourceSet(sources=[_ok(0, markdown="# heading\n\ntext")]), log=LOG)
    assert context.sources[0].title == "T0"
    assert context.sources[0].markdown == "# heading\n\ntext"


def test_truncates_to_input_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    # Tiny budget so only the first couple of sources fit; the rest are dropped.
    monkeypatch.setattr(config, "MAX_GENERATE_INPUT_TOKENS", 30)
    big = "x" * 40  # ~10 tokens of markdown alone, plus url/title
    source_set = SourceSet(sources=[_ok(i, markdown=big) for i in range(10)])
    context = assemble_context(source_set, log=LOG)
    assert 0 < len(context.sources) < 10  # truncated


def test_empty_source_set_yields_empty_context() -> None:
    assert assemble_context(SourceSet(sources=[]), log=LOG).sources == []


def test_orders_by_weight_descending_stable_on_ties() -> None:
    source_set = SourceSet(sources=[_ok(0), _ok(1), _ok(2)])
    context = assemble_context(
        source_set, weights={"https://s.io/0": 0.1, "https://s.io/2": 5.0}, log=LOG
    )
    # 2 (weight 5.0) first, then 1 (default 1.0, tie broken by original order), then 0 (0.1).
    assert [s.url for s in context.sources] == [
        "https://s.io/2",
        "https://s.io/1",
        "https://s.io/0",
    ]


def test_low_weight_source_dropped_before_high_weight_under_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(config, "MAX_GENERATE_INPUT_TOKENS", 30)
    big = "x" * 40
    source_set = SourceSet(sources=[_ok(i, markdown=big) for i in range(3)])
    context = assemble_context(
        source_set, weights={"https://s.io/0": 0.1, "https://s.io/1": 0.1}, log=LOG
    )
    urls = [s.url for s in context.sources]
    assert "https://s.io/2" in urls
    assert "https://s.io/0" not in urls or "https://s.io/1" not in urls


def test_dedupes_by_title_keeping_first_seen() -> None:
    # Same article syndicated across two newsletter editions with distinct tracking URLs but an
    # identical title — only the first-seen copy should survive (2026-07-31 burn-in).
    dup = ScrapedSource(
        url="https://tracking.example.com/edition-a/real-post",
        outcome=SourceOutcome.ok,
        title="How ChatGPT Optimizes Its Agent Loop",
        markdown="body a",
    )
    dup_other_edition = ScrapedSource(
        url="https://tracking.example.com/edition-b/real-post",
        outcome=SourceOutcome.ok,
        title="How ChatGPT Optimizes Its Agent Loop",
        markdown="body b",
    )
    context = assemble_context(SourceSet(sources=[dup, dup_other_edition, _ok(0)]), log=LOG)
    assert [s.url for s in context.sources] == [
        "https://tracking.example.com/edition-a/real-post",
        "https://s.io/0",
    ]


def _themed(i: int, title: str) -> ScrapedSource:
    return ScrapedSource(
        url=f"https://t.io/{i}", outcome=SourceOutcome.ok, title=title, markdown="body"
    )


def test_sources_carry_a_theme_hint() -> None:
    source_set = SourceSet(sources=[_themed(0, "A new LLM agent"), _themed(1, "dbt and Iceberg")])
    context = assemble_context(source_set, log=LOG)
    assert [s.theme_hint for s in context.sources] == ["IA", "Data"]


def test_ia_sources_capped_to_a_share_of_the_context(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "MIN_AI_SOURCES_KEPT", 0)
    ai = [_themed(i, f"LLM agent news {i}") for i in range(20)]
    data = [_themed(100 + i, f"Lakehouse pipeline {i}") for i in range(7)]
    context = assemble_context(SourceSet(sources=ai + data), log=LOG)
    hints = [s.theme_hint for s in context.sources]
    assert hints.count("Data") == 7
    assert hints.count("IA") == 3  # floor(7 * 0.3 / 0.7)


def test_ia_cap_drops_the_lowest_weight_ia_sources_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(config, "MIN_AI_SOURCES_KEPT", 1)
    ai = [_themed(i, f"LLM agent news {i}") for i in range(3)]
    context = assemble_context(SourceSet(sources=ai), weights={"https://t.io/2": 5.0}, log=LOG)
    assert [s.url for s in context.sources] == ["https://t.io/2"]


def test_ia_floor_keeps_an_all_genai_day_writable() -> None:
    ai = [_themed(i, f"LLM agent news {i}") for i in range(12)]
    context = assemble_context(SourceSet(sources=ai), log=LOG)
    assert len(context.sources) == config.MIN_AI_SOURCES_KEPT
