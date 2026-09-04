"""Post-run notification: one email per run, sent from `cli.py` after `run_pipeline` returns.

Mirrors `ingest/` and `publish/`: `ports.py` declares the `Notifier` Protocol the CLI depends on,
`gmail.py` is the production adapter, `fakes.py` holds the hermetic test double, and
`message.py` is the pure function that turns a finished `Run` (plus its data bag) into an email.

Deliberately not a pipeline step: `STEP_ORDER` halts on the first failure or terminal status,
which is exactly the outcome this must still report on.
"""

from __future__ import annotations
