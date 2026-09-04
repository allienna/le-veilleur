"""Pure formatting: turn a finished `Run` (plus its final data bag) into an email.

No I/O, no port dependency — trivially unit-testable. `cli.py` calls this, then hands the
result to a `Notifier`.
"""

from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import quote

from minion import secrets
from minion.config import ARTICLE_URL_TEMPLATE, CLOUD_RUN_JOB_NAME, CLOUD_RUN_REGION
from minion.generate.models import GeneratedArticle
from minion.models import Run, RunStatus, StepName

_STATUS_LABELS: dict[RunStatus, str] = {
    RunStatus.success: "OK",
    RunStatus.success_with_warnings: "OK (avertissement)",
    RunStatus.skipped: "SKIPPED",
    RunStatus.failure: "KO",
    RunStatus.aborted: "ABORTED",
    RunStatus.running: "EN COURS",
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


def build_message(run: Run, data: Mapping[str, object]) -> tuple[str, str]:
    """Return `(subject, body)` for `run`'s post-run notification email."""
    label = _STATUS_LABELS[run.status]
    lines: list[str] = [f"Statut : {label} ({run.status.value})"]
    if run.error:
        lines.append(f"Raison : {run.error}")
    for step in run.steps:
        if step.status is RunStatus.failure:
            lines.append(f"  - {step.name.value}: {step.error}")

    lines.append("")
    if _published(run):
        lines.append(f"Article : {ARTICLE_URL_TEMPLATE.format(date=run.date)}")
    else:
        lines.append("Article : pas publié ce run.")

    article = data.get("article")
    lines.append("")
    lines.append("Post LinkedIn :")
    lines.append("---")
    if isinstance(article, GeneratedArticle):
        lines.append(article.linkedin.strip())
    else:
        lines.append("(aucun article généré ce run)")
    lines.append("---")

    if run.cost_usd is not None or run.tokens is not None:
        cost = f"{run.cost_usd:.2f} $" if run.cost_usd is not None else "?"
        tokens = f"{run.tokens} tokens" if run.tokens is not None else "? tokens"
        lines.append("")
        lines.append(f"Coût : {cost} ({tokens})")

    duration = _duration(run)
    if duration is not None:
        lines.append(f"Durée : {duration}")

    lines.append("")
    lines.append(f"Logs : {_logs_url(run)}")

    subject = f"Le Veilleur — {run.date} — {label}"
    return subject, "\n".join(lines)
