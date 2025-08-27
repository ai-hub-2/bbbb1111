variable "region" {
	type        = string
	description = "AWS region (must support SES inbound e.g., us-east-1)"
	default     = "us-east-1"
}

variable "inbound_bucket" {
	type        = string
	description = "S3 bucket name for inbound raw emails"
}

variable "lambda_zip_path" {
	type        = string
	description = "Path to packaged Lambda ZIP"
	default     = "../../services/ses_inbound/function.zip"
}