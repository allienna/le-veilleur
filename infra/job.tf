# The Cloud Run Job (the Minion). Terraform owns the Job *shape*; the image tag is bumped
# out-of-band by scripts/deploy-minion.sh (`gcloud run jobs update --image`), so `image` and the
# client-metadata fields sit under ignore_changes. timeout=1200s is the 20-minute hard cap;
# max_retries=0 — a failed run is not auto-retried, replay is a deliberate action.
#
# memory=1Gi is load-bearing, not a round number. At the Cloud Run default of 512Mi a 44-source
# run was OOM-killed (signal 9) about five minutes into `generate`: the process is killed outright
# by the OS, so no application code runs to record a terminal status and the run leaves no trace
# of why it died. 512Mi is simply tight for Python + Node + the `claude` subprocess carrying up to
# the 500k-input-token context cap. 1Gi gives real headroom and, for a few-minutes-a-day job,
# does not move the monthly bill.
resource "google_cloud_run_v2_job" "minion" {
  name     = "minion"
  location = var.region

  template {
    template {
      service_account = google_service_account.minion.email
      max_retries     = 0
      timeout         = "1200s"

      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/minion/minion:${var.image_tag}"
        args  = ["run"]

        # Unbuffered stdout: each JSON log line reaches Cloud Logging immediately rather than
        # sitting in Python's block buffer, which matters for diagnosing a run that dies
        # unexpectedly (an uncaught exception, not the OOM-kill case — nothing survives SIGKILL
        # either way).
        env {
          name  = "PYTHONUNBUFFERED"
          value = "1"
        }

        resources {
          limits = {
            cpu    = "1"
            memory = "1Gi"
          }
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].template[0].containers[0].image,
      client,
      client_version,
    ]
  }

  depends_on = [
    google_secret_manager_secret_iam_member.minion_accessor,
  ]
}

# Cloud Scheduler invokes the Job through this binding — the invoker SA holds run.invoker on the
# Job and nothing else.
resource "google_cloud_run_v2_job_iam_member" "scheduler_invoker" {
  name     = google_cloud_run_v2_job.minion.name
  location = google_cloud_run_v2_job.minion.location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler_invoker.email}"
}
