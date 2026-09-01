"""In-memory implementations of the store ports.

These are the *only* implementations: the pipeline is a one-shot job, so run state lives for
the length of the process and its durable trace is Cloud Logging. The lock keeps its
compare-and-set-with-stale-reclaim semantics because the orchestrator contract depends on it.
"""

from __future__ import annotations

from datetime import datetime

from minion.clock import Clock
from minion.config import RUN_TIMEOUT, STEP_ORDER
from minion.models import Lock, Run, RunStatus, RunStep, StepName


class InMemoryRunStore:
    """Run store backed by dicts. `start_run` overwrites and clears previous steps."""

    def __init__(self) -> None:
        self._runs: dict[str, dict[str, object]] = {}
        self._steps: dict[str, dict[StepName, RunStep]] = {}

    def start_run(self, run: Run) -> None:
        self._runs[run.date] = {
            "run_id": run.run_id,
            "status": run.status,
            "started_at": run.started_at,
            "ended_at": run.ended_at,
            "error": run.error,
        }
        self._steps[run.date] = {}  # clear prior children (idempotent replay)

    def upsert_step(self, date: str, step: RunStep) -> None:
        self._steps.setdefault(date, {})[step.name] = step

    def finalize_run(
        self,
        date: str,
        status: RunStatus,
        ended_at: datetime,
        error: str | None,
        cost_usd: float | None = None,
        tokens: int | None = None,
    ) -> None:
        doc = self._runs[date]
        doc["status"] = status
        doc["ended_at"] = ended_at
        doc["error"] = error
        doc["cost_usd"] = cost_usd
        doc["tokens"] = tokens

    def get_run(self, date: str) -> Run | None:
        doc = self._runs.get(date)
        if doc is None:
            return None
        children = self._steps.get(date, {})
        steps = [children[name] for name in STEP_ORDER if name in children]
        return Run(
            run_id=str(doc["run_id"]),
            date=date,
            status=doc["status"],  # type: ignore[arg-type]
            started_at=doc["started_at"],  # type: ignore[arg-type]
            ended_at=doc["ended_at"],  # type: ignore[arg-type]
            error=doc["error"],  # type: ignore[arg-type]
            cost_usd=doc.get("cost_usd"),  # type: ignore[arg-type]
            tokens=doc.get("tokens"),  # type: ignore[arg-type]
            steps=steps,
        )


class InMemoryLockStore:
    """Global single-flight lock with stale reclaim, evaluated against an injected clock."""

    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._lock: Lock | None = None

    def acquire(self, lock: Lock) -> bool:
        held = self._lock
        if held is not None and not self._is_stale(held):
            return False
        self._lock = lock  # fresh acquire or reclaim of a stale lock
        return True

    def release(self, run_id: str) -> None:
        if self._lock is not None and self._lock.run_id == run_id:
            self._lock = None

    def _is_stale(self, held: Lock) -> bool:
        return held.started_at < self._clock.now() - RUN_TIMEOUT
