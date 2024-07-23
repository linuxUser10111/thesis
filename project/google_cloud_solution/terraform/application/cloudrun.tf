resource "google_cloud_run_service" "ml_project" {
  name     = "ml-project-cloudrun"
  location = "eu-west3"

  template {
    spec {
      containers {
        image = "europe-west3-docker.pkg.dev/${var.project}/ml-docker-registry/ml_docker:${var.image_tag}"
        resources {
            limits = {
                cpu    = "1"
                memory = "2Gi"
            }
        }
      }
      service_account_name = "${var.service_account_app}@${var.project}.iam.gserviceaccount.com"
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.gcp_services, google_service_account.app_service_account,
    google_service_account_iam_member.iam_binding_instanceuser_service_account,
  ]
}

resource "google_cloud_run_service_iam_member" "allUsers" {
    project     = "${var.project}"
    service     = google_cloud_run_service.ml_project.name
    location    = google_cloud_run_service.ml_project.location
    role        = "roles/run.invoker"
    member      = "allUsers"
    depends_on  = [google_cloud_run_service.ml_project]
}
