"""PodcastStep: happy path, disabled flag, no sources, and every best-effort failure mode."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest

from minion import config
from minion.clock import FrozenClock
from minion.config import PARIS_TZ
from minion.ingest.models import ScrapedSource, SourceOutcome, SourceSet
from minion.logging import bind
from minion.podcast.fakes import FakeAudioStorage, FakeAudioSynthesizer, FakeScriptWriter
from minion.podcast.models import PodcastArtifact
from minion.podcast.ports import (
    AudioOverviewResult,
    AudioSynthesisError,
    AudioUploadError,
    PodcastGenerationError,
    ScriptTurn,
)
from minion.publish.fakes import FakeContentRepository
from minion.steps.base import StepContext
from minion.steps.podcast import PodcastStep

T0 = datetime(2026, 6, 1, 6, 0, tzinfo=PARIS_TZ)
DATE = "2026-06-01"


def _sources(n: int = 2) -> SourceSet:
    return SourceSet(
        sources=[
            ScrapedSource(url=f"https://a.example/{i}", outcome=SourceOutcome.ok, title=f"T{i}")
            for i in range(n)
        ]
    )


def _ctx(**data: Any) -> StepContext:
    return StepContext(run_id="R", date=DATE, clock=FrozenClock(T0), log=bind("R"), data=data)


def _step(
    writer: FakeScriptWriter,
    synth: FakeAudioSynthesizer,
    storage: FakeAudioStorage,
    repo: FakeContentRepository,
) -> PodcastStep:
    return PodcastStep(
        script_writer=writer, audio_synthesizer=synth, audio_storage=storage, content_repo=repo
    )


def _turns() -> list[ScriptTurn]:
    return [ScriptTurn(speaker="A", text="Bonjour."), ScriptTurn(speaker="B", text="Salut.")]


def _result() -> AudioOverviewResult:
    return AudioOverviewResult(
        audio_bytes=b"MP3DATA", content_type="audio/mpeg", duration_seconds=1200
    )


def test_happy_path_publishes_episode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=[f"https://storage.googleapis.com/bucket/{DATE}.mp3"])
    repo = FakeContentRepository()
    result = _step(writer, synth, storage, repo).run(_ctx(sources=_sources()))

    episode = result.payload["podcast"]
    assert isinstance(episode, PodcastArtifact)
    assert episode.available is True
    assert episode.audio_url == f"https://storage.googleapis.com/bucket/{DATE}.mp3"
    assert episode.duration_seconds == 1200
    assert result.warning is None
    assert len(writer.calls) == 1
    sources, target_words = writer.calls[0]
    assert len(sources) == 2
    assert target_words == round(
        config.PODCAST_TARGET_DURATION.total_seconds() / 60 * config.PODCAST_WORDS_PER_MINUTE
    )
    assert len(synth.calls) == 1
    turns, language_code = synth.calls[0]
    assert turns == _turns()
    assert language_code == config.PODCAST_LANGUAGE_CODE
    assert len(storage.calls) == 1
    assert storage.calls[0][0] == f"{DATE}.mp3"
    assert len(repo.calls) == 1
    assert repo.calls[0].path_content().keys() == {f"site/src/content/podcasts/{DATE}.md"}


def test_disabled_via_env_var_skips_entirely(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(config.PODCAST_ENABLED_ENV_VAR, "false")
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=["https://x"])
    repo = FakeContentRepository()
    result = _step(writer, synth, storage, repo).run(_ctx(sources=_sources()))

    assert result.payload == {}
    assert result.warning is None
    assert writer.calls == []
    assert synth.calls == []
    assert storage.calls == []
    assert repo.calls == []


def test_no_ok_sources_skips_cleanly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    failed_source = ScrapedSource(url="https://a.example/0", outcome=SourceOutcome.failed)
    empty = SourceSet(sources=[failed_source])
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=["https://x"])
    repo = FakeContentRepository()
    result = _step(writer, synth, storage, repo).run(_ctx(sources=empty))

    assert result.payload == {}
    assert result.warning is None
    assert writer.calls == []


def test_script_generation_failure_warns_without_synthesis(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[PodcastGenerationError("boom")])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=["https://x"])
    repo = FakeContentRepository()
    result = _step(writer, synth, storage, repo).run(_ctx(sources=_sources()))

    assert result.payload == {}
    assert result.warning == config.PODCAST_UNAVAILABLE_WARNING
    assert synth.calls == []
    assert repo.calls == []


def test_audio_synthesis_failure_warns_without_upload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[AudioSynthesisError("boom")])
    storage = FakeAudioStorage(outcomes=["https://x"])
    repo = FakeContentRepository()
    result = _step(writer, synth, storage, repo).run(_ctx(sources=_sources()))

    assert result.payload == {}
    assert result.warning == config.PODCAST_UNAVAILABLE_WARNING
    assert storage.calls == []
    assert repo.calls == []


def test_audio_upload_failure_warns_without_commit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=[AudioUploadError("boom")])
    repo = FakeContentRepository()
    result = _step(writer, synth, storage, repo).run(_ctx(sources=_sources()))

    assert result.payload == {}
    assert result.warning == config.PODCAST_UNAVAILABLE_WARNING
    assert repo.calls == []


def test_commit_exhausts_retries_warns(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=["https://x"])
    repo = FakeContentRepository(fail_times=config.GITHUB_RETRIES + 1)
    step = PodcastStep(
        script_writer=writer,
        audio_synthesizer=synth,
        audio_storage=storage,
        content_repo=repo,
        sleep=lambda _: None,
    )
    result = step.run(_ctx(sources=_sources()))

    assert result.payload == {}
    assert result.warning == config.PODCAST_UNAVAILABLE_WARNING


def test_commit_uses_a_feat_commit_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=[f"https://storage.googleapis.com/bucket/{DATE}.mp3"])
    repo = FakeContentRepository()
    _step(writer, synth, storage, repo).run(_ctx(sources=_sources()))

    assert repo.calls[0].message == f"feat: add {DATE} podcast episode"


def test_missing_source_set_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.PODCAST_ENABLED_ENV_VAR, raising=False)
    writer = FakeScriptWriter(outcomes=[_turns()])
    synth = FakeAudioSynthesizer(outcomes=[_result()])
    storage = FakeAudioStorage(outcomes=["https://x"])
    repo = FakeContentRepository()
    with pytest.raises(RuntimeError, match="missing a SourceSet"):
        _step(writer, synth, storage, repo).run(_ctx())
