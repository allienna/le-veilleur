"""Tests for the deterministic keyword theme hint."""

from __future__ import annotations

from minion import config
from minion.generate.classify import classify


def test_genai_source_is_ia() -> None:
    assert classify("GPT-6 tops every benchmark", "OpenAI released a new LLM today.") == "IA"


def test_data_source_is_data() -> None:
    title = "The age of domain-optimized analytical databases on DataFusion"
    assert classify(title, "Lakehouse, Iceberg and DuckDB reshape the warehouse.") == "Data"


def test_software_source_is_software() -> None:
    title = "Worker Backpressure (Part 1) - Canva Engineering Blog"
    assert classify(title, "Our queue workers slow down when distributed dependencies fail.") == (
        "Software"
    )


def test_title_outweighs_a_passing_body_mention() -> None:
    assert classify("Hiring your first engineering manager", "Some teams use an LLM.") == (
        "Leadership"
    )


def test_keywords_match_whole_words_only() -> None:
    # "ai" must not fire inside "maintain" / "detail".
    assert classify("How we maintain detail", "") == config.DEFAULT_THEME


def test_no_hit_falls_back_to_the_default_theme() -> None:
    assert classify("Untitled", "lorem ipsum") == config.DEFAULT_THEME


def test_every_keyword_theme_is_in_the_allowlist() -> None:
    assert set(config.THEME_KEYWORDS) <= config.THEME_ALLOWLIST


def test_passing_ai_mentions_do_not_make_a_leadership_piece_ia() -> None:
    title = "What makes a great engineering manager"
    body = "AI tools help. An LLM can draft notes. But hiring, feedback and team culture matter."
    assert classify(title, body) == "Leadership"
