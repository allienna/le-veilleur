"""Podcast layer: the NotebookLM Enterprise audio overview + its GCS upload.

Mirrors `publish/`: the podcast step depends on the Protocols in `ports.py`, the production
adapters (`notebooklm.py`, `gcs.py`) implement them, and `fakes.py` provides hermetic doubles so
the whole pipeline runs without NotebookLM Enterprise, GCS, or network in CI.
"""
