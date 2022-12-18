import os
import datetime
from dataclasses import dataclass

import jwt
from flask import Flask, request
from flask_mysqldb import MySQL

# __name__ -> "__main__"
server = Flask(__name__)
mysql = MySQL(server)

# CONFIG
# This will print None first, then "localhost" after running export MYSQL_HOST=localhost in terminal
# print(f"server.config['MYSQL_HOST']: {server.config.get('MYSQL_HOST')}")
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

PORT = 5050


@dataclass
class AccessToken:
    username: str
    exp: datetime
    iat: datetime
    admin: bool


class AuthResponse:
    MISSING_CREDENTIALS = ("missing credentials", 401)
    INVALID_CREDENTIALS = ("invalid credentials", 401)
    NOT_AUTHORIZED = ("not authorized", 403)


@server.route("/", methods=["GET"])
def test():
    return f"[{datetime.datetime.now()}] auth server running on port: {PORT}", 200


@server.route("/login", methods=["POST"])
def login():
    # parse authorization header from the request and create an auth object
    auth = request.authorization
    if not auth:
        return AuthResponse.MISSING_CREDENTIALS

    # check db  for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return AuthResponse.INVALID_CREDENTIALS
        else:
            return create_jwt(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return AuthResponse.INVALID_CREDENTIALS


def create_jwt(username: str, secret: str, is_admin=False):
    token = AccessToken(
        username=username,
        exp=datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(days=1),
        iat=datetime.datetime.utcnow(),
        admin=is_admin,
    )
    return jwt.encode(
        token.__dict__,
        secret,
        algorithm="HS256",
    )


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return AuthResponse.INVALID_CREDENTIALS

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET", algorithm=["HS256"])
        )
    except Exception:
        return AuthResponse.NOT_AUTHORIZED

    return decoded, 200


if __name__ == "__main__":
    # Server will listen to any ip address on the host
    # Without this, host will default to localhost (physical machine).
    # This server will be running inside a docker container
    # but the container(host) address is decided when it's being spined up
    # that's why we are not using a static address here.
    # You can also create a docker network and assign a static ip address within the network
    server.run(host="0.0.0.0", port=PORT)
