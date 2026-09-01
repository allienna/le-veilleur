# infra/

Infrastructure-as-code for the pipeline. Terraform, GCP project `veilleur-app`, region
`europe-west1`. Operate it with [`RUNBOOK.md`](RUNBOOK.md).

| File | Resources |
|------|-----------|
| `versions.tf` / `variables.tf` | Provider pins; `project_id`, `region`, `billing_account`, `budget_amount_eur`, `image_tag`. |
| `apis.tf` | Every API the pipeline needs. |
| `registry.tf` | The Artifact Registry repo for the Minion image, and the four secret *slots* (values are added by `scripts/add-secret-versions.sh`, never by Terraform). |
| `iam.tf` | Runtime `minion-sa` (per-secret accessor only — no project roles), `scheduler-invoker-sa`, `budget-killswitch-sa`. |
| `job.tf` | Cloud Run Job `minion` — `timeout=1200s`, `max_retries=0`, `memory=1Gi`, image under `ignore_changes` + `run.invoker` for the scheduler SA. |
| `scheduler.tf` | Cloud Scheduler `minion-daily` — `0 6 * * *` Europe/Paris, OAuth token → Jobs `:run`. |
| `killswitch.tf` | Monthly budget → Pub/Sub → 2nd-gen function that pauses the Scheduler at 100%. |
| `outputs.tf` | Job/scheduler names, SA emails, Artifact Registry URL. |

## Why the project is still called `veilleur-app`

A GCP project id cannot be renamed, and this one already holds the provisioned secrets, the
Artifact Registry repo and the budget. It is invisible from the outside: only the GitHub repo name
reaches users, through the Pages URL. Renaming would mean re-provisioning every secret for no
user-visible gain.

## State

This root is **self-contained** — it owns every resource the pipeline needs. The veilleur-app PoC
split the shared singletons (secrets, Artifact Registry, APIs) into a separate throwaway "spike"
state; that split is consolidated here.

**Consequence, and the one thing to get right before the first apply:** several of those resources
already exist in the project, created by that other state. Terraform does not know about them, so
a naive `apply` fails with "already exists". Import them first — see RUNBOOK.md §0.

There is no remote backend configured, so the state is local. Keep it somewhere durable and
backed up, or add a GCS backend before this matters.

## No Vertex AI, no Firestore

The Minion's entire authority is accessor on four secrets. Image generation goes through a Gemini
API key rather than Vertex IAM (which also lets the pipeline run on a laptop with no GCP
credentials), and there is no datastore: run state is in-process, and published artefacts live in
the git repo.
