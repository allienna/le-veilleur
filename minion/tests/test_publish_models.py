"""Publish artefact models: defaults and `extra="forbid"` enforcement."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from minion.publish.models import CommitResult, ImageArtifact


def test_image_artifact_reports_available_when_bytes_present() -> None:
    art = ImageArtifact(filename="2026-06-01.png", png=b"\x89PNGxxxx")
    assert art.available is True
    assert art.png == b"\x89PNGxxxx"


def test_image_artifact_is_unavailable_when_imagen_gave_up() -> None:
    """Empty bytes are the "no hero image" signal the github step reads to skip the commit."""
    assert ImageArtifact(filename="2026-06-01.png", png=b"").available is False


def test_commit_result_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        CommitResult.model_validate({"path": "p", "sha": "abc", "unexpected": 1})
