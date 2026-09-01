"""Fiche-generation port — mirrors `minion.generate.ports`, but for a single-source call.

The article is generated through the `/generate` slash command vendored at
`.claude/commands/generate.md`. There is no equivalent per-source command, so
`FicheGenerateRunner` invokes `claude` with an inline literal prompt instead: the fiches feature
owns its own prompt text, in `runner.py`.
"""

from __future__ import annotations

from typing import Protocol

from minion.fiches.models import FicheInvocation
from minion.generate.models import ContextSource


class FicheGenerateTransportError(RuntimeError):
    """A failure invoking the per-source fiche call — binary missing, timeout, non-zero exit.

    Distinct from a validation failure: a transport error on one source is caught by the
    `fiches` step and that source's fiche is skipped (never a run failure — plan AD, "fiches are
    non-blocking")."""


class FicheGenerateRunner(Protocol):
    """Runs one per-source fiche invocation and returns its artefact text plus usage telemetry."""

    def invoke(self, source: ContextSource) -> FicheInvocation:
        """Invoke the fiche prompt for `source`, returning the artefact text and (when reported)
        the call's USD cost + token count. Raises `FicheGenerateTransportError` on a transport
        failure; the caller parses + validates the returned text."""
        ...
