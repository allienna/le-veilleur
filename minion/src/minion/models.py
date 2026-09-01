"""Pydantic boundary models for the orchestrator.

Holds the run-state contract (`Run`, `RunStep`, `RunStatus`, `StepName`) plus the
Minion-internal concurrency `Lock`. These types were generated from JSON Schema in the
veilleur-app PoC, where they had to be shared with a TypeScript PWA; that PWA is gone, so
the codegen (and its pnpm workspace) is gone with it and the models live here directly.

Identity note: the run is keyed by `date` — the idempotency key. `run_id` is a per-attempt
ULID carried as a field, so replaying a date reuses the key but mints a fresh `run_id`.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "ALREADY_RUNNING",
    "Lock",
    "Run",
    "RunStatus",
    "RunStep",
    "StepName",
]

# Run-level abort reason written to `Run.error` when the concurrency guard trips.
ALREADY_RUNNING = "already_running"

_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"


class RunStatus(Enum):
    success = "success"
    success_with_warnings = "success_with_warnings"
    failure = "failure"
    skipped = "skipped"
    aborted = "aborted"
    running = "running"


class StepName(Enum):
    """The pipeline steps, in execution order — `config.STEP_ORDER` is `tuple(StepName)`."""

    gmail = "gmail"
    scrape = "scrape"
    validate_input = "validate_input"
    assemble = "assemble"
    generate = "generate"
    validate_output = "validate_output"
    imagen = "imagen"
    github = "github"
    fiches = "fiches"


class RunStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: StepName
    status: RunStatus
    started_at: datetime | None = None
    ended_at: datetime | None = None
    error: str | None = Field(default=None, description="Error message if the step failed.")


class Run(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(description="ULID for this run attempt; disambiguates attempts in logs.")
    date: str = Field(description="Run date YYYY-MM-DD (Europe/Paris).", pattern=_DATE_PATTERN)
    status: RunStatus
    started_at: datetime | None = None
    ended_at: datetime | None = None
    error: str | None = Field(
        default=None, description='Run-level failure or abort reason (e.g. "already_running").'
    )
    cost_usd: float | None = Field(
        default=None,
        description="Total LLM cost in USD, from the `claude` CLI's `total_cost_usd`. None when "
        "the run never reached `generate`.",
    )
    tokens: int | None = Field(
        default=None, description="Total LLM tokens consumed by `generate`. None when none ran."
    )
    steps: list[RunStep] = Field(description="Ordered per-step records.")


class Lock(BaseModel):
    """The single global concurrency lock.

    A lock is *stale* (and reclaimable) when `started_at` is older than `RUN_TIMEOUT` — the
    holding run exceeded the wall-clock cap and is presumed dead.
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str
    date: str
    started_at: datetime
