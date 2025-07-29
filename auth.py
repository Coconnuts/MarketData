import requests
from config import CLIENT_ID, REDIRECT_URI, AUTHORIZATION_CODE, CLIENT_SECRET

# Schwab token endpoint
token_url = "https://api.schwabapi.com/v1/oauth/token"

# Your credentials and authorization code
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = REDIRECT_URI
authorization_code = AUTHORIZATION_CODE

# Form the request body
payload = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "state": "bI6pGpUTIQYnzxpPTtxG5Bdg73u7QINTdRlZJIFpsTk"  # Optional, if you used a state parameter
}

response = requests.post(token_url, data=payload)

if response.status_code == 200:
    tokens = response.json()
    print("Access token:", tokens["access_token"])
    print("Refresh token:", tokens["refresh_token"])
else:
    print("Error:", response.status_code, response.text)