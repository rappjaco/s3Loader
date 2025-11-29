import requests
import webbrowser, os
from pathlib import Path

BACKEND_HOSTNAME = "http://localhost:8000/"
LOGIN_URI = "api/v1/login"
USER_TOKEN_URI = "api/v1/user_token"
APP_NAME="S3Loader"
CRED_PATH = Path(f"{os.getenv("HOME")}/.config/{APP_NAME}/token")

def read_user_token():
    with open(CRED_PATH, "r") as file:
        user_token = file.read()
    return user_token

def check_local_credentials():
    if CRED_PATH.exists():
        return True
    return False

def create_local_credentials():
    try:
        webbrowser.open(f"{BACKEND_HOSTNAME}{LOGIN_URI}")
        user_token_input = input("Paste Login Access Token: ")
        CRED_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CRED_PATH, "w") as file:
            file.write(user_token_input)
        return True
    except:
        return False

def login_auth_flow():
    try: 
        user_token = read_user_token()
        response = requests.post(
            f"{BACKEND_HOSTNAME}{USER_TOKEN_URI}",
            data={"user_access_token": user_token}
        )
        if response.json() == 401:
            try:
                print("Updating Creds")
                create_local_credentials()
                login_auth_flow()
            except Exception as e:
                print(f"error: {e}")

        user_info = response.json()
        print(f"Hello, {user_info.get("name")}")
    except Exception as e:
        print(f"login failed: {e}")


def user_login_init():
    if check_local_credentials():
        login_auth_flow()
    else:
        try:
            create_local_credentials()
        except Exception as e:
            print(f"Creating local Credentials Failed: {e}")
        try:
            login_auth_flow()
        except Exception as e:
            print(f"{e}")
