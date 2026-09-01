"""Run-state ports.

Two stores, both in-process only: the run record that the orchestrator assembles and reads
back after finalize, and the single-flight lock. Published artefacts are not stored here —
they are committed to the repo, and git is the record.

`get_run` returns the *assembled* view: the run-level fields plus its ordered step records.
Replaying a date overwrites the same run and clears its previous steps.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from minion.models import Lock, Run, RunStatus, RunStep


class RunStore(Protocol):
    """Reads and writes run documents and their per-step children."""

    def start_run(self, run: Run) -> None:
        """Overwrite the record for `run.date` with the initial running state and clear any
        previous step records (idempotent replay)."""
        ...

    def upsert_step(self, date: str, step: RunStep) -> None:
        """Write/overwrite the record for `step.name` on `date`."""
        ...

    def finalize_run(
        self,
        date: str,
        status: RunStatus,
        ended_at: datetime,
        error: str | None,
        cost_usd: float | None = None,
        tokens: int | None = None,
    ) -> None:
        """Set the terminal `status`, `ended_at`, run-level `error`, and the LLM `cost_usd`/`tokens`
        for `date`. Cost/tokens are None when the run never reached `generate`."""
        ...

    def get_run(self, date: str) -> Run | None:
        """Assemble the full `Run` (run-level fields + ordered step children), or None."""
        ...


class LockStore(Protocol):
    """The global single-flight concurrency guard."""

    def acquire(self, lock: Lock) -> bool:
        """Atomically take the lock. Returns True if acquired — either no lock was held, or
        the held lock was stale (its `started_at` older than `RUN_TIMEOUT`) and reclaimed.
        Returns False if a live lock is held by another run."""
        ...

    def release(self, run_id: str) -> None:
        """Release the lock iff it is currently held by `run_id` (no-op otherwise)."""
        ...
