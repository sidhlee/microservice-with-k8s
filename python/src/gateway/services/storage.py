import pika
from pika.spec import PERSISTENT_DELIVERY_MODE
import json
from gridfs import GridFS
from pika.adapters.blocking_connection import BlockingChannel
from server import AccessToken


def queue_upload_video(file, fs: GridFS, channel: BlockingChannel, token: AccessToken):
    '''
    Put the video file in MongoDB and publish a message to the queue
    '''
    try:
        file_id = fs.put(file)
    except Exception:
        return "internal server error", 500

    message = {
        "video_file_id": str(file_id),
        "mp3_file_id": None,
        "username": token.username,
    }

    try:
        channel.basic_publish(
            # Be passing an empty exchange name, each queue gets bound to the default exchange
            # with the queue name being the routing key
            exchange="",
            # You will need to add a new queue named "video"
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # Durable message - persist message in the queue in case of pod failure
                delivery_mode=PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception:
        # rollback uploaded image because downstream service will not be able to process them
        fs.delete(file_id)
        return "internal server error", 500
