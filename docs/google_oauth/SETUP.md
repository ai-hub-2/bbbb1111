# Google OAuth (Google Identity Services) Setup

This guide configures a production-ready Google Sign-In flow instead of creating Gmail accounts.

## 1) Create OAuth Client
- Go to Google Cloud Console → APIs & Services → Credentials
- Create OAuth client ID (Web application)
- Authorized JavaScript origins: https://yourapp.example.com
- Authorized redirect URIs: https://yourapp.example.com/oauth/google/callback
- Download client credentials (client_id)

## 2) Frontend (Web)
Use Google Identity Services JS to trigger sign-in and get credential on the client:
```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
<div id="g_id_onload"
     data-client_id="YOUR_CLIENT_ID"
     data-login_uri="https://yourapp.example.com/oauth/google/callback"
     data-auto_prompt="false">
</div>
<div class="g_id_signin" data-type="standard"></div>
```

## 3) Backend (Server)
Validate the credential JWT and create a session.
Example (Python Flask):
```python
from flask import Flask, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
GOOGLE_CLIENT_ID = "YOUR_CLIENT_ID"

@app.post('/oauth/google/callback')
def google_callback():
	credential = request.form.get('credential') or request.json.get('credential')
	token_info = id_token.verify_oauth2_token(credential, requests.Request(), GOOGLE_CLIENT_ID)
	# token_info contains sub (user id), email (if scope), name, picture
	# TODO: upsert user, create session
	return jsonify({'user_id': token_info['sub'], 'email': token_info.get('email')})
```

## 4) Scopes and Consent
- Default sign-in requires no extra scopes
- For Gmail/Calendar APIs, request specific scopes and pass Google verification

## 5) Security
- Enforce HTTPS
- Rotate client secrets
- CSRF protection on the callback if you use state param
- Store minimal PII; apply retention policies

## 6) Testing
- Add test users in OAuth consent screen while in Testing mode
- Move to Production after verification when requesting sensitive scopes