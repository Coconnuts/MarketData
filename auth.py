import requests
from config import CLIENT_ID, REDIRECT_URI, REFRESH_TOKEN
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
# auth.py - A module for handling OAuth authentication with Schwab API
def refresh_access_token():
    if not all([CLIENT_ID, REDIRECT_URI, REFRESH_TOKEN]):
        raise ValueError("Missing one or more required environment variables.")

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }

    try:
        response = requests.post(TOKEN_URL, data=payload)
        response.raise_for_status()
        tokens = response.json()
        access_token = tokens.get("access_token")
        expires_in = tokens.get("expires_in")

        print(f"[auth.py] ✅ Token refreshed. Expires in {expires_in} seconds.")
        return access_token

    except requests.exceptions.RequestException as e:
        print(f"[auth.py] ❌ Failed to refresh token: {e}")
        return None

def get_authenticated_session():
    access_token = refresh_access_token()
    if not access_token:
        raise Exception("Failed to obtain access token.")

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    })
    return session