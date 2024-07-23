variable "project" {
  type        = string
  default     = "bachlelor-ml"
  description = "project name for environment"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to use in the environment"
}

variable "service_account_app" {
  type        = string
  default     = "service-account"
  description = "service account to use for the app"
}


