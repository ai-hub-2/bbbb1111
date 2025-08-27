#!/usr/bin/env python3
import os
import hmac
import hashlib
from flask import Flask, request, jsonify, abort
from email.parser import BytesParser
from email.policy import default
import re

app = Flask(__name__)

MAILGUN_SIGNING_KEY = os.getenv('MAILGUN_SIGNING_KEY', '')
OTP_REGEX = re.compile(r'\b(\d{4,8})\b')
SERVICE_ENABLED = os.getenv('SERVICE_ENABLED', 'true').lower() == 'true'


def verify_mailgun_signature(timestamp: str, token: str, signature: str) -> bool:
	if not MAILGUN_SIGNING_KEY:
		return False
	digest = hmac.new(MAILGUN_SIGNING_KEY.encode(), msg=f"{timestamp}{token}".encode(), digestmod=hashlib.sha256).hexdigest()
	return hmac.compare_digest(digest, signature)


@app.post('/webhook/mailgun')
def mailgun_inbound():
	# Kill-switch: disable real operation if SERVICE_ENABLED=false
	if not SERVICE_ENABLED:
		return jsonify({'error': 'service disabled'}), 503
	# Signature verification
	signature = request.form.get('signature', '')
	timestamp = request.form.get('timestamp', '')
	token = request.form.get('token', '')
	if not verify_mailgun_signature(timestamp, token, signature):
		abort(401)

	# Extract basic fields
	mail_from = request.form.get('from', '')
	recipient = request.form.get('recipient', '')
	subject = request.form.get('subject', '')
	stripped_text = request.form.get('stripped-text', '')
	stripped_signature = request.form.get('stripped-signature', '')
	html = request.form.get('stripped-html', '')

	# Attempt to parse raw MIME if provided
	otp_codes = []
	links = []
	if 'body-mime' in request.files:
		raw = request.files['body-mime'].read()
		msg = BytesParser(policy=default).parsebytes(raw)
		payload = msg.get_body(preferencelist=('plain', 'html'))
		if payload:
			content = payload.get_content()
			otp_codes += OTP_REGEX.findall(content)
			links += re.findall(r'https?://\S+', content)

	# Fallback to stripped text/html
	otp_codes += OTP_REGEX.findall(stripped_text or '')
	otp_codes += OTP_REGEX.findall(stripped_signature or '')
	links += re.findall(r'https?://\S+', (stripped_text or ''))
	links += re.findall(r'https?://\S+', (html or ''))

	# Deduplicate
	otp_codes = list(dict.fromkeys(otp_codes))
	links = list(dict.fromkeys(links))

	result = {
		'from': mail_from,
		'recipient': recipient,
		'subject': subject,
		'otp_codes': otp_codes,
		'links': links,
	}

	# TODO: push to queue/DB. For now return JSON.
	return jsonify(result), 200


if __name__ == '__main__':
	port = int(os.getenv('PORT', '8080'))
	app.run(host='0.0.0.0', port=port)