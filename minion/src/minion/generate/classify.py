"""Deterministic theme hint for one source — a keyword score, not a model call.

It runs inside `assemble`, on every OK source of the day, so it has to be free and instant: an
LLM classifier would add a `claude -p` call to a run already bounded at 20 minutes. It only has
to be good enough to stop a GenAI-heavy inbox from becoming a GenAI-only reading list; the
article's real theme is still chosen by `/generate`.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from functools import cache

from minion import config

# A title hit says more about the subject than a passing mention in the body.
_TITLE_WEIGHT = 3


@cache
def _pattern(keyword: str) -> re.Pattern[str]:
    """Word-bounded, case-insensitive; a trailing `*` turns the keyword into a prefix."""
    prefix = keyword.endswith("*")
    body = re.escape(keyword.removesuffix("*"))
    return re.compile(rf"(?<!\w){body}{'' if prefix else r'(?!\w)'}", re.IGNORECASE)


def _hits(text: str, keywords: Iterable[str]) -> int:
    return sum(len(_pattern(k).findall(text)) for k in keywords)


def classify(title: str, markdown: str) -> str:
    """The best-scoring theme of `config.THEME_KEYWORDS`, or `config.DEFAULT_THEME` on no hit.

    `config.NON_DOMINANT_THEME` (IA) must outscore every other theme by `IA_DOMINANCE_RATIO` to
    win; otherwise the best of the rest does. Ties go to the theme ranked first in
    `config.THEME_PRIORITY`.
    """
    head = markdown[: config.CLASSIFY_HEAD_CHARS]
    scores = {
        theme: _TITLE_WEIGHT * _hits(title, keywords) + _hits(head, keywords)
        for theme, keywords in config.THEME_KEYWORDS.items()
    }
    ia = scores.pop(config.NON_DOMINANT_THEME, 0)
    best = max(scores.values(), default=0)
    if ia > 0 and ia >= config.IA_DOMINANCE_RATIO * best:
        return config.NON_DOMINANT_THEME
    if best == 0:
        return config.DEFAULT_THEME
    return next(t for t in config.THEME_PRIORITY if scores.get(t, 0) == best)
