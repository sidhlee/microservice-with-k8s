import pika
from pika.adapters.blocking_connection import BlockingChannel
import sys
import os
import time
import gridfs
from pymongo import MongoClient
from services import to_mp3


def main():
    # mongodb host is on local machine, not deployed in our cluster.
    # minikube.internal gives access to host system's local environment
    client = MongoClient("host.minikube.internal", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq connection
    connection = pika.BlockingConnection(
        # "rabbitmq" will resolve to the host ip address of the service "rabbitmq"
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    def callback(channel: BlockingChannel, method, properties, body):
        error = to_mp3.start(body, fs_videos, fs_mp3s, channel)
        if error:
            # negative acknowledgement is made for the message identified with the delivery tag
            # so that the message can be retried
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. TO exit press CTRL+C")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # gracefully shutdown on keyboard interrupt
        print("Interrupted")
        try:
            # exit from python by raising SystemExit
            sys.exit(0)
        except SystemExit:
            # exit the child process immediately
            os._exit(0)
