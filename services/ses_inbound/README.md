# AWS SES Inbound Lambda

Parses raw inbound emails saved to S3 by an SES Receipt Rule, extracting OTP codes and links.

## Architecture
- SES Domain: Verify domain and set MX to SES
- Receipt Rule: "Store in S3" action → Bucket inbox-raw
- Lambda Trigger: S3 PUT (inbox-raw) → lambda_function.handler
- Optional: Forward parsed payload to SQS/DB/Webhook

## Deploy
```bash
# Package
zip function.zip lambda_function.py

# Create IAM role with permissions: AWSLambdaBasicExecutionRole + S3 read on bucket
# Create function
aws lambda create-function \
  --function-name ses-inbound-parser \
  --runtime python3.11 \
  --role arn:aws:iam::<ACCOUNT>:role/ses-inbound-role \
  --handler lambda_function.handler \
  --zip-file fileb://function.zip

# Add S3 trigger in console or via CLI
```

## Permissions
- S3:GetObject on the inbound bucket/prefix
- CloudWatch Logs for Lambda

## Notes
- Configure SES in a region that supports inbound (e.g., us-east-1)
- Handle large emails by enabling S3 payloads
- Add retries, DLQ (SQS), and idempotency in production