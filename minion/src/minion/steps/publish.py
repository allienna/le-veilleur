"""Real publishing steps: `imagen` (step 7) and `github` (step 8).

Data bag contract:
- `imagen` -> reads `article`; writes `image` (ImageArtifact) + `article` with `frontmatter.image`
- `github` -> reads `article` + `image`; commits the image, the article markdown and the LinkedIn
              post; writes `commits` + `commit_sha`

There is no separate persistence step: the commit *is* the publication, and git is the recovery
mechanism. A run whose commit hard-fails is replayed by date — the Gmail window is a pure
function of the date, so a replay is deterministic.

The Imagen fallback is the sole producer of `success_with_warnings` on the article path: on a
rejection the step rewrites the prompt once, then gives up on the image and lets the article ship
without one (the site falls back to its own placeholder SVG). Never a hard fail — a missing hero
image must not cost the day's article.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from minion import config
from minion.generate.models import GeneratedArticle
from minion.models import StepName
from minion.publish.models import CommitResult, ImageArtifact
from minion.publish.ports import (
    ContentRepoError,
    ContentRepository,
    ImageGenerator,
    ImagenBlockedError,
    PromptRewriter,
)
from minion.publish.serialize import render_post
from minion.steps.base import StepContext, StepResult


def _require_article(ctx: StepContext) -> GeneratedArticle:
    article = ctx.data.get("article")
    if not isinstance(article, GeneratedArticle):
        raise RuntimeError("publish step missing a GeneratedArticle in the data bag")
    return article


@dataclass
class ImagenStep:
    """Step 7: generate the hero image, with a rewrite-then-give-up fallback."""

    image_generator: ImageGenerator
    prompt_rewriter: PromptRewriter
    name: StepName = StepName.imagen

    def _generate_with_fallback(self, ctx: StepContext, base_prompt: str) -> bytes:
        """Return the PNG bytes, or empty bytes when Imagen cannot be satisfied.

        Tries the base prompt, then up to `IMAGEN_RETRIES` softened rewrites.
        """
        prompt = base_prompt
        try:
            return self.image_generator.generate(prompt)
        except ImagenBlockedError as exc:
            reason = str(exc)
            ctx.log.warning("imagen rejected prompt", extra={"reason": reason})
        for attempt in range(config.IMAGEN_RETRIES):
            try:
                prompt = self.prompt_rewriter.soften(prompt, reason)
                image = self.image_generator.generate(prompt)
                ctx.log.info("imagen succeeded after rewrite", extra={"attempt": attempt + 1})
                return image
            except ImagenBlockedError as exc:
                reason = str(exc)
                ctx.log.warning("imagen rejected rewrite", extra={"attempt": attempt + 1})
            except Exception:
                # The rewrite itself failed (no OAuth token, `claude` missing, subprocess error).
                # It is best-effort — give up on the image, never hard-fail.
                ctx.log.warning("prompt rewrite failed; shipping without a hero image")
                break
        ctx.log.warning("imagen unavailable", extra={"reason": reason})
        return b""

    def run(self, ctx: StepContext) -> StepResult:
        article = _require_article(ctx)
        base_prompt = f"{article.image_prompt}\n\n{config.IMAGEN_BRAND_TEMPLATE}"
        png = self._generate_with_fallback(ctx, base_prompt)

        filename = f"{ctx.date}.png"
        artifact = ImageArtifact(filename=filename, png=png)
        # Back-fill the hero filename only when there is an image to point at; an empty value
        # makes `render_post` omit the key entirely.
        updated = article.model_copy(
            update={
                "frontmatter": article.frontmatter.model_copy(
                    update={"image": filename if png else ""}
                )
            }
        )
        ctx.log.info("hero image step done", extra={"available": bool(png)})
        return StepResult(
            payload={"image": artifact, "article": updated},
            warning=None if png else config.IMAGEN_FALLBACK_WARNING,
        )


@dataclass
class GithubStep:
    """Step 8: commit the image, the article markdown and the LinkedIn post."""

    content_repo: ContentRepository
    sleep: Callable[[float], None] = time.sleep
    name: StepName = StepName.github

    def _commit_with_retry(self, path: str, content: bytes, message: str) -> str:
        """Commit one file with exponential-backoff retry; raise after exhausting."""
        for attempt in range(config.GITHUB_RETRIES + 1):
            try:
                return self.content_repo.put_file(path, content, message)
            except ContentRepoError:
                if attempt >= config.GITHUB_RETRIES:
                    raise
                self.sleep(config.GITHUB_BACKOFF_BASE.total_seconds() * (2**attempt))
        raise AssertionError("unreachable")  # pragma: no cover

    def run(self, ctx: StepContext) -> StepResult:
        article = _require_article(ctx)
        image = ctx.data.get("image")
        if not isinstance(image, ImageArtifact):
            raise RuntimeError("github step missing an ImageArtifact in the data bag")

        message = f"feat: add {ctx.date} article"
        commits: list[CommitResult] = []

        # Commit the image BEFORE the markdown: an image-only commit is harmless, whereas a post
        # referencing a missing hero image is visibly broken.
        if image.available:
            image_path = config.POST_IMAGE_PATH_TEMPLATE.format(date=ctx.date)
            commits.append(
                CommitResult(
                    path=image_path, sha=self._commit_with_retry(image_path, image.png, message)
                )
            )

        md_path = config.POST_MD_PATH_TEMPLATE.format(date=ctx.date)
        md_sha = self._commit_with_retry(md_path, render_post(article).encode("utf-8"), message)
        commits.append(CommitResult(path=md_path, sha=md_sha))

        # The LinkedIn post is the day's actual deliverable. Committed last and outside site/:
        # a failure here must not leave the article unpublished, but losing it silently would
        # defeat the point of the run, so it is not swallowed either.
        linkedin_path = config.LINKEDIN_PATH_TEMPLATE.format(date=ctx.date)
        # The post text alone, no heading: the whole file is meant to be selected and pasted
        # into LinkedIn, and the filename already carries the date.
        linkedin_body = f"{article.linkedin.strip()}\n"
        commits.append(
            CommitResult(
                path=linkedin_path,
                sha=self._commit_with_retry(linkedin_path, linkedin_body.encode("utf-8"), message),
            )
        )

        ctx.log.info("article committed", extra={"paths": [c.path for c in commits]})
        return StepResult(payload={"commits": commits, "commit_sha": md_sha})
