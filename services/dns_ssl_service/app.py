#!/usr/bin/env python3
import os
import socket
import ssl
from flask import Flask, request, jsonify
import dns.resolver
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQS = Counter('dns_ssl_requests_total', 'Total requests', ['endpoint'])
ERRS = Counter('dns_ssl_errors_total', 'Total errors', ['endpoint'])
LAT  = Histogram('dns_ssl_request_seconds', 'Request latency', ['endpoint'])

resolver = dns.resolver.Resolver()
resolver.lifetime = 3.0
resolver.timeout = 3.0

@app.get('/metrics')
def metrics():
	return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.get('/dns')
@LAT.labels('dns').time()
def dns_lookup():
	REQS.labels('dns').inc()
	domain = request.args.get('domain', '')
	record = request.args.get('type', 'A').upper()
	if not domain:
		ERRS.labels('dns').inc()
		return jsonify({'error': 'domain required'}), 400
	try:
		answers = resolver.resolve(domain, record)
		values = [str(a) for a in answers]
		return jsonify({'domain': domain, 'type': record, 'values': values})
	except Exception as e:
		ERRS.labels('dns').inc()
		return jsonify({'error': str(e)}), 502

@app.get('/ssl')
@LAT.labels('ssl').time()
def ssl_info():
	REQS.labels('ssl').inc()
	host = request.args.get('host', '')
	port = int(request.args.get('port', '443'))
	if not host:
		ERRS.labels('ssl').inc()
		return jsonify({'error': 'host required'}), 400
	try:
		context = ssl.create_default_context()
		with socket.create_connection((host, port), timeout=5) as sock:
			with context.wrap_socket(sock, server_hostname=host) as ssock:
				cert = ssock.getpeercert()
				return jsonify({
					'host': host,
					'issuer': dict(x[0] for x in cert.get('issuer', [])),
					'subject': dict(x[0] for x in cert.get('subject', [])),
					'notBefore': cert.get('notBefore'),
					'notAfter': cert.get('notAfter'),
					'san': cert.get('subjectAltName', []),
				})
	except Exception as e:
		ERRS.labels('ssl').inc()
		return jsonify({'error': str(e)}), 502

if __name__ == '__main__':
	port = int(os.getenv('PORT', '9090'))
	app.run(host='0.0.0.0', port=port)