# Podcast feature (two-speaker script via Claude + Cloud Text-to-Speech): a dedicated,
# minimally-scoped SA — never the Minion's own runtime SA — plus a bucket for the daily audio
# file. minion-sa impersonates this SA at runtime rather than holding a stored key, so there is
# no new secret to provision.
#
# Originally built against NotebookLM Enterprise; abandoned after a live 400 traced to a
# license/subscription-tier requirement that only exists inside a Cloud Identity/Google
# Workspace organization (docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/
# set-up-notebooklm) — not available to a personal GCP project. Cloud Text-to-Speech is GA, has
# no such organizational requirement, and needs no dedicated custom role: any principal with the
# API enabled and basic project access can call it, billed against whichever project's quota it
# authenticates under (`roles/serviceusage.serviceUsageConsumer` below is what makes podcast-sa
# that principal, rather than relying on it inheriting anything from minion-sa).

# ─── Podcast SA: Cloud TTS + the audio bucket, nothing else ──────────────────────────────
resource "google_service_account" "podcast" {
  account_id   = "podcast-sa"
  display_name = "Le Veilleur podcast (script + Cloud TTS) SA"
}

resource "google_project_iam_member" "podcast_tts_consumer" {
  project = var.project_id
  role    = "roles/serviceusage.serviceUsageConsumer"
  member  = "serviceAccount:${google_service_account.podcast.email}"
}

# minion-sa (the Job's actual runtime identity) mints short-lived tokens as podcast-sa via
# google.auth.impersonated_credentials — no key material is ever stored for this SA.
resource "google_service_account_iam_member" "minion_impersonates_podcast" {
  service_account_id = google_service_account.podcast.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${google_service_account.minion.email}"
}

# ─── Audio bucket: 30-day lifecycle, matching the site/RSS retention window ──────────────
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
