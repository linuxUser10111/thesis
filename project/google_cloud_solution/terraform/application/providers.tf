provider "google" {
    reqion                      = "eu-west3"
    zone                        = "eu-west3-b"
    impersonate_service_account = "service-account@${var.project}.iam.gserviceaccount.com"
}

provider "google-beta" {
    reqion                      = "eu-west3"
    zone                        = "eu-west3-b"
    impersonate_service_account = "service-account@${var.project}.iam.gserviceaccount.com"
}