resource "google_project_service" "pubsub" {
  project = var.project_id
  disable_dependent_services = false
  for_each = toset(["pubsub.googleapis.com", "run.googleapis.com", "artifactregistry.googleapis.com", "cloudbuild.googleapis.com"])
  service = each.key
}

resource "google_pubsub_topic" "default" {
  name = "default-topic"
  depends_on = [google_project_service.pubsub]
}

resource "google_pubsub_subscription" "default" {
  name  = "default-subscription"
  topic = google_pubsub_topic.default.name
  depends_on = [google_pubsub_topic.default]
}

resource "google_cloud_run_v2_service" "backend" {
  name     = "backend-service"
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
      ports {
        container_port = 8000
      }
    }
  }
  depends_on = [google_project_service.pubsub]
}
