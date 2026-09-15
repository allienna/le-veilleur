"""Tests for the generation steps: assemble, the generate retry loop, validate_output gate
."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import pytest

from minion import config
from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.generate.fakes import FakeGenerateRunner
from minion.generate.models import AssembledContext, ValidationError, ValidationReport
from minion.generate.ports import GenerateTransportError
from minion.ingest.models import ScrapedSource, SourceOutcome, SourceSet
from minion.logging import bind
from minion.publish.fakes import FakeContentRepository
from minion.steps.base import StepContext
from minion.steps.generation import (
    AssembleStep,
    GenerateStep,
    GenerationFailedError,
    OutputValidationError,
    ValidateOutputStep,
)

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)


def _ctx(data: dict[str, Any]) -> StepContext:
    return StepContext(
        run_id="RUN", date="2026-06-01", clock=FrozenClock(T0), log=bind("RUN"), data=data
    )


def _artifact(**overrides: Any) -> str:
    payload: dict[str, Any] = {
        "theme": "ai",
        "frontmatter": {"title": "T", "date": "2026-06-02", "themes": ["IA"]},
        "body": "a clean synthesis body",
        "linkedin": "a post",
        "image_prompt": "a prompt",
    }
    payload.update(overrides)
    return json.dumps(payload)


# --- AssembleStep ----------------------------------------------------------------


def test_assemble_step_writes_context() -> None:
    sources = SourceSet(
        sources=[
            ScrapedSource(url="https://s.io/1", outcome=SourceOutcome.ok, title="T", markdown="m")
        ]
    )
    result = AssembleStep().run(_ctx({"sources": sources}))
    context = result.payload["context"]
    assert isinstance(context, AssembledContext)
    assert [s.url for s in context.sources] == ["https://s.io/1"]


# --- GenerateStep: parse / theme / transport -------------------------------------


def _step(runner: FakeGenerateRunner, **kwargs: Any) -> GenerateStep:
    return GenerateStep(runner=runner, content_repo=FakeContentRepository(), **kwargs)


def test_generate_parses_and_stores_article() -> None:
    runner = FakeGenerateRunner(outputs=[_artifact()])
    result = _step(runner).run(_ctx({"context": AssembledContext(sources=[])}))
    assert result.payload["article"] is not None
    report = result.payload["report"]
    assert isinstance(report, ValidationReport) and report.ok


def test_unknown_theme_normalized_to_the_default() -> None:
    runner = FakeGenerateRunner(outputs=[_artifact(theme="quantum-computing")])
    result = _step(runner).run(_ctx({"context": AssembledContext(sources=[])}))
    assert result.payload["article"].theme == config.DEFAULT_THEME  # type: ignore[union-attr]


def test_transport_error_retries_then_propagates() -> None:
    runner = FakeGenerateRunner(error=GenerateTransportError("boom"))
    step = _step(runner, sleep=lambda _s: None)
    with pytest.raises(GenerateTransportError):
        step.run(_ctx({"context": AssembledContext(sources=[])}))
    assert len(runner.calls) == 1 + config.CLAUDE_TRANSPORT_RETRIES  # initial + transport retries


def test_recent_history_from_content_repo_reaches_the_runner() -> None:
    from minion.models import RecentArticle
    from minion.publish.ports import ContentRepoError

    runner = FakeGenerateRunner(outputs=[_artifact()])
    history = [RecentArticle(date="2026-05-31", title="Hier", themes=["IA"])]
    step = GenerateStep(runner=runner, content_repo=FakeContentRepository(recent_articles=history))
    step.run(_ctx({"context": AssembledContext(sources=[])}))
    assert runner.history_calls[0] == history

    class _BrokenContentRepository(FakeContentRepository):
        def get_recent_articles(self, n: int) -> list[RecentArticle]:
            raise ContentRepoError("boom")

    runner2 = FakeGenerateRunner(outputs=[_artifact()])
    step2 = GenerateStep(runner=runner2, content_repo=_BrokenContentRepository())
    result = step2.run(_ctx({"context": AssembledContext(sources=[])}))
    assert result.payload["article"] is not None  # a history-read failure never fails the run
    assert runner2.history_calls[0] == []


# --- GenerateStep: validation retry loop -----------------------------------------


def test_invalid_then_valid_retries_with_feedback() -> None:
    runner = FakeGenerateRunner(outputs=[_artifact(linkedin="x" * 3001), _artifact()])
    step = _step(runner, sleep=lambda _s: None)
    result = step.run(_ctx({"context": AssembledContext(sources=[])}))
    assert result.payload["article"] is not None
    assert len(runner.calls) == 2  # one retry
    assert runner.calls[0] == []  # first attempt: no feedback
    assert any("LinkedIn" in msg for msg in runner.calls[1])  # errors fed back


def test_unparseable_output_is_retried() -> None:
    runner = FakeGenerateRunner(outputs=["this is not json", _artifact()])
    result = _step(runner, sleep=lambda _s: None).run(
        _ctx({"context": AssembledContext(sources=[])})
    )
    assert result.payload["article"] is not None
    assert len(runner.calls) == 2


def test_exhausted_validation_retries_raises() -> None:
    runner = FakeGenerateRunner(outputs=[_artifact(linkedin="x" * 3001)])  # always invalid
    step = _step(runner, sleep=lambda _s: None)
    with pytest.raises(GenerationFailedError, match="linkedin_too_long"):
        step.run(_ctx({"context": AssembledContext(sources=[])}))
    assert len(runner.calls) == 1 + config.MAX_GENERATE_RETRIES  # initial + validation retries


# --- ValidateOutputStep ----------------------------------------------------------


def test_validate_output_passes_on_ok_report() -> None:
    result = ValidateOutputStep().run(_ctx({"report": ValidationReport(errors=[])}))
    assert result.terminal_status is None


def test_validate_output_fails_closed_on_errors() -> None:
    report = ValidationReport(errors=[ValidationError(code="x", message="bad")])
    with pytest.raises(OutputValidationError):
        ValidateOutputStep().run(_ctx({"report": report}))


def test_validate_output_fails_closed_when_report_missing() -> None:
    with pytest.raises(OutputValidationError, match="no validation report"):
        ValidateOutputStep().run(_ctx({}))
