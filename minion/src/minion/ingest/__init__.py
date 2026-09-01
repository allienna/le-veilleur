"""Ingestion subpackage: real Gmail + scrape steps and their supporting models.

Mirrors the `store/` layout — `ports.py` declares the `GmailClient` / `ScraperClient` Protocols
the steps depend on, `gmail.py` / `scraper.py` are the production implementations, `fakes.py`
holds hermetic test doubles, `models.py` the Minion-internal Pydantic boundary models, and
`extract.py` the pure URL-extraction helpers — all intermediate pipeline values carried in the
orchestrator data bag.
"""

from __future__ import annotations
