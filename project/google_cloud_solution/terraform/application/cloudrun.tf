resource "google_cloud_run_service" "ml_project" {
  name                       = "ml-project-cloudrun"
  project                    = var.project
  provider                   = "google-beta"
  location                   = var.region
  autogenerate_revision_name = true

  metadata {
    annotations = {
      "run.googleapis.com/ingress" = "all"
    }
  }

  template {
    spec {
      timeout_seconds= "3600"
      containers {
        image = "europe-west3-docker.pkg.dev/${var.project}/ml-docker-registry/ml_docker:${var.image_tag}"
        resources {
          limits = {
            cpu    = "2000m"
            memory = "5Gi"
          }
        }
      }
      service_account_name = "${var.service_account_app}@${var.project}.iam.gserviceaccount.com"
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"    = 0
        "autoscaling.knative.dev/maxScale"    = 3
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.gcp_services, google_service_account.app_service_account,
    # google_project_iam_member.iam_binding_instanceuser_service_account,
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
