"""Pure formatting: turn a finished `Run` (plus its final data bag) into an HTML email.

No I/O, no port dependency — trivially unit-testable. `cli.py` calls this, then hands the
result to a `Notifier`. The look borrows the site's own header (site/src/layouts/BaseLayout.astro:
slate-900 bar, amber owl badge, Poppins/Work Sans) and palette (site/tailwind.config.mjs), kept to
inline styles + table layout since this ships as raw HTML in an email, not through Astro/Tailwind.
"""

from __future__ import annotations

import base64
import html
import re
from collections.abc import Mapping
from urllib.parse import quote, unquote, urlparse

from minion import secrets
from minion.config import ARTICLE_URL_TEMPLATE, CLOUD_RUN_JOB_NAME, CLOUD_RUN_REGION
from minion.fiches.extract import extract_cited_sources
from minion.generate.models import AssembledContext, GeneratedArticle
from minion.ingest.models import SourceOutcome, SourceSet
from minion.models import Run, RunStatus, StepName
from minion.podcast.models import PodcastArtifact
from minion.publish.models import ImageArtifact

_STATUS_LABELS: dict[RunStatus, str] = {
    RunStatus.success: "OK",
    RunStatus.success_with_warnings: "OK (avertissement)",
    RunStatus.skipped: "SKIPPED",
    RunStatus.failure: "KO",
    RunStatus.aborted: "ABORTED",
    RunStatus.running: "EN COURS",
}

# (background, text) — mirrors the site's amber/navy palette for OK, standard semantic colors
# for warning/skip/failure so the status reads at a glance in an inbox list.
_STATUS_COLORS: dict[RunStatus, tuple[str, str]] = {
    RunStatus.success: ("#dcfce7", "#166534"),
    RunStatus.success_with_warnings: ("#fef3c7", "#92400e"),
    RunStatus.skipped: ("#e2e8f0", "#334155"),
    RunStatus.failure: ("#fee2e2", "#991b1b"),
    RunStatus.aborted: ("#e2e8f0", "#334155"),
    RunStatus.running: ("#e2e8f0", "#334155"),
}

_NAVY = "#0f172a"  # site's slate-900 header bar
_AMBER = "#f59f0a"  # site's `primary`
_CREAM = "#f8f7f5"  # site's `background-light`

# Click-tracking wrappers (TLDR's `tracking.tldrnewsletter.com/CL0/<encoded target>/1/...`) hide
# the real destination; the encoded target is what a reader wants to recognise.
_TRACKED_TARGET = re.compile(r"/CL0/([^/]+)")

# Why an ingested source never reached /generate, by scrape outcome. An OK source missing from
# the context was cut by `assemble`: a duplicate title, the IA cap or the token budget.
_EXCLUDED_REASONS: dict[SourceOutcome, str] = {
    SourceOutcome.ok: "doublon ou plafond IA",
    SourceOutcome.paywalled: "payante",
    SourceOutcome.failed: "échec du téléchargement",
}


def _published(run: Run) -> bool:
    """Whether the `github` step actually committed the article this run."""
    return any(s.name is StepName.github and s.status is RunStatus.success for s in run.steps)


def _duration(run: Run) -> str | None:
    if run.started_at is None or run.ended_at is None:
        return None
    total_seconds = int((run.ended_at - run.started_at).total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}m{seconds:02d}s"


def _logs_url(run: Run) -> str:
    query = (
        'resource.type="cloud_run_job" '
        f'resource.labels.job_name="{CLOUD_RUN_JOB_NAME}" '
        f'resource.labels.location="{CLOUD_RUN_REGION}" '
        f'jsonPayload.runId="{run.run_id}"'
    )
    return (
        f"https://console.cloud.google.com/logs/query;query={quote(query)}"
        f"?project={secrets.PROJECT_ID}"
    )


def _target_host(url: str) -> str:
    """The host a reader would recognise: the tracked target's, else the URL's own."""
    match = _TRACKED_TARGET.search(url)
    target = unquote(match.group(1)) if match else url
    return urlparse(target).netloc.removeprefix("www.") or url


def _source_item_html(url: str, title: str, note: str) -> str:
    """One linked source: its title (else the target host), then host and note in grey."""
    host = _target_host(url)
    meta = " · ".join(part for part in (host if title else "", note) if part)
    meta_html = f'<span style="color:#94a3b8;"> — {html.escape(meta)}</span>' if meta else ""
    return (
        f'<li style="margin-bottom:4px;"><a href="{html.escape(url)}" '
        f'style="color:{_NAVY};text-decoration:none;">{html.escape(title or host)}</a>'
        f"{meta_html}</li>"
    )


