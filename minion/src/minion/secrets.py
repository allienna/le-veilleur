# pyright: basic
# ^ google-cloud-secret-manager ships incomplete type stubs (see pyproject reportMissingTypeStubs);
# this SDK-boundary helper is dropped to basic checking.
"""Secret Manager helper — the accessor for the four runtime secrets.

Locally, a plain environment variable of the same (upper-snake) name is used instead, so the
pipeline runs on a laptop with no GCP credentials.

`ANTHROPIC_API_KEY` must not be in the environment: importing this module refuses if it is set,
which blocks accidental activation of the API-key path. The agentic steps authenticate with
`CLAUDE_CODE_OAUTH_TOKEN` only. See infra/RUNBOOK.md §3c for the deliberate break-glass.
"""

from __future__ import annotations

import os

from google.api_core.exceptions import NotFound
from google.cloud import secretmanager

PROJECT_ID = "veilleur-app"


class MissingSecretError(LookupError):
    """Raised by `require()` when a Secret Manager secret has no accessible version."""


def _assert_anthropic_api_key_absent() -> None:
    if os.environ.get("ANTHROPIC_API_KEY") is not None:
        msg = (
            "ANTHROPIC_API_KEY is set in env. The API-key path is disabled by default — "
            "unset it before running the Minion, or activate it explicitly as the documented "
            "break-glass (infra/RUNBOOK.md §3c)."
        )
        raise RuntimeError(msg)


_assert_anthropic_api_key_absent()


_CLIENT: secretmanager.SecretManagerServiceClient | None = None


def _client() -> secretmanager.SecretManagerServiceClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = secretmanager.SecretManagerServiceClient()
    return _CLIENT


def env_var_for(name: str) -> str:
    """The environment-variable name that overrides secret `name` (`github-pat` -> `GITHUB_PAT`)."""
    return name.replace("-", "_").upper()


def get(name: str) -> str:
    """Return secret `name`, from the environment if set, otherwise from Secret Manager.

    The environment override is what lets the whole pipeline run on a laptop with no GCP
    credentials at all — the reason image generation goes through a Gemini API key rather than
    Vertex IAM. In Cloud Run nothing sets these, so the Secret Manager path is taken.

    Raises `google.api_core.exceptions.NotFound` if the secret or its versions don't exist.
    Use `require()` if you want absence signalled as a domain-level `MissingSecretError`.
    """
    override = os.environ.get(env_var_for(name))
    if override:
        return override
    secret_path = f"projects/{PROJECT_ID}/secrets/{name}/versions/latest"
    response = _client().access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("utf-8")


def require(name: str) -> str:
    """Return `get(name)`, but translate absence into a domain-level `MissingSecretError`."""
    try:
        return get(name)
    except NotFound as exc:
        msg = f"Secret {name!r} has no accessible version in project {PROJECT_ID!r}"
        raise MissingSecretError(msg) from exc
