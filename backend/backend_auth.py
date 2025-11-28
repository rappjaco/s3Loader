import os
from fastapi.responses import RedirectResponse
import requests

CLIENT_ID = "1076159486506-oib7sr7s0ja826pgbt6b1bqfeelmrkt7.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8000/api/v1/login"
TOKEN_URL = "https://oauth2.googleapis.com/token"
PROVIDER_URL = "https://accounts.google.com/o/oauth2/v2/auth"
PROVIDER_URI = f"?scope=profile&response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}"


try:
    CLIENT_SECRET = os.getenv("S3_LOADER_CLIENT_SECRET")
except Exception as e:
    print(f"error: {e}")


def github_oauth_redirect():
    print(PROVIDER_URL + PROVIDER_URI)
    return RedirectResponse(url=f"{PROVIDER_URL}{PROVIDER_URI}")


def github_token_resolve(code):
    response = requests.post(
        f"{TOKEN_URL}",
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )
    return response.json()


def auth_user_data(token):
    response = requests.get(
        "https://www.googleapis.com/auth/userinfo.profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response
