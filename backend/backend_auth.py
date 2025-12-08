import os
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlmodel import Field, SQLModel, Session, select
import requests

CLIENT_ID = "1076159486506-oib7sr7s0ja826pgbt6b1bqfeelmrkt7.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8000/api/v1/login"
TOKEN_URL = "https://oauth2.googleapis.com/token"
PROVIDER_URL = "https://accounts.google.com/o/oauth2/v2/auth"
PROVIDER_URI = f"?scope=openid%20profile%20email&response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}"

security = HTTPBearer()

try:
    CLIENT_SECRET = os.getenv("S3_LOADER_CLIENT_SECRET")
except Exception as e:
    print(f"error: {e}")


def oauth_redirect():
    return RedirectResponse(url=f"{PROVIDER_URL}{PROVIDER_URI}")


def token_resolve(code):
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
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response

def validate_user_token(user_token: HTTPAuthorizationCredentials = Depends(security)):
    response = auth_user_data(user_token.credentials)
    if (response.status_code != 200):
        raise HTTPException(403, detail="Token expired login again")
    return response.json()


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str =Field(index=True, unique=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)



class LoginHandler():
    def __init__(self, token, engine):
        self.token = token
        self.engine = engine

    
    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def get_user_info(self):
        return auth_user_data(self.token)

    def create_user(self):
        with Session(self.engine) as session:
            try:
                user_dict = {}
                user_data = self.get_user_info().json()
                user_dict["name"] = user_data["name"]
                user_dict["email"] = user_data["email"]
                user_exists = session.exec(select(User).where(User.email == user_dict["email"]))
                if user_exists:
                    return True
                valid_user_model = User.model_validate(user_dict)
                session.add(valid_user_model)
                session.commit()
                session.refresh(valid_user_model)
                print(f"User {user_dict["email"]} created.")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
