# pyright: basic
# ^ wraps a raw JSON API over httpx; like gcs.py this external-boundary adapter is dropped to
# basic checking. Behaviour is covered by FakeAudioSynthesizer + the gated integration test.
"""Production `AudioSynthesizer` over the Cloud Text-to-Speech REST API.

One `text:synthesize` call per script turn (the API is single-utterance, synchronous — there is
no multi-speaker "conversation" mode like NotebookLM's Audio Overview), alternating
`config.PODCAST_VOICE_A`/`_B` by the turn's speaker, then concatenating the returned MP3 bytes
back to back in order. Plain MP3 concatenation (no re-encoding/silence-gap library) is a known
rough edge — it plays back fine in practice for same-codec/same-bitrate MP3 frames, but two
speakers cutting straight into each other with no gap is a coarser result than a real dialogue
engine. Acceptable for a best-effort, secondary artefact; revisit with `pydub`/`ffmpeg` if the
lack of a gap between lines is audibly bad.

`duration_seconds` is estimated from the script's own word count (`config.PODCAST_WORDS_PER_MINUTE`)
rather than inspected from the audio — there is no audio-parsing library in the dependency set,
and this value is informational only (shown in the RSS feed / site), not used to drive playback.

Auth is by impersonating the dedicated `podcast-sa` (`_auth.impersonated_access_token`), not a
stored key.
"""

from __future__ import annotations

import base64

import httpx

from minion import config
from minion.podcast._auth import impersonated_access_token
from minion.podcast.ports import AudioOverviewResult, AudioSynthesisError, ScriptTurn

_SYNTHESIZE_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

_VOICE_BY_SPEAKER = {"A": config.PODCAST_VOICE_A, "B": config.PODCAST_VOICE_B}


class GoogleCloudTtsSynthesizer:
    """`AudioSynthesizer` over the Cloud Text-to-Speech REST API."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(timeout=config.PODCAST_TTS_TIMEOUT.total_seconds())

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {impersonated_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def _synthesize_one(self, turn: ScriptTurn, language_code: str) -> bytes:
        payload = {
            "input": {"text": turn.text},
            "voice": {"languageCode": language_code, "name": _VOICE_BY_SPEAKER[turn.speaker]},
            "audioConfig": {"audioEncoding": "MP3"},
        }
        try:
            response = self._client.post(_SYNTHESIZE_URL, headers=self._headers(), json=payload)
        except httpx.HTTPError as exc:
            raise AudioSynthesisError(f"Cloud TTS request failed: {exc}") from exc
        if response.is_error:
            raise AudioSynthesisError(
                f"Cloud TTS returned {response.status_code}: {response.text[:300]}"
            )
        body = response.json()
        encoded = body.get("audioContent")
        if not encoded:
            raise AudioSynthesisError("Cloud TTS response carried no audioContent")
        try:
            return base64.b64decode(encoded)
        except (ValueError, TypeError) as exc:
            raise AudioSynthesisError(
                f"Cloud TTS returned unparseable audioContent: {exc}"
            ) from exc

    def synthesize(self, turns: list[ScriptTurn], language_code: str) -> AudioOverviewResult:
        chunks = [self._synthesize_one(turn, language_code) for turn in turns]
        total_words = sum(len(turn.text.split()) for turn in turns)
        duration_seconds = round(total_words / config.PODCAST_WORDS_PER_MINUTE * 60)
        return AudioOverviewResult(
            audio_bytes=b"".join(chunks),
            content_type="audio/mpeg",
            duration_seconds=duration_seconds,
        )
