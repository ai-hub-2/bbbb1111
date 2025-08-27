# Production Guide: Email Inbound + Google OAuth + DNS/SSL Service

This repository provides production-ready components for:
- Inbound email processing (Mailgun webhook + AWS SES → S3 → Lambda)
- Google OAuth sign-in (replace any notion of Gmail account automation)
- DNS/WHOIS/SSL inspection microservice with Prometheus metrics

Important constraints
- Disposable/temp-mail domains are routinely blocked by major providers (incl. Google). Do not rely on temp mail for third-party verifications.
- Automating Gmail account creation violates TOS and is unreliable; use Google Identity Services instead.

## Architecture Overview
- Email Domain (your TLD) → MX to provider
  - Option A: Mailgun Routes → HTTPS webhook (/webhook/mailgun)
  - Option B: AWS SES Inbound → S3 → Lambda parser
- Processing: Extract OTPs/links → enqueue → persist
- Auth: Google Identity Services (OAuth) for login
- Observability: logs, metrics, alerts

## Deploy Steps
1) Domain and Email
- Buy/verify domain. Configure MX to Mailgun or SES
- SPF/DKIM/DMARC for sending reputation
- Catch-all or aliasing for test/QA flows

2) Mailgun Inbound Webhook
- Deploy /services/inbound_mailgun (Flask or container)
- Protect with HTTPS; set MAILGUN_SIGNING_KEY
- In Mailgun: Route → forward to https://api.example.com/webhook/mailgun

3) AWS SES Inbound (Alternative)
- Verify domain in SES (supported region)
- Receipt Rule: Store to S3 (bucket inbox-raw)
- Lambda trigger on S3 PUT → /services/ses_inbound/lambda_function.py

4) Google OAuth
- Follow /docs/google_oauth/SETUP.md
- Use client-side credential and server-side verification

5) DNS/SSL Service
- Use dnspython with timeouts/retries
- SSL checks via Python ssl with SNI
- WHOIS via paid API if reliability needed
- Add caching (Redis) and rate-limiting

## Security
- HTTPS everywhere; verify webhook signatures
- Secret management (AWS Secrets Manager / GCP Secret Manager)
- Least-privilege IAM roles for Lambda/S3
- Input validation, MIME parsing limits
- PII minimization and retention policies

## Reliability
- Retries with backoff; DLQ for failed events (SQS)
- Idempotency keys for webhooks
- Structured logging, metrics, tracing
- Health checks and readiness probes

## Performance
- Async ingestion (queue) and background processing
- TTL-aware caching for DNS/WHOIS
- Bounded concurrency to protect dependencies

## Compliance
- GDPR/CCPA for email content
- CAN-SPAM when sending
- Data residency depending on region

## Operations
- Dockerize services; use CI/CD
- Infra as Code: Terraform or AWS CDK
- Monitoring: certificate expiry, MX failures, webhook errors

## Limitations and Non-Goals
- Do not attempt to make temp mail "accepted by Google"; design with your own controlled domain instead.
- Do not automate Gmail account creation; use OAuth.

## Next Steps
- Wire parsed OTPs to your auth/test flows
- Add persistence (PostgreSQL) and API endpoints to fetch latest OTP by session
- Add unit/integration tests and synthetic monitors