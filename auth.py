import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("S_CLIENT_ID")
CLIENT_SECRET = os.getenv("S_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("S_REFRESH_TOKEN")
REDIRECT_URI = os.getenv("S_REDIRECT_URI")
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
ENV_PATH = ".env"

print("[auth.py] ✅ Loaded ENV:")
print("  CLIENT_ID:", CLIENT_ID)
print("  CLIENT_SECRET:", CLIENT_SECRET)
print("  REFRESH_TOKEN:", REFRESH_TOKEN)
print("  REDIRECT_URI:", REDIRECT_URI)


def save_tokens_to_env(access_token, refresh_token=None):
    # Read the current .env lines
    with open(ENV_PATH, "r") as f:
        lines = f.readlines()

    # Update or insert tokens
    new_lines = []
    for line in lines:
        if line.startswith("ACCESS_TOKEN="):
            new_lines.append(f"ACCESS_TOKEN={access_token}\n")
        elif line.startswith("REFRESH_TOKEN=") and refresh_token:
            new_lines.append(f"REFRESH_TOKEN={refresh_token}\n")
        else:
            new_lines.append(line)

    # If not found, append
    if not any(line.startswith("ACCESS_TOKEN=") for line in new_lines):
        new_lines.append(f"ACCESS_TOKEN={access_token}\n")
    if refresh_token and not any(line.startswith("REFRESH_TOKEN=") for line in new_lines):
        new_lines.append(f"REFRESH_TOKEN={refresh_token}\n")

    with open(ENV_PATH, "w") as f:
        f.writelines(new_lines)

def refresh_access_token():
    print("[auth.py] 🔁 Attempting token refresh...")
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        raise ValueError("Missing CLIENT_ID, CLIENT_SECRET, or REFRESH_TOKEN")

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = None
    try:
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        tokens = response.json()
        access_token = tokens["access_token"]
        new_refresh_token = tokens.get("refresh_token", REFRESH_TOKEN)
        expires_in = tokens.get("expires_in")

        save_tokens_to_env(access_token, new_refresh_token)

        print(f"[auth.py] ✅ Token refreshed. Expires in {expires_in} seconds.")
        return access_token

    except requests.exceptions.RequestException as e:
        error_text = ""
        if response is not None:
            try:
                error_text = response.text
            except Exception:
                pass
        print(f"[auth.py] ❌ Token refresh failed: {e}")
        print(f"Response: {error_text}")
        return None

def get_authenticated_session():
    access_token = refresh_access_token()
    if not access_token:
        raise Exception("Failed to refresh access token.")

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    })
    return session