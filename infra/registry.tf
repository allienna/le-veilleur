# The Artifact Registry repo holding the Minion image, and the four secret *slots* the Minion
# reads at run time. Values are NOT managed here — Terraform owns the slot, `scripts/
# add-secret-versions.sh` adds versions, so no secret material ever reaches the state file.
#
# Two of these slots already exist in the project from the veilleur-app PoC. Import them before
# the first apply rather than letting Terraform try to create them again — see RUNBOOK.md.
resource "google_artifact_registry_repository" "minion" {
  location      = var.region
  repository_id = "minion"
  format        = "DOCKER"
  description   = "Le Veilleur Minion container images"

  depends_on = [google_project_service.enabled]
}

resource "google_secret_manager_secret" "runtime" {
  for_each = toset(local.minion_runtime_secrets)

  secret_id = each.key

  replication {
    auto {}
  }

  depends_on = [google_project_service.enabled]
}
