"""The `/generate` spec and the Python models must agree.

`.claude/commands/generate.md` is the prompt shipped in the image; `GeneratedArticle` is what the
pipeline parses its output into. They are written in different files, in different languages, and
nothing but this test stops them from drifting — a drift that would only surface as a failed
production run.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from minion import config
from minion.generate.models import GeneratedArticle
from minion.publish.serialize import count_sources

SPEC = Path(__file__).resolve().parents[1] / ".claude" / "commands" / "generate.md"


def _spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def _contract_example() -> dict[str, object]:
    """The first ```json block in the spec that carries the output shape (has a `body` key)."""
    for block in re.findall(r"```json\n(.*?)```", _spec_text(), re.DOTALL):
        # The example uses `…` placeholders, so swap them for parseable strings.
        candidate = block.replace("…", "x")
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict) and "body" in parsed:
            return parsed
    raise AssertionError("no output-shape example found in generate.md")


def test_spec_exists_where_the_dockerfile_copies_it() -> None:
    assert SPEC.is_file(), f"missing {SPEC}"


def test_contract_example_validates_against_the_model() -> None:
    """`extra="forbid"` means a stray key in the spec's example is a real production failure."""
    article = GeneratedArticle.model_validate(_contract_example())
    assert article.frontmatter.themes


def test_spec_lists_exactly_the_configured_themes() -> None:
    spec = _spec_text()
    for theme in config.THEME_ALLOWLIST:
        assert f"`{theme}`" in spec, f"theme {theme!r} missing from the spec's allowlist"


def test_spec_states_the_real_caps() -> None:
    """A cap stated wrongly in the prompt sends the model into a retry loop it cannot exit."""
    spec = _spec_text()
    assert str(config.MAX_LINKEDIN_CHARS) in spec
    assert str(config.MAX_IMAGE_PROMPT_CHARS) in spec
    assert str(config.WHOLESALE_NGRAM) in spec
    assert str(config.MAX_QUOTE_WORDS) in spec


def test_spec_forbids_the_frontmatter_keys_the_model_would_reject() -> None:
    spec = _spec_text()
    for key in ("image", "sources", "description", "tags", "kind"):
        assert f"`{key}`" in spec, f"the spec must tell the model not to emit {key!r}"


def test_spec_sources_example_is_parseable_by_count_sources() -> None:
    """The article template's Sources list must match the parser that derives the source count,
    or every published article would claim `sources: 0`."""
    template = re.search(r"```markdown\n(.*?)```", _spec_text(), re.DOTALL)
    assert template is not None
    assert count_sources(template.group(1)) == 2  # the two entries in the template
