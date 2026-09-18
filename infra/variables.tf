# Infra variables. This root is self-contained — it owns every resource the pipeline needs.

# The GCP project keeps the veilleur-app id: a project id cannot be renamed, and it is invisible
# from the outside (only the GitHub repo name reaches users, via the Pages URL). Overridable, but
# changing it means re-provisioning every secret.
variable "project_id" {
  description = "GCP project hosting the pipeline."
  type        = string
  default     = "veilleur-app"
}

variable "region" {
  description = "GCP region for regional resources (Cloud Run, Scheduler, Functions, Artifact Registry)."
  type        = string
  default     = "europe-west1"
}

variable "billing_account" {
  description = "Billing account ID (XXXXXX-XXXXXX-XXXXXX) the budget kill-switch is created on. No default — supply via tfvars/CLI."
  type        = string
}

variable "budget_amount_eur" {
  description = "Monthly budget cap in EUR for the kill-switch."
  type        = number
  default     = 30
}

variable "image_tag" {
  description = "Initial Cloud Run Job image tag. The deploy script bumps the live image out-of-band (image is under ignore_changes)."
  type        = string
  default     = "latest"
}

variable "podcast_enabled" {
  description = "Ordinary, reversible operational toggle for the podcast step — static PODCAST_ENABLED env var on the Job (not a security break-glass)."
  type        = bool
  default     = true
}

variable "podcast_budget_amount_eur" {
  description = "Monthly notify-only budget cap in EUR for the podcast feature, separate from and in addition to the kill-switch's budget_amount_eur."
  type        = number
  default     = 8
}
