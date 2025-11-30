import requests
from client_auth import read_user_token


BACKEND_HOSTNAME = "http://localhost:8000/"
S3_URI = "api/v1/list"

def list_files():
    user_token = read_user_token()
    response = requests.get(f"{BACKEND_HOSTNAME}{S3_URI}",
                            headers={"Authorization": f"Bearer {user_token}"})
    
    for object in response.json():
        print(object["Key"])