"""Generation subpackage: the agentic `/generate` step and its supporting pieces.

Mirrors `ingest/` — `ports.py` declares the `GenerateRunner` Protocol the step depends on,
`runner.py` is the production `claude -p "/generate"` subprocess client, `fakes.py` a hermetic
test double, `models.py` the Minion-internal artefact models, `assemble.py` the deterministic
context-assembly helper, and `validate.py` the pure structural + copyright validators. The
artefact stays Minion-internal, in the data bag.
"""

from __future__ import annotations
