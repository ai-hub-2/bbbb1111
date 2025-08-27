# Mailgun Inbound Webhook Service

Production-ready Flask service that verifies Mailgun signatures, parses inbound emails (OTP codes and links), and returns JSON. Integrate by forwarding Mailgun Routes to this endpoint.

## Configure Mailgun
- Create a Route: Match Recipient (e.g., .*@inbound.yourdomain.com)
- Action: Forward to https://your-api.example.com/webhook/mailgun
- Enable signing and note your signing key

## Environment
- MAILGUN_SIGNING_KEY: Your Mailgun signing key

## Run locally
```bash
pip install -r requirements.txt
export MAILGUN_SIGNING_KEY=... && python app.py
```

## Production
- Run behind HTTPS (e.g., Nginx/ALB)
- Use health checks, logs, metrics
- Push parsed payload to your queue/DB