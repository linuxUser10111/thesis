provider "google" {
    reqion                      = "eu-west3"
    zone                        = "eu-west3-b"
    access_token                = data.google_service_account_access_token.default.access_token
    request_timeout 	        = "60s"
}

provider "google-beta" {
    reqion                      = "eu-west3"
    zone                        = "eu-west3-b"
    access_token                = data.google_service_account_access_token.default.access_token
    request_timeout 	        = "60s"
}

provider "google" {
 alias = "impersonation"
 scopes = [
   "https://www.googleapis.com/auth/cloud-platform",
   "https://www.googleapis.com/auth/userinfo.email",
 ]
}

data "google_service_account_access_token" "default" {
 provider               	= google.impersonation
 target_service_account 	= "${var.service_account_app}@${var.project}.iam.gserviceaccount.com"
 scopes                 	= ["userinfo-email", "cloud-platform"]
 lifetime               	= "1200s"
}