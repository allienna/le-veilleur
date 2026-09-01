"""The run state machine.

`run_pipeline` mints a per-attempt ULID, takes the global lock (aborting if another run holds
it), records the run as `running`, drives the steps recording each one, finalizes the run, and
releases the lock — on success or failure.

Invariants enforced here:
- Idempotent replay: `start_run` overwrites the record for `date` and clears its previous
  steps, so a re-run for the same date leaves no duplicates or orphans.
- Concurrency guard: a second invocation while a run is live aborts `already_running` and
  executes no steps — and, crucially, does NOT touch the record for `date` (it belongs to the
  live run).
- Observable steps: every step is recorded `running` → terminal with timestamps; a raising step
  is recorded `failure` and halts the remaining steps.
"""

from __future__ import annotations

from typing import cast

from minion.clock import Clock, new_run_id
from minion.logging import bind
from minion.models import ALREADY_RUNNING, Lock, Run, RunStatus, RunStep
from minion.steps import STEPS, Step, StepContext
from minion.store.ports import LockStore, RunStore


def run_pipeline(
    date: str,
    *,
    run_store: RunStore,
    lock_store: LockStore,
    clock: Clock,
    steps: tuple[Step, ...] = STEPS,
) -> Run:
    """Execute the pipeline for `date`. Returns the final (assembled) run, or an in-memory
    aborted run if the concurrency guard tripped."""
    run_id = new_run_id()
    log = bind(run_id)
    started_at = clock.now()

    lock = Lock(run_id=run_id, date=date, started_at=started_at)
    if not lock_store.acquire(lock):
        log.warning("run aborted: already_running")
        # Do not record — the run for `date` belongs to the live run that holds the lock.
        return Run(
            run_id=run_id,
            date=date,
            status=RunStatus.aborted,
            started_at=started_at,
            ended_at=clock.now(),
            error=ALREADY_RUNNING,
            steps=[],
        )

    try:
        run_store.start_run(
            Run(run_id=run_id, date=date, status=RunStatus.running, started_at=started_at, steps=[])
        )
        log.info("run started")

        data: dict[str, object] = {}
        status = RunStatus.success
        run_error: str | None = None
        warning_reason: str | None = None  # first run-level warning, latched

        for step in steps:
            step_log = bind(run_id, step=step.name.value)
            step_started = clock.now()
            run_store.upsert_step(
                date, RunStep(name=step.name, status=RunStatus.running, started_at=step_started)
            )
            try:
                result = step.run(StepContext(run_id, date, clock, step_log, data))
            except Exception as exc:
                run_store.upsert_step(
                    date,
                    RunStep(
                        name=step.name,
                        status=RunStatus.failure,
                        started_at=step_started,
                        ended_at=clock.now(),
                        error=str(exc),
                    ),
                )
                step_log.exception("step failed")  # emit the traceback for Cloud Logging
                status = RunStatus.failure
                run_error = f"{step.name.value}: {exc}"
                break

            data.update(result.payload)
            run_store.upsert_step(
                date,
                RunStep(
                    name=step.name,
                    status=RunStatus.success,
                    started_at=step_started,
                    ended_at=clock.now(),
                ),
            )

            if result.warning is not None and warning_reason is None:
                # Latch the first warning: the step succeeded and the pipeline continues, but the
                # final run status downgrades to success_with_warnings unless a later
                # failure/terminal status overrides it. Per-step record stays success.
                warning_reason = result.warning
                step_log.warning("run warning latched", extra={"warning": warning_reason})

            if result.terminal_status is not None:
                # Graceful early-exit: the step succeeded but ends the run with a
                # non-failure terminal status (e.g. skipped/no_sources). Halt remaining steps.
                status = result.terminal_status
                run_error = result.reason
                step_log.info(
                    "run terminated early",
                    extra={"status": status.value, "reason": result.reason},
                )
                break

        if status is RunStatus.success and warning_reason is not None:
            # Downgrade only a clean success (a failure/terminal status takes precedence).
            status = RunStatus.success_with_warnings
            run_error = warning_reason
        # LLM cost/tokens surfaced by the generate step; absent (None) when the run never reached
        # `generate` — e.g. skipped/no_sources or an early-step failure.
        cost_usd = cast("float | None", data.get("cost_usd"))
        tokens = cast("int | None", data.get("tokens"))
        run_store.finalize_run(date, status, clock.now(), run_error, cost_usd, tokens)
        log.info("run finished", extra={"status": status.value})

        final = run_store.get_run(date)
        assert final is not None
        return final
    finally:
        lock_store.release(run_id)
