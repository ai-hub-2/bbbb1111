import os
import json
import boto3
import re
from email import policy
from email.parser import BytesParser

s3 = boto3.client('s3')
OTP_REGEX = re.compile(r'\b(\d{4,8})\b')
LINK_REGEX = re.compile(r'https?://\S+')


def parse_email_from_s3(bucket: str, key: str):
	obj = s3.get_object(Bucket=bucket, Key=key)
	raw = obj['Body'].read()
	msg = BytesParser(policy=policy.default).parsebytes(raw)
	from_addr = msg.get('From', '')
	recipient = msg.get('To', '')
	subject = msg.get('Subject', '')

	content = ''
	if msg.is_multipart():
		for part in msg.walk():
			ctype = part.get_content_type()
			if ctype in ('text/plain', 'text/html'):
				try:
					content += part.get_content()
				except Exception:
					pass
	else:
		try:
			content = msg.get_content()
		except Exception:
			content = ''

	otps = list(dict.fromkeys(OTP_REGEX.findall(content)))
	links = list(dict.fromkeys(LINK_REGEX.findall(content)))

	return {
		'from': from_addr,
		'recipient': recipient,
		'subject': subject,
		'otp_codes': otps,
		'links': links,
	}


def handler(event, context):
	# Expecting SES receipt rule to drop raw email into S3
	records = event.get('Records', [])
	results = []
	for r in records:
		s3_info = r.get('s3', {})
		bucket = s3_info.get('bucket', {}).get('name')
		key = s3_info.get('object', {}).get('key')
		if not bucket or not key:
			continue
		parsed = parse_email_from_s3(bucket, key)
		results.append(parsed)

	# In production: push to SQS/SNS/DB; here we just return
	return {
		'statusCode': 200,
		'body': json.dumps({'results': results})
	}