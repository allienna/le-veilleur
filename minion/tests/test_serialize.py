"""Slug derivation + Astro content serialization.

The shapes asserted here are the site's content-collection schemas
(site/src/content/config.ts). If these tests drift from that file, `astro build` breaks.
"""

from __future__ import annotations

from minion import config
from minion.fiches.models import FicheDoc
from minion.generate.models import ArticleFrontmatter, GeneratedArticle
from minion.publish.serialize import (
    count_sources,
    normalize_themes,
    render_fiche,
    render_post,
    slugify,
)


def test_slugify_basic() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_folds_accents() -> None:
    assert slugify("Le Veilleur déchaîné") == "le-veilleur-dechaine"


def test_slugify_collapses_punctuation_and_strips_edges() -> None:
    assert slugify("  --AI & Cloud: 2026 edition!--  ") == "ai-cloud-2026-edition"


def test_slugify_caps_length_without_trailing_hyphen() -> None:
    slug = slugify("word " * 40)  # far exceeds the cap
    assert len(slug) <= config.SLUG_MAX_LEN
    assert not slug.endswith("-")


def test_slugify_falls_back_when_empty() -> None:
    assert slugify("???") == "source"


_BODY = """# Titre

Intro [[1](https://a.example/x)].

---

## Sources

1. [A](https://a.example/x)
2. [B](https://b.example/y)

## Pour aller plus loin

- [C](https://c.example/z) — parce que.
"""


def _article(body: str = _BODY, **fm: object) -> GeneratedArticle:
    base: dict[str, object] = {
        "title": "T",
        "date": "2026-06-01",
        "themes": ["IA"],
        "image": "2026-06-01.png",
    }
    base.update(fm)
    return GeneratedArticle(
        theme="IA",
        frontmatter=ArticleFrontmatter.model_validate(base),
        body=body,
        linkedin="post",
        image_prompt="prompt",
    )


def test_count_sources_counts_only_the_sources_list() -> None:
    """ "Pour aller plus loin" entries must not inflate the count the site displays."""
    assert count_sources(_BODY) == 2


def test_count_sources_is_zero_without_a_sources_section() -> None:
    assert count_sources("# Titre\n\nJuste du texte.\n") == 0


def test_normalize_themes_orders_by_site_frequency_and_caps() -> None:
    themes = normalize_themes(["Data", "Tech", "IA", "Leadership"])
    assert themes == ["IA", "Leadership", "Tech"]  # capped at MAX_THEMES, priority order


def test_normalize_themes_drops_unknown_labels() -> None:
    assert normalize_themes(["IA", "Blockchain"]) == ["IA"]


def test_normalize_themes_never_returns_empty() -> None:
    """An article with no theme would vanish from every tag page."""
    assert normalize_themes(["Blockchain"]) == [config.DEFAULT_THEME]


def test_render_post_field_order_matches_the_site() -> None:
    out = render_post(_article())
    assert out.startswith("---\n") and "\n---\n\n" in out
    fm_block = out[: out.index("\n---\n\n")]
    order = [line.split(":")[0] for line in fm_block.splitlines() if ":" in line and line != "---"]
    assert order == ["title", "date", "themes", "sources", "image"]


def test_render_post_derives_the_source_count_from_the_body() -> None:
    assert "sources: 2" in render_post(_article())


def test_render_post_emits_bare_date_and_bare_theme_sequence() -> None:
    out = render_post(_article())
    assert "date: 2026-06-01" in out  # unquoted, matching the site's other articles
    assert "themes: [IA]" in out


def test_render_post_quotes_and_escapes_scalars() -> None:
    out = render_post(_article(title='A "quoted": colon'))
    assert 'title: "A \\"quoted\\": colon"' in out


def test_render_post_omits_image_when_imagen_gave_up() -> None:
    """No `image` key at all, so the site falls back to its own placeholder SVG."""
    out = render_post(_article(image=""))
    assert "image:" not in out


def _fiche(**over: object) -> FicheDoc:
    base: dict[str, object] = {
        "slug": "a-source",
        "title": "A Source",
        "date": "2026-06-01",
        "url": "https://a.example/x",
        "authors": ["Someone"],
        "keywords": ["agents", "IA"],
        "theme": "IA",
        "tone": "opinion",
        "used_in": ["2026-06-01"],
        "body": "## Résumé\n\nDu texte.\n",
    }
    base.update(over)
    return FicheDoc.model_validate(base)


def test_render_fiche_uses_english_keys() -> None:
    """French keys do not match the Astro schema and fail the build."""
    out = render_fiche(_fiche())
    fm_block = out[: out.index("\n---\n\n")]
    order = [line.split(":")[0] for line in fm_block.splitlines() if ":" in line and line != "---"]
    assert order == ["title", "date", "url", "authors", "keywords", "theme", "tone", "used_in"]


def test_render_fiche_omits_optional_fields_when_absent() -> None:
    out = render_fiche(_fiche(authors=[], tone=None))
    assert "authors:" not in out and "tone:" not in out
    assert 'used_in: ["2026-06-01"]' in out
