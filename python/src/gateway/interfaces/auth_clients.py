import os
import requests
from flask import Request


# TODO: put this in a common lib
class AuthResponse:
    MISSING_CREDENTIALS = ("missing credentials", 401)
    INVALID_CREDENTIALS = ("invalid credentials", 401)
    NOT_AUTHORIZED = ("not authorized", 403)


def login(request: Request):
    auth = request.authorization
    if not auth:
        return None, AuthResponse.MISSING_CREDENTIALS

    basic_auth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/login", auth=basic_auth
    )

    if response.status_code == 200:
        return response.message, None
    else:
        return None, (response.message, response.status_code)


def validate_token(request: Request):
    if "Authorization" not in request.headers:
        return None, AuthResponse.MISSING_CREDENTIALS

    token = request.headers["Authorization"]

    if not token:
        return None, AuthResponse.MISSING_CREDENTIALS

    response = requests.post(
        f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.token, None
    else:
        return None, (response.message, response.status_code)
