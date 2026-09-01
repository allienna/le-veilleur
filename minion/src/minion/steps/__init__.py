"""The ordered pipeline-step registry.

`STEPS` is the canonical all-stub sequence, kept as the orchestrator's default so the lifecycle
tests have a generic pipeline of the right shape. `build_pipeline` assembles the *real* one:
ingestion (`gmail` / `scrape` / `validate_input`), generation (`assemble` / `generate` /
`validate_output`), publishing (`imagen` / `github`), and per-source analysis (`fiches`), each
wired to its injected client. Either way the ordering is fixed by `STEP_ORDER`.
"""

from __future__ import annotations

from minion.config import STEP_ORDER
from minion.fiches.ports import FicheGenerateRunner
from minion.generate.ports import GenerateRunner
from minion.ingest.ports import GmailClient, ScraperClient
from minion.models import StepName
from minion.publish.ports import ContentRepository, ImageGenerator, PromptRewriter
from minion.steps.base import Step, StepContext, StepResult
from minion.steps.fiches import FichesStep
from minion.steps.generation import AssembleStep, GenerateStep, ValidateOutputStep
from minion.steps.ingestion import GmailStep, ScrapeStep, ValidateInputStep
from minion.steps.publish import GithubStep, ImagenStep
from minion.steps.stubs import build_stub_steps

STEPS: tuple[Step, ...] = build_stub_steps()

__all__ = ["STEPS", "Step", "StepContext", "StepResult", "build_pipeline"]


def build_pipeline(
    gmail_client: GmailClient,
    scraper_client: ScraperClient,
    generate_runner: GenerateRunner,
    image_generator: ImageGenerator,
    prompt_rewriter: PromptRewriter,
    content_repo: ContentRepository,
    fiche_runner: FicheGenerateRunner,
) -> tuple[Step, ...]:
    """The production pipeline — every step real."""
    real: dict[StepName, Step] = {
        StepName.gmail: GmailStep(client=gmail_client),
        StepName.scrape: ScrapeStep(client=scraper_client),
        StepName.validate_input: ValidateInputStep(),
        StepName.assemble: AssembleStep(),
        StepName.generate: GenerateStep(runner=generate_runner),
        StepName.validate_output: ValidateOutputStep(),
        StepName.imagen: ImagenStep(
            image_generator=image_generator, prompt_rewriter=prompt_rewriter
        ),
        StepName.github: GithubStep(content_repo=content_repo),
        StepName.fiches: FichesStep(runner=fiche_runner, content_repo=content_repo),
    }
    return tuple(real[name] for name in STEP_ORDER)
