# A second, low-threshold, NOTIFY-ONLY budget for the podcast feature alone. Deliberately NOT
# attached to the killswitch Pub/Sub topic or function (killswitch.tf) — that pauses the entire
# `minion-daily` Scheduler job, which would be disruptive to the whole pipeline over a small
# podcast overrun. Omitting `all_updates_rule` means GCP falls back to emailing the billing
# account's default recipients at each threshold crossing — an early-warning tripwire, not an
# automated action.
resource "google_billing_budget" "podcast_cap" {
  billing_account = var.billing_account
  # Deliberately shaped identically to monthly_cap (killswitch.tf) while diagnosing a bare
  # "Request contains an invalid argument" 400 from the Billing Budgets API with no field-level
  # detail — same threshold count/values, no special characters in display_name. Re-add the
  # "(notify-only)" wording and a 0.5 warning threshold once this variant is confirmed to apply.
  display_name = "Veilleur podcast ${var.podcast_budget_amount_eur} EUR per month"

  budget_filter {
    projects = ["projects/${var.project_id}"]
    # NOTE: this tracks whole-project spend at a low threshold, not podcast-specific spend —
    # NotebookLM Enterprise / GCS costs are not reliably separable from the rest of the project's
    # billing via a label filter at this time. If/when Cloud Billing exposes a clean SKU or label
    # split for this feature, narrow this filter; until then this is a coarse early-warning
    # budget, documented as such in infra/RUNBOOK.md.
  }

  amount {
    specified_amount {
      currency_code = "EUR"
      units         = var.podcast_budget_amount_eur
    }
  }

  threshold_rules {
    threshold_percent = 0.8
  }
  threshold_rules {
    threshold_percent = 1.0
  }

  depends_on = [google_project_service.enabled]

  lifecycle {
    ignore_changes = [budget_filter[0].projects]
  }
}
