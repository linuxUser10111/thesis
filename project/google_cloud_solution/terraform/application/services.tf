variable "gcp_service_list" {
  type        = list(string)
  description = "services necessary for the project"
  default     = [
     "run.googleapis.com", 
     "containerregistry.googleapis.com"
    ]
}

resource "google_project_service" "gcp_services" {
  for_each = toset(var.gcp_service_list)
  project  = var.project
  service  = each.key
}

