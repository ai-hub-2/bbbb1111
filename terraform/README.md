# Terraform for SES Inbound (S3 + Lambda)

This Terraform module provisions:
- S3 bucket for raw inbound emails
- Lambda function (you package and provide ZIP path)
- IAM roles/policies
- S3 → Lambda notifications on object create

Notes:
- SES Receipt Rules are region-scoped; Terraforming SES receipt rules is possible but requires verified domain and MX already configured. Start by verifying your domain and pointing MX to SES in the console, then optionally add Terraform for rules.

## Usage
```bash
cd terraform/ses_inbound
terraform init
terraform apply -var "inbound_bucket=your-inbound-bucket"
```

Ensure you built the Lambda zip at path set in variable `lambda_zip_path`.

## Next
- Configure SES Receipt Rule: "Store in S3" to the bucket above
- Test by sending email to your inbound domain
- Observe Lambda logs in CloudWatch