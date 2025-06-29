import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")