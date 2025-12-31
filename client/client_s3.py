import requests
from client_auth import read_user_token


BACKEND_HOSTNAME = "http://localhost:8000/"
S3_LIST_URI = "api/v1/list"
S3_UPLOAD_URI = "api/v1/upload"


def list_files():
    
    user_token = read_user_token()
    bearer_token = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"{BACKEND_HOSTNAME}{S3_LIST_URI}",
                        headers=bearer_token)
    if response.status_code == 403:
        raise Exception("Token as expired login again")
    else:
        print("test")
        for object in response.json():
            print(object["Key"])
 

def upload_file(file_path):
    user_token = read_user_token()
    if file_path.find("/"):
        file_name_list = file_path.split("/")
        file_name = file_name_list[-1]
    else:
        file_name = file_path
    bearer_token = {"Authorization": f"Bearer {user_token}"}
    with open(file_path, "rb") as file:
        file = file.read()    
        response = requests.post(f"{BACKEND_HOSTNAME}{S3_UPLOAD_URI}",
                             headers=bearer_token, 
                             files={"file": (file_name, file)}
                             )
    return response.json()