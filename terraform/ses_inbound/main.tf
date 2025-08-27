terraform {
	required_version = ">= 1.5.0"
	required_providers {
		aws = {
			source  = "hashicorp/aws"
			version = ">= 5.0"
		}
	}
}

provider "aws" {
	region = var.region
}

resource "aws_s3_bucket" "inbound" {
	bucket = var.inbound_bucket
	force_destroy = true
}

resource "aws_iam_role" "lambda_role" {
	name               = "ses-inbound-lambda-role"
	assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_assume" {
	statement {
		effect  = "Allow"
		principals { type = "Service", identifiers = ["lambda.amazonaws.com"] }
		actions = ["sts:AssumeRole"]
	}
}

resource "aws_iam_role_policy_attachment" "basic_logs" {
	role       = aws_iam_role.lambda_role.name
	policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "s3_read" {
	name = "s3-read-inbound"
	role = aws_iam_role.lambda_role.id
	policy = jsonencode({
		Version = "2012-10-17",
		Statement = [{
			Effect = "Allow",
			Action = ["s3:GetObject"],
			Resource = ["${aws_s3_bucket.inbound.arn}/*"]
		}]
	})
}

resource "aws_lambda_function" "parser" {
	function_name = "ses-inbound-parser"
	runtime       = "python3.11"
	role          = aws_iam_role.lambda_role.arn
	handler       = "lambda_function.handler"

	filename         = var.lambda_zip_path
	source_code_hash = filebase64sha256(var.lambda_zip_path)
	environment {
		variables = {
			LOG_LEVEL = "INFO"
		}
	}
}

# Note: Create S3 PUT notification to Lambda (via aws_s3_bucket_notification) after bucket is created
resource "aws_s3_bucket_notification" "inbound_events" {
	bucket = aws_s3_bucket.inbound.id

	lambda_function {
		lambda_function_arn = aws_lambda_function.parser.arn
		events              = ["s3:ObjectCreated:Put"]
	}

	depends_on = [aws_lambda_permission.allow_s3]
}

resource "aws_lambda_permission" "allow_s3" {
	statement_id  = "AllowS3Invoke"
	action        = "lambda:InvokeFunction"
	function_name = aws_lambda_function.parser.function_name
	principal     = "s3.amazonaws.com"
	source_arn    = aws_s3_bucket.inbound.arn
}