# Podcast feature (NotebookLM Enterprise): a dedicated, minimally-scoped SA — never the Minion's
# own runtime SA — plus a bucket for the daily audio file. minion-sa impersonates this SA at
# runtime rather than holding a stored key, so there is no new secret to provision.

# ─── Podcast SA: NotebookLM Enterprise + the audio bucket, nothing else ──────────────────
resource "google_service_account" "podcast" {
  account_id   = "podcast-sa"
  display_name = "Le Veilleur podcast (NotebookLM Enterprise) SA"
}

# "Cloud NotebookLM User" — confirmed against docs.cloud.google.com/iam/docs/roles-permissions
# /discoveryengine: at project scope it grants only notebooks.create/list (+ accounts.create,
# locations.completeExternalIdentities, resourcemanager.projects.get/list) — NOT
# audioOverviews.* or sources.*, which live only in "Cloud NotebookLM Admin"
# (roles/discoveryengine.notebookLmOwner, project-wide) or the per-notebook Owner/Editor roles
# (roles/discoveryengine.notebook{Owner,Editor}, resource-scoped, can't be bound before a
# notebook exists). Starting with the least-privileged option on the working assumption — common
# elsewhere in this product family, unconfirmed here — that creating a notebook makes the creator
# its resource-level Owner automatically. If a real run 403s on sources.batchCreate or
# audioOverviews.create, switch this to notebookLmOwner.
resource "google_project_iam_member" "podcast_notebooklm_user" {
  project = var.project_id
  role    = "roles/discoveryengine.notebookLmUser"
  member  = "serviceAccount:${google_service_account.podcast.email}"
}

# minion-sa (the Job's actual runtime identity) mints short-lived tokens as podcast-sa via
# google.auth.impersonated_credentials — no key material is ever stored for this SA.
resource "google_service_account_iam_member" "minion_impersonates_podcast" {
  service_account_id = google_service_account.podcast.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${google_service_account.minion.email}"
}

# ─── Audio bucket: 30-day lifecycle, aligned with the NotebookLM notebook purge window ────
resource "google_storage_bucket" "podcast_audio" {
  name                        = "${var.project_id}-podcast-audio"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  depends_on = [google_project_service.enabled]
}

resource "google_storage_bucket_iam_member" "podcast_sa_object_admin" {
  bucket = google_storage_bucket.podcast_audio.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.podcast.email}"
}

# TODO(verify before apply): confirm that a plain public GCS object (this binding) is sufficient
# for podcast-app RSS enclosure fetches (unauthenticated GET at storage.googleapis.com/...), or
# whether a CDN/signed-URL layer is actually required. The rest of the site is already public and
# unauthenticated on GitHub Pages, so this should be consistent — verify with a real fetch once
# the bucket exists (e.g. `curl -I` for correct Content-Type/Accept-Ranges headers).
resource "google_storage_bucket_iam_member" "podcast_audio_public_read" {
  bucket = google_storage_bucket.podcast_audio.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}