def _source_group_html(heading: str, items: list[str]) -> str:
    if not items:
        return ""
    return f"""
        <div style="font-size:13px;font-weight:700;color:{_NAVY};margin:14px 0 6px;">
          {html.escape(heading)} ({len(items)})
        </div>
        <ul style="margin:0;padding-left:18px;font-size:13px;line-height:1.45;color:#1e293b;">
          {"".join(items)}
        </ul>"""


def _sources_section_html(data: Mapping[str, object], article: GeneratedArticle | None) -> str:
    """Every source the run ingested: cited, read but not cited, and dropped before /generate."""
    source_set = data.get("sources")
    context = data.get("context")
    if not isinstance(source_set, SourceSet):
        return ""
    read = context.sources if isinstance(context, AssembledContext) else []
    cited = extract_cited_sources(article.body, read) if article is not None else []
    cited_urls = {s.url for s in cited}
    read_urls = {s.url for s in read}

    excluded = sorted(
        (s for s in source_set.sources if s.url not in read_urls),
        key=lambda s: list(_EXCLUDED_REASONS).index(s.outcome),
    )
    groups = [
        _source_group_html(
            "Citées dans l'article",
            [_source_item_html(s.url, s.title, s.theme_hint) for s in cited],
        ),
        _source_group_html(
            "Lues par Claude, non citées",
            [
                _source_item_html(s.url, s.title, s.theme_hint)
                for s in read
                if s.url not in cited_urls
            ],
        ),
        _source_group_html(
            "Écartées avant Claude",
            [
                _source_item_html(s.url, s.title or "", _EXCLUDED_REASONS[s.outcome])
                for s in excluded
            ],
        ),
    ]
    return f"""
      <tr><td style="padding:24px 32px 0;">
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.04em;color:#64748b;">
          Sources du jour
        </div>
        {"".join(groups)}
      </td></tr>"""


def _linkedin_share_url(article_url: str) -> str:
    return f"https://www.linkedin.com/sharing/share-offsite/?url={quote(article_url, safe='')}"


def _hero_image_html(data: Mapping[str, object]) -> str:
    image = data.get("image")
    if not isinstance(image, ImageArtifact) or not image.available:
        return ""
    encoded = base64.b64encode(image.png).decode("ascii")
    return f"""
      <tr><td style="padding:20px 32px 0;">
        <img src="data:image/png;base64,{encoded}" width="536" alt="Illustration du jour"
             style="width:100%;max-width:536px;border-radius:8px;display:block;" />
      </td></tr>"""


def _article_section_html(run: Run, article: GeneratedArticle | None) -> str:
    if not _published(run):
        return """
      <tr><td style="padding:20px 32px 0;font-size:14px;color:#64748b;">
        Article : pas publié ce run.
      </td></tr>"""
    url = ARTICLE_URL_TEMPLATE.format(date=run.date)
    title = html.escape(article.frontmatter.title) if article is not None else ""
    heading = (
        f'<div style="font-size:18px;font-weight:700;color:{_NAVY};margin-bottom:12px;">'
        f"{title}</div>"
        if title
        else ""
    )
    return f"""
      <tr><td style="padding:20px 32px 0;text-align:center;">
        {heading}
        <a href="{url}"
           style="display:inline-block;background:{_AMBER};color:{_NAVY};font-weight:700;
                  font-size:14px;padding:12px 28px;border-radius:8px;text-decoration:none;">
          Lire l'article
        </a>
      </td></tr>"""


def _linkedin_section_html(run: Run, article: GeneratedArticle | None) -> str:
    if article is None:
        body = "(aucun article généré ce run)"
        share_button = ""
    else:
        body = html.escape(article.linkedin.strip())
        share_button = ""
        if _published(run):
            share_url = _linkedin_share_url(ARTICLE_URL_TEMPLATE.format(date=run.date))
            share_button = f"""
        <div style="margin-top:12px;">
          <a href="{share_url}"
             style="font-size:13px;font-weight:700;color:{_NAVY};text-decoration:none;
                    border:1px solid #cbd5e1;border-radius:8px;padding:8px 16px;
                    display:inline-block;">
            Partager sur LinkedIn
          </a>
        </div>"""
    return f"""
      <tr><td style="padding:24px 32px 0;">
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.04em;color:#64748b;margin-bottom:8px;">
          Post LinkedIn
        </div>
        <div style="background:{_CREAM};border:1px solid #e5e5e0;border-radius:8px;
                    padding:16px;font-size:14px;line-height:1.5;color:#1e293b;
                    white-space:pre-wrap;">{body}</div>
        {share_button}
      </td></tr>"""


