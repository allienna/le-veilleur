"""Step contracts: the interface every pipeline step implements.

A `Step` is invoked with a `StepContext` (run identity, clock, a bound logger, and a shared
data bag carried across steps) and returns a `StepResult`. Raising from `run()` signals step
failure — the orchestrator records it and halts the run (AC-7). A step may instead return a
`StepResult` carrying a `terminal_status` to end the run *gracefully* (e.g. `skipped`) without
it being a failure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from minion.clock import Clock
from minion.logging import BoundLogger
from minion.models import RunStatus, StepName


def _empty_bag() -> dict[str, object]:
    return {}


@dataclass
class StepContext:
    """Everything a step needs to run, plus the data bag shared across steps."""

    run_id: str
    date: str
    clock: Clock
    log: BoundLogger
    data: dict[str, object] = field(default_factory=_empty_bag)


@dataclass
class StepResult:
    """A step's output, merged into the run's shared data bag by the orchestrator.

    `terminal_status` lets a step end the run gracefully: when set, the orchestrator
    finalizes the run with that status and `reason`, marks this step success, and halts the
    remaining steps — distinct from raising, which is a failure. `validate_input` uses
    `terminal_status=RunStatus.skipped, reason="no_sources"` for an empty mailbox (FR-4).

    `warning` lets a step finish normally (the pipeline continues) yet downgrade the *final*
    run status to `success_with_warnings`. The orchestrator latches the first warning reason; it
    never overrides a later `failure` or a graceful `terminal_status`. The `imagen` give-up
    fallback is one producer, a partly-failed `fiches` step the other. The per-step record stays
    `success` — the warning is run-level.
    """

    payload: dict[str, object] = field(default_factory=_empty_bag)
    terminal_status: RunStatus | None = None
    reason: str | None = None
    warning: str | None = None


class Step(Protocol):
    """A single ordered pipeline step."""

    name: StepName

    def run(self, ctx: StepContext) -> StepResult: ...
