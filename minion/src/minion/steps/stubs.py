"""Stub implementations of the pipeline steps.

Each stub logs and returns a canned, right-shaped payload — no external calls. They exist so
the orchestrator lifecycle can be tested against a generic pipeline of the right shape,
independently of any real adapter.
"""

from __future__ import annotations

from dataclasses import dataclass

from minion.config import STEP_ORDER
from minion.models import StepName
from minion.steps.base import StepContext, StepResult

# Canned, right-shaped output per step.
_CANNED_PAYLOADS: dict[StepName, dict[str, object]] = {
    StepName.gmail: {"newsletters": []},
    StepName.scrape: {"articles": []},
    StepName.validate_input: {"valid": True, "sources": 0},
    StepName.assemble: {"context": ""},
    StepName.generate: {"article": None, "linkedin": "", "imagePrompt": ""},
    StepName.validate_output: {"valid": True},
    StepName.imagen: {"imageBytes": None},
    StepName.github: {"commit": None},
    StepName.fiches: {"fiched": 0},
}


@dataclass
class StubStep:
    """A no-op step that logs and returns its canned payload."""

    name: StepName
    payload: dict[str, object]

    def run(self, ctx: StepContext) -> StepResult:
        ctx.log.info("step executing (stub)")
        return StepResult(payload=dict(self.payload))


def build_stub_steps() -> tuple[StubStep, ...]:
    """One stub per canonical step, in execution order (driven by STEP_ORDER)."""
    return tuple(StubStep(name=name, payload=dict(_CANNED_PAYLOADS[name])) for name in STEP_ORDER)
