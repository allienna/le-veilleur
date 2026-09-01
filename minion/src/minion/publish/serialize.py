"""Deterministic slug + Astro content-file serialization.

Pure functions, no I/O. A dependency-free YAML emitter keeps the frontmatter contract small and
auditable (the field sets are fully controlled by the models here) and avoids a `pyyaml` review.
Stable field ordering keeps GitHub commits byte-idempotent across replays.

The emitted shapes match site/src/content/config.ts exactly — the `articles` and `fiches`
collections. Deviating breaks the Astro build, which is the real gate.
"""

from __future__ import annotations

import re
import unicodedata

from minion import config
from minion.fiches.models import FicheDoc
from minion.generate.models import GeneratedArticle

_NON_SLUG = re.compile(r"[^a-z0-9]+")
# A numbered entry in the body's `## Sources` list, e.g. `3. [Titre](https://…)`.
_SOURCE_ENTRY = re.compile(r"^\d+\.\s*\[.*\]\(\S+\)\s*$")


def slugify(title: str) -> str:
    """Turn a title into a URL-safe slug: NFKD ASCII-fold → lowercase → hyphenate → cap length.

    Falls back to "source" when the title has no slug-able characters (e.g. all punctuation).
    """
    folded = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = _NON_SLUG.sub("-", folded.lower()).strip("-")
    slug = slug[: config.SLUG_MAX_LEN].rstrip("-")  # trim any hyphen left by truncation
    return slug or "source"


def count_sources(body: str) -> int:
    """Count the numbered entries under the body's `## Sources` heading.

    The site renders this as "• N sources", so it must match what the article actually cites.
    Derived here rather than asked of the model: one less field to trust and to validate.
    """
    total, inside = 0, False
    for line in body.splitlines():
        if line.startswith("## Sources"):
            inside = True
            continue
        if inside:
            if line.startswith("## "):  # next section ends the list
                break
            if _SOURCE_ENTRY.match(line.strip()):
                total += 1
    return total


def normalize_themes(themes: list[str]) -> list[str]:
    """Keep only known theme labels, de-duplicated, ordered by site frequency, capped.

    An empty result falls back to `DEFAULT_THEME` — an article with no theme would vanish from
    every tag page, so the pipeline never emits one.
    """
    kept = {t for t in themes if t in config.THEME_ALLOWLIST}
    ordered = [t for t in config.THEME_PRIORITY if t in kept]
    return ordered[: config.MAX_THEMES] or [config.DEFAULT_THEME]


def _yaml_scalar(value: str) -> str:
    """Emit a double-quoted YAML scalar with `"` and `\\` escaped."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _yaml_quoted_seq(values: list[str]) -> str:
    """Emit a YAML flow sequence of quoted scalars, e.g. `["a", "b"]`."""
    return "[" + ", ".join(_yaml_scalar(v) for v in values) + "]"


def _yaml_bare_seq(values: list[str]) -> str:
    """Emit a YAML flow sequence of bare scalars, e.g. `[IA, Leadership]`.

    Only for values from a closed vocabulary with no YAML metacharacters — the theme labels.
    """
    return "[" + ", ".join(values) + "]"


def _frontmatter(lines: list[str], body: str) -> str:
    return "---\n" + "\n".join(lines) + "\n---\n\n" + body.rstrip() + "\n"


def render_post(article: GeneratedArticle) -> str:
    """Serialize the article to `site/src/content/articles/{date}.md`.

    `image` is omitted entirely when the Imagen step could not supply one: the site's layouts
    fall back to their own placeholder SVG, which beats committing a broken filename.
    """
    fm = article.frontmatter
    lines = [
        f"title: {_yaml_scalar(fm.title)}",
        f"date: {fm.date}",
        f"themes: {_yaml_bare_seq(normalize_themes(fm.themes))}",
        f"sources: {count_sources(article.body)}",
    ]
    if fm.image:
        lines.append(f"image: {fm.image}")
    return _frontmatter(lines, article.body)


def render_fiche(fiche: FicheDoc) -> str:
    """Serialize one fiche to `site/src/content/fiches/{date}-{slug}.md`.

    The frontmatter keys are English on purpose: French keys do not match the Astro schema and
    fail the build.
    """
    lines = [
        f"title: {_yaml_scalar(fiche.title)}",
        f"date: {fiche.date}",
        f"url: {_yaml_scalar(fiche.url)}",
    ]
    if fiche.authors:
        lines.append(f"authors: {_yaml_quoted_seq(fiche.authors)}")
    lines.append(f"keywords: {_yaml_quoted_seq(fiche.keywords)}")
    lines.append(f"theme: {_yaml_scalar(fiche.theme)}")
    if fiche.tone:
        lines.append(f"tone: {_yaml_scalar(fiche.tone)}")
    lines.append(f"used_in: {_yaml_quoted_seq(fiche.used_in)}")
    return _frontmatter(lines, fiche.body)
