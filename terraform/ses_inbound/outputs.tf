output "inbound_bucket" {
	value       = aws_s3_bucket.inbound.bucket
	description = "Inbound S3 bucket name"
}

output "lambda_arn" {
	value       = aws_lambda_function.parser.arn
	description = "Lambda function ARN"
}