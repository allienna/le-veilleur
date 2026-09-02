# Every API the pipeline needs. This root is self-contained: the veilleur-app PoC split the
# singletons (secrets, Artifact Registry, APIs) into a separate "spike" state, and that split is
# consolidated here. `disable_on_destroy = false` avoids the re-enablement propagation lag on
# re-apply.
#
# Deliberately absent: aiplatform (image generation goes through the Gemini API key, not Vertex
# IAM) and firestore (there is no datastore any more).
locals {
  apis = [
    "run.googleapis.com",              # the Cloud Run Job
    "artifactregistry.googleapis.com", # the Minion image
    "secretmanager.googleapis.com",    # the four runtime secrets
    "gmail.googleapis.com",            # ingestion
    "cloudscheduler.googleapis.com",   # the daily trigger
    "pubsub.googleapis.com",           # budget event transport
    "cloudfunctions.googleapis.com",   # the kill-switch function (2nd gen)
    "cloudbuild.googleapis.com",       # 2nd-gen function source build
    "eventarc.googleapis.com",         # 2nd-gen function Pub/Sub trigger
    "billingbudgets.googleapis.com",   # the budget itself
  ]
}

resource "google_project_service" "enabled" {
  for_each = toset(local.apis)

  service                    = each.key
  disable_on_destroy         = false
  disable_dependent_services = false
}
