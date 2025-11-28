import requests
import webbrowser

BACKEND_HOSTNAME = "http://localhost:8000/"
URI = "api/v1/login"


def user_login():
    webbrowser.open(f"{BACKEND_HOSTNAME}{URI}")
