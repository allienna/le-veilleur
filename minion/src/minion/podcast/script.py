# pyright: basic
# ^ subprocess boundary to the external `claude` CLI, like generate/runner.py; dropped to basic
# checking. Behaviour is covered by FakeScriptWriter + the gated integration test.
"""Production `ScriptWriter` over a one-shot `claude -p` call.

Mirrors `generate/runner.py`'s context-file pattern (a temp JSON file, referenced by path in the
instruction, keeps argv short) and `publish/imagen.py`'s `ClaudePromptRewriter` (a single inline
instruction, no vendored slash-command spec — this is a secondary, best-effort artefact, not the
`/generate` contract). Same OAuth-only env as every other `claude` subprocess call in this
codebase: `CLAUDE_CODE_OAUTH_TOKEN` injected, `ANTHROPIC_API_KEY` stripped.
"""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import tempfile

from minion import config, secrets
from minion.ingest.models import ScrapedSource
from minion.podcast.ports import PodcastGenerationError, ScriptTurn

_INSTRUCTION = """\
You are writing a French two-host "deep dive" podcast script summarizing today's tech-watch \
sources for the file at {context_path}. That file is a JSON array of objects, each with \
"url", "title" and "markdown" (the source's extracted content).

Write a natural, conversational French dialogue between two hosts, named only "A" and "B", \
discussing the most interesting and important stories across these sources — synthesizing \
across sources, not reading them one by one. Aim for roughly {target_words} words total, \
split naturally between both speakers.

Reply with ONLY a JSON array, no preamble or code fences, of objects shaped exactly like:
[{{"speaker": "A", "text": "..."}}, {{"speaker": "B", "text": "..."}}, ...]
Each element is one line of dialogue. Keep individual lines conversational (one or two \
sentences), not monologues.
"""


def _parse_result_text(stdout: str) -> str:
    """Unwrap the `claude --output-format json` envelope into the raw artefact text.

    Mirrors `generate/runner.py::_parse_output`'s fallback: if stdout isn't that envelope,
    treat the whole stdout as the artefact text.
    """
    try:
        envelope = json.loads(stdout)
    except json.JSONDecodeError:
        return stdout
    if isinstance(envelope, dict) and "result" in envelope:
        return str(envelope["result"])
    return stdout


def _parse_turns(text: str) -> list[ScriptTurn]:
    stripped = text.strip()
    # Tolerate a fenced code block even though the instruction asks for none.
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.startswith("json"):
            stripped = stripped[4:]
        stripped = stripped.strip()
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise PodcastGenerationError(f"script response was not valid JSON: {exc}") from exc
    if not isinstance(parsed, list) or not parsed:
        raise PodcastGenerationError("script response was not a non-empty JSON array")
    turns: list[ScriptTurn] = []
    for entry in parsed:
        if not isinstance(entry, dict):
            raise PodcastGenerationError(f"script turn was not an object: {entry!r}")
        speaker = entry.get("speaker")
        line = entry.get("text")
        if speaker not in ("A", "B") or not isinstance(line, str) or not line.strip():
            raise PodcastGenerationError(f"malformed script turn: {entry!r}")
        turns.append(ScriptTurn(speaker=speaker, text=line.strip()))
    return turns


def _build_env() -> dict[str, str]:
    """Inherit env minus `ANTHROPIC_API_KEY`, then inject `CLAUDE_CODE_OAUTH_TOKEN`."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CODE_OAUTH_TOKEN"] = secrets.require(config.ANTHROPIC_OAUTH_TOKEN_SECRET)
    return env


def _write_sources(sources: list[ScrapedSource]) -> str:
    payload = [
        {"url": s.url, "title": s.title or s.url, "markdown": s.markdown or ""} for s in sources
    ]
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", prefix="podcast-sources-", delete=False, encoding="utf-8"
    ) as handle:
        json.dump(payload, handle)
        return handle.name


class ClaudeScriptWriter:
    """`ScriptWriter` over a one-shot `claude -p` subprocess (OAuth-only env)."""

    def write_script(self, sources: list[ScrapedSource], target_words: int) -> list[ScriptTurn]:
        context_path = _write_sources(sources)
        instruction = _INSTRUCTION.format(context_path=context_path, target_words=target_words)
        try:
            result = subprocess.run(
                [
                    "claude",
                    "-p",
                    instruction,
                    "--permission-mode",
                    "bypassPermissions",
                    "--output-format",
                    "json",
                ],
                capture_output=True,
                text=True,
                timeout=config.PODCAST_SCRIPT_TIMEOUT.total_seconds(),
                env=_build_env(),
                check=False,
            )
        except FileNotFoundError as exc:
            raise PodcastGenerationError("claude binary not found on PATH") from exc
        except subprocess.TimeoutExpired as exc:
            raise PodcastGenerationError("podcast script generation timed out") from exc
        finally:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(context_path)

        if result.returncode != 0:
            raise PodcastGenerationError(
                f"claude exited {result.returncode}: {result.stdout[:300] or result.stderr[:300]}"
            )
        return _parse_turns(_parse_result_text(result.stdout))
