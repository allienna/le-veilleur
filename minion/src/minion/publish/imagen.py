# pyright: basic
# ^ wraps the google-genai SDK (incomplete stubs) and the `claude` subprocess boundary; like
#   generate/runner.py it is dropped to basic checking. Behaviour is covered by the in-memory
#   fakes + the gated integration test (no Imagen/Claude in CI).
"""Production publishing adapters: Imagen image generation + Claude prompt rewrite.

`GeminiImageGenerator` asks Imagen for one 16:9 image and returns its PNG bytes, raising
`ImagenBlockedError` when nothing usable comes back (moderation / empty / quota). It talks to
the Gemini API with an API key rather than to Vertex AI with GCP IAM, so the same code path
runs in Cloud Run and on a laptop with no GCP credentials. Imagen already returns PNG, so
there is no re-encoding step and no image library in the dependency set.

The rewrite-then-omit-image fallback lives in the `imagen` step, not here.

`ClaudePromptRewriter` softens a rejected prompt via a one-shot `claude -p` call under the same
OAuth-only env as `/generate` (`CLAUDE_CODE_OAUTH_TOKEN` injected, `ANTHROPIC_API_KEY` stripped).
"""

from __future__ import annotations

import os
import subprocess

from google import genai
from google.genai.types import GenerateImagesConfig

from minion import config, secrets
from minion.publish.ports import ImagenBlockedError

_REWRITE_INSTRUCTION = (
    "You are refining an image-generation prompt that a safety filter rejected. Rewrite it to be "
    "softer, gentler, and unambiguously safe-for-work while keeping the same subject and the "
    "Le Veilleur owl mascot. Reply with ONLY the rewritten prompt, no preamble.\n\n"
    "Rejection reason: {reason}\nOriginal prompt: {prompt}"
)


class GeminiImageGenerator:
    """`ImageGenerator` over the Gemini API's Imagen model (API key, no GCP IAM)."""

    def __init__(self) -> None:
        self._client: genai.Client | None = None

    def _get_client(self) -> genai.Client:
        if self._client is None:  # lazy — constructing the client needs the API key
            self._client = genai.Client(api_key=secrets.require(config.GEMINI_API_KEY_SECRET))
        return self._client

    def generate(self, prompt: str) -> bytes:
        try:
            response = self._get_client().models.generate_images(
                model=config.IMAGEN_MODEL,
                prompt=prompt,
                config=GenerateImagesConfig(
                    aspect_ratio=config.IMAGEN_ASPECT_RATIO, number_of_images=1
                ),
            )
            images = response.generated_images
            if images:
                image_obj = images[0].image
                if image_obj is not None and image_obj.image_bytes:
                    return image_obj.image_bytes
        except Exception as exc:
            # Auth / quota / 5xx / network — surface as ImagenBlockedError so the step follows the
            # rewrite/omit fallback rather than hard-failing the run.
            raise ImagenBlockedError(f"Imagen generation failed: {exc}") from exc
        raise ImagenBlockedError("Imagen returned no usable image (safety filter, empty, or quota)")


def _build_env() -> dict[str, str]:
    """Inherit env minus `ANTHROPIC_API_KEY`, then inject `CLAUDE_CODE_OAUTH_TOKEN`."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CODE_OAUTH_TOKEN"] = secrets.require(config.ANTHROPIC_OAUTH_TOKEN_SECRET)
    return env


class ClaudePromptRewriter:
    """`PromptRewriter` over a one-shot `claude -p` subprocess (OAuth-only env)."""

    def soften(self, prompt: str, reason: str) -> str:
        instruction = _REWRITE_INSTRUCTION.format(reason=reason, prompt=prompt)
        result = subprocess.run(
            ["claude", "-p", instruction, "--permission-mode", "bypassPermissions"],
            capture_output=True,
            text=True,
            timeout=config.CLAUDE_TIMEOUT.total_seconds(),
            env=_build_env(),
            check=False,
        )
        rewritten = result.stdout.strip()
        # A failed rewrite is non-fatal: fall back to the original prompt so the step can still
        # retry Imagen once before giving up on the image.
        return rewritten or prompt
