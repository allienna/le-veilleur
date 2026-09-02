"""Gated integration test for the real `/generate` runner.

Marked `integration` so it is deselected by default (`addopts = -m 'not integration'`) — CI stays
hermetic. Run explicitly with `uv run pytest -m integration` on a host that has the `claude` CLI
and the OAuth token secret; the vendored `.claude/commands/generate.md` supplies the spec.
"""

from __future__ import annotations

import json
import shutil

import pytest

from minion import config
from minion.generate.models import AssembledContext, ContextSource, GeneratedArticle
from minion.generate.runner import ClaudeGenerateRunner
from minion.secrets import MissingSecretError, require


@pytest.mark.integration
def test_real_generate_emits_parseable_artefact() -> None:
    if shutil.which("claude") is None:
        pytest.skip("claude binary not on PATH")
    try:
        require(config.ANTHROPIC_OAUTH_TOKEN_SECRET)
    except MissingSecretError:
        pytest.skip("OAuth token secret not provisioned")

    context = AssembledContext(
        sources=[
            ContextSource(
                url="https://example.com/cloud-news",
                title="Cloud News",
                markdown="# Cloud News\n\nA short note about cloud-native scheduling changes.",
            )
        ]
    )
    invocation = ClaudeGenerateRunner().invoke(context, [])
    article = GeneratedArticle.model_validate(json.loads(invocation.text))
    assert article.theme
    assert article.body
