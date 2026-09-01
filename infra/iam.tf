# Service accounts + IAM for the pipeline. All bindings are additive — they reference the
# secrets by ID and never grant project-wide secret access (least privilege).

# ─── Runtime SA: the identity the Cloud Run Job executes as ───────────────────────────────
resource "google_service_account" "minion" {
  account_id   = "minion-sa"
  display_name = "Le Veilleur Minion runtime SA"
}

# Per-secret accessor on exactly the four secrets the Minion reads at runtime.
# `anthropic-api-key-fallback` is deliberately never granted: the agentic steps authenticate with
# CLAUDE_CODE_OAUTH_TOKEN only, and secrets.py raises if ANTHROPIC_API_KEY is present.
locals {
  minion_runtime_secrets = [
    "gmail-oauth-refresh-token",
    "anthropic-oauth-token",
    "github-pat",     # fine-grained, contents:write on allienna/le-veilleur only
    "gemini-api-key", # Imagen 4 Fast via the Gemini API
  ]
}

resource "google_secret_manager_secret_iam_member" "minion_accessor" {
  for_each = toset(local.minion_runtime_secrets)

  # Fully-qualified resource name (not the short id) so the binding can't accidentally resolve
  # against a different project if provider config changes.
  secret_id = "projects/${var.project_id}/secrets/${each.key}"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.minion.email}"
}

# No project-level roles: image generation goes through the Gemini API key rather than Vertex
# IAM, and there is no Firestore any more (run state is in-process, artefacts live in the repo).
# The four secret bindings above are the Minion's entire authority.

# ─── Scheduler invoker SA: only run.invoker on the Job (binding lives in job.tf) ──────────
resource "google_service_account" "scheduler_invoker" {
  account_id   = "scheduler-invoker-sa"
  display_name = "Cloud Scheduler → Minion Job invoker"
}

# ─── Kill-switch function SA: pause the Scheduler on a 100% budget event ──────────────────
resource "google_service_account" "killswitch" {
  account_id   = "budget-killswitch-sa"
  display_name = "Budget kill-switch function SA"
}

# Scoped to Scheduler admin so the function can pause/resume the daily job. Project-level
# is the tightest the Scheduler IAM surface supports for a pause action.
resource "google_project_iam_member" "killswitch_scheduler_admin" {
  project = var.project_id
  role    = "roles/cloudscheduler.admin"
  member  = "serviceAccount:${google_service_account.killswitch.email}"
}
