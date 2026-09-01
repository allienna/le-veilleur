"""Smoke test: the minion package imports cleanly, with no credentials present."""

import importlib


def test_package_imports() -> None:
    assert importlib.import_module("minion") is not None
