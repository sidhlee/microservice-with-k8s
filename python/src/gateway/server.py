import os
import datetime
import json
from dataclasses import dataclass

import gridfs
import pika
from flask import Flask, request
from flask_pymongo import PyMongo

from interfaces import auth_clients
from services import storage


# TODO: this is copied from auth.server.py. Make a separate package.
@dataclass
class AccessToken:
    username: str
    exp: datetime
    iat: datetime
    admin: bool


server = Flask(__name__)
server.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(server)

# GridFS can be s3 replacement that makes it easier
# to replicate production environment
# MongoDB has a default size limit for BSON document (16MB)
# but GridFS divides files into 256kB "chunks" and
# stores them in 2 collections(tables): one for chunks and
# the other for metadata
fs = gridfs.GridFS(mongo.db)

# synchronous communication with rabbitMQ
# Queue will be deployed as a "stateful set" in our kubernetes cluster
# , accessible by "rabbitmq" label passed here.
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    """
    Communicate with auth service to authenticate the user
    (validate the credentials)
    and return JWT to the client.
    """
    # The request is from Flask
    token, err = auth_clients.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    decoded_jwt, err = auth_clients.validate_token(request)

    decoded_jwt_dict = json.loads(decoded_jwt)
    token = AccessToken(**decoded_jwt_dict)

    if decoded_jwt_dict["admin"]:
        if len(request.files) > 1:
            return "only 1 file can be uploaded", 400
        if len(request.files) == 0:
            return "request does not contain a file to upload", 400

        # This loop only runs once (for now)
        for file in request.files.values():
            err = storage.queue_upload_video(file, fs, channel, token)

            if err:
                return err

        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
