import requests
import base64
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

auth_code = input("Paste your auth code here: ").strip()

# Encode client credentials
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI
}

response = requests.post("https://api.schwabapi.com/v1/oauth/token", headers=headers, data=data)

if response.status_code == 200:
    tokens = response.json()
    print("✅ Access Token:", tokens["access_token"])
    print("♻️ Refresh Token:", tokens["refresh_token"])
    print("⏳ Expires in:", tokens["expires_in"], "seconds")
else:
    print("❌ Token exchange failed:", response.status_code, response.text)