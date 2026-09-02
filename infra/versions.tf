terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.10"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region

  # Personal user ADC (not a service account) has no baked-in quota project, and
  # billingbudgets.googleapis.com refuses to answer without one. Bill quota to this project.
  billing_project       = var.project_id
  user_project_override = true
}
