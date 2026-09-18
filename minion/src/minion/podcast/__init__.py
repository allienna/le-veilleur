"""Podcast layer: a two-speaker script (Claude) synthesized via Cloud Text-to-Speech, uploaded
to GCS.

Mirrors `publish/`: the podcast step depends on the Protocols in `ports.py`, the production
adapters (`script.py`, `tts.py`, `gcs.py`) implement them, and `fakes.py` provides hermetic
doubles so the whole pipeline runs without Claude, Cloud TTS, GCS, or network in CI.
"""
