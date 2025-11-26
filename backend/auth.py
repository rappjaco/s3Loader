import os
from fastapi.responses import RedirectResponse
from authlib.integrations.httpx_client import AsyncOAuth2Client
import requests

GITHUB_CLIENT_ID = "Ov23liApBxqTascxXx7d"
REDIRECT_URI= "http://localhost:8000/api/v1/login"
GITHUB_URL = "https://github.com/"

try:
    GITHUB_CLIENT_SECRET = os.getenv("S3_LOADER_CLIENT_SECRET")
except Exception as e:
    print(f"error: {e}")


def github_oauth_redirect():
    return RedirectResponse(url=f"https://github.com/login/oauth/authorize?client_id=Ov23liApBxqTascxXx7d&redirect_uri={REDIRECT_URI}")

def github_token_resolve(code):
    response = requests.post(
        f"{GITHUB_URL}/login/oauth/access_token",
        headers={'Accept': 'application/json'},
        data= {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
        )
    return response.json()








