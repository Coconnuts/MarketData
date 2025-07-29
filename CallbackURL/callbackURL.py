import sys
from flask import Flask, request, redirect, session, abort
import os
import secrets
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CLIENT_ID  # Ensure you have a config.py with CLIENT_ID defined

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Required for secure sessions

# Schwab OAuth2 config
REDIRECT_URI = "https://127.0.0.1:8443/receive"

# Route to start the OAuth2 flow
@app.route('/start', methods=['GET'])
def start():
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    auth_url = (
        "https://api.schwabapi.com/v1/oauth/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
    )

    return redirect(auth_url)

# OAuth2 callback route to receive the authorization code
@app.route('/receive', methods=['GET'])
def receive():
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = session.get('oauth_state')

    if not stored_state or state != stored_state:
        print("State mismatch or missing")
        return "Invalid state. Request may not be legitimate.", 400

    if code:
        print(f"Authorization code received: {code}")
        return f"""
            <h2>Authorization Code Received</h2>
            <p><strong>Code:</strong> {code}</p>
            <p><strong>State:</strong> {state}</p>
            <p>You can now close this tab and paste the code into your app.</p>
        """, 200
    else:
        print("No code in request:", request.args)
        return "No authorization code received. Please try again.", 400

# Run the Flask app with HTTPS
if __name__ == '__main__':
    cert_path = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key_path = os.path.join(os.path.dirname(__file__), 'key.pem')
    app.run(host='127.0.0.1', port=8443, ssl_context=(cert_path, key_path))