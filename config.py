import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("S_CLIENT_ID")
REDIRECT_URI = os.getenv("S_REDIRECT_URI")
REFRESH_TOKEN = os.getenv("S_REFRESH_TOKEN")