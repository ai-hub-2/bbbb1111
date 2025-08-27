# Deploy to Google Cloud Run

This guide deploys the Mailgun webhook and DNS/SSL microservice to Cloud Run using Artifact Registry.

## Prerequisites
- GCP project and billing enabled
- Service Account JSON with roles: Artifact Registry Writer, Cloud Run Admin, Service Account User
- gcloud CLI locally (optional)

## GitHub Secrets
- GCP_PROJECT_ID: your project id
- GCP_REGION: e.g., us-central1
- GCP_SA_KEY: JSON key of the CI service account
- MAILGUN_SIGNING_KEY: your Mailgun webhook signing key

## CI/CD (recommended)
- Workflow: `.github/workflows/cloudrun-deploy.yml`
- Triggers on push to main (service changes) or manual dispatch

## Manual Commands
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# Configure docker auth
gcloud auth login
gcloud config set project $PROJECT_ID
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build & push images
IMAGE_MAILGUN=$REGION-docker.pkg.dev/$PROJECT_ID/apps/inbound-mailgun:latest
docker build -t $IMAGE_MAILGUN services/inbound_mailgun
docker push $IMAGE_MAILGUN

IMAGE_DNSSSL=$REGION-docker.pkg.dev/$PROJECT_ID/apps/dns-ssl-service:latest
docker build -t $IMAGE_DNSSSL services/dns_ssl_service
docker push $IMAGE_DNSSSL

# Deploy services
gcloud run deploy inbound-mailgun \
  --image $IMAGE_MAILGUN --region $REGION --platform managed \
  --allow-unauthenticated --port 8080 \
  --set-env-vars MAILGUN_SIGNING_KEY=your_signing_key

gcloud run deploy dns-ssl-service \
  --image $IMAGE_DNSSSL --region $REGION --platform managed \
  --allow-unauthenticated --port 9090

# Get URLs
gcloud run services describe inbound-mailgun --region $REGION --format 'value(status.url)'
gcloud run services describe dns-ssl-service --region $REGION --format 'value(status.url)'
```

## Mailgun Route
- Forward to: `https://<inbound-mailgun-url>/webhook/mailgun`
- Ensure signature verification passes