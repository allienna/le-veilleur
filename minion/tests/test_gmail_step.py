"""Tests for GmailStep over FakeGmailClient."""

from __future__ import annotations

from datetime import datetime

import pytest

from minion import config
from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.ingest.fakes import FakeGmailClient
from minion.ingest.models import Newsletter
from minion.logging import bind
from minion.steps.base import StepContext
from minion.steps.ingestion import GmailStep

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)


def _ctx() -> StepContext:
    return StepContext(run_id="RUN", date="2026-06-01", clock=FrozenClock(T0), log=bind("RUN"))


def _newsletter(sender: str, urls: list[str], subject: str = "s") -> Newsletter:
    return Newsletter(sender=sender, subject=subject, received_at=T0, candidate_urls=urls)


def test_collects_and_dedupes_urls_across_newsletters() -> None:
    client = FakeGmailClient(
        newsletters=[
            _newsletter("a@x.com", ["https://x.com/1", "https://x.com/2"]),
            _newsletter("b@y.com", ["https://x.com/2", "https://y.com/3"]),
        ]
    )
    result = GmailStep(client=client).run(_ctx())
    assert result.payload["candidate_urls"] == [
        "https://x.com/1",
        "https://x.com/2",
        "https://y.com/3",
    ]
    assert len(result.payload["newsletters"]) == 2  # type: ignore[arg-type]


def test_denylist_filters_by_domain(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "EXCLUDED_SENDERS", frozenset({"@spam.com"}))
    client = FakeGmailClient(
        newsletters=[
            _newsletter("Promo <promo@spam.com>", ["https://spam.com/ad"]),
            _newsletter("Real <news@good.com>", ["https://good.com/post"]),
        ]
    )
    result = GmailStep(client=client).run(_ctx())
    assert result.payload["candidate_urls"] == ["https://good.com/post"]
    assert len(result.payload["newsletters"]) == 1  # type: ignore[arg-type]


def test_denylist_filters_by_exact_address(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "EXCLUDED_SENDERS", frozenset({"noisy@news.com"}))
    client = FakeGmailClient(newsletters=[_newsletter("noisy@news.com", ["https://news.com/x"])])
    result = GmailStep(client=client).run(_ctx())
    assert result.payload["candidate_urls"] == []


def test_url_cap_truncates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "MAX_URLS", 3)
    client = FakeGmailClient(
        newsletters=[_newsletter("a@x.com", [f"https://x.com/{i}" for i in range(10)])]
    )
    result = GmailStep(client=client).run(_ctx())
    assert len(result.payload["candidate_urls"]) == 3  # type: ignore[arg-type]


def test_source_weights_default_to_one() -> None:
    client = FakeGmailClient(newsletters=[_newsletter("a@x.com", ["https://x.com/1"])])
    result = GmailStep(client=client).run(_ctx())
    assert result.payload["source_weights"] == {"https://x.com/1": 1.0}


def test_source_weights_by_exact_address_and_domain(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "NEWSLETTER_WEIGHTS", {"@tldr.tech": 0.3, "noisy@news.com": 0.05})
    client = FakeGmailClient(
        newsletters=[
            _newsletter("Ed <ed@tldr.tech>", ["https://tldr.tech/1"]),
            _newsletter("noisy@news.com", ["https://news.com/1"]),
            _newsletter("Real <news@good.com>", ["https://good.com/1"]),
        ]
    )
    result = GmailStep(client=client).run(_ctx())
    assert result.payload["source_weights"] == {
        "https://tldr.tech/1": 0.3,
        "https://news.com/1": 0.05,
        "https://good.com/1": 1.0,
    }


def test_url_cap_shares_the_pool_across_newsletters(monkeypatch: pytest.MonkeyPatch) -> None:
    """A prolific sender arriving first no longer fills the whole pool (2026-10-09)."""
    monkeypatch.setattr(config, "MAX_URLS", 10)
    monkeypatch.setattr(config, "NEWSLETTER_WEIGHTS", {})
    client = FakeGmailClient(
        newsletters=[
            _newsletter("ed@tldr.tech", [f"https://tldr.tech/{i}" for i in range(80)]),
            _newsletter("ed@data.io", [f"https://data.io/{i}" for i in range(5)]),
        ]
    )
    urls: list[str] = GmailStep(client=client).run(_ctx()).payload["candidate_urls"]  # type: ignore[assignment]
    assert sum(u.startswith("https://data.io/") for u in urls) == 5
    assert len(urls) == 10


def test_url_cap_splits_the_pool_by_weight(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "MAX_URLS", 10)
    monkeypatch.setattr(config, "NEWSLETTER_WEIGHTS", {"@heavy.io": 4.0, "@light.io": 1.0})
    client = FakeGmailClient(
        newsletters=[
            _newsletter("a@light.io", [f"https://light.io/{i}" for i in range(20)]),
            _newsletter("b@heavy.io", [f"https://heavy.io/{i}" for i in range(20)]),
        ]
    )
    urls: list[str] = GmailStep(client=client).run(_ctx()).payload["candidate_urls"]  # type: ignore[assignment]
    assert sum(u.startswith("https://heavy.io/") for u in urls) == 8
    assert sum(u.startswith("https://light.io/") for u in urls) == 2


def test_subject_prefix_weight_overrides_sender_weight(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "NEWSLETTER_WEIGHTS", {"@tldr.tech": 0.8})
    monkeypatch.setattr(config, "NEWSLETTER_SUBJECT_WEIGHTS", {"TLDR": 0.5, "TLDR AI": 0.2})
    client = FakeGmailClient(
        newsletters=[
            _newsletter("ed@tldr.tech", ["https://a.io/1"], subject="tldr ai 2026-06-01"),
            _newsletter("ed@tldr.tech", ["https://d.io/1"], subject="TLDR Data 2026-06-01"),
            _newsletter("ed@tldr.tech", ["https://x.io/1"], subject="Weekly digest"),
        ]
    )
    result = GmailStep(client=client).run(_ctx())
    assert result.payload["source_weights"] == {
        "https://a.io/1": 0.2,  # longest prefix wins, case-insensitive
        "https://d.io/1": 0.5,
        "https://x.io/1": 0.8,  # no subject match: falls back to the sender
    }


def test_auth_failure_propagates() -> None:
    client = FakeGmailClient(error=RuntimeError("invalid_grant"))
    with pytest.raises(RuntimeError, match="invalid_grant"):
        GmailStep(client=client).run(_ctx())
