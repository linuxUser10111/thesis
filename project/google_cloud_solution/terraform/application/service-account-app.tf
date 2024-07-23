resource "google_service_account" "app_service_account" {
  project       = var.project
  account_id    = var.service_account_app
  display_name  = "Service account for the app"
}

### all permissions for the service account

resource "google_project_iam_member" "app_cloudrun_sa_role_monitoring" {
    project = var.project
    role    = "roles/monitoring.metricWriter"
    members  = ["serviceAccount:${google_service_account.app_service_account.email}"]
}

resource "google_project_iam_member" "iam_binding_instanceuser_service_account" {
    project = var.project
    role    = "roles/cloudsql.instanceuser"
    members  = ["serviceAccount:${google_service_account.app_service_account.email}"]
}

