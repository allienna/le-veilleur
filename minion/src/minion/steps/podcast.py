"""Real step: `podcast` (step 10, final).

Data bag contract:
- reads `sources` (a `SourceSet`, written by `scrape`/`validate_input`)
- writes `podcast` (a `PodcastArtifact`) only when an episode was actually produced and committed

Never raises: disabled via `PODCAST_ENABLED`, no OK sources, a NotebookLM failure/timeout, a GCS
upload failure, or an exhausted commit retry are all soft failures — the step returns a
`warning` and the run still finishes as `success_with_warnings`, exactly like `imagen`'s
give-up path and `fiches`' partial-failure path (`steps/publish.py`, `steps/fiches.py`). Placed
last in `STEP_ORDER` so it can never block the article, image, or fiches from shipping.
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable
from dataclasses import dataclass

from minion import config
from minion.ingest.models import SourceSet
from minion.models import StepName
from minion.podcast.models import PodcastArtifact
from minion.podcast.ports import (
    AudioStorage,
    AudioUploadError,
    NotebookLMClient,
    PodcastGenerationError,
)
from minion.publish.ports import ContentRepoError, ContentRepository
from minion.publish.serialize import render_podcast_episode
from minion.steps.base import StepContext, StepResult


def _podcast_enabled() -> bool:
    return os.environ.get(config.PODCAST_ENABLED_ENV_VAR, "true").lower() in ("1", "true", "yes")


@dataclass
class PodcastStep:
    """Step 10: generate the day's audio overview via NotebookLM Enterprise and publish it."""

    notebooklm: NotebookLMClient
    audio_storage: AudioStorage
    content_repo: ContentRepository
    sleep: Callable[[float], None] = time.sleep
    name: StepName = StepName.podcast

    def _commit_with_retry(self, files: list[tuple[str, bytes]], message: str) -> str:
        """Same bounded exponential-backoff retry as `GithubStep` — raises `ContentRepoError`
        after exhausting, which the caller treats as a soft failure, not a hard one."""
        for attempt in range(config.GITHUB_RETRIES + 1):
            try:
                return self.content_repo.put_files(files, message)
            except ContentRepoError:
                if attempt >= config.GITHUB_RETRIES:
                    raise
                self.sleep(config.GITHUB_BACKOFF_BASE.total_seconds() * (2**attempt))
        raise AssertionError("unreachable")  # pragma: no cover

    def run(self, ctx: StepContext) -> StepResult:
        if not _podcast_enabled():
            ctx.log.info("podcast disabled via env var")
            return StepResult()

        sources = ctx.data.get("sources")
        if not isinstance(sources, SourceSet):
            raise RuntimeError("podcast step missing a SourceSet in the data bag")
        ok_sources = sources.ok_sources
        if not ok_sources:
            ctx.log.info("no OK sources; skipping podcast episode")
            return StepResult()

        source_pairs = [(s.url, s.title or s.url) for s in ok_sources]

        try:
            result = self.notebooklm.generate_episode(
                date=ctx.date, sources=source_pairs, language_code=config.PODCAST_LANGUAGE_CODE
            )
        except PodcastGenerationError as exc:
            ctx.log.warning("notebooklm generation failed", extra={"error": str(exc)[:300]})
            return StepResult(warning=config.PODCAST_UNAVAILABLE_WARNING)

        object_name = config.PODCAST_AUDIO_OBJECT_TEMPLATE.format(date=ctx.date)
        try:
            audio_url = self.audio_storage.upload(
                object_name, result.audio_bytes, result.content_type
            )
        except AudioUploadError as exc:
            ctx.log.warning("audio upload failed", extra={"error": str(exc)[:300]})
            return StepResult(warning=config.PODCAST_UNAVAILABLE_WARNING)

        episode = PodcastArtifact(
            date=ctx.date,
            title=f"Le Veilleur — {ctx.date}",
            audio_url=audio_url,
            duration_seconds=result.duration_seconds,
            notebook_id=result.notebook_id,
        )

        try:
            self._commit_with_retry(
                [
                    (
                        config.PODCAST_MD_PATH_TEMPLATE.format(date=ctx.date),
                        render_podcast_episode(episode).encode("utf-8"),
                    )
                ],
                f"feat: add {ctx.date} podcast episode",
            )
        except ContentRepoError as exc:
            ctx.log.warning("podcast episode commit failed", extra={"error": str(exc)[:300]})
            return StepResult(warning=config.PODCAST_UNAVAILABLE_WARNING)

        # Best-effort hygiene, never allowed to affect today's outcome — the Protocol promises
        # this never raises, but the step guards anyway rather than trusting every adapter to.
        try:
            purged = self.notebooklm.purge_notebooks_older_than(config.PODCAST_NOTEBOOK_PURGE_DAYS)
            ctx.log.info("podcast notebooks purged", extra={"count": purged})
        except Exception:
            ctx.log.warning("podcast notebook purge failed")

        ctx.log.info("podcast episode published", extra={"audio_url": audio_url})
        return StepResult(payload={"podcast": episode})