def _status_section_html(run: Run) -> str:
    label = _STATUS_LABELS[run.status]
    bg, fg = _STATUS_COLORS[run.status]
    lines = [f"Statut : {label} ({run.status.value})"]
    if run.error:
        lines.append(f"Raison : {html.escape(run.error)}")
    failed_items = "".join(
        f"<li>{html.escape(step.name.value)}: {html.escape(step.error or '')}</li>"
        for step in run.steps
        if step.status is RunStatus.failure
    )
    failed_html = (
        f'<ul style="margin:8px 0 0;padding-left:20px;font-size:13px;color:#991b1b;">'
        f"{failed_items}</ul>"
        if failed_items
        else ""
    )
    reason_html = ""
    if len(lines) > 1:
        reason_html = (
            f'<div style="margin-top:8px;font-size:13px;color:#475569;">'
            f"{html.escape(lines[1])}</div>"
        )
    return f"""
      <tr><td style="padding:20px 32px 0;">
        <span style="display:inline-block;padding:6px 14px;border-radius:999px;
                     font-size:13px;font-weight:700;background:{bg};color:{fg};">
          {html.escape(lines[0])}
        </span>
        {reason_html}
        {failed_html}
      </td></tr>"""


def _metrics_html(run: Run, data: Mapping[str, object]) -> str:
    parts: list[str] = []
    if run.cost_usd is not None or run.tokens is not None:
        cost = f"{run.cost_usd:.2f} $" if run.cost_usd is not None else "?"
        tokens = f"{run.tokens} tokens" if run.tokens is not None else "? tokens"
        parts.append(f"Coût : {cost} ({tokens})")
    duration = _duration(run)
    if duration is not None:
        parts.append(f"Durée : {duration}")
    sources = data.get("sources")
    if isinstance(sources, SourceSet):
        parts.append(
            f"Sources : {sources.ok_count} OK / {sources.total} "
            f"({sources.paywalled_count} payantes, {sources.failed_count} échouées)"
        )
    if not parts:
        return ""
    return f"""
      <tr><td style="padding:20px 32px 0;font-size:13px;color:#64748b;">
        {" · ".join(html.escape(p) for p in parts)}
      </td></tr>"""


def _podcast_section_html(data: Mapping[str, object]) -> str:
    episode = data.get("podcast")
    if not isinstance(episode, PodcastArtifact) or not episode.available:
        return ""
    return f"""
      <tr><td style="padding:20px 32px 0;">
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.04em;color:#64748b;margin-bottom:8px;">
          Épisode du jour
        </div>
        <a href="{html.escape(episode.audio_url)}"
           style="font-size:14px;color:{_NAVY};text-decoration:underline;">
          Écouter l'épisode
        </a>
      </td></tr>"""


def build_message(run: Run, data: Mapping[str, object]) -> tuple[str, str]:
    """Return `(subject, html_body)` for `run`'s post-run notification email."""
    label = _STATUS_LABELS[run.status]
    article = data.get("article")
    if not isinstance(article, GeneratedArticle):
        article = None

    body = f"""<!doctype html>
<html lang="fr">
  <body style="margin:0;padding:0;background:{_CREAM};
               font-family:'Poppins','Work Sans','Segoe UI',Arial,sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
           style="background:{_CREAM};padding:24px 0;">
      <tr><td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0"
               style="max-width:600px;width:100%;background:#ffffff;border-radius:12px;
                      overflow:hidden;border:1px solid #e5e5e0;">
          <tr><td style="background:{_NAVY};padding:24px 32px;">
            <table role="presentation" cellpadding="0" cellspacing="0"><tr>
              <td style="width:40px;height:40px;background:{_AMBER};border-radius:50%;
                         text-align:center;vertical-align:middle;font-size:20px;">🦉</td>
              <td style="padding-left:12px;color:#ffffff;font-size:20px;font-weight:900;
                         letter-spacing:-0.02em;text-transform:uppercase;">Le Veilleur</td>
            </tr></table>
            <div style="color:#94a3b8;font-size:13px;margin-top:8px;">{run.date} — {label}</div>
          </td></tr>
          {_status_section_html(run)}
          {_hero_image_html(data)}
          {_article_section_html(run, article)}
          {_linkedin_section_html(run, article)}
          {_metrics_html(run, data)}
          {_sources_section_html(data, article)}
          {_podcast_section_html(data)}
          <tr><td style="padding:24px 32px 32px;">
            <a href="{_logs_url(run)}" style="font-size:12px;color:#94a3b8;">Voir les logs</a>
          </td></tr>
        </table>
      </td></tr>
    </table>
  </body>
</html>"""

    subject = f"Le Veilleur — {run.date} — {label}"
    if article is not None:
        subject += f" — {article.frontmatter.title}"
    return subject, body
